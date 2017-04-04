---
category: Python
date: '2012-02-20'
layout: article
redirect_from: '/Python/syntax-error-keyword-argument-repeated/'
slug: 'syntax-error-keyword-argument-repeated'
tags:
    - python
    - vcs
title: 'SyntaxError: keyword argument repeated'
---

It turns out that repeated keyword arguments (kwargs) were illegal in
python 2.4, ignored in python 2.5 and illegal again in python 2.6. This
means that if some have crept into your codebase, you’ve now got a
handful of syntax errors!

For example, here’s test.py:

    def foo(**kwargs):
        for k, v in kwargs.iteritems():
            print "%s: %s" % (k, v)

    foo(a = 1, b = 2, a = 3)

And here’s what happens when you run it under 2.4, 2.5 and 2.6:

    nick@pluto:~/tmp$ python2.4 test.py
      File "test.py", line 5
        foo(a = 1, b = 2, a = 3)
    SyntaxError: duplicate keyword argument

    nick@pluto:~/tmp$ python2.5 test.py
    a: 3
    b: 2

    nick@pluto:~/tmp$ python2.6 test.py
      File "test.py", line 5
        foo(a = 1, b = 2, a = 3)
    SyntaxError: keyword argument repeated

How could this creep in? Most likely through revision control mergers.
Function calls with lots of kwargs are often laid out like:

    foo(
        kwarg_with_a_long_name=1,
        another_self_documenting_flag=False,
    )

Alice adds a kwarg for whatever="bar", at the start on the kwargs list,
before kwarg\_with\_a\_long\_name. So does Bob, but Bob adds it at the
end. The revision control system will happily merge these two changes
without conflicts as:

    foo(
        whatever="bar",
        kwarg_with_a_long_name=1,
        another_self_documenting_flag=False,
        whatever="bar",
    )

And under python 2.5, neither Alice or Bob are likely to notice ...
after all, foo() is being called with kwarg whatever="bar" just as they
intended.

But when the underlying system is upgraded to python 2.6, a mysterious
“SyntaxError: keyword argument repeated” appears, and no-one can quite
work out who to blame!
