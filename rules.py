from actions import Action
# from conditions.conditions import Evaluable  NOTE: creates circular import problem!


class Rule:
    """
    The default Rule. Checks a condition, if holds - performs an action.
    """
    def __init__(self, condition, action: Action, prm=None):
        """
        Constructor.
        :param condition: A condition object. (see conditions.py)
        :param action: An action object. (see actions.py)
        :param prm: Parameters for this rule.
        """
        self.condition = condition
        self.action = action
        self.prm = prm

    def run(self, snapshot_data):
        """
        Executes the rule. Apply pre_check_parse to cur and last states, and if the condition holds on them -
        run the given action.
        :param snapshot_data:
        :param last_state: Result from a Parser.parse() method.
        :param cur_state: Result from a Parser.parse() method.
        :return: True if action performed, False otherwise.
        """
        if self.condition.evaluate(snapshot_data):
            # log it
            # print("LS: * CS: * R: %s C: %s A: %s - executed", str(self), str(self.condition), str(self.action))
            self.action.run(self.condition)
            return True
        return False
