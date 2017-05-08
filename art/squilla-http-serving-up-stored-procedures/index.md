---
category: SQL
date: '2014-01-20'
layout: article
redirect_from: '/SQL/squilla-http-serving-up-stored-procedures/'
slug: 'squilla-http-serving-up-stored-procedures'
summary: |
    A (somewhat sketchy) connector between HTTP and postgres stored
    procedures ...
tags:
    - sql
    - django
    - backend
    - speculation
    - postgres
title: 'Squilla: Serving up Stored Procedures'
---

I'm a pretty [keen user of Django](/tag/django) but it has to be
recognized that ORM-based frameworks do introduce a certain amount of
complexity into a project.

You *do* get field validation, delete cascading, event triggers, all
kinds of exciting stuff, but here's an interesting thought: a lot of
that stuff already exists in SQL.

I'll be concentrating on [PostgreSQL](http://www.postgresql.org/) 9.3
for the purposes of this article but many other databases work very
similarly.

Views
=====

Django allows you to perform queries across multiple tables, pulling
together related entities in a single query. For example, a query like:

~~~
Article.objects.get(id=7).select_related('comment_set')
~~~

... would pull in an Article, and pull in all Comments related to that
article by doing something like:

~~~
SELECT * FROM article
LEFT JOIN comment ON (comment.article_id = article.id)
WHERE article.id = 7;
~~~

