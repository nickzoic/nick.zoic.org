---
title: "Geeetech A20T: First Prints"
date: '2023-08-02'
layout: draft
summary: "First prints on the Geeetech A20T"
tags:
  - 3dprint
---

I've written about [Assembly and configuration of the Geeetech A20T 3D printer](/art/geeetech-a20t-assembly-and-configuration/) and also [Multi-Material 3D Printing With OpenSCAD, Cura and the Geeetech A20T](/art/multi-material-3d-printing-openscad-cura-geeetech/) 
and now it's time to actually print something!

## Straight out of the box

The SD card which came with the printer contains a couple of G-Code files
which I assume are tuned up for the printer.

## Setting up a Cura Profile

I've started off using the
[Ultimaker Cura](https://ultimaker.com/software/ultimaker-cura/) 5.4.0
built-in profile for this printer.

### First Boats

I tried printing off a [Benchy](https://www.thingiverse.com/thing:763622)
using three PLA filaments: blue for the main hull, orange for the trim and white
for the infill.  I just used the default profile for this.

![Boat1](img/boat1.jpg)
![Boat2](img/boat2.jpg)
*Not a very successful Benchy*

It didn't work very well.  The boat is a mass of ooze, the colours are 
all jumbled up, and the colour change tower hit the nozzle, broke off the
build plate and then jammed between the boat and the print cooling fan, 
causing the Y motor to skip and misalign.  I stopped it not long thereafter.

Clearly some work needs to be done.  It looks like the temperature is 
far too high, with liquid blobs all over the place, and also the
retraction is far too short and/or too fast ... it is a mess of 
spiderwebs.  Also the support has bonded far too strongly to the print
and is impossible to remove.
