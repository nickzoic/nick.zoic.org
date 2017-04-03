---
category: etc
date: '2014-07-19'
layout: article
redirect_from: '/etc/programming-for-startups/'
slug: 'programming-for-startups'
title: Programming for Startups
---

> I presented a session on 'Programming for non-Programmers' talk at
> General Assembly Founder's Bootcamp ... here's some notes which I
> jotted down afterwards ...

[I](https://generalassemb.ly/instructors/nick-moore/2879) presented a
talk on "Programming for non-Programmers" as part of [General
Assembly](http://ga.co/)'s "[Founder's
Bootcamp](https://generalassemb.ly/education/founders-bootcamp-a-two-day-startup-mba/melbourne/5351)"
course this morning.

The [slides](http://nick.zoic.org/files/pfnp.pdf) are probably a bit too
terse to be useful so here's some notes. Feel free to get in touch if
you've got questions or feedback:

Programming for non-Programmers
===============================

I've been dealing with software & systems for about 20 years now, and
this presentation goes for 90 minutes, so obviously we're not going to
cover everything in detail.

This talk isn't really about how to write software, it's about how not
to burn through all your money on software development without achieving
anything.

I've split it into three parts:

1.  Architecture
2.  Agility
3.  Implementation

Architecture
============

Very Fast ... but very dumb
---------------------------

Computers (these days) are very fast:

-   Billions of cycles / sec
-   Millions of bytes / sec
-   Thousands of writes / sec

So there are many problems you can easily solve in software.

*All attendees but one were indeed interested in doing something
software centric ...*

But computers are also very dumb. They're still quite lousy at:

-   Face recognition
-   Voice recognition
-   Handwriting recognition
-   "Do What I Mean".

As a startup, you can't really afford to be researching interesting
challenging problems in computer science, so if your idea needs any of
these things to be useful you're probably better off leaving it to
Google.

I mentioned [this](https://www.google.com.au/search?q=hp+racist)
unfortunate kerfuffle re: facial recognition.

Performance
-----------

These days, infrastructure is so easy to rent or buy that you can built
anything you want, from a single CPU to hundreds of CPUs, from \$5/month
up until your money runs out. But as a startup, you don't want to spend
more than you need to.

How do you know what to actually spend? Look at your business plan. You
should have a milestone your aiming for ... maybe say 10,000 users. Work
out what you need for that milestone. 10,000 users who use your service
once a day is maybe 1 request per second. You could probably get away
with running on a [free AWS micro
instance](http://aws.amazon.com/free/).

Likewise, if your application doesn't *need* high reliability, don't
bother building it. It's a lot of fun [reading up on how Netflix do
it](http://nick.zoic.org/etc/some-thoughts-on-aws/) but for startups its
often not necessary and you probably can't afford it.

Components
----------

*SOURCE CODE IS NOT AN ASSET*.

[Kurt](https://generalassemb.ly/instructors/kurt-falkenstein/1183)
talked about how your intellectual property is an asset and how even
your [losses are an
asset](https://www.ato.gov.au/General/Losses/How-companies-use-tax-losses/),
but it is important to realize that your software itself is not an
asset.

> Measuring programming progress by lines of code is like measuring
> aircraft building progress by weight.
>
> -- Bill Gates

Software is something you have to build to make your business work, but
it isn't the point of your business, just a tool. The less of it you
have to write the better. Use existing components whenever you can.

If your planned exit is by selling your business, your buyers will be
interested in your customer base, your brand and maybe your algorithms.
They'll rewrite your actual software to work their way anyway.

(Does anyone think Facebook couldn't have replicated the software of
[WhatsApp](http://en.wikipedia.org/wiki/WhatsApp) for a whole lot less
than they paid for it?)

The key to using existing components is to divide and conquer. Split the
problem up into parts and choose a good tool for each part.

### Front-end vs. Back-end

The main division here is about trust. You can never trust a device you
don't control, so keep your business rules in the back-end and just use
the front-end for presentation.

This is actually a very old architectural model called [Tiered
Architecture](http://en.wikipedia.org/wiki/Multitier_architecture) which
splits into Presentation, Logic and Data. These correspond to a
front-end, and back-end and a database. The presentation layer is all
about showing the data to the user, the logic layer about enforcing
business rules and the data layer about enforcing consistency and not
forgetting stuff.

### Message Queues

There's also interesting things like [Message
Queues](http://en.wikipedia.org/wiki/Message_queue) to consider, which
have actually [been around a
while](http://en.wikipedia.org/wiki/Dataflow_architecture) but are
suddenly trendy again. They're a way of getting around people's
expectations that everything will be instantaneous on the web. You
respond to requests immediately but queue the actual work up to be done
more slowly in the background.

### External Services

There's also external services such as email and credit-card gateways to
consider. Some of these are very good and some are rather painful to
deal with.

*we mentioned some details here but that can wait for another blog post
I think ...*

Websites & Webapps
------------------

There's a range of options:

-   CMS sites, like a wordpress site.
-   Static HTML
-   HTML with Templates & Forms: lots of Rails and Django sites work
    this way
-   HTML with some AJAX improvements
-   "Single page HTML5", which are really apps written in Javascript.

As you go down the list, the results get more sophisticated, more
capable and more flexible, but also more expensive to develop. There's
an upgrade path there where you can start out with something very simple
and improve it as you go along.

I've tried using [jQueryMobile](http://jquerymobile.com/) and such to
make HTML5 apps which look like native, but people's expectations of
native apps are so high that they always thing the HTML5 imitations look
sluggish compared to a native app. Take the same app and make it look
like a website, it seems really quick compared to a website.

Some of my favourite Web programming / HTML5 resources:

-   [Dive into HTML5](http://diveintohtml5.info/)
-   [Douglas Crockford on Javascript](http://javascript.crockford.com/)
-   [CanIUse](http://caniuse.com/#cats=HTML5)
-   I've also [written a few articles on HTML5
    myself](http://nick.zoic.org/html5/).

Apps & Applications
-------------------

There's also native apps for various platforms:

-   iOS, Android, Windows Phone
-   PC Applications (Windows, Mac, Linux)
-   Hybrid & Mixed approaches.

The nice thing about apps is they get sold in an app store, so you don't
have to set up your own payment infrastructure. On the other hand, the
app store takes a pretty big percentage.

I once had a conversation with a client which went something like this:

> Client: "Can you write us an iPhone app?"
>
> Me: "Sure, what do you want it to do?"
>
> Client: "I want it to get our logo on our customer's home screen".
>
> Me: "But it's got to *do something*, right?
>
> Client: "Of course, or they wouldn't put it on their home screen".

The app wasn't there to solve a technical requirement, but a marketing
one. Users can install your HTML5 site [on their home
screen](http://cubiq.org/add-to-home-screen) but it is still a different
path that the app store one and users may find it confusing.

We also talked briefly about [Sencha](http://www.sencha.com/) and
[Unity](http://en.wikipedia.org/wiki/Unity_%28game_engine%29) and
[Haxe](http://haxe.org/) as ways of getting out of this mess.

You could also consider mixed approaches where a relatively simple
native app does hardware interfacing, and the passes off to a more
visually exciting HTML5 site for display back to the user.

Agility
=======

I talked a bit about the [Agile Manifesto](http://agilemanifesto.org/)
and whether or not it was [still
relevant](http://pragdave.me/blog/2014/03/04/time-to-kill-agile/). I
won't recap it all here since there is no shortage of discussion on the
web.

> The word "agile" has been subverted to the point where it is
> effectively meaningless.
>
> -- Dave Thomas, co-author of the Agile Manifesto

Everyone seemed to have heard of Agile, which was nice. Mostly I talked
about breaking the work up into Sprints and Phases and thus not getting
stuck in a [Death
March](http://en.wikipedia.org/wiki/Death_march_%28project_management%29)
or for that matter a series of [Death
Sprints](http://www.kuro5hin.org/?op=displaystory;sid=2002/7/12/62459/7742).

Mostly I want to emphasize here that this is mostly a matter of
[organizational culture](http://www.ietf.org/tao.html), not a set of
rules you can follow.

I also mentioned:

-   [Pomodoro
    Technique](http://en.wikipedia.org/wiki/Pomodoro_Technique)
-   [Trello](https://trello.com/) for doing cards without actually
    having index cards.

I've just finished a project which used Trello to coordinate tasks
between five team members in five different locations, three in
Australia and two in the UK! I'm totally blown away by just how well it
worked.

I skipped over Revision Control but probably the best place to start
learning these days is [Github](https://github.com/). Here's a pretty
good [Introduction to Git](http://rogerdudler.github.io/git-guide/).

Documentation
-------------

Nobody particularly likes writing documentation and it seems like the
kind of thing a startup can't afford to do. But actually if done right
it is a great way to clarify your ideas before development starts.

In particular, we talked about [Document Driven
Development](https://www.google.com.au/search?client=ubuntu&channel=fs&q=document+driven+development),
particularly writing an informal document such as the the FAQ or help
file or
[README](http://tom.preston-werner.com/2010/08/23/readme-driven-development.html)
first before you try to do more formal documentation.

If you sit down and write:

> Q: How do I log in? A: You can log in with a username and password, or
> via Facebook.

... well, you just wrote a testable requirement without even thinking
about it. Likewise, if you write:

> Q: How do I pay if I don't have a credit card? A: At the moment we can
> only accept automatic payments by credit card.

... you just documented a limitation that you can come back to at the
end of your first development phase.

There are also other kinds of documents to consider

-   User Stories
-   Wireframes
-   Requirements
-   Specifications

... these don't have to be a formal process, but work out some way to
keep them up to date and track changes, as they provide a valuable
record of how your ideas are progressing.

Testing & Regressions
---------------------

There's a logic riddle which goes something like this:

> Q: Why do cars have brakes? A: So you can drive fast without crashing.

Why write tests? So you can iterate fast without breaking your
production servers!

This isn't an original observation, by the way, see this

:   series of blog posts:
    [1](http://jonjagger.blogspot.ie/2011/07/why-do-cars-have-brakes.html)
    [2](http://www.devjoy.com/2013/02/why-do-cars-have-brakes/)
    [3](http://manuel.kiessling.net/2011/04/07/why-developing-without-tests-is-like-driving-a-car-without-brakes-2/) ...
    but I think it's a useful one!

Humans are very bad at doing repetitive tasks repeatably, so write
automated tests. There's lots of good tools out there to do this in the
web world, such as [Selenium](http://docs.seleniumhq.org/) and
[SauceLabs](https://saucelabs.com/).

Implementation
==============

*We kind of rushed through this bit because time was running out and the
group didn't seem to be at this phase just yet. I'll have to have a
think about how to write a better talk and/or blog post about these
decisions at some point.*

Languages
---------

> You can do anything in any language. You can also eat soup with a
> knife.
>
> -- [Ville Vainio](http://reddit.com/u/vivainio).

There are many different languages out there, and they each have good
points and bad. But there's a reason this question is way down here at
the end of the slides.

If you were starting a delivery business, you wouldn't decide, on day 1,
what brand of cars to buy. You'd have a look around at several brands,
get some idea of which brands supplied which kinds of vehicles at the
prices you needed, then shelve that information untl you were ready to
actually buy.

Likewise, the decision about what platforms, languages and frameworks to
go with can be put off until after you've nailed a lot of other
specifications down. As a startup a large input may be who is actually
available to hire.
