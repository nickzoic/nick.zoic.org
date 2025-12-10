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

## Dynamos

Front wheel hub dynamos are cool, but you need to rebuild the
whole wheel around them.
Those old school [bottle dynos](https://en.wikipedia.org/wiki/Bottle_dynamo)
are heavy and bulky.
There's modern looking alternatives like 
[Velogical](https://www.velogical-engineering.com/dynamo/product-information/?lang=en)
dynamos but they're expensive for something I'm not sure
I'll use much.

So I thought I'd look into making my own.

## Brushless motors

A [brushless motor](https://en.wikipedia.org/wiki/Brushless_DC_electric_motor#Brushless_solution)[0]
works pretty simply:

* A *current* flowing through the *stator* produces a magnetic field, which interacts
  with the *rotor*'s permanent magnets and causes a *torque* on the rotor.
* The *rotor* rotates, and the interaction of the moving magnetic fields induces a 
  *voltage* in the stator, in the opposite direction to the current.

An AC generator works the same way but in the opposite direction:

* As the *rotor* rotates, it's magnetic field induces a *voltage* in the stator
* The load *current* produces a magnetic field in the *stator*, which interacts with
  the *rotor* and causes a *torque* on the rotor, in the opposite direction to its rotation.

[0] There are other kinds, but let's stick to this one.

## KV

These sorts of motors are rated in `KV`, which doesn't stand for kilovolts (`kV`),
and doesn't measure how *powerful* the motor is, it's more like how it is geared.
It's short for "RPMs per Volt"[1], so a `1000KV` motor spinning at 1000 RPM will
generate about 1V [2], and spinning at 5000 RPM will generate about 
5V peak-to-peak.
Different KV ratings suit different sizes of battery pack and propeller.

[1] Dimensional analysis time: that's `$ s^-1 V^-1 $` which we could call
    `$ C s^-1 J^-1 $` or `$ A J^-1 $`.  Amps per Joule?  Doesn't really
    help us very much.

[2] Peak to peak?  Per phase?  This isn't very well documented.

In this application we actually want a small number, because that will get us
the most voltage per RPM, which is desireable because both high RPM and low
voltage lead to losses.

## 2212 motors

Brushless motor technology has come a long way in the last few years,
driven by the popularity of tiny drones.
So maybe we can use one backwards as a generator.

A common type of brushless motor found in drones etc is the `2212` motor.
This number comes about because the stator is 22mm in diameter and 12mm in 
axial length.
The stator is on the inside of the motor, and the rotor is a thin shell of
magnets surrounding it.

2212 motors seem to be available from all the usual hobby and direct import
source, with ratings ranging from about 900KV to 3500KV and costing around
AUD10 - AUD20.

Engineering diagrams are suprisingly hard to find but here's some info:

* [rhydolabz](https://www.rhydolabz.com/documents/26/BLDC_A2212_13T.pdf)
* [2212 Brushless Motor 1000KV](https://www.temu.com/goods.html?goods_id=601103209840102&sku_id=17608591017152)

## Three phases

These motors are "three phase" ... there's three wires, and three windings,
arranged in a [Y configuration](https://en.wikipedia.org/wiki/Three-phase_electric_power#Wye_(or,_star;_Y)) 
with no access to the "neutral".  

Three phases seems a bit over the top, but think of single phase like pedalling
a bike: there's dead spots at the top and bottom of the pedal stroke where neither
foot is well-aligned to push.
Three phase is like if you had three feet on each side, and three pedals on each side.
There would always be one of your six feet in the right place to put power down,
leading to a smoother power output and higher efficiency.

## On the bike

Maybe we can put a little wheel on the rotor and press it into the rim.
The very high ratio of bicycle wheel size to generator wheel size leads to 
very high RPM at the generator.
The generator wheel might be 20mm across, call it 63mm circumference.
If the bike is rolling at 18 km/h = 5 m/s that going to be about 80 RPS = 4800 RPM.

At 4800 RPM, we should be getting about 4.8 Volts peak.
On paper.
In practice there's going to be all sorts of losses, but that's a start.

From there we can rectify the three phases into a capacitor, and then use that
stored energy to run lights or charge a battery pack etc.

## ... and off the bike

Testing on the bike is awkward, but I have a handy drill press which has several
selectable (belt driven!) spindle speeds up to 2500 RPM, so if I wanted to 
simulate a wheel going 50 km/h = 14 m/s I could mount a disc about 107mm in
diameter into it and use that as a "rolling road" at various speeds.

## Rectification

To power lights etc we first need to *rectify* our 3-phase AC into DC.
[This is a good primer on 3 phase recification](https://www.electronics-tutorials.ws/power/three-phase-rectification.html).
We don't have a neutral terminal on these motors so we'll use full wave
rectification.  That means six diodes, and our current will be flowing through
two of them at any moment.  

Each diode introduces a voltage drop, so we'll use a 
[Schottky Diodes](https://en.wikipedia.org/wiki/Schottky_diode)
like the 
[1N5819](https://www.st.com/content/ccc/resource/technical/document/datasheet/26/db/14/60/52/47/47/5b/CD00001625.pdf/files/CD00001625.pdf/jcr:content/translations/en.CD00001625.pdf)
which has a relatively low voltage drop of 550mV at 1A.

That's still 1.1V lost just in the rectifiers!  An alternative would be to 
try out [synchronous rectification](https://en.wikipedia.org/wiki/Active_rectification)
but designing a circuit around six mosfets and six opamps is out of my depth.

Once the AC voltage is rectified into DC, power can be used to charge a capacitor or
a battery via a buck / boost converter.



