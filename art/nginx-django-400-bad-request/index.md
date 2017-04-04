---
category: Systems
date: '2014-02-26'
layout: article
redirect_from: '/Systems/nginx-django-400-bad-request/'
slug: 'nginx-django-400-bad-request'
summary: |
    I was setting up Django using Gunicorn behind an Nginx proxy the other
    day, and hit this problem which took a while to find an answer for ...
    all Django would do was return `400 Bad Request`
tags:
    - systems
    - nginx
    - django
    - python
title: 'Nginx proxy_pass to upstream Django always giving 400 Bad Request'
---

Problem
=======

I was setting up Django using Gunicorn behind an Nginx proxy the other
day, and hit this problem which took a while to find an answer for so I
figure I'll post it here.

The nginx config file looked like this:

~~~
upstream gunicorn_django {
    server localhost:8000;
}

location / {
    try_files $uri @proxy;
}

location @proxy {
    proxy_pass http://gunicorn_django;
}
~~~

... and all Django would do was return `400 Bad Request` every time when
accessed through the proxy, even though it worked perfectly when
accessed directly.

Cause
=====

Thanks to the comment in [this Stack Overflow
question](http://stackoverflow.com/questions/21399288/bad-request-400-nginx-gunicorn#)
by [Rune Kaagaard](http://stackoverflow.com/users/164449/rune-kaagaard),
I worked out that nginx was rewriting the Host header before passing to
the proxied host:

~~~
    Host: gunicorn_django
~~~

Django is fussy about the contents of the Host header, and [requires it
to be valid](https://code.djangoproject.com/ticket/20264) according to
[RFC 952](http://rfc-editor.org/rfc/rfc952.txt), as shown in
`django.http.request`:

~~~
host_validation_re = re.compile(r"^([a-z0-9.-]+|\[[a-f0-9]*:[a-f0-9:]+\])(:\d+)?$")
~~~

Solution
========

The easiest way around it is to prevent Nginx from rewriting the Host
header:

~~~
location @proxy {
    proxy_set_header Host $http_host;
    proxy_pass http://gunicorn_django;
}
~~~

... as a bonus, your Django applications can now know what Host was
originally being asked for.

Alternatively, don't use `_` in your upstream name, and this problem
won't occur!

Postscript
==========

Worrying about underscores in received Host headers seems like overkill
to me, and if they wanted to strictly adhere to [RFC
952](http://rfc-editor.org/rfc/rfc952.txt) they're being overly
permissive anyway, as it requires:

> The first character must be an alpha character. The last character
> must not be a minus sign or period. \[...\] Single character names or
> nicknames are not allowed.

... although the newfangled [RFC
1123](http://tools.ietf.org/html/rfc1123#page-13) is a little more
permissive:

> One aspect of host name syntax is hereby changed: the restriction on
> the first character is relaxed to allow either a letter or a digit.

... and anyway, how do you know those are valid IPv4 or IPv6 addresses?
But you really don't want to go down [that rabbit
hole](http://stackoverflow.com/questions/106179/regular-expression-to-match-hostname-or-ip-address)
because it only leads to
[madness](http://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags/1732454#1732454).
I think [Postel's
Law](http://en.wikipedia.org/wiki/Robustness_principle) should apply
here.
