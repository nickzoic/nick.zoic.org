---
category: etc
date: '2015-10-30'
layout: article
redirect_from: '/etc/squawk-cc-the-true-story/'
slug: 'squawk-cc-the-true-story'
summary: 'Distributed Disruption of Surveillance ...'
tags:
    - www
    - crypto
title: 'Squawk.CC -- The true story'
---

Metadata Retention
==================

On Monday, before [OSDC 2015](https://2015.osdc.com.au/) got started,
some of us attendees were sitting around a bar in Salamanca Place and
the topic of [Australia's new Metadata Retention
legislation](https://www.ag.gov.au/dataretention) came up, as it tends
to.

"It's the first step onto a slippery slope!", I spluttered into my
espresso martini. "And expensive and ineffective anyway!" (espresso
martinis tend to have that effect on me). "Even our Minister for
Communications, uh, Prime Minister uses a VPN and encrypted chat clients
these days."

The Legislation
===============

For the moment, the explanation of the legislation says:

> Paragraph 187A(4)(b) puts beyond doubt that service providers are not
> required to keep information about subscribers’ web browsing history.

... but the wording of
[187A(4)(b)](https://www.comlaw.gov.au/Details/C2015A00039/Html/Text#_Toc416860259)
is clearly written by lawyers not engineers:

> (4) This section does not require a service provider to keep, or cause
>     to be kept:
>
> > (b) information that:
> >
> > > \(i) states an address to which a communication was sent on the internet,
> > > from a telecommunications device, using an internet access service
> > > provided by the service provider; and
> > >
> > > (ii) was obtained by the service provider only as a result of
> > >     providing the service; or
> >
> > Note: This paragraph puts beyond doubt that service providers are
> > not required to keep information about subscribers’ web browsing
> > history.

There's a [thoughtful article
here](https://bendechrai.com/2015/03/31/the-myth-of-the-innocuousness-of-metadata/)
... at this point, and given [the situation in the
UK](http://www.theguardian.com/law/2015/oct/30/uk-internet-providers-may-yet-be-required-to-keep-your-browsing-data),
I don't think anyone believes this is over.

Initial Idea
============

Back to Salamanca ...

"Anyway", I declaimed, "all it would take to make the whole web metadata
logging thing intractable would be for someone to inject some code into
web pages which caused a whole bunch of random IPs to get prodded every
time someone loaded a page."

"You should implement that and do a lightning talk on it", exclaimed
[Ben Dechrai](https://bendechrai.com/), appearing in a cloud of
[Buzzconf](http://buzzconf.io/) stickers. "Dunno", I said, considering
another martini. "I've got [a talk](/etc/osdc-2015-hobart/) to prepare
already, and I might actually want to listen to someone else talking for
a change too ..."

"How about I implement it and give you the credit", offers Ben.

"How about you implement it and I get another drink ..." I suggested,
heading back to the bar ...

Launch at OSDC
==============

So to cut a long story short, Ben went and implemented it in his copious
free time the next day.

On Thursday's lightning talks at OSDC 2015, he announced
[squawk.cc](http://squawk.cc/), which by this point had not just a
domain name but [a github repo](https://github.com/bendechrai/squawk), a
logo contributed by
[Donna](https://2015.osdc.com.au/speaker/profile/38/) and an SSL
certificate is on its way from [Let's
Encrypt](https://letsencrypt.org/).

Why do you want to destroy Western Civilization, and also won't somebody think of the children?
===============================================================================================

The point of Squawk isn't to destroy Western Civilization As We Know It,
it is to demonstrate the uselessness and invasiveness of trying to log
this kind of thing en masse.

Further Work
============

As it stands, Squawk is rather dumb and picks addresses completely at
random from the top few Australian A-class netblocks, doing a single
`GET /` request via AJAX. It could be made a lot better. Why not make a
pull request?
