---
category: VR
date: '2014-10-06'
layout: article
redirect_from: '/VR/oculus-rift-dk2/'
slug: 'oculus-rift-dk2'
summary: 'The Oculus Rift DK2 ends a 20 year wait for consumer VR ...'
tags:
    - vr
title: Oculus Rift DK2
---

Intro
=====

My [Oculus Rift Development Kit 2](http://www.oculus.com/dk2/) arrived
on Thursday, ending a 20 year wait ...

In 1994-5 I was taking classes in Computer Graphics, and
special-ordering books like [Garage
VR](http://www.amazon.com/Garage-Virtual-Reality-Book-Disk/dp/0672302705)
and [Zen of Code
Optimization](http://www.amazon.com/Zen-Code-Optimization-Ultimate-Software/dp/1883577039)
from the uni bookshop. [VRML](/etc/vrml/) was going to be the next big
thing any day now, and [we couldn't
wait](http://www.imdb.com/title/tt0104692/) for the
[Metaverse](http://en.wikipedia.org/wiki/Snow_Crash).

At some point I gutted an old Toshiba laptop (monochrome
[T3400](http://www.pcmag.com/article2/0,2817,1167527,00.asp), if I
remember correctly ...) and tried to build a HMD out of the LCD panel.
Cutting up a few plastic fresnel lenses, 
a set of plastic safety goggles and a whole lot of cardboard, I could
produce two 320 pixel wide images out of the 640x480 greyscale panel.
Using [scan-line rendering](http://en.wikipedia.org/wiki/Scanline_rendering) meant I
could calculate both images at the same time ... trying to push enough
performance out of the 33MHz 486 CPU to do real time rendering was not
easy. Sadly, extending the display cable of the laptop degraded the
signal and produced an odd plaid-like effect on the screen, the
cardboard and duct tape construction was a bit shaky and the optics
never did work very well. It went in the bin in some house move or
another, and I can't even find a photo of it now.

So, swept along on a great wave of nostalgia, I signed up for the Oculus
Rift developer program ...

First Impressions
=================

These guys really now how to make a [cardboard
box](https://www.google.com.au/search?q=oculus+rift+dk2+unbox). The Rift
is obviously pretty close to actual production since all the niceties
(plastic wraps on cables and little packets of silica) are all there
already, and the inner carton is only a glossy surface away from being
ready for retail.

The HMD itself ... well, we've come a long way since
[cardboard](https://cardboard.withgoogle.com/) and duct tape. It's
mostly just a plastic box surrounding some optics and [the display from
a Galaxy Note
3](https://www.ifixit.com/Teardown/Oculus+Rift+Development+Kit+2+Teardown/27613)
but it is a comfy and adjustable box and fits pretty well with only a
little daylight leaking in.

I tried it first on my Linux laptop with SDK 0.3.2 ... there's only one
simple demo with it, which is a 3D world containing a house. It is very
pretty, but there's not much to it ... so far as I can tell the world is
entirely static. It's enough to show up one shortcoming of the display
technology though: for me at least the image seems very 'gritty', with
individual pixels appearing as spots of light against a dark grid.
[Psychedelic flywire](http://arkleyworks.com/?p=2093), kind of. This may
be fixable in software, though, if the rendering engine can know a
little more about the layout of the hardware pixels.

Head Tracking
=============

The biggest revelation, straight away, is the head tracking. I haven't
got the IR tracker set up yet, but there's an accelerometer in the DK2
and it works straight out of the box. Even with the lag caused by my
slow laptop, the difference is astounding. Without head tracking, it's
just a TV stuck to your head. With it, it is just a little bit magic.
You look up, and see the ceiling, and it really does come as a surprise
to look down and [not be able to see your own
feet](http://intelligentgames.wordpress.com/2010/04/09/dont-look-down-legs-in-fps-games/).

To Be Continued
===============

Unfortunately the 3D performance on this laptop is a bit limited, and
the latest SDK 0.4.1 isn't out for Linux just yet anyway, so watch this
space ...

Resources
=========

-   Official [Oculus Rift DK2](http://www.oculus.com/dk2/) site
-   [Twenty Milliseconds](http://www.twentymilliseconds.com/): VR UX.
-   [Live coding in VR with the Oculus Rift, Firefox WebVR, JavaScript
    and Three.js](https://www.youtube.com/watch?v=db-7J5OaSag).
-   [Minecrift](https://www.wearvr.com/apps/minecrift)
-   [Interfacing to the Wii Balance
    Board](https://www.mattcutts.com/blog/linux-wii-balanceboard/).
