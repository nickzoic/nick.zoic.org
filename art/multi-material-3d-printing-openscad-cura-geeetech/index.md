---
title: Multi-Material 3D Printing With OpenSCAD, Cura and Geeetech
date: '2023-07-17'
layout: draft
summary: "How to do multi material 3D printing with OpenSCAD and Cura and a Geeetech A20T"
tags:
  - 3dprint
  - python
---

I've been messing around with my [cheapo printer](/art/aldi-coccoon-3d-printer/)
for a few years now and I'm considering upgrading to a new one, particularly to
print with multiple filament colours.

I mostly use [OpenSCAD](https://openscad.org/) to design
[stuff](https://github.com/nickzoic/models3d/) and
[OpenSCAD support for multi materials is not good](https://github.com/openscad/openscad/issues/1608).

It'd be great to fix that, but in the meantime I needed a quick solution.
[Erik Nygren has made a good start](https://erik.nygren.org/2018-3dprint-multicolor-openscad.html)
but I wanted to get something working with
[Ultimaker Cura](https://ultimaker.com/software/ultimaker-cura/) and
without having to save a whole lot of separate 
[STL](https://en.wikipedia.org/wiki/STL_%28file_format%29) files.

I've been considering the
[Geeetech A20T](https://www.geeetech.com/geeetech-a20t-triple-color-mixing-filament-detector-breakingresuming-250x250x250mm-p-1108.html).
It has three extruders feeding into a single nozzle.
On Youtube, there's a 
[Geeetech A10M review at Teaching Tech](https://www.youtube.com/watch?v=AbZhNvMM4Os) and [six Geeetech A10M upgrades at Teaching Tech](https://www.youtube.com/watch?v=8o--HmfZ57I)
which git you some idea of how these printers work.

The printer has three physical extruders, and some built in
firmware to do mixing and fading between the extruders.

# G-Code

I think it can be set up in Cura to have up to
[8 or maybe 16 virtual extruders](https://community.ultimaker.com/topic/41834-can-i-add-more-than-8-extruders-in-cura/)
each of which is a different blend of the three actual extruders, 
set up in the printer settings G-code using the 
[M163](https://marlinfw.org/docs/gcode/M163.html) and
[M164](https://marlinfw.org/docs/gcode/M164.html)
commands. 

**Note that G-code standardization is quite broken across
different brands of printer and different firmwares.  There's 
multiple interpretations of even basic stuff like tool
changes and lots of optional features which your printer
may or may not support.**

For example these commands select a 50/30/20 mix of the three
filaments in the real extruders 0, 1 and 2, and assign that
mix to a "virtual tool" 3:

```
M163 S0 P0.5
M163 S1 P0.3
M163 S2 P0.2
M164 S3
```

Once these virtual tools are set up, Cura will automatically
use them for the different extruders using the tool change
commands `T0` .. `T7`.  So by fiddling with the "Start G-Code"
in the printer settings, you can set up several extra
colour mixes so for example this sequence would set up
tools 3 through 7 as mixes of tools 1 and 2 (the second
and third filaments), so you could for example load white,
red and blue and print in white and several shades of purple.

```
M163 S0 P0
M163 S1 P0.84
M163 S2 P0.16
M164 S3

M163 S0 P0
M163 S1 P0.67
M163 S2 P0.33
M164 S4

M163 S0 P0
M163 S1 P0.5
M163 S2 P0.5
M164 S5

M163 S0 P0
M163 S1 P0.33
M163 S2 P0.67
M164 S6

M163 S0 P0
M163 S1 P0.16
M163 S2 P0.84
M164 S7
```

Using [M166](https://marlinfw.org/docs/gcode/M166.html)
should let you assign a Z-gradient to a tool as well!
