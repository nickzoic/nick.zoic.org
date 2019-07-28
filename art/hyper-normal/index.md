---
date: '2019-05-14'
layout: draft
tags:
    - speculation
    - maths
title: 'Hyper-Normal'
summary: "Why is it that every case is an exception to a rule?"
---

## Of Lines, Squares, Cubes and Hypercubes

Sample a single variable, it doesn't really matter what we're measuring.

For the sake of the example, let's assume it has a
[normal distribution](https://en.wikipedia.org/wiki/Normal_distribution).
(if it doesn't measure it in such a way that it does).

About 95.5% of samples will be within 2 standard deviations of the mean.  
About 4.5% of the population, by this definition, are 'outliers'.

OK, so now imagine a distribution of two unrelated variables.
Rather than lying along a line, our points lie in a plane.
95.5% of points within the boundaries of one axis, and 95.5% are within the
boundaries of the other axis, and because the two variables are unrelated
we can calculate that `95.5% x 95.5% = 91.20%` of points will be within both sets of
boundaries.  Or to put it another way, 8.80% of points are outliers in at least
one dimension.

With three variables, you can think of the points as a cloud in three dimensions.
It's getting harder to draw, but the 'normal' region is now a cube,
with most points within the cube but some outside.
In each dimension, 95.5% of points lie within the walls of the cube.
So the probability of a point lying inside the cube in all three dimensions is
`95.5% * 95.5% * 95.5% = 87.1%`.  About 12.9% of points are outliers, points which
are outside the cube in at least one direction.

But let's imagine we have even more variables, more dimensions to play with.
It's hard to visualize [hypercube](https://en.wikipedia.org/wiki/Hypercube)s,
but we can extrapolate the maths above.
An N-dimensional cube has `95.5% ^ N` of points within it so it's easy to calculate
the number of points within and without the cube:

dimensions|normies|outliers
:---:|:----:|:----:
  1|95.5|4.5
  2|91.2|8.8
  3|87.1|12.9
  4|83.2|16.8
  5|79.4|20.6
  6|75.9|24.1
  7|72.4|27.6
  8|69.2|30.8
  9|66.1|33.9

By the time we're measuring 9 dimensions, over a third of samples are an outlier in at 
least one dimension.

## Exceptional People

We can keep the maths going into more and more variables!

I put it to you that people are very very complicated things and that people
do not in fact have
[four dimensional personalities](https://en.wikipedia.org/wiki/Myers%E2%80%93Briggs_Type_Indicator)
but *hundreds* of variables, some of which are more obvious and some of which
are less so but all of which are contributions to their individual personality.

Let's assume there's a hundred or so dimensions which we can measure.
What are the odds that *you* are an outlier in at least one of those?

dimensions|normies|outliers
:---:|:----:|:----:
 10|63.1|36.9
 20|39.8|60.2
 30|25.1|74.9
 40|15.9|84.1
 50|10.0|90.0
 65| 5.0|95.0
 85| 2.0|98.0
100| 1.0|99.0

In other words, if you're *not* an outlier in some way or another,
that's pretty damn unusual!
