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

## Background: The Experiment

In my [PyConAU 2025 talk](/art/pycon-pyconau-2025-melbourne/) I talk a little bit
about testing modified versions of the
[human *G6PD* gene in yeast (Geck et al)](https://www.biorxiv.org/content/10.1101/2025.08.11.669723v2),
in that study we just used a simple linear interpolation of growth rates and it worked
out fine but this is an attempt to tackle the interesting mathematics of yeast growth.

*G6PD* is a gene for an [antioxidant enzyme also called G6PD](https://en.wikipedia.org/wiki/Glucose-6-phosphate_dehydrogenase), and
[pathogenic variants of *G6PD*](https://en.wikipedia.org/wiki/Glucose-6-phosphate_dehydrogenase_deficiency)
can lead to
[haemolysis](https://en.wikipedia.org/wiki/Hemolysis)
(the destruction of red blood cells) and thus
[Haemolytic anemia](https://en.wikipedia.org/wiki/Hemolytic_anemia).

### Many Variants

The aim is to test thousands of variants of *G6PD* against each other, and to score
the different variants from bad (0) to good (1).
This should give us some additional insight into the structure and behaviour of the G6PD
protein, as well as some clinical insights into patients with unknown variants, eg:
if a patient has *this* variant, is that likely to be a problem for them?

This experiment is done in brewer's yeast
([*Saccharomyces cerevisiae*](https://en.wikipedia.org/wiki/Saccharomyces_cerevisiae))
because they reproduce very quickly and no-one minds you killing a billion of
them before lunch.

The experiment is done by knocking out the yeast's own [*ZWF1*](https://www.alliancegenome.org/gene/SGD:S000005185) gene 
and inserting variants of [human *G6PD*](https://www.alliancegenome.org/gene/SGD:S000005185) using plasmids.  The variants used are a library
of all possible single base substitutions.

### Turbidostat

Once that's done, the yeasts are cultured and then placed under oxidative stress
by adding some bleach.
This is done in a *turbidostat* which keeps the yeast suspension at a set
[turbidity](https://en.wikipedia.org/wiki/Turbidity).
This is measured as a quantity [OD<sub>600</sub>](https://en.wikipedia.org/wiki/OD600)
which is the [optical density](https://en.wikipedia.org/wiki/Absorbance)
of 600nm ([orange](https://en.wikipedia.org/wiki/Orange_(colour)))
light on a 1cm path through the yeast suspension.

![experimental setup](img/turbidostat.svg)
*experimental setup*

The turbidostat uses a pump to add nutrients and remove excess yeasts to keep the 
turbidity the same, much like a [thermostat](https://en.wikipedia.org/wiki/Thermostat) 
controls temperature by turning a heater on and off.

This means there's always plenty of nutrients for the yeasts, it is as if they are
growing in an unlimited environment where they can multiply indefinitely, doubling
in population every 90 minutes or so.

Under these conditions, the yeasts are [haploid](https://en.wikipedia.org/wiki/Haploid) and
reproduce asexually.
Because of this the "daughter cells" will have exactly the same genome as the parent, and
thus our population of variants is preserved.

However, more successful variants will reproduce more rapidly than less successful
variants, and come to dominate the population.

### Yeast Population

In this experiment the turbidity setpoint is OD<sub>600</sub> = 0.5.
[Getting from OD<sub>600</sub> to cell concentration is complicated](https://www.nature.com/articles/s41598-023-28800-z)
but using an approximation of 1 × 10^7 cells per mL per OD<sub>600</sub>,
there's about a billion (1 × 10^9) cells in each 200mL turbidostat.

### Measurements

Samples were taken at ten timepoints, for each of the four replicates.
I'm only really interested in the two "stress" replicates at this point, so
I'm ignoring the two "control" replicates.

Samples were taken at every four hours at first, backing off to every 12 hours.
The intention of this was to get some more subtlety in scoring, rather than just
a score of survived or didn't.

> more samples were taken within the first 24 hours intending to capture
variants with very low activity that were rapidly lost from the population

**I should emphasize at this point that I had nothing to do with the "wet lab" side of 
things, all that hard work was done by other people, and the closest I get to working
with actual yeasts is having a beer while thinking about the numbers which come out
of these experiments!**

At the same time, the number of "volume replacements" made by the turbidostat
was recorded, based on the run time of the turbidostat's pump which
indicates how much growth medium was added.

| Nominal Time | Volume Replacements (stress 3) | Volume Replacements (stress 4) |
|---|---|---|
| 0 | 0 | 0 |
| 4 | 0.52 | 0.45 |
| 8 | 2.11 | 2.06 |
| 12 | 3.71 | 3.68 | 
| 16 | 5.23 | 5.19 |
| 24 | 8.78 | 8.82 |
| 36 | 13.92 | 19.95 |
| 48 | 19.31 | 19.31 |
| 60 | 24.63 | 24.65 |
| 72 | 30.57 | 30.32 |

For each sample, sequencing was performed to see what proportion
of the yeasts were of what varieties.

The number of sequences captured at each time point varied quite
a lot, the smallest sample being 1.4 Mseq and the largest
6.6 Mseq!

| Nominal Time | Experiment | Number of Sequences |
|---|---|---|
| 0 | library | 9465789 |
| 4 | stress 3 | 2194742 |
| 8 | stress 3 | 1601970 |
| 12 | stress 3 | 2377144 |
| 16 | stress 3 | 2529157 |
| 24 | stress 3 | 1259293 |
| 36 | stress 3 | 2829533 |
| 48 | stress 3 | 1616839 |
| 60 | stress 3 | 4933458 |
| 72 | stress 3 | 4457441 |
| 4 | stress 4 | 1408777 |
| 8 | stress 4 | 2892289 |
| 12 | stress 4 | 3877352 |
| 16 | stress 4 | 4711909 |
| 24 | stress 4 | 2751762 |
| 36 | stress 4 | 2264457 |
| 48 | stress 4 | 2469222 |
| 60 | stress 4 | 6577424 |
| 72 | stress 4 | 1639330 |

For the paper, we just did a linear least-squares fit of 
population fraction to volume replacements, and that was 
adequate to get some nice results for score distribution
with good correlation between replicates, and the distribution of 
nonsense and synonymous variants was as expected:

![good correlation between replicates and good distribution of nonsense and synonymous variants](img/g6pd_histo.svg)
*good correlation between replicates and good distribution of nonsense and synonymous variants (unpublished preliminary data)*

## Selected Variants

![selected variants](img/plot-exp.svg)
*selected variants (unpublished preliminary data)*

This graph shows several selected variants from the experimental data, and how 
their population changes with time.

| Variant | Classification | Score |
|---|---|---|
| p.= | wild type | ~ 1 |
| p.Ala109Ter | nonsense | ~ 0 |
| p.Ala300Met | missense | high |
| p.Asp282Gln | missense | high |
| p.Gln195Leu | missense | medium |
| p.Phe237Ser | missense | medium | 
| p.Phe241Pro | missense | low |

## More Math!

However, it'd be nice to consider a better mathematical model for the
yeast growth.

The turbidostat lets the yeast population grow indefinitely.
Imagine we really did have a big enough experimental setup to allow
the population to grow exponentially and unbounded.

We assume that there's plenty of robust variants in the mix.
Because of exponential growth, these variants will come to dominate
the population and all other varieties will be diluted into insignificance eventually.

The overall population `$P$` at time `$t$` can thus be approximated by:

`$ P_{t}=P_{0}a^{t} $`

Where `$a$` is our growth rate (`$a \approx 1.6$` for `$t$` in hours)

Less robust variants will replicate more slowly or not at all.
A variety `$v$` at time `$t$` would have a population:

`$ p_{v,t}=p_{v,0}a^{k_{v}t} $`

... where `$k_{v}$` is the score of variety `$v$`.

Our turbidostat only keeps a fraction of the yeast suspension around, but the
ratio of variants will be the same as in the unlimited case.
A variety `$v$` at time `$t$` will have a fraction `$f_{v,t}$` of population:

`$ f_{v,0}=p_{v,0}/P_{0} $`

`$ f_{v,t}=p_{v,t}/P_{t}=p_{v,0}a^{k_{v}t}/P_{0}a^{t}=f_{v,0}a^{(k_{v}-1)t} $`



### Processing Results


## More Math!

# Original Notes

**Copy from my original Yeast Thoughts document as shared with Alan back in Feb 2024,
just switched into MathJax.  Then I'll fix this up to make it read a bit better.**

 We have raw sequence counts at several times, but what we actually want is a score for each variant, varying from 0 (totally useless) to 1 (totally unaffected).

We assume that nonsense variants are going to end up with a score of 0 and wild types/synonyms with a score of 1: eg: there's no enhancement of function likely.

We further assume that there are plenty of wild types/synonyms present in the mix, and that dead yeasts still contribute to turbidity (based on extensive evidence *in vitro*) and to DNA sequencing.

For our yeast *Saccharomyces cerevisiae*, population doubles about every 1.5 hours so `$a\sim=1.6$` (for `$t$` in hours).



We can fit an exponential to the observed numbers and use the exponent to derive the score from `$k_{v}$`, limiting to the range [0,1].

As a sanity check, all synonymous variants should have `$k=1$`. We don't really care about `$P_{0}$` or `$a$` or `$f_{v,0}$` but a more sophisticated approach might.

Problems

If we've stumbled onto an enhancement variant then synonymous variants might end up with `$k<1$`. In which case we should normalize scores.

Mediocre varieties (`$0.5\lesssim k\lesssim0.9$`) actually increase in population fraction for a bit while the worse varieties are eliminated which messes up the exponential fit a little. Perhaps ignore data points before the maximum fraction? If the maximum fraction is the last value then we know k=1.

Alternatively fit to `$$ f_{v,t}=f_{v,0}(1-a^{xt})a^{(1-k_{v})t} $$` or something.
