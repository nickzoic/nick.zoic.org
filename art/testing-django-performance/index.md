---
category: Python
date: '2013-07-11'
layout: article
redirect_from: '/Python/testing-django-performance/'
slug: 'testing-django-performance'
summary: |
    I presented at the MelbDjango user group on 11 July 2013, here's the
    slides and some quick scribblings re: the content of my talk, and the
    feedback from the Djangonauts present.
tags:
    - python
    - django
    - testing
title: Testing Django Performance
---

I presented at the [MelbDjango](http://melbdjango.com/) user group on 11
July 2013, [here's the slides](../../talk/melbdjango1/).

Notes
=====

Some quick scribblings re: the content of my talk, and the feedback from
the Djangonauts present.

Performance Testing
-------------------

I'm talking about Performance Testing, not particularly about
Performance Improvement, although I'll touch on a few common traps
later. Specifically, I'm splitting testing up into:

-   Code Profiling: where are the bottlenecks, what do we try next?
-   Relative Performance: we've made some changes, did it help?
-   Absolute Performance: can we survive success?

Test Platform
-------------

This is really just a plug for [Amazon AWS](http://aws.amazon.com/)
`:-)`

Synthetic Test Data
-------------------

Empty databases go fast! You need to work with the business people, or
your own business plan, to work out what the requirements of "success"
are for your project, and then generate synthetic test data which fits
that profile, so that your testing actually has some meaningful results.

Django makes it very easy to generate test data from simple Python code.
I like the 'random', 'inflect' and 'loremipsum' modules for this.
Generating test data which looks a lot like real data not only makes
your testing more relistic, it makes the test data useful for your
designers etc as dummy data.

> **note**
>
> Sam Stewart pointed out [Factory
> Boy](https://github.com/rbarrois/factory_boy) which I haven't used but
> looks like an easy way to set this up.

Simulating Load -- Siege
------------------------

[Siege](http://www.joedog.org/siege-home/) is one of the easier load
testing tools to get into.

The important thing here is to make sure your load testing model also
matches the business model ... Three big things to consider are:

-   Concurrency: how many users do we expect, and how much will they
    overlap
-   URLs: we need a list of URLs for Siege to probe, generally we can
    generate this from python code too.
-   Cacheability: There's a big difference between 10000 articles
    accessed uniformly and 10000 articles for which 90% of accesses are
    for the "top 100".

I had collected some data showing this off but it didn't really fit into
the time available, maybe next time!

System Under Load
-----------------

> **note**
>
> I somehow didn't end up with a slide for this, but ...

Look at where the CPU is going:

-   If it is largely in django's 'python' processes, suspect templates.
-   If it is largely in postgres/mysql processes, suspect bad queries.
-   If there doesn't seem to be much load but everything is going slow,
    suspect I/O bottleneck (probably bad queries doing table scans).

Antipatterns -- N + 1
---------------------

Or: how to not torture your SQL layer.

Query Logging
-------------

Postgres & MySQL both offer quite good options for logging queries.

> **note**
>
> There's also lots of middleware options, which I think I forgot to
> mention.

Other Bottlenecks
-----------------

-   Disk IOPS, you'll want to learn about 'iostat' or your system's
    equivalent
-   Network: sometimes you run into limited bandwidth or resources such
    as sockets / ports.
-   Entropy: I thought I'd written a blog post about this but it turns
    out I never got around to finishing it. Some refs:

    -   [Randomness and Entropy in Ubuntu
        9.10](http://bredsaal.dk/improving-randomness-and-entropy-in-ubuntu-9-10).
    -   [Timer Entropy Daemon](http://www.vanheusden.com/te/)
    -   [RNG Utils](http://github.com/infinity0/rngutils)
        (entropy gatherers)

    I couldn't remeber the name of the system command to check the
    entropy pool in linux, because all you have to do is:

        cat /proc/sys/kernel/random/entropy_avail 

    It may sound a bit farfetched but I've run into this problem on a
    couple of production systems which happen to be running on virtuals.

Other Stuff
===========

-   The slides were put together with
    [Reveal.js](http://lab.hakim.se/reveal-js/) which is really just a
    bundle of HTML5 you can hack on.
-   For the same kind of thing in a friendlier package, Brenton used
    [slide.es](http://slid.es/). I might give that a go next time ...
-   I seem to remember ranting on about [Design Patterns in Dynamic
    Programming](http://norvig.com/design-patterns/), and [Design
    Patterns in
    Python](http://legacy.python.org/workshops/1997-10/proceedings/savikko.html).
-   I probably also went on about the amazing work of [Doug
    Engelbart](http://en.wikipedia.org/wiki/Douglas_Engelbart) (1925 -
    2013), especially the [Mother of All
    Demos](http://archive.org/details/dougengelbartarchives).
-   Thanks to [Common Code](http://commoncode.com.au/) for organizing,
    hosting and sponsoring [MelbDjango](http://melbdjango.com/).
