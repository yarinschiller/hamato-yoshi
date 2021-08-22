"""
See parsers/proc/mounts.py

As far as I can understand, /proc/<pid>/mounts does exactly the same as /proc/mounts.
- Mr. Black
"""
from parsers import test_parser
import parsers.proc.mounts


class MountsPID(parsers.proc.mounts.Mounts):
    def __init__(self, path='proc/{pid}/mounts'):
        parsers.proc.mounts.Mounts.__init__(self, path)


if __name__ == '__main__':
    test_parser('/proc/7531/mounts', MountsPID)
