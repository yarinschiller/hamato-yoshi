"""
Table 1-1: Process specific entries in /proc
..............................................................................
 File		Content
 ...       ...
 fd		Directory, which contains all file descriptors
"""
import os

from parsers import Dir


class FD(Dir):
    def __init__(self, path='/proc/{pid}/fd'):
        Dir.__init__(self, path)

    def _entry_parse(self, e):
        return os.readlink(os.path.join(self.path, e))
