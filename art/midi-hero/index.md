---
date: '2022-02-22'
layout: article
tags:
  - electronics
  - music
  - microcontrollers
title: 'MIDI Hero'
summary: 'Turning a thrift store Guitar Hero controller into a MIDI controller'
---

# In The Beginning ...

I picked up a [Guitar Hero](https://en.wikipedia.org/wiki/Guitar_Hero)
type controller from the thrift store on impulse (it was $7).
It turns out to be a well-worn
[Playstation 2](https://en.wikipedia.org/wiki/PlayStation_2) controller,
but since I don't have a PS2, well ... it's going to become something else.

![Weird Little Unit](img/weird-little-unit.jpg)
*It's a weird little unit*

Inside, it's very retro ... a total mess of little PCBs and flying wires instead of the
more modern flexi-PCB kind of construction.  But that's good for my 
purposes, since it makes it much easier to butcher.

![Big Mess of Wires](img/big-mess-of-wires.jpg)
*A Big Mess of Wires*

In its current form it has:

* 5 "fret" buttons (resistive rubber contacts I think)
* A tiny power switch and red LED on their own tiny board
* A separate board for the start and select buttons
* Some kind of multi-axis tilt sensor I think
* The "whammy" mechanism, which turns a metric potentiometer
* The main CPU board, with:
  * An anonymous ASIC 
  * The two "strum" buttons
  * A little bluetooth (?) daughterboard
* A battery holder for 4 x AA batteries.

# ... Let There Be Rock

So, the plan is to turn this ridiculous thing into something which can 
actually be played as a musical instrument.  The obvious choice for this 
is [MIDI](https://en.wikipedia.org/wiki/MIDI), a
[standard](http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html)
invented back in 1981 for doing exactly this kind of thing.  The guitar would send 
MIDI messages and then a synthesizer, or synthesizer software running on
a computer, turns that into actual music.

*There are [real](https://koalaaudio.com.au/products/artiphon-instrument-1) 
[ones](https://playjammy.com/) [of](https://www.rorguitars.com/products/expressiv-midi-pro)
[these](http://www.muzines.co.uk/articles/yamaha-g10/347) controllers out there already
but that's not entirely the point.*

Computers can receive MIDI signals from a special interface to the old-school
[5 pin MIDI](https://learn.sparkfun.com/tutorials/midi-tutorial/hardware--electronic-implementation), or [MIDI over USB](https://www.midi.org/midi-articles/basic-of-usb).
Since I don't have one of the former handy right now I'll concentrate on
the latter for the moment.
As a bonus, USB can provide power to the instrument.

*5-pin MIDI or synthesized audio might also be useful for live performance,
but let's not get ahead of ourselves here `:-)`.*

# Inputs

## Frets

5 fret buttons doesn't seem like much compared to the 90-odd fret
positions on a real guitar neck.
But there's a lot of songs which have a small number of chords,
thankfully.
99% of my ukulele songbook would get covered by:

| Gn | Rd | Yy | Bu | Or | Chord | In C  | Notes     |
|----|----|----|----|----|-------|-------|-----------|
| X  |    |    |    |    |   I   |   C   | C E G     |
| X  | X  |    |    |    |   ii  |   Dm  | D F A     |
|    | X  |    |    |    |   II  |   D   | D F♯ A    |
| X  | X  | X  |    |    |   II7 |   D7  | D F♯ A C♯ |
| X  |    | X  |    |    |   iii |   Em  | E G B     |
|    | X  | X  |    |    |   IV  |   F   | F A C     |
|    |    | X  |    |    |   V   |   G   | G B D     |
|    | X  |    | X  |    |   v   |   Gm  | G B♭ D    |
|    | X  | X  | X  |    |   V7  |   G7  | G B D F   |
|    |    | X  | X  |    |   vi  |   Am  | A C E     |
|    |    |    | X  |    |   VI  |   A   | A C♯ E    |
|    |    |    | X  | X  |  ♭VII |   B♭  | B♭ D F    |
|    |    |    |    | X  |   VII |   B   | B D♯ F♯   |
|    |    | X  |    | X  |   vii |   Bm  | B D F♯    |
|    |    | X  | X  | X  |  VII7 |   B7  | B D♯ F♯ A |

Or something like that, anyway.  There's still a few playable combinations
left over.

## Alternative Frets

Chords actually sound pretty bad with a lot of the synth tools
I've been messing with.  They add plenty of weird crap to make up for the
"thinness" of a single note, so maybe we need a chromatic solo mode, maybe
something like:

| Gn | Rd | Yy | Bu | Or | Note |
|----|----|----|----|----|------|
| X  |    |    |    |    | C    |
| X  | X  |    |    |    | D    |
| X  |    | X  |    |    | C♯   |
| X  | X  | X  |    |    | D♯   |
|    | X  |    |    |    | E    |
|    | X  | X  |    |    | F    |
|    | X  |    | X  |    | F♯   |
|    | X  | X  | X  |    | --   |
|    |    | X  |    |    | G    |
|    |    | X  | X  |    | A    |
|    |    | X  |    | X  | G♯   |
|    |    | X  | X  | X  | --   |
|    |    |    | X  |    | B    |
|    |    |    | X  | X  | B♭   |
|    |    |    |    | X  | C    |

or alternatively it might be easier to have one button, probably
the middle button for ergonomics, be a dedicated "sharpener" button:

| Gn | Rd | Yy | Bu | Or | Note   |
|----|----|----|----|----|--------|
| X  |    |    |    |    | C      |
| X  |    | X  |    |    | C♯     |
| X  | X  |    |    |    | D      |
| X  | X  | X  |    |    | D♯     |
|    | X  |    |    |    | E      |
|    | X  | X  |    |    | E♯ = F |
|    | X  |    | X  |    | F      |
|    | X  | X  | X  |    | F♯     |
|    |    |    | X  |    | G      |
|    |    | X  | X  |    | G♯     |
|    |    |    | X  | X  | A      |
|    |    | X  | X  | X  | A♯     |
|    |    |    |    | X  | B      |
|    |    | X  |    | X  | B♯ = C |

Anyway, the point is, it's an arbitrary mapping between button
combinations and note combinations, and those extra "select" buttons
could switch between mappings.

## Strums

The frets would be used to select which chord to play, but the strum sensor would
be responsible for actually triggering it.

![strum strum strum](img/strum-strum-strum.jpg)
*strum mechanism (the two buttons on the right*

The strum mechanism is really just a little cam which operates two switches
which look suspiciously like [ALPS](https://deskthority.net/wiki/Alps_SKCL/SKCM_series)
clone keyboard switches.  These are mounted on the back of the main board,
which mounts to the case using four screws.  I'll probably replace this with a bit of 
proto board with a couple of similar switches on it, but it might be nice to 
consider some kind of [piezo](https://en.wikipedia.org/wiki/Piezoelectric_sensor)
sensor to give the instrument some [expression](https://en.wikipedia.org/wiki/Musical_expression)

The relationship between the two different switches and the MIDI message
I'm not sure about.  Should an upward strum be different from a downward strum?
Is a down-down-down-down strum different to a down-up-down-up strum?
Does holding the 'flipper' down do anything different?
This will take a bit of experimentation too see what "feels" right I guess.

*Up and Down strums could even feed different instrument numbers, or different
modes (eg: chord vs: solo) or voices or octaves or different velocities, or all sorts of things*

## Whammy Bar

There's a little [Whammy Bar](https://en.wikipedia.org/wiki/Vibrato_systems_for_guitar#Origin_of_names)
which operates a standard metric
[potentiometer](https://en.wikipedia.org/wiki/Potentiometer).
It only rotates one way (down), but it should be able to 
feed a MIDI pitch wheel input.

This looked pretty dreadful when I first opened it up, but it's not as 
bad as I thought: I'll just wire it across 3.3V and Ground and that
should be enough to give me a good analog signal for the ADC.

![No whammies!](img/no-whammies.jpg)
*whammy mechanism*

## Other

There's also the START and SELECT buttons which could send other MIDI
messages to change channels or instruments or whatever.

There's plenty of empty real estate on the guitar, so adding in some other
inputs should be possible.  Perhaps for example a
[capacitive slider strip](../esp32-capacitive-sensors/) on the unused
part of the neck for "fretless" operation, or various knobs to send
[MIDI CC](https://www.noterepeat.com/articles/how-to/213-midi-basics-common-terms-explained#G)
messages.

There's a board with a couple of tilt sensors already, but an
[accelerometer](../rocket-surgery-airborne-iot-telemetry-buzzconf/)
would be a more modern alternative and could feed into a control channel as well.

Plus, of course, I should make some room for [neopixels](../saturnalia-a-rotating-christmas-tree/)!

# Microcontroller

Handily there's a [CircuitPython](https://circuitpython.org)
[USB MIDI library](https://circuitpython.readthedocs.io/en/latest/shared-bindings/usb_midi/index.html) already.
I'm a big fan of [not writing C if I don't have to](../linuxconf-2017-hobart/)
and this library supports a lot of [junkbox boards](/tag/microcontrollers/) I already have, so that
seems like an obvious choice.  I just have to find one with enough I/O pins.

Just to begin with I need 5 digital I/O pins for the fret buttons and
2 for the strum buttons.  It'd be nice to have a couple of analogue inputs for
knobs, too.

I have a 'beta' [adafruit Metro M4 Express](https://circuitpython.org/board/metro_m4_express/) lying around from
[some work I did a long time ago](https://github.com/adafruit/circuitpython/issues/703) and it comes with USB-MIDI already on board so it seems like a good choice.  
I've upgraded that to CircuitPython 7.1.1.

*There's also [I2S](https://en.wikipedia.org/wiki/I%C2%B2S) support
so it's possible I could implement a
[Karplus-Strong](http://amid.fish/javascript-karplus-strong) synth right
on the instrument with output to a standard guitar jack, but I'll worry about that later.*

It seems odd at first, but USB devices can present as many kinds of thing
at once, using "endpoints".  So the single USB port on the board can
simultaneously present as a mass storage device (for program code) and as a 
serial terminal device (for the interactive console) and as a MIDI device
for sending music to the computer!

## Making Sounds

Linux audio support continues to be a
[nightmare](http://www.tedfelix.com/linux/linux-midi.html)
but I eventually worked out that the devices were visible from ALSA
and got [fluidsynth](https://www.fluidsynth.org/) working via its GUI "qsynth".
I'm really hoping there's a friendlier way to do this in the future!

```
$ amidi --list-devices
Dir Device    Name
IO  hw:3,0,0  Metro M4 Express MIDI 1
IO  hw:4,0,0  MPK mini play MIDI 1
```

*Update: I've finally worked out that [lmms](https://lmms.en.softonic.com/)
actually does work if you go into the overall settings and set MIDI interface
to "ALSA Raw-MIDI" using the device names above *and* you go into the
instrument settings and tell it to use MIDI input. Duh.*

Using `amidi`, I dumped some raw MIDI messages out of a little AKAI
MIDI keyboard, and then turned them into this work of musical genius:

```
import usb_midi
import time

op = usb_midi.ports[1]

messages = [
    b'\x90\x3C\x39',  # key down, middle C
    b'\x80\x3C\x00',  # key up
    b'\x90\x40\x48',
    b'\x80\x40\x00',
    b'\x90\x43\x49',
    b'\x80\x43\x00',
    b'\x90\x43\x49\x90\x40\x4C\x90\x3C\x4D',
    b'\x80\x43\x00\x80\x40\x00\x80\x3C\x00',
]

while True:
    for msg in messages:
        op.write(msg)
        time.sleep(0.5)
```

This is just sending a sequence of raw MIDI events over the USB port, and yes!
It works!

* `\x90` is a key down message, and `\x80` is a key up message.

* `\x3c` (60) is Middle C, and `\x40` (64) and `\x43` (67) are the E and G above that.

* The third number in each message is a "velocity", how hard the key was hit, more
  or less.  That varies a little for key down, and is zero for the key up messages.

* The last two lines combine the up and down messages for three notes C, E and G
  to play a C Major chord.

So, all our code will have to do is listen for buttons and send similar messages.
Almost too easy! 

## Jammin' ...

Also in the junkbox: a
[Freetronics ThinkerShield](https://www.freetronics.com.au/products/thinker-shield) 
There's not a lot on this board, although it's kind of handy if you like
alligator clips, but there is a pot and a pushbutton.  Which is enough to
implement our first interactive MIDI instrument, which sounds like a 
glitchy theremin played through autotune:

```
import usb_midi
import digitalio
import analogio
import board

midi_out = usb_midi.ports[1]

knob = analogio.AnalogIn(board.A5)

button = digitalio.DigitalInOut(board.D7)
button.switch_to_input()

while True:
    # Just busy wait until the button gets pressed
    while not button.value: pass

    # Scale the 0..65535 range of the input to the 0..127 range
    # of MIDI notes (not very nicely)
    note = knob.value // 512

    # Play the note
    midi_out.write(bytes((0x90, note, 0x7F)))

    # Wait until the button gets released or the knob gets moved
    while button.value and (knob.value // 512 == note): pass

    # Cancel the old note, go back around and wait for next note.
    midi_out.write(bytes((0x80, note, 0x00)))
```

[source](src/shield1/main.py)

I can already see that CircuitPython's [lack of interrupt driven I/O](https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio/handling-interrupts) is going to drive me bananas, but let's stick with it for now.

# No Guts, No Glory

It's time for the innards of the guitar to come out.  The original boards can go
in the junkbox, perhaps they'll be handy to make a MIDI *input* for PS2
so you can play Guitar Hero on a keytar `:-)`

Once all the extraneous parts are out, in goes a new board for the strum buttons.
The dimensions are actually pretty tight, so I desoldered the old switches.
The little protoboards i had are juuuuuust too short for this job but this is okay
for a first go around.

![New Strum Buttons](img/new-strum-buttons.jpg)
*New Strum Buttons board*

So I've done a very rough job of soldering the five fret buttons and two 
strum buttons to I/O pins 6 through 12, and wedged the board into a corner
of the case ... and well, it kinda sorta works:

```
import usb_midi
import digitalio
import board

def make_button(pin):
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    return btn

# Note: buttons are all pulled *low* by being pressed
# TODO fix this just to make code more readable

s_up = make_button(board.D6)
s_dn = make_button(board.D7)

f_gn = make_button(board.D8)
f_rd = make_button(board.D9)
f_yy = make_button(board.D10)
f_bu = make_button(board.D11)
f_or = make_button(board.D12)

chords = {
        1: [ 60, 64, 67 ],      # C
        2: [ 62, 66, 69 ],      # D
        3: [ 62, 65, 69 ],      # Dm
        4: [ 67, 71, 74 ],      # G
        5: [ 64, 67, 71 ],      # Em
        6: [ 65, 69, 72 ],      # F
        7: [ 62, 66, 69, 73 ],  # D7
        8: [ 69, 73, 76 ],      # A
        10: [ 67, 70, 74 ],     # Gm
        12: [ 69, 72, 64 ],     # Am
        14: [ 67, 71, 74, 77 ], # G7
        16: [ 71, 75, 78 ],     # B
        20: [ 71, 74, 78 ],     # Bm
        24: [ 70, 74, 77 ],     # B♭
        28: [ 71, 75, 78, 81 ], # B7
    }

def get_notes():
    val = ( (1 if not f_gn.value else 0) +
            (2 if not f_rd.value else 0) + 
            (4 if not f_yy.value else 0) +
            (8 if not f_bu.value else 0) +
            (16 if not f_or.value else 0) )
    return set(chords.get(val, []))

midi_out = usb_midi.ports[1]

while True:

    while s_up.value and s_dn.value: pass

    notes = get_notes()

    for note in notes:
        midi_out.write(bytes((0x90, note, 0x5f)))

    while not s_up.value or not s_dn.value: pass

    for note in notes:
        midi_out.write(bytes((0x80, note, 0)))
```

[source](src/chords1/main.py)


# UPDATE 24th February 2022

I implemented the "Alternative Frets" tuning as above, which 
sounds a lot better through the synth program than feeding
it chords. I also made an "up strum" shift the note played 
up an octave, so now the instrument has 2 octaves range,
from C4 to C6.

I also hot-glued the CPU board into place, added strain relief to the
USB cable and rewired the thing completely.  Originally I'd just soldered
onto a bunch of 0.1" strip headers and plugged those into the 
Metro board, but that was pretty dodgy.  This time I used a 
little "prototype shield" board I bought off Ebay ages ago.
This makes it a lot easier to solder and much less prone to falling
to pieces in your hands.  There's no room on the top side of the other
proto board as it turns out, it's hard up against the case, so this will
also give me a place to wire in an accelerometer as well.

All the pin assignments have changed, but there's now a whammy bar 
and the select and start buttons are wired in.  The input pins are 
all set to pull down and the buttons pull them up, which makes the 
code more readable!  

When I get around
to it I'll add a pair of pots for setting control channel info.

![all rewired up](img/all-rewired-up.jpg)
*All rewired up*

The soldering is terrible, but the code is very slowly improving:


```
import usb_midi
import digitalio
import analogio
import board

def make_button(pin):
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.DOWN
    return btn

fret_green = make_button(board.D2)
fret_red = make_button(board.D3)
fret_yellow = make_button(board.D4)
fret_blue = make_button(board.D5)
fret_orange = make_button(board.D6)

button_select = make_button(board.D8)
button_start = make_button(board.D9)

strum_down = make_button(board.D10)
strum_up = make_button(board.D11)

pitch_wheel = analogio.AnalogIn(board.A0)

notes = {
        (True, False, False, False, False): 60,    # C
        (True, False, True, False, False):  61,    # C♯
        (True, True, False, False, False):  62,    # D
        (True, True, True, False, False):   63,    # D♯
        (False, True, False, False, False): 64,    # E
        (False, True, True, False, False):  65,    # F
        (False, True, False, True, False):  66,    # F♯
        (False, False, True, False, False): 67,    # G
        (False, False, True, False, True):  68,    # A♯
        (False, False, True, True, False):  69,    # A
        (False, False, False, True, True):  70,    # B♭
        (False, False, False, True, False): 71,    # B
        (False, False, False, False, True): 72,    # C
    }

midi_out = usb_midi.ports[1]

# All notes off
midi_out.write(bytes((0xb0, 123, 0)))

while True:

    while not strum_up.value and not strum_down.value: pass

    frets = (fret_green.value, fret_red.value, fret_yellow.value, fret_blue.value, fret_orange.value)
    note = notes.get(frets, None)
    
    if note is not None:
        if strum_up.value: note = note + 12
        midi_out.write(bytes((0x90, note, 0x3f)))

        while strum_up.value or strum_down.value:
            
            pitch_down = (65000 - pitch_wheel.value) >> 3
            if pitch_down < 0: pitch_down = 0
            
            pitch_down = 0x2000 - pitch_down
            pitch_l = pitch_down & 0x7F
            pitch_h = pitch_down >> 7
            midi_out.write(bytes((0xE0, pitch_l, pitch_h)))
            
        midi_out.write(bytes((0x80, note, 0)))
```

[source](src/solo1/main.py)

I've also been playing with LMMS, and have worked out that by assigning
a channel ID to each instrument, I can make it specific to that MIDI 
channel.  The MIDI channel could be set by the strum direction or by the
"Select" button, either way.  It's quite nice to be able to switch 
instrument chains at the touch of a button.

# TO BE CONTINUED

So it's kinda sorta playable, but there's a lot of things still to do:

* Work out where latency is coming from (it's not as bad as it was)
* Find an instrument which sounds nice in LMMS (uh, maybe)
* Record a video (with kickass sound!)

Further work (maybe):

* Switch to a smaller, battery-powered CPU
* Implement 5-pin MIDI and/or an onboard synthesizer.
* Add some more controls etc.

# UPDATE: IS THIS A GOOD IDEA

No.

MIDI instruments are cool.
If you want to make an actual MIDI musical instrument,
don't try to turn a $7 toy into one, start from a blank
canvas.
These fret buttons are super nasty rubber things
and there aren't really enough of them.
This strum mechanism is crappy and plastic.
Maybe a brand-name controller would be less crappy.

It was kind of fun though and it looks pretty funny.

You could easily make something nicer using good quality
keyboard switches for the frets and
[velocity-sensitive piezo pads](https://beammyselfintothefuture.wordpress.com/2015/01/28/sensing-hit-velocity-and-quick-subsequent-hits-of-a-piezo-with-an-arduino-teensy/) 
for the "strum" mechanism.

My "vision" for it would have a grid of keys for the fretboard, perhaps
arranged like a tiny piano or perhaps more like the buttons on a
[Button Accordion](https://en.wikipedia.org/wiki/Chromatic_button_accordion).
For strumming, there would be one or more velocity sensitive pads which could be
tapped with the right hand, with different pads corresponding to different MIDI
channels, and some knobs for setting parameters.

An alternative would be to avoid MIDI altogether, and instead have the fret
buttons activate a series of simple electronic
[electrical resonators](https://en.wikipedia.org/wiki/Electrical_resonance)
set up to very slightly decay, and the piezo strum sensor to inject an
electrical 'kick' into these active circuits to cause them to ring.
It might be fun to prototype something like this anyway.

# MORE STUFF

* This [review of the ROR MIDI PRO 2 Guitar](https://www.youtube.com/watch?v=4-BR1qBFcNQ) which is an actual guitar with lots of MIDI controls, pads and so on.
* The [Suzuki Omnichord](http://www.suzukimusic.co.uk/omnichord-heaven/index.html) and [Suzuki Q-chord](http://www.suzukimusic.co.uk/qchord/) are a similar concept
  to the "vision" thing above, although I don't know how the "strum plate" works.
* [Another one on the Q-chord and other electronic zitherish instruments](https://www.youtube.com/watch?v=pAIar0O-yvg)
* [Q-Chord.net](https://web.archive.org/web/20120328025455/http://qchord.net/docs/qchord-manual.htm), sadly defunct but still with us thanks to archive.org
* [The Magical Musical Thing](https://www.youtube.com/watch?v=jRKqVYAfbGw) 

# UPDATE 2023

Since back-of-an-envelope calculations lead me to conclude that an array of
actual physical AF LC oscillators will be inconveniently huge, I'm wondering how it'd
work to have an audio sensor, something like a piezo pickup attached to a 
metal plate, feeding signal into a multi-'string' implementation of the
[Karplus-Strong](http://amid.fish/javascript-karplus-strong) synthesis algorithm
running on a microcontroller.  You could then tap, rap, slap, scrape or shout into 
the pickup and that signal would be used as the input to the KS filter, to be
tuned and decayed.

