---
date: '2021-01-28'
layout: draft
tags:
  - apple
  - games
title: 'Writing an Apple 2 game in 2021 Part 2'
summary: 'Part 2, where I actually do some stuff'
---

PREVIOUSLY: In [Writing an Apple 2 game in 2021 Part 1](/art/writing-an-apple-2-game-in-2021-1)
I give a bit of an introduction to the Apple 2 platform and discuss how I'm hoping
to proceed and what I'm trying to write.

In this article, I'm going to talk more about the process of building and running
the software.

# The Mighty 6502

The [6502](https://en.wikipedia.org/wiki/MOS_Technology_6502)
was first launched in 1975: 
*Here's a [6502 Instruction Set](https://www.masswerk.at/6502/6502_instruction_set.html)
page*

## Zero Page

I know I've criticized the 6502 before as being a CPU with "approximately 1 register",
but now I'm getting to know it a bit better I'm starting to think of it more
like a CPU with 259 registers, 256 of which just happen to be mapped to the start of RAM.

These are the "zero page" locations, and many instructions have a special "zero page"
addressing mode.  As always, memory access is slightly slower than registers, but the
base speed of the 6502 is so low already that it barely matters.

For example, when splitting a byte into nybbles it seems sensible to stash the value
in X.  But, assuming the value is stored in a zero page address, it's actually faster
to reload in from the zero page (3 cycles) than to TAX then TXA (2 cycles each).

## Registers

In addition to the 256 zero-page locations there's three main registers of 8 bits each:
A, X and Y.

A is the main "accumulator" which is where most of the ALU operations happen.
X and Y are "index registers" which have fewer operations on them, but are used by
the addressing modes.  Compared to even a [Z80](https://en.wikipedia.org/wiki/Zilog_Z80)
it's pretty minimal!

There's also an 8 bit stack pointer, 7 bits of processor flags and a 16-bit program
counter.

## Addressing Modes

Accumulator-centric instructions like `ADC` (add with carry), `CMP` (compare),
`EOR` (exclusive or), `LDA` (load), `ORA` (or), `SBC` (subtract with borrow)
and `STA` (store) all support a large number of addressing modes:

In the following table, `n` represents an 8 bit quantity following the instruction,
and `nn` represents a 16-bit little-endian quantity following the instruction.

* `M[nn]` represents an 8-bit quantity in memory location `nn`.
* `Z[n]` represents an 8-bit quantity in zero page location `n`.
* `ZZ[n]` represents a 16-bit quantity in zero page location `n` and `n+1` (little-endian)

Remember zero page locations wrap around.

addressing mode | meaning | typical cycles
--- | --- | ---
immediate | `n` | 2
zeropage | `Z[n]` | 3
zeropage,X | `Z[n+X]` | 4
absolute | `M[nn]` | 4
absolute,X | `M[nn+X]` | 4\*
absolute,Y | `M[nn+Y]` | 4\*
(indirect,X) | `M[ZZ[n+X]]` | 6
(indirect),Y | `M[ZZ[n]+Y]` | 5\*

Note the asymmetry of those last two modes.  The first uses `n+X` to choose a zero page
location, then goes and gets the memory pointed to by the 16-bit value at that location.
The second uses `n` to choose a zero page location, then adds Y to the 16-bit value at
that location to get a new address, which it goes and gets.

The second form is probably what you're after in most cases.

## Beg, Steal or Borrow ...

One thing which caught me out and I figure I should mention here.  To add 1000
to a 16-bit quantity in zero-page location `foo`, you do something like:

```
CLC        ; clear the carry flag  
LDA foo    ; load the low byte
ADC $#E8   ; add 232 (1000 = 768 + 232)
STA foo    ; store the low byte
           ; carry flag is now set if we need to carry
LDA foo+1  ; load the high byte
ADC $#03   ; add 3 to the high byte, plus carry if needed)
STA foo+1  ; store the high byte
```

whereas to *subtract* the carry flag has the opposite sense: `0` means a borrow
and `1` means no borrow.  So to subtract 1000, you'd do:

```
SEC        ; set the carry flag (clear the borrow flag)
LDA foo    ; load the low byte
SBC $#E8   ; sub 232 (1000 = 768 + 232)
STA foo    ; store the low byte
           ; carry flag is now *clear* if we need to borrow.
LDA foo+1  ; load the high byte
SUB $#03   ; sub 3 from the high byte, and borrow if needed)
STA foo+1  ; store the high byte
```

This was ... [surprising to me](https://en.wikipedia.org/wiki/Carry_flag#Vs._borrow_flag).

# Graphics

So, I think I've decided to make a Lo-Res game.

The Lo-Res screen is, as mentioned last time, 40x48 squishy rectangular pixels,
in 16 colours, two of which are identical (grey and gray?)

## Main Loop

There's two screens: one at $0400 and one at $0800 and we can flip between them
so that our updates don't make a flickery mess.  So our general game loop looks 
like 

```
forever:
    draw onto screen 1
    switch to screen 1
    update game state
    draw onto screen 2
    switch to screen 2
    update game state
```

OK so all our graphics routines are going to need to be able to switch between 
screen base addresses.  We can do this by storing the screen base page at 
one of those spare zero page locations, and all the graphics routines will
use that to start of their target address calculations.  So now we've got our
"main loop", which runs forever, and in 6502 looks something like:

```
zp_screen_page = $F0      ; zero page location we're using for screen base

io_gr_graphics = $C050    ; apple I/O: set graphics mode
io_gr_full = $C052        ; ... set graphics full page
io_gr_pri = $C054         ; select screen 1
io_gr_sec = $C055         ; select screen 2
io_gr_lores = $C056       ; select lores mode

entry
    lda io_gr_graphics    ; switch to graphics, lores, full screen
    lda io_gr_lores
    lda io_gr_full

main_loop
    lda #$08              ; draw onto screen 2
    sta zp_screen_page
    jsr draw_everything
    
    lda io_gr_sec         ; switch to screen 2
   
    lda #$04              ; draw onto screen 1 
    sta zp_screen_page
    jsr draw_everything

    lda io_gr_pri         ; switch to screen 1

    jmp main_loop         ; go around again
```

Okay! So now *all* we have to do is implement `draw_everything`.

![Draw the rest of the damn owl](img/damn_owl.png)

## Sprites

The basic building block of this kind of graphics is the
[Sprite](https://en.wikipedia.org/wiki/Sprite_%28computer_graphics%29),
a kind of moveable template for drawing pixels.
Each of the moveable parts of our graphics will be its own sprite.

Pretty clearly we need some way of drawing sprites.
Some computers of this era had sprite coprocessors to help out with this
but the Apple 2 didn't, so we're on our own.

Each sprite will be an array of pixel values, and we unless all our sprites are to be
monotonously rectangular, we'll need some way to handle transparency. Conveniently,
when we converting [Apple's colour palette to RGB](https://mrob.com/pub/xapple2/colors.html)
we can see that two colours, $5 and $A, render identically as a boring mid-grey.

We don't really need two identical colours in our palette so let's use one of them
to mark transparency.  As we draw each pixel we'll check if it has the value $A and
if so, we'll not draw it.

This is slightly complicated by the fact that LoRes packs two pixels into each byte,
but if we XOR the byte value with $AA then we just need to look for a clear upper or
lower nybble which is a bit easier.  We end up doing something like:

```
LDA sprite,X      ; load a byte of pixel
EOR $#AA          ; flip the A's to 0's
BEQ dont_draw_any ; it's all transparent, skip
BIT $#F0          ; check the top 4 bits
BEQ only_draw_bot ; only draw the bottom bits
BIT $#0F          ; check the bottom 4 bits
BEQ only_draw_top ; only draw the top bits
                  ; write the whole thing
```

... except that BIT, weirdly and rather annoyingly, has no immediate address mode.
But that's the general idea.  If the byte is $AA skip both halves, otherwise check
each nybble and only write one half, otherwise write the whole thing.

Sprites get drawn on top of a background, which is really just an enormous sprite too.
The main difference is that the background is much wider than the screen and doesn't
need to support transparency.

Okay, so putting our sprite drawing routine together:

![Goose Movie](img/goose2.gif)

### Drawing Sprites

Using [GIMP with non-square pixels](http://jubatian.com/articles/using-non-square-pixel-aspect-ratios-in-gimp/)




