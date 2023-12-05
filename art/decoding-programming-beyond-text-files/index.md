---
date: '2020-09-05'
layout: article
summary: '"Decoding: Programming beyond text files" at PyCOnline AU 2020'
tags:
  - languages
  - python
  - speculation
title: 'DECODING: Programming Beyond Text Files'
---

This is an approximate transcription for my talk
[Decoding: Programming beyond text files](https://2020.pycon.org.au/program/lyrjgy/)
at [PyCOnline AU 2020](https://2020.pycon.org.au/).
I'll fix the transcription up and add some slides in
once I can bear to hear myself speak ever again.

The video is up on youtube: [Decoding: Programming Beyond Text Files (PyConAU 2020)](https://youtu.be/Ay6iM_I9694)


*The talk is based on the article
[Programming Beyond Text Files](/art/programming-beyond-text-files/).*

*I've also written a bit about the experience of 
[making the video](/art/decoding-the-making-of/) ...
it's the first time I've tried recording a talk and I learned a lot
(starting from almost complete ignorance)*

*Also see [Katie Bell's "Text files full of punctuation? There must be a better way to code."](https://2020.pycon.org.au/program/hhpfhw/)*

*Also also I should credit [Lilly Ryan's "Don't Look Back in Anger: Wildman 
Whitehouse and the Great Failure of 1858"](https://www.youtube.com/watch?v=GuNoaAFnTPg)
for inspiration to look into the history of some of this stuff*

# DECODING: Programming Beyond Text Files

        Most systems supply several text editors
        to select from, and the Real Programmer
        must be careful to pick one that reflects
        his personal style.
        -- "Real Programmers Don't Use PASCAL", Ed Post, 1983

We're used to thinking of programs as text files:
according to computing folklore the first step on
the road to being a Real Programmer is to pick a
text editor "that reflects [your] personal style".

We choose our favourite text editor, argue
passionately about code formatting standards
and feel guilty when our diffs are ugly.
But what if these things are just a
vestigial hangover
from computing's earliest evolution?

        Things are like they are because they got that way.
        -- Gerald Weinberg, _The Secrets of Consulting_, 1985.

As Gerald Weinberg says,
“Things are like they are because they got that way”.

Complex systems don’t just ‘happen’, they evolve, through a series of decisions each of which seemed like a good idea at the time.

A lot of the things we take for granted in programming come from these early decisions. It’s easy to assume that they’re purposeful, even immutable. In this talk I’ll discuss some alternatives, and where they could perhaps lead.

But first, some computing history:

## Punched Tape / Serial Communications

This story begins in the mid 19th Century, when the first
"printing telegraphs" transformed telegraphy from using Morse Code,
to using a typewriter-like keyboard and mechanical printer.

Using Morse code required an operator to tap out a difficult
encoding of dots and dashes, and to receive messages by translating
those audible signals back into letters.
By switching to an automatic encoder, messages could be sent
with less training, and having messages print on paper allowed
records to be kept.

Over the next hundred years or so this technology
developed into the "Teleprinter", a device which
allowed an operator to type a message on a standard
typewriter keyboard and have it printed instantly on the
other side of the world.

Various standards evolved to encode characters, but 
eventually, most devices settled on ASCII as a 
data interchange format. ASCII defines 7 bit characters,
with 32 "control" characters used to do things like
advance the printer paper or ring a bell.
If you've ever wondered why your Linux terminal
thinks it is a typewriter,or misbehaves when you "cat"
a binary, this is why.

Links:

* [Wikipedia: Teleprinter](https://en.wikipedia.org/wiki/Teleprinter)
* [Wikipedia: Wheatstone System](https://en.wikipedia.org/wiki/Wheatstone_system)
* [Wikipedia: Punched Tape](https://en.wikipedia.org/wiki/Punched_tape)

## Punched Cards / Line-Oriented Text

During the same period, Punched Cards were also being
developed as a storage medium.
Punched Cards were used for machine control, music, information storage
and collation.

A whole industry sprang up to support the use of cards for indexing and 
collation. Methods for sorting and searching notched cards using long 
needles were standardized. Very early computers were developed to process
cards by counting and accumulating values punched into them.
The information age had begun.

There were many standards developed for machine-readable punched cards,
with different dimensions and numbers of holes, but 
the IBM 80 column card introduced in 1928 became 
the most common standard for punched cards. Millions of these cards were produced.
The 80 column IBM card led naturally to the 80 column IBM video terminal:
each terminal row could display the contents of a single punched card.

Links:

* [Wikipedia: Punched Card](https://en.wikipedia.org/wiki/Punched_card)
* [Interesting article about the origin of punch card sizes](http://exple.tive.org/blarg/2019/10/23/80x25/)
* [Ken Shirriff on the history of the 80x24 display](http://www.righto.com/2019/11/ibm-sonic-delay-lines-and-history-of.html)

## Early Computers

Early languages like FORTRAN began in this era.
They are very line oriented: each statement is a single line,
suitable for punching onto a single card.

Punched Cards themselves can't easily be edited.
But programs can be corrected and rearranged
a line at a time, by inserting, removing and
replacing cards from the deck.

Sections of code can be gathered into modules,
held with rubber bands, and these modules can be
copied, shared between programs and stored on 
shelves: literal libraries of code.

Links:

* [ASCII](https://en.wikipedia.org/wiki/ASCII)

## Compilation to Punched Tape

When the program is ready to be run, the cards are fed
to another program, the 'compiler'.
This 'compiles' them into a long strip of punched tape.
Punched tape is very much denser than punch cards, with
binary representation and no extraneous whitespace.
But it is much harder for humans to read and manipulate.

And this split between the continuous and the line-oriented
has continued to this day, with files divided into:

* Easily manipulated, line oriented text files like decks of
  punched cards, and
* Compact but difficult to edit binary files like punched tapes.

## Printing Code

While punched cards often had their contents typed
along the top edge, actually reading code in this way
was not very convenient. So people tended to print out
their programs for analysis.

Pictured here is MIT computer scientist Margaret Hamilton,
with the listings of the Apollo mission 
lunar module software developed by her team.

Printing code continued on into the 90s.
When I first started my Computer Science
degree, most of us accessed the shared Unix computers through 
80-column VT220 terminals, and it was pretty usual to 
print your code out on the enormous dot-matrix printers
so you could read it while debugging your code on
the limited space of the 80x25 monitor.

## Structured Data

Line-oriented files are somewhat of a universal standard.
Minor quibbles about the interpretation of line feeds aside,
pretty much all systems can read and edit ASCII line-oriented text.
But beyond that, there's not much agreement on how files are
structured.

There have been many attempts to make a universal format for
structured data, beginning with the ASCII standard itself.
ASCII contains four control characters: FS GS RS and US
which provide four levels of record structure.
But because they are difficult to enter in a regular text editor
they've been largely ignored.

The most widespread structured data format is "Comma Separated
Values", or CSV. This format is not particularly well standardized
and is extremely limited in what it can express.
But its compatibility with text-oriented tools makes it a natural
bridge between the structured and the unstructured.

More recently, complex structured formats like XML and JSON have
attempted to build a better bridge.
They're editable in a text editor but still parseable by the computer.
But these formats are caught between being a good binary
standard and a good text standard.
They are at once defined by their standards as recursively parsable
structured data and by convention as line-oriented text.

## Structured Code

Programming languages have a similar problem.

C is nominally whitespace-agnostic: you can write a C program
all on one line if you are not afraid of your co-workers.
C is parsed according to a well-defined context free grammar.
There's no need to worry about lines.
Well, except for the minor issue of C preprocessor directives,
which are line oriented, and the use of line numbers in compiler
error messages. 

Python went with the bold decision to have significant whitespace.
A statement belongs on a line, and whitespace alignment actually matters.
Well, a lot of the time. In practice, expressions can span multiple
lines and generators and lambdas allow you to pack a lot into a single
line.

Writing either of these languages means keeping the compiler's
grammar and the human reader's expectations in sync.
Some languages have a pretty well defined
"right" way to lay out code in text, and a tool to enforce this:
Python's 'black' and Go's 'gofmt', for example.
You can edit your code and then pass it through the appropriate
tool to make sure your formatting agrees exactly with the rest
of the team.

But you still have to understand both worlds.

Links:

* [History of C](http://www.jslint.com/chistory.htm)

## Homoiconicity

The programming language LISP is famously "homoiconic", meaning
"same representation". 
LISP programs manipulate data structures called 'S-Expressions', and 
LISP programs are themselves S-Expressions.
It is natural for LISP programs to manipulate other LISP programs.

On the other hand the C standard library only has really good support
for line-oriented reads, and that's what ends up baked into most other
programming languages.

So if you're writing a program which reads files, it's easier to write it
in a line-oriented way, even if it is a program for manipulating source.
This is why the C preprocessor, and revision control systems, are all 
line-oriented: it's the easiest way to it.

Most syntax is not line-oriented, in fact in many languages you can
write perfectly valid programs all on one very long line
(if you are not afraid of your colleagues)
So why are we still writing in text files?

In short, we write line-oriented code, because
the code we already wrote is good at reading
and writing line-oriented files.
Our languages aren't homoiconic, but if we're careful with how we format
our code we can pretend they are.

## Working With Structure

        Making things easy is hard.
        -- Ted Nelson

## Structured Editing

Python doesn't execute your Python source directly.  Instead, it
first parses it into an intermediate format: the Abstract Syntax
Tree (or AST).  This is a convenient way to arrange the code in 
memory before compiling to Python Byte Code.

Katie Bell talked in more detail about the AST earlier today,
but just to summarize: the AST is a tree of nodes, each of which
represents some part of the program: an "if statement", or a block
of statements, part of an expression, or a single identifier
for example.  They're arranged in a tree, representing the non-linear
structure of your program. You can peek under the hood of the AST
compilation process using the 'ast' module.

When we compile code, the compiler has to parse it into an AST.
While we're editing code, most editors do some kind of parsing just
for syntax highlighting.  Then they write it out to disk as 
line-oriented text, and the compiler has to parse it again,
if it can.

Writing code which doesn't compile is kind of useless ...
so why not just edit the AST directly?
An editor which worked directly on AST nodes would never allow
you to write syntactically incorrect code, by definition.
Syntax highlighting would become trivial. 
You could display the code in whatever way
suits you: fonts, line lengths, indentation sizes are all just
a "stylesheet" over the AST.
And it's easy to convert the AST to Python source,
or a tree-like format such as JSON.

The development environment could also compile directly to
Python Byte Code, and could even keep track of changes and
update byte code in place on running code.

I'm a huge fan of rapid development cycles.
Waiting to see updates is a distraction and a drag.
Imagine a development environment smart enough to keep track
of the bytecodes you'd changed and re-run only the tests which
executed those bytecodes.

## Revision Control

Okay, so, it'd be *relatively* easy to replace the text editor
with something AST oriented.
A bigger issue for the adoption of non-line-oriented
files is revision control.

To allow multiple programmers to work on the same
file concurrently, revision control systems must
*merge* changes. 

First a common ancestor is identified, and then
the changes made by each programmer are extracted.
Each file is compared to its ancestor line by line,
looking for parts which have been added, removed
or modified.

Then the two sets of changes are combined.
Combining changes is one of those things which sounds
easy but is remarkably complicated to actually
come up with an algorithm for.

The standard 'diff' and 'merge' tools are line-oriented,
they coordinate the addition and removal of lines of text.
They have no understanding of the deeper syntax or semantics
of the file, and only really work on text files with
many line breaks.  Reformatting or shuffling parts around 
leads to very large change sets, which rarely merge without
conflict.

Conflicts arise when multiple changes occur to the same 
section of the code, and the merge tool cannot determine which
outcome should take precedence. Generally these conflicts are
marked to warn the programmer that they will have to take 
manual action to resolve them.

This also means that the output of a merge of two valid
programs is not necessarily a valid, parseable program. 
This is problematic for our structured editor, which has
no idea how to handle a syntactically invalid program.

## Example: clean structure merge

However, a 'merge' utility which *does* understand the
syntax tree of the programming language can avoid these issues.

What ever the language: JSON or XML; C or Python, we can
exploit the structure of the syntax tree to compare and
merge syntax tree nodes instead of lines.

Instead of just looking for the insertion, deletion and
modification of *lines*, our change operations become about
sections of trees, which can be also be *moved*. This is 
a godsend for anyone who's ever felt guilty for making a 
large, conflicting conflicting by changing the indentation
of a block.

Additionally, a structured merge can guarantee that the 
result of the merge will always be syntactically valid,
thus can always be loadable by a structured editor. 
Conflicts will still occur, but they can be marked in a
syntactically appropriate way.

Instead of just looking for the insertion, deletion and modification of *lines*, our change operations become about sub-trees.

Common sub-trees can be identified, and list-like structures such as blocks can be merged. Changes where a sub-tree is moved can be identified and treated as a move rather than a delete and insert.
This would be a godsend for anyone who's ever felt guilty for making a large, conflicting change by altering the indentation of a block.

There are some difficulties:

1. for a start, the Python AST doesn’t encode comments, which some people may feel are kind of important. They’d have to be added in to the tree somehow.

2. The merge tool would have to work out how to represent conflicts while fulfilling its promise to always emit valid code.
When two developers make overlapping changes, a conflict occurs. which needs a human to resolve it.  In conventional merges, this is marked with some special lines:

The merge program doesn’t even bother to make these look like program code: after all, the program syntax is almost certainly broken anyway.

A structured merge has to emit parseable code, so conflict markers have to be inserted as a syntax tree node, such as a comment, and other parts of the tree may have to be patched up to maintain the correct structure.

3. The exact rules for how to merge tree structures are not easy to define. How far can a sub-tree move before we treat it as a new sub-tree? If one programmer changes the contents of a sub-tree, and another programmer duplicates the sub-tree, should the changes be inserted twice?

But as the saying goes: “we do these things not because they are easy, but because we thought they were going to be easy”.

If try to merge these change sets with a conventional merge:

```
- if condition_0:
+ if condition_1:
      block
      contents
```

```
- if condition_0:
+ if condition_2:
+     additional
      block
      contents
```

We might end up with a conflict like this:

```
<<<<<<< HEAD
if condition_1:
    block
=======
if condition_2:
    additional
>>>>>>> branch
    block
    contents
```

But with a structural merge, which understands
what a block actually is, we might end up with:

```
# CONFLICT HEAD
if condition1:
    block
    contents
# CONFLICT branch
if condition2:
    additional
    block
    contents
# CONFLICT END
```

Which while it probably doesn't do what you want 
is at least valid, parseable Python.


## Future 

        Because things are the way they are,
        things will not stay the way they are.
        -- Bertolt Brecht

## Ted Nelson's Hypertext

I've talked about history a lot to try and explain where
a lot of the assumptions we make about code come from.
But not every historical system is founded on those same
assumptions.

Way back in the 60s, Ted Nelson coined the term "hypertext" as follows:

        Let me introduce the word 'hypertext'
        to mean a body of written or pictorial
        material interconnected in such a
        complex way that it could not conveniently
        be presented or represented on paper.
        -- Ted Nelson 

Modern computer systems are definitely interconnected and
complex and cannot be conveniently represented on paper.
So presenting them as a printable,
linear, 80 column document is a little strange.

To come at this from another perspective:
here's a rectangle, representing the 800x500
pixel resolution of the VT220 80 column display.
Here's a somewhat larger rectangle representing
a modern 4K monitor.
We have a lot more room to move these days.
There's even colour!

## Visual Environments

We can even consider using *graphics*.
Freed from worrying about our programs as text, we
can present them and work with them in a way which is more interesting.

Visual programming has been quite popular in education.
The 1982 program "Rocky's Boots" was an educational game which
taught boolean logic through a graphical schematic-like interface.
Truly an amazing piece of software for its time.

"Scratch", and a number of "Scratchlike" imitators,
move the main input mechanism of programming from typing to 
drag-and-drop. Colourful blocks can only be assembled in
syntactically valid combinations. Despite its apparent
simplicity surprisingly complex programs can be written.

Other environments such as "Labview" and "Code Red"
allow programming by dragging connections betwen nodes,
modelling the flow of signals and data.

These are *data flow* languages, where the order of code
execution is completely unrelated to the way components
are arranged on the page. It therefore makes a lot of 
sense that their presentation is mobile, 2 dimensional,
non-linear.

Spreadsheets are another example of a data flow language.
Formulae aren't evaluated based on their position on the sheet,
but rather by their position within a directed acyclic graph
of cells.  While spreadsheets may not be a programmer's idea
of a programming language, they are one of the most accessible
and widespread forms of programming.

These sorts of languages have been held back by a lack of
tooling: it's hard to get work done effectively
in a language without
the ability to merge and track changes efficiently.

But the same is true of more conventional languages.
In Javascript, for example, function definitions are
"hoisted" to the top of their enclosing scope, so for
example you can define co-recursive functions:

```
// O(N^ly joking)

function is_even(n) {
    return n==0 || is_odd(n-1);
}

function is_odd(n) {
    return is_even(n-1);
}
```

These two functions are not really defined in any particular
order, it is irrelevant which comes first. They could be
swapped without consequence.  The same is true, much of the
time, for Python classes and methods: they refer to each other,
but the order of their declaration is unimportant.

Javascript is also famous for its “callback hell” of functions which
pass pointers to other functions.
This is a close match to the underlying event model, which reflects
the reality of network programming.
But it can make reading the code rather bewildering.

One solution to this is to use “promises” to hide the essential callback
structure of the code.

Another solution might be to work out a more readable way to represent
this essential structure. Don’t change the event model, change the view.

## Flobot

Inspired by these examples, I developed "Flobot",
a visual flow based language for controlling
robotic toys.
The robot's behaviour can be adjusted by
dragging connections between sensors, functions
and actuators.
Changes to connections are reflected in immediate
changes to the robot's behaviour.

Invalid connections, like connecting an output
to another output, are simply not permitted.
I found that this was a great advantage in that there
are no "wrong" Flobot programs, only surprising ones.

The Flobot programs are compiled to Python, which is then
executed by MicroPython embedded on the robot.

Flobot is effectively a visual editor for a subset of Python.
With a little more work, code can be ‘flipped’ between the visual
data-flow representation and the native Python representation.
Not all Python syntax makes sense in the visual metaphor of Flobot,
so those parts could be rendered as ‘black box’ functions.
But the general shape of the code – the flow of events from sensors
to actuators – would exist in both representations.

This idea, of code having multiple representations simultaneously,
is particularly interesting. Different representations might prove more
effective for different people or different tasks.
Perhaps it will prove useful to change your own perspective from time
to time, just to ‘unstick’ your thinking.

## Programming Beyond Files

Perhaps this is taking it all a little
too far, but I love the idea of the whole
filesystem being replaced by an tree
of nodes, treated homogeneously all the way
from the root of the filesystem to the
individual atom of a parsed program.
Perhaps this would be an append-only 
structure, or some kind of conflict-free
replicated data type (CRDT).

We’d lose a lot of our old friends like
find and grep and diff3, but we could replace
them, and think about what we'd gain ...

## Further Work

Our systems are often spread across multiple platforms
and multiple languages, often multiple continents.
Code isn't just code: there's requirements, issues,
discussion, tests, APIs, logs ... all scattered among
disparate, incompatible systems.

To solve a problem we have to jump between issues and
lines numbers, log messages and version ids.
Imagine, for a moment, navigating through all those 
resources seamlessly, connecting and correcting as you go.
All spread across the several million pixels in front of you.

It sounds like science fiction.  What are we waiting for?

# IMAGE CREDITS

<li>Printing Telegraph: By Ambanmba (talk) - Own work, Public Domain, https://commons.wikimedia.org/w/index.php?curid=7904405</li>
<li>Teleprinter: By Jamie - Flickr: Telex machine TTY, CC BY 2.0, https://commons.wikimedia.org/w/index.php?curid=19282428</li>
<li>System 3 Punchcard: By ArnoldReinhold - http://en.wikipedia.org/wiki/File:System_3_punch_card.jpg, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=5970365</li>
<li>Fortran Punched Card: By Arnold Reinhold CC BY-SA 2.5, https://commons.wikimedia.org/w/index.php?curid=775153</li>
<li>IBM Video Terminal: By David L. Mills, PhD - http://www.eecis.udel.edu/~mills/gallery/gallery8.html, Public Domain, https://commons.wikimedia.org/w/index.php?curid=32890452</li>
<li>Punched Card Deck: By ArnoldReinhold - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=16041053</li>
<li>McBee Card Deck: Whole Earth Catalog https://nevalalee.wordpress.com/tag/the-whole-earth-catalog/</li>
<li>Lochkarte Computer: By Stahlkocher - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=1006474</li>
<li>Margaret Hamilton: By Draper Laboratory; restored by Adam Cuerden. Public Domain, https://commons.wikimedia.org/w/index.php?curid=59655977</li>

## FONT

Based on "Print Char 21" by Rebecca Bettencourt / Kreative
... based on the font of the `APPLE ][`

