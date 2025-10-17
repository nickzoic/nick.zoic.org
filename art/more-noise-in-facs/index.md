---
layout: draft
date: '2025-10-17'
title: 'Thinking more about noise in FACS experiments'
tags:
  - bioinformatics
uses_mathjax: 3
---

VAMP-seq[^vamp] and other
[Fluorescence-activated cell sorting (FACS)](https://en.wikipedia.org/wiki/Flow_cytometry#Cell_sorting_by_flow_cytometry) 
based experiments measure cells using fluorescent proteins and then sort them 
into multiple *bins* based on how much they fluoresce.

[^vamp]: Matreyek, K.A., Starita, L.M., Stephany, J.J. et al.
    Multiplex assessment of protein variant abundance by massively parallel sequencing.
    Nat Genet 50, 874–882 (2018).
    doi: [10.1038/s41588-018-0122-z](https://doi.org/10.1038/s41588-018-0122-z)

Cells which are genetically identical are not always sorted into the same bin:
instead there is some "noise" in the system which distributes them across multiple
bins.
Then the distribution of the population across those bins is used to compare the activity
of different cell variants.

This article continues from my
[Quantized Counting Considerations](/art/quantized-counting-considerations) 
article, as I attempt to investigate what the noise in the system is, where it comes from
and how we can model it, with a goal of more accurate variant scoring and 
better detection of experimental error conditions.

## Protocols

## Noise Distributions

* PDF
* CDF

### Uniform

[Uniform](https://en.wikipedia.org/wiki/Continuous_uniform_distribution)

### Normal

[Normal](https://en.wikipedia.org/wiki/Normal_distribution)

### Log Normal

[Log Normal](https://en.wikipedia.org/wiki/Log-normal_distribution)

### Rayleigh

[Rayleigh](https://en.wikipedia.org/wiki/Rayleigh_distribution)

### Pareto 

[Pareto](https://en.wikipedia.org/wiki/Pareto_distribution)

## Possible Noise Sources

### Detector Noise

[Shot Noise](https://en.wikipedia.org/wiki/Shot_noise) 
and [Johnson-Nyquist Noise](https://en.wikipedia.org/wiki/Johnson%E2%80%93Nyquist_noise)
and [Quantization Error](https://en.wikipedia.org/wiki/Quantization_(signal_processing))

### Cell Asymmetry


### Cell Cycle

