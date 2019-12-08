---
date: '2019-12-08'
layout: article
tags:
  - esp32
  - silly
  - robots
  - 3dprint
  - micropython
title: 'Saturnalia: A rotating Christmas tree'
summary: "Apparently I have a little too much time on my hands and maybe a little too much enthusiasm for the holiday season"
---

So we have an enormous, fake Christmas tree.  An
[eight foot tall monstrosity](https://en.wikipedia.org/wiki/Yeti)
in plastic and steel, which for 11 months lurks under the house in a giant bag,
waiting for December to come around so it can loom over our living room.

## Rotating Table

A couple of years ago I built a rotating table for the tree to sit on, out of a 
cheap lazy susan bearing and a couple of big circles of MDF.
This makes it really easy to wrap tinsel around the tree, and to decorate it
evenly all over, but one side always ends up getting left against the wall.

Which made me think: what if the tree could very slowly rotate on its own?

Like most silly ideas, it sat and fermented for a while until this year,
finally, I had a chance to put it into action.  Late last year I bought a
[cheap 3D printer](/art/aldi-cocoon-3d-printer/) and I have a bunch of 
random motors and [microcontrollers](/tag/microcontroller/) laying around so
I set out to make it work as much as possible with junkbox parts.

## Motor Drives

The first thing I needed was a way to drive the base.  I thought about belt drives
or adding some kind of gear right around the edge of the platform, but keeping things
aligned seemed like a challenge and I wanted to keep the side load on the
bearing to a minimum.

There's a 10mm gap between the base and the platform though, so there's a little
room in there for the gears.
The bearing has a nicely formed metal edge at 305mm OD, so it seemed natural
to use that as a guide and build the gear around it.

![The turntable platform](img/turntable.jpg)
*The turntable platform*

I quite like working in [OpenSCAD](https://openscad.org/) so I grabbed the excellent
[openscad gears library](https://github.com/chrisspen/gears) and experimented a bit
with [involute gears](https://en.wikipedia.org/wiki/Involute_gear) to pick an 
appropriate [gear modulus](https://en.wikipedia.org/wiki/Gear#Standard_pitches_and_the_module_system)
and number of teeth.

![Big Gear Segments](img/big-gear.png)
*Big Gear Segments*

After some fiddling around with the design, I ended up with a tooth diameter of 335.5mm 
and since the required gear is way bigger than the 120 x 135mm printable area of my printer,
I picked 9 segments of 13 teeth each for a total of 117 teeth.  I printed these 3 at 
a time, and after a couple of bad prints due to broken and jammed filaments I finally
had my full big gear.  There's a real thrill to lining up printed parts and discovering
that they fit perfectly!

![Printing big gear](img/printing-big-gear.jpg)
*Printing big gear*

It fits exactly around the 305mm outer diameter of the lazy susan bearing, with 
three screws holding each segment in place.

![Big gear on base](img/big-gear.jpg)
*Big gear on base*

*pictured: two screws per segment*

*not pictured: yet another trip to the hardware store*

I wanted to have the motor components all accessible from on top of the base in case I need
to fix anything.
So the big gear is actually attached to the stationary base and the motor is attached to
the rotating platform.
The motor mounts through a 51mm round hole in the platform, cut with a hole saw, which allows
the smaller gear to be on an eccentric so it can be moved in and out a little to adjust the
gear clearance.

![Eccentric mount for 28BYJ-48 motor](img/motor-mount-small.jpg)
*Eccentric mount for 28BYJ-48 motor*

First I tried a [NEMA-23 stepper](http://www.piclist.com/techref/io/stepper/nemasizes.htm)
I happened to have in the junkbox, directly driving a 7 
tooth pinion.  This worked okay and had plenty of power, but the aim was to turn the tree
quite slowly and at low speeds it was jerky and not terribly effective.

I also tried out a small [28BYJ-48 stepper](https://web.archive.org/web/20180308144538/https://grahamwideman.wikispaces.com/Motors-+28BYJ-48+Stepper+motor+notes), which has a 1:64ish ratio gearbox built in.
While it did an okay job at very low speeds, it had barely enough torque to do the
job and stalled a lot once the platform was weighed down a bit.  It would probably have been
fine for a more modest tree though.

So with yet more OpenSCAD work I ended up with the following:

![Gear Train](img/big-motor-3.png)
*Gear Train*

The NEMA-23 motor turns a 7 tooth pinion ('A'), which engages with a large 39 tooth gear 
('B') on the output shaft.
There's another 7 tooth pinion on the lower end, which drives
the 117 tooth gear on the base.
So overall there's about a 93:1 drive ratio between the stepper and the 
platform.

The output shaft assembles using a square end and a square socket in the primary output gear.
By making the square end's diagonal just a smidge smaller than the bearing ID it can be assembled 
through the bearings. and the shaft then retains the bearings in their seats.

The primary input gear is currently just press fitted onto the stepper motor shaft and retained with
a little superglue, but i may need to come up with somethng better if it comes loose again --
perhaps a metal collar and grub screw or a keyway ground into the stepper shaft.

The whole thing is sized to use every last mm of the printable area of my printer.
The teeth are a slightly smaller pitch than the secondary gears, but still pretty chunky.

![Printing small gears](img/printing-small-gears.jpg)
*Printing small gears*

The output shaft is supported by a couple of cheap 6901Z ball bearings and has
another 7 tooth pinion ('C') on the lower end, which drives the 117 tooth gear on the base.
The stepper is a 1.8⁰ per step or 200 steps per revolution of its output
shaft, so overall that's about 18624½ steps per revolution of the platform.

![Geartrain in base](img/big-motor-3-2.png)
*Geartrain in base*

![Base mounted on platform](img/gearbox-1.jpg)
*Base mounted on platform*

The gears need a housing to support them, and that's 3D printed as well.
The lower part contains the eccentric and the seats for a couple of cheap
6901Z ball bearings.  These are a nice size to use because they are quite 
compact but the 12mm ID is big enough for a 3D printed driveshaft.

![6901Z bearings](img/bearings.jpg)
*6901Z bearings*

The upper part contains the motor mount for the NEMA-23 motor.
A couple of wood screws hole the whole thing down the the platform.

![Gearbox with cover & motor mount](img/gearbox-2.jpg)
*Gearbox with cover & motor mount*

The secondary pinion is very close to the stationary base, which it is moving
relative to, so I've added a socket for a 8mm ball bearing in the end of the 
pinion.  This prevents the teeth of the pinion from touching the base and 
allows the pinion to glide smoothly over the base surface.  The ball is pressed
into place in a vice and then loosely retained by the socket.

The [3D Models are on GitHub](https://github.com/nickzoic/models3d/tree/master/saturnalia)
although there's still some work to be done.
(Since printing it, I've made the lid a little heavier and added some mounting 
ears just to keep the cover from buzzing)

## Slip Ring

The motor and controller need power to run, and getting power to a continuously
rotating platform isn't easy.

There's a device called a
"[slip ring](https://en.wikipedia.org/wiki/Slip_ring)"
which allows this to happen using sliding
contacts, and while these are pretty cheap on Ebay I thought it wouldn't quite 
fit the spirit of this junkbox project, so instead I figured that any concentric
connector would do in a pinch.

The most suitable connector in the junkbox was a 6.35mm / 1/4" phono connector,
as used in guitar leads and similar audio applications.
This isn't rated to any particular voltage or current
but they're very cheap and the contacts are pretty well formed for this sort of thing.

![Phono plug slip ring socket](img/phono-slip-ring-1.jpg)
*Phono plug slip ring: socket*

![Phono socket and plug](img/phono-slip-ring-2.jpg)
*Phono plug slip ring: plug*

Power is supplied from an old laptop charger at 15V, through the slip ring and
then power goes to the L293D based motor driver and to a couple of 5V/3A buck
converters.  Running the slip ring at a higher voltage lets us run it at a lower
current, hopefully reducing losses and increasing its life.

## Lights

The tree lights also have to be powered the same way, and so a 5V/3A buck 
converter module is used to supply power to a couple of strings of WS2811 based
LEDs.  These are controlled from the same processor as the stepper driver
using the
[MicroPython NeoPixel library](http://docs.micropython.org/en/latest/esp32/quickref.html#neopixel-driver).
 
![WS2811 lights](img/lights-2.jpg)
*WS2811 lights*

The lights themselves are just bought from Ebay and so far I'm very happy with
them.  Each light has its own tiny PCB and controller.  The strings can be connected
together but the wiring is far too flimsy to run more than one string at high
brightness ... later LEDs turn yellowish as the blue LED runs out of voltage to
function.

## Software

This is still very much a work in progress, or to put it another way, it's 
rather janky.

[Code in MicroPython/ESP32](https://github.com/nickzoic/saturnalia/) controls
both stepper and lights.

A simple web server using [PyCoSe](https://github/nickzoic/pycose/) lets 
the tree be remote controlled from devices on our home WiFi.
Yeah, PyCoSe is a bit experimental at this point and I'm mostly using it for
this project to eat my own dog food.

## Further Work

The software needs a lot of work.  I think I might have just dislocated a pinion.
And the lights and baubles are not yet hanging (some of the lights are still in the
mail) and the videos are yet to be shot.  Also I want to add in some more explanatory
text about how the motors and gears work.

If I was starting the design process over again I'd consider using a 
[Cycloidal Drive](https://en.wikipedia.org/wiki/Cycloidal_drive) instead.

If you're interested in following along, [follow me on Twitter](https://twitter.com/nickzoic/)
and I'll post updates and videos and so on there.

## Acknowledgements

Thanks to my family for inspiring and putting up with this strange project and
the terrible state of the loungeroom while I was assembling it ...

![messy loungeroom](img/messy.jpg)

Merry Christmas (etc) to all of you out there in Internetland
and all the best wishes for 2020 `:-)`
