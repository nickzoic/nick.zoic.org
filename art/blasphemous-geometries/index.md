---
layout: draft
title: Blasphemous Geometries
uses-mathjax: 3
---

grid for quantized simulation[1] 

[1] games


* nodes as a quantum of area
* edges as a quantum of distance

a "good" grid will have $`A \propto r^2`$

Ideally all nodes will have the same number of edges, although a mix 
of $`N`$ and $`N+1`$ would be okay.  It would be very useful for this
to be a repetitive pattern or at least in some way predictable.

(consider the soccer ball)

## Bad Grids

### Trivial: 0-, 1-, 2- connected

### Ugly: 3-, 4-, 6- connected

A 4- connected grid is the obvious option, the familar grid of graph paper,
the chessboard, minecraft.

```
A - B - C - D
|   |   |   |
E - F - G - H
|   |   |   |
J - K - L - M
```

But drop water on flat ground in minecraft and it'll spread out faster along
the axes than the diagonals, forming a diamond shape.  Starting from one node,
in $`N`$ steps we can cover $`2N^2 + 2N + 1`$ nodes.

```
        4
      4 3 4
    4 3 2 3 4
  4 3 2 1 2 3 4
4 3 2 1 0 1 2 3 4            0 1 2 3 4
  4 3 2 1 2 3 4                2 3 4
    4 3 2 3 4                  3 4
      4 3 4                    4
        4

```
(visualize this as two interlaced diamonds, an outer one with $`(N+1)^2`$ nodes
and an inner one with $`N^2`$ nodes.  Or think of it as a central $`0`$ 
surrounded by 4 triangles each of which has area $`(N^2+N)/2`$ ...)

```
A - B - C - D
| / | / | / |
E - F - G - H
| / | / | / |
J - K - L - M
```
If we add a set of diagonal links to our 4-connected grid we get a 6-connected
grid.  Every node has 6 neighbours.  This is not uncommon as hex maps for war
games and as hex plots for 2D histograms.  The issues are less pronounced than in
4- connected grids but our puddles still aren't round:


```
   3 3 3 3
  3 2 2 2 3
 3 2 1 1 2 3
3 2 1 0 1 2 3            0 1 2 3
 3 2 1 1 2 3                2 3
  3 2 2 2 3                  3
   3 3 3 3
```

Think of this as a central $`0`$ surrounded by six triangles ... our area is 
$`3N^2 + 3N + 1`$.  

That's rounder, but it's still not $`\pi r^2`$

We can think of 3- connected as being like 6- connected but with half the edges
missing.  It isn't very useful or pretty as ASCII art:

```
      3   3
     ,2. ,2.
    3  `1'  3
   ,2. ,0. ,2.
  3' `1' `1' `3
     ,2. ,2.
    3' `3' `3

```

although it does look nice as crochet.  Unsuprisingly, our area is $`(3/2)N^2 + (3/2)N + 1`$.

### Non-planar: 7- and 8- connected

It seems like we can get "rounder" by increasing the number of neighbours per
node.

An 8- connected grid would be like the way a king moves on a chessboard:
all the adjoining squares plus the diagonals.  But these grids aren't planar,
eg: if you flatten them out some edges cross.  The diagonal moves go through
each other.

A 7- connected grid is harder to visualize, but you can imagine trying to add in 
edges to a 6- connected grid.  The areas between the edges are triangles, so
there's no more links you can add in without edges crossing other edges, which 
would make the grid non-planar.

I'm not interested in non-planar grids for now but maybe we'll come back to them.

### 5- connected?

```
A - B - C - D
|   |   |   |
E - F - G - H
| / | / | / |
J - K - L - M
|   |   |   |
N - O - P - Q
| / | / | / |
R - S - T - U
```

