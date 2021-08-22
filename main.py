from time import sleep

from rich.live import Live

from dashboard import make_dashboard, refresh_dashboard
from snapshot import ProcSnapshot, Snapshot
from copy import deepcopy
import inspect

from utils import *
from typing import Tuple
import conditions.conditions as cnd
import parsers
import parsers.proc
import parsers.proc.PID
import rules
import actions as act
import parsers.proc.meminfo
import parsers.proc.vmstat
import parsers.proc.mounts
import parsers.proc.PID.fd
import parsers.proc.PID.fdinfo
import parsers.proc.PID.maps
import parsers.proc.PID.mountinfo
import parsers.proc.PID.mountspid
import parsers.proc.PID.status
import parsers.proc.total_processes_info
from hamato_yoshi_types import ParsersObjectsDict


# YAML_FILE = 'rules_new.yaml'
# YAML_FILE = 'rules_test.yaml'
YAML_FILE = 'rules_demo.yaml'


def get_parsers_classes() -> dict:
    """
    Returns the classes of all available parser (not core parsers like REGEX/DIR/BASE!).
    :return: ^
    """
    parsers_classes = get_sub_classes_of_object_recursively(parsers.SnapshotParser)

    # Delete parsers that cannot be initialized directly
    for name, obj in inspect.getmembers(parsers):
        if type(obj) == type(parsers.SnapshotParser):
            parsers_classes.pop(name, '')

    # Initiate each parser object (Doesn't happen before to prevent initialization of parsers the cannot be initialized)
    for parser_name, parser_object in parsers_classes.items():
        parsers_classes[parser_name] = parser_object()
    return parsers_classes


def load_yaml_to_rules_and_parsers(rules_file_path: str) -> Tuple[dict, ParsersObjectsDict]:
    """
    Load the YAML file to a dictionary, gets the rules from the file and create a dictionary of the parsers from the
    file.
    :param rules_file_path:
    :return: Dict of rules and parsers (parsers objects)
    """
    yaml_dict = load_yaml_file_to_dict(rules_file_path)
    parsers_dict = deepcopy(yaml_dict['parsers'])
    for section in {'conditions', 'rules_catalogue', 'parsers'}:
        if section in yaml_dict:
            yaml_dict.pop(section)

    active_rules_dict = yaml_dict

    # Changes the parsers descriptions to parsers objects, loads parsers from yaml to parsers dict
    for parser, parser_description in parsers_dict.items():
        parsers_dict[parser] = \
            getattr(parsers, parser_description.pop('class', ''), parsers.Default)(**parser_description)

    parsers_dict.update(get_parsers_classes())  # loads built in available parsers to parsers dict
    return active_rules_dict, parsers_dict


def convert_rules_dicts_to_rules_objects(rule_dicts_list: list) -> list:
    """
    Gets a list of dicts that (each dict) describes rule of the following format:
      '{
        'condition':      condition_dict
        'action':         Action_string
        'action_prm (optional)': action_prm_string
        }'
    and returns a list of objects of Rule.
    :param rule_dicts_list: The rule dict to convert to rule object.
    :return: Rule object (from rules.py file)
    """
    rules_objects_list = []
    for rule_dict in rule_dicts_list:
        condition = cnd.get_evaluable(rule_dict.get('condition', None))
        action_class = getattr(act, rule_dict.get('action', None), act.Action)
        action_prm = rule_dict.get('action_prm', None)
        action = action_class(action_prm)
        rule = rules.Rule(condition, action)
        rules_objects_list.append(rule)
    return rules_objects_list


