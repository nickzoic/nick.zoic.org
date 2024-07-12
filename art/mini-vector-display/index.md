---
layout: draft
title: "Look Mum No Pixels: a Mini Vector Display"
summary: Making a miniature vector display out of a new/old CRT.
date: '2024-07-09'
tags:
  - electronics
---

## Vector Displays

[Vector Display](https://en.wikipedia.org/wiki/Vector_monitor)
[Vectrex](https://en.wikipedia.org/wiki/Vectrex)

[CRT](https://en.wikipedia.org/wiki/Cathode-ray_tube)

## Micro CRT

There's a bunch of ["Micro CRT"s on Ebay](https://www.ebay.com.au/sch/i.html?_nkw=micro+crt&_sacat=293),
there are a lot of different sellers but they're all pretty much the same as
[the one I bought](https://www.ebay.com.au/itm/404936807399), with a 4 inch 
[Flat CRT](https://en.wikipedia.org/wiki/Cathode-ray_tube#Flat_CRTs)
tube with power supply and composite video circuitry.

The part numbers seem to be `VIS4001D`, `VIS4001EA` or `VIS4001EC`,
with some small differences between them.

<p><table><tr><td>
<a href="img/ebay1.jpg"><img src="img/ebay1t.jpg"/></a>
</td><td>
<a href="img/ebay2.jpg"><img src="img/ebay2t.jpg"/></a>
</td><td>
<a href="img/ebay3.jpg"><img src="img/ebay3t.jpg"/></a>
</td></tr></table>
<em style="display: inline-block; width: 100%; text-align: center">images from Ebay listing</em>
</p>

## Resources

* ["Experiment with Sony flat 4inch CRT"](https://geeseang.wordpress.com/experiment-with-sony-flat-4inch-crt/)
[[archive.org]](https://web.archive.org/web/20230522080743/https://geeseang.wordpress.com/experiment-with-sony-flat-4inch-crt/)
* [tweet by ZxSpectROM](https://twitter.com/ZxSpectROM/status/1407363271171186695)
* [Jerry Walker on youtube](https://www.youtube.com/watch?v=mh_9LUYnDv0)
* [DiodeGoneWild on youtube](https://www.youtube.com/watch?v=l9CXZXSwG7I)

## Connectors

There's a six-pin connector for brightness/contrast pots, and a 4 pin 
connector for power and composite video.  JST XH? 

## Power

The sticker on the side of the assembly says `DC12V,4.0W`.

[This tweet](https://twitter.com/ZxSpectROM/status/1408460498882940934) 
includes an infrared image of the board with the three-terminal TO220
regulator clocking in at 56.3⁰C, which suggests that a
large proportion of the 4W power consumption is getting radiated from
that device alone.

![flir.jpg](img/flirt.jpg)
*Image: [ZxSpectROM on Twitter](https://twitter.com/ZxSpectROM/)*

By contrast, the tube itself and the "may cause mortal damage" HV power
module seem to run fairly cool.
This is good because I'll want to make a 3D printed housing for this thing
eventually.

## Displaying Composite Video

[RPi Composite Video](https://en.wikipedia.org/wiki/Raspberry_Pi#Video)

You can also get composite video out of a RPi Pico, with a bit of trickery
([1](http://www.breakintoprogram.co.uk/projects/pico/composite-video-on-the-raspberry-pi-pico),
[2](https://areed.me/posts/2021-07-14_implementing_composite_video_output_using_the_pi_picos_pio/))

## Taking Control

But what I *actually* want is to control the horizontal and the vertical
and the beam intensity separately, from a microcontroller.  This would then
let me implement a vector display.

Controlling the actual device may prove a little tricky, so let's start with
the simplest possible thing.  I already have a device which can act like a 
vector CRT ... my old [Tektronix 2225 oscilloscope](https://w140.com/tekwiki/wiki/2225),
which I pulled out of a skip at Monash Uni many years ago.

And I have any number of microcontroller boards.  The
[ESP32](/tag/esp32/) runs
[micropython](/tag/micropython/) has two 8-bit
DACs on board, so let's go with that for the moment.

There's some code up at
[github:nickzoic/mini-vector](https://github.com/nickzoic/mini-vector/)

### points

We can start off by defining an array of points to visit:

```
points = [
        (0.0, 0.0),
        (0.0, 1.0),
        (0.25, 1.0),
        (0.75, 0.5),
        (0.75, 1.0),
        (1.0, 1.0),
        (1.0, 0.0),
        (0.75, 0.0),
        (0.25, 0.5),
        (0.25, 0.0),
]
```

Here's how those points would look plotted:

![a big N](img/big-n.svg)
*a big N*

[`micropython-itertools`](https://pypi.org/project/micropython-itertools/)
implements a lot of the core python `itertools`, including a handy function `cycle`
which repeats an iterable indefinitely, so `cycle(points)` runs through all the points
in an endless loop.

If you don't have `itertools` installed you can always define this function yourself:

```
def cycle(iterable):
    while True:
        yield from iterable
```

### segments

At this point, I wanted to loop over each line segment.
Unfortunately, it doesn't include `pairwise`, so I had to implement that myself:

```
from itertools import cycle

def pairwise(iterable):
    it = iter(iterable)
    a = next(it)
    for b in it:
        yield a, b
        a = b
```

now we can easily step through the line segments like this:

```
for (x1, y1), (x2, y2) in pairwise(cycle(points)):
    print (x1, y1, x2, y2)
```

now we've got each line segment, what are we going to do with it?
Let's try breaking it up into a number of intermediate points,

```
steps = 8

for (x1, y1), (x2, y2) in pairwise(cycle(points)):
    for s in range(0,steps):
        f = s / steps
        x = x1 * (1-f) + x2 * f
        y = x1 * (1-f) + y2 * f
        print(x,y)
```

### intensity

