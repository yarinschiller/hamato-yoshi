# from conditions.evaluable import Evaluable  NOTE: creates circular import problem!
from dashboard import log_hamato_yoshi, SubjectName


class Action:
    def __init__(self, *args, **kwargs):
        pass

    def run(self, condition):
        print(f"Action! condition:\n {condition}")

        # diff = DeepDiff(last_state, cur_state)
        # print(diff.to_dict())


class LogCurrent(Action):
    def __init__(self, format_string):
        Action.__init__(self)
        self.format_string = format_string


class LogToDashboard(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subject_name = args[0]["subject_name"]
        self.title = args[0]["title"]
        self.message = args[0]["message"]

    def run(self, condition):
        print("Logging to dashboard!")
        log_hamato_yoshi(self.subject_name,
                         self.title,
                         self.message)
