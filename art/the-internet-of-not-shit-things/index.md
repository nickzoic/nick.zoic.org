---
category: etc
date: '2016-05-07'
layout: article
redirect_from: '/etc/the-internet-of-not-shit-things/'
slug: 'the-internet-of-not-shit-things'
tags: iot
title: 'The Internet of (Not Shit) Things'
summary: Trying to better understand the problems of the IoT by actually listening to its detractors.
---

The Internet of Things! Existential menace or meaningless buzzword?
Automating away drudgery or just eroding privacy? Cornucopia or
Panopticon?

The Internet of Shit
====================

The negative side of the argument is eloquently expressed in too many
places to list here, often under the catchy name "[The Internet of
Shit](https://www.google.com.au/search?client=ubuntu&channel=fs&q=internet+of+shit)".
There's even an [@internetofshit twitter
account](https://twitter.com/internetofshit).

But why such skepticism in a world of rampant technophilia? Why are we
not, in fact, welcoming our [robot
overlords](https://en.wikipedia.org/wiki/Robot_Overlords)?

Very Valid Criticisms
---------------------

There are a lot of criticisms out there, but for me the top ones are:

-   [If you're not the customer, you're the
    product](http://www.information-age.com/technology/security/1290603/facebook-is-%22deliberately-killing-privacy%22-says-schneier).
    The backend services have to get paid for somehow. and if you're not
    paying directly, you're paying by accepting advertising and/or by
    having your privacy sold.
-   Your hi-tech device may suddenly turn into a [container of
    hummus](https://medium.com/@arlogilbert/the-time-that-tony-fadell-sold-me-a-container-of-hummus-cb0941c762c1)
    if the service provider no longer feels like supporting it.
-   Uselsss if the Internet isn't available. Even the most reliable
    networks sometimes go down. Consumer routers fail.
-   Crypto support on IoT devices is often very weak. Partly because of
    lack of entropy, lack of CPU resources, etc. It's tricky to use a
    protocol like SSL on a tiny CPU.
-   It's hard enough to get people to [change their smoke alarm
    batteries](http://duracellfiresafety.com.au/) or [update Internet
    Explorer](https://heimdalsecurity.com/blog/security-alert-millions-exposed-internet-explorer-vulnerability/).
    No-one ever is going to reflash their thermostat.
-   The software for things like lightbulbs is often
    [awful](https://mjg59.dreamwidth.org/40397.html), and open to all
    kinds of exploitation. This shouldn't be too surprising since even
    the manufacturers of [electronic locks have trouble getting this
    right](http://blog.trendmicro.com/let-get-door-remote-root-vulnerability-hid-door-controllers/).

Not Shit Things
===============

Turning the criticisms around, what requirements do we get:

-   Devices need to be *retargetable*. That [Nest
    Thermostat](https://nest.com/thermostat/meet-nest-thermostat/) is
    really just a rotary encoder and a display, so why shouldn't it do
    other things, or more things, if you no longer want it to be just
    a thermostat. Why should all your lightbulbs be locked into a single
    vendor?
-   Communications need to be *local*. Sure, it's nifty that you can
    switch your lights on from Low Earth Orbit, but it is ridiculous to
    bounce every light-switch-flip off some
    [Cloud](http://knowyourmeme.com/photos/1044247-old-man-yells-at-cloud) somewhere.
-   The network needs to be *protected*. Mostly from the Internet, but
    [also from the local
    network](http://www.dhanjani.com/blog/2013/08/hacking-lightbulbs.html).

Any candidate solution has to address these requirements.

Further Work
============

I'd like to do some more work on defining a simple candidate protocol
which would meet these requirements and hopefully [get it published as
an RFC](https://www.ietf.org/tao.html). In the meantime, I'll be talking
about [The Internet of
Toys](../buzzconf-nights-esp8266-flobot-ciril/) at [Buzzconf
Nights](https://buzzconf.io/nights/) and continuing to develop these
ideas.

UPDATE
======

-   I'll be talking about this stuff at [PyCon AU's inaugural Internet
    of Things
    mini-conf](https://2016.pycon-au.org/programme/internet_of_things_miniconf)
    which should be fun! More news as it comes to light.
