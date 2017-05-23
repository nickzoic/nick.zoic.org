---
category: HTML5
date: '2014-01-02'
layout: article
redirect_from: '/HTML5/static-jquery-dynamic/'
slug: 'static-jquery-dynamic'
summary: |
    A couple of people have mentioned that while they like the idea of
    offloading their site to a CDN, they're not ready to have their site
    look like some relic from 1999 ...
tags:
    - html5
    - mobile
    - architecture
    - aws
    - www
    - django
    - static
title: Static Sites using jQuery to appear Dynamic
---

This is a little addendum to my [previous post about static vs. dynamic
sites](../static-vs-dynamic-sites/). A couple of people have
mentioned that while they like the idea of offloading their site to a
CDN (such as [AWS S3](http://aws.amazon.com/s3/)), they're not ready to
have their site look like some relic from 1999.

jQueryUI Autocomplete
=====================

One of the most obvious changes since the bad old days is the
helpfulness of modern web forms. Rather than expect you to scroll
through a `<select>` list of 10,000 items, they use widgets like
[jQueryUI Autocomplete](http://jqueryui.com/autocomplete/) to help you
find your choice, and they use [AJAX calls to load subsets of the list
of choices
dynamically](http://api.jqueryui.com/autocomplete/#option-source),
rather than having to load the whole list upfront.

For example, a postcode selector could be implemented something like
this:

``` {.sourceCode .javascript}
$("input.postcode").autocomplete({
minLength: 2,
source: '/api/postcodes/'
});
```

... and on the backend, the `/api/postcodes/` URL would connect to a
handler (django view, etc) which asks the database to
`SELECT code, name FROM postcodes WHERE name LIKE ?` or similar. This
works great, except that everytime a user goes and selects a postcode,
that's another dynamic query your backend has to deal with, despite the
postcode data hardly ever changing.

To get around this, we *could* export the whole postcodes database to a
single file and load the whole thing once the page has rendered. It'd
still look better than stuffing all the postcode data into an HTML
select box, but we can do better.

Serving up Postcode Searches
============================

The autocomplete widget will accept a function as the data source, so we
can have more control over the URL which is used to retrieve the data.
For example, we can change the URL format used:

``` {.sourceCode .javascript}
$("input.postcode").autocomplete({
minLength: 2,
source: function(request, response) {
        var match = request.term.toUpperCase().match(/[A-Z]{2}/);
        if (match) {
        $.ajax(
            '/postcodes/search_' + match[0] + '.json'
        ).done(function (data) {
        var termre = new RegExp($.ui.autocomplete.escapeRegex(request.term));
        response(data.filter(
                    function (x) {
            return termre.test(x);
                    })
                );
            }).fail(function () {
        response([]);
            });
        } else {
    response([]);
        }
}
});
```

... this appears to be dynamic, in that the user gets a filtered list,
but it is actually being fed from a group of small JSON files in the
directory `/postcodes/`. As these are static files, they can be uploaded
to a CDN, get cached by the browser, etc.

Of course, the downside is that you now need a way to maintain 676
little JSON files, `search_AA.json` through `search_ZZ.json`. The
easiest way to do this depends on your framework ...

Generating the Files in Django
==============================

In Django, you write models and views to return the proper data. This is
handy for development anyway, since you can generate the pages
dynamically in development and statically in production

`models.py`:

``` {.sourceCode .python}
from django.db import models

class Postcode(models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=200)
```

`views.py`:

``` {.sourceCode .python}
from postcode.models import Postcode
from django.http import HttpResponse
import json

def postcode_search(request, term):
    data = [
        "%s %s" % (pc.name, pc.code)
        for pc in Postcode.objects.filter(name__istartswith=term)
    ]
    return HttpResponse(
        json.dumps(data),
        mimetype="application/json"
    )
```

`urls.py`:

``` {.sourceCode .python}
from django.conf.urls import patterns, include, url
from postcode.views import *

urlpatterns = patterns('',
    url(r'^postcode/search_(?P<term>\w+).json', postcode_search),
)
```

Going Static With Django Medusa
===============================

[Django Medusa](https://github.com/mtigas/django-medusa/) provides an
easy way to replicate your dynamic content to static content instead.
Medusa needs some hints as to which files to generate, which go in a
file called `renderers.py`:

``` {.sourceCode .python}
from django_medusa.renderers import StaticSiteRenderer
import string

class PostcodeSearchRenderer(StaticSiteRenderer):

    def get_paths(self):
        for a in string.uppercase:
            for b in string.uppercase:
                yield "/postcode/search_%s.json" % (a+b)

renderers = [
    PostcodeSearchRenderer,
]
```

Now when you run `manage.py staticsitegen`, all 676 itty bitty JSON
files will be created.

Based on my postcode database, the biggest of these files,
`search_MO.json` is 13kB, which is a big improvement over the \~300kB
required to download the whole thing. There are 429 files which are just
`[]` ... there aren't many suburb names starting with `QZ`.

Obviously, this approach could be made more sophisticated, with variable
length prefixes and so on. But with this relatively simple approach
we've already achieved an appearance of dynamic content with an entirely
static backend.
