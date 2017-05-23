---
category: Python
date: '2011-05-01'
layout: article
redirect_from: '/Python/python-in-the-browser/'
slug: 'python-in-the-browser'
tags:
    - python
    - javascript
    - www
title: Python in the Browser
---

Netscape shipped [the first Javascript interpreter in
1995](http://en.wikipedia.org/wiki/Javascript) and its position in the
web browser has made it almost universal. But imagine, for the sake of
the argument, if Python had got there first.

The timing would have been close, with [Python 1.2 out in
1995](http://en.wikipedia.org/wiki/History_of_Python#Version_1.0) too.
And there's a lot of similarity between the languages: dynamic typing,
first-class functions, eval() (and somewhat bizarre treatment of
whitespace) ... it isn't hard to imagine a Python VM running in the
browser with access to a global "document" and "window" object.

Why Would This Be A Good Thing
==============================

I read a blog post recently by Ian Bicking which describes [running the
same language on client and server as "not a big
deal"](http://www.ianbicking.org/blog/2011/03/javascript-on-the-server-and-the-client-is-not-a-big-deal.html)
(admittedly, talking about Node.js, eg: JavaScript running on the
server). I don't tend to agree ...

The RPC Problem
---------------

Whenever two pieces of unconnected code communicate, the way they
communicate has to be agreed upon, and the two parts must stay in sync
or communication fails. One way to do this is to define a protocol
describing the communication between them. I'm fine with [writing
protocols](http://tools.ietf.org/html/rfc4429) but this generally just
means you now have three parts to keep in sync: the client
implementation, the server implementation and the code itself.
Machine-readable descriptions like XML Schema and WSDL attempt to fix
part of that problem ... but wouldn't it be nice to just declare this
stuff just as functions which call other functions?

``` {.sourceCode .python}
@runs_on_the_server
def get_user(username, password)
    return db.tables['user'].select(username=username, password=password)

@runs_on_the_client
def handle_login(form):
    user = get_user(form.username, form.password)
```

The python compiler can see that a function which runs\_on\_the\_client
is calling a function which runs\_on\_the\_server, and can go away and
create some kind of RPC interface for us without bothering us with the
details. There's an argument (see above) that this abstracts away all
the HTTP goodness, but that, to me, is the whole point.

One criticism of this is that you might get confused as to what code is
running where. For this reason, I think some very explicit mechanism
like the decorators shown above is necessary. Writing the server and
client code in different languages is not sufficient to enforce good
security in any case, as any fan of SQL injection can tell you ...

Validation
----------

It is pretty common that you want to validate a form field on the
frontend, to save a whole lot of round-trips, and also on the back-end,
because the frontend can't be trusted. This isn't hard to do if your
validation step is just a regexp -- and I've written code which depends
on exactly this -- but not all validation steps can be sanely expressed
as regular expressions. If you're going to have to write a validator
function, you should only have to write it once:

``` {.sourceCode .python}
@runs_on_both
def validate_number(n):
    return n % 13 != 0
```

"But how hard can it be to write \_that\_ twice", you say. But the point
is, if it is only written in one place then it can't get out of sync
between \_this\_ version of the client and \_this\_ version of the
server, resulting in either the server accepting something the client
shouldn't be allowed to send or the client sending the server something
it will only reject.

Progress
========

Assuming for the moment that this is a worthwhile goal, what progress
has been made towards it?

Not Python
----------

[Google Web Toolkit](http://code.google.com/webtoolkit/) is pretty well
established as a toolkit for compiling Java across to JavaScript.

[Node.js](http://nodejs.org/) is probably the closest anyone's getting
to mainstream acceptance of this idea, but you're stuck writing your
server code in JavaScript.

There's also the possibility of writing your own language which runs on
both platforms, for example:
[Links](http://lambda-the-ultimate.org/node/1441).
[CoffeeScript](http://coffeescript.org/) might also be
a possibility here,

I can't help thinking that one of the Lisp family would be a good
candidate too.

Python
------

But, sticking with Python:

-   Obviously, a Python VM plugin would be one possibility, but that
    would have to be supported for multiple browsers and no-one likes
    installing plugins anyway so getting any kind of traction would be
    near impossible.
-   Another bad idea would be implementing the Python VM in JavaScript.
    I'm pretty sure that writing an interpreter in an interpreted
    language is a mortal sin, even if JavaScript is mostly JITted these
    days anyway.
-   [Pyjamas](http://pyjs.org/) is more-or-less a GWT for Python, and
    allows you to write Python apps which can either run locally or by
    translating from Python's AST to JavaScript and using AJAX.
-   There are also [several projects called
    py2js](http://google.com/search?q=py2js) all of which seem to do AST
    to JavaScript conversion. I'm still trying to work out which of them
    are separate projects, and how they relate to Pyjamas' "pyjs" code.
-   And finally, before I noticed python's
    [inspect.getsource](http://docs.python.org/library/inspect.html#retrieving-source-code)
    I started work on a Python Bytecode to Javascript decompiler. It was
    actually working pretty well, and the idea of avoiding another
    load-and-compile-to-AST cycle still appeals.
-   Conceivably, a Python to JS converter could provide a "beachhead"
    for the use of a Python plugin ... or, indeed, for a total
    replacement of the browser!

Tropyc
======

I ended up writing a bytecode to JS converter, it is pretty sketchy but
I put it on github anyway: [Tropyc](https://github.com/nickzoic/tropyc).

I've come to terms with node.js in the meantime, partly because it has
gotten better and partly because my understanding of Javascript has
improved.
