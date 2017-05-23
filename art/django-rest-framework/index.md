---
category: Python
date: '2014-02-06'
layout: article
redirect_from: '/Python/django-rest-framework/'
slug: 'django-rest-framework'
summary: |
    Django REST Framework: The Good, the Bad and the Ugly. Presented at
    MelbDjango 0.9 on 6 Feb 2014
tags:
    - python
    - django
    - architecture
    - www
title: Django REST Framework
---

Presented at [MelbDjango](http://melbdjango.com/) 0.9 on 6 Feb 2014.
[Here's the slides](/talk/melbdjango2/):

<iframe src="/talk/melbdjango2/" width="100%" height="400px" frameborder="0"></iframe>

Notes
=====

-   Thanks to [Common Code](http://commoncode.com.au/) for organizing,
    hosting and sponsoring [MelbDjango](http://melbdjango.com/).
-   Not much to add from tonight, except that around half the attendees
    have used or at least tried [Django REST
    Framework](http://django-rest-framework.org/) or the fairly similar
    [TastyPie](http://tastypieapi.org/) so it is obviously a bit of a
    thing at the moment.
-   Curtis's [django-nap](https://github.com/funkybob/django-nap) might
    be worth a look as a more minimalist take on a REST Framework.

Alternatives to REST
====================

I have some reservations about REST, mostly because it seems very
focussed on the "nouns" (resources) at the expense of the "verbs". Also
I fear that REST-as-she-is-spoke is tied a bit *too* closely to
HTTP/1.1.

Whereas RPC approaches are generally protocol-neutral and all about the
"verbs" (messages). I quite like [designing around
messages](../basic-mobile-app-architecture/) but they also have
their drawbacks and it seems to me there must be some kind of middle
ground.

> **note**
>
> I've done some further thinking about this: see [Tranquil APIs](../tranquil-apis/).