class LoadConfig:
    def __init__(self, rules_dict: dict):
        self.rules_dict = rules_dict

    def load_rules_to_snapshot(self, rules_dicts_list: list, snapshot: Snapshot):
        """
        Loads rules from given rules_dict to given snapshot object using the "_load_rule" method.
        :param rules_dicts_list: list of rules to load to the given snapshot
        :param snapshot: snapshot to load rules to
        :return:
        """
        rules_objects_list = convert_rules_dicts_to_rules_objects(rules_dicts_list)
        # TODO: Print when new rule added, currently not possible.No API for condition in rule.
        print(rules_dicts_list)
        snapshot.load_rules(rules_objects_list)

    def load_system_rules(self, snapshot: Snapshot):
        """
        Loads system rules from the YAML file to the given snapshot
        :param snapshot: The snapshot to load the "system rules" to
        :return:
        """
        self.load_rules_to_snapshot(self.rules_dict["system_rules"], snapshot)

    def get_rules_for_pid(self, pid: int):
        """
        Get the ruled that are relevant to the given pid.
        :param pid: Look for the rules for this pid.
        :return: list of rules for the given pid.
        """
        pid_exe, pid_cmdline = get_exe_cmdline(pid)
        pid_rules_dict = self.rules_dict.get(pid_exe, dict())
        if pid_rules_dict:
            exe_rules = pid_rules_dict.get("rules", list())
            cmdline_rules = pid_rules_dict.get(pid_cmdline, list())
            return exe_rules + cmdline_rules
        return list()


def at_first_only(first, second):
    return [x for x in first if x not in second]


class PsListMonitor:
    """
    Responsible to update the given snapshot_dict with who is alive/dead.
    Use its 'update()' function in a loop to iteratively update the given snapshot_dict.
    """

    def __init__(self, load_rules: LoadConfig, snapshot_dict: dict, parsers_dict: dict):
        """
        Constructor.
        :param load_rules: An already initialized LoadRules object
        :param snapshot_dict: A dict of {pid : snapshot object}, with one entry {'*system*' : system snapshot}
        :param parsers_dict: A dict of all available parsers {'parser_name': ParserObject}
        """
        self.ps_list = list()
        self.load_rules = load_rules
        self.snapshot_dict = snapshot_dict
        self.parsers_dict = parsers_dict

    def update(self):
        """
        Updates the list pids based on who is currently alive/dead.
        New living pids are added, and new deaths are popped.
        """
        cur_ps_list = get_pid_list()
        if self.ps_list != cur_ps_list:
            ps_killed = at_first_only(self.ps_list, cur_ps_list)
            ps_new = at_first_only(cur_ps_list, self.ps_list)
            self.ps_list = cur_ps_list
            for pid in ps_killed:
                if pid in self.snapshot_dict:
                    self.snapshot_dict.pop(pid).killed()
            for pid in ps_new:
                rules_for_pid = self.load_rules.get_rules_for_pid(pid)
                if rules_for_pid:
                    new_proc_snapshot = ProcSnapshot(pid, self.parsers_dict)
                    self.load_rules.load_rules_to_snapshot(rules_for_pid, new_proc_snapshot)
                    self.snapshot_dict[pid] = new_proc_snapshot


def main():
    freq_time = 0.3
    parsers_dict: ParsersObjectsDict
    rules_dict: dict

    # load yaml file
    rules_dict, parsers_dict = load_yaml_to_rules_and_parsers(rules_file_path=YAML_FILE)

    # init
    load_config = LoadConfig(rules_dict)

    # A dict collecting a snapshot of the system + a snapshot per each process
    snapshot_dict = {"*system*": Snapshot(parsers_dict)}

    # Apply the rules on the system's snapshot (load these rules into the snapshot object)
    load_config.load_system_rules(snapshot_dict["*system*"])

    # Create a monitoring object to continuously discover new/dead processes and load rules to their snapshots
    ps_list_monitor = PsListMonitor(load_config, snapshot_dict, parsers_dict)

    # Forever: take new snapshots and update
    dashboard = make_dashboard()
    with Live(dashboard, auto_refresh=False, screen=True):
        while True:
            # check for new or killed processes, modify snapshot_dict accordingly.
            ps_list_monitor.update()

            # take snapshot
            for snapshot in snapshot_dict.values():
                snapshot.take()
                # TODO: make it to smart sleep

            # refresh dashboard
            refresh_dashboard(dashboard)

            # sleep
            sleep(freq_time)


if __name__ == '__main__':
    main()
