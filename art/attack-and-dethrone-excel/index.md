---
date: '2023-03-05'
layout: draft
title: 'Attack and Dethrone Excel'
tags:
    - python
    - languages
    - gui
summary: |
    My latest project — CountESS: a visual computing framework for bioinformatics.
---

I've [yakked on about spreadsheets](/art/spreadsheets/) plenty, and issues
like [scientists having to rename human genes to stop Excel from misinterpreting
them as dates](https://www.theverge.com/2020/8/6/21355674/human-genes-rename-microsoft-excel-misreading-dates)
so I'm not going to go into that again here.

And I've spent quite a bit of time talking about and experimenting with
[visual programming](/art/decoding-programming-beyond-text-files/)
because I really do think that it is ridiculous that my code is the same
width as a punched card and my 8 megapixel 32-bit-colour
monitor spends most of its life emulating an array of green screen
[text terminals from 1978](https://en.wikipedia.org/wiki/VT100).

So it is with immense excitement that I can announce that I've been working on
[CountESS](https://github.com/CountESS-Project/CountESS/),
a visual computing framework for scientific computing.

Process files far too large for a spreadsheet and perform library operations in 
[Numpy](https://numpy.org), [Pandas](https://pandas.pydata.org/) and
[Dask](https://www.dask.org) without writing any code.
Plug in specific snippets of Python and R where necessary.
Implement your own data manipulation
plugins and publish them directly to [PyPI](https://pypi.org/).

The project's focus is on addressing some specific problems in bioinformatics,
but for me the mission is much bigger ...

![Attack and Dethrone Excel](img/dethrone.jpg)
*Attack and Dethrone Excel*
