---
date: '2018-02-01'
layout: draft
tags:
    - backend
    - languages
    - speculation
title: 'Unconventional Numerics'
summary: "It's not just floats and ints, you know ..."
---

Most languages have a pretty conventional hierarchy of numeric types,
consisting of integers and floats and maybe decimals (fixed point)
and rationals (fractions) wedged in between.

The CPU itself probably only supports a few sizes of integer and a 
couple of sizes of float, but using types to label an integer as, eg:
a fixed point number lets your code treat numbers more naturally and
not risk stuffing up your decimal places.

This article is about a couple of other types I've been thinking about.
There's probably prior art if only I knew where to look for it, but 
these aren't represented in the databases or languages I'm familiar with
so I thought it was worth writing about them.

Probabalistic Counters
======================

Not so long ago, [Gangnam Style](https://www.youtube.com/watch?v=9bZkp7q19f0)
became the first YouTube video to clock over 2<sup>31</sup> views, 
[resulting in an integer overflow](https://arstechnica.com/business/2014/12/gangnam-style-overflows-int_max-forces-youtube-to-go-64-bit/)
and forcing YouTube to update to 64 bit counters.

(yeah, that's right, that's a smidge over 2 billion views.  It's now closer to 3 billion views,
but 2<sup>64</sup> should be safe for a while yet ...)

Now, for a lot of applications this is a pretty simple decision ... using an extra 4 bytes on a
counter doesn't really matter compared to a the size of a video file.  But in some applications
shifting all counters to 64 bit might be impractical.

If your values are 'sparse', eg: mostly zero, it might be worth storing only the non-zero 
values.  But this doesn't work well if you're looking for the large values among a lot of small values. 

If we're not worried about individual counts, perhaps we can *scale* the values by
only incrementing our counters `1/N` of the time.  That'll neatly scale the values down
by a factor of `N`, at the cost of introducing some noise.  That noise will be a lot worse
on the small values but Beyond a limit, precision doesn't really matter -- no-one's that
worried about the difference between 2,000,000,000 views and 2,000,000,001, they're displaying
it as '2M' anyway.

If we don't know the range, or we want a greater dynamic range, we can base the probability
of incrementing the counter on its current value.  So, for example,

   P<sub>increment</sub> = 1/(n+1)

Then we just need a function which can turn the recorded number back into an approximate
'real' count.

[Law of Large Numbers](https://en.wikipedia.org/wiki/Law_of_large_numbers)

[Law of the Iterated Logarithm](https://en.wikipedia.org/wiki/Law_of_the_iterated_logarithm)

Probabilities
=============


