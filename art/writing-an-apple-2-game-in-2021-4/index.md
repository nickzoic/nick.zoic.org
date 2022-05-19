---
date: '2022-05-19'
layout: draft
tags:
  - apple
  - games
title: 'Writing an Apple 2 game in 2021 (Part 4)'
summary: "Part 4 -- Oh no, it's 2022"
---

It's 2022, just over a year since the last update of this series,
and, well, life has continued to get in the way of my plans `:-)`

*If you're reading this because you guessed the URL, hurrah!  Clever you!  It isn't done yet!  Come back later!*

# Goose Containment

One thing which is really obvious from the [part 3](/art/writing-an-apple-2-game-in-2021-3/)
simulation is that there's no boundary to the screen.  Our goose wanders where it will, with
no respect for memory layout.

## Perimeter

So we need to add some kind of barrier, at least around the edge of the map.
This can be done easily enough by just checking the goose's position on the map and stopping
movement if it has reached the edge.  As a bonus, we could change the scroll behaviour so that
as the goose reaches the 'edge of the world', it moves from the center of the screen.
This would provide a very clear signal that there's no more map over there.

## Internal Walls

The goose game maps also have lots of barriers in the scenery —
fences, walls, shrubs — and finding your way through these is an important part of the game.
The movement routines need to be told about these somehow.  One possibility here is to encode
the "impassibilty" of a part of the map into the pixel values of the map. A byte value of 
`$Ax` or `$xA` (Colour `$A` is that "Grey #2" we're using for sprite transparency)
might be used to indicate that a location is impassible, for example, so scattering a handful
of grey pixels into the scenery would be
sufficient to enforce these barriers.  Grey parts which are *not* impassible, like gravel
paths, could just use the identical "Grey #1", encoded as `$5`.

Alternatively, we could encode barriers as a separate bitmask, or as simple exclusion rules stored
alongside the map, for example for each row keep a list of columns which are forbidden. We can 
make the map just slightly narrower to give us space for this stuff at the end of every row.

## Sprite Collisions

And lastly, there's *moving barriers*, gates and the like.  We have to handle sprite collisions
for things like people too, because they block and/or shoo the goose, so we can probably just treat
[inanimate objects like NPCs](https://www.ign.com/articles/2015/07/22/fallout-3-broken-steel-train-is-actually-just-a-giant-npc-hat)
who happen to have very boring behaviours.

We'll leave that to next time.

## On-water Matters

Our goose, and various other sprites, are also rendered differently when in the water … the 
lower couple of rows go missing.  This could be done by map pixel color keying on two blue
pixels, encoded as `$66`, or by encoding wet areas similar to the exclusion rules mentioned above:
for each row, a range of pixels can be declared "under water" and this is then easy to check against.

# Behaviours

The stuff about sprites brings up an interesting point: while there's a bunch of 'vegetables' in the game,
objects which don't really do anything but you can carry them around, there's also a bunch of objects which
have actions. Gates open and close, humans give chase, sprinklers, umm, sprinkle, that kind of thing.

I think the way I want to do this is to have the "action" in the loop just update the status of the object.
Then the code in the "logic" part of the program can detect the actions from the states and update their state,
sprite and position accordingly.


# Making the code public

An article on [hacker news](https://news.ycombinator.com/item?id=31410617)
brought a bit of attention & a request to release the source so, sure, okay
I guess.  



