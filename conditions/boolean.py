import operator

from conditions.evaluable import Evaluable
from hamato_yoshi_types import YamlKey
from snapshot_data import SnapshotData


class BooleanLogic(Evaluable):
    "Abstract class for evaluating boolean logic using 'and', 'or' and 'not' operators."

    def __init__(self, x: Evaluable, y: Evaluable = None):
        self.x = x
        if y is not None:
            self.y = y

    def evaluate(self, snapshot_data: SnapshotData) -> bool:
        raise NotImplemented


class BooleanLogicBinary(BooleanLogic):
    "Class for evaluating binary boolean terms like AND(x,y), OR(x,y)"

    def __init__(self, x: Evaluable, y: Evaluable, logic_operator):
        super().__init__(x, y)
        self.logic_operator = logic_operator

    def evaluate(self, snapshot_data: SnapshotData) -> bool:
        left = self.x.evaluate(snapshot_data)
        right = self.y.evaluate(snapshot_data)
        return self.logic_operator(left, right)


class BooleanLogicUnary(BooleanLogic):
    "Class for evaluating unary boolean terms like NOT(x), TRUTH(x)"

    def __init__(self, x: Evaluable, logic_operator):
        super().__init__(x)
        self.logic_operator = logic_operator

    def evaluate(self, snapshot_data: SnapshotData) -> bool:
        left = self.x.evaluate(snapshot_data)
        return self.logic_operator(left)


class Or(BooleanLogicBinary):
    def __init__(self, x: Evaluable, y: Evaluable):
        super().__init__(x, y, operator.or_)


class And(BooleanLogicBinary):
    def __init__(self, x: Evaluable, y: Evaluable):
        super().__init__(x, y, operator.and_)


class Not(BooleanLogicUnary):
    def __init__(self, x: Evaluable):
        super().__init__(x, operator.not_)


BOOLEAN_LOGIC_BINARY = {
    'or': Or,
    'and': And
}
BOOLEAN_LOGIC_UNARY = {
    'not': Not
}

BOOLEAN_LOGIC_CLASSES = {**BOOLEAN_LOGIC_UNARY, **BOOLEAN_LOGIC_BINARY}


def boolean_logic_factory(boolean_logic_name : YamlKey, cond1: Evaluable, cond2: Evaluable) -> BooleanLogic:
    logic_class = BOOLEAN_LOGIC_CLASSES[boolean_logic_name]
    if cond2:
        return logic_class(cond1, cond2)
    else:
        return logic_class(cond1)
