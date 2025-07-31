---
category: etc
date: '2018-05-01'
updated: '2025-07-25'
layout: article
title: 'ZOMBIE: Remote control of the DOM'
summary: |
    What if you could have a rich web frontend without developing one?
tags:
    - architecture
    - www
    - html5
    - python
    - speculation
    - gui
---

## Frontend and Backend

It's pretty common the write a web application in 
[two parts](../mobile-app-architecture/): a frontend, 
perhaps using [Angular](https://angular.io/) or [Knockout](http://knockoutjs.com/);
and a backend, perhaps using [Django](https://www.djangoproject.com/)
or [Rails](http://rubyonrails.org/) or some similar framework.  The two codebases
are largely independent, joined only by an [API](../tranquil-apis/) between them, perhaps conforming
to REST principles and maybe even a [Swagger](https://swagger.io/) or
[Pact](https://docs.pact.io/) defining the API.

But that means three conjoined components already, and we haven't even considered
the database, or any external components or gateways.   
Sure, you could forego a separate frontend and just write everything as
[HTML templates](../templates-fugit/), but then you'd have to do actual page
loads and people would think you
were uncool (to be fair:
[AJAX partial content loads](../static-jquery-dynamic/)
are one of the few things which are actually good about the modern web)

### Compiling to Javascript

So it'd be nice to write all your code in one place instead and have the whole
thing just sort itself out: after all, computers are supposed to be good at 
organising things.  Projects like [Haste](https://haste-lang.org/) and
[Batavia](https://batavia.readthedocs.io/en/latest/) and my 
(long dead) [Tropyc](https://github.com/nickzoic/tropyc) aim to compile a source
language up to Javascript to run selected parts of it in the browser.

I was originally thinking about this ... I don't know, some time
after 2006 which was when I got into Python but before 2011 which 
is when the idea morphed into
[Python in the Browser](../python-in-the-browser/) and crawled off to die.

Zombie takes a rather stupider, more direct approach.

## zombie.js

The browser loads a dummy page with content suitable for SEO.  There's not much 
interesting about that page, but it includes the zombie loader:

{% highlight html %}
<script src="/zombie"></script>
{% endhighlight %}
That's going to make the browser `GET` the zombie loader code, which looks something
like:

{% highlight javascript %}
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
{% endhighlight %}

This tiny snippet of code is wrapped in `(function() { ... })();` which just
creates an anonymous function and then immediately runs it.  This gives us 
a nice clean function scope to work inside.

Within that scope it creates a function `Z`, which establishes a connection
back to the server endpoint `POST /zombie` and sends a message `msg`.

When the server replies, the `xhr.onload` function is run.  The `xhr.responseText`
gets compiled into a javascript function using `new Function('Z', xhr.responseText)`,
which indicates that the function takes one parameter (`'Z'`).  It's a slightly nicer
way of saying `eval("function (Z) {" + xhr.responseText + "}")`, basically.

We then run that function, which can do whatever we want it to:
update the DOM, run snippets of Javascript, set up further functions, whatever.
We pass in the `Z` function — yeah, the same one we're currently writing.
The new function can use `Z` to send more messages back to our server,
without us having to pass `Z` around in a global namespace.

Lastly, the outer function runs `Z()` to `POST` an inital, blank message and kick
the whole process off.

The browser is no longer an independent process with its own mind:
it is a zombie, under control of the server process.

The server could be implemented in just about any language, the messaging protocol could run
over [POST requests](http://blog.fanout.io/2013/03/04/long-polling-doesnt-totally-suck/)
or over [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
or whatever technology the browser people come up with next.  The zombie messaging
protocol is all contained in that function `Z` so it doesn't really matter.

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

### ... and what about RESTful and Microservices and so on?

So rather than your HTML5 frontends consuming your microservices directly, they
talk to their Zombie [BFF (Backend for Frontend)](https://samnewman.io/patterns/architectural/bff/)
which talks to those services on their behalf: easy peasy.  The BFF layer doesn't 
hold much state, maybe just a little bit of per-user cache and session info, so can
be scaled out horizontally, geographically dispersed and killed off on a whim.

### Why Zombie?

At this point, the `BRAINS!` jokes are just writing themselves.
For the real inspiration, see
[Ophiocordyceps unilateralis](https://www.theatlantic.com/science/archive/2017/11/how-the-zombie-fungus-takes-over-ants-bodies-to-control-their-minds/545864/) 
but there's no way I'm naming a project that.

## zombie.py

To be continued ... very sketchy first experiments for a Python implementation of
[Zombie on GitHub](https://github.com/nickzoic/zombie/)


