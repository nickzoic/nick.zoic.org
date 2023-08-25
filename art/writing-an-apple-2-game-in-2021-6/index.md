---
date: '2023-08-24'
layout: draft
tags:
  - apple
  - games
title: 'Writing an Apple 2 game in 2021 (Part 6)'
summary: "Part 6 -- Oh gosh, is that the time?
---

Previously:
* [Part 1](/art/writing-an-apple-2-game-in-2021-1/): About the Apple2 and what to write?
* [Part 2](/art/writing-an-apple-2-game-in-2021-2/): More about 6502 and LoRes.
* [Part 3](/art/writing-an-apple-2-game-in-2021-3/): Controls & Movement
* [Part 4](/art/writing-an-apple-2-game-in-2021-4/): Background, Splash Screen, One Sprite.
* [Part 5](/art/writing-an-apple-2-game-in-2021-4/): More 6502, Multiple Sprites, CC65

# PART 6: 938 Days, Not Much Progress

Well, we're well into our third year of not achieving much on this project.
This is longer than it took to get from the first available Apple II to the
introduction of the Apple II+ with Applesoft BASIC and Disk II controllers.

To be fair, they didn't have the Internet back then, so they didn't have anything
to distract them.  But it's been 269 days since the 
[last update](/art/writing-an-apple-2-game-in-2021-4/) so I'd better get on with it.

## Priorities

Men were real men back then, but also games were real games.
By which I mean, everything was a smidge less sophisticated `:-)`.

Having recently had a look at a couple of examples,
[Spare Change](https://archive.org/details/SpareChange4amCrack)

## Alternatives

Perhaps I should scrap the LORES goose entirely and going with a grid of tiles?
It worked for 
[Beneath Apple Manor](https://en.wikipedia.org/wiki/Beneath_Apple_Manor)
and [Ultima IV](/art/ultima-iv-reflections/) after all!

The [eccentric HIRES memory layout](https://en.wikipedia.org/wiki/Apple_II_graphics#High-Resolution_%28Hi-Res%29_graphics)
doesn't exactly make this easy, of course, but the color interference issues
could be minimized with careful tile layout (eg: making tiles a multiple of 7
pixels wide).  I'd still have green grass, blue water and white geese with orange beaks, but 
we'd lose a lot of the fun, undersaturated colors that made this idea attractive
in the first place.








