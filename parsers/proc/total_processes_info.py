import parsers
from utils import get_pid_list


class TotalProcessesInfo(parsers.Default):
    def __init__(self, path='/proc'):
        parsers.Default.__init__(self, path)

    def _parse(self):
        pid_list = get_pid_list()
        result = dict(PPID=dict(),)
        for pid in pid_list:
            with open(f"/proc/{pid}/stat", 'r') as f:
                fields = f.read().split()
                ppid = fields[3]
                if ppid not in result["PPID"]:
                    result["PPID"][ppid] = [pid]
                else:
                    result["PPID"][ppid].append(pid)
        return result