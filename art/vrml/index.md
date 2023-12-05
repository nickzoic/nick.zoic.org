---
date: '2009-08-18'
layout: article
tags:
  - networks
  - languages
title: 'VRML: Very Odd.'
---

So the [VRML](https://en.wikipedia.org/wiki/VRML) rendering thing isn’t
panning out so well. “Making the simple things simple by making the
difficult things impossible”.

We’re talking, here, about a language which has a clock, but no way to
display the time. You can display strings on billboards, and the
billboards even point at the camera most of the time. But you can’t cast
the float time to a displayable string, without calling out to
Javascript anyway, and I never could get that to work the same way
twice. So I made a little analogue clock where a sphere slides along a
cylinder And that sort of works. Sort of. Of course, it doesn’t stay
quite still either which makes it rather difficult to read.

You can interpolate the position of Things. But you can’t interpolate
points in IndexedLineSets, so my poor nodes are floating there in space
without the links showing. Maybe if I interpolated the center and the
lengths of a cylinder for each link, perhaps? But really, surely, that’s
too much work to go to for something that’s meant to be a visualization
tool, not and end to itself.

Also, like it’s little friend HTML, it never renders the same way on two
different platforms. And never tells you why. Argh.

Anyway, that’s my rant. There must be some way to do this. I’m sure it’d
be a very simple Java applet. There’s lots of them out there. Surely
someone else has DONE this.

(Actually, this would all be within the abilities of HTML5 Canvas, I
suspect!)
