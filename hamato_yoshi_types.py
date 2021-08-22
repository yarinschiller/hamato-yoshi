# A python object representing the contents of a specific path at a specific point in time.
#
# Example:
#   cat /proc/self/status
#   Name:   cat
#   State:  R (running)
#   Tgid:   5452
#   Pid:    5452
#   ...
#
# The state object for this path would look like:
#   {'Name' : 'cat', 'State' : 'R (running)', 'Tgid' : '5452', 'Pid' : '5452'}
#
import typing
from collections import defaultdict
from typing import Dict
from rules import Rule

import rules
# from parsers import SnapshotParser


# A list of rules objects
RulesList = typing.List[Rule]

# A sub state of a parser (current or stored states...)
ParserSubState = dict


class ParserState:
    def __init__(self):
        self._current: ParserSubState = ParserSubState()
        self._stored: ParserSubState = ParserSubState()

    @property
    def current(self):
        return self._current

    @property
    def stored(self):
        return self._stored

    def update(self, new: ParserSubState):
        self._stored = self._current
        self._current = new


# A string holding the absolute path to some /proc/some/important/path (see
Path = str

# Example: Meminfo
ParserName = str

# A dict of parsers objects
ParsersObjectsDict = Dict[ParserName, object]


# <YamlKey>: <YamlValue>  in the yaml file
# Example <YamlKey>: x, y
# Example <YamlValue>: Meminfo.Meminfo, 100000, Count(Maps.sofiles)
YamlKey = str
YamlValue = typing.Union[str, dict]

# Example: 'Less', 'Greater', ...
YamlValueComparator = YamlValue

# A (possibly nested) condition in the yaml file
ConditionsDict = Dict[YamlKey, YamlValue]

# Example Meminfo.Memtotal (so Memtotal is the field of the yaml_value, so that's the yaml_value_field)
YamlValueField = str


# A dictionary translating paths to their current+stored states
class ParsersStates:
    def __init__(self):
        self.parser_states: Dict[ParserName, ParserState] = defaultdict(ParserState)

    def __getitem__(self, parser_name: ParserName):
        return self.parser_states[parser_name]

    def __setitem__(self, parser_name: ParserName, new_parser_state: dict):
        self.parser_states[parser_name].update(new_parser_state)
