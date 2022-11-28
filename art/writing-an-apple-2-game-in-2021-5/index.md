---
date: '2022-11-28'
layout: article
tags:
  - apple
  - games
title: 'Writing an Apple 2 game in 2021 (Part 5)'
summary: "Part 5 -- Getting Sidetracked, Of Course"
---

Previously:
* [Part 1](/art/writing-an-apple-2-game-in-2021-1/): About the Apple2 and what to write?
* [Part 2](/art/writing-an-apple-2-game-in-2021-2/): More about 6502 and LoRes.
* [Part 3](/art/writing-an-apple-2-game-in-2021-3/): Controls & Movement
* [Part 4](/art/writing-an-apple-2-game-in-2021-4/): Background, Splash Screen, One Sprite.

# More thinking about 6502

Getting to grips with the 6502 CPU is hard, because it's so alien to a modern programmer.
There's just so little there.  All sorts of trade-offs you'd normally make about branch 
prediction and cache coherency simply don't matter because there isn't any branch prediction
and there isn't any cache.

There also isn't any multiplication or division, which makes all kinds of things tricky.

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

(This is fixed in the [65C02](http://www.6502.org/tutorials/65c02opcodes.html) as used in the [Enhanced Apple IIe](https://en.wikipedia.org/wiki/Apple_IIe#Enhanced_IIe) and [Apple IIc](https://en.wikipedia.org/wiki/Apple_IIc),
by the way, along with a bunch more instructions and addressing modes)

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

OK so I've gotten very bogged down at this point with too much other work and too much other stuff going on,
but I'll just mention a couple of little side-tracks before I hit publish and come back to it later

## cc65

[cc65](https://cc65.github.io/) is a freeware
[C](https://www.ioccc.org/) compiler for the 6502 and friends.

By default it tries to build an
[AppleSingle](https://en.wikipedia.org/wiki/AppleSingle_and_AppleDouble_formats)
binary, but I don't have the right tools for that so we turn it off with `-D __EXEHDR__=0`

I use [a2tools](https://github.com/catseye/a2tools) to write the compiled code
to disk as a binary file called `PROGRAM` which loads at the correct address.


[Makefile](files/Makefile):
```
MAKEFLAGS += r
TARGET = apple2
TARGET_LIB = ${TARGET}.lib
START_ADDR = 2000  # hex
LIBRARIES = library.o

%.s: %.c
        cc65 -Oi -o $@ -t ${TARGET} $<

%.o: %.s
        ca65 -o $@ $<

%.bin: %.o ${LIBRARIES}
        ld65 -o $@ -t ${TARGET} -D __EXEHDR__=0 -S 0x${START_ADDR} $^ ${TARGET_LIB}

%.dsk: %.bin
        cp dos33_loader.dsk $@
        a2in B.${START_ADDR} $@ PROGRAM $<

run_%: %.dsk
        mame apple2p -volume -24 -uimodekey DEL -flop1 $<
```

The [dos33\_loader.dsk](files/dos33_loader.zip) is a bootable DOS 3.3 disk which automatically runs 
a a tiny Applesoft program called `HELLO` which loads the binary file `PROGRAM`.
Printing a `CHR$(4)` followed by a DOS command runs that command, I don't know why.

```
10 PRINT CHR$(13) CHR$(4) "BRUN PROGRAM"
```

The compiled code isn't spectacularly efficient, because it does stuff like:

```
        lda     _io_gr_graphics+1
        sta     ptr1+1
        lda     _io_gr_graphics
        sta     ptr1
        lda     #$00
        tay
        sta     (ptr1),y
```

... rather than the somewhat simpler `sta io_gr_graphics`
(it hasn't noticed it is a `char * const`, so it could just use that address in "absolute" mode)
but it's pretty easy to reverse engineer the calling
convention and write a `library.h` and `library.s` with the weirder and more performance-critical parts in assembly.

I'd rather dispense with DOS and use our tiny loader from before, with a boot sector loader to display
the splash screen immediately and then load the compiled C code at `$0C00`, etc, but this is a good start.

## Higher Level Languages

Of course, shifting to C isn't necessarily going far enough, so the temptation is still there to try to compile a
[minimal Forth](https://gist.github.com/lbruder/10007431) or
[minimal LISP](https://carld.github.io/2017/06/20/lisp-in-less-than-200-lines-of-c.html) or similar.

I also have a bit of an [ongoing obsession](https://github.com/nickzoic/tropyc)
with the concept of a self-hosting Python
compiler which would use the built-in Python
[disassembler](https://docs.python.org/3/library/dis.html)
library to retrieve bytecodes for a 
function and then compile those to target code.  Perhaps this could be used to compile a limited subset of 
Python code to 6502, without the stress of having to write an actual parser or compiler.

# THAT'S ALL FOR NOW

For updates either [follow the RSS](https://nick.zoic.org/feed.rss) or [follow me on Twitter](https://twitter.com/nickzoic/)
