---
date: '2023-02-05'
layout: article
title: 'Trying to unbind a specific event handler function from an event in Python Tkinter?'
summary: |
    Yeah, it unbinds everything, it's a bug.
tags:
    - python
    - tkinter
    - gui
---

This is a very specific bug in Python Tkinter, where attempting to unbind a 
specific event handler function from a Tkinter widget's event handler actually
unbinds all the event handler functions.

It's actually already documented, on the
[Old Python Bug Tracker #31485](https://bugs.python.org/issue31485) / 
[New Python Bug Tracker #75666](https://github.com/python/cpython/issues/75666)
and on the [Tkinter-Discuss Mailing List almost 10 years ago](https://mail.python.org/pipermail/tkinter-discuss/2012-May/003152.html) but it is still an issue in 
Python 3.11 and it took me a while to find so I'm documenting it here using 
the terms I first used to search for it.  Amusingly, posting about
[bugs which took ages to find](/art/wget-certificate-private-key/) 
was one of the reasons I started this blog.

# tkinter.Misc.unbind(self, sequence, funcid=None)

Anyway, the Python 3.11 code in `/usr/lib/python3.11/tkinter/__init__.py` reads:

```
    def unbind(self, sequence, funcid=None):
        """Unbind for this widget for event SEQUENCE  the
        function identified with FUNCID."""
        self.tk.call('bind', self._w, sequence, '')
        if funcid:
            self.deletecommand(funcid)
```

Which, well, it definitely does unbind the function identified by `funcid` but
it also unbinds all the other functions too.  Which is pretty confusing if you
had multiple handlers listening for the same event.

The underlying implementation (in `_bind`) is pretty confusing, but suffice
to say your call to `bind` is somehow writing a little bit of Tcl/Tk code and
attaching that to the widget, and your call to `unbind` is clearing it out again.

## A fixed unbind

To delete a specific handler you have to work out where it is in the Tcl/Tk
code, and there's a few implementations in the issues linked above but here's mine
which uses a regular "now you've got two problems" expression to fix the bound
code:

```
def unbind(widget, seq, funcid):
    # widget.unbind(seq, funcid) doesn't actually work as documented. This is
    # my own take on the horrible hacks found at https://bugs.python.org/issue31485
    # and https://github.com/python/cpython/issues/75666 and
    # https://mail.python.org/pipermail/tkinter-discuss/2012-May/003152.html
    # Also quite horrible.  "I'm not proud, but I'm not tired either"

    widget.bind(seq, re.sub(
        r'^if {"\[' + funcid + '.*$', '', widget.bind(seq), flags=re.M
    ))
    widget.deletecommand(funcid)
```

... you could make this into a FixedUnbindMixin class I suppose, or make
like a Ruby programmer and monkey patch it until such time as a fix is
merged into tkinter.

Also note that if you call unbind without a `funcid` (or call bind without
`add=True` and that happens to write over an existing handler) that
previously registered command is never collected, which is maybe not great 
if you do it a lot.

Perhaps the reason this bug has lain dormant for so long is that it'd be
better to just bind events on a parent object instead?

