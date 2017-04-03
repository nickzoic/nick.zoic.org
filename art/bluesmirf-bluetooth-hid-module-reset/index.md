---
category: etc
date: '2012-08-22'
layout: article
redirect_from: '/etc/bluesmirf-bluetooth-hid-module-reset/'
slug: 'bluesmirf-bluetooth-hid-module-reset'
tags: 'bluetooth, electronics, keyboard'
title: BlueSMiRF Bluetooth HID Module
---

The [Roving Networks](http://rovingnetworks.com/)
[RN-42](http://www.rovingnetworks.com/products/RN_42) modules are handy
pieces of kit, and can be obtained neatly packaged up as the [SparkFun
BlueSMiRF](https://www.sparkfun.com/categories/115).

The module makes it very easy to interface a microcontroller to
Bluetooth using various of the standard human interface profiles: you
can make your microcontroller act like a bluetooth keyboard, or a mouse,
or a serial port.

Bluetooth HID Keyboard
======================

The [BlueSMiRF HID](https://www.sparkfun.com/products/10938) version
starts up as an imitation keyboard -- it can be paired with a device
just like a normal bluetooth keyboard. ASCII characters sent in the
serial port are transformed into Bluetooth keyboard events.

I'm particularly interested in using this as a way of getting data into
[uncooperative devices](http://www.apple.com/ipad/ios/). This technique
is used by the
[iCade](http://www.thinkgeek.com/files/iCADE/iCade_Dev_Resource_v1_3.pdf)
for example.

Command Mode
============

The RN-42 runs in two modes: "Command Mode" and "Data Mode".

From the [Advanced User
Manual](http://www.rovingnetworks.com/resources/download/47/Advanced_User_Manual)
section 3.1:

> Upon power up the device will be in data mode. To enter command mode,
> send the characters "\$\$\$" through the serial port or from the
> remote Bluetooth connection. The device will respond with "CMD"
> \[...\] You must enter command mode with in the 60 second
> configuration window or the module will go into fast data mode where
> all characters are ignored including the "\$\$\$".

This introduces two problems:

1.  The characters "\$\$\$" could be accidentally sent during the
    configuration window, unintentionally putting the device into
    command mode. This is unlikely to happen by chance, but leaves the
    link vulnerable to an injection attack.
2.  You must enter command mode within the first 60 seconds or lose the
    chance to do so.

The way to get around this is to switch to command mode immediately when
the device starts up, execute any commands you need to and then switch
to "fast data mode", where the RN-42 will ignore the \$\$\$. If you need
to enter command mode again, you have to pull the RESET line low to
reset the device.

As a bonus, which the RESET line is held low, the RN-42 goes into ultra
low power mode, conserving battery power while it is not being used.

Adding a RESET line
===================

Unfortunately, the RESET line isn't brought out to a pin on the
BlueSMiRF board. Fortunately, it is relatively easy to add it.

The module has six through holes at 0.1" pitch, suitable for soldering a
header to. I've soldered in an 8 pin header to provide two extra pins,
and then very delicately soldered a 10K resistor between one of these
spare pins and the RESET pin of the RN-42 module:

![Adding a reset line to the Bluetooth HID
module](%7Cfilename%7C/images/bluesmirf-bluetooth-hid-module-reset.jpg)

The 10K resistor lets you control the 3.3V line from 5V logic, just like
the resistors on the BlueSMiRF board for the RX and CTS lines (see
[schematic](https://www.sparkfun.com/datasheets/RF/BlueSMiRF-Gold-ChipAnt-v1.pdf)).
The pin can then be pulled low from a spare I/O pin on the
microcontroller, causing the RN-42 to shut down into low power mode and
reset when it is brought back up.
