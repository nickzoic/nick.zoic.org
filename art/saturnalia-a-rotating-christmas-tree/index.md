---
date: '2019-12-07'
layout: draft
slug: vrml
tags:
  - esp32
  - silly
  - robots
  - 3dprint
  - micropython
title: 'Saturnalia: A rotating Christmas tree'
---

So we have an enormous, fake Christmas tree.  An eight foot tall monstrosity in 
plastic and steel, which for 11 months lurks under the house in a giant bag,
waiting for December to come around.

## Rotating Table

A couple of years ago I built a rotating table for the tree to sit on, out of a 
cheap lazy susan bearing and a couple of big circles of MDF.
This makes it really easy to wrap tinsel around the tree, and the decorate it
evenly all over, but one side always ends up getting left against the wall, which 
made me think: what if the tree could very slowly rotate on its own?

## Motor Drives

![turntable.jpg](img/turntable.jpg)
![big-gear.jpg](img/big-gear.jpg)

First, I printed off a 117 tooth gear for the base.  It's cut into 9 pieces of 13 teeth
each, and fits exactly around the 305mm outer diameter of the lazy susan bearing.

![printing-big-gear.jpg](img/printing-big-gear.jpg)

I wanted to have the motor components all accessible from on top of the base so the
big gear is actually attached to the stationary base and the motor is attached to
the rotating platform.
The motor mounts through a 51mm round hole in the platform, which allows the smaller gear to 
be on an eccentric so it can be moved in and out a little to adjust the gear clearance.

![motor-mount-small.jpg](img/motor-mount-small.jpg)

First I tried a NEMA-23 stepper I happened to have in the junkbox, directly driving a 7 
tooth pinion.  This worked okay and had plenty of power, but the aim was to turn the tree
quite slowly and at low speeds it wasn't terribly effective.

I also tried out a small 28BYJ-48 stepper, which has a 1:64ish ratio gearbox built in.
While it did an okay job at very low speeds, it had barely enough torque to do the
job.

So with yet more OpenSCAD work I ended up with the following:

![big-motor-3.png](img/big-motor-3.png)

The NEMA-23 motor turns a 7 tooth pinion ('A'), which engages with a large 39 tooth gear 
('B') on the output shaft.
The output shaft is supported by a couple of cheap 6901Z ball bearings and has
another 7 tooth pinion ('C') on the lower end, which drives the 117 tooth gear on the base.

![printing-small-gears.jpg](img/printing-small-gears.jpg)

So overall there's about a 93:1 drive ratio between the stepper and the 
platform.
The stepper is a 1.8⁰ per step or 200 steps per revolution of its output
shaft, so overall that's about 18624½ steps per revolution of the platform.

![gearbox-1.jpg](img/gearbox-1.jpg)
![gearbox-2.jpg](img/gearbox-2.jpg)

The gears need a housing to support them, and that's 3D printed as well.
The lower part contains the eccentric and the seats for the bearings.
The uppoer part contains the motor mount for the NEMA-23 motor.
A couple of wood screws hole the whole thing down the the platform.

[3D Models on GitHub](https://github.com/nickzoic/models3d/)

## Slip Ring

The motor and controller need power to run, and getting power to a continuously
rotating platform isn't easy.
There's a device called a 'slip ring' which allows this to happen using sliding
contacts, and while these are pretty cheap on Ebay I thought it wouldn't quite 
fit the spirit of this junkbox project, so instead I figured that any concentric
connector would do in a pinch.
The most suitable connector was a 6.35mm / 1/4" phono connector, as used in guitar
leads and similar audio applications.  This isn't rated to any particular current
but the contacts are pretty well formed for this sort of thing.

![phono-slip-ring-1.jpg](img/phono-slip-ring-1.jpg)
![phono-slip-ring-2.jpg](img/phono-slip-ring-2.jpg)

Power is supplied from an old laptop charger at 15V, goes to a phono socket 
mounted on the stationary base which sticks up through the rotating platform,
and a right-angle phono plug transmits power to the L293D motor driver module.

## Lights

The tree lights also have to be powered the same way, and so a 5V/3A buck 
converter module is used to supply power to a couple of strings of WS2811 based
LEDs.  These are controlled from the same processor as the stepper driver.
 
![lights-2.jpg](img/lights-2.jpg)

## Software

[Code in MicroPython/ESP32](https://github.com/nickzoic/saturnalia/) controls
both stepper and lights.

A simple web server using [PyCoSe](https://github/nickzoic/pycose/) lets 
the tree be remote controlled from devices on our home WiFi.

## Acknowledgements

Thanks to my family for inspiring and putting up with this strange project and
the terrible state of the loungeroom while I was assembling it ...

![messy loungeroom](img/messy.jpg)
