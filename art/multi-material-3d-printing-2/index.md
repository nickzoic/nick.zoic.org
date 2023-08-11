---
title: "Multi Material 3D Printing (part 2)"
date: '2023-08-02'
layout: draft
summary: "More on multi-material 3D Printing"
tags:
  - 3dprint
---

## Mixing

I'm beginning to think I'd be better off with a
[Reprap Diamond](https://reprap.org/wiki/Diamond_Hotend) style
printhead which looks like it has a much smaller internal "mixed" volume,
or maybe just give up and go with
[three separate nozzles](https://www.aliexpress.com/item/32887495430.html)
after all.

Altering the printer so radically might sound a bit crazy but it'd
actually be a fairly simple upgrade I think, so long as you don't mind
having the three nozzles share a heater and thermostat.

Of course, something in my tiny brain is telling me: if you can't decide
between 3 individual nozzles and one three-way mixing nozzle, perhaps you
need a two-way mixing nozzle plus another separate nozzle ... or two
two-way mixing nozzles!  The possibilities are endless.
This way, clearly, lies madness.

## Multiple Settings

The most maddening thing about Cura turns out to be the per-extruder
settings.  It's really easy to set the infill for one material and forget
to change it for the others, for example.  It'd be nice if the UI 
supported this in some way, perhaps by highlighting fields where 
different materials have different values.

## Saving to SD Card

It'd be nice to buffer the print from the PC to the printer, ideally
without having to mess around with OctoPrint.

the [M28 Start SD Write](https://marlinfw.org/docs/gcode/M028.html),
[M29 Stop SD Write](https://marlinfw.org/docs/gcode/M029.html),
[M23 Select SD File](https://marlinfw.org/docs/gcode/M023.html) and
[M24 Start or Resume SD print](https://marlinfw.org/docs/gcode/M024.html)
commands should make this possible by wrapping the g-code in something
like:

```
M28 buffer.gco
; rest of the g-code goes here
M29
M23 buffer.gco
M24
```

I think with this code in place the printer's built-in filament
run-out and power fail resume functions should actually work, too.
