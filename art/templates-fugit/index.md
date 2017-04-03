---
category: etc
date: '2011-04-28'
layout: article
redirect_from: '/etc/templates-fugit/'
slug: 'templates-fugit'
tags: templates
title: Templates Fugit
---

Ever since I started working on Internet Stuff, I've been wrestling with
crazy Template Languages. This article is an attempt to compare some of
the more common template languages out there.

I've consolidated this from a series of blog articles I wrote back in
2009. As a result, some of it may be a little disjointed and/or
outdated.

Template Languages
==================

Like most of its ilk, TT2 doesn’t want to interpret its template
language from within the already interpreted Perl … that’d be silly.
Instead, it compiles the template code to Perl, and loads that. Which
sounds like a great way to do it. So why, in my little benchmark test
(see below), is it &gt;20x slower than doing a whole bunch of prints?
Preliminary benchmark results:

The Benchmark
=============

The very simple benchmark just does a thousand runs of a table with 100
rows of 10 columns each for each of the engines. This is a very very
primitive test, but I wanted something which would be very quick to code
up. I don't count the time it takes to compile the templates, since the
compiled templates are generally cached anyway

[The benchmark source code is available
here](http://code.zoic.org/templates_fugit/)

The Results
===========

As measured on my machine, with all the usual caveats:

  Language   Method / Library         Elapsed
  ---------- ------------------------ ---------
  C          printf                   0.450
  Perl       print                    0.829
  Python     print                    1.567
  Perl       Text::Template::Simple   1.678
  Python     Mako                     1.820
  Python     Jinja                    10.775
  Perl       Template Toolkit 2       25.079
  Perl       HTML::Template           40.510
  Python     django                   46.758
  Python     SimpleTAL                64.546
  Python     genshi                   88.289
  Perl       Petal                    91.444

The C/printf version is “cheating”, it doesn’t read from a data
structure and is just an attempt to see how long it takes to do the
actual I/O. These results don’t match up with the previous ones because
they’re on a different machine, and are to /dev/null to eliminate any
I/O restrictions as a factor. The setup is otherwise the same as for the
previous articles. 91ms might not seem like much, but it all adds up and
this is for a \_very\_ simple benchmark.

‘Petal’ was the real shock … I was expecting that its very abstract
nature would make it relatively easy to optimize the output, but instead
it takes 75x the time to run than the ‘prints’ version.

But isn’t CPU time cheap?
=========================

Well, yeah. It is, compared to programmer time. Which is why we’re doing
this stuff in Perl/Python in the first place … but my point is, if you
can get a 20x speedup by using a faster template language, so long as it
is not particularly much harder to deal with, you might as well. CPU
time may be cheap, but systems admin time isn’t, and running 20 servers
takes more work that running 1, or more to the point, running 100
servers takes more work than running 4.
