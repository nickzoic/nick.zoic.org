---
date: '2020-06-10'
layout: draft
tags:
    - backend
    - languages
    - speculation
    - maths
title: 'Unconventional Numerics - Probabilities'
summary: "How to deal with probabilities"
---

# Storing Probabilities

Probabilities have an interesting property: they are bounded in the range `[0,1]`.
There's a limited number of operations which it is sensible to do on probabilities, 
and those all maintain this boundary.  For example, you can find the inverse of a 
property by subtracting it from 1:  

```
P(not A) = 1 - P(A)
```

Or you can find the intersection of two probabilities by multiplying them:

```
P(A & B) = P(A) * P(B)
```

If you want to logically 'OR' two probabilities, you can't just add them up, 
as this might lead to a number > 1.  Instead, you invert, multiple and invert them:

```
P(A | B) = 1 - ( (1-P(A)) * (1-P(B)))
```

# Floats and Doubles

If you go around storing probabilities in floats, you've got some issues:

1. You're wasting the sign bit, which is always '0' (positive).
2. You're wasting the exponent bits, which are almost always '0'.
3. Floating point numbers behave differently near `0` and near `1`.
4. Combining probabilities always comes down to floating point multiplication.

# Fixed Point

You could simply store probabilities as a fixed-point number, so that each
value is in a set range.  For example, in a 16 bit float:

| Value | Probability |
|---|---|
| 0000 | 0.0000000000000000 |
| 0001 | 0.0000152590218967 |
| 0010 | 0.0002441443503471 |
| 7FFF | 0.4999923704890517 |
| 8000 | 0.5000076295109483 |
| A000 | 0.6250095368886854 |
| D0D0 | 0.8156862745098039 |
| FFFF | 1.0000000000000000 |

Inverting a probability is easy: subtract it from 0xFFFF.
You don't have the same problem as floats do, where 1/1000
Multiplying probabilities is fine too: calculate `A * B / 0xFFFF`
(or if you don't want to divide, calculate `(A * B + A + B) >> 16`)


