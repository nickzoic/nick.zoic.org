---
category: HTML5
date: '2013-05-20'
layout: article
redirect_from: '/HTML5/mobile-app-architecture/'
redirect_from: '/HTML5/basic-mobile-app-architecture/'
redirect_from: '/art/basic-mobile-app-architecture/'
slug: 'mobile-app-architecture'
summary: |
    I want to discuss some weirder things on this blog, but I think it'd be
    a good idea to start off with an overview of how to build a very simple
    HTML5- or Native App friendly architecture.
tags:
    - html5
    - backend
    - mobile
    - architecture
title: Basic Mobile App Architecture
---

I want to discuss some weirder things on this blog, but I think it'd be
a good idea to start off with an overview of how to build a very simple
HTML5- or Native App friendly architecture.

1: UX
=====

> Design is not just what it looks like and feels like. Design is how it
> works.
>
> -- [Steve Jobs](http://en.wikiquote.org/wiki/Steve_Jobs)

Start here. Seriously. Applications exist to serve users, so the first
thing you have to consider is who the users are and what they need. Some
of those users will be the public interface, some will be the
administrative interfaces, but all users appreciate a good design.

[Storyboard](https://en.wikipedia.org/wiki/Storyboard) the application
out with lots of examples. Don't think of it as paper templates or badly
drawn screenshots, it is a series of sketches of "scenes" from the
"movie" of your application.

Use a
[whiteboard](https://itunes.apple.com/au/app/jotnot-scanner-pro-scan-multipage/id307868751?mt=8),
or pencil and paper, or one of the many mockup
tools or whatever works for you. Let the graphic designers [agonize over the
pixels](http://blog.mengto.com/the-one-pixel-rule/), as they will.

2: Entities
===========

> There are only two hard things in Computer Science: cache invalidation
> and naming things.
>
> -- [Phil Karlton](http://karlton.hamilton.com/)

At this point, I like to start thinking about entities, and how to name
them.

Some entities are the obvious nouns:

-   a Player
-   a Board
-   a Piece

Others are not so obvious: moving a Piece could also be thought of as
creating a new Move in the Game. Sometimes an entity represents a
relationship between two other entities, where that relationship has
properties of its own. Include notes on the relationships between entity
types, and *why*.

It may seem silly to be arguing about names at this point, but at some
point you may end up with a Competition, a Game, a Round and a Match,
all of which are distinct entities with different purposes. You'll be
glad you wrote up which was which *before* the backend team, the
frontend team and the database schema get confused and use the same
labels differently.

Write it up somewhere and stick to it.

3: Messages
===========

> All mass is interaction.
>
> -- [Richard P. Feynman](http://en.wikiquote.org/wiki/Richard_Feynman)

Typically, the next step is to start writing an actual database schema,
or a a RESTful protocol, or a class hierarchy, or something along those
lines.

But given the message-oriented world we find ourselves in client/server
applications (or quantum physics), I think it helps to first map out the
interactions, the *messages* sent at each step. So when you go from your
login screen to your welcome screen, a message gets sent requesting a
login and another message comes back with some login information.

> **note**
>
> I've done some further thinking on protocols and combining messages,
> leading to [Tranquil APIs](/etc/tranquil-apis/).

This is a good time to think about combining messages. If the UI always
displays the top 5 news stories to the user when they first log in, you
can save a request and a round-trip time by always including this
information along with the confirmation that login was successful. Even
networks with a lot of throughput can have lousy latency, so saving a
round-trip may be enough to make your app noticably snappier.
Additionally, your back-end may be able to service the requests in
parallel for even lower latency.

Public API
----------

You now have a list of messages and you can start thinking about how to
implement them. For a web-based app, this comes down to:

-   Old-fashioned HTTP GET / POST
-   [AJAX](http://en.wikipedia.org/wiki/AJAX_(programming))
-   ["Comet" / Long
    Polling](http://en.wikipedia.org/wiki/Comet_(programming))
-   [WebSocket](http://en.wikipedia.org/wiki/WebSocket)
-   Other Protocols (for native apps)

Which of these techniques is appropriate for which of your message
exchanges is beyond the scope of this post, although I intend to cover
WebSocket programming a lot more at a later date. To support a wide
range of browsers / devices you may need to provide a fallback: if
there's no WebSocket available in the browser, use Long Polling. If Long
Polling doesn't work in the user's network, use AJAX polling every 30
seconds. [If everything is broken, redirect the user
here.](http://www.ie6countdown.com/).

Whether your public API should include an API version number is
[hotly](http://stackoverflow.com/questions/389169/best-practices-for-api-versioning)
[contested](http://www.jbarnette.com/2009/04/07/http-apis.html), and I'm
not going to go into it here.

4: Development!
===============

> Make a mess, clean it up!
>
> -- [Burrell
> Smith](http://www.folklore.org/StoryView.py?story=Make_a_Mess,_Clean_it_Up!.txt)

Stub Back-End
-------------

At last, we get to write some code!

But it won't, at first, be very good code.

Which tool you use depends on which protocols you decided your API
needed. I like to use [Tornado](http://www.tornadoweb.org/) because it
is very simple and has good support for long poll and WebSocket.
[Node.js](http://nodejs.org/) is popular too. But if
[PHP](http://php.net/) or [CGI.pm](http://search.cpan.org/dist/CGI/) is
what you know best, do that.

You won't be connecting to a database or anything glamorous like that.
Instead, write some tiny stubs for each handler in your API (example in
Tornado):

~~~
class UserInfoHandler(tornado.web.RequestHandler):

    def get(self, user_id):
        self.write({
            'user_id': user_id,
            'name': 'John Doe %d' % user_id,
        })

class MessageWSHandler(tornado.websocket.WebSocketHandler):

    def on_message(self, message):
        self.write_message("What?")
~~~

Front-end(s)
------------

The stub back-end isn't going to stay. But it provides a handy point of
reference for the front-end developers while the real back-end is
getting developed. Their AJAX calls are answered, albeit with useless
pseudo-information, and instead of cut-and-pasting *Lorem Ipsum* all
over the place they can have it handed to them by a server.

Between the storyboards, the API documentation and the stub back-end to
play with, front-end development shouldn't be too hard. The data
returned by the stub back-end is predictable, so you can easily set up
tests with [Selenium](http://docs.seleniumhq.org/) and/or something like
[Sauce Labs](https://saucelabs.com/).

And you can develop HTML5 and native apps in parallel, so long as they
all agree on the API.

Back-end
--------

Leave the stub back-end in place somewhere where the front-end guys can
get to it, and start work on the real back-end. There's lots to consider
here, with many different products to choose from. But to keep it simple
I'd suggest you identify:

-   A disk-backed database which meets your indexing needs, SQL or
    otherwise (I'm fond of [MongoDB](http://www.mongodb.org/))
-   A memory-based cache (for example [memcache](http://memcached.org/)
    or [Redis](http://redis.io)
-   Perhaps a message queue (eg: [ØMQ](http://zeromq.org))
-   A language & framework which makes it easy to bind them all together
    (eg: [Tornado](http://www.tornadoweb.org/),
    [Django](http://djangoproject.com/), [Node.js](http://nodejs.org/),
    [Rails](http://rubyonrails.org/))

Once you've picked the database you can go back to your diagram of
entity relationships and turn it into a schema ... for an SQL database
this is probably a file full of SQL statements, for
[Django](http://djangoproject.com/) it is the
[models.py](https://docs.djangoproject.com/en/1.11/topics/db/models/)
file. For a lot of NoSQL databases there isn't a schema as such, but you
can still write up a description of what goes where.

In general, it isn't a bad idea to keep the database
[normalized](https://en.wikipedia.org/wiki/Database_normalization).
Rather than
[denormalizing](https://en.wikipedia.org/wiki/Database_normalization#Denormalization)
within the database, consider keeping such data only in the memory cache
... if the memory cache gets flushed, you can always regenerate the
denormalization.

5: You Didn't Mention Agile Once!
=================================

> The greatest challenge to any thinker is stating the problem in a way
> that will allow a solution.
>
> -- Bertrand Russell

This whole plan looks very, uh,
[waterfally](http://en.wikipedia.org/wiki/Waterfall_model). It isn't
meant to be. Changes just have to be propagated down.

For this reason, I'd recommend putting the docs in the source code
repository. To make a change, make a new branch, change what you need to
and "bubble" the changes down through the steps above. So the branch
ends up tying together the UX change, the message change, the API
change, and the back- and front- end changes.

To make merging less painful, save the docs in a diffable text format
like
[ReStructuredText](http://docutils.sourceforge.net/docs/user/rst/quickref.html)
or [MarkDown](http://daringfireball.net/projects/markdown/syntax). If
you're feeling really extreme, you could save diagrams as
[GraphViz](http://www.graphviz.org/) and [XFig](http://www.xfig.org/)
format, but that might be overkill. Saving individual diagrams as
separate files with sensible names can be worthwhile though.
