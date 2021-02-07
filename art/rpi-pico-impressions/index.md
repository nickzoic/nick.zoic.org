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

The big drawcard is the
[Programmable I/O](https://www.cnx-software.com/2021/01/27/a-closer-look-at-raspberry-pi-rp2040-programmable-ios-pio/)
which is a programmable, state-machine driven I/O peripheral.
It's really four tiny demi-CPUs which can handle simple I/O tasks,
and potentially offers a way to offload timing-critical activities
like driving NeoPixels.

This idea of having a tiny coprocessor to handle I/O is interesting,
there's a similar thing going on with the
[ESP32 ULP](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/ulp.html)
and it kind of makes sense.

Another option is something like the 
[QuickLogic QORC](/art/quicklogic-qorc-quickfeather-devkit/)
chip which integrates an Cortex M4 and an FPGA, letting you move I/O 
wrangling off the CPU and onto gateware.

Only time will tell if these peripherals prove useful enough to win a place
in the hearts and minds of embedded programmers!

# Building MicroPython

MicroPython is right there on the RPi Pico page as a development platform,
and it's likely that a lot of new RPi Pico users will find it a great
starting point for getting to know the platform.

## Download and Build

The RPi Pico port isn't merged into the main MicroPython repository yet, 
instead you can find it [here](https://github.com/raspberrypi/micropython/)
in the 'pico' branch.

There's instructions for building it [here](https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf), but to summarize:

```
sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential
git clone https://github.com/raspberrypi/micropython/
cd micropython
git checkout pico
git submodule update --init -- lib/pico-sdk
cd lib/pico-sdk
git submodule update --init
cd ../..
make -C mpy-cross
cd ports/rp2
make
```

You should now have a `build/firmware.uf2` file ready to copy onto your device.

## Having another look at WebUSB

One thing which sets these modules apart from the ESP32 etc is the onboard
USB.  I've [written a lot about this](/art/micropython-webusb/) in the past,
the use of serial ports is a serious limitation and a disadvantage to beginners.
A technology like WebUSB could be a great help.

The RP2040 includes a USB PHY, or "Physical Layer", but that's really just
some slightly different IO drivers on two pins, `DP` and `DM`.  There's also
some integrated support for low level USB operations
(see [the RP2040 datasheet](https://datasheets.raspberrypi.org/rp2040/rp2040-datasheet.pdf)
section 4.1)
which should help out with performance compared to using
[V-USB](https://www.obdev.at/products/vusb/index.html) or
[LUFA](http://www.fourwalledcubicle.com/LUFA.php) over GPIO pins.

Instead both the MicroPython and CircuitPython ports use
[TinyUSB](https://github.com/hathach/tinyusb/).
This is great because there's even
[already an example](https://github.com/hathach/tinyusb/tree/master/examples/device/webusb_serial/src/)
in the TinyUSB repository.

Note that the code used in the RP2 build is the version under 
`/lib/pico-sdk/lib/tinyusb/`, which is a fork supporting RP2,
not the general version under `/lib/tinyusb/`.  This will probably
get merged back eventually.

It isn't working perfectly yet but there's a demo of connecting to 
RPi Pico MicroPython via WebUSB [here](/art/micropython-webusb/).