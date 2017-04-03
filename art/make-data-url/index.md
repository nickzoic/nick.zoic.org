---
category: etc
date: '2011-07-25'
layout: article
redirect_from: '/etc/make-data-url/'
slug: 'make-data-url'
tags: www
title: 'Making "data" URLs'
---

[data URLs](http://en.wikipedia.org/wiki/Data_URI_scheme)
([RFC2397](http://www.ietf.org/rfc/rfc2397)) allow you to embed small
images and such right into your HTML or CSS and thus avoid the [overhead
of an HTTP
request](http://code.google.com/speed/page-speed/docs/request.html) just
for one tiny 16x16 icon. I think these are a more elegant solution for
small icons than [CSS
Sprites](http://www.alistapart.com/articles/sprites), because they
localize the icons right there in the stylesheet.

There are lots of "online tools" out there, but the process is actually
trivial: a data URL is just a base64 encoding of the file with a label
and a mime-type tacked on the front. So for the Unix-heads among us I
present the following tiny bash script:

``` {.sourceCode .bash}
#!/bin/bash

for filename; do
    mimetype=`file -b --mime-type $filename`
    encoded=`base64 -w 0 $filename`
    echo "data:$mimetype;base64,$encoded"
done
```

It takes one or more files as arguments, and outputs a URL for each, one
per line. It uses the `file` command to determine the MIME type of the
files, and the `base64` command to encode it. You use it like this:

    $ dataurl sort_up.gif sort_dn.png
    data:image/gif;base64,R0lGODlhEAAQALMLAJLNXpDEaZPNX4/NU5bUWJnXWpDNVIvFWXyuWmOPRf///////wAAAAAAAAAAAAAAACH5BAEAAAsALAAAAAAQABAAAAQvcMlJq704612V4ouSJJ8mAgiZnYVwqJY4EsEIU55oAKSHiQNe6We7XXI5kHK5iQAAOw==
    data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAIVBMVEWZ11qQzVSPzVOLxVljj0V8rlr///+W1FiTzV+SzV6QxGnd5+EIAAAAL0lEQVQImWNIgwIG/AwXFyjDaQqU4QhluLgvcQEzUiY0u0GkPEOgalLcCJuMygAAMbUyf2u25M8AAAAASUVORK5CYII=

You can then cut and paste the URLs output by this script into your CSS
like so:

    background-image: url(data:image/gif;base64,R0lGODlhEAAQALMLAJLNXpDEaZPNX4/NU5bUWJnXWpDNVIvFWXyuWmOPRf///////wAAAAAAAAAAAAAAACH5BAEAAAsALAAAAAAQABAAAAQvcMlJq704612V4ouSJJ8mAgiZnYVwqJY4EsEIU55oAKSHiQNe6We7XXI5kHK5iQAAOw==)

or into your HTML like so:

    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAIVBMVEWZ11qQzVSPzVOLxVljj0V8rlr///+W1FiTzV+SzV6QxGnd5+EIAAAAL0lEQVQImWNIgwIG/AwXFyjDaQqU4QhluLgvcQEzUiY0u0GkPEOgalLcCJuMygAAMbUyf2u25M8AAAAASUVORK5CYII=" />

<div style="height: 16px; width: 16px; background-image: url(data:image/gif;base64,R0lGODlhEAAQALMLAJLNXpDEaZPNX4/NU5bUWJnXWpDNVIvFWXyuWmOPRf///////wAAAAAAAAAAAAAAACH5BAEAAAsALAAAAAAQABAAAAQvcMlJq704612V4ouSJJ8mAgiZnYVwqJY4EsEIU55oAKSHiQNe6We7XXI5kHK5iQAAOw==)"> </div>
![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAIVBMVEWZ11qQzVSPzVOLxVljj0V8rlr///+W1FiTzV+SzV6QxGnd5+EIAAAAL0lEQVQImWNIgwIG/AwXFyjDaQqU4QhluLgvcQEzUiY0u0GkPEOgalLcCJuMygAAMbUyf2u25M8AAAAASUVORK5CYII=)

HTTP overhead is something around 500 bytes. Base64 encoding increases
the size of files by 1/3, so using this encoding method is likely to be
worthwhile only on images smaller than 1.5KB or so ... but that is the
case for an awful lot of small icons.
