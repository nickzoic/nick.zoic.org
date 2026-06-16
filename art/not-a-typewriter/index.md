---
layout: draft
title: 'ENOTTY: Not a typewriter'
summary: 'What is a computer anyway?'
tags:
  - c
  - linux
date: '2026-06-16'
---

This is kind of a third installment following on from
[Boot Naked Linux](/art/boot-naked-linux/) and
[Forest for the trees](/art/forest-for-the-trees/) so
maybe go read those first if you didn't already.

## What is a computer anyway?

## Terminals and keyboards and the Linux console (oh my)

*A lot of this stuff is supported by the
[ncurses](https://tldp.org/HOWTO/NCURSES-Programming-HOWTO/intro.html)
library so we probably don't need to reinvent that particular
wheel but it makes sense to understand the *ahem* challenges.*

### ASCII 

A lot of you will be familiar with the idea of "computer
text" as [Unicode](https://en.wikipedia.org/wiki/Unicode)[^monster]
strings where Unicode is able to represent hundreds of
thousands of distinct symbols from many of the world's scripts.

[^monster]:

    > Actually, "Unicode" is the name of the consortium.
    > The name of the character set is "Unicode's Monster"...
    
    -- [@FakeUnicode on Twitter](https://x.com/FakeUnicode/status/893305253420027904)

But back at the dawn of computing time, you had 7-bit 
ASCII and you liked it.  It's very much centered on English,
you can't even write café or Zoë or jalapeño
[properly](https://en.wikipedia.org/wiki/English_terms_with_diacritical_marks).
Quotation marks, apostrophes and diacritics have all been
wedged together in a mess of typewriter conventions
and it could do that, because back then computer terminals
were "teletypewriters", things which printed your conversation
with the computer onto paper, so they could type an `e` then back
up and type a `'` over the top of it and it'd look a bit like
an `é`[^overtype]

![typewriter](img/typewriter.png)
*thanks to [overtype: the over-the-top typewriter simulator](https://uniqcode.com/typewriter/)*

[^overtype]: see also [The centralized ASCII tilde](https://en.wikipedia.org/wiki/Tilde#The_centralized_ASCII_tilde) for the history here.

### Keyboards

This is still important to us because when we're dealing
with the console we're dealing with this jurassic[^jurassic]
layer of technology.

[^jurassic]: as in, "ASCII finds a way".

When you press and release keys on the keyboard the kernel
translates the keycodes into the ASCII codes used by old
terminals.  Many keys have obvious ASCII codes, such as 
`a` and `Z` and `~` but there's no ASCII code for `F1` 
or `Home` or `PgUp` etc.  So the console
[mangles these keys](https://en.wikipedia.org/wiki/ANSI_escape_code#Terminal_input_sequences) into "escape sequences", which
arrive at our program exactly as if the user splattered
a bunch of keys all in an instant.

Just some examples:

| key | plain | with shift | with control | with control-shift |
|---|---|---|---|---|
| 1 | 49: `1` | 33: `!` | 49: 1 | 33: ! |
| 2 | 50: `2` | 64: `@` | 0: NUL | 0: NUL |
| 3 | 51: `3` | 35: `#` | 27: ESC | 35: `#` |
| 4 | 52: `4` | 35: `$` | 28: FS | 35: `$` |
| 5 | 53: `5` | 35: `%` | 29: GS | 35: `%` |
| 6 | 54: `6` | 94: `^` | 30: RS | 30: RS |
| 7 | 55: `7` | 38: `&` | 31: US | 38: `&` |
| 8 | 56: `8` | 42: `*` | 127: DEL | 42: `*` |
| 9 | 57: `9` | 40: `(` | 57: `9` | 40: `(` |
| `a` .. `z` | `a` .. `z` | `A` .. `Z` | 1-26: control characters | 1-26: control characters | 
| Backspace | 127: DEL | 127: DEL | 8: BS | 8: BS |
| Delete | ESC `[3~` | ESC `[3;2~` | ESC `[3;5~` | ESC `[3;6~` |
| Enter | 13: CR | 13: CR | 13: CR | 13: CR |
| `[` | 91: `[` | 123: `{` | 27: ESC | 27: ESC |
| `\\` | 92: `\\` | 124: `|` | 28: FS | 28: FS |
| `]` | 93: `]` | 125: `}` | 29: GS | 29: GS |
| `/` | 47: `/` | 63: `?` | 31: US | 127: DEL |
| `-` | 45: `-` | 95: `_` | ???  | 31: US |
| Tab | 9: HT | ESC `[Z` | 9: HT | ESC `[Z` |
| F1 | ESC `OP` | ESC `[1;2P` | ESC `[1;5P` | ESC `[1;6P` |
| F5 | ESC `[15P` | ESC `[15;2P` | ESC `[15;5P` | ESC `[15;6P` |
| `` ` `` | 96: `` ` `` | 126: `~` | 0: NUL | 30: RS |
| Insert | ESC `[2~` | ??? | nothing | nothing |

Just gloriously inconsistent, and I especially like
`/` and `` ` `` which can each be four different
things.

I've been working in the Linux console ever since there was such
a think as a Linux console and I had no idea it was possible
to type *all the ASCII characters* from 0 to 127 on a 
regular keyboard:

| code | key(s) |
|---|---|
| 0 | Control-2, or Control-`` ` `` |
| 1 .. 26 | Control-A through Control-Z |
| 27 | Escape, or Control-3, or Control-[ |
| 28 .. 31 | Control-4 through Control-7 |
| 32 .. 126 | normal printable characters |
| 127 | Backspace, or Control-8, or Control-Shift-/ |

 Sadly, the first character
code which lets us know this is an escape sequences is the
`ESC` character, exactly what is produced by the "Esc" key.
So the only way we can tell if this is the start of a
escape sequence, and not just someone hitting the "Esc" key,
is to see if the code arrive superhumanly fast[^fast].
Which is a terrible hack, but here we are.

[^fast]: At least on my keyboard, mashing "Esc" key and
    `[` together will get you a pair of codes indistiguishable
    from the start of an escape sequence at least half the time,
    so we have to consider *several* characters of input
    and treat them as normal input if they aren't a valid
    escape code.

There's no way at all to tell the difference between
Alt-A and someone mashing Escape and A at the same time.
There's also no way to tell the difference between
Control-J and Enter, or Control-I and Tab, for example.

With all this in mind, why bother with the console at all?
We could access keyboard scan codes directly, but then it'd 
be much harder to support remote access over ssh, etc.
So dealing with all this is probably going to be worth it
in the long run.

### Console

Going back the other way, the console can do more than just
display letters: we can position the cursor, change colours,
there's even a sequence to check the number of rows and
columns.  By default this is limited to
[CP437](https://en.wikipedia.org/wiki/Code_page_437)
(I think)



