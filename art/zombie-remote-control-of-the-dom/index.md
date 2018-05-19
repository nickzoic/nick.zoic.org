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

*I was originally thinking about this ... I don't know, some time
after 2006 which was when I got into Python but before 2011 which 
is when the idea morphed into
[Python in the Browser](../python-in-the-browser/) and crawled off to die.

I've talked a lot about
[mobile app architecture](../mobile-app-architecture/) and
[mobile application APIs](../tranquil-apis/) and
so on on this blog, but I don't think I've mentioned this before.
This isn't the [silliest](../squilla-http-serving-up-stored-procedures/)
[thing](../omnicode/) [I've](../squawk-cc-the-true-story/)
[written](../youve-got-no-mail/) about on this blog, so here goes:*

## Frontend and Backend

It's pretty common the write a web application in two parts: a frontend, 
perhaps using [Angular](https://angular.io/) or [Knockout](http://knockoutjs.com/);
and a backend, perhaps using [Django](https://www.djangoproject.com/)
or [Rails](http://rubyonrails.org/) or some similar framework.  The two codebases
are largely independent, joined only by an API between them, perhaps conforming
to REST principles and maybe even a [Swagger](https://swagger.io/) or
[Pact](https://docs.pact.io/) defining the API.

But that means three conjoined components already, and we haven't even considered
the database, or any external components or gateways.   
Sure, you could forego a separate frontend and just write everything as HTML
templates, but then you'd have to do actual page loads and people would think you
were uncool (to be fair: AJAX partial content loads are one of the few things
which are actually good about the modern web)

### Compiling to Javascript

So it'd be nice to write all your code in one place instead and have the whole
thing just sort itself out: after all, computers are supposed to be good at 
organising things.  Projects like [Haste](https://haste-lang.org/) and
[Batavia](https://batavia.readthedocs.io/en/latest/) and my 
(long dead) [Tropyc](https://github.com/nickzoic/tropyc) aim to compile a source
language up to Javascript to run selected parts of it in the browser.

Zombie takes a rather stupider, more direct approach.

## zombie.js

The browser loads a dummy page with content suitable for SEO.  There's not much 
interesting about that page, but it includes the zombie loader:

```
<script src="/zombie"></script>
```
That's going to make the browser `GET` the zombie loader code, which looks something
like:
```
(function () {
  function Z (msg) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function () {
      (new Function('Z', xhr.responseText))(Z);
    };
    xhr.open("POST", "/zombie");
    xhr.send(msg);
  }
  Z();
})();
```
This tiny snippet of code creates a function `Z`, which establishes a connection
back to the server, passes over a message `args` and asks it what to do next.
The server can reply with commands to update the DOM and to run snippets of Javascript.
Those snippets, in turn, can use `Z` to send more messages back
to the server.  The browser is no longer an independent process with its own mind:
it is a zombie, under control of the server process.

The server could be implemented in just about any language, the messaging protocol could run
over [POST requests](http://blog.fanout.io/2013/03/04/long-polling-doesnt-totally-suck/)
or over [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
or whatever technology the browser people come up with next.  So long as the zombie
messaging protocol is agreed upon, it doesn't really matter.

### That's horrible ...

Yes, this all sounds horribly inefficient and in a lot of ways it is: your backend 
is sending chunks of HTML instead of neat snippets of JSON, and there's some extra
chatter back and forth as events occur.  But the transport is compressed anyway,
and because we have control of both ends of the process, we can choose to only send
events we're interested in receiving, not every keystroke and mouse movement.

And in return for which, we've reduced our cognitive load: only one code base,
no need for a build pipeline, no need to document or implement an API.  The time
we would have spent on that stuff we can spend on developing features our users
actually care about.

### ... and insecure!

The zombie loader is indeed `eval()`ing code (more or less), and that sounds like
a scary thing, but that code is coming from the same server from which the loader
was loaded: you've already been bitten, you might as well start staggering around.

### But what about RESTful and Microservices and so on?

So rather than your HTML5 frontends consuming your microservices directly, they
talk to their Zombie [BFF (Backend for Frontend)](https://samnewman.io/patterns/architectural/bff/)
which talks to those services on their behalf: easy peasy.  The BFF layer doesn't 
hold much state, maybe just a little bit of per-user cache and session info, so can
be scaled out horizontally, geographically dispersed and killed off on a whim.

(at this point, the `BRAINS!` jokes are just writing themselves)

## zombie.py

To be continued ... very sketchy first experiments for a Python implementation of
[Zombie on GitHub](https://github.com/nickzoic/zombie/)


