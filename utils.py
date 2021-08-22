import os
from collections import defaultdict
import yaml


def load_yaml_file_to_dict(rules_file_path: str) -> defaultdict:
    """
    Static function that loads the given YAML file path to a dict and returns it
    :param rules_file_path: A path to YAML rules file.
    :return: dict of the YAML file content
    """
    yaml_dict = defaultdict(dict)
    with open(rules_file_path, 'r') as f:
        yaml_dict.update(yaml.load(f, Loader=yaml.FullLoader))
    return yaml_dict


def get_pid_list():
    return [int(e) for e in os.listdir("/proc/") if e.isdigit() and os.path.isdir(os.path.join("/proc", e))]


def get_exe_cmdline(pid):
    """
    Extract the exe and cmdline parameters for a given PID.
    Used to identify the process in the rules.
    Example:
    $ python3 -c 'while(True): print(1)'
    $ ps -le
    $ F S   UID   PID  PPID  C PRI  NI ADDR SZ  WCHAN TTY          TIME CMD
    $ ...
    $ 0 S  1000  9054  9039  2  80   0 -  5293      - tty3     00:00:00 python3
    $ ls -l /proc/9054/exe
    $ lrwxrwxrwx 1 cyber cyber 0 Jul 28 15:49 /proc/9054/exe -> /usr/bin/python3.9
    $ ls -l /proc/9054/cmdline
    $ -r--r--r-- 1 cyber cyber 0 Jul 28 15:49 /proc/9054/cmdline
    $ cat /proc/9054/cmdline
    $ python3-cwhile(True): print(1)
    Returns: ('/usr/bin/python3.9', 'python3-cwhile(True): print(1)')
    :param pid: PID
    :return: (exe, cmdline)
    """
    try:
        exe_path = os.readlink(f"/proc/{pid}/exe")
        # read and parse cmdline
        # (argument list null terminated and null separated -> space separated and remove last null)
        cmdline = open(f"/proc/{pid}/cmdline", "r").read().replace('\0', ' ')[:-1]
        return exe_path, cmdline
    except:
        return None, None


def get_processes_dict():
    result = dict()
    p_list = get_pid_list()
    for pid in p_list:
        exe_path, cmdline = get_exe_cmdline(pid)
        if exe_path is None and cmdline is None:
            print(f"Skipping PID: {pid}")
            continue
        # print(cmdline)
        if exe_path not in result:
            result[exe_path] = {cmdline: [pid]}
            continue
        if cmdline not in result[exe_path]:
            result[exe_path][cmdline] = [pid]
            continue
        result[exe_path][cmdline].append(pid)
    return result


def all_proc_exe(exe, processes_dict=None):
    if not processes_dict:
        processes_dict = get_processes_dict()
    result = list()
    for pid_list in processes_dict.get(exe, dict()).values():
        result += pid_list
    return result


def get_sub_classes_of_object_recursively(root_object) -> dict:
    """
    returns a list of the subclasses of a given object
    :param root_object: The object to get subclasses from
    :return: List of the available subclasses of the given object
    """
    subclasses = {}
    for subclass in root_object.__subclasses__():
        subclasses[str(subclass).split('.')[-1][:-2]] = subclass
        recursive_subclasses = get_sub_classes_of_object_recursively(subclass)
        subclasses.update(recursive_subclasses)
    return subclasses


def convert_dict_values_to_lists_recursively(dict_to_convert: dict):
    """
    :param dict_to_convert:
    :return:
    """
    for key, value in dict_to_convert.items():
        if type(value) is dict:
            convert_dict_values_to_lists_recursively(value)
        elif type(value) is not list:
            dict_to_convert[key] = [value]


def unite_dicts_with_lists_values(dict1: dict, dict2: dict):
    """

    :param dict1:
    :param dict2:
    :return:
    """
    for key, value in dict2.items():
        if key not in dict1.keys():
            dict1[key] = dict2[key]
        else:
            if type(value) is dict:
                unite_dicts_with_lists_values(dict1[key], dict2[key])
            elif type(value) is list:
                dict1[key] = value + dict2[key]