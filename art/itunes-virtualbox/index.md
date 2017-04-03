---
category: etc
date: '2012-02-20'
layout: article
redirect_from: '/etc/itunes-virtualbox/'
slug: 'itunes-virtualbox'
tags: 'apple, linux, virtualbox'
title: 'iPhone / iTunes / Windows XP / VirtualBox / Ubuntu 9.10'
---

Finally got this to work properly. The biggest trap is that when it
restores / upgrades / whatever, it changes its USB ID, so don’t filter
just on what it is when its working, or it will get stuck in recovery
mode. DAMHIK.:

1.  Install VirtualBox from the deb package at
    <http://www.virtualbox.org/wiki/Downloads>
2.  Tell hal to keep away from monoliths:
    `/etc/hal/fdi/policy/10-noiphone.fdi`:

        <?xml version="1.0" encoding="UTF-8"?>
        <deviceinfo version="0.2">
        <device>
        <match key="info.vendor" string="Apple, Inc.">
        <merge key="info.ignore" type="bool">true</merge>
        </match>
        </device>
        </deviceinfo>

3.  Tell usbhid to keep away too: `/etc/modprobe.d/usbhid.conf`:

        # iPhone
        options usbhid quirks=0x05ac:0x1294:0x04
        options usbhid quirks=0x05ac:0x1281:0x04

    Then run `module-assistant update` and reboot or otherwise reload
    the usbhid module

4.  

    Configure VirtualBox to allow a filter for all Apple products (0x05AC) and

    :   leave the other fields blank

5.  Start the virtual machine, select the iPhone device, run
    iTunes, etc.
6.  If restoring / updating / whatever, note that every time the iPhone
    disconnects and reconnects or changes its ID, you’ll need to
    reselect the device ... so watch it while it is working and check
    the Devices &gt;&gt; USB Devices menu any time it seems to
    get stuck.

Refs / Thanks To
================

> -   <http://teknofire.net/articles/2009/07/06/ubuntu-vmware-and-accessing-the-iphone/>
> -   <http://swiss.ubuntuforums.org/showthread.php?t=1285097>
> -   <http://ubuntuforums.org/showthread.php?t=1318160>
> -   <http://blahonga.yanson.org/2009/07/pain-upgrading-iphone-to-30-under.html>
> -   <http://forums.virtualbox.org/viewtopic.php?f=2&t=18852>

Update
======

Backing up the iPhone using iTunes on VirtualBox is godawful slow. CPU
load is pegged at 80-90% of one CPU, and it takes hours. This page:
<http://forums.virtualbox.org/viewtopic.php?f=7&p=107254> helpfully
mentions that it works okay if run from a smaller window, and despite
the ludicrousness of this idea I gave it a go … CPU load is much lower
and … well, its still slow, but it is at least moving.

Yep, took about an hour to back up \~15GB of stuff on the iPhone, as
opposed to the several hours it used to take to get nowhere. Weird.

Update 2
========

I think that slowness problem is fixed in more recent versions ... I'm
now using VirtualBox 4.

Update 3
========

I use iTunes on Snow Leopard these days, and yes, you can make Snow
Leopard run under VirtualBox if you try hard enough :-). It doesn't seem
to have the same slowdown problems.
