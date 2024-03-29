---
date: '2023-08-20'
layout: article
summary: |
    PyConAU 2023 Adelaide!
tags:
- conference
- python
title: 'PyConAU 2023 Adelaide!'
---

I was at [PyConAU 2023 Adelaide](https://2023.pycon.org.au/)
... my first in-person conference since
[PyConAU and Compose Melbourne in 2018](https://nick.zoic.org/art/pycon-2018-sydney/)
so I was very excited ...
I presented on my current work, CountESS, and also for the inaugural PyConAU Fair I
presented a silly toy I created out of a thrift shop guitar hero controller ...

## CountESS

* [Slides from "CountESS: Count-based Experimental Scoring and Statistics"](/talk/pycon2023/countess/)
* [Video at YouTube](http://youtu.be/JzU6cbvZ0a0)
* [countess github repo](https://github.com/CountESS-Project/CountESS/)

**ERRATA: I somehow got [Frederick Sanger](https://en.wikipedia.org/wiki/Frederick_Sanger)'s
name wrong in the slides and just read it out without noticing. Ooops. Hopefully I'll be able to 
put a correction in the video.  Sorry, Fred.**

## MIDI Hero

... at the inaugural PyConAU Fair!

* [PyConAU Fair on Youtube](https://www.youtube.com/watch?v=Q16T5wsKdCM)
* [MIDI Hero blogpost 1](/art/midi-hero/)
* [MIDI Hero blogpost 2](/art/midi-hero-2/)

There's some video from the fair itself including me making boop boop noises
but not very muscially.  On of these days I'll fix the terrible latency on
this device and it'll be actually fun to play.

## Other Videos

The videos are now appearing on [the PyConAU YouTube channel](https://www.youtube.com/@PyConAU)
(here's the [2023 playlist](https://www.youtube.com/playlist?list=PLs4CJRBY5F1KwxIxbTmhN9jX4hBtE-OKJ))
and so far ones that I've found interesting:

### Bio sciences

* [Alan Rubin: Building a biological database with Python](https://youtu.be/uy7FEXW9onE)

  This is all about MaveDB, which is somewhat related to CountESS in that it deals with
  Multiplex Assays of Variant Effect, which is the kind of data which CountESS can process.

* [David Lawrence: Analysing and sharing genetic data with Python](https://youtu.be/vmQ1_Pzh4Us)

  More dataflows!  This time on the clinical analysis side.

  Building a graphical query into a Django `Q` query which
  then turns into an efficient SQL query on the backend.
  This is [the kind of thing I've dabbled with a little](/art/tranquil-apis/)
  and it's a really interesting aim.

### Other science stuff

* [Alex Ware: An Introduction to PySpark](https://youtu.be/ZFLOMSuWHxg)

  How is PySpark useful and how is it like and unlike Pandas?

  Should CountESS be running over Spark?  Quite possibly.

* [Andrew Williams: Using Python and 19,200 bits/second serial links to manage antennae for the Square Kilometre Array](https://youtu.be/tYP6nypJWtY)

  The number 19,200 will apparently haunt me forever.
  It's interesting to see the lengths that this
  team have had to go to to avoid radio interference.

### Other

* [Russell Keith-Magee: How to build a cross-platform graphical user interface with Python](https://youtu.be/vmQ1_Pzh4Us)

  All about Toga, which is a nice GUI toolkit alternative to ... well, all the other ones.

  CountESS's GUI should probably be rewritten in Toga if only because it solves a
  couple of immediate irritations and hopefully looks a bit nicer on Mac / Windows
  than just the Tkthemes.

* [Amanda J Hogan: Zero or Hero? Assessing Pygame Zero in the classroom](https://youtu.be/g5Tw1sYzXg0)

  Amanda brings some perspective on what it's like to teach beginner programmers,
  which I think is really interesting as we're all begineers from time to time.

  Also check out the [Education Showcase](https://www.youtu.be/Z60fVOQJzpc) for the
  other side of the same story.

### WASM, etc

Yeah, I'm [still interested in WASM](/art/web-assembly-on-esp32-with-wasm-wamr/) for many reasons,
not the least of which is that I'm sick of hearing about containers.  Katie's & Jim's talks are
somewhat connected so watch Katie's first ...

* [Katie Bell: What can't WebAssembly do?](https://youtu.be/JbZAsSzzk0E)

* [Jim Mussared: WASM in your wheel](https://youtu.be/yVA4TUtTDks)

... the tragic thing is, at some point I might have to admit that maybe Java
got it right in the first place with JAR files containing their own dependencies, etc.
