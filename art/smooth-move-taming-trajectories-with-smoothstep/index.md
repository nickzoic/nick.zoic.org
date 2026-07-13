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

## SmoothStep and SmootherStep and Smooth<sup>n</sup>Step

[SmoothStep](https://en.wikipedia.org/wiki/Smoothstep) is a family of polynomial functions
which smoothly transition from 0 to 1.

`$ S_1(x) = \begin{cases}0, & x <= 0 \\ 3x^2 - 2x^3, & 0 <= x <= 1 \\ 1, & 1 <= x\end{cases} $`

They're kind of like the [Logistic Function](https://en.wikipedia.org/wiki/Logistic_function)
with the same kind of [sigmoid](https://en.wikipedia.org/wiki/Sigmoid_function) curve except
the the tapered ends finish exactly at 0 and 1 instead of tapering off into infinity.

The first derivative `$ S^\prime_1 $`, is polynomial too:

`$ S'_1(x) = \begin{cases}0, & x <= 0 \\ -6x^2 + 6x, & 0 <= x <= 1 \\ 0, & 1 <= x\end{cases} $`

and has the handy property that it is neatly zero at both ends.

`$ S_2(x) = \begin{cases}0, & x <= 0 \\ 6x^5 - 15x^4 +10x^3, & 0 <= x <= 1 \\ 1, & 1 <= x\end{cases} $`
but using [Linear Algebra](https://en.wikipedia.org/wiki/Linear_algebra)
this function can be worked out to an arbitrary depth:

`$ S_6(x) = \begin{cases}0, & x <= 0 \\ 924x^{13} - 6006x^{12} + 16380x^{11} - 24024x^{10} + 20020x^9 - 9009x^8 + 1716x^7, & 0 <= x <= 1 \\ 1, & 1 <= x\end{cases} $`

More generally, up to the `$ n $`-th derivative of the `$ n $`-th smoothstep function starts and ends at zero:

`$ S^{(m)}_n(0) = S^{(m)}_n(1) = 0 ; m <= n $`

If you want to mess around with these equations in Python, the `numpy.polynomial` library is rather handy:

```
>>> from numpy.polynomial import Polynomial
>>> S_6 = Polynomial([0,0,0,0,0,0,0,1716,-9009,20020,-24024,16380,-6006,924])
>>> print(S_6)
0.0 + 0.0·x + 0.0·x² + 0.0·x³ + 0.0·x⁴ + 0.0·x⁵ + 0.0·x⁶ + 1716.0·x⁷ -
9009.0·x⁸ + 20020.0·x⁹ - 24024.0·x¹⁰ + 16380.0·x¹¹ - 6006.0·x¹² + 923.0·x¹³
>>> pop = S_6.deriv(6)
>>> print(pop)
0.0 + 8648640.0·x - (1.8162144e+08)·x² + (1.2108096e+09)·x³ - (3.6324288e+09)·x⁴ +
(5.4486432e+09)·x⁵ - (3.99567168e+09)·x⁶ + (1.14162048e+09)·x⁷
>>> pop(0)
np.float64(0.0)
>>> pop(1)
np.float64(0.0)
```

## From Here To There

When we [worked out the 5th order Smoothstep function](https://en.wikipedia.org/wiki/Smoothstep#5th-order_equation)
`$ S_2 $`, we used some linear algebra to work out the 
coefficients `$ a_n $`:

`$ \begin{bmatrix}0 & 0 & 0 & 0 & 0 & 1 \\ 1 & 1 & 1 & 1 & 1 & 1 \\ 0 & 0 & 0 & 0 & 1 ^ 0 \\ 5 & 4 & 3 & 2 & 1 & 0 \\ 0 & 0 & 0 & 2 & 0 & 0 \\ 20 & 12 & 6 & 2 & 0 & 0 \end{bmatrix} \begin{bmatrix} a_5 \\ a_4 \\ a_3 \\ a_2 \\ a_1 \\ a_0 \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \\ 0 \\ 0 \\ 0 \\ 0 \end{bmatrix} $`

Our 'target' matrix can represent other situations of starting and finishing position, velocity and acceleration:

`$ T = \begin{bmatrix} x_0 & x_1 & v_0 & v_1 & a_0 & a_1 \end{bmatrix} $`

```
>>> import numpy
>>> A = [[0,0,0,0,0,1],[1,1,1,1,1,1],[0,0,0,0,1,0],[5,4,3,2,1,0],[0,0,0,2,0,0],[20,12,6,2,0,0]]
>>> T1 = [0,1,0,0,0,0]
>>> M1 = numpy.linalg.solve(A,T1)
>>> print(M1)
[  6. -15.  10.   0.   0.   0.]
>>> T2 = [0,1,0,1,0,0]
>>> M2 = numpy.linalg.solve(A,T2)
>>> print(M2)
array([ 3., -8.,  6.,  0.,  0.,  0.])
```

... and we can use this to produce a `Polynomial`:
```
>>> from numpy.polynomial import Polynomial
>>> print(Polynomial(M2[::-1]))
0.0 + 0.0·x + 0.0·x² + 6.0·x³ - 8.0·x⁴ + 3.0·x⁵
```

