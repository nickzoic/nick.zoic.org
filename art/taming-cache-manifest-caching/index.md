---
category: HTML5
date: '2011-09-22'
layout: article
redirect_from: '/HTML5/taming-cache-manifest-caching/'
slug: 'taming-cache-manifest-caching'
tags:
    - html5
    - mobile
title: 'Taming "cache.manifest" Caching'
---

HTML5 apps can use [Cache
Manifests](http://www.w3.org/TR/html5/offline.html#manifests) to
configure the browser's Application Cache, allowing faster startup of
HTML5 apps and also offline operation.

There is a problem, however. The behaviour of cache manifests can make
development [a smidge
tricky](http://diveintohtml5.org/offline.html#debugging) . This is
because the browser will only check if the contents of the Application
Cache have changed if the Cache Manifest has changed. You can manually
edit this file every time, but you'd probably rather not.

So here's some alternatives:

1. Updating `cache.manifest` using a "Go Live" script
=====================================================

If you stage your code to a development server using a "Go Live" script,
you can update the `cache.manifest` contents whenever the files
contained in it change.

This script uses [sed](http://en.wikipedia.org/wiki/Sed), and
illustrates the approach:

``` {.sourceCode .bash}
#!/bin/bash

DATETIME=`date +%Y-%m-%d\ %H:%M:%S`

sed -i -e "s/^#DATE.*/#DATE $DATETIME/" cache.manifest
```

This looks for comment lines starting with `#DATE` and fills in the
current date. The `-i` option causes sed to modify the original file.

Whenever you run the script, the manifest file is updated, and since
files are reloaded [unless the cache.manifest is byte-for-byte
identical](http://www.w3.org/TR/html5/offline.html#downloading-or-updating-an-application-cache),
the changed comment is enough to cause it to reload.

2. Dynamic `cache.manifest` using SSI
=====================================

If your web server supports [Server Side
Includes](http://en.wikipedia.org/wiki/Server_Side_Includes), you can
use them in a similar way to make a dynamic cache manifest. SSIs are
usually used to make dynamic HTML, as suggested by their formatting, but
there's no reason they can't be used for other types of document:

    CACHE MANIFEST
    # <!--#flastmod file="index.html"-->
    # <!--#flastmod file="whatever.js"-->
    # <!--#flastmod file="whatever.css"-->
    whatever.js
    whatever.css

The tactic is the same: the ''flastmod'' directive inserts the last
modification time of the file, so changing any of those files will cause
the comments in the cache.manifest to change, and that will cause the
browser to reload the files.

In Apache, the configuration looks something like this:

``` {.sourceCode .apache}
Alias /whatever /var/www/whatever
<Directory /var/www/whatever>
     Options +Includes
     AddHandler server-parsed .manifest
</Directory>
CacheDisable /whatever/ihealth.manifest
```

You are, of course, paying a penalty in terms of server overhead: the
server has to `stat` several files, and always returns the entire
cache.manifest in a `200` reply rather than returning a `304`. But this
is quite possibly a worthwhile tradeoff in a lot of situations.
