---
title: "Smooth Move: Taming Trajectories with SmoothStep"
layout: draft
uses_mathjax: 3
tags:
  - robots
  - 3dprint
---

## Position, Velocity, Acceleration, Jerk?

[Jerk](https://wikipedia.org/Jerk_%28Physics%29) is the third derivative of
position, or the rate of change of acceleration, which might seem like a pretty
abstract thing to be worried about but:

Imagine a mass in a box under constant acceleration.  The mass is pushing up 
against the side of the box which causes it to accelerate too.  But if we change
the acceleration, the mass is going to slide around until it reaches a new
equilibrium.

Now imagine the box is your skull and the mass is your brain.  Jerk is real!

### Higher Orders

There's also higher derivatives which are sometimes called
[Snap, Crackle and Pop](https://en.wikipedia.org/wiki/Fourth,_fifth,_and_sixth_derivatives_of_position)

## SmoothStep

[SmoothStep](https://en.wikipedia.org/wiki/Smoothstep) is a family of polynomial functions
which smoothly transition from 0 to 1.

`$ S_1(x) = \begin{cases}0, & x <= 0 \\ 3x^2 - 2x^3, & 0 <= x <= 1 \\ 1, & 1 <= x\end{cases} $`

They're kind of like the [Logistic Function](https://en.wikipedia.org/wiki/Logistic_function)
with the same kind of [sigmoid](https://en.wikipedia.org/wiki/Sigmoid_function) curve except
the the tapered ends finish exactly at 0 and 1 instead of tapering off into infinity.

The first derivative of `$ S_1 $`, `$ S^\prime_1 $`, is polynomial too:

`$ S'_1(x) = \begin{cases}0, & x <= 0 \\ -6x^2 + 6x, & 0 <= x <= 1 \\ 0, & 1 <= x\end{cases} $`

and has the handy property that it is neatly zero at both ends.

`$ S_2(x) = \begin{cases}0, & x <= 0 \\ 6x^5 - 15x^4 +10x^3, & 0 <= x <= 1 \\ 1, & 1 <= x\end{cases} $`
but using [Linear Algebra](https://en.wikipedia.org/wiki/Linear_algebra)
this function can be worked out to an arbitrary depth:

`$ S_6(x) = \begin{cases}0, & x <= 0 \\ 923x^{13} - 6006x^{12} + 16380x^{11} - 24024x^{10} + 20020x^9 - 9009x^8 + 1716x^7, & 0 <= x <= 1 \\ 1, & 1 <= x\end{cases} $`

More generally, the `$ n $`-th derivative of the `$ n $`-th smoothstep function starts and ends at zero:

`$ S^{(n)}_n(0) = S^{(n)}_n(1) = 0 $`

## From Here To There

When we [worked out the 5th order Smoothstep function] `$ S_2 $`, we used some linear algebra:

`$ \begin{matrix}0 & 0 & 0 & 0 & 0 & 1 \\ 1 & 1 & 1 & 1 & 1 & 1 \\ 5 & 4 & 3 & 2 & 1 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 2 & 0 & 0 \\ 20 & 12 & 6 & 2 & 0 & 0 \end{matrix} M = \begin{matrix} 0 \\ 1 \\ 0 \\ 0 \\ 0 \\ 0 \end{matrix} $`

`$ M = \begin{matrix} 6 & -15 & 10 & 0 & 0 & 0 \end{matrix} $`
