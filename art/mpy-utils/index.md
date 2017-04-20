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
