"""
3.5	/proc/<pid>/mountinfo - Information about mounts
--------------------------------------------------------

This file contains lines of the form:

36 35 98:0 /mnt1 /mnt2 rw,noatime master:1 - ext3 /dev/root rw,errors=continue
(1)(2)(3)   (4)   (5)      (6)      (7)   (8) (9)   (10)         (11)

(1) mount ID:  unique identifier of the mount (may be reused after umount)
(2) parent ID:  ID of parent (or of self for the top of the mount tree)
(3) major:minor:  value of st_dev for files on filesystem
(4) root:  root of the mount within the filesystem
(5) mount point:  mount point relative to the process's root
(6) mount options:  per mount options
(7) optional fields:  zero or more fields of the form "tag[:value]"
(8) separator:  marks the end of the optional fields
(9) filesystem type:  name of filesystem of the form "type[.subtype]"
(10) mount source:  filesystem specific information or "none"
(11) super options:  per super block options

Parsers should ignore all unrecognised optional fields.  Currently the
possible optional fields are:

shared:X  mount is shared in peer group X
master:X  mount is slave to peer group X
propagate_from:X  mount is slave and receives propagation from peer group X (*)
unbindable  mount is unbindable

(*) X is the closest dominant peer group under the process's root.  If
X is the immediate master of the mount, or if there's no dominant peer
group under the same root, then only the "master:X" field is present
and not the "propagate_from:X" field.

For more information on mount propagation see:

  Documentation/filesystems/sharedsubtree.txt
"""
from parsers import SnapshotParser, test_parser


class Mountinfo(SnapshotParser):
    def __init__(self, path='/proc/{pid}/mountinfo'):
        SnapshotParser.__init__(self, path)

    def _parse(self):
        """
        Return a dict {id : mountinfo_dict} of all mountinfos.
        :param path: str - "/proc/<pid>/mountinfo"
        :return: {0 : { 'mount ID':  unique identifier of the mount (may be reused after umount)
                        'parent ID':  ID of parent (or of self for the top of the mount tree)
                        'major:minor':  value of st_dev for files on filesystem
                        'root':  root of the mount within the filesystem
                        'mount point':  mount point relative to the process's root
                        'mount options':  per mount options
                        'optional fields':  zero or more fields of the form "tag[:value]"
                        'separator':  marks the end of the optional fields
                        'filesystem type':  name of filesystem of the form "type[.subtype]"
                        'mount source':  filesystem specific information or "none"
                        'super options':  per super block options
                    ...
                  }
        """
        mountinfos = {}
        with open(self.path, 'r') as f:
            for i, line in enumerate(f):
                split_line = line.split()
                # Pad split line to 6 values
                for i in range(len(split_line), 11):
                    split_line.append('')
                (
                    mount_id, parent_id, major_minor, root, mount_point, mount_options, optional_fields, seperator,
                    fs_type, mount_source, super_options
                ) = split_line

                mountinfos[int(i)] = {'mount ID': mount_id,
                                      'parent ID': parent_id,
                                      'major:minor': major_minor,
                                      'root': root,
                                      'mount point': mount_point,
                                      'mount options': mount_options,
                                      'optional fields': optional_fields,
                                      'separator': seperator,
                                      'filesystem type': fs_type,
                                      'mount source': mount_source,
                                      'super options': super_options}
                return mountinfos

if __name__ == '__main__':
    test_parser('/proc/7531/mountinfo', Mountinfo)
