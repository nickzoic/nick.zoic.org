---
category: etc
date: '2016-03-20'
layout: article
redirect_from: '/etc/ciril-cubic-inch-robots-in-labs/'
slug: 'ciril-cubic-inch-robots-in-labs'
summary: A project to create mini robots for education purposes
tags:
    - robots
    - microcontrollers
    - electronics
    - education
title: 'Ciril: Cubic Inch Robots in Labs'
---

<p class="note">
For updates, see the <a href="http://ciril.mnemote.com/">Ciril Project Page</a>
</p>

The [ESP8266](http://esp8266.com/) opens up new possibilities for
hardware design of educational robots. This project aims to put together
an open hardware design compatible with the
[Flobot](http://github.com/mnemote/flobot) project and also projects
such as [NodeMCU](http://nodemcu.com/).

I've started a [Ciril project on
Github](https://github.com/mnemote/ciril/) for this which has more
information and which I'll update as I go along.

Why so small?
=============

The eventual aim is for dimensions of approximately 1 cubic inch (25 x
25 x 25 mm = 16 cubic centimeters), but the immediate goal is
approximately 40 x 40 x 40 mm (4 cubic inches).

The intention is to be a size which is easy for a small child to pick up
one-handed and which is small enough to explore line following and so on
experiments on a desktop sized platform (approx 1m\^2)

Prototype
=========

The prototype uses two 10mm stepper motors (from Ebay), along with four
[L9110S](http://www.elecrow.com/download/datasheet-l9110.pdf) to drive
them. There's also a [NodeMCU](http://nodemcu.com/) in the box, with an
ESP-12E module on board. And Lego wheels.

![ciril prototype](ciril-proto.jpg)

The kinematics need a lot of work, but I'm amazed by how much torque the
tiny motors have ...

Alternatives
============

Direct driving the wheels is a bit ... minimalist. The size of tyre
they're able to drive is very limited and the stub axle is under a lot
of load.

![ciril big-wheels render](ciril-wheels.png)

As an alternative, perhaps 3D-printed wheels with an internal gear and
an O-ring groove around the outside. They take up a lot of room
internally, but perhaps the axle could be offset downwards and the
wheels made a little smaller.

The motors can also be offset to make a bit more room. The wasted
'cheeks' on either side of the wheels could be occupied by LiPo cells.

Links
=====

-   [Flobot project](http://github.com/mnemote/flobot).
-   [Ciril project](https://github.com/mnemote/ciril/).
