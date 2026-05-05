---
title: Unknown Unknowns in MAVE Data
date: '2026-04-15'
layout: article
tags: 
  - bioinformatics
summary: "Thoughts from this year's Mutational Scanning Symposium"
---

> But there are also unknown unknowns -- the ones we don't know we don't know.
> -- [Donald Rumsfeld](https://en.wikipedia.org/wiki/There_are_unknown_unknowns)[^rumsfeld]

I've just finished up at this year's [Mutational Scanning Symposium](https://mss2026.org)
which was three days of incredible dense information and also getting to
meet a lot amazing friendly people including the [MAVEdb](https://mavedb.org/) team
who I've been working with for years but haven't met in person until now.

It left me with a lot to think about[^covid], too much to write up all at once, and for some
of the specifics I'll have to wait for the videos to come up on the
[Atlas of Variant Effects YouTube Channel](https://www.youtube.com/@cmap_cegs8443/)
but I've got to start somewhere and one thing came up as a recurring theme ...

## The VUS Crisis

This year seemed to be quite clinically oriented and several speakers mentiond the
["VUS Crisis"](https://www.insideprecisionmedicine.com/topics/molecular-dx/heidi-rehm-on-tackling-the-variant-of-uncertain-significance-crisis/) ... 
basically, we've discovered a lot of genetic variants, and while we've
determined that some of them are pathogenic and some benign, that leaves a 
hell of a lot of variants in neither category, aka "variants of unknown significance".

## Significance

MAVEs don't provide enough evidence on their own, but there are 
[Standards and Guidelines](https://pubmed.ncbi.nlm.nih.gov/25741868/) 
on how they can assist in classifying variants.
A high or low score in a MAVE can provide supporting evidence of pathogenicity or
benignity, or vice-versa (it depends what you're measuring).
In general this is done by picking thresholds beyond which the score
is regarded as significant.

[ExCALIBR](https://www.biorxiv.org/content/10.1101/2025.04.29.651326v2)[^swords] provides
a methodology for setting these thresholds and also the introduction is a good 
introduction to the concept of supporting evidence.  ExCALIBR's output provides both
an estimate of pathogenicity and a strength of evidence based on Bayesian stats.

## In search of mediocrity

I'm particularly interested in [hypomorphic](https://en.wikipedia.org/wiki/Muller%27s_morphs#Hypomorph)
variants, which are variants which produce an effect on a gene which reduces its
effectiveness but doesn't completely remove it.
Hypomorphic variants can be tricky to spot experimentally because
[negative feedback within the cell](https://en.wikipedia.org/wiki/Negative_feedback#Biology)
can mean that a gene which produces a protein which is half as effective just gets
[expressed more](https://en.wikipedia.org/wiki/Regulation_of_gene_expression)
to compensate.

But this isn't true for all genes and also the inefficient expression may have deleterious effects
on the whole organism even if individual cells do okay, so these variants are still interesting clinically.

Our current scoring and classification system doesn't really clarify between "we don't have
enough evidence to say if this variant is benign or pathogenic" and "we know this variant is hypomorphic",
and I think this is worth further investigation.

The first question I'm working on is:

* is there evidence of these variants in existing experimental data, such as that found in MAVEdb?

# TO BE CONTINUED

[^rumsfeld]: [Better known for other work](https://www.reddit.com/r/math/comments/rlamc/better_known_for_other_work/)

[^covid]: Unfortunately, also COVID.

[^swords]: Not to be mistaken for
      [ExCalibR](https://arxiv.org/pdf/2304.12311) or 
      [ExcalibR](https://mrsdprojects.ri.cmu.edu/2016teamg/wp-content/uploads/sites/18/2016/09/TeamG_CoDR.pdf) or
      [ExCalibr](https://nyudatascience.medium.com/excalibr-an-award-winning-system-for-educators-to-calibrate-exams-488bf78d396d) or
      [EXCALIBR](https://www.sciencedirect.com/science/article/abs/pii/S0925753507000495) ...
      researchers, do not name your new calibration tool after the famous sword.
