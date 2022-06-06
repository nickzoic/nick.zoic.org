---
category: HTML5
date: '2013-11-24'
layout: article
redirect_from: '/HTML5/static-vs-dynamic-sites/'
slug: 'static-vs-dynamic-sites'
summary: |
    The current storm in a teacup seems to be about static vs. dynamic
    website design. As usual, this is a False Dichotomy ... actually,
    there's a whole range of options to explore.
tags:
    - html5
    - mobile
    - architecture
    - aws
    - www
    - static
title: 'Static vs. Dynamic Sites'
---

The current
[storm](http://www.reddit.com/r/programming/comments/1qygeu/response_to_paul_graham_static_sites_fixies/)
in a
[teacup](https://www.bitballoon.com/blog/2013/11/18/ecstatic-on-static-sites-and-fixies)
seems to be about static vs. dynamic website design. As usual, this is a
[False Dichotomy](http://en.wikipedia.org/wiki/False_dilemma) ...
actually, there's a whole range of options to explore.

Different Types of Dynamic
==========================

Utterly Static

:   Media assets such as `founders-in-garage.jpg` are utterly static.
    They may hopefully one day be replaced by prettier assets such as
    `founders-on-yacht.jpg` but in the meantime they can be thrown
    directly into the repository, deployed out to a CDN and
    cached indefinitely.

Statically Deployed

:   Your CSS is probably compiled from [SASS](http://sass-lang.com/) or
    similar, and your Privacy Policy, etc, pages are probably templated
    out of your CMS. Your Javascript may well be [compiled from some
    more exotic language](https://github.com/jashkenas/coffeescript/wiki/list-of-languages-that-compile-to-js) too. It can be handy to do
    this stuff dynamically in development systems, but when deploying to
    production you really might as well deploy the compiled versions as
    static files which change only when the site is redeployed. For
    example, [this blog is statically generated using
    Pelican](../new-static-site/) and then
    copied up to [AWS S3](http://aws.amazon.com/s3/).

Periodically Updated

:   Some content changes periodically, but not often compared to the
    number of times it is read. For example, a news site might update
    its headlines every few minutes. Rather than having every request
    for the homepage hit the database every time, just to see if
    anything has changed, it can be worthwhile to take periodic
    snapshots and serve them up as if they were static files! The [HTTP
    ETag](http://en.wikipedia.org/wiki/HTTP_ETag) mechanism makes it
    easy for browsers to detect if anything has changed before loading
    the content again.

Dynamically Updated

:   Even content which changes too quickly for this to be a practical
    approach can benefit from a caching layer. Whenever objects are
    updated, throw the fully serialized HTML / JSON objects into a
    key/value store. You can use a filesystem, or (for example) [NGINX
    can read directly from
    memcached](http://nginx.org/en/docs/http/ngx_http_memcached_module.html).

Utterly Dynamic

:   Well, some stuff is always going to have to be generated fresh
    every time. Individualized views, custom searches, that kind
    of thing. But it is the exception to the rule: [99% of your user
    interaction probably isn't that
    dynamic!](http://en.wikipedia.org/wiki/1%25_rule_(Internet_culture))
    And if your data really has to be *that* fresh, perhaps you need to
    be looking into [Websockets](http://websocket.org/) instead?

Combining Types of Content
==========================

Not only are there a whole range of different levels of dynamicism to
choose from, your site can combine them as appropriate.

For example, your news site could:

-   Use a *Periodically Updated* `index.html` page with the front page
    content embedded in it for immediate display.
-   This page loads *Statically Deployed* CSS and Javascript assets, and
    some *Utterly Static* media assets too. Assuming the user has been
    to your site recently, these will largely return `304 Not Modified`.
-   The Javascript can then load the user profile\[*\]\_ from a cache
    of*Dynamically Updated\* user profile JSON docs. This data can then
    be used to customize the user's experience.

Making this work elegantly may involve some messing around with [Cache
Manifests](../taming-cache-manifest-caching/)
and [Cross-Origin Request
Sharing](http://en.wikipedia.org/wiki/Cross-origin_resource_sharing) but
it has the potential to radically decrease the amount of infrastructure
you have to deal with to handle page views.

SEE ALSO
========

* [Static Sites using jQuery to appear Dynamic](/art/static-jquery-dynamic) 
  (it's not actually jQuery specific, that was just what people used for
  this kind of thing in 2014.)
