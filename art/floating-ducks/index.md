---
date: '2025-04-05'
layout: draft
tags:
  - database
  - testing
title: 'Floating Ducks'
summary: 'Floating Ducks: Analysing and fixing a weird bug in DuckDB'
---

## The Issue

I was waiting for tests to run on other things in DuckDB when I
happened to notice
[Issue 16901: multiple right joins produce wrong result](https://github.com/duckdb/duckdb/issues/16901)
which looked kind of odd.  I couldn't quite work out what the example
code was trying to do:

```
CREATE TABLE t0(c0 DOUBLE);
CREATE TABLE t1(c0 DOUBLE);
CREATE TABLE t2(c0 DOUBLE);
INSERT INTO t0(c0) VALUES (0.0);
INSERT INTO t1(c0) VALUES ('-0.0');
INSERT INTO t2(c0) VALUES (0.0);

select subquery1.s1, t2.c0 from
(
  select t0.c0 as s1, t1.c0 as s2
  FROM t0
        RIGHT JOIN t1 ON t0.c0 = t1.c0 where NOT t0.c0
) as subquery1
right join t2 on CAST(subquery1.s1 AS TEXT) = CAST(t2.c0 AS TEXT);

┌────────┬────────┐
│   s1   │   c0   │
│ double │ double │
├────────┼────────┤
│  NULL  │  0.0   │
└────────┴────────┘
```

... but yeah, it did look like it was getting the wrong result, and 
I could reproduce the same result from that query.  But why?
The query has two right joins and a subquery so it's kind of hard to
follow, so I wanted to come up with something simpler ...

## Negative Zero?

The first thing which jumped out at me was the negative zero value.
A `DOUBLE` is an [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754)
double precision floating point number, and these have some odd
properties and rules.

One of these is the ["signed zero"](https://en.wikipedia.org/wiki/Signed_zero).
There's actually two zero values in IEEE floating point, positive zero and
negative zero.  They are "equal", in that `+0.0 == -0.0`, but not always 
interchangeable.

This isn't just a DuckDB thing, it goes 
[all the way down to the silicon](https://www.felixcloutier.com/x86/fdiv:fdivp:fidiv).

For example `(1/+0.0::DOUBLE) = 'inf'::DOUBLE` whereas `(1/-0.0::DOUBLE) = '-inf'::DOUBLE`
and at least in DuckDB they cast to text as different values:
`0.0::DOUBLE::TEXT = '0.0'` but `(-0.0::DOUBLE)::TEXT = '-0.0'`.

(Note that this doesn't apply to DuckDB's INTEGER or DECIMAL types, which
have a different internal representation, just `FLOAT` and `DOUBLE`)

## Simplifying

The first thing to do was to work out whether I could find a simpler
query which exhbits the same problem.  After a little messing around
I came up with:

```
create table x as (select 0.0::double as a);
create table y as (select '-0.0'::double as b);
select * from x inner join y on a = b;

┌────────┬────────┐
│   a    │   b    │
│ double │ double │
├────────┼────────┤
│  0.0   │  0.0   │
└────────┴────────┘
```

Whichever table is on the left table gets chosen for both columns:

```
select * from y inner join x on a = b;

┌────────┬────────┐
│   b    │   a    │
│ double │ double │
├────────┼────────┤
│  -0.0  │  -0.0  │
└────────┴────────┘
```

This doesn't look *very* wrong, but note that value `b` ... there is 
no row where `y.b` is `0.0::DOUBLE`, so where is it coming from?

Of course, it only makes a difference if you care about the value of `b::text`
or similar, but the original query did.

A little more experimentation revealed that this problem only occurs
when you join on `a = b`.  Joining on anything else 
such as `a = +b` or `a = b::FLOAT` or `a = sin(b)` all get the expected result:

```
select * from x inner join y on a = +b;

┌────────┬────────┐
│   a    │   b    │
│ double │ double │
├────────┼────────┤
│  0.0   │  -0.0  │
└────────┴────────┘
```

This made me suspect there was some optimization working specifically for 
joins on equalities, so I went looking through the source code ...

## Into the Source

After a bit of stumbling about I found the following comment in
`src/optimizer/remove_unused_columns.cpp`:

```
// for inner joins with equality predicates in the form of (X=Y)
// we can replace any references to the RHS (Y) to references to the LHS (X)
// this reduces the amount of columns we need to extract from the join hash table
```

This seemed like a pretty likely candidate!

A quick experiment at removing the optimization entirely showed that this fixed
the problem, but the optimization is pretty sensible for any column type
which doesn't have this weird property.  I couldn't find any other equivalent
situations for numeric types or unicode strings or anything like that.

So I ended up writing up 
[PR #16965](https://github.com/duckdb/duckdb/pull/16965) to prevent the 
optimization just for floating point columns and after a bit of wrestling
worked out how to get it to pass the CI tests and got that PR submitted.

Some time soon the PR will get accepted and merged and closed and this little
piece of work will be put away.

I have no idea what the original bug reporter was trying to do.

I have quite a lot of experience with SQL but I don't think I've ever joined
on a floating point column, and if I ever have I'm sure I never worried
about inserting negative zeros or comparing the results as cast to strings.

# So: what is the point of this?



