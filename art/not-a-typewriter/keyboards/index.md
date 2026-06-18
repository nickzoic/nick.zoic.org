---
layout: extra
title: 'Not a Typewriter: Keyboard Layouts'
---

I'm trying to work out which of these key combos can be relied 
on to be available from the console and from xterms.

So far, in addition to the printables, it's looking like F1 through
F10 and Shift-F1 through Shift-F10, plus Tab, Escape and Enter.
Control-(digit or letter) and Alt-(digit or letter) are okay too.

Dubious: Control-F\*, F11 and F12, Alt-Symbol.

## Acer Travelmate B117 laptop, Linux console

control-shift never does naything except in the rare
case where shift-whatever == control-whatever when it does
that.  And control-shift-`-` makes a 31: US.

| key | plain | shift | control | control-shift |
|---|---|---|---|---|
| Esc | Esc | Esc | Nothing |
| F1 | Esc [ [ A | Esc [ 2 3 ~ | Esc [ [ A |
| F2 | Esc [ [ B | Esc [ 2 4 ~ | Esc [ [ B |
| F3 | Esc [ [ C | Esc [ 2 5 ~ | Esc [ [ C |
| F4 | Esc [ [ D | Esc [ 2 6 ~ | Esc [ [ D |
| F5 | Esc [ [ E | Esc [ 2 8 ~ | Esc [ [ E |
| F6 | Esc [ 1 7 ~ | Esc [ 2 9 ~ | Esc [ 1 7 ~ |
| F7 | Esc [ 1 8 ~ | Esc [ 3 1 ~ | Esc [ 1 8 ~ |
| F8 | Esc [ 1 9 ~ | Esc [ 3 2 ~ | Esc [ 1 9 ~ |
| F9 | Esc [ 2 0 ~ | Esc [ 3 3 ~ | Esc [ 2 0 ~ |
| F10 | Esc [ 2 1 ~ | Esc [ 3 4 ~ | Esc [ 2 1 ~ |
| F11 | Esc [ 2 3 ~ | Esc [ 2 3 ~ | Esc [ 2 3 ~ |
| F12 | Esc [ 2 4 ~ | Esc [ 2 4 ~ | Esc [ 2 4 ~ |
| PrtSc | 20: DC4 | Nothing | 20: DC4 |
| Pause/Break | Esc [ P |
| Del | Esc [ 3 ~ | Esc [ 3 ~ | Esc [ 3 ~ |
| Ins | Esc [ 2 ~ | Esc [ 2 ~ | Esc [ 2 ~ |
| `` ` `` | `` ` `` | `~` | 0: NUL |
| 1 | 1 | ! | nothing |
| 2 | 2 | @ | 0: NUL |
| 3 | 3 | # | 27: ESC |
| 4 | 4 | $ | 28: FS |
| 5 | 5 | % | 29: GS |
| 6 | 6 | ^ | 30: RS |
| 7 | 7 | & | 31: US |
| 8 | 8 | * | 127: DEL |
| 9 | 9 | ( | nothing |
| 0 | 0 | ) | nothing |
| - | - | _ | 31: US | 31: US |
| = | = | + | nothing |
| Backspace | 127: DEL | 127: DEL | 8: BS |
| Tab | 9: TAB | 9: TAB | nothing |
| [ | [ | { | 27: ESC |
| ] | ] | } | 29: GS |
| \\ | \\ | \| | 28: FS |
| ; | ; | : | nothing |
| ' | ' | " | 7: BEL |
| Enter | 13: LF | 13: LF | 13: LF |
| , | , | < | nothing |
| . | . | > | nothing |
| / | / | ? | 127: DEL |
| PgUp | Esc [ 5 ~ | nothing | Esc [ 5 ~ | Esc [ 5 ~ |
| Up | Esc [ A | Esc [ A | Esc [ A | Esc [ A |
| PgDn | Esc [ 6 ~ | nothing | Esc [ 6 ~ | Esc [ 6 ~ |
| Left | Esc [ D | Esc [ D | Esc [ D | Esc [ D |
| Down | Esc [ B | Esc [ B | Esc [ B | Esc [ B |
| Right | Esc [ C | Esc [ C | Esc [ C | Esc [ C |

There's also some shenanigans when the Fn key is held down:

| Fn- + | Equivalent | Code |
|---|---|---|
| Fn-PgUp | Home | Esc [ 1 ~ |
| Fn-PgDn | End | Esc [ 4 ~ |

Plus a kind of numpad overlay.

## `kvm -nographic` in an `xterm-256color`

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
| `` ` `` | 96: `` ` `` | 126: `~` | 0: NUL | 30: RS |
| `-` | 45: `-` | 95: `_` | ???  | 31: US |
| `/` | 47: `/` | 63: `?` | 31: US | 127: DEL |
| Tab | 9: HT | ESC `[Z` | 9: HT | ESC `[Z` |
| F1 | ESC `OP` | ESC `[1;2P` | ESC `[1;5P` | ESC `[1;6P` |
| F2 | ESC `OQ` | ESC `[1;2Q` | ESC `[1;5Q` | ESC `[1;6Q` |
| F3 | ESC `OR` | ESC `[1;2R` | ESC `[1;5R` | ESC `[1;6R` |
| F4 | ESC `OS` | ESC `[1;2S` | ESC `[1;5S` | ESC `[1;6S` |
| F5 | ESC `[15~` | ESC `[15;2~` | ESC `[15;5~` | ESC `[15;6~` |
| F6 | ESC `[17~` | ESC `[17;2~` | ESC `[17;5~` | ESC `[17;6~` |
| F7 | ESC `[18~` | ESC `[18;2~` | ESC `[18;5~` | ESC `[18;6~` |
| F8 | ESC `[19~` | ESC `[19;2~` | ESC `[19;5~` | ESC `[19;6~` |
| F9 | ESC `[20~` | ESC `[20;2~` | ESC `[20;5~` | ESC `[20;6~` |
| F10 | ESC `[21~` | ESC `[21;2~` | ESC `[21;5~` | ESC `[21;6~` |
| F11 | ??? | ESC `[23;2~` | ESC `[23;5~` | ESC `[23;6~` |
| F12 | ESC `[24~` | ESC `[24;2~` | ESC `[24;5~` | ESC `[24;6~` |
| Insert | ESC `[2~` | ??? | nothing | nothing |
| Home | ESC `[H` | ??? | ESC `1;5H` | ??? |
| End | ESC `[F` | ??? | ESC `1;5F` | ??? |
| PgUp | Esc `[5~` | ??? | ESC `[5;5~` | ??? |
| PgDn | ESC `[6~` | ??? | ESC `[6;5~` | ??? |

Just gloriously inconsistent, and I especially like
`/` and `` ` `` which can each be four different
things.  Plus holding down 'Alt' will stick an escape before
whatever key you press next, even if it was a control character,
including Esc, unless it was already an escape sequence in which
case it does nothing, unless it was an escape sequence with 
modifier values, in which case it adds 2 to the modifier.

| Alt- | Code |
|---|---|
| Alt-A | ESC `A` |
| Alt-1 | ESC `1` |
| Alt-Tab | ESC TAB |
| Alt-Esc | ESC ESC |
| Alt-Shift-5 | ESC `%` |
| Ctrl-Alt-`` ` `` | ESC NUL |
| Alt-F1 | ESC `[1;3P` |
| Alt-F5 | ESC `[15;3~` |
| Ctrl-Alt-Shift-F10 | ESC `[21;8~` |


The longest escape sequence (not counting the escape seems to be 6 characters.
although if there's an actual Meta key it might be 7.

## An aside: ASCII

I've been working in the Linux console ever since there was such
a thing as a Linux console and all this time I had no idea it was possible
to type *all the ASCII characters* from 0 to 127 on a
regular keyboard:

| code | key(s) |
|---|---|
| 0 | Control-2, or Control-`` ` `` |
| 1 .. 26 | Control-A through Control-Z |
| 27 | Escape, or Control-3, or Control-[ |
| 28 .. 31 | Control-4 through Control-7 |
| 32 .. 126 | normal printable characters we know and love |
| 127 | Backspace, or Control-8, or Control-Shift-/ |

