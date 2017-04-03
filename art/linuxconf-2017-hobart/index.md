---
category: etc
date: '2017-01-11'
layout: article
redirect_from: '/etc/linuxconf-2017-hobart/'
slug: 'linuxconf-2017-hobart'
summary: |
    I've been to LinuxConf before and I've been to Hobart before but this
    time I'm going to LinuxConf in Hobart ...
tags: 'conference, micropython, microcontrollers'
title: LinuxConf 2017 in Hobart
---

I've been to [LinuxConf](/etc/linuxconf-2016-geelong/) before and I've
been to [Hobart](/etc/osdc-2015-hobart/) before but this time I'm going
to [LinuxConf in Hobart](https://linux.conf.au/) ...

Sadly this year I'll only be there for the miniconfs, but I'm still
really looking forward to it ... and thankfully it is almost all
recorded so I'll be watching along from home where I can.

Open Hardware Miniconf: MicroPython on ESP32
============================================

I'll be talking about the implementation of [MicroPython on
ESP32](https://github.com/micropython/micropython-esp32/) at the Open
Hardware Miniconf on Tuesday.

I've been lucky enough to be involved with this port and would like to
thank Damien for his help getting started and
[Microbric](https://microbric.com/) for their support of this effort.

-   [MicroPython on ESP32 Slides](/lca2017/)
-   [MicroPython on ESP32 Video](https://youtu.be/-MrqCmq3Z5k)

So far the port supports only very basic I/O and TCP / IPv4 ... whereas
the ESP platform supports a whole bunch of really interesting hardware.
I hope today's presentation provides a good starting point to new
contributors ... pull requests welcome and raising new issues or
commenting on existing ones is also a great contribution! Thanks to
everyone I spoke to afterwards for your feedback and please get in touch
if you have questions.

My first job when I get back home will be to work out a test harness for
the various hardware platforms which now run MicroPython with the
intention of being able to put them all through their paces on real
hardware. This will make it a lot easier for us to keep up with the
rapid updates to the ESP IDF. (Don't get me wrong, I'm not complaining!)

We might also put together some kind of meetup to discuss further in
person ...

Open Hardware MiniConf
======================

Huge congratulations to the OHMC crew who managed to put together a
great experimental platform seemingly out of nothing but sweat and
enthusiasm and to Espressif for embracing this process and supporting
the miniconf with hardware donations and troubleshooting support.

It was great to see a whole bunch of people soldering for the first
time, and giving it a good go. It did make it pretty clear I need
reading glasses for fine work though.

-   [the IoTuz platform](http://www.openhardwareconf.org/wiki/OHC2017)
-   Tim's lightning talk about [Tomu](http://tomu.im/) (I can't find the
    video though)

Other Presentations
===================

Other presentations I was at:

-   [The Opposite of the Cloud -- Tom
    Eastman](https://linux.conf.au/schedule/presentation/111/)

    > Tom's observation here is that where 'the cloud' means running
    > your services on other people's computers, there's a whole
    > category of 'managed services' which work the opposite way around
    > and he makes some interesting suggestions about how we could think
    > about security in that context

-   [Almost Open - Just close the door behind you -- Steven
    Ellis](https://linux.conf.au/schedule/presentation/147/)

    > Steve looks at the contrast between Open Source and vendor
    > lock-in. Discussion ensues ;-). One of the points he makes which I
    > think is really important is that contributing back to Open Source
    > can actually be a financial positive to companies as they don't
    > have to maintain their own forks and can benefit more from
    > the community.

-   [Knit One, Compute One -- Kris
    Howard](https://linux.conf.au/schedule/presentation/120/)

    > I'd already heard of Kris' connection between knitting and
    > computing and it was indeed interesting. Just like in programming,
    > there's a battle in knitting patterns between the concrete 'bits'
    > of knit and purl and the abstract layers of 'cables' and so on.
    > I'm particulatly impressed by the concept of a knitting markup
    > language and the tool which renders non-flat designs into 3D
    > models so you can see the way the stitches pull the resulting
    > article out of the plane.

-   [Choose your own adventure, please! -- Pia
    Waugh](https://linux.conf.au/schedule/presentation/108/)

    > The is a great keynote which rambles all over the place from
    > prehistory to transhumanity via Trogdor and SPACESHIP! A great
    > reminder that being a pack of scruffy nerds doesn't mean we can't
    > choose to change the world, and choose to change it for
    > the better.

-   [Pushing on a Piece of String - OSIAs adventures in influencing
    governments -- Paul
    Foxworthy](https://linux.conf.au/schedule/presentation/172/)

    > Paul summarizes the efforts that OSIA has been putting in to
    > influence government to work more with Open Source technology.
    > Also, I get outed as having joined the OSIA board.

Videos
======

The above was just the first two days, and not even the conference
proper! I'm going to be catching up on videos over the next couple of
weeks and will post some updates when I do ...
