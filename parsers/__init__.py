import inspect
import os
import re

import parsers
from utils import get_pid_list, get_sub_classes_of_object_recursively,\
    convert_dict_values_to_lists_recursively, unite_dicts_with_lists_values


class SnapshotParser:
    "Abstract class for parsing snapshot data from some system path"

    def __init__(self, path):
        self.original_path = path  # always stores the pre-formatted path to reformat later.
        self.path = path

    def _parse(self):
        raise NotImplemented

    def parse(self, *kwargs):
        self._format_path(*kwargs)
        result = dict()
        try:
            result.update(self._parse())
        except Exception as e:
            # raise
            result.update(exception=str(e), type=type(e))

        return result

    def _format_path(self, *args):
        """
        Replace the given kwargs with the '{*}' in the value of path (input = 3, 5, path == "/x/{pid}/z/{tid}/r..."
         --> path == "/x/3/z/5/r...")
        :param args: arguments to format into the path.
        """
        self.path = self.original_path
        if args:
            self.path = re.sub('{[^{}]*}', '{}', self.path)

            # counts number of '{}' in the given sub parsed path
            num_of_parentheses = self.path.count('{}')

            # if there are too many parentheses in the path, remove the redundant ones.
            if num_of_parentheses > len(args):
                # splits according to the first len(args) '{}' appearances to save them for the later format.
                split_path = self.path.split('{}', len(args))

                # reset path.
                self.path = ''

                # adds all relevant parentheses back to the path.
                for i in range(len(args)):
                    self.path += split_path[i] + '{}'

                # remove redundant parentheses.
                self.path += re.sub('{}', '', split_path[len(args)])

            # format the path according to given args.
            self.path = self.path.format(*args)


class Default(SnapshotParser):
    def __init__(self, path):
        SnapshotParser.__init__(self, path)

    def _parse(self):
        result = dict(stat=os.stat(self.path))
        if os.path.islink(self.path):
            result.update(type="link", link=os.readlink(self.path))
        if os.path.isfile(self.path):
            result.update(type="file", content=open(self.path, 'rb').read())
        if os.path.isdir(self.path):
            result.update(type="dir", listdir=os.listdir(self.path))

        return result


class Regex(SnapshotParser):
    def __init__(self, path, regex_string):
        SnapshotParser.__init__(self, path)
        self.regex = re.compile(regex_string)

    def _run_regex(self, data, instance_index=0):
        return dict(data=self.regex.findall(data)[instance_index])

    def _parse(self):
        data = open(self.path, "rb").read().decode('utf-8')
        result = self._run_regex(data)
        return result


class ForEachPID(SnapshotParser):
    def __init__(self, pid_parser_class_name: str):
        SnapshotParser.__init__(self, '/proc')
        self.pid_parser = None
        for parser_name, parser_object in get_sub_classes_of_object_recursively(parsers.SnapshotParser).items():
            if parser_name == pid_parser_class_name:
                self.pid_parser = parser_object()
                break

    def _parse(self):
        pid_list = get_pid_list()
        result = dict()
        for pid in pid_list:
            pid_result = self.pid_parser.parse(pid)
            convert_dict_values_to_lists_recursively(pid_result)
            # for key in pid_result.keys():
            #     if key != 'exception':
            #         if key not in result.keys():
            #             result[key] = list()
            #         result[key].append(pid_result[key])
            unite_dicts_with_lists_values(result, pid_result)
        return result


class Dir(SnapshotParser):
    def _entry_parse(self, e):
        return os.path.join(self.path, e)

    def _parse(self):
        result = dict()
        if os.path.isdir(self.path):
            listdir = os.listdir(self.path)
            result.update({e: self._entry_parse(e) for e in listdir})
        else:
            result.update(error="%s is not a dir" % (self.path,))
        return result


def extract_field(snapshot_data, field_name):
    """
    Extracts the field_value from the given snaphot_data {self.field_name : field_value}
    :param snapshot_data: dict {field_name : field_value}
    :return: field_value - data for BooleanOperator.evaluate(data1, data2)
    """
    snapshot_data.get(field_name, None) if snapshot_data is not None else None


def count_entries(snapshot_data):
    """
    Returns the number of entries in the given snapshot_data {self.field_name : field_value}
    """
    return len(snapshot_data)


def test_parser(path, parser_class):
    import json
    p = parser_class(path)
    result = p.parse()
    print(json.dumps(result, indent=True))
