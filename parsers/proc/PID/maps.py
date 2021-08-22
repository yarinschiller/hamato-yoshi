"""
The /proc/PID/maps file contains the currently mapped memory regions and
their access permissions.

The format is:

address           perms offset  dev   inode      pathname

08048000-08049000 r-xp 00000000 03:00 8312       /opt/test
08049000-0804a000 rw-p 00001000 03:00 8312       /opt/test
0804a000-0806b000 rw-p 00000000 00:00 0          [heap]
a7cb1000-a7cb2000 ---p 00000000 00:00 0
a7cb2000-a7eb2000 rw-p 00000000 00:00 0
a7eb2000-a7eb3000 ---p 00000000 00:00 0
a7eb3000-a7ed5000 rw-p 00000000 00:00 0
a7ed5000-a8008000 r-xp 00000000 03:00 4222       /lib/libc.so.6
a8008000-a800a000 r--p 00133000 03:00 4222       /lib/libc.so.6
a800a000-a800b000 rw-p 00135000 03:00 4222       /lib/libc.so.6
a800b000-a800e000 rw-p 00000000 00:00 0
a800e000-a8022000 r-xp 00000000 03:00 14462      /lib/libpthread.so.0
a8022000-a8023000 r--p 00013000 03:00 14462      /lib/libpthread.so.0
a8023000-a8024000 rw-p 00014000 03:00 14462      /lib/libpthread.so.0
a8024000-a8027000 rw-p 00000000 00:00 0
a8027000-a8043000 r-xp 00000000 03:00 8317       /lib/ld-linux.so.2
a8043000-a8044000 r--p 0001b000 03:00 8317       /lib/ld-linux.so.2
a8044000-a8045000 rw-p 0001c000 03:00 8317       /lib/ld-linux.so.2
aff35000-aff4a000 rw-p 00000000 00:00 0          [stack]
ffffe000-fffff000 r-xp 00000000 00:00 0          [vdso]

where "address" is the address space in the process that it occupies, "perms"
is a set of permissions:

r = read
w = write
x = execute
s = shared
p = private (copy on write)

"offset" is the offset into the mapping, "dev" is the device (major:minor), and
"inode" is the inode  on that device.  0 indicates that  no inode is associated
with the memory region, as the case would be with BSS (uninitialized data).
The "pathname" shows the name associated file for this mapping.  If the mapping
is not associated with a file:

[heap]                   = the heap of the program
[stack]                  = the stack of the main process
[vdso]                   = the "virtual dynamic shared object",
                        the kernel system call handler

or if empty, the mapping is anonymous.
"""
from typing import List

from parsers import SnapshotParser, test_parser


class Maps(SnapshotParser):
    def __init__(self, path='/proc/{pid}/maps'):
        SnapshotParser.__init__(self, path)

    def _parse(self):
        """
        Returns a dict of {addresses: { <address> : {  perms : <value>,
                                        offset : <value>,
                                        dev : <value>,
                                        inode : <value>,
                                        pathname : <value>},
                                        ...
                                        }
                           files: [],
                           permissions: {'r': [{pathname: <pathname>, address: <address>}, ...],
                           'w': [{pathname: <pathname>, address: <address>}, ...],
                           'x': [{pathname: <pathname>, address: <address>}, ...],
                           'p': [{pathname: <pathname>, address: <address>}, ...]}
                           }
        :return: Dict {files: [], addresses: {<address> : {<field_name> : field_value}}}
        """
        addresses = {}
        permissions_dict = {'r': list(), 'w': list(), 'x': list(), 'p': list()}
        files = list()
        with open(self.path, 'r') as f:
            for line in f.readlines():
                split_line = line.split()
                # Pad split line to 6 values
                for i in range(len(split_line), 6):
                    # Append empty fields if necessary
                    split_line.append('')
                (address, perms, offset, dev, inode, pathname) = split_line
                addresses[address] = {'perms': perms,
                                      'offset': offset,
                                      'dev': dev,
                                      'inode': inode,
                                      'pathname': pathname}
                if pathname:
                    files.append(pathname)
                for perm in perms:
                    if perm in permissions_dict.keys():
                        permissions_dict[perm].append({'pathname': pathname, 'address': address})
        return {'addresses': addresses, 'files': list(set(files)), 'permissions': permissions_dict}


if __name__ == '__main__':
    import sys

    test_parser(sys.argv[1], Maps)