---
date: '2022-06-01'
layout: draft
tags:
  - apple
  - games
title: 'Writing an Apple 2 game in 2021 (Part 5)'
summary: "Part 5 -- Coming Soon"
---

# More thinking about 6502

See also this [really good guide to the 6502 instruction set](https://www.masswerk.at/6502/6502_instruction_set.html)

## Instructions which can mutate memory

The accumulator is a bit of a bottleneck, with zero page memory kind of taking
the place of registers, so it's worth considering which instructions
can mutate memory directly:

* INC / DEC
* ROL / ROR / ASL 

That's not a lot of options ... the other logical operations store
their result in the accumulator instead of in memory:

* ADC / SBC
* AND / ORA / EOR
* ROL A / ROR A / ASL A

So for those you're stuck doing something like LDA; EOR imm; STA.

## Missing Immediate Mode

One of the most frustrating "missing instructions" is `BIT imm` ... there's
`CMP imm` and `AND imm` but no `BIT imm`, only `BIT zeropage` and `BIT absolute`.

So if you want to non-destructively check for an arbitary bit being set in the accumulator, you can't
just do `BIT #$40` ... instead you have to either store that $40 in a zero page 
location or you could do `AND #$40` but restore A from somewhere.

## Indirect addressing

ADC, AND, CMP, EOR, LDA, ORA, SBC and STA all support "zeropage,X" and "indirect"
addressing for their source, or in the case of STA their destination.

`Zeropage,X` addressing takes a zeropage address as an operand, adds X and then uses
that zeropage address as the address to work on.

`(Indirect, X)` addressing does the same thing and then loads the 16-bit address at 
that address and that address + 1 and uses *THAT* as the address to work on.

... and `(Indirect), Y` works *completely differently*.  Note the different punctuation.
It takes a zero page address, then looks up the 16-bit address at that address and that address + 1, and then adds Y to *that*.

```
STA $1234   ; A -> M[ $1234 ]
STA $56, X  ; A -> M[ $56 + X ]
STA ($78,X) ; A -> M[ MM[$78+X] ] 
STA ($9A),Y ; A -> M[ MM[$9A] + Y ] 
```

Because registers are only eight bit, if you
want to operate anywhere in memory you have to use a zero page pair as a pointer
to the start and then Y as an offset within that.
Y is only 8 bits though, so you also need to change the high byte of the pointer,
something like:

```
memcpy16
!zone {
  LDY #$00
  LDX zp_length+1
.loop.x
  BNE .loop.y
  LDY zp_length
  BEQ .done.y
.loop.y
  DEY
  LDA (zp_src_addr), Y
  STA (zp_dst_addr), Y
  CPY #0
  BNE .loop.y
.done.y
  CPX #0
  BEQ .done.x
  INC zp_src_addr+1
  INC zp_dst_addr+1
  DEX
  JMP .loop.x
.done.x
  RTS
}
```

But what good is the very weird `(indirect,X)` mode?  
[Assembly Cookbook for the Apple II/IIe](https://mirrors.apple2.org.za/ftp.apple.asimov.net/documentation/programming/6502assembly/Assembly_Cookbook_for_the_Apple_II_IIe.pdf)
(p79) describes it as "an oddball" and not much use other than with X = 0,
and a quick look at the
[Apple II DOS Source Code](https://computerhistory.org/blog/apple-ii-dos-source-code/)
suggests the same ... it is used, but only with X = 0.

# MULTIPLE SPRITES

Okay, time to actually make some progress on this game.
At the moment, there's exactly one sprite, the goose.
Let's have a list of sprites instead.

* Number of Sprites
* For each Sprite
  * Bottom-most Row (map coord, 0..255)
  * Left-most Row (map coord, 0..255)
  * Height (rows, 0..16 or so)
  * Width (pixels, 0..16 or so)
  * Image (16 bit memory address)

Handling all the sprites as separate image files seems painful, so I might use a "sprite sheet"
approach instead. The sprite sheet is always a fixed width, so starting from an image address you
always add a constant to get to the next row.  This potentially wastes a bit of space but makes the
maths easier (and sprite drawing is very much an inner loop, so the faster we make it the better)

## Occlusion

We want to write these from back to front so they occlude in the correct way.
We could do this by keeping the sprite list ordered, but for now let's just run through it once per row.

# OH COME ON NOW LET'S BE SERIOUS

For updates either [follow the RSS](https://nick.zoic.org/feed.rss) or [follow me on Twitter](https://twitter.com/nickzoic/)

