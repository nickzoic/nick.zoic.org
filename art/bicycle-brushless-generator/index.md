---
layout: draft
draft: 2025-11-24
title: Bicycle brushless generator experiment
tags:
  - cycling
  - electronics
  - not-computers
---

Keeping lights and gadgets charged on the bike is tricky.
There's only so many battery packs you can carry around.
Solar isn't really pracical on a 2-wheeler.
But there's power to spare when you're rolling down a hill.
So dynamos are a popular option.  

Front wheel hub dynamos are cool, but you need to rebuild the
whole wheel around them.
Those old school [bottle dynos](https://en.wikipedia.org/wiki/Bottle_dynamo)
are heavy and bulky.
There's modern looking alternatives like 
[Velogical](https://www.velogical-engineering.com/dynamo/product-information/?lang=en)
dynamos but they're expensive for something I'm not sure
I'll use much.

## Brushless motors

A motor turns electricity into movement, and a generator turns movement
into electricity, but they're pretty much the same device.

Brushless motors have come a long way in the last few years,
driven by the popularity of tiny drones.
So maybe we can use one backwards as a generator.

A typical brushless motor is a 1503, which has an 18mm OD external rotor,
which holds a ring of permanent magnets.
There's a three phase stator inside, 
the "1503" is because the stator is 15mm OD x 3mm thick, maybe.
It's surprisingly difficult to find engineering diagrams of these motors.

In flight these things rev to 19,000 RPM and move an amazing amount
of power for their size.

## On the bike

Maybe we can put a little tyre on the outside of the rotor 
and press it into the rim.  Call that 3mm thick, so a 24mm OD,
so about a 75mm circumference.

Doing the maths, at a typical 20 km/h the motor is turning about
4500 RPM, which is pretty slow for this kind of motor.
It won't reach its RPM limit until 85 km/h or so, which is
pretty unlikely even downhill on a laden pushbike.

Some kind of bracket could pick up on the rear brake bridge
if there is one (the bit between the seat stays)

* Wheel circumference for a 700x40c = 2200mm
* at 60kmph = 1000 m/min, that's about 455 RPM

rated to 19krpm

+ wheel + o-ring tyre = 24mm dia = 75mm circumference

track circumference ~= wheel circumference
(actually a little bit less but whatever)

1000 m/min / 75mm = 13333 RPM

## Electronic Limit

In theory it doesn't matter what voltage the generator puts out:
power = volts * amps so you can get the same amount of power out
with a lower voltage and a higher current.  But in practice the
voltage out of the generator has to be rectified, which means 
that there's a couple of diodes in the way, causing a ~600mV 
voltage drop.  If the generator is only putting out 1V, then 
half the power is being lost in the rectifiers!

[2212 Brushless Motor 1000KV](https://www.temu.com/goods.html?goods_id=601103209840102&sku_id=17608591017152)

"1000KV" is an odd unit, it means 1000RPM per volt.
