"""
Table 1-1: Process specific entries in /proc
..............................................................................
 File		Content
 ...       ...
 mounts      Mounted filesystems


$ cat mounts
rootfs / lxfs rw,noatime 0 0
none /dev tmpfs rw,noatime,mode=755 0 0
sysfs /sys sysfs rw,nosuid,nodev,noexec,noatime 0 0
proc /proc proc rw,nosuid,nodev,noexec,noatime 0 0
devpts /dev/pts devpts rw,nosuid,noexec,noatime,gid=5,mode=620 0 0
none /run tmpfs rw,nosuid,noexec,noatime,mode=755 0 0
none /run/lock tmpfs rw,nosuid,nodev,noexec,noatime 0 0
none /run/shm tmpfs rw,nosuid,nodev,noatime 0 0
none /run/user tmpfs rw,nosuid,nodev,noexec,noatime,mode=755 0 0
binfmt_misc /proc/sys/fs/binfmt_misc binfmt_misc rw,relatime 0 0
tmpfs /sys/fs/cgroup tmpfs rw,nosuid,nodev,noexec,relatime,mode=755 0 0
cgroup /sys/fs/cgroup/devices cgroup rw,nosuid,nodev,noexec,relatime,devices 0 0
C:\134 /mnt/c drvfs rw,noatime,uid=1000,gid=1000,case=off 0 0
D:\134 /mnt/d drvfs rw,noatime,uid=1000,gid=1000,case=off 0 0
"""
from parsers import Regex, test_parser


class Mounts(Regex):
    def __init__(self, path='/proc/mounts'):
        Regex.__init__(self, path, regex_string="(.+) (.+) (.+) (.+) (.+) (.+)\n")

if __name__ == '__main__':
    test_parser('/proc/mounts', Mounts)
