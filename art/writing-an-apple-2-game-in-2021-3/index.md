---
date: '2021-02-06'
layout: draft
tags:
  - apple
  - games
title: 'Writing an Apple 2 game in 2021 (Part 3)'
summary: 'Part 3 -- now with multiple sprites'
---

Progress has been very slow as I've picked up a new contract
which does tend to cut into my 6502 assembly writing time.  

Previously, in [Writing an Apple 2 game in 2021 Part 1](/art/writing-an-apple-2-game-in-2021-1/)
I gave a bit of an introduction to the Apple 2 platform and discussed how I'm hoping
to proceed and what I'm trying to write.
In [Writing an Apple 2 game in 2021 Part 2](/art/writing-an-apple-2-game-in-2021-2/)
I talked a bit about the 6502 and how to draw stuff
on the Lo-Res screen.
In this article, I'm going to get background scrolling and multiple sprites
working.

# Keyboard Controls & Movement

[Previously](/art/writing-an-apple-2-game-in-2021-2/#reading-the-keyboard) I
mentioned that there's no way to detect a key being held down, and there's no 
key autorepeat.  So we'll have to remember which way the goose is going, and
keep going until it hits something or the user presses a stop key.

On top of that, there's just no way to draw the goose heading straight up the 
screen. Not in these few pixels anyway. Left and up a bit, right and up a bit, no
problem, but not straight up.

So I'm going to abandon the traditional WASD keyboard layout for WEASDZX layout.

![WEASDZX Layout](img/weasdzx2.jpg) ![WEASDZX Layout](img/weasdzx3.jpg) 

`S` in the center is for stop.  
There have to be a couple of other keys on the right as well, for grabbing and
carrying things. probably `L` and `P`.

If I can work out how the mouse -> paddle 
support works in the emulator I might try and support joystick mode too.

# Movement

Normally a diagonal move is a tricky 1.4 times as long as a orthogonal one, but
in this case our chonky 3:2 pixels and our two pixel high rows combine to give us a 
diagonal move 5/6ths as long as a double horizontal one. Close enough.

![WEASDZX Semi-Diagonals](img/weasdzx1.jpg) 

# Demonstration!

Thanks to the magic of `iframe` and the incredible work of
[Apple2js](https://github.com/ScullinSteel/apple2js)
I can embed code demos right here in the blog!  This might not work perfectly 
in all browsers, but try mousing over the window and pressing `A`, `S` and `D` to
move the goose ...

<iframe src="apple2js-mini.html#goose1" width="612px" height="460px" frameborder="0" onmouseover="this.focus()" onmouseout="this.blur()"></iframe>

In the previous article I included a small .gif movie of the goose animation which
clocks in at about 1MB.  Incredibly, the entire Apple 2 emulator plus the disk image
for the lores goose game comes out smaller than this!

There have to be a couple of other keys on the right as well, for grabbing and
carrying things. probably `L` and `P`.

# Multiple Sprites

# COMING SOON: PART 4 

For updates either [follow the RSS](https://nick.zoic.org/feed.rss) or [follow me on Twitter](https://twitter.com/nickzoic/)
