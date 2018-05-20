---
category: etc
date: '2012-02-16'
layout: article
redirect_from: '/etc/gcc-linker-libs/'
slug: 'gcc-linker-libs'
tags:
    - c
title: 'GCC 4.6 linker switches'
summary: GCC 4.6 is slightly fussier about the order of its options than predecessors ...
---

An odd little one: I was compiling some older code on gcc 4.6 / Ubuntu
11.10 and it failed to make, with the traditional error:

    undefined reference to `sqrt'

My Makefile was trying to do something like this:

    gcc -c -o eg.o eg.c
    gcc -lm -o eg eg.o

... yep, there's `-lm` so what's the problem?

It turns out that gcc 4.6 has become fussier about the order of its
options now, and wants the libs on the end when linking, like this:

    gcc -c -o eg.o eg.c
    gcc -o eg eg.o -lm

This will catch you out if you set up your Makefile like this:

    LDFLAGS=-lm

Because the libs always appear up front. Instead, put the libs on the
end where they belong by doing this in the Makefile:

    LDLIBS=-lm

If you're still having trouble with the order of libraries, it might
help to add this as well:

    LDFLAGS=-Xlinker --no-as-needed

Which will pass the `--no-as-needed` flag to `ld`, to relax the
constraints on the order which things are evaluated by the linker, or
something.
