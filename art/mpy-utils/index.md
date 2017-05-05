---
category: etc
date: '2016-11-24'
layout: article
redirect_from: '/etc/mpy-utils/'
slug: 'mpy-utils'
tags:
    - micropython
    - microcontrollers
    - esp8266
    - python
title: Micropython Utilities
summary: some utility programs to copy and mount MicroPython filesystems from your computer
---

I just released [mpy-utils](https://github.com/nickzoic/mpy-utils) which
lets you [FUSE](https://en.wikipedia.org/wiki/Filesystem_in_Userspace)
mount the MicroPython filesystem using only the REPL. It's also
available on PyPI:

    pip3 install mpy-utils

It is awfully slow, but seems to work pretty well. Most of the hard work
was already done by the excellent
[fusepy](https://github.com/terencehonles/fusepy), and thanks to Damien
and
[pyboard.py](https://github.com/micropython/micropython/blob/master/tools/pyboard.py)
for the hints on how to get Micropython REPL working in raw mode.

UPDATE 2017-04-04
=================

Rather unexpectedly, [Tony D from Adafruit](https://learn.adafruit.com/users/tdicola)
made a [youtube video about mpy-utils](https://youtu.be/NdXtvtYrOs4) which was quite
interesting to see, as it points out quite a few flaws in the package.  I've tried to 
turn them into github issues ...

UPDATE 2017-05-06
=================

Sometimes stupid is better than clever.

I was presenting mpy-utils at the [MicroPython Meetup](https://www.meetup.com/MicroPython-Meetup/)
including the nifty FUSE-only-works-on-Linux-and-OSX bit, and one of the members said 

> aha, I know how you do this, you just poll the files and then send the changes!

Well, no, we did something much cleverer by mounting the whole thing as a filesystem, but
that got me thinking: FUSE is clever, but is also responsible for [issues](https://github.com/nickzoic/mpy-utils/issues) #1, #5, #6, #7 ... perhaps stupid would be better?

So version 0.1.6 of mpy-utils now includes `mpy_watch` which works exactly in the most
obvious way: it polls your files for changes every second and sends them when they change.

It also keeps a copy in memory and sends only the differences, using Python's difflib to 
work that out.  That makes it far, far quicker for the usual case.  And there's a filename filter
in place to stop it trying to send crazy editor tempfiles and stuff.

Future improvements:

* it could avoid polling using one of the cross-platform watchdogs
* it could be a bit smarter about binaries.  
* the diff could look a little more closely at text to insert/replace to see if
  it can save even more bytes
* the code is pretty dismal but it's 2am here so that can wait
