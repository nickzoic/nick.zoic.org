---
title: Yeast Thoughts
date: '2025-09-23'
summary: "Some thoughts about the yeast modeling we've been doing"
tags:
  - bioinformatics
  - simulation
layout: draft
uses_mathjax: 3
---

**Copy from my original Yeast Thoughts document as shared with Alan back in Feb 2024,
just switched into MathJax.  Then I'll fix this up to make it read a bit better.**

 We have raw sequence counts at several times, but what we actually want is a score for each variant, varying from 0 (totally useless) to 1 (totally unaffected).

We assume that nonsense variants are going to end up with a score of 0 and wild types/synonyms with a score of 1: eg: there's no enhancement of function likely.

We further assume that there are plenty of wild types/synonyms present in the mix, and that dead yeasts still contribute to turbidity (based on extensive evidence *in vitro*) and to DNA sequencing.

The turbidostat lets the yeast population grow indefinitely, so we can pretend the population can grow exponentially and unbounded. So a variety `$v$` at time `$t$` will have a population:

`$$ p_{v,t}=p_{v,0}a^{k_{v}t} $$`

... where `$a$` is the growth rate and `$k_{v}$` is the score of variety `$v$`.
For our yeast *Saccharomyces cerevisiae*, population doubles about every 1.5 hours so `$a\sim=1.6$` (for `$t$` in hours).

We assume that there's plenty of wild types / synonymous variants in the mix. Because of exponential growth, these varieties (`$k=1$`) will come to dominate the population and all other varieties will be diluted into insignificance eventually.

So the overall population `$P$` at time `$t$` can be approximated by:

`$$ P_{t}=P_{0}a^{t} $$`

... and a variety `$v$` at time `$t$` will have a fraction `$f$` of population:

`$$ f_{v,0}=p_{v,0}/P_{0} $$`

`$$ f_{v,t}=p_{v,t}/P_{t}=p_{v,0}a^{k_{v}t}/P_{0}a^{t}=f_{v,0}a^{(k_{v}-1)t} $$`

We can fit an exponential to the observed numbers and use the exponent to derive the score from `$k_{v}$`, limiting to the range [0,1].

As a sanity check, all synonymous variants should have `$k=1$`. We don't really care about `$P_{0}$` or `$a$` or `$f_{v,0}$` but a more sophisticated approach might.

Problems

If we've stumbled onto an enhancement variant then synonymous variants might end up with `$k<1$`. In which case we should normalize scores.

Mediocre varieties (`$0.5\lesssim k\lesssim0.9$`) actually increase in population fraction for a bit while the worse varieties are eliminated which messes up the exponential fit a little. Perhaps ignore data points before the maximum fraction? If the maximum fraction is the last value then we know k=1.

Alternatively fit to `$$ f_{v,t}=f_{v,0}(1-a^{xt})a^{(1-k_{v})t} $$` or something.
