---
date: '2019-10-17'
layout: draft
tags:
  - speculation
  - languages
title: 'Much Ado about Spreadsheets'
---

## Background

[Spreadsheets](https://en.wikipedia.org/wiki/Spreadsheet)  have been around a very long time.
Starting off as blank paper ledgers back when [Computers](https://en.wikipedia.org/wiki/Computer_(job_description))
were [Human](https://www.nasa.gov/feature/jpl/when-computers-were-human), they then became
[arguably the first](http://www.bricklin.com/firstspreadsheetquestion.htm)
[Killer App](https://en.wikipedia.org/wiki/Spreadsheet#VisiCalc) for personal computers.

An electronic spreadsheet has a grid of cells, named by column/row coordinates, and each cells can 
be set to just a plain value or to a formula which derives the cell value from other cell values.
Because cell values can depend on other cell values in turn, the spreadsheet forms a kind of 
[visual dataflow language](/art/programming-beyond-text-files/) and thus
[spreadsheets are turing complete](https://www.felienne.com/archives/2974).

[Microsoft Excel](https://products.office.com/en-au/excel)
is ubiquitous in business, adding formatting and charting and multiple sheets per file 
and integration with the rest of the office suite.  Despite its limitations, probably
more useful business work has been done in Excel and its imitators than in all other
languages combined.

It's hard to deny the convenience of using a spreadsheet to manipulate tabular data, as
opposed to editin whatever kind of markup.  Standard unix tools like
[sort](http://www.man7.org/linux/man-pages/man1/sort.1.html) and 
[awk](https://en.wikipedia.org/wiki/AWK) are powerful but
[not easy for beginners](https://likegeeks.com/awk-command/) especially those 
less used to command line programming.

## Issues

However, the standard spreadsheet has some pretty severe problems.
From [botched economic analysis](https://theconversation.com/the-reinhart-rogoff-error-or-how-not-to-excel-at-economics-13646)
to [scrambled genes](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-016-1044-7).

Some issues:

* Types are per *cell*, not per *row* or *column*.  A column could have a whole jumble
  of different typed cells in it.
* Aggregate functions like `SUM()` can easily be incorrectly set up to address a subset of
  rows in a table area, losing important data.
* It's not clear, at first glance, if a cell is a static value or gets its value from a 
  formula.
* Formulae are cut-and-pasted between cells, and its easy to get this wrong.  The
  differences between relative and absolute addresses are subtle and easy to confuse.
* Header rows and columns are not really marked separate from data, so it's easy to 
  accidentally sort them along with the data they're meant to be labelling.
* Presentation information, like fonts and column widths, are jumbled up with formulae
  and with data.  
* Dealing with large amounts (>1Mrows) of data in spreadsheets can be rather slow.

## Some ideas

Back in about 2010 or so I got interested in methods for extracting formulae and data from
spreadsheets into regular code.  A spreadsheet would get imported and each cell treated as
a simple assignment statement like `a10 = a7 + b9;` and the resulting mess could be sorted
into an appropriate order and then executed quickly.
There's a lot of business logic wrapped up in spreadsheets no-one fully understands
any more, and this would be a first step towards converting that into readable logic.

However, the process of extracting the patterns from thousands of formulae scattered
among cells is pretty fraught, and there's no way[1] to differentiate or give names to
variables, constants and labels,so the resulting code is no less of a mess than the original
spreadsheet, really.
Here we are again, [Naming Things](https://martinfowler.com/bliki/TwoHardThings.html).

[1] (There's actually some facilities for naming things built in to Excel, but because
they're pretty well hidden they're not used a lot.)










