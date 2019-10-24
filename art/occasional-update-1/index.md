---
date: '2019-10-24'
layout: draft
tags:
title: 'Occasional Update'
summary: "Where am I? What have I been up to? Is this thing even working?"
---

I've barely written anything on this blog or made any progress on 
open source stuff in the last year.

Partly it's been because of a big family holiday, our first overseas trip
with the kids.
Partly it's been a bit of [burnout after a busy year](/Dtag/conference/),
or maybe just disaffection at the way the industry seems to be heading,
and taking the whole world with it.
Maybe it's just been a chance to catch up with myself and think about
what I want to be doing.

Some good things have come out of it: my fitness has improved a lot as
I'm cycling a lot more, and I've started to learn ukulele, which I show
no real talent for but I'm enjoying a lot.  It's fun to be a beginner!

I've also been unearthing some stuff from 10 years ago, particularly the
work I was doing on [Virtual Localization](/art/virtual-localization/).
When I walked away from that work it seemed like I'd left my run too late,
but apparently not.  Also there's a bunch of work I did on "Mixed-mode" 
simulation (embedding Linux containers into network simulators) and on
geo-addressing which disappeared off into departmental tech reports and
never saw the light of day again.

There's some weird auto-archaeology going on here.  Lots of the stuff
I'd written was in [LaTeX](https://www.latex-project.org/) and stored in
[CVS](https://en.wikipedia.org/wiki/Concurrent_Versions_System)
or [Subversion](http://subversion.tigris.org/), to
get back to it I had to dig out a CD-ROM drive to read backup disks 
and use [cvs2svn](https://pypi.org/project/cvs2svn/) and
[svn2git](https://github.com/nirvdrum/svn2git).  I'm [throwing lots of 
that code onto Github](https://github.com/nickzoic/old-radio/) so it won't get
lost again, but in 10 years the build pipelines I used for my papers
have slowly rusted and not everything builds any more. I've always 
disliked the idea of checking in "output" files (eg: the built PDFs) but
perhaps this illustrates the usefulness of containers or
[Immutable Builds](complete-containers-immutable-git).

I was looking at some code I wrote in 1999, and it's actually quite 
scary how little has changed in those 20 years.
SQL databases, wrestling with HTTP, DOM updates.
Some parts of the technology have improved 100x, even 1000x but the
overall experience of development has barely changed.


