from typing import Dict

from conditions.boolean import BOOLEAN_LOGIC_CLASSES, boolean_logic_factory
from conditions.comparator import comparator_factory
from conditions.evaluable import Evaluable
from hamato_yoshi_types import ConditionsDict, YamlValueComparator


def get_evaluable(condition_dict: ConditionsDict) -> Evaluable:
    key = list(condition_dict.keys())[0]
    if key in BOOLEAN_LOGIC_CLASSES:  # or, and, not
        cond1 = get_evaluable(condition_dict[key]['cond1'])
        cond2 = None
        if 'cond2' in condition_dict[key]:
            cond2 = get_evaluable(condition_dict[key]['cond2'])
        return boolean_logic_factory(key, cond1, cond2)  # x OR y
    else:  # Less, Equals, Greater, ...
        comparator_name: YamlValueComparator = condition_dict['op']
        x = condition_dict['x']
        y = condition_dict.get('y', None)
        return comparator_factory(comparator_name, x, y)  # x < y
