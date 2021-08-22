# class Field(Rule):
#     def __init__(self, condition, action, prm):
#         Rule.__init__(self, condition, action, prm)
#         self.field_name = prm
#
#     def _pre_check_parse(self, data_state):
#         """
#         Extracts the field_value from the given data_state {self.field_name : field_value}
#         :param data_state: dict {field_name : field_value}
#         :return: field_value - data for condition.check(data1, data2)
#         """
#         return data_state.get(self.field_name, None) if data_state is not None else None
#
#
# class CountEntries(Rule):
#     def __init__(self, condition, action, prm):
#         Rule.__init__(self, condition, action, prm)
#         # self.field_name = prm
#
#     def _pre_check_parse(self, data_state):
#         return len(data_state)
