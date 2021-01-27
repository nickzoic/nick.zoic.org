---
date: '2021-01-28'
layout: draft
tags:
  - apple
  - games
title: 'Writing an Apple 2 game in 2021 Part 2'
summary: 'Part 2, where I actually do some stuff'
---

*In [Writing an Apple 2 game in 2021 Part 1](/art/writing-an-apple-2-game-in-2021-1)
I give a bit of an introduction to the Apple 2 platform and discuss how I'm hoping
to proceed and what I'm trying to write.*

*In this article, I'm going to talk more about the process of building and running
the software.*

# Assets

Converting [Apple's colour palette to RGB](https://mrob.com/pub/xapple2/colors.html)

Using [GIMP with non-square pixels](http://jubatian.com/articles/using-non-square-pixel-aspect-ratios-in-gimp/)

# 6502 Assembly

I know I've criticized the 6502 before as being a CPU with "approximately 1 register",
but now I'm getting to know it a bit better I'm starting to think of it more
like a CPU with 256 registers, which just happen to be mapped to the start of RAM.

These are the "zero page" locations, and many instructions have a special "zero page"
addressing mode.  As always, memory access is slightly slower than registers, but the
base speed of the 6502 is so low already that it barely matters.

For example, when splitting a byte into nybbles it seems sensible to stash the value
in X 

        LDA $22   ; 3 cycles
        TAX       ; 2 cycles
        AND #$0F  ; 2 cycles
        STA $23   ; 3 cycles
        TXA       ; 2 cycles
        AND #$F0  ; 2 cycles
        STA $24   ; 3 cycles

        LDA $22   ; 3 cycles
        AND #$0F  ; 2 cycles
        STA $23   ; 3 cycles
        LDA $22       ; 2 cycles
        AND #$F0  ; 2 cycles
        STA $24   ; 3 cycles




