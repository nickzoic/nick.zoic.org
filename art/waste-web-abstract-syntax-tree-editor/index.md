---
date: '2018-03-12'
layout: article
slug: 'waste-web-abstract-syntax-tree-editor'
summary: 'Editing an ASTs in the browser'
tags:
  - languages
  - www
  - python
title: WASTE: Web Abstract Syntax Tree Editor
---

I've been playing around with this using HTML5 and [Ractive](https://ractive.js.org/),
trying to make a fairly generic tree editor called "WASTE": Web Abstract Syntax Tree Editor.

* [repo](https://github.com/nickzoic/waste/)
* [demo](https://nickzoic.github.io/waste/waste.html)

I think this idea applies especially well to [MicroPython](/art/micropython-webusb/) ...

## Details

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

