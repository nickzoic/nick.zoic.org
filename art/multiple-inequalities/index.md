---
category: Python
date: '2012-02-20'
layout: article
redirect_from: '/Python/multiple-inequalities/'
slug: 'multiple-inequalities'
tags:
    - python
    - appengine
title: Multiple Inequalities in Google AppEngine
---

So I’m playing around with Google AppEngine (still!) trying to put
together some kind of sensible use for it. AppEngine is neat-O, but it
is also quite limited in what it can and can’t do. One of the most
glaring problems (for my toy app) is the datastore query API, which has
various restrictions, including:

> Inequality Filters Are Allowed On One Property Only

Now this is pretty obviously an efficiency measure: retrieving on
inequalities involves iterating along one index, and the datastore isn’t
in the business of picking which one to iterate along. But its also
really annoying if you actually want to do something which needs
multiple inequalities.

The way around it, of course, is to let the datastore handle the first
inequality, and then post-filter to assess the rest. This works great
(despite various other datastore limitations, eg: never returning more
than 1000 rows) but having to do it explicitly in the main part of the
code reduces the elegance of the code:

``` {.sourceCode .python}
Things.all().filter("foo >", foo).filter("bar >", bar).filter("qux >", qux)
```

is more elegant than:

``` {.sourceCode .python}
[ t for t in Things.all().filter("foo >", foo) if t.bar > bar and t.qux > qux]
```

especially if you’re generating the queries on the fly. Wouldn’t it be
nice to be able to have the filter() method work out whether this was a
disallowed inequality and if so, handle it as a post-filter?

Well, with a little Python magic, this is possible. First, a mixin class
lets us declare models as:

``` {.sourceCode .python}
class Things(MultiInequalityMixin, db.Model):
    # etc
```

Using the following Mixin class:

``` {.sourceCode .python}
class MultiInequalityMixin(object):
    """ Allows multiple inequality matches in a query. """

    @classmethod
    def all(cls, **kwds):
        return MultiInequalityQuery(cls, **kwds)
```

This just gets Things.all() to pass back our own special Query() object
instead of the standard one. The MultiInequalityQuery class derives from
the standard db.Query class, and overrides Query.filter() with its own
method. Its filter() method passes through the first inequality as
normal, but later inequalities get turned into little post-filter
closures and stashed in a list. Then the \_\_iter\_\_ iterator method
checks these post-filters as it yields up the results:

``` {.sourceCode .python}
class MultiInequalityQuery(db.Query):

     def filter(self, prop_op, value):
        """ pass through most queries, except inequalities
        where this wouldn't be allowed. """

        prop_op_match = prop_op_regex.match(prop_op)
        if prop_op_match:
            prop, op = prop_op_match.groups()

            if self.ineq_prop not in (prop, None):
                self.ineq_post.append(make_closure(prop, op, value))
                return self
            self.ineq_prop = prop

        super(MultiInequalityQuery, self).filter(prop_op, value)
        return self

    def __iter__(self):
        """ Chain onto the Query.__iter__ but reject objects not passing
        all the postfilters """

        for x in super(MultiInequalityQuery, self).__iter__():
            if all([ f(x) for f in self.ineq_post ]):
                    yield x
```

… and some other methods which wrap up the other methods (fetch, count)
based on \_\_iter\_\_. I haven’t even considered GQL because it just,
somehow, doesn’t do much for me :-) but it should be doable in the same
way. There are limitations here: it’s not all that efficient to load up
a lot of rows and throw most of them out again. The “best” (eg: most
restrictive) inequality should go first, but which one is it?

I've published the [Multiple Inequalities in Google AppEngine code
here](http://code.zoic.org/inequality_mixin/) ... note that this is
still pretty sketchy and I'm not really interested in developing it
further myself. Take it and run with it!
