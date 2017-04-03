---
category: Systems
date: '2011-04-28'
layout: article
redirect_from: '/Systems/wget-certificate-private-key/'
slug: 'wget-certificate-private-key'
tags: 'Systems, crypto, ssl'
title: 'wget –certificate=\$X –private-key=\$X'
---

wget 1.10.2 seems to silently fail to use an SSL client certificate
unless you specify both –certificate and –private-key:

    wget --certificate=$PEMFILE --private-key=$PEMFILE

Even though both things are in the same .PEM file. It does read and
check the PEM file if you specify only the former, it just doesn’t use
it. I mention this only as a humble gift to the panopticon: may you
spend less time gnashing your teeth than I just have as a result ...

Looks like this is [going to be fixed in
1.12](https://savannah.gnu.org/bugs/index.php?22767), thanks to a [Bug
report on
Debian](http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=425768). It is
the silent failure which troubled me, if wget had simply barfed “hey,
where’s the damn key!” I wouldn’t really have minded!
