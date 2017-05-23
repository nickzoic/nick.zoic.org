---
category: etc
date: '2012-08-22'
layout: article
redirect_from: '/etc/cryptographic-hash-uris/'
slug: 'cryptographic-hash-uris'
subtitle: Cryptographic Hash URIs
tags:
    - www
    - speculation
    - crypto
title: 'Imagine There''s No URLs'
---

**Imagine** ...

It is 1990 at CERN, and work is beginning on a new information
management system called
"[Mesh](https://www.w3.org/History/1989/proposal.html)". They need a
[uniform way to identify
resources](https://en.wikipedia.org/wiki/Uniform_resource_identifier).
The syntax of [URLs](http://en.wikipedia.org/wiki/URL) is becoming
[quite complex](http://www.w3.org/People/Berners-Lee/FAQ.html). What if
we do away with [all this](http://en.wikipedia.org/wiki/True_Names) and
just identify a Resource by its [Cryptographic
Hash](http://en.wikipedia.org/wiki/Cryptographic_hash_function) ?

Cryptographic Hash URIs {#cryptographic-hash-uris-1}
=======================

> I have to say that now I regret that the syntax is so clumsy.
> *\[...\]* But it is too late now.
>
> -- [Tim
> Berners-Lee](http://www.w3.org/People/Berners-Lee/FAQ.html#etc)

An [MD2](http://en.wikipedia.org/wiki/MD2_(cryptography)) hash is 128
bits long. This is plenty big enough that even with a [trillion
pages](http://googleblog.blogspot.com.au/2008/07/we-knew-web-was-big.html)
there is [little chance](http://en.wikipedia.org/wiki/Birthday_problem)
of collision.

Even in 1990 it would have been obvious that MD2 would be obsoleted
soon, and that this would
[continue](http://en.wikipedia.org/wiki/MD4#Security) to occur. Tim
could wisely include the hash name at the start, so a URI might look
like:

    md2:65d39bdcda41f0aeb232d7d90e58bb6c

These URIs can be used in documents to refer to other documents, just
like we use URLs today. I'm not really interested in speculating about
[HTML](http://infomesh.net/html/history/early/), so we'll just assume
that it stays much the same, and links for
[pages](http://www.w3.org/History/19921103-hypertext/hypertext/WWW/TheProject.html)
and [images](http://en.wikipedia.org/wiki/Les_Horribles_Cernettes) stay
in their familiar form:

~~~
<a href="md2:6c508c14308f608dd24602201cfc13fe">The World Wide Web Project</a>
<img src="md2:742b8198cff94b32c92ec8a44fad9091" alt="LHC">
~~~

MD2 was obsoleted by MD4, which was obsoleted by MD5 then
[SHA-1](http://en.wikipedia.org/wiki/SHA-1) and now
[SHA-2](http://en.wikipedia.org/wiki/SHA-2). The modern version of these
URLs would probably use SHA-2 hashes 224 bits long, for example:

    sha2:930a7d0833e427f99b5d8b06d7275d0e1704e4ead87c016018a2c381

As a sad footnote, this leaves [Sun
Microsystems](http://web.archive.org/web/19990421184325/http://www.sun.com/)
as "the colon in emm-dee-five-colon."

Caching
=======

A [URL](https://en.wikipedia.org/wiki/URL) gets its uniqueness from
centralized authority: the [Domain Name
System](https://en.wikipedia.org/wiki/Domain_Name_System) guarantees the
uniqueness of the first part, and the filesystem of the web server
guarantees the uniqueness of the second part.

Except when it doesn't. Domain names change ownership, [Round Robin
DNS](https://en.wikipedia.org/wiki/Round-robin_DNS) and [Load
Balancers](http://en.wikipedia.org/wiki/Load_balancing_(computing))
switch between filesystems and the filesystems are always subject to
change.

This makes caching web resources rather difficult, and has led to
schemes like [ETags](https://en.wikipedia.org/wiki/HTTP_ETag) which add a
revision identifier to a resource to make it possible to see if it has
changed. Cryptographic hashes are frequently used to calculate ETags.

In contrast, Cryptographic Hash URIs describe resources which never
change, so are easy to cache.

Security
========

Resources may be modified on the server: you think you're downloading a
particular version of a particular file, but it may have been tampered
with. Resources may also be
[modified in transit by your ISP](http://www.mattcutts.com/blog/confirmed-isp-modifies-google-home-page/)
or by [other
intermediaries](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).

A client loading a resource by Cryptographic Hash URI can tell if the
file has been modified by calculating the hash of the received resource
itself, and alerting the user if the calculated hash does not match the
URI they asked for.

Publishing Documents
====================

> When you see URLs on grocery bags, on billboards, on the sides of
> trucks, at the end of movie credits just after the studio logos --
> that was us, we did that.
>
> -- [JWZ](http://www.jwz.org/gruntle/nomo.html)

There is, of course, a problem. I can write all the documents I want on
my local disk, and link them to each other, but how do I *publish* them
so that others can see them.

[Usenet](http://tools.ietf.org/html/rfc1036) was [still going
strong](http://en.wikipedia.org/wiki/Usenet#Public_venue) at the time,
and can provide some inspiration.

-   Expand on IHAVE/GIVEME protocols here.

Problems
========

There's some stuff here I need to expand on ...

-   Crosslinking
-   Updating Documents
-   Signing Documents
-   Ranking Documents
-   Publishing URLs with [QR Codes](http://en.wikipedia.org/wiki/QR_code)
