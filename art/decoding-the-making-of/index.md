---
date: '2020-08-27'
layout: draft
summary: 'Behind the scenes of my PyConline AU 2020 presentation'
tags:
  - conference
title: 'Decoding: The making of'
---

![Decoding: Programming Beyond Text Files](img/title-x.png)

So [PyCOnline AU 2020](https://2020.pycon.org.au/) is all online this year 
and I decided to prerecord my presentation of
[Decoding: Programming beyond text files](https://2020.pycon.org.au/program/lyrjgy/)
so as not to have to worry about Internet on the day.

This page is some "behind the scenes" info on how I did it and what I'd do differently
next time ...

# Recording

Recorded on my Olympus E-M5 mkII which I've not really used for video before but
it can record 1080p at 50fps so I figured that would be good.

![Olympus E-M5 with Fuji 28mm](img/camera.jpg)

Lens is a old manual Fuji EBC 28mm f/3.5 on an adaptor (so, equiv 52mm on a m4/3).
I picked this one just because it was the right focal length for the shot I wanted.

I shot this in lots of little takes because I wasn't quite sure how it was all
going to fit together and I *thought* that it'd be easier to fix it up later.

Originally I was planning on chroma-keying (green screening) out my background and
putting the slides *under* my video.  Instead I found there was lots of noise in the
background so I just chroma-keyed out as much as I could and then put the slides 
*over* my video, using "Lighten" to combine them.  It mostly worked.
There's a couple of moments where you can see my shoulder through the image.

Microphone setup was an Olympus lapel mic on a long cable, plugged into the camera,
but because I kept getting caught up in the cable I ended up dangling it from the 
ceiling just out of shot.  This kind of worked but it's a bit "phasey" ... this
room is very reflective.

![Terrible microphone setup](img/microphone.jpg)

## Files

* 70 MOV files
* 17.6 GB
* 1h24m53s total

# Slides

* 67 .PNG files for slides

# Editing

I edited it down with [Davinci Resolve 16](https://www.blackmagicdesign.com/au/products/davinciresolve/) which is fantastic and *free*.

There's certainly a learning curve.

I ended up using the Fusion 'UltraKey' component to delete the background, which
worked okay. The most complicated Fusion code involved:

* two masks to mask out most of the background
* a transform to scale me down and shift me right
* Ultrakey to delete remaining background
* another mask to stop UltraKey deleting bits of my face

## Mysterious Rendering Error

I had a nasty moment towards the very end when with less than 24 hours to go to 
submit the video, on the final render I got this error:

![davinci resolve error message](img/error-message.png)
*Render job 11 failed as the current clip could not be processed. The Fusion composition on the current frame or clip could not be processed successfully*

Which isn't particularly helpful.  I still don't know what it was complaining about.
I eventually found an online tip which said you could make Resolve slightly less fussy
about frame errors by going to:

`Davinci Resolve` >> `Preferences` >> `UI Settings` >> `User` >> `Stop renders when a frame or clip cannot be processed`

Which may have left a single glitchy frame behind but so be it.  The original message
was utterly useless so I have no idea what I could do to fix it.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Dear <a href="https://twitter.com/Blackmagic_News?ref_src=twsrc%5Etfw">@Blackmagic_News</a> please hire me so I can find out who wrote this error message and snub them at parties.</p>&mdash; nick moore (@nickzoic) <a href="https://twitter.com/nickzoic/status/1298450533691191296?ref_src=twsrc%5Etfw">August 26, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

(for future reference: Resolve 16.2.4.016, on Windows 10 Home 1909 18363.1016)


## Intermediate Files:

* 189 GB of intermediate cache / optimized files

A huge amount of data get created as part of the video generation pipeline.
You'd better have somewhere fast to put it.
I ended up having to delete a whole bunch of steam games to make enough room!

## Final Files:

20 minutes 40 seconds of video:

* 1080p: 1.11 GB
* 720p: 454 MB
* 576 (PAL): 274 MB

# If I was going to start over today

* Buy a decent microphone up front and do a lot more test recording and review.
  Probably a ceiling boundary mic would work in this little reverby office.

* It's pretty noisy here so most takes were done quite late at night, most of the ones
  done during daylight were unusable so I should have just not bothered.

* I underestimated how much time it was going to take to glue the parts back together,
  and how tricky it was to get takes filmed on different days to match up with lighting
  and camera position etc.

* I used the Fuji lens because at f/3.5 it's twice as 'bright' as the Olympus zoom at 
  f/4.9 ... quite a lot of shots are 'soft' because the DoF is small and focus was off by a bit.
  It's pretty hard to get this sorted out on your own.
  I'd probably have been better off using the autofocus zoom and making up for the
  smaller aperture with ...

* ... more lights!  I needed more specific lighting.  Again, though, tiny office, I'd
  need to ceiling mount something.

* Also I'd stump up for a better black background.  I used a halloween tablecloth, 
  but it isn't as matte as it should be ... you can see every now and then a grey area
  to my right which is a curve in the fabric (I deleted most of these in post, but a 
  few moments got through).  Black or green felt might have worked better.

* I'd pretend it was a normal conference presentation with slides,
  prop my laptop up under the camera and grab my remote clicker so I could do the thing in
  one long take.  At the same time use `ffmpeg` to record the slides into a video with 
  the same time cues as the talking, then just line them up in the editor and trim 
  where necessary.

* Going up to the camera to start it recording meant that ever recording starts with my 
  big blurry moon face, which means that the white balance and auto exposure is thrown
  way off at the start of each take, and I had to wait a white for it to settle.  There's
  a couple of bits where you can see the light changing when I didn't wait long enough
  for the camera to settle down

* Also this means that the "media library" icons all look like tired ghosts.

* Another way to handle the print-on might have been to make the slides with a black
  background but a transparent corner cut off to show the presenter through. Since the
  slides are just still images this could be nicely alpha blended in, probably making
  all the fancy keying unnecessary.

# A Couple More Thoughts

* Ironically, the slides were written in HTML using `vim`.

* It turns out that Davinci Resolve includes a visual language "Fusion" for manipulating
  videos, and so at least part of the production was done in a visual language!

  ![Fusion Graph](img/fusion.png)

* This annoyed the heck out of me because the project is an opaque thing, there's no way
  to be sure you've backed it up against accidentally deleting the wrong bit of a timeline.

* Really, what I want is a GUI for writing `ffmpeg` filters.
