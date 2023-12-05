---
category: Languages
date: '2010-06-01'
layout: article
tags:
    - languages
title: Fibonacci Regex Perversity
summary: Repeated substitutions are Turing Complete
---

Repeated Substitutions
======================

Consider these two regex substitutions:

    s/fi?b/i/
    s/fii(i*)b/f$1bfi$1b/

(For those unfamiliar with [Perlish
regexes](http://en.wikipedia.org/wiki/PCRE): that first one says
“replace the string `fb` or `fib` with the string `i`”. The second one
says “replace a string `fiiXb` with `fXbfiXb`, where X is zero or more
`i` s.”)

We can repeatedly apply these rules to a string until the string stops
changing. So for example, our string might mutate as follows:

    fiiiiib
    fiiibfiiiib
    fibfiibfiibfiiib
    ifiibfiibfiiib
    ifbfibfbfibfibfiib
    iiiiiifbfib
    iiiiiiii

Expanding the path of `fiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiib` is left as an
exercise to the reader, although this perl script might help:

    #!/usr/bin/perl -w

    $_ = "fiiiiib";
    print "$_\n";

    print "$_\n" while s/fi?b/i/g || s/fii(i*)b/f$1bfi$1b/g;    

What on earth is this all this substituion doing? Well, it is
calculating [Fibonacci
numbers](http://en.wikipedia.org/wiki/Fibonacci_number) of course!

Thinking In Unary
-----------------

Regexes don’t handle arithmetic well, so we represent numbers in
[unary](http://en.wikipedia.org/wiki/Unary_numeral_system) ... a string
of n `i` s represents the number n. When dealing with unary, you can add
numbers by simply appending them. `f` and `b` are like parens around the
number we’re calculating the Fibonacci number of. So `iiiii` represents
the number 5, and `fiiiiib` represents the fifth Fibonacci number, aka
fib(5).

So the sequence of strings above could also be written:

    fib(5)
    fib(3)+fib(4)
    fib(1)+fib(2)+fib(2)+fib(3)
    1+fib(0)+fib(1)+fib(0)+fib(1)+fib(1)+fib(2)
    6+fib(0)+fib(1)
    8

So really, any language that allows a sufficiently powerful regex
mechanism is [able to calculate Fibonacci
numbers](http://blog.progopedia.com/2010/may/30/10-unnatural-ways-calculate-fibonacci-numbers/),
albeit using [the worst algorithm in the
world](http://bosker.wordpress.com/2011/04/29/the-worst-algorithm-in-the-world/).

Turing Machines
---------------

And it is pretty easy to see how to implement a [Turing
machine](http://en.wikipedia.org/wiki/Turing_machine) by representing
each state transition as a regex substitution. For example, we can
represent the "tape" as a string of `0s` and `1s`, and the "head" as a
symbol inserted just before the "current" symbol. The tape can be
extended indefinitely by matching the end of the string as if it were a
blank symbol.

Taking the [Copy
Subroutine](http://en.wikipedia.org/wiki/Turing_machine_examples#A_copy_subroutine)
as an example, using `0` and `1` for the tape symbols 0 and 1, and using
`A` through `E` to represent the head in states s~0~ through s~5~, and
`H` for the head when halted. Translating to that notation, the state
transitions are:

Current State | Current Symbol | New Symbol | Move Head | New State
:---:|:---:|:---:|:---:|:---:
A | 0 |   |   | H
A | 1 | 0 | R | B
B | 0 | 0 | R | C
B | 1 | 1 | R | B
C | 0 | 1 | L | D
C | 1 | 1 | R | C
D | 0 | 0 | L | E
D | 1 | 1 | L | D
E | 0 | 1 | R | A
E | 1 | 1 | L | E

We can cope with the unbound tape by either matching `$` (end-of-string)
as if it were a `0`, or by simply extending the tape any time the head
is at the very end of it, eg:

    s/([A-Z])$/${1}0/

And the rest of the state transitions become simple string
substitutions. To move the head right, simply swap it with the symbol
you've just written. To move it left, put it behind the preceding
symbol:

    s/A0/H0/
    s/A1/0B/
    s/B0/0C/
    s/B1/1B/
    s/0C0/D01/
    s/1C0/D11/
    s/C1/1C/
    s/0D0/E00/ 
    s/1D1/D11/
    s/E0/1A/
    s/0E1/E01
    s/1E1/E11

We can write this into a Perl script too:

    #!/usr/bin/perl -w

    # Initial state of the tape.
    $_ = "A1111";
    print "$_\n";

    # Look out for the halting state
    while (! /H/) {

        # If we're at the end of the tape, extend it.
        s/([A-Z])$/${1}0/;

        # Do exactly one substitution.
        s/A0/H0/   ||
        s/A1/0B/   ||
        s/B0/0C/   ||
        s/B1/1B/   ||
        s/0C0/D01/ ||
        s/1C0/D11/ ||
        s/C1/1C/   ||
        s/0D0/E00/ ||
        s/1D0/E10/ ||
        s/0D1/D01/ ||
        s/1D1/D11/ ||
        s/E0/1A/   ||
        s/0E1/E01/ ||
        s/1E1/E11/ ;
    
        print "$_\n";
    }

and when we run it we can watch the turing machine at work:

    A111
    0B11
    01B1
    011B
    0110C
    011D01
    01E101
    0E1101
    E01101
    1A1101
    10B101
    101B01
    1010C1
    10101C
    1010D11
    101D011
    10E1011
    1E01011
    11A1011
    110B011
    1100C11
    11001C1
    110011C
    11001D11
    1100D111
    110D0111
    11E00111
    111A0111
    111H0111

so these languages are bound to be [Turing
Complete](http://en.wikipedia.org/wiki/Turing_complete) as well, even if
they do turn out to be [Turing
Tarpits](http://en.wikipedia.org/wiki/Esoteric_programming_language#Turing_tarpit).

A Farewall To Unary
-------------------

Unary arithmetic is tedious and inefficient. Fortunately, Perl Regexs
also offer an "expression" mode, which lets us do away with unary and
instead write some "advanced" rules which handle decimal arithmetic:

    s/(\d+)\+(\d+)/$1+$2/eg;
    s/(\d+)-(\d+)/$1-$2/eg;

Now, this is kind of cheating: those aren't really regular expression
substitutions at all! If we're going to allow the `s///e` form, we're
really allowing anything at all, since you could just do
`s/(.*)/artibrary_function($1)/`. In fact, we can even go a bit silly
and say that if it looks like an arithmetic expression it is Perl's
problem:

    s/(\d+([-+*\/]\d+)+)/eval($1)/eg

But the point is, once we've defined some basic arithmetic in these
terms, we can define the rest of our fib function in such a way as to
use these:

    s/fib\([01]\)/1/g;
    s/fib\((\d+)\)/fib($1-1)+fib($1-2)/g;

We can run this set of expressions just like before:

    fib(5)
    fib(5-1)+fib(5-2)
    fib(4)+fib(3)
    fib(4-1)+fib(4-2)+fib(3-1)+fib(3-2)
    fib(3)+fib(2)+fib(2)+fib(1)
    fib(3)+fib(2)+fib(2)+1
    fib(3-1)+fib(3-2)+fib(2-1)+fib(2-2)+fib(2-1)+fib(2-2)+1
    fib(2)+fib(1)+fib(1)+fib(0)+fib(1)+fib(0)+1
    fib(2)+1+1+1+1+1+1
    fib(2)+6
    fib(2-1)+fib(2-2)+6
    fib(1)+fib(0)+6
    1+1+6
    8

What's The Point Of All This?
=============================

I’m quite interested in substitution as a kind of pure functional
programming. This article is slowly expanding in that direction ... More
later.
