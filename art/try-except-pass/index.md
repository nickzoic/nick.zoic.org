---
category: etc
date: '2014-01-10'
layout: article
redirect_from: '/etc/try-except-pass/'
slug: 'try-except-pass'
summary: 'A short rant about a common beginner''s mistake in dynamic languages'
tags:
    - python
    - javascript
title: 'Try: Except: Pass'
---

Catching Exceptions
===================

A few times now I've seen this specific code crop up in dynamic language
code written by programmers who perhaps have more of a background in
less dynamic languages. There's a function which you want to call,
`do_something_amazing()`, but sometimes that function throws an
exception and in that case you're happy for the code to continue as if
the function were never run. So you write something like this:

    try:
        do_something_amazing()
    except:
        pass

This works fine, so you commit the patch and move on.

Unintended Consequences
=======================

Later, you or someone else is making a change to
`do_something_amazing()`, and you make a small error. Perhaps in one
particular corner case you overstep an array boundary. Or divide by
zero. Or misspell an identifier.

All of these things are runtime exceptions in Python ... `IndexError`,
`ZeroDivisionError` and `NameError` respectively. So they'll cause
`do_something_amazing()` to fail silently before it even gets started,
or even worse, fail silently after it has already succeeded!

And if they're in a branch, the problem won't turn up until that code
branch is actually taken! Not such a problem if you've got 100% test
coverage, but I've seen code with this problem in the field much more
often that I've seen code with 100% test coverage ...

In short:

-   Never catch an exception you don't know what to do with.
-   If you must catch it, make sure you can throw it back.
-   Make sure the scope of your `try:` is small enough that you're sure
    that you know what the exception is being caused by.

Javascript
==========

I've picked on Python here, but there's an equivalent mistake in
Javascript too:

    try { 
        do_something_amazing();
    } catch (e) {
        // do nothing
    }

... this is just as pernicious, and probably more commonly spotted.
