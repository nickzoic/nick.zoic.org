---
date: '2021-01-21'
layout: draft
tags:
  - architecture
title: 'QR Codes, How to use'
summary: 'QR Codes are suddenly everywhere ... what are they, how do they work and how can you use them effectively?'
---

# The Great Unpleasantness

All of a sudden, QR codes are everywhere.
Due to the current Great Unpleasantness, we're being asked to check in to venues to
make contact tracing easier, and after the
[utter failure of Bluetooth-based automatic tracing](https://github.com/vteague/contactTracing/blob/master/blog/2020-07-07IssueSummary.md) 
the common mechanism seems to be QR codes.

But what are they, how do they work and how can you use them effectively?

## Kept in the Dark and Fed Bullshit

Several years ago I worked on a
[project for a large agricultural client](https://nick.zoic.org/art/osdc-2015-hobart/), a 
producer of mushrooms.  Mushrooms are fascinating things in their own right
but this project was all about the logistics of mushroom delivery: how to get
the right palette of mushrooms to the right place at the right time.

In this particular project, there was a divide between production facilities and
a separate, SAP ERP system.  Palettes were produced in one system but warehousing
was handled in the other.  One option would have been to implement some kind of
EDI process between the systems, but initial investigations showed that this was
error prone due to manual interventions in the process: the data coming out of 
the production system wasn't always correct.

We worked around this with QR Codes.  Every palette produced got a sticker 
containing human readable information about that palette, and a QR code 
encoding the same information.  Each sticker had a unique serial number,
so that palettes could be tracked from place to place.  When a new palette
was scanned, the QR code contained enough information to create it in the 
ERP system.  So in effect, we were doing EDI but over barcodes rather than wires.

This project took about 2 years to roll out around Australia and I learned
rather a lot about using barcodes in the field, so this article attempts to
summarize this.

# What is a QR code?

A [QR Code](https://en.wikipedia.org/wiki/QR_code) is a 2 dimensional barcode 
which encodes a string of characters in a way which is easy to scan automatically.
There's built in error checking and correction, and scanning software is able
to correct for rotation (scanning it upside down) and skew (scanning from an angle).

## Encodings

## Error Correction


# Guidelines

The following guidelines are to help get the best possible scanning experience.
You may have to bend or break some of them for your application, but the closer
you stick to optimal scanning to better the result you're going to get.

## Make it bright

The higher contrast the better.  QR codes are best printing in black and white,
although they scan okay so long as there's a large amount of contrast.
When placing codes, consider lighting too: you want them to be well lit, but
to make sure the user's camera doesn't cast a shadow on the code which may 
confuse scanning.

Avoid shiny stock or lamination which may cause reflections to obscure parts of the code.

## Make it big

QR codes can be printed at any size, subject to the limits of your printer and
your real estate, but the camera you're using to scan them has some limitations too.
Phone cameras don't generally focus well at very close distances, so if you print
your codes too small you might have trouble scanning them.

For a typical phone camera, you want the code
to be taking up a good amount of the screen when the phone is 20cm or so from the
page, so at least 70mm across.

## Keep it flat

QR codes don't scan well on curved surfaces such as cylinders or t-shirts.
You can reduce the amount of curvature by making the code a bit smaller.

If you can, place the QR code so that it can be scanned face-on, with a minimum
of skew.  While QR code libraries can correct some skew, they have their limits and
the easier you make it for the software the more consistent the results.

## Respect the borders

QR code standards call for a white border around the code, three times the width
of a single QR code pixel.  I know your graphic design people won't like it, but 
do it anyway, or at the very least keep any interference in this area to the palest
of colours.

## No funny business

And don't even think about printing a logo in the middle or something.
Sure, people do it, but you're relying on the error correction to fix it and
that's inherently degrading the quality of your error correction.

