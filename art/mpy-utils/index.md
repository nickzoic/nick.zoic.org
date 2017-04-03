---
category: etc
date: '2016-11-24'
layout: article
redirect_from: '/etc/mpy-utils/'
slug: 'mpy-utils'
tags: 'micropython,microcontrollers,esp8266,python'
title: Micropython Utilities
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
