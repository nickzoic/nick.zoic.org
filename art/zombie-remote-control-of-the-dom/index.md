---
category: etc
date: '2018-05-01'
layout: draft
title: 'ZOMBIE: Remote control of the DOM'
summary: |
    What if you could have a rich web frontend without developing
    one?
tags:
    - architecture
    - www
    - html5
    - python
---

*I've talked a lot about
[mobile app architecture](../mobile-app-architecture/) and
[mobile application APIs](../tranquil-apis/) and
so on on this blog, but I don't think I've mentioned this before
and it came up in conversation so I thought I'd write it.*

*I was originally thinking about this ... I don't know, some time
after 2006 which was when I got into Python but before 2011 which 
is when the idea morphed into
[Python in the Browser](../python-in-the-browser/) and crawled off to die.
This isn't the [silliest](../squilla-http-serving-up-stored-procedures/)
[thing](../omnicode/) [I've](../squawk-cc-the-true-story/)
[written](../youve-got-no-mail/) about on this blog, so here goes:*

# ZOMBIE: Remote Control of the DOM

## Frontend and Backend

It's pretty common the write a web application in two parts: a frontend, 
perhaps using [Angular](https://angular.io/) or [Knockout](http://knockoutjs.com/)
or some similar framework, and a backend, perhaps using [Django](https://www.djangoproject.com/)
or [Rails](http://rubyonrails.org/) or some similar framework.  The two codebases
are largely independent, joined only by an API between them, perhaps conforming
to REST principles.

That means three conjoined components already, and we haven't even considered
the database, or any external components or gateways.   
Sure, you could forego a separate frontend and just write everything as HTML
templates, but then you'd have actual page loads and people would think you
were uncool.

### Compiling to Javascript

So it'd be nice to write all your code in one place instead and have the whole
thing just sort itself out: after all, computers are supposed to be good at 
organising things.  Projects like [Haste](https://haste-lang.org/) and
[Batavia](https://batavia.readthedocs.io/en/latest/) and my 
(long dead) [Tropyc](https://github.com/nickzoic/tropyc) aim to compile a source
language up to Javascript to run selected parts of it in the browser.

Zombie takes a rather stupider, more direct approach.

## zombie.js

The browser loads a dummy page with content suitable for SEO.  At the end of that
page is the `zombie.js` loader, which established a connection back to the server
to ask it what to do next.  The server can reply with commands to update the DOM
and to run snippets of Javascript.  Those snippets, in turn, can send messages back
to the server.  The browser is no longer an independent process with its own mind:
it is a zombie, under control of the server process.

The server could be implemented in just about any language, the messaging protocol could run
over [POST requests](http://blog.fanout.io/2013/03/04/long-polling-doesnt-totally-suck/)
or over [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
or whatever technology the browser people come up with next.  So long as the zombie
messaging protocol is agreed upon, it doesn't really matter.

### That's horrible!

Yes, this all sounds horribly inefficient and in a lot of ways it is: your backend 
is sending chunks of HTML instead of neat snippets of JSON, and there's some extra
chatter back and forth as events occur.  But the transport is compressed anyway,
and because we have control of both ends of the process, we can choose to only send
events we're interested in receiving, not every keystroke and mouse movement.

And in return for which, we've reduced our cognitive load: only one code base,
no need for a build pipeline, no need to document or implement an API.  The time
we would have spent on that stuff we can spend on developing features our users
actually care about.

### What about RESTful and Microservices and so on?

So rather than your HTML5 frontends consuming your microservices directly, they
talk to their Zombie [BFF (Backend for Frontend)](https://samnewman.io/patterns/architectural/bff/)
which talks to those services on their behalf: easy peasy.  The BFF layer doesn't 
hold much state, maybe just a little bit of per-user cache and session info, so can
be scaled out horizontally, geographically dispersed and killed off on a whim.

(at this point, the BRAINS! jokes are just writing themselves)

## zombie.py







