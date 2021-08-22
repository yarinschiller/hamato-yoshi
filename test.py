from pprint import pprint

from conditions.conditions import get_evaluable
from main import load_yaml_file_to_dict
from snapshot_data import SnapshotData


def main():
    conditions_dict = load_yaml_file_to_dict('rules_new.yaml')
    for rule_name, rule_body in conditions_dict['rules'].items():
        conditions_dict = rule_body['condition']
        pprint(conditions_dict)
        snapshot_evaluator = get_evaluable(conditions_dict)
        snapshot_data = SnapshotData()
        print(snapshot_evaluator.evaluate(snapshot_data))
        pprint(snapshot_evaluator)

if __name__ == '__main__':
    main()

