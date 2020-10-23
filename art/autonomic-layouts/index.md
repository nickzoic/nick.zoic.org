---
date: '2020-10-24'
layout: draft
title: 'Autonomic Layouts'
tags:
    - speculation
    - languages
summary: |
    Following up on the "Programming Beyond Text Files" with some
    further points ...
---

*This follows up on [Programming Beyond Text Files](/art/programming-beyond-text-files/)
and [DECODING: Programming Beyond Text Files](/art/decoding-programming-beyond-text-files/)*

# Autonomic Layouts

## Visual Programming Layout Problem

One thing which always gets brought up when talking about visual programming
languages is how fiddly they are.  Nodes are dragged and dropped onto an arbitary
space and the relationship between the nodes is left to the reader's imagination.

I attempted to provide some guidance for this in 
[Flobot](/art/flobot-graphical-dataflow-language-for-robots/) by
restricting sensor nodes to the top of the screen, and actuator nodes to the bottom
of the screen.  Nodes always have inputs on top and outputs on the bottom, so the
logical flow from top to bottom is established.

You can buck the trend and build Flobot networks in weird S shapes but loops
are disallowed and so there's a clear hierarchy. 

## Automatic Node Placement

One possibility would be to use
[Force Directed Placement](https://en.wikipedia.org/wiki/Force-directed_graph_drawing) 
or Energy Minimization or similar to place nodes in "the right place".

(I'm a bit obsessed with these kids of algorithms, ever since playing with
[Xspringies](https://web.archive.org/web/20130330210456/http://www.cs.rutgers.edu/~decarlo/software.html) and [Graphviz](https://graphviz.org/) as an undergrad: see also [Virtual Localization](https://nick.zoic.org/art/virtual-localization/))

Nodes would then automatically locate themselves between their related nodes by attraction,
avoiding overlapping with other nodes by repulsion.
Clever algorithms can avoid local minima and end up with a "nice" layout every time.

With any non-trivial layout there are many equivalent 'solutions', 






