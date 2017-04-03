---
category: etc
date: '2013-06-10'
layout: article
redirect_from: '/etc/new-static-site/'
slug: 'new-static-site'
summary: 'This site is now created using Pelican and hosted on Amazon S3.'
tags: static
title: New Static Blog Site
---

Up until now I've been running this blog on a homebrewed static blog
site generator I wrote on a whim ... a very minimalist thing based
around 'make', 'rst2html' and some python pickling.

But it made heavy use of
[SSI](http://en.wikipedia.org/wiki/Server_Side_Includes), meaning I was
stuck running my own webserver instead of handing the job off to S3. And
there were a lot of features I'd never got around to implementing!

Then I happened to notice the rather nifty
[Pelican](http://getpelican.com/) which uses a lot of the same basic
ideas but has an active community, themes, and so on. Since it can also
use ReStructuredText, it was a simple process to port all the old
articles across ... all I lost in the process was some metadata such as
the article dates, which I've largely recovered by looking at the
revision history.

S3
==

By the time anyone sees this, it'll be hosted on AWS S3, thanks to the
instructions: [Setting up a blog with Pelican and Amazon
S3](http://lexual.com/blog/setup-pelican-blog-on-s3/), and the builtin
support for S3 in Pelican.

Its unlikely I really need S3 at this point, but there's always the
possibility of some article or another hitting Hacker News or Reddit or
equivalent and frying my poor little web server crispy.

Theme
=====

The theme is based closely on ['subtle' from
pelican-themes](https://github.com/asselinpaul/subtle), and I'm slowly
mutating it towards my idea of happiness.

The wallpaper is from: [Subtle
Patterns](http://subtlepatterns.com/3px-tile/).

"Bitter" and "Source Sans Pro" font suggestion thanks to: [inSquare
Media](http://www.insquaremedia.com/blog/15-web-design-stuff/50-our-favourite-google-font-combinations).

Updates
=======

Finally getting this site looking decent with a few more theme tweaks,
an excessively smartypants error-not-found document and a couple of
[fixes to Pelican's URL
generation](https://github.com/getpelican/pelican/issues/926). Next I
plan to hook into the [LinkedIn Share
API](http://developer.linkedin.com/documents/share-api).
