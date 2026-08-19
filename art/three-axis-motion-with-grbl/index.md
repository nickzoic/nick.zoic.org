---
title: Three-axis motion with GRBL
summary: getting three stepper stages to work with GRBL software and drivers
layout: draft
---

For an upcoming project I want to get three axis motion working with
stepper motors and linear stages which use a trapezoidal thread to move 
in a very accurate way.

## Stepper Stages

I used [these stages](https://www.ebay.com.au/itm/358054743590) which
have a NEMA11 motor and a Tr6-2 thread (1mm pitch, double start),
resulting in 100 steps per mm.  As shipped the end plates were a little
misaligned, and needed to be properly set up[^1].

[^1] loosen the two screws, send the stages out to the end
of their travel and then tighten the end screws again.  No more problem!

## GRBL board

I combined them with this [GRBL driver board from Ebay](https://www.ebay.com.au/itm/234270397356).
In the photos it is identified as `LY-GRBL3-10086-V11` but the
board as shipped is identified as `LY-3Axis-4.0-V2.0`.
It is otherwise the same.

![the board](img/board.png)
![back](img/back.jpg)

It shows up as a USB device with identifiers `0483:5740 STMicroelectronics Virtual COM Port`
and device strings `Product: LUNYEE_4axis_Control` and `Manufacturer: tomeko net`.
In Linux it appears as `/dev/ttyACM0` (etc).

The `$I` command reveals it is running a custom build of GRBL 1.1f:

```
Monport
[VER:1.1f.20230316:����������������������������������������������������������������]
[OPT:VMZHL,35,254]
```

### Stepper Drivers

The board comes pre-populated with three `A4988` drivers.
They have little heatsinks and [current limit trimpots which
need to be set up](https://ardufocus.com/howto/a4988-motor-current-tuning/)

As shipped the board has all three [stepper driver jumpers populated](https://software.farm.bot/v7/Device/arduino-firmware/microstepping.html),
meaning each step is 1/16th of a real step.
So we get 1600 microsteps per mm.

### GRBL Settings

GRBL keeps a bunch of [settings](https://github.com/gnea/grbl/blob/master/doc/markdown/settings.md) 
in NVRAM and these are the ones I changed:

Setting | Purpose | Stock Value | New Value
---|---|---|---
$3 | Direction Invert (X,Y,Z) | 6 (invert Y and Z) | 3 (invert X and Y)
$20 | Soft Limit enable | 0 | 1
$27 | Homing pull-off, mm | 2.000 | 1.000 
$100, $101, $102 | X,Y,Z steps per mm | 800,800,800 | 1600,1600,1600
$110, $111, $112 | X,Y,Z max rate | 2000,2000,100 | 2000,2000,2000
$130, $131, $132 | X,Y,Z limit | 500,500,200 | 100,100,100

The stages are actually about 103mm long so by keeping the limit switch activation
point about 1mm from the end and reducing homing pull-off to 1mm the stage limits are 
a very neat 0 - 100 mm.

For some reason the Z axis is inverted in hardware, I checked my stepper wiring many times
and it just is.  So I invert X and Y to match, so that 0 is with the stage at the stepper end
and 100 is with the stage at the far end.

### Axis Connectors

Each axis has it's own [JST XH2.5](https://electronics.alibaba.com/buyingguides/xh2.54-connectors-what-you-actually-need-to-know)
with the following pinout.

Pin | Phase | Header Color | Stepper Color |
---|---|---|---
1 | A- | Grey | Red |
2 | A+ | Blue | Blue |
3 | B- | Purple | Green |
4 | B+ | White | Black |

Except Y2 which has the pins opposite for some reason, but I'm not using that one.

The steppers had bare wires and I had some spare pre-wired headers so I just made up some frankencables.
Using motors with pre-installed connectors would save a lot of messing about with solder.

### Limit / Home switches

When the board first wakes up, it doesn't know where the stepper stages are positioned.
So it has to perform a homing cycle, and to do that it needs some switches to tell it when
each axis is 'home'.

These wire to two-pin "dupont" connectors on the board.  For now I've just used microswitches
in a 3d printed plastic carrier which clips to the stepper.

### Board Power

The stepper drivers are powered from the DC connector, 5.5mm OD / 2.5mm center positive, 7 - 36V.  
I found a 19V 4A supply to suit.
Don't forget to turn on the switch.

The logic is, or at least can be, powered from the USB-C port while the motor power is off.
There are a number of other power connectors on the board whose purpose is not entirely clear but
is presumably for spindles, lasers, etc.

There are three red power LEDs on the board which might be helpful to know about:

![leds](img/leds.png)

* A: Motor Power labelled `PWR`
* B: USB-C Power (no label)
* C: Either Motor or USB-C Power labelled `3V3`

There's two LEDs at C which are labelled `3V3` and `RUN` on my board and opposite on the
one pictured at EBay.  

## Does it work?

Yes!  The three axis can be controlled independently or together using G-Code commands.
Note that GRBL starts a homing cycle with `$H` instead of the more common `G28`.

![image](img/image.jpg)
