"""
3.8	/proc/<pid>/fdinfo/<fd> - Information about opened file
---------------------------------------------------------------
This file provides information associated with an opened file. The regular
files have at least three fields -- 'pos', 'flags' and mnt_id. The 'pos'
represents the current offset of the opened file in decimal form [see lseek(2)
for details], 'flags' denotes the octal O_xxx mask the file has been
created with [see open(2) for details] and 'mnt_id' represents mount ID of
the file system containing the opened file [see 3.5 /proc/<pid>/mountinfo
for details].

A typical output is

	pos:	0
	flags:	0100002
	mnt_id:	19

All locks associated with a file descriptor are shown in its fdinfo too.

lock:       1: FLOCK  ADVISORY  WRITE 359 00:13:11691 0 EOF

The files such as eventfd, fsnotify, signalfd, epoll among the regular pos/flags
pair provide additional information particular to the objects they represent.

	Eventfd files
	~~~~~~~~~~~~~
	pos:	0
	flags:	04002
	mnt_id:	9
	eventfd-count:	5a

	where 'eventfd-count' is hex value of a counter.

	Signalfd files
	~~~~~~~~~~~~~~
	pos:	0
	flags:	04002
	mnt_id:	9
	sigmask:	0000000000000200

	where 'sigmask' is hex value of the signal mask associated
	with a file.

	Epoll files
	~~~~~~~~~~~
	pos:	0
	flags:	02
	mnt_id:	9
	tfd:        5 events:       1d data: ffffffffffffffff pos:0 ino:61af sdev:7

	where 'tfd' is a target file descriptor number in decimal form,
	'events' is events mask being watched and the 'data' is data
	associated with a target [see epoll(7) for more details].

	The 'pos' is current offset of the target file in decimal form
	[see lseek(2)], 'ino' and 'sdev' are inode and device numbers
	where target file resides, all in hex format.

	Fsnotify files
	~~~~~~~~~~~~~~
	For inotify files the format is the following

	pos:	0
	flags:	02000000
	inotify wd:3 ino:9e7e sdev:800013 mask:800afce ignored_mask:0 fhandle-bytes:8 fhandle-type:1 f_handle:7e9e0000640d1b6d

	where 'wd' is a watch descriptor in decimal form, ie a target file
	descriptor number, 'ino' and 'sdev' are inode and device where the
	target file resides and the 'mask' is the mask of events, all in hex
	form [see inotify(7) for more details].

	If the kernel was built with exportfs support, the path to the target
	file is encoded as a file handle.  The file handle is provided by three
	fields 'fhandle-bytes', 'fhandle-type' and 'f_handle', all in hex
	format.

	If the kernel is built without exportfs support the file handle won't be
	printed out.

	If there is no inotify mark attached yet the 'inotify' line will be omitted.

	For fanotify files the format is

	pos:	0
	flags:	02
	mnt_id:	9
	fanotify flags:10 event-flags:0
	fanotify mnt_id:12 mflags:40 mask:38 ignored_mask:40000003
	fanotify ino:4f969 sdev:800013 mflags:0 mask:3b ignored_mask:40000000 fhandle-bytes:8 fhandle-type:1 f_handle:69f90400c275b5b4

	where fanotify 'flags' and 'event-flags' are values used in fanotify_init
	call, 'mnt_id' is the mount point identifier, 'mflags' is the value of
	flags associated with mark which are tracked separately from events
	mask. 'ino', 'sdev' are target inode and device, 'mask' is the events
	mask and 'ignored_mask' is the mask of events which are to be ignored.
	All in hex format. Incorporation of 'mflags', 'mask' and 'ignored_mask'
	does provide information about flags and mask used in fanotify_mark
	call [see fsnotify manpage for details].

	While the first three lines are mandatory and always printed, the rest is
	optional and may be omitted if no marks created yet.

	Timerfd files
	~~~~~~~~~~~~~

	pos:	0
	flags:	02
	mnt_id:	9
	clockid: 0
	ticks: 0
	settime flags: 01
	it_value: (0, 49406829)
	it_interval: (1, 0)

	where 'clockid' is the clock type and 'ticks' is the number of the timer expirations
	that have occurred [see timerfd_create(2) for details]. 'settime flags' are
	flags in octal form been used to setup the timer [see timerfd_settime(2) for
	details]. 'it_value' is remaining time until the timer exiration.
	'it_interval' is the interval for the timer. Note the timer might be set up
	with TIMER_ABSTIME option which will be shown in 'settime flags', but 'it_value'
	still exhibits timer's remaining time.
"""
import os
import re

from parsers import Dir


class FDinfo(Dir):
    def __init__(self, path='/proc/{pid}/fdinfo'):
        Dir.__init__(self, path)

    def _entry_parse(self, e):
        data = open(os.path.join(self.path, e), 'rb').read().decode('utf-8')
        return {m[0]: int(m[1]) for m in re.findall(r"(.+):\s*(\d+)\n", data)}
