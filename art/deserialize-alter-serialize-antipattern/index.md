---
category: etc
date: '2015-11-12'
layout: article
redirect_from: '/etc/deserialize-alter-serialize-antipattern/'
slug: 'deserialize-alter-serialize-antipattern'
summary: |
    I was talking to $PERSON from $BIG_COMPANY the other day, and they
    happened to mention that around 80% of their CPU time was spent on
    serializing and deserializing data ...
tags:
    - architecture
    - systems
    - speculation
title: 'Deserialize / Alter / Serialize: an Antipattern?'
---

CPU Time
========

I was talking to \$PERSON from \$BIG\_COMPANY the other day, and they
happened to mention that around 80% of their CPU time was spent on
serializing and deserializing data. We're talking
[Protocol Buffers and C++ here](https://developers.google.com/protocol-buffers/docs/cpptutorial)
so it isn't the usual suspects.

Deserialize / Alter / Serialize
===============================

With anything web-related, once flushed from the cover of frameworks and
libraries, an enormous proportion of operations end up looking something
like:

{% highlight python %}
    def update_attribute(new_value):
        object = deserialize(input_stream)
        object.attribute = new_value
        output_stream.write(object.serialize())
{% endhighlight %}

... where the `input_stream` and `output_stream` are connections to a
database of some kind. The serialization and deserialization may be
hidden in the database bindings, or even in the core of the database
itself, but it's a general pattern.

The problem is that to improve efficiency, `object`'s class tends to
grow to encapsulate more and more information. Anything not in there has
to be fetched separately, after all, so it is natural to denormalize as
much into there as you can. So a "user" object tends to grow to include
names, addresses, preferences, many-to-many relationships, anything else
you might need to update the user in a hurry.

But this means we're unserializing and then reserializing all these
elements from protocol format to native format and back with every
operation. And while it doesn't take a lot of CPU to deserialize a
single element or construct a single native object, it quickly adds up.

If you're moving a lot of data around, a small increase in efficiency
can be worth a lot.

Antipattern?
============

As I'm fond of saying "when in hole, stop
[digging](http://minecraft.gamepedia.com/Tutorials/Things_not_to_do#Don.27t_dig_straight_down)".
If the deserialize / alter / serialize pattern is causing you pain,
perhaps it is an [antipattern](http://c2.com/cgi/wiki?AntiPattern)?

[Cap'n Proto](https://capnproto.org/) looks like it has a lot of
potential here, since it doesn't actually deserialize to native objects
... instead it offers a class which is easily manipulated *in situ*.

I think it's a great idea, but as per [Conway's
Law](https://en.wikipedia.org/wiki/Conway%27s_law) these kind of APIs
often represent administrative boundaries within the organization, so it
is difficult to co-ordinate making such a change in protocol. If you're
currently using JSON or ProtoBufs you're probably stuck with it.

A Modest Proposal
=================

Back in the day, XML ran into exactly this problem. RAM was smaller back
then, and big datasets couldn't be deserialized all in one go, so [XML
SAX Parsers](https://en.wikipedia.org/wiki/Simple_API_for_XML) ruled the
earth.

Instead of parsing the entire document in one go, a SAX parser runs over
the document and generates 'events' at the start and end of every tag.
These events cause callback functions to be run, and the callback
functions can pull out the parts of the document you're interested in.
The event callbacks can also emit, element by element, a new XML
document. So you can alter or transform an XML document without ever
loading the whole thing into RAM at one time.

This general idea could be used with other protocol languages too, so
your new pseudocode looks like:

{% highlight python %}
    def update_attribute(new_value):

        def updater(key, value):
            if key == 'attribute': return new_value
            else: return value

        update(input_stream, output_stream, updater)
{% endhighlight %}

... all `update` has to do is to call the `updater` function for every
element in the structure, passing the name of the element within the
structure and the existing value. The `updater` function can then modify
the structure on the fly.

More generally, a `transform` function could allow a new structure to be
built, much as SAX does. This can even be done asynchronously, so that
the data to be written can start being emitted even before the data
being read is fully received, much like [Cut-through
Switching](https://en.wikipedia.org/wiki/Cut-through_switching).

Conclusion
==========

Even a small improvement in serialization efficiency has an enormous
dividend.

It is easy to think of the sophisticated class structures as the "real"
data and the serialized data as a pale reflection of that reality, but
perhaps this isn't the right way to think of it at all ...
