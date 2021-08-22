from snapshot_data import SnapshotData


class Evaluable:
    """
    Abstract class for evaluable boolean expression.
    """

    def evaluate(self, snapshot_data: SnapshotData) -> bool:
        raise NotImplemented
