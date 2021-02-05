---
date: '2021-01-28'
layout: article
tags:
  - micropython
  - microcontrollers
  - electronics
title: 'RPi Pico: First impressions'
summary: 'My first impressions of the new Raspberry Pi Pico / RP2040, with MicroPython'
---

# First Impressions

I received a couple of
[Raspberry Pi Pico](https://www.raspberrypi.org/documentation/pico/getting-started/)s
this morning from [Little Bird Electronics](https://www.littlebird.com.au/)
and this is a quick write up of the out-of-box experience.

## Booting and Flashing

As expected from RPi, the web documentation is fantastic.  Right there on the site
from day one is a
[Getting Started with MicroPython](https://www.raspberrypi.org/documentation/pico/getting-started/)
page, which is great to see.  Downloading the UF2 file and copying it to the
board (it appears as a mass storage device) takes only a moment, and as soon
as it reboots a familar `/dev/ttyACM0` is available.

```
MicroPython v1.13-290-g556ae7914 on 2021-01-21; Raspberry Pi Pico with RP2040
Type "help()" for more information.
>>> 
```

*I haven't tried this on Windows / Mac just yet but hopefully it will work in 
much the same way as [other MicroPython boards](http://mpy-tut.zoic.org/tut/installing.html)*

Unfortunately the mass storage interface is no longer available!  This is a pity
because this is a great feature especially for beginners.  If that's you, I'd
recommend checking out
[Adafruit's CircuitPython fork](https://circuitpython.org/board/raspberry_pi_pico/)
instead until MicroPython gets this going.
More on that later.

```
Adafruit CircuitPython 6.2.0-beta.1 on 2021-01-27; Raspberry Pi Pico with rp2040
>>> 
```

The board itself it pretty minimal: there's a single green LED on GPIO25, so at
least we can run Embedded Hello World:

```
import machine
import time

led = machine.Pin(25, machine.Pin.OUT)
while True:
    led.toggle()
    time.sleep(1)
```

## Pinouts

![RPi Pico Pinout](img/Pico-R3-Pinout.svg)
*From [raspberrypi.org](https://www.raspberrypi.org/documentation/pico/getting-started/)*

What might not be clear from this diagram is that there's two each of the
UART, SPI and I2C ports, and they can be moved around between different sets of pins,
but not to totally arbitrary pins.  So you can have a combination of those busses, but
not all of them all at once.  It seems like an odd way to do things but perhaps it
will make board layouts simpler.

*See Section 2.19.2 in the [RP2040 Datasheet](https://datasheets.raspberrypi.org/rp2040/rp2040-datasheet.pdf) and once again curse the world of PDF documents and their inability to play
nicely with hyperlinks*.

The good news is that the USB connection is direct via it's own PHY so unlike the 
a lot of microcontroller boards you don't lose a serial port the console.

The Pico is surface mountable to your own boards too, or there's a various smaller
boards available 
and a [Feather compatible board is on the way](https://www.adafruit.com/feather2040).

## Where does this sit in the market?

With 2 x 144 MHz ARM cores and 264 KB of SRAM, it's a lot more powerful than 
an AVR based Arduino, and the boards are really quite cheap.

It's a pretty direct competitor to the
[ESP32](/tag/esp32/) and similar chips, but without the WiFi interface.

Will it be able to gain the kind of critical mass which has built up around those
platforms?  Only time will tell.

