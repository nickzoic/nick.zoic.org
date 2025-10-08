---
title: We've Got A Search Engine At Home
date: '2025-10-06'
summary: "We don't need to stop at $SEARCH_ENGINE, we've got a search engine at home"
tags:
  - www
  - database
layout: draft
---

Everyone uses search engines for everything, all the time. 
I'm totally guilty of this.
Why open up "[python.org](https://python.org/)" and search for
"[multiprocessing](https://www.python.org/search/?q=multiprocessing&submit=)"
when you can just go to a third party search engine and type in "python multiprocessing".
Or have your URL bar do it for you.

But what if you *didn't want to do that*.  
Sometimes people might not want to share their search history with a third party.
There are some search engines which [claim to be private](https://duckduckgo.com/) 
but can you trust that?

Let's get this out of the way up front: One obvious use case is getting away with murder.
That's not a very inspiring thought.
There are other reasons, I promise.
Not everyone wants to share everything with a seller of advertising.
Details of what documents your developers are reading for could be a commercially sensitive,
or a security concern.

## Web Spiders

If this was the 1990s, we'd be talking about writing a [Web Crawler](https://en.wikipedia.org/wiki/Web_crawler).
We'd set up a big server to recursively and repeatedly scan through websites slurping up 
data and we'd feed that into an index and hurrah! VC will surely follow.

This is still a valid way to go about things if you want a specialized search engine 
looking in only selected sites.
I could probably cover 90% of my searches with selected programming and science sites plus
wikipedia, and then just have a link on the results page linking to the usual suspect search engines.

But if we're interested in the *whole* web ...

## CommonCrawl

... thankfully we don't have to do recurse over the whole thing any more.
[Common Crawl](https://commoncrawl.org/) has already done it for us.

[Common Crawl's July 2025 Archive](https://commoncrawl.org/blog/july-2025-crawl-archive-now-available)
already covers 2.42 billion web pages.  It's split into 100,000 "WET" files, each entry of 
which has a URL, headers and plain text.  And these can be freely downloaded,
totalling 6.5 TiB.

Which is, don't get me wrong, a lot.  
But [AAA games are taking up gigabytes](https://www.techspot.com/article/2680-game-install-sizes/)
and 6.5TiB is only a couple of days at 10GBit/s.
Or the files are freely available as a [public S3 bucket](https://commoncrawl.org/get-started)
but of course data tranfer and processing charges apply.

A new archive is released [once a month or so](https://commoncrawl.org/blog) so 
we're limited in our ability to search the latest news but for a lot of applications
that's fine.
Sadly there's no "diff" available so we have to download the whole damned
thing every time.

### WET files

WET files are pretty simple compressed text files which look a lot like a
[HTTP 1.1 persistent](https://en.wikipedia.org/wiki/HTTP_persistent_connection#HTTP_1.1)
connection. The WET file is a subset of the [WARC (Web ARChive) File standard](https://bibnum.bnf.fr/WARC/)

They look like this:
```
WARC/1.0
WARC-Type: conversion
WARC-Target-URI: https://nick.zoic.org/
WARC-Date: 2001-02-03
WARC-Identified-Content-Language: eng
Content-Type: text/plain
Content-Length: 23

content content content


WARC/1.0
WARC-Type: conversion
```
**etc**

Content has been folded, spindled and mutilated into `text/plain` (plain, but Unicode)
and stuck end on end into these files.
Each file is about 65MiB compressed, about 200MiB uncompressed and contains
information on about 24,000 pages.

They're not complicated, but helpfully, there's already a
[python WARC library](https://en.wikipedia.org/wiki/HTTP_persistent_connection#HTTP_1.1)
which makes it easier to let us step through records one at a time:

```
import sys
import warc

for file in sys.argv[1:]:
    with warc.open(file) as fh:
        for record in fh:
            print(record.get('WARC-Target-URI'), record.payload.length )
```

So, overall, we have to parse through 200TiB of data comprising 2.4 billion
web pages, and do something useful with all that.

## Waves of Mutilation

### Languages

Every page in the archive comes with a `WARC-Identified-Content-Language` header
which has one or more languages nominated: these are three letter
[ISO 639-3](https://en.wikipedia.org/wiki/ISO_639-3) codes not the more 
familiar two letter [ISO-639-1](https://en.wikipedia.org/wiki/ISO_639-1) codes,
and not including a country code for region/dialect localization.

Unsurprisingly, `eng` wins the day with runners-up including `rus`, `zho`, `deu`, `spa`, `jpn`, `fra` and `por` and a very long tail of other languages.

Language is pretty important for indexing texts as operations like 
[stopwords](https://en.wikipedia.org/wiki/Stop_word) and 
[stemming](https://www.nltk.org/api/nltk.stem.SnowballStemmer.html)
depend on it.
Multi-language documents are a whole 'nother problem.

### Document Numbering System

One thing we're going to need is a
[document numbering system](https://en.wikipedia.org/wiki/Discordianism#The_Pentabarf)
to allow us to retrieve our files efficiently.
Since there's exactly 100,000 files in the archive, let's try:

`offset_in_file * 100000 + file_number`

This will let us open an WET file, seek directly to the record we want and 
retrieve it immediately.
We can speed up indexing into the gzipped file using
[gztool](https://github.com/circulosmeos/gztool) or using 
something like [BGZF](https://biopython.org/docs/dev/api/Bio.bgzf.html)
or something like [rapidgzip](https://pypi.org/project/rapidgzip/0.0.1/#python-library).

Basically: record the offset of the compressed block, record the offset within the
compressed block.

### Building an Index

## Querying the Index









