---
title: 'Jerkus Maximus: Simple Jerk-Limited Trajectories'
layout: draft
uses_mathjax: 3
---


![notes](img/notes.jpg)

## See also

* Ruckig [paper](https://arxiv.org/abs/2105.04830) /
[ruckig.com](https://ruckig.com)


Given an initial `$x_0$`, `$v_0$` and `$a_0$` and a constant jerk `$j$`,
we can calculate:

`$a_t = a_0 + jt$`
`$v_t = v_0 + a_0t + \frac{1}{2}jt^2$`
`$x_t = x_0 + v_0t + \frac{1}{2}a_0t^2 + \frac{1}{6}jt^3$`

[Jerk](https://en.wikipedia.org/wiki/Jerk_(physics)) and
[Snap, Crackle and Pop](https://en.wikipedia.org/wiki/Fourth,_fifth,_and_sixth_derivatives_of_position)

[Sigmoid function or S-curve](https://en.wikipedia.org/wiki/Sigmoid_function)

[Smoothstep](https://en.wikipedia.org/wiki/Smoothstep)

`$ S_6(x) = \begin{cases} 0, & if x <= 0 \\ 924x^{13} - 6006x^{12} + 16380x^{11} - 24024x^{10} + 20020x^9 - 9009x^8, & if 0 <= x <= 1 \\ 1, & if x >= 1 \end{cases} $`


