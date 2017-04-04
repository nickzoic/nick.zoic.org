---
category: etc
date: '2016-03-25'
layout: article
redirect_from: '/etc/nodemcu-plus-plus/'
slug: 'nodemcu-plus-plus'
summary: 'Improving on the design of the NodeMCU modules ...'
tags:
    - robots
    - microcontrollers
    - electronics
title: 'NodeMCU++ ?'
---

NodeMCU {#nodemcu-1}
=======

I've been using [NodeMCU](http://nodemcu.com/index_en.html) boards for a
couple of ESP8266 projects, and they're certainly a very easy way to get
into ESP8266. The NodeMCU module contains an
[ESP-12E](http://www.esp8266.com/wiki/doku.php?id=esp8266-module-family#esp-12-e_q)
module and a
[CH340](https://www.olimex.com/Products/Breadboarding/BB-CH340T/resources/CH340DS1.PDF)
USB-to-serial chip.

However, this is also the least satisfying aspect of the NodeMCU
experience. The USB interface appears as a generic serial port, with all
the attendant baud-rate configuration issues, and while
[esptool](https://github.com/themadinventor/esptool) and
[luatool](https://github.com/4refr0nt/luatool) work very well, having
the host upload code at 9600 bits per second is *rather* frustrating.

Clever [use of the DTR and RTS
lines](https://raw.githubusercontent.com/nodemcu/nodemcu-devkit/master/Documents/NODEMCU_DEVKIT_SCH.png)
allow the host computer to reset and reflash the ESP

Additionally, while the USB port is disconnected, the CH340 is still
using up space and power to no purpose.

An alternative
==============

As an alternative, a small USB-enabeled CPU such as an
[ATMega8U2](http://www.atmel.com/devices/ATMEGA8U2.aspx) with
[LUFA](http://lufa-lib.org/), or even an
[ATtiny167](http://www.atmel.com/devices/ATTINY167.aspx) with
[V-USB](https://www.obdev.at/products/vusb/index.html) could be used.
The ESP would still be the 'primary' CPU, but the AVR would provide USB
interfacing and additional functionality.

This chip would interface between the USB host and the serial
programming port of the ESP8266, manipulating the same "reset" and "boot
mode" pins as the CH340 solution does. But rather than presenting to the
USB host OS as a serial port, it would present a more sophisticated and
controllable interface, with ioctls to control its behaviour. A
user-space driver could then even expose the contents of the ESP flash
as a file system.

The AVR controllers also have plenty of nice onboard I/O, so the chip
could continue to be useful while disconnected. Simple serial port
commands from the ESP to the AVR could read and write individual pins on
the AVR, or use the AVR to provide stepper motor control.

Trying it out
=============

I've got a few [ESP-12F](http://tech.scargill.net/esp-12f/) in the box,
and I bought a couple of [DigiSpark](http://digistump.com/products/1)
modules, which look like a good place to start with V-USB. I'll update
this page as I go along.

Eventually, this work may feed in to the [Cubic Inch
Robot](http://ciril.mnemote.com/) project.
