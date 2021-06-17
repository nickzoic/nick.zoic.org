---
date: '2021-06-16'
layout: article
tags:
  - architecture
  - www
title: 'QR Codes and the Great Unpleasantness'
summary: 'QR Codes are suddenly everywhere ... what are they, how do they work and how can you use them effectively?'
---

# The Great Unpleasantness

All of a sudden, QR codes are everywhere.
Due to the current viral pandemic, we're being asked to check in to venues to
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
encoding the same information.  That information included a serial number to
track the individual palette, but also lots of information about the product
containe by the palette: what it was, how much there was, date and time of
production, etc.  The system for producing stock was separate from the ERP
system, but when a new palette was scanned, the QR code contained
enough information to import it into the ERP system.
So in effect, we were doing EDI but over barcodes rather than wires.

This project took about 2 years to roll out around Australia and I learned
rather a lot about using barcodes in the field, so this article attempts to
summarize this.

# What is a QR code?

A [QR Code](https://en.wikipedia.org/wiki/QR_code) is a 2 dimensional barcode 
which encodes a string of characters in a way which is easy to scan automatically.
There's built in error checking and correction, and scanning software is able
to correct for rotation (scanning it upside down) and skew (scanning from an angle).

I'm not going to go into symbols, modules, etc here: there's plenty on that
Wikipedia page, but the most important things to consider are:

## Encodings

Like with a lot of barcodes, there are various encodings available:

* purely numeric (0-9)
* alphanumeric (0-9, A-Z, some punctuation)
* binary
* kanji/kana

Larger encodings need more bits per symbol, so a QR code which sticks to 
alphanumeric encoding only needs 68% of the dots of one which encodes the
same length of message using a binary encoding for example.

## Error Correction

Additionally, QR codes can be printed with varying levels of error correction.
Error correction means that if a few of the little black-or-white squares are
misread (perhaps because of some dirt, or a reflection, or whatever) the symbol
as a whole can still be correctly read.

Errors which can't be corrected can still often be detected, which is why 
sometimes you think you've scanned the code and it just ... doesn't.

## QR code size

The number of dots in a QR code varies depending on the amount of information
it has to encode. A larger encoding, more error correction or a longer message
will all need more dots  which means either the barcode gets bigger or the 
dots get smaller.

## URLs

Not all QR codes are URLs, but it's a pretty common application.

If you encode something which looks like a URL, most phones will scan
it and jump to that website.  Conveniently, the first bits of URLs
are not case sensitive so you can often use Alphanumeric encoding
if you plan your URLs right.

# Guidelines

The following guidelines are to help get the best possible scanning experience.
You may have to bend or break some of them for your application, but the closer
you stick to optimal scanning to better the result you're going to get.

## Make it bright

The higher contrast the better.  QR codes are best printing in black and white,
although they scan okay so long as there's a large amount of contrast: you can
get away with a dark blue foreground or a beige background for example.
You can't invert the colours though.

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

## Error correction

Error correction is built into all QR codes, but for a relatively small increase in
barcode size you can increase error correction to "High".

## No funny business

And don't even think about printing a logo in the middle or something.
Sure, people do it, but you're relying on the error correction to fix it and
that's inherently degrading the quality of your error correction.

# Contact Tracing in Victoria

I've been meaning to write this up for about a year now, and every time I 
go to do so I think the whole thing is just about over, but it isn't, and
we're going to have to think about contact tracing for some time yet.

Here in Victoria, the typical contact tracing QR code is used with the
[Service Victoria phone application](https://service.vic.gov.au/check-in).
The code itself is quite huge, but there's a six digit code under the QR code
which gives you a pretty good idea of how few symbols would actually be needed.

For example, here's a Service Vic QR code I found on the web:

![pretty huge QR code](img/ivanhoe.png) 

It's pretty huge, and as a result not that easy to scan.  The code itself encodes the 
string:

```
https://service.vic.gov.au/check-in/start?metadata=eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbklkIjoiYTc3N2I3YjItZjkwZi00OWI5LWJiZmItYjZjZTVhMTkxNTVhIiwibG9jYXRpb25OYW1lIjoiSXZhbmhvZSBQdWJsaWMgR29sZiBDb3Vyc2UiLCJqdGkiOiI5MzJmZjA5Ny1mNDc3LTQ0YmYtYTAxZi1kOGYzMWQ2MjJjNjUiLCJleHAiOjMxODYzNjQ2NzQsImlhdCI6MTYwODUyNzg3NCwiaXNzIjoiaHR0cHM6Ly9kdnJzLnNlcnZpY2UudmljLmdvdi5hdSJ9.AIVsqC8c286fuMvW3HezimSyWcJmwv1bwxl-Bo_Z7i83_zlWCZ_xkwlzUqpsqXFgWR3VLbkZXPfOzQED72W41TOVAaCdJR9Jx38gxccfLYq8Izq4U_AL28_nYsFOgX3PMIqpqrFSAG5U8FTlGDiuGkt4pfsmArsAP2f6MzncE0hZO-AV`
```

That "metadata" nonsense is actually another encoding:
a thing called a [JWT](https://en.wikipedia.org/wiki/JSON_Web_Token) or "JSON Web Token", which is a way
of wrapping up a payload and securely signing it.

The "payload" of the JWT is in turn a [JSON](https://en.wikipedia.org/wiki/JSON) document:

```
{
    "locationId":"a777b7b2-f90f-49b9-bbfb-b6ce5a19155a",
    "locationName":"Ivanhoe Public Golf Course",
    "jti":"932ff097-f477-44bf-a01f-d8f31d622c65",
    "exp":3186364674,
    "iat":1608527874,
    "iss":"https://dvrs.service.vic.gov.au"
}
```

This is some vast overkill.  We know that locations have
six alphanumeric digit codes you can enter in by hand if the barcode
doesn't scan, so there's no need to 128-bit [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier)s, names,
another URL.

We don't need a secure HMAC signature, the exact second the barcode
was created or a 50 year expiry timestamp either:
what scenario are we protecting against here?

## Okay, so what would I do differently?

* For a start, check-in shouldn't need to be an app.  A URL to a public
  website would suffice.  That greatly reduces the technical requirements on phones
  and the requirement for the government to release and maintain an app.
* To avoid you having to re-enter name and phone every time, a cookie
  could be stored on your device in the usual way. No need for a login or whatever.
* The identifier in the QR code can be a lot shorter: the same as the
  six digit identifier you type in!  Fewer symbols = smaller, easier to
  scan QR code.
* The checkin could also be available as a plain old webpage where you enter
  the code, in case you just can't scan it but you're happy to type a URL / 
  load a bookmark / yell "hey google find victorian covid checkin" or whatever
  it is floats your boat.
* These things combined would result in a simpler, easier to scan code
  with much fewer possibilities for things to go wrong!

As an example, the following QR code encodes `HTTPS://EXAMPLE.COM/QR/ABCDEF`
at the highest error correction level.  That's all that is actually needed to
provide a registration service, and would be much easier to print and
scan than the behemoth Service Victoria QR codes:

![example qr code](img/example.png)
