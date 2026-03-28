---
title: unknown unknowns in MAVE data
date: '2026-03-28'
layout: draft
tags: 
  - bioinformatics
uses_mathjax: 3
---

I've just finished up at this year's [Mutational Scanning Symposium](https://mss2026.org)
which was three days of incredible dense information and also getting to
meet a lot amazing friendly people including the [MAVEdb](https://mavedb.org/) team
who I've been working with for years but haven't met in person until now.

It left me with a lot to think about, too much to write up all at once, and for some
of the specifics I'll have to wait for the videos to come up on the 'tubes,
but I've got to start somewhere and one thing came up as a recurring theme ...

# The VUS Crisis

This year was quite clinically oriented and a lot of speakers mentiond the
["VUS Crisis"](https://www.insideprecisionmedicine.com/topics/molecular-dx/heidi-rehm-on-tackling-the-variant-of-uncertain-significance-crisis/) ... 
basically, we've discovered a lot of genetic variants, and while we've
determined that some of them are pathogenic and some benign, that leaves a 
hell of a lot of variants in neither category, aka "variants of unknown significance".

# Significance

MAVEs don't provide enough evidence on their own, but there are 
[Standards and Guidelines](https://pubmed.ncbi.nlm.nih.gov/25741868/) 
on how they can assist in classifying variants.
A high or low score in a MAVE can provide supporting evidence of pathogenicity or
benignity, or vice-versa (it depends what you're measuring).
In general this is done by picking thresholds beyond which the score
is regarded as significant.

[ExCALIBR](https://www.biorxiv.org/content/10.1101/2025.04.29.651326v2)[^1]

# Score Distributions

So I mention this in ["Yeast Thoughts"](../yeast-thoughts/#statistical-treatment-of-frequencies)
but when we do a MAVE experiment we don't measure every cell.
We take a *sample* of cells, and that means we've got to deal with *statistics*.

Specifically, when we

`$$ \sigma_{v,t} = \left\{
\begin{array}{ c l } 
\sqrt{\frac{\hat{f}_{v,t}(1-\hat{f}_{v,t})}{C_t}} \approx \sqrt{c_{v,t}} / C_t & \quad \textrm{if } c_{v,t} > 0 \\
1 / C_t & \quad \textrm{if } c_{v,t} = 0 \\
\end{array}\right. $$`



[^1]: Not to be mistaken for
      [ExCalibR](https://arxiv.org/pdf/2304.12311) or 
      [ExcalibR](https://mrsdprojects.ri.cmu.edu/2016teamg/wp-content/uploads/sites/18/2016/09/TeamG_CoDR.pdf) or
      [ExCalibr](https://nyudatascience.medium.com/excalibr-an-award-winning-system-for-educators-to-calibrate-exams-488bf78d396d) or
      [EXCALIBR](https://www.sciencedirect.com/science/article/abs/pii/S0925753507000495) ...
      researchers, do not name your new tool after a famous sword.

