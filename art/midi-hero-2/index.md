---
date: '2023-06-30'
layout: draft
tags:
  - electronics
  - music
  - microcontrollers
title: 'MIDI Hero (2)'
summary: 'Turning a thrift store Guitar Hero controller into a MIDI controller (continued)'
---

# MIDI Hero (part 2)

Well, it looks like [we're going to PyConAU](https://2023.pycon.org.au/program/8PDEHA/) and to celebrate
the [MIDI Hero guitar](/art/midi-hero/) is going to get some sensor upgrades ...

Sticking with the [Adafruit Metro M4 Express](https://circuitpython.org/board/metro_m4_express/) currently 
in it, we've got quite a few pins to play with:

| Pin | Function |
|-----|----------|
| A0  | Analog Input or Output |
| A1  | Analog Input or Output |
| A2  | Analog Input or Digital I/O |
| A3  | Analog Input or Digital I/O |
| A4  | Analog Input or Digital I/O |
| A5  | Analog Input or Digital I/O |
| SDA | SDA or Analog Input |
| SCL | SCL or Analog Input |
| D0  | Digital I/O or Serial1 RX |
| D1  | Digital I/O or I2S SDI or Serial1 TX |
| D2  | Digital I/O or I2S MC |
| D3  | Digital I/O or I2S BCK |
| D4  | Digital I/O |
| D5  | Digital I/O |
| D6  | Digital I/O |
| D7  | Digital I/O |
| D8  | Digital I/O or I2S SDO |
| D9  | Digital I/O or I2S WS |
| D10 | Digital I/O |
| D11 | Digital I/O |
| D12 | Digital I/O |
| D13 | Digital I/O (red LED) |
| SCK | Digital I/O or SPI SCK |
| MISO | Digital I/O or SPI MISO |
| MOSI | Digital I/O or SPI MOSI |

There were three things I wanted to add to this project:

* On-board Synthesis (Audio Out) 

  This would be cool because the instrument could have its own voice rather than
  being just a synth input device.

* More fret controls, possibly a fretless slider

  The five buttons are pretty limiting, and there's plenty of room on the 'fretboard'
  for more controls.

* Nicer strum control, possible a piezo or similar sensor

  The clicky strum thingy is quite annoying, I'm interested to see how a piezo or 
  force sensor would feel to play.

So let's work out how those might work.

![Endless Possibilities](img/endless-possibilities.jpg)
