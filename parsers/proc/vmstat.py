"""
#cat /proc/vmstat
nr_free_pages 20223354
nr_alloc_batch 899
nr_inactive_anon 393025
nr_active_anon 808058
nr_inactive_file 1639308
nr_active_file 1026244
nr_unevictable 0
nr_mlock 0
nr_anon_pages 33812
nr_mapped 32819
nr_file_pages 3733000
nr_dirty 65
nr_writeback 0
nr_slab_reclaimable 334931
nr_slab_unreclaimable 26922
nr_page_table_pages 7012
nr_kernel_stack 915
nr_unstable 0
nr_bounce 0
nr_vmscan_write 5812807
nr_vmscan_immediate_reclaim 5539
nr_writeback_temp 0
nr_isolated_anon 0
nr_isolated_file 0
nr_shmem 1067448
nr_dirtied 3433782
nr_written 9211885
numa_hit 3168851306
numa_miss 0
numa_foreign 0
numa_interleave 67441
numa_local 3168851306
numa_other 0
workingset_refault 29351
workingset_activate 6715
workingset_nodereclaim 0
nr_anon_transparent_hugepages 195
nr_free_cma 0
nr_dirty_threshold 4549598
nr_dirty_background_threshold 2274799
Pgpgin 36054419 #The number of memory pages read from startup to now
pgpgout 45830912
Pswpin 8101573 #The number of swap partition pages read from startup to now
pswpout 5812807
pgalloc_dma 0
pgalloc_dma32 161404306
pgalloc_normal 3979543730
pgalloc_movable 0
Pgfree 4161177252       #Number of pages released from startup to now
Pgactivate 11895760     #Number of pages activated from startup to now
Pgdeactivate 12364831   #Number of pages to be activated from startup to now
Pgfault 9456580348      #Number of secondary page faults from startup to now
Pgmajfault 1038166      #The number of page faults from startup to now
pgrefill_dma 0
pgrefill_dma32 335375
pgrefill_normal 11804406
pgrefill_movable 0
pgsteal_kswapd_dma 0
pgsteal_kswapd_dma32 0
pgsteal_kswapd_normal 0
pgsteal_kswapd_movable 0
pgsteal_direct_dma 0
pgsteal_direct_dma32 0
pgsteal_direct_normal 0
pgsteal_direct_movable 0
 Pgscan_kswapd_dma 0    #Number of DMA memory pages scanned from startup to kswapd background process
pgscan_kswapd_dma32 0
 Pgscan_kswapd_normal 0 #The number of normal memory pages scanned from the startup to the current kswapd background process
pgscan_kswapd_movable 0
 Pgscan_direct_dma 0    #Number of pages that are directly reclaimed from startup to DMA memory area
pgscan_direct_dma32 0
 Pgscan_direct_normal 0 #Number of pages that are directly reclaimed from startup to normal storage
pgscan_direct_movable 0
pgscan_direct_throttle 0
zone_reclaim_failed 0
pginodesteal 0
 Slabs_scanned 0        #Number of slices scanned from startup to now
 Kswapd_inodesteal 0    #Number of pages recycled by kswapd for other purposes from startup to now
kswapd_low_wmark_hit_quickly 64
kswapd_high_wmark_hit_quickly 0
 Pageoutrun 1           #Number of pages recycled from the start to the present by kswapd call
 Allocstall 0           #Number of pages requested to be directly recycled from startup to now
pgrotated 5766223
drop_pagecache 0
drop_slab 0
numa_pte_updates 0
numa_huge_pte_updates 0
numa_hint_faults 0
numa_hint_faults_local 0
numa_pages_migrated 0
pgmigrate_success 0
pgmigrate_fail 0
compact_migrate_scanned 0
compact_free_scanned 0
compact_isolated 0
compact_stall 0             #compact_stall is incremented every time a process stalls to run memory compaction so that a huge page is free for use.
compact_fail 0              #compact_fail is incremented if the system tries to compact memory but failed.
compact_success 0           #compact_success is incremented if the system compacted memory and
htlb_buddy_alloc_success 0
htlb_buddy_alloc_fail 0
unevictable_pgs_culled 0
unevictable_pgs_scanned 0
unevictable_pgs_rescued 0
unevictable_pgs_mlocked 0
unevictable_pgs_munlocked 0
unevictable_pgs_cleared 0
unevictable_pgs_stranded 0
thp_fault_alloc 1662087
thp_fault_fallback 7594
thp_collapse_alloc 1032
thp_collapse_alloc_failed 0
thp_split 1677
thp_zero_page_alloc 1
thp_zero_page_alloc_failed 0
"""
from parsers import Regex, test_parser


class Vmstat(Regex):
    def __init__(self, path='/proc/vmstat'):
        Regex.__init__(self, path, r"(.+)\s(\d+)\n")

    def _run_regex(self, data, instance_index=None):
        return {m[0]: int(m[1]) for m in self.regex.findall(data)}


if __name__ == '__main__':
    test_parser('/proc/vmstat', Vmstat)
