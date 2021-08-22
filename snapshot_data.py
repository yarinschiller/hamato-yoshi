from typing import List

from hamato_yoshi_types import ParsersStates, ParserName, YamlValue, YamlValueField, ParserSubState


func_dict = {
    None: lambda x: x,
    "Count": lambda x: len(x),
}


def _decompose_yaml_value(yaml_value: YamlValue):
    """
    static function that takes a path (e.g 'Count(Maps.sofiles)' or 'Meminfo.Memtotal' or 'FD') and decompose it to
    func name, parser name and fields list (if each one of them is available, if one of them is missing,
     the returned value will be None)
    :param yaml_value: path to decompose
    :return: triplet of three values - func_name, parser_name, fields
    """
    func_name = None
    parser_name: ParserName = yaml_value
    fields: List[YamlValueField] = list()

    split_path = yaml_value.split('(')
    if len(split_path) == 2:
        func_name = split_path[0]
        yaml_value = split_path[1][:-1]
    split_path = yaml_value.split('.')
    parser_name = split_path[0]
    if len(split_path) >= 2:
        fields = split_path[1:]
    return func_name, parser_name, fields


def _extract_fields_from_parser_sub_state(parser_name: ParserName, parser_sub_state: ParserSubState,
                                          yaml_value_fields: List[YamlValueField]):
    """
    Gets parser_sub_state (parser current/stored state which is a dictionary) and extracts recursively value from
     it by the given fields list.
    :param yaml_value_fields: A list of fields to extract from the given parser_sub_state.
    :param parser_sub_state: The state to extract fields from.
    :return: The extracted fields from the parser_sub_state.
    """
    for yaml_value_field in yaml_value_fields:
        if type(parser_sub_state) is not ParserSubState or yaml_value_field not in parser_sub_state.keys():
            print(f"Parser '{parser_name}' have no field named '{yaml_value_field}'")
        else:
            parser_name += '.' + yaml_value_field
            parser_sub_state = parser_sub_state.get(yaml_value_field)
    return parser_sub_state


class SnapshotData:
    """interface for extracting a snapshot value of a given path (either current or stored)"""

    def __init__(self):
        self.parsers_states: ParsersStates = ParsersStates()

    def _get_yaml_value(self, yaml_value: YamlValue, current_flag=True):
        func_name, parser_name, yaml_value_fields = _decompose_yaml_value(yaml_value)

        parser_state = self.parsers_states[parser_name]
        parser_state = parser_state.current if current_flag else parser_state.stored

        data_from_parser = _extract_fields_from_parser_sub_state(parser_name, parser_state, yaml_value_fields)
        data_from_parser = func_dict[func_name](data_from_parser)
        return data_from_parser

    def get_current(self, yaml_value: YamlValue):
        """
        :param yaml_value:
        :return:
        """
        return self._get_yaml_value(yaml_value, current_flag=True)

    def get_stored(self, yaml_value: YamlValue):
        """
        :param yaml_value:
        :return:
        """
        return self._get_yaml_value(yaml_value, current_flag=False)

    def update_parser_state(self, parser_name: ParserName, new_parser_current_state: ParserSubState):
        """
        Updates the given parser_name parser state to the given current_parser_state
        :param parser_name: the name (key) of the parser to update
        :param new_parser_current_state: the new state to update the parser with
        :return:
        """
        self.parsers_states[parser_name] = new_parser_current_state


if __name__ == '__main__':
    print(_decompose_yaml_value('Count(Meminfo.Memtotal)'))
    print(_decompose_yaml_value('Count(FD)'))
    print(_decompose_yaml_value('Meminfo.Memtotal'))
    print(_decompose_yaml_value('Meminfo'))