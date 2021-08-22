from hamato_yoshi_types import YamlValue, YamlKey
from snapshot_data import SnapshotData


class Comparable:
    """
    Abstract class for comparable values.
    """

    def get_value(self, snapshot_data: SnapshotData):
        raise NotImplemented


class Constant(Comparable):
    def __init__(self, value):
        Comparable.__init__(self)
        self.value = value

    def get_value(self, snapshot_data: SnapshotData):
        """
        Constants ignore the snapshot_data
        """
        return self.value


class SnapshotField(Comparable):
    def __init__(self, yaml_value: YamlValue):
        Comparable.__init__(self)
        self.yaml_value = yaml_value

    def get_value(self, snapshot_data: SnapshotData):
        raise NotImplemented


class SnapshotFieldCurrent(SnapshotField):
    def get_value(self, snapshot_data: SnapshotData):
        return snapshot_data.get_current(self.yaml_value)


class SnapshotFieldStored(SnapshotField):
    def get_value(self, snapshot_data: SnapshotData):
        return snapshot_data.get_stored(self.yaml_value)


def is_snapshot_field(yaml_value: YamlValue):
    "Test if value from the yaml (i.e. 'Meminfo.Meminfo') represents a valid /proc/<path>.field"
    if (isinstance(yaml_value, str)):
        return True


def comparable_value(yaml_value: YamlValue, stored=False) -> Comparable:
    """Wrap value with the most relevant Comparable class"""
    if is_snapshot_field(yaml_value):
        if stored:
            return SnapshotFieldStored(yaml_value)
        else:
            return SnapshotFieldCurrent(yaml_value)
    else:
        return Constant(yaml_value)
