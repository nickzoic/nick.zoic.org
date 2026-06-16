---
layout: draft
title: 'ENOTTY: Not a typewriter'
summary: 'What is a computer anyway?'
tags:
  - c
  - linux
---

This is kind of a third installment following on from
[Boot Naked Linux](/art/boot-naked-linux/) and
[Forest for the trees](/art/forest-for-the-trees/) so
maybe go read those first if you didn't already.

## What is a computer anyway?

## Terminals and keyboards and the Linux console (oh my)

### ASCII 

A lot of you will be familiar with the idea of "computer
text" as [Unicode](https://en.wikipedia.org/wiki/Unicode)[^monster]
strings where Unicode is able to represent hundreds of
thousands of distinct symbols from many of the world's scripts.

[^monster]:
  > Actually, "Unicode" is the name of the consortium.
  > The name of the character set is "Unicode's Monster"...
  > -- [@FakeUnicode on Twitter](https://x.com/FakeUnicode/status/893305253420027904)

But back at the dawn of computing time, you had 7-bit 
ASCII and you liked it.  It's very much centered on English,
you can't even write café or Zoë or jalapeño
[properly](https://en.wikipedia.org/wiki/English_terms_with_diacritical_marks).
Quotation marks, apostrophes and diacritics have all been
wedged together in a mess of typewriter conventions[^overtype]
and it could do that, because back then computer terminals
were "teletypewriters", things which printed your conversation
with the computer onto paper, so they could type an `e` then back
up and type a `'` over the top of it and it'd look a bit like
an `é`[^typewriter]

![typewriter](img/typewriter.png)

[^overtype]: see also
  [The centralized ASCII tilde](https://en.wikipedia.org/wiki/Tilde#The_centralized_ASCII_tilde)
  for the history here.

[^typewriter]: thanks to [overtype: the over-the-top typewriter simulator](https://uniqcode.com/typewriter/)

### Keyboards

This is still important to us because when we're dealing
with the console we're dealing with this jurassic[^jurassic]
layer of technology.

[^jurassic]: as in, "ASCII finds a way".

When you press and release keys on the keyboard the kernel
translates the keycodes into the ASCII codes used by old
terminals.  Many keys have obvious ASCII codes, such as 
`a` and `A` and `~` but there's no ASCII code for `F1` 
or `Home` or `PgUp` etc.  So the console
[mangles these keys](https://en.wikipedia.org/wiki/ANSI_escape_code#Terminal_input_sequences) into "escape sequences", which
arrive at our program exactly as if the user splattered
a bunch of keys all in an instant. Sadly, the first "special"
code which lets us know this is an escape sequences is the
`ESC` code, exactly what is produced by the "Esc" key.
So the only way we can tell if this is a special sequence is
to see if the code arrive superhumanly fast, which is a terrible
hack, but here we are.  At least on my keyboard, mashing
"Esc" key and `[` will get you a pair of codes indistiguishable
from the start of an escape sequence.

With that in mind, why bother with the console at all?
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

