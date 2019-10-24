---
date: '2018-02-09'
layout: article
slug: 'programming-beyond-text-files'
redirect_from: '/art/syntax-tree-editors/'
summary: 'Are programs really text files?'
tags:
  - languages
  - python
  - speculation
title: Programming Beyond Text Files
---

## Programs as Text Files

We're used to thinking of programs as text files: the first step on the road
to being a [Real Programmer](http://web.mit.edu/humor/Computers/real.programmers)
is pick a text editor "that reflects [your] personal style".  In old-school Unix 
that's probably `vi` or `emacs`, but even modern IDEs are really a tangle of
enhancements wrapped around a text editor.

<img src="img/dec-vt100.jpg" class="medium" alt="DEC VT100 Terminal"/>
*[DEC VT 100 terminal](https://en.wikipedia.org/wiki/VT100).
[Photo by Jason Scott - Flickr: IMG_9976, CC BY 2.0](https://commons.wikimedia.org/w/index.php?curid=29457452)*

And code style is a subject for endless debate.
[80-(ish)-column typewriters](https://en.wikipedia.org/wiki/Characters_per_line) led to 
[80-column punched cards](https://en.wikipedia.org/wiki/Punched_card#IBM_80-column_punched_card_format_and_character_codes)
led to [80-column terminals](https://en.wikipedia.org/wiki/VT100) and now 80 column
code is enshrined in everyone's coding standards.
Even [punctuation](https://en.wikipedia.org/wiki/Digraphs_and_trigraphs#C) and 
[whitespace](https://www.python.org/dev/peps/pep-0008/)
turn out to be fraught, and endless arguments ensue.

UPDATE:
* [Interesting article about the origin of punch card sizes](http://exple.tive.org/blarg/2019/10/23/80x25/)

<img src="img/margaret-hamilton-800px.jpg" class="narrow" alt="Margaret Hamilton"/>
*[Margaret Hamilton](https://en.wikipedia.org/wiki/Margaret_Hamilton_(scientist\))
pictured next to printouts of the Apollo mission software.
[Public Domain, retouched by Adam Cuerden](https://commons.wikimedia.org/wiki/File:Margaret_Hamilton_-_restoration.jpg)*

Back when monitors were small and computer time was expensive, we used to print out listings
so we could take our programs away to think about.  When did you last print out a program?

## Programming beyond Text

But that's not the only way to program:
[Scratchlikes](https://wiki.scratch.mit.edu/wiki/Alternatives_to_Scratch#Drag_and_Drop_Programming)
allow you to edit a syntax tree with drag-and-drop actions and some 
[Visual Languages](/art/flobot-graphical-dataflow-language-for-robots/)
may even do away with the syntax tree!  This can be great for avoiding getting bogged
down in typing and syntax, but they do place a lot of reliance on mousing,
annoying fluent typists.

Perhaps instead we could edit the AST directly, but in a keyboard oriented way.
 
Languages with very little syntax, like Lisp, are very well suited to writing such an 
editor.  JSON is only a little harder.  Python is not going to be all that easy.
The trick will be to balance keystroke driven operations with automatic tree operations,
so that you can type code naturally but then drag-and-drop subtrees as well.
The language grammar may need to be extended slightly to allow comments etc, but this
could be a good thing: if you're going to have a markup language for code documentation,
why not make it a first-class part of your code and subject to syntax checking along with
everything else?

I haven't used it in years, but [Oxygen XML](https://www.oxygenxml.com/) did a pretty good
job of this: once you specify a schema, XML documents are very tightly restricted in what
can possibly go where so the UI was able to guide you pretty effectively as I recall.

### UPDATE

I've been playing around with this using HTML5 and [Ractive](https://ractive.js.org/),
trying to make a fairly generic tree editor called 
["WASTE": Web Abstract Syntax Tree Editor](/art/waste-web-abstract-syntax-tree-editor/)

## Programming beyond files

The above assumes that you're going to work by parsing your code into your editor,
manipulating the AST and then (when you hit save) serializing the AST back out into
a form which can be parsed back into an AST by a compiler.  On the upside, that fits
in with your existing tools, but it also seems
[rather wasteful](/art/deserialize-alter-serialize-antipattern/)

Since the code is always in a syntactically valid form (it has to be, after all: it is 
being manipulated as an AST) it should be also possible to write an incremental compiler
which keeps your output code / bytecode up to date as you edit your source code.  I'm a
big fan of
[Software Development at 1Hz](https://hackernoon.com/software-development-at-1-hz-5530bb58fc0e),
why not take that to the next level and have your tests constantly rerunning themselves
whenever you touch code which they depend on?

One of the arguments against doing this is that we have so many good tools for dealing
with plain text files, but I think we
could make even smarter tools with a better underlying data structure.  The Lisp
world uses [homoiconicity](https://en.wikipedia.org/wiki/Homoiconicity) to its 
advantage: treating programs as data and data as programs is easy when your programs
are just data structures.

Perhaps this is taking it all a little too far, but I love the idea of the whole 
filesystem being replaced by an append-only tree of nodes, treated homogeneously all the way
from the root of the filesystem to the individual atom of a parsed program.  We'd
[lose a lot of our old friends](/art/a-canticle-for-diff3/)
like `find` and `grep` and `diff3`, but think of what we'd gain ...

### UPDATE (again)

Another interesting reference: the [New York Times' Oak Editor](https://open.nytimes.com/building-a-text-editor-for-a-digital-first-newsroom-f1cb8367fc21) which is kind of similar.

And another visual language: [Prograph](https://medium.com/@noelrap/prograph-c3caa90b89e8)
