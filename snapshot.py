from hamato_yoshi_types import ParsersObjectsDict, ParserName, ParserSubState, RulesList
from snapshot_data import SnapshotData

PID_IN_PATH_CONST = '{pid}'


class Snapshot:
    """
    Holds a state snapshot of the system according to later given paths, parsers, and rules.
    """

    def __init__(self, parsers_dict: ParsersObjectsDict):
        """
        Constructor.
        """
        # dict of parsers objects {'parser_name': ParserObject(*initialized*)}
        self.parsers_dict = self._my_parsers(parsers_dict)
        # self.parsers_dict = parsers_dict

        # List of rules relevant to the snapshot
        self.rules: RulesList = list()

        # Object of snapshot data that relevant to the snapshot's parsers
        self.snapshot_data = SnapshotData()

    def load_rules(self, rules_list: RulesList):
        """
        Load the given rules list to the snapshot's rules list.
        :param rules_list: The rules to load.
        :return:
        """
        self.rules = rules_list

    def _apply_parse(self, parser_name: ParserName) -> ParserSubState:
        """
        Override to the parse method of the given parser.
        :param parser_name: The parser to parse
        :return: a dict of the parsed data
        """
        # parser = self.parsers_dict.get(parser_name)
        # if PID_IN_PATH_CONST in parser.path:
        #     print("PID parser in System!")
        return self.parsers_dict.get(parser_name).parse()

    def _my_parsers(self, parsers_dict: ParsersObjectsDict):
        """
        Extracts the parsers that relevant to the system snapshot.
        :param parsers_dict: All available parsers
        :return: Parsers dict that relevant to system snapshot.
        """
        my_parsers = dict()
        for parser_name, parser_object in parsers_dict.items():
            if PID_IN_PATH_CONST not in parser_object.path:
                my_parsers[parser_name] = parser_object
        return my_parsers

    def take(self):
        """
        for each parser, update state and than run all relevant rules.
        """
        # Iterate over relevant parsers and update their states in the snapshot_data object
        for parser_name in self.parsers_dict.keys():
            self.snapshot_data.update_parser_state(parser_name, self._apply_parse(parser_name))

        # Iterate over relevant rules and run them
        for rule in self.rules:
            rule.run(self.snapshot_data)


class ProcSnapshot(Snapshot):
    """
    A snapshot for specific /proc/<pid>
    """

    def __init__(self, pid: int, parsers_dict: ParsersObjectsDict):
        """
        Constructor.
        :param pid: /proc/<pid> to snap
        """
        Snapshot.__init__(self, parsers_dict)
        self.parsers_dict = parsers_dict  # all available parsers are relevant to proc_snapshot object
        self.pid: int = pid

    def _apply_parse(self, parser_name: ParserName) -> ParserSubState:
        return self.parsers_dict.get(parser_name).parse(self.pid)

    def killed(self):
        print(f"ProcSnapshot({self.pid}) killed")
