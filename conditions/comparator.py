import collections

from conditions.comparable import Comparable, comparable_value
from conditions.evaluable import Evaluable
from hamato_yoshi_types import YamlKey, YamlValue, YamlValueComparator
from snapshot_data import SnapshotData


class Comparator(Evaluable):
    """Abstract class for comparison operators like Less, Equals, In, etc."""

    def __init__(self, x: Comparable, y: Comparable):
        self.x: Comparable = x
        self.y: Comparable = y

    def evaluate(self, snapshot_data: SnapshotData) -> bool:
        x_value = self.x.get_value(snapshot_data)
        y_value = self.y.get_value(snapshot_data)
        try:
            return self._evaluate(x_value, y_value)
        except TypeError as e:
            print(f"Can't compare <{x_value}> of type {type(x_value)} with <{y_value}> of type {type(y_value)}.")
            return False

    def _evaluate(self, a, b) -> bool:
        raise NotImplemented


class Diff(Comparator):
    def _evaluate(self, a, b) -> bool:
        # TODO: check if changes in permissions in the new parser invokes something
        return a != b


class Less(Comparator):
    def _evaluate(self, a, b) -> bool:
        return a < b


class Equals(Comparator):
    def _evaluate(self, a, b) -> bool:
        if isinstance(a, list or set) and isinstance(b, list or set):
            return collections.Counter(a) == collections.Counter(b)
        else:
            return a == b


class Contains(Comparator):
    def _evaluate(self, a, b) -> bool:
        return set(b).issubset(set(a))


class NotEquals(Comparator):
    def _evaluate(self, a, b) -> bool:
        return a != b


class Greater(Comparator):
    def _evaluate(self, a, b) -> bool:
        return a > b


class LessEq(Comparator):
    def _evaluate(self, a, b) -> bool:
        return a <= b


# BOOLEAN_OPERATORS: dict[YamlValueComparator, type(Comparator)] = {
BOOLEAN_OPERATORS = {
    'Equals': Equals,
    'NotEquals': NotEquals,
    'Less': Less,
    'Greater': Greater,
    'LessEq': LessEq,
    'Contains': Contains,
    'Diff': Diff
}


def comparator_factory(comparator_name: YamlValueComparator, x: YamlValue, y: YamlValue) -> Comparator:
    comparable_x = comparable_value(x)
    comparable_y = comparable_value(y) if y else comparable_value(x, stored=True)
    comparator_class: type(Comparator) = BOOLEAN_OPERATORS[comparator_name]
    comparator = comparator_class(comparable_x, comparable_y)
    return comparator
