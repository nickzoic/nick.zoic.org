---
category: etc
date: '2014-06-16'
layout: article
redirect_from: '/etc/tranquil-apis/'
slug: 'tranquil-apis'
summary: |
    Tranquil is a protocol framework which is designed to be very simple and
    very extensible.
tags:
    - architecture
    - www
    - html5
    - django
title: Tranquil APIs
---

I'm reaching the end of a project based on REST and [Django REST
Framework](/python/django-rest-framework/). There have been good parts
and bad, but out of it has come some [thinking about
architecure](/html5/basic-mobile-app-architecture/) and the inspiration
to do things a bit differently.

I've put together an alternative to REST which I'm calling *Tranquil*.

Summary
=======

*Tranquil* is a protocol framework which helps define the communication
between web client and server. It is designed to be very simple and very
extensible.

Tranquil is similar in intention to
[REST](http://en.wikipedia.org/wiki/Representational_state_transfer),
however:

-   Tranquil is transport agnostic, so transport could be by
    [WebSockets](http://websocket.org/), [AMQP](http://amqp.org/) or
    [avian carrier](http://www.ietf.org/rfc/rfc1149.txt).
-   Tranquil allows multiple queries per request to reduce round-trips
    and so multiple queries can be made within the one
    database transaction.
-   Tranquil actions are extensible, allowing the usual [Create, Read,
    Update and
    Delete](http://en.wikipedia.org/wiki/Create,_read,_update_and_delete)
    but also more complex operations such as [Map,
    Reduce](http://en.wikipedia.org/wiki/MapReduce) and
    [Atomic](http://en.wikipedia.org/wiki/Atomic_(computer_science))
    increments, appends and so on.
-   Tranquil actions are composable, allowing front-end developers to
    adjust for their own data requirements.

By contrast with [JSON-RPC](http://json-rpc.org/) and
[SOAPjr](http://www.soapjr.org/), Tranquil places more emphasis on
entities and less on methods, with the intention of reducing the
proliferation of custom methods.

Further Reading
===============

-   [Tranquil APIs](http://www.tranquil-apis.org/) documentation site.
-   Lightning Talk at [OSDC 2014](/etc/osdc-2014-gold-coast/)
    [Slides](/osdc2014/tranquil-apis.html), [Video (youtube,
    4 minutes)](http://www.youtube.com/watch?v=iCptoG4DpMI#t=590)
