---
date: '2020-09-04'
layout: draft
tags:
  - micropython
title: 'Lilygo T-Watch 2020'
---

[Lilygo, aka Shenzhen Xin Yuan Electronic Technology Co., Ltd](http://lilygo.cn)
were kind enough to send me some samples of their new watches: well,
wrist-mounted computers, really.

# Lilygo T-Watch 2020

The first one I'm going to look at is the T-Watch 2020, the latest of their
wristwatch devices.  It's a bit chonky, the body is 49mm x 40mm by 12.7mm thick, 
but the edges are round and the black plastic back makes it seem a little less
so.
Even though I don't generally wear a wristwatch, it's light enough to not feel weird.

On board is an [ESP32](/tag/esp32/) microcontroller (specifically ESP32D0WDQ6),
16MB of flash memory and a bunch of peripherals.
Under a little thumbnail-removable cover on the side is a standard MicroUSB port
for charging, and attached to a standard CP210x-type UART.
There's a little cable supplied but it's accessible enough that you can use a
normal microUSB cable.

Under the back cover you can see a tiny speaker and even a removable battery!
Remarkable in a device this small, please pay attention phone manufacturers!

Out of the box it's running some firmware which looks like a watch and lets
you set scan WiFi and so on but I didn't really look much more at it,
because that's not what we're here to talk about: what's fun about this device 
is that it can run [MicroPython](/tag/micropython/).

(This trail has been broken by [y0no](https://y0no.fr/posts/micropython-ttgo-twatch2020/)
[(en translation)](https://translate.google.com/translate?hl=&sl=auto&tl=en&u=https%3A%2F%2Fy0no.fr%2Fposts%2Fmicropython-ttgo-twatch2020%2F) and
[mooond](https://gitlab.com/mooond/t-watch2020-esp32-with-micropython/-/wikis/home)
but I thought I'd give it a go too)

# MicroPython

First things first: I build the newly released MicroPython 1.13 for ESP32,
plugged in the watch and flashed it the usual way.

It doesn't do much like this: you can connect to the serial port and get a 
Python prompt, but that's not very useful.

## Proof of Life

First things first: is this device really working?
There's a [technical document for T-Watch 2020](https://t-watch-document-en.readthedocs.io/en/latest/introduction/product/2020.html)
which includes lots of great information, including 
peripherals and pinouts.
Starting with the most basic "proof of life", GPIO4 is attached to the
vibration motor, so we can pulse that GPIO and see what happens

```
import machine
import time
p = machine.Pin(4, machine.Pin.OUT)
p(1)
time.sleep(1)
p(0)
```

Yep, that buzzes for 1 second!  Can we do more?

```
import machine
pp = machine.PWM(machine.Pin(4))
pp.freq(10)
pp.duty(1)
```

The GPIO signal doesn't seem to drive the motor directly, but by using a really low
duty cycle and varying the PWM frequency between 5 and 30 Hz you can make a variety
of different vibrations at least ... potentially handy.

Likewise, GPIO12 is the display backlight: you can PWM it at 100Hz and set the
background brightness with the duty cycle.

```
import machine
pp = machine.PWM(machine.Pin(12), freq=1000, duty=512)
```

It's a bit confusing to try to work out which pin is which internally, as 
some of the docs are mixed up between the older, expandable watch and this 
current model.
[This pin map on github](https://github.com/Xinyuan-LilyGO/TTGO_TWatch_Library/blob/master/docs/pinmap.md) is possibly the best guide.
It doesn't list GPIO 12 though, which I've confirmed is a backlight pin.

The button on the side, which looks like a little crownwheel but isn't,
is attached to Pin 36 on older watches but doesn't seem to be attached to
anything on this model, which is a bit annoying.  If you hold it down for 
a few seconds it toggles the watch on and off though, which is handy.

## I2C

There's several I2C peripherals listed at various pins: let's see if we can
find them.

```
>>> import machine
>>> i0 = machine.I2C(sda=machine.Pin(21),scl=machine.Pin(22))
>>> i0.scan()
[25, 53, 81]
>>> i1 = machine.I2C(sda=machine.Pin(23),scl=machine.Pin(32))
>>> i1.scan()
[56]
```

According to the sites linked above, these should be (respectively):

* BMA423 Accelerometer
* AXP202 Power Management
* PCF8563 RTC
* FT6236U Touch Sensor

### RTC

The simplest device we can talk to is the RTC: so simple we don't really
need a library to get started.  We can just read out registers 2, 3 and 4 
over I2C to get the seconds, minutes and hours:

```
import machine
import time
i0 = machine.I2C(sda=machine.Pin(21),scl=machine.Pin(22))
while True:
    s, m, h = i0.readfrom_mem(81, 2, 3)
    print("%-02s:%-02s:%-02s" % (h,m,s))
    time.sleep(1)
```

... and this seems like it probably works, until ...

```
19:16:55
19:16:56
19:16:57
83:16:64
83:16:65
83:16:66
83:16:67
83:16:68
```

... it turns out that these values are in BCD, and have some
spare bits besides.  Correcting for that:

```
import machine
import time
i0 = machine.I2C(sda=machine.Pin(21),scl=machine.Pin(22))
while True:
    s, m, h = i0.readfrom_mem(81, 2, 3)
    print("%d%d:%d%d:%d%d" % ((h>>4)&3, h&0xF, (m>>4)&7, m&0xF, (s>>4)&7, s&0xF))
    time.sleep(1)
```

... we get much more sensible results:

```
13:16:55
13:16:56
13:16:57
13:16:58
13:16:59
13:17:00
13:17:01
13:17:02
13:17:03
13:17:04
13:17:05
```

We're probably better off using a library for the RTC, but it's nice to know
we can talk to it from MicroPython if we have to!
