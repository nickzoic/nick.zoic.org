---
layout: draft
title: 'Yeast Thoughts (2)'
date: '2025-10-20'
summary: 'Simulating Yeast Growth (for fun and profit)'
tags:
  - bioinformatics
  - simulation
uses_mathjax: 3
---

This article continues on from [Yeast Thoughts](/art/yeast-thoughts/), where I
discuss an experiment on the human *G6PD* gene using a yeast model, and talk
about about the math required to analyse the results of the experiment.

## Simulation

It's possible to model some of the expected behaviours mathematically[^matus]
but the maths gets pretty complicated so I thought it might be worth considering
how to *simulate* the yeast population instead.

[^matus]: Matuszewski S, Hildebrandt ME, Ghenu AH, Jensen JD, Bank C.
    A Statistical Guide to the Design of Deep Mutational Scanning Experiments.
    Genetics. 2016 Sep;204(1):77-87.
    doi: [10.1534/genetics.116.190462](https://doi.org/10.1534/genetics.116.190462).
    Epub 2016 Jul 13. Erratum in: Genetics. 2025 Mar 17;229(3):iyaf002.
    doi: [10.1093/genetics/iyaf002](https://doi.org/10.1093/genetics/iyaf002).
    PMID: 27412710; PMCID: [PMC5012406](https://pmc.ncbi.nlm.nih.gov/articles/PMC5012406/).

Rather than dealing with a bunch of equations for population, maybe we can get away with
thinking of the population at any given time as a vector of counts, so 

### Parameters

Let's start by replicating the *G6PD* work in simulation.  This is all going to be pretty
back-of-the-envelope but hopefully it'll give us a similar shape of output to our real experiment,
and allow us to consider what effect changes in the experiment would have on the quality of
the output.

The library includes about 2 hundred thousand (2 × 10<sup>5</sup>) barcodes for 

The turbidostat holds about a billion (1 × 10<sup>9</sup>) yeast cells at any moment, and dilutes the population
constantly to keep them multiplying without limit.  

At each sample, about 2 million (2 × 10<sup>6</sup>) sequences are taken.

