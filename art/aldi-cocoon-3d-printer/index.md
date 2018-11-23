---
title: Aldi "Cocoon Create" 3D Printer
date: '2018-11-23'
layout: article
summary: "A pretty nifty little printer"
tags:
  - 3dprint
---

# Hardware 

I picked up a "[Cocoon Create Model Maker](https://cocoonproducts.com.au/model-maker/)"
printer from Aldi the other day, on sale for $300.  It's a pretty direct copy of a 
[Wanhao Duplicator i3 Mini](http://www.wanhao3dprinter.com/Unboxin/ShowArticle.asp?ArticleID=88)
but with the advantage that you can drive up to the shops and grab one, and it is
covered by Aldi's excellent warrantee support.

I've been meaning to have a go at
3d printing for years now, and in fact there's an elderly and rather dodgy Prusa i3
sitting on the shelf, but I never did get anything to actually work properly despite
hours of messing about and replacing parts.

So I bought this nifty little printer.  It is rather small, and has a quite limited
print volume of 120 wide x 135 deep x 100 high.  But it worked straight out of the box
and that's pretty impressive.  It is fully assembled, very quick to unpack and in the box
is also a scraper, and a glue stick, and spare magnetic beds, and a few lengths of test
filament, and a micro SD card with some 
pre-prepared models, so you really can level the bed and print a test or two without
anything else, although I picked up a kilo of PLA filament while I was there.

![Unpacking the Printer](printer1.jpg)

The printer has a small controller built in, with a little backlit multi-line LCD and a 
rotary dial to select stuff.  It can print directly from a microSD card without being
attached to a computer, or it can plug into your computer to print from host software.
[Ultimaker Cura](https://en.wikipedia.org/wiki/Cura_(software)) is included on the SD card
as well.

On the downside: it is fairly noisy, with both hot-end cooling fan and the processor 
cooling fans making a racket.  Neither fan is under software control, so they keep
running even when the printer isn't doing anything.  And there's no heated bed.

# Firmware

The main problem I've had though is the built-in driver software, which occasionally 
crashes while the head is heating up, and has some really terrible user interface.
The control knob detents seem to have no correspondence to UI transitions, and the 
whole UI seems quite badly thought out, with meaningless menu structures and so on.
But it works well enough to be used, so I guess that's okay.

I haven't tried upgrading the firmware yet, but it seems pretty likely it is based
on the Open Source [Marlin](http://marlinfw.org/) software, not that the Cocoon manuals
document this or anything.  If so, it might be possible to improve it.

# Software

I'm more impressed with Cura, which works great out of the box and comes with the 
printer's profile built in.  I've been running it under [wine](https://www.winehq.org/)
to avoid having to work out how to transfer the profile across to the Linux version.

The design I've been doing in [OpenSCAD](https://www.openscad.org/) which is quite
an interesting way to approach design.
The OpenSCAD syntax drives me a bit nuts so I'm thinking of trying out 
[PySCAD](https://pyscad.readthedocs.io/en/latest/) as well.

# Projects

* I've made a start on 3d models for [Ciril](/art/ciril-cubic-inch-robots-in-labs/)
* I got to print a couple of parts for the latest
  [Heart of Pluto](http://heartofpluto.co/) Colour Changer ... great to be able to
  help out with such a cool project
* I'm hoping to design some bits for our [Water Rockets](/art/rocket-surgery-airborne-iot-telemetry-buzzconf/) 
* I made some keyrings for kids at school ... especially good for the kids with
  less common names! 
* I've made a whole lot of rubbish :-)

I've uploaded some works in progress to [github:nickzoic/models3d](https://github.com/nickzoic/models3d/)	

![Color Changers](changers1.jpg)
![Keyrings](keyrings1.jpg)
![Rubbish](rubbish1.jpg)
