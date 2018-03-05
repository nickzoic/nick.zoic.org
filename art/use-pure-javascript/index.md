---
category: HTML5
date: '2017-02-11'
layout: article
redirect_from: '/HTML5/use-pure-javascript/'
slug: 'use-pure-javascript'
tags:
    - html5
    - javascript
    - functional-programming
title: '"use pure"; in Javascript'
summary: 'a modest proposal for better javascript: like "use strict" but purer.'
---

## use strict

Perl's introduction of [the 'use strict' pragma](http://perldoc.perl.org/strict.html) was revolutionary, removing
a whole swathe of very easy "foot guns" from the language. It wasn't
long before every Perl script started:

    #!/usr/bin/perl -w
    use strict;

Forcing programmers to declare variables turned out to be a huge win
([who'd have thought?](https://en.wikipedia.org/wiki/ALGOL_68#mode:_Declarations))
and many errors which were hard to find previously were suddenly dragged
into the light of day.

Javascript started processing [a similar 'use strict' pragma](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode)
at JS 1.8.5 / ECMAScript 5, using a weird little piece of syntax which
appears to be an unevaluated string but is really a pragma:

    function foo() {
        "use strict";
        // be strict within the scope of this function
    }

It has similar effects on JS code as it did on Perl.

## ES6 and FP

Doing [Functional Programming in Javascript](../the-emperors-new-closure-functional-programming-in-javascript/)
can greatly improve the legibility and reliability of your code, and ES6
introduces all sorts of lovely syntax for to make your FP nicer. But
there's still a problem: enforcement.

In a [purely functional program](https://en.wikipedia.org/wiki/Purely_functional_programming)
you can be certain that the way functions interact is limited, as side
effects and side causes are not possible. So the order of evaluation no
longer matters, and functions can be memoized or eliminated or lazily
evaluated as the runtime sees fit.

If the language doesn't provide these constraints, then the runtime is
not able to make these optimizations.

## "use pure";

This post proposes a Use Pure Directive with similar rules to the
existing [Use Strict Directive](http://www.ecma-international.org/ecma-262/7.0/index.html#use-strict-directive)
... a small string at the start of a function scope which is really a
pragma.

    function foo() {
        "use pure";
        // this function is pure, and any functions declared within are limited
        // to its scope.
    }

This pragma would declare that within its scope all functions are pure
and can be optimized as such. Access to global or outer scope variables,
or any other kind of impure state, is forbidden and causes an error at
compile or run time.

As the "use pure" pragma only forbids behaviour rather than changing it,
any code which runs correctly in a JS runtime which understands it,
should also run correctly in a JS runtime which does not. Therefore it
is safe to use a pure-aware linter, cross-compiler, etc and still have
the unmodified code run properly in a non-pure-aware runtime.

## Pure Closures

I think you'd still be able to do closures within pure functions, so long as the 
containing functions are marked as pure:

    function new_accumulator() {
        "use pure";
        var acc = 0;
        return function() {
            acc += 1;
            return acc;
        }
    }

... but this might not stand up to closer scrutiny, I'm not sure yet ...

## UPDATE

Just noticed [pure functions in D](https://dlang.org/spec/function.html#pure-functions) ...

