"""
meminfo:

Provides information about distribution and utilization of memory.  This
varies by architecture and compile options.  The following is from a
16GB PIII, which has highmem enabled.  You may not have all of these fields.

> cat /proc/meminfo

MemTotal:     16344972 kB
MemFree:      13634064 kB
MemAvailable: 14836172 kB
Buffers:          3656 kB
Cached:        1195708 kB
SwapCached:          0 kB
Active:         891636 kB
Inactive:      1077224 kB
HighTotal:    15597528 kB
HighFree:     13629632 kB
LowTotal:       747444 kB
LowFree:          4432 kB
SwapTotal:           0 kB
SwapFree:            0 kB
Dirty:             968 kB
Writeback:           0 kB
AnonPages:      861800 kB
Mapped:         280372 kB
Shmem:             644 kB
KReclaimable:   168048 kB
Slab:           284364 kB
SReclaimable:   159856 kB
SUnreclaim:     124508 kB
PageTables:      24448 kB
NFS_Unstable:        0 kB
Bounce:              0 kB
WritebackTmp:        0 kB
CommitLimit:   7669796 kB
Committed_AS:   100056 kB
VmallocTotal:   112216 kB
VmallocUsed:       428 kB
VmallocChunk:   111088 kB
Percpu:          62080 kB
HardwareCorrupted:   0 kB
AnonHugePages:   49152 kB
ShmemHugePages:      0 kB
ShmemPmdMapped:      0 kB


    MemTotal: Total usable ram (i.e. physical ram minus a few reserved
              bits and the kernel binary code)
     MemFree: The sum of LowFree+HighFree
MemAvailable: An estimate of how much memory is available for starting new
              applications, without swapping. Calculated from MemFree,
              SReclaimable, the size of the file LRU lists, and the low
              watermarks in each zone.
              The estimate takes into account that the system needs some
              page cache to function well, and that not all reclaimable
              slab will be reclaimable, due to items being in use. The
              impact of those factors will vary from system to system.
     Buffers: Relatively temporary storage for raw disk blocks
              shouldn't get tremendously large (20MB or so)
      Cached: in-memory cache for files read from the disk (the
              pagecache).  Doesn't include SwapCached
  SwapCached: Memory that once was swapped out, is swapped back in but
              still also is in the swapfile (if memory is needed it
              doesn't need to be swapped out AGAIN because it is already
              in the swapfile. This saves I/O)
      Active: Memory that has been used more recently and usually not
              reclaimed unless absolutely necessary.
    Inactive: Memory which has been less recently used.  It is more
              eligible to be reclaimed for other purposes
   HighTotal:
    HighFree: Highmem is all memory above ~860MB of physical memory
              Highmem areas are for use by userspace programs, or
              for the pagecache.  The kernel must use tricks to access
              this memory, making it slower to access than lowmem.
    LowTotal:
     LowFree: Lowmem is memory which can be used for everything that
              highmem can be used for, but it is also available for the
              kernel's use for its own data structures.  Among many
              other things, it is where everything from the Slab is
              allocated.  Bad things happen when you're out of lowmem.
   SwapTotal: total amount of swap space available
    SwapFree: Memory which has been evicted from RAM, and is temporarily
              on the disk
       Dirty: Memory which is waiting to get written back to the disk
   Writeback: Memory which is actively being written back to the disk
   AnonPages: Non-file backed pages mapped into userspace page tables
HardwareCorrupted: The amount of RAM/memory in KB, the kernel identifies as
	      corrupted.
AnonHugePages: Non-file backed huge pages mapped into userspace page tables
      Mapped: files which have been mmaped, such as libraries
       Shmem: Total memory used by shared memory (shmem) and tmpfs
ShmemHugePages: Memory used by shared memory (shmem) and tmpfs allocated
              with huge pages
ShmemPmdMapped: Shared memory mapped into userspace with huge pages
KReclaimable: Kernel allocations that the kernel will attempt to reclaim
              under memory pressure. Includes SReclaimable (below), and other
              direct allocations with a shrinker.
        Slab: in-kernel data structures cache
SReclaimable: Part of Slab, that might be reclaimed, such as caches
  SUnreclaim: Part of Slab, that cannot be reclaimed on memory pressure
  PageTables: amount of memory dedicated to the lowest level of page
              tables.
NFS_Unstable: NFS pages sent to the server, but not yet committed to stable
	      storage
      Bounce: Memory used for block device "bounce buffers"
WritebackTmp: Memory used by FUSE for temporary writeback buffers
 CommitLimit: Based on the overcommit ratio ('vm.overcommit_ratio'),
              this is the total amount of  memory currently available to
              be allocated on the system. This limit is only adhered to
              if strict overcommit accounting is enabled (mode 2 in
              'vm.overcommit_memory').
              The CommitLimit is calculated with the following formula:
              CommitLimit = ([total RAM pages] - [total huge TLB pages]) *
                             overcommit_ratio / 100 + [total swap pages]
              For example, on a system with 1G of physical RAM and 7G
              of swap with a `vm.overcommit_ratio` of 30 it would
              yield a CommitLimit of 7.3G.
              For more details, see the memory overcommit documentation
              in vm/overcommit-accounting.
Committed_AS: The amount of memory presently allocated on the system.
              The committed memory is a sum of all of the memory which
              has been allocated by processes, even if it has not been
              "used" by them as of yet. A process which malloc()'s 1G
              of memory, but only touches 300M of it will show up as
	      using 1G. This 1G is memory which has been "committed" to
              by the VM and can be used at any time by the allocating
              application. With strict overcommit enabled on the system
              (mode 2 in 'vm.overcommit_memory'),allocations which would
              exceed the CommitLimit (detailed above) will not be permitted.
              This is useful if one needs to guarantee that processes will
              not fail due to lack of memory once that memory has been
              successfully allocated.
VmallocTotal: total size of vmalloc memory area
 VmallocUsed: amount of vmalloc area which is used
VmallocChunk: largest contiguous block of vmalloc area which is free
      Percpu: Memory allocated to the percpu allocator used to back percpu
              allocations. This stat excludes the cost of metadata.
"""
from parsers import Regex, test_parser


class Meminfo(Regex):
    def __init__(self, path='/proc/meminfo'):
        Regex.__init__(self, path, r"(.+):\s*(\d+)\s([A-Za-z]+)\n")

    def _run_regex(self, data, instance_index=None):
        # x = self.regex.findall(data)
        # print(type(x))
        return {m[0]: int(m[1]) for m in self.regex.findall(data)}


if __name__ == '__main__':
    test_parser('/proc/meminfo', Meminfo)