This is rather helpful, but the same thing could be done by setting up
an article\_with\_comments
[View](http://www.postgresql.org/docs/9.3/static/sql-createview.html)
which performs the join internally.

~~~
CREATE VIEW article_with_comments AS 
SELECT *,
    (SELECT JSON_AGG(comment.*) FROM comment WHERE article_id=article.id) AS comments_json ,
    (SELECT MAX(id) FROM comment WHERE article_id=article.id) AS max_comment_id
FROM article;
~~~

You can now query the View, which encapsulates the underlying details.

~~~
SELECT * FROM article_with_comments;

SELECT * FROM article_with_comments WHERE max_comment_id > 3;
~~~

Triggers
========

Django supports
[Signals](https://docs.djangoproject.com/en/dev/topics/signals/) which
run when changes are made to objects in the database.

The equivalent in SQL is to use
[Triggers](http://www.postgresql.org/docs/9.3/static/sql-createtrigger.html)
which offer the same kind of functionality.

Stored Procedures
=================

All modern SQL databases support [Stored
Procedures](http://en.wikipedia.org/wiki/Stored_procedure): chunks of
code stored in the database and which run within it. Stored procedures
are often written in some kind of [SQL
dialect](http://www.postgresql.org/docs/9.3/static/plpgsql.html), but
various databases allow "plugin" languages such as
[Python](http://www.postgresql.org/docs/9.3/static/plpython.html) or
[C](http://www.postgresql.org/docs/9.3/static/xfunc-c.html).

They're certainly [not trendy any
more](http://programmers.stackexchange.com/questions/65742/stored-procedures-a-bad-practice-at-one-of-worlds-largest-it-software-consulting),
but just perhaps that makes them worth another look!

Messages
========

I've talked before about [APIs based on
messages](/html5/basic-mobile-app-architecture/#messages). The general
idea is that each of these messages translates into a stored procedure
call. Each stored procedure runs a series of SQL commands, and sends
back the result as JSON. This is very similar to what happens in a
Django (etc) handler, only it is happening right there in the database
server!

Because these messages are not necessary
[idempotent](http://en.wikipedia.org/wiki/Idempotence), messages should
be carried by HTTP POST.

Stored Procs take named parameters, which map nicely onto the standard
[HTTP POST
x-www-form-urlencoded](http://en.wikipedia.org/wiki/POST_(HTTP)#Use_for_submitting_web_forms),
so we'll pass input through that way.

Sketchy Demo Code
=================

This very small bit of Python code demonstrates the general idea. It
uses psycopg2 and wsgiref libraries:

~~~
from urlparse import parse_qsl

import psycopg2
import psycopg2.extras

import json

db = psycopg2.connect("dbname='squilla' user='nick' password='hunter12'")

def application(environ, start_response):

    # Get the HTTP parameters

    name = environ['PATH_INFO'][1:]
    assert(name.isalnum())
    query = parse_qsl(environ['QUERY_STRING'], keep_blank_values=True)

    # Turn them into an SQL Query accessing a stored procedure

    sqlquery = (
    'SELECT * FROM public."%s" (' % name +
    ', '.join( '"%s" := %%s' % q[0] for q in query if q[0].isalnum())
    )
    sqlparams = [ str(q[1]) for q in query if q[0].isalnum() ]

    # Turn the response into JSON

    cursor = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute(sqlquery, sqlparams)
    response = json.dumps(cursor.fetchall())

    # Return the response in HTTP

    start_response('200 OK', [
        ( 'Content-Type', 'application/json' ),
        ( 'Content-Length', str(len(response)) ),
    ])
    return response

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    make_server('localhost', 8001, application).serve_forever()
~~~

Drawbacks
=========

-   **Having to learn SQL** ... One of the nice things about
    [Django](http://djangoproject.com/) or
    [SQLAlchemy](http://sqlalchemy.org/) and all the other ORMs is not
    having to write your own SQL. The downside of this is you have to
    keep a pretty close eye on the SQL they generate or you end up
    [getting burned](/python/testing-django-performance/). So you end up
    learning SQL anyway.
-   **Versioning stored procedures and triggers and migrating them** ...
    This is worthy of its own whole article.
    [South](http://south.aeracode.org/) does a great job of this for
    Django, so I'm looking for an equivalent. I've seen a few techniques
    for this but will come back and write a separate "Best Practice"
    post on this later.
-   **The application server layer just got a lot thinner** ... so
    you'll probably need to [scale Postgres
    out](http://wiki.postgresql.org/wiki/Replication,_Clustering,_and_Connection_Pooling)
    sooner than you might otherwise have had to.

Further Work
============

-   In the code above, all parameters are passed through as strings, and
    all returns are just done by JSONifying whatever comes back.

    Postgres actually has quite a lot of [function type information
    available](http://www.postgresql.org/docs/9.3/static/catalog-pg-proc.html)
    through its internal `pg_catalog.pg_proc` and `pg_catalog.pg_type`
    tables, and this could be scanned through at startup and used to
    help prepare parameters before calling the proc.

-   Postgres supports [advanced
    types](http://www.postgresql.org/docs/9.3/static/datatype.html),
    which could be passed in and out as JSON data structures. Functions
    which return the [json data
    type](http://www.postgresql.org/docs/9.3/static/datatype-json.html)
    should be able to construct their return value directly, rather than
    trying to squash their return data into a faux-table.
-   Many operations *are*
    [RESTful](http://en.wikipedia.org/wiki/Representational_state_transfer),
    and so rather than implementing a whole heap of tiny stored
    procedures it would make sense to support [GET, PUT, PATCH and
    DELETE](http://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods)
    against Views. Stored procedures can then be invoked by Triggers
    where necessary.
-   It'd make more sense to implement this using an asynchronous
    framework like [Tornado](http://tornadoweb.org/): we're spending
    *all* of our time in database operations so we need to be able to
    keep a lot of concurrent cursors running. [psycopg2 supports
    asynchronous database
    operations](http://initd.org/psycopg/docs/advanced.html#asynchronous-support),
    so that's good.
-   Having the web server handle session cookies and so on and pass them
    through to the stored procedures would be useful. Perhaps a
    "request" parameter would make sense for this.
-   Obviously, it needs
    [CSRF](http://en.wikipedia.org/wiki/Cross-site_request_forgery)
    protection and careful consideration of [SQL
    injection](http://xkcd.com/327/) hacks too!

Conclusion
==========

I can't see everyone abandoning Django and Rails and Node.js to come and
try this out, *but* I'd like to kick the idea around a bit longer and
see if I can write a demo project in it and see how it goes. Once
there's something worth seeing it'll be on
[GitHub](https://github.com/nickzoic/squilla).

Every project needs a name, so I decided to call it Squilla, because I
couldn't come up with any good "SQL on Squ..." jokes and anyway [Mantis
Shrimp](http://en.wikipedia.org/wiki/Squilla) are
[Awesome](http://theoatmeal.com/comics/mantis_shrimp).
