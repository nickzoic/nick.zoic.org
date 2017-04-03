---
category: Languages
date: '2016-04-20'
layout: article
redirect_from: '/Languages/a-canticle-for-diff3/'
slug: 'a-canticle-for-diff3'
tags: Languages
title: A Canticle for Diff3
---

A brief and not necessarily totally accurate history of diff3
=============================================================

`Diff3` is one of the most amazing, historic pieces of software in use
today. It is an amazingly simple idea which changed the way we think
about software. And even most of the people who use it don't really know
much about it ...

![(from [Something
Awful](https://www.somethingawful.com/photoshop-phriday/cutrate-literary-classics/6/)
"Cut-rate Literary
Classics")](%7Cfilename%7C/images/Canticle_Lebowski.jpg)

diff
----

To understand `diff3`, we first must understand `diff`.

`diff` is a pretty simple beast ... given two text files which have a
lot in common, `diff` will extract the differences between them, line by
line, and present the changes in a human-readable format:

    --- old/file
    +++ new/file
    @@ -1,3 +1,4 @@
     this line didn't change
    -this line got changed
    +into this line
    +and this one got added
     this line didn't change either

This is handy because you can see what changed and what didn't.

patch
-----

Even better, the computer can apply these changes, so instead of storing
all of the versions of your document, you can store just the changes.
And that is pretty much the idea behind the original [RCS "Revision
Control System"](https://en.wikipedia.org/wiki/Revision_Control_System)
... store all the changes so you can rewind to an earlier version of
your code, back when it worked properly.

merge
-----

Now it so happens that if two people start off with the same file, and
each makes some changes, they can both make diffs. And if the diffs
don't overlap, you can apply both of them to the original file, and end
up a file with both of their changes in it. ('patch' is clever enough to
use the unchanged lines as 'context', to work out if the matches aren't
quite right. It's pretty neat.)

Pretty handy if there's multiple people all trying to get some work
done. And there we have [CVS (Concurrent Versioning
System)](https://en.wikipedia.org/wiki/Concurrent_Versions_System).

Where the diffs do overlap, there's 'conflicts' ... parts of the patches
will fail, and have to be manually corrected. [Merges don't always
work](/python/syntaxerror-keyword-argument-repeated/) but it's a very
good start.

diff3
-----

'diff' and 'patch' work pretty well, but they don't work all the time.
'[diff3](http://www.cis.upenn.edu/~bcpierce/papers/diff3-short.pdf)'
goes a step further, working around 'diff' and instead taking the three
original files and creating a fourth which merges the changes.

Better merging is better versioning, not just concurrent but
distributed. Better versioning is better development. Better, faster,
more flexible. If you have good versioning you can undo your mistakes,
cherry-pick the good bits, collaborate and review and compare. (You can
even use the word 'Agile' if you must.)

However ...
===========

... I'm not much of a historian and I didn't write all this down just to
rabbit on about the history of revision control, as fascinating as it
is. This is just some background for another idea I'm playing with ...
