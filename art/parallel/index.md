---
category: Languages
date: '2011-05-15'
layout: article
redirect_from: '/Languages/parallel/'
slug: parallel
tags:
    - languages
    - functional-programming
    - parallel-programming
title: Functional Parallel Programming
---

Guy Steele’s recent talk [\[VID\]](http://www.vimeo.com/6624203)
[\[PDF\]](http://research.sun.com/projects/plrg/Publications/ICFPAugust2009Steele.pdf)
[\[PAPER\]](http://portal.acm.org/citation.cfm?id=1596550.1596551) on
“Organizing Functional Code for Parallel Execution” [came up a while ago
on
reddit](http://www.reddit.com/r/programming/comments/b0eck/or_foldl_and_foldr_considered_slightly_harmful/)
and I found it very interesting.

I haven’t had a lot to do with functional programming in my career, but
I’m kind of perpetually hovering on the fringes of learning more and I
find myself attracted to the functional way within imperative languages
such as Perl and Python.

One of the things I’ve always found fascinating about Haskell (and Lisp,
for that matter) is that once you dig down far enough, you keep hitting
the singly linked list, formed by consing new elements onto the start of
a slightly shorter list. It always seems strange that there, after
hiking all this way into the functional wilderness, is the datastructure
you left back in the carpark on day 1 of Comp Sci 101.

Anyway, the lecture, and trying to learn Haskell at the moment, got me
thinking. It’s pretty likely that this has already been covered in Guy’s
talk, but in order to understand what he’s on about I had to write it
out myself, so I thought I’d do it here. It won’t make a lot of sense
unless you’ve watched the first half of the video or at least read the
slides, so see you in a while :-)

OK, so here’s the classic Haskell length function:

``` {.sourceCode .haskell}
length [] = 0
length a:x = 1 + length x
```

Imagine we could use the operator ++ on the left hand side (let’s not
call this language Haskell++). Where it normally joins two lists into
one, it would instead split one list into two … IF the list can be split
this way. If this list is empty or singleton, the match fails … just
like the match a:x would fail on an empty list:

``` {.sourceCode .haskell}
length [] = 0
length (x++y) = length x + length y
length _ = 1
```

Having length x + length y would normally be a bad thing, preventing
tail call optimization, but as Guy points out at about the 20 minute
mark (slide 31), this is an “Opportunity for parallelism” ... the two
lengths can be calculated independently.

Of course, if we represent the conc lists as Haskell structures we don’t
need this syntactic sugar, but I think this is exactly the sort of
situation which never gets exploited \_unless\_ there's syntactic sugar.

Also, a [Cool example in
Erlang](http://dustin.github.com/2010/03/04/erlang-conc.html)
