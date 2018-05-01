---
date: '2018-02-28'
layout: draft
slug: 'afunctional-programming-languages'
summary: 'What if there were no functions?'
tags:
  - languages
  - functional-programming
title: Afunctional Programming Languages
---

## What?

Many, many years ago, maybe around 2000, I was waffling on about something or another
about Functional Programming to someone and forgot the word for, uh, the other thing.
Disfunctional Programming?  Unfunctional?  Afunctional?  Oh, yeah, Imperative.  That's it.
Now, where was I?

Disfunctional Programming was a bit too easy to make jokes about, but for some reason
the word 'Afunctional' stuck in my head and I started wondering what it might possibly
mean.  Obviously, there are languages with no or very primitive functions, like
assembly langauges with [JSR](https://en.wikipedia.org/wiki/Subroutine#Jump_to_subroutine)
and BASIC's [GOSUB](https://en.wikipedia.org/wiki/GOSUB)
but they're not particularly interesting: you can force a functional paradigm onto them 
with a calling convention.

### Returning Control

So what is a "function" anyway?  The
[mathematical definition](https://en.wikipedia.org/wiki/Function_(mathematics\))
is about taking inputs and returning an output, but in programming something else
is returned: control.  When we call a function, we give it control and we expect
to get control back: we say "please work out the
[43rd Fibonacci Number](/art/fibonacci-regex-perversity/) and get back to me".
The function isn't just returning the answer to the caller, it is also waking the
caller back up.  Even "void functions" which return no (useful) value are returning
control.

### Asynchronicity

There's another way here, commonly called
[Asynchronous method invocation](https://en.wikipedia.org/wiki/Asynchronous_method_invocation)
where we don't actually pass control to the function being called, we just queue up
a request for it to be run and then get on with what we're doing.  The runtime will 
then schedule that method to be run and notify us when the result is ready.  This is 
a very common way of doing things in Javascript, where for example you can perform an
asynchronous web request like so:

    function get_example() {
        var xhr = new XMLHttpRequest();
        xhr.onload = function () {
            console.log(xhr.responseText); 
        }
        xhr.open("GET", "http://example.com/");
        xhr.send();
    }

Calling `xhr.open()` doesn't give up control for long: that method almost immediately
returns, and then our `get_example()` function finishes and returns too.
When ([much later in CPU terms](https://blog.codinghorror.com/the-infinite-space-between-words/))
the answer finally comes back from the Internet
it is put in our `xhr` object, and the anonymous function we supplied as
`xhr.onload` gets called to return control to us so we can do something,
in this case write some stuff to the console.

This way of programming is often derided as [Callback Hell](http://callbackhell.com/)
because each action leads to a callback which leads to another action which leads to a callback,
and so on, but by taking care we can avoid making our code too confusing.  If we wanted
`get_example` to do something *after* it got the example, we'd need to pass it a callback
to call once it was done.  And so on.

There are alternatives such as
[ES6 Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) and
[Python asyncio](https://docs.python.org/3/library/asyncio.html#module-asyncio) which 
attempt to address the problem.  With promises, we can write the same code above as:

    function get_example() {
        new Promise(function(resolve, reject) {
            var xhr = new XMLHttpRequest();
            xhr.onload = function() { resolve(xhr.responseText); }
            xhr.open("GET", "http://example.com/");
            xhr.send();
        }).then(
            function(text) { console.log(text); }
        )
    }

The syntax scales somewhat better, but it is still doing the same thing as before:
my anonymous function is getting called when it is ready.

# to be continued ...

### Parallel Programming

* probably should mention CSP / Actors in here at some point
* async vs sync loops - hassle of converting between them
* distinction between callbacks and messages?

## How?

* unix pipes
* C runtime

## Components

* Types - Sources, Transformers, Sinks
* Map, Reduce, etc

## Syntax

* Composition with `|` and `;` and `[ ]`
* Error redirection

