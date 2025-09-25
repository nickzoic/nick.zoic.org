---
title: vamp-seq binned scored considered ...
date: '2025-09-25'
summary: "How to better get a score from bin counts"
tags:
  - bioinformatics
  - simulation
layout: draft
uses_mathjax: 3
---

## VAMP-seq

Recently I've worked with a bunch of experimental data from VAMP-seq[^1]
and while I'm a big fan of
[glowing jellyfish](https://en.wikipedia.org/wiki/Green_fluorescent_protein)
and the
[sorting machine](https://www.bdbiosciences.com/en-au/products/instruments/flow-cytometers/research-cell-sorters/bd-facsaria-iii)
looks like an espresso machine made by [SGI](https://en.wikipedia.org/wiki/SGI_O2),
there's one thing which always bothered me about this paper.

[^1]: Matreyek, K.A., Starita, L.M., Stephany, J.J. et al.
    Multiplex assessment of protein variant abundance by massively parallel sequencing.
    Nat Genet 50, 874–882 (2018).
    doi: [10.1038/s41588-018-0122-z](https://doi.org/10.1038/s41588-018-0122-z)

So to very briefly summarize how VAMP-seq works:

1. To see how much different cells are expressing a gene, you fuse that gene with
   a gene for EGFP or similar, so the cells glow more the more the gene is expressed.
2. Then you set up the cell sorting machine to sort the cells into four "bins".
   First a sample is measured to establish quartile thresholds for the sorter, 
   so that cells get sorted into four groups, with roughly the same population
   in each group.
3. Then you sort the cells into four output tubes.
4. Then you sequence each of the four tubes and count up variants per "bin".
5. Variants are scored by combining counts from each bin.

There are several things which can go wrong here. 
Thresholds can be set incorrectly or inaccurately.
Output tubes can get contaminated, sequenced differently,
lost or swapped[^2] into the wrong bin.
Some of these problems are probably avoidable using careful lab techniques
but human error is inevitable.
[^2]: Hallway discussions, MSS 2025 Barcelona.

I'll come back to that later, but in the mean time let's talk scoring.

## VAMP-seq Scoring

> VAMP-seq scores are calculated from the scaled,
> weighted average of variants across `$N$` bins. 

The scaled, weighted averages are calculated like this:

`$ \displaystyle W_{v} = \sum_{i=1}^{N}{w_i F_{v,i}} / \sum_{i=1}^{N}{F_{v,i}} $`

where the weights `$w_i$` are generally given by

`$ w_i = i/N $`

So for example (ignoring scaling for clarity), if 500 cells of a particular variant
go into the sorter, they might end up with 100 in bin 1, 250 in bin 2,
150 in bin 3, and none in bin 4.

The score for this variant would be:
`$$ s = (0.25 \cdot 100 + 0.50 \cdot 250 + 0.75 \cdot 150 + 1.00 \cdot 0 ) / 500 = 0.525 $$`

This makes sense: the majority of counts are in bin 2 (score 0.5) with some 
hanging over each side, and there's slightly more counts in bin 3 than bin 1 so
the score is a little overbalanced to the right, a little bit higher than 0.5.

## Quantization

## Standard Deviation

## Error Detection

|bin1|bin2|bin3|bin4|score|analysis|
|---|---|---|---|---|---|
|100|250|150|0|0.525|typical|
|100|125|100|100|0.525|high sd|
|0|450|50|0|0.525|low sd|
|315|0|5|180|0.525|experimental error?|



