---
title: 'WASTE: Web Abstract Syntax Tree Editor'
date: '2018-03-12'
layout: article
summary: 'Editing an AST in the browser'
tags:
  - languages
  - www
  - python
---

I'm interested in the idea of [Programming beyond Text Files](/art/programming-beyond-text-files/) and
I've been playing around with this using HTML5 and [Ractive](https://ractive.js.org/).

I'm trying to make a fairly generic editor which can be adapted to many grammars, including
JSON, Markdown and Python.  Why in the browser?  Well, I recently switched across to 
[Fastmail](https://fastmail.com/) who really are proof that a browser based client can be 
just as good as a native one, and developing in the browser environment means that the 
app is cross platform from day one.

I'm calling it "WASTE": Web Abstract Syntax Tree Editor.

* [repo](https://github.com/nickzoic/waste/)
* [demo](https://nickzoic.github.io/waste/waste.html)

I think this idea applies especially well to [MicroPython and WebUSB](/art/micropython-webusb/) ...
the device can serve up its own IDE.

## Details

When a program text file is opened, it is parsed into a tree of objects by a PEG parser.
(This may be a problem for Python: [peg.js](https://pegjs.org/) doesn't support
pythonesque punctuation -- however [chevrotain](https://github.com/SAP/chevrotain) apparently
does, so maybe that's a better way to go)

Anyway, each AST node is a Javascript object with a "type" and a "value".  
For JSON, `true` is represented by `{ 'type': 'atom', 'value': 'true' }`
and `{ "foo": 23, "bar": "baz" }` by

```
{ 'type': 'object', 'value': [
   [ { "type": "string", "value": "foo" }, { "type": "number": "value": "23" } ],
   [ { "type": "string", "value": "bar" }, { "type": "string": "value": "baz" } ]
] }
```

This is a lot wordier than native JSON representatio, but lets us iterate over
key/value pairs and represent values exactly as they are in the JSON, for example.

This is then translated to HTML via a Ractive template which uses recursion
(`{{>thing}}`) to traverse the structure and convert it to HTML.  Ractive also
carries changes and events back from the HTML to the underlying AST.

To save the file, we serialize it back ... or maybe compile it directly!

## Bindings

The trickiest thing with the editor has got to be coming up with a mapping of keyboard
and mouse operations to tree transformations.  Subtrees can be dragged and dropped into 
place on the tree, and maintaining the typical mappings for Ctrl-Z,X,C,V make sense
to make it easy for users.  Other keys not typically used in syntax are Escape, Enter,
Home, End, PgUp PgDn, Insert, Delete and the up/down arrow keys.  What keys do depends
somewhat on context too: the aim is to have as few extraneous keystrokes as possible.

Up | Previous Sibling
Down | Next Sibling
Escape | Parent
Enter | Depends on contact: First Child / Next Sibling / Next-Sib-Of-Parent
Delete | Delete current node

## Editing Python

For typing a language like Python, the syntax can follow your typing, to automatically
parse code as you type, much like a Pratt parser.  To keep the syntax tree valid while
editing code, ephemeral `pass` / `None` / `0` nodes can be temporarily inserted.

    i

With just one character, we can't tell much, it could be an identifier so we'll make it
an identifier.

    if

... whereas `if` is a keyword so it can't be an identifier. We can see this, turn it into
a conditional element with an empty condition and action

    if None:
        pass

... and then select the condition so it is overwritten as you type:

    if a:
        pass

... keep typing and you keep entering stuff for the condition:

    if a == b:
        pass

... hit tab to move to the action, which since it is ephemeral (`pass` doesn't actually do 
anything, so you can always replace it).

    if a == b:
        print()

... we see the open paren and now we know that's a function invocation ... so now we're 
inserting arguments into the list of arguments.  Hit " and you're entering a string, which
will handle escaping and so on for you ...

    if a == b:
        print("hello")

Hit enter to pop out of the string into arguments list, and again to pop out of the
print to the next statement in the `if`, then again to pop out to after the `if`.
Now type `else:` ...

