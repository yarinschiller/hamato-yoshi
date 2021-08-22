"""

Table 1-2: Contents of the status files (as of 4.19)
..............................................................................
 Field                       Content
 Name                        filename of the executable
 Umask                       file mode creation mask
 State                       state (R is running, S is sleeping, D is sleeping
                             in an uninterruptible wait, Z is zombie,
			     T is traced or stopped)
 Tgid                        thread group ID
 Ngid                        NUMA group ID (0 if none)
 Pid                         process id
 PPid                        process id of the parent process
 TracerPid                   PID of process tracing this process (0 if not)
 Uid                         Real, effective, saved set, and  file system UIDs
 Gid                         Real, effective, saved set, and  file system GIDs
 FDSize                      number of file descriptor slots currently allocated
 Groups                      supplementary group list
 NStgid                      descendant namespace thread group ID hierarchy
 NSpid                       descendant namespace process ID hierarchy
 NSpgid                      descendant namespace process group ID hierarchy
 NSsid                       descendant namespace session ID hierarchy
 VmPeak                      peak virtual memory size
 VmSize                      total program size
 VmLck                       locked memory size
 VmPin                       pinned memory size
 VmHWM                       peak resident set size ("high water mark")
 VmRSS                       size of memory portions. It contains the three
                             following parts (VmRSS = RssAnon + RssFile + RssShmem)
 RssAnon                     size of resident anonymous memory
 RssFile                     size of resident file mappings
 RssShmem                    size of resident shmem memory (includes SysV shm,
                             mapping of tmpfs and shared anonymous mappings)
 VmData                      size of private data segments
 VmStk                       size of stack segments
 VmExe                       size of text segment
 VmLib                       size of shared library code
 VmPTE                       size of page table entries
 VmSwap                      amount of swap used by anonymous private data
                             (shmem swap usage is not included)
 HugetlbPages                size of hugetlb memory portions
 CoreDumping                 process's memory is currently being dumped
                             (killing the process may lead to a corrupted core)
 THP_enabled		     process is allowed to use THP (returns 0 when
			     PR_SET_THP_DISABLE is set on the process
 Threads                     number of threads
 SigQ                        number of signals queued/max. number for queue
 SigPnd                      bitmap of pending signals for the thread
 ShdPnd                      bitmap of shared pending signals for the process
 SigBlk                      bitmap of blocked signals
 SigIgn                      bitmap of ignored signals
 SigCgt                      bitmap of caught signals
 CapInh                      bitmap of inheritable capabilities
 CapPrm                      bitmap of permitted capabilities
 CapEff                      bitmap of effective capabilities
 CapBnd                      bitmap of capabilities bounding set
 CapAmb                      bitmap of ambient capabilities
 NoNewPrivs                  no_new_privs, like prctl(PR_GET_NO_NEW_PRIV, ...)
 Seccomp                     seccomp mode, like prctl(PR_GET_SECCOMP, ...)
 Speculation_Store_Bypass    speculative store bypass mitigation status
 Cpus_allowed                mask of CPUs on which this process may run
 Cpus_allowed_list           Same as previous, but in "list format"
 Mems_allowed                mask of memory nodes allowed to this process
 Mems_allowed_list           Same as previous, but in "list format"
 voluntary_ctxt_switches     number of voluntary context switches
 nonvoluntary_ctxt_switches  number of non voluntary context switches
..............................................................................

For example, to get the status information of a process, all you have to do is
read the file /proc/PID/status:

  >cat /proc/self/status
  Name:   cat
  State:  R (running)
  Tgid:   5452
  Pid:    5452
  PPid:   743
  TracerPid:      0						(2.4)
  Uid:    501     501     501     501
  Gid:    100     100     100     100
  FDSize: 256
  Groups: 100 14 16
  VmPeak:     5004 kB
  VmSize:     5004 kB
  VmLck:         0 kB
  VmHWM:       476 kB
  VmRSS:       476 kB
  RssAnon:             352 kB
  RssFile:             120 kB
  RssShmem:              4 kB
  VmData:      156 kB
  VmStk:        88 kB
  VmExe:        68 kB
  VmLib:      1412 kB
  VmPTE:        20 kb
  VmSwap:        0 kB
  HugetlbPages:          0 kB
  CoreDumping:    0
  THP_enabled:	  1
  Threads:        1
  SigQ:   0/28578
  SigPnd: 0000000000000000
  ShdPnd: 0000000000000000
  SigBlk: 0000000000000000
  SigIgn: 0000000000000000
  SigCgt: 0000000000000000
  CapInh: 00000000fffffeff
  CapPrm: 0000000000000000
  CapEff: 0000000000000000
  CapBnd: ffffffffffffffff
  CapAmb: 0000000000000000
  NoNewPrivs:     0
  Seccomp:        0
  Speculation_Store_Bypass:       thread vulnerable
  voluntary_ctxt_switches:        0
  nonvoluntary_ctxt_switches:     1

This shows you nearly the same information you would get if you viewed it with
the ps  command.  In  fact,  ps  uses  the  proc  file  system  to  obtain its
information.  But you get a more detailed  view of the  process by reading the
file /proc/PID/status. It fields are described in table 1-2.

The  statm  file  contains  more  detailed  information about the process
memory usage. Its seven fields are explained in Table 1-3.  The stat file
contains details information about the process itself.  Its fields are
explained in Table 1-4.

(for SMP CONFIG users)
For making accounting scalable, RSS related information are handled in an
asynchronous manner and the value may not be very precise. To see a precise
snapshot of a moment, you can see /proc/<pid>/smaps file and scan page table.
It's slow but very precise.
"""
from parsers import SnapshotParser


class Status(SnapshotParser):
    """
    Parser for /proc/PID/status.
    Example format:
        cat /proc/144/status
            Name:	md
            Umask:	0000
            State:	I (idle)
            Tgid:	144
            Ngid:	0
            Pid:	144
            ...
    """

    def __init__(self, path='/proc/{pid}/status'):
        SnapshotParser.__init__(self, path)

    def _parse(self):
        """
        Return a dict of {field : status}
        Example:
            FDstatus('/proc/144/status')._parse()
            {'Name'     : 'md',
             'Umask'    : '0000',
             'State'    : 'I (idle)',
             'Tgid'     : '144',
             'Ngid'     : '0',
             'Pid'     : '144',
             ...
            }
        :return: Dict {field_name : field_value}
        """
        d = {}
        with open(self.path, 'r') as f:
            for line in f:
                line = ''.join(line.split())
                (key, value) = line.split(':')
                d[key] = value
        return d
