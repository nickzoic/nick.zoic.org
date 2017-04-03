---
category: etc
date: '2011-04-28'
layout: article
redirect_from: '/etc/hyperterminal-eats-ascii-lf-0x0a/'
slug: 'hyperterminal-eats-ascii-lf-0x0a'
tags: 'windows, protocols, rs232'
title: 'Hyperterminal “send text file” eats ASCII LF / 0x0A'
---

I stumbled across this problem because I was reading a protocol document
for a device connected by RS-232. The document described what bytes to
put in a text file, and how to use Hyperterminal’s “send text file” to
send them. That all worked great. But as soon as I tried to get it
working in C\#, nothing nada zip. Unfortunately, “Line Feed” (ASCII LF,
0x0A) was one of those bytes.

This problem is mostly suffered by people trying to use Hyperterminal to
send files to, eg: a microcontroller. But it looks like I’m not the only
one to have stumbled upon this one: just try searching for ["11 0d 0a 44
4d"](http://google.com/#q=%2211%200d%200a%2044%204d%22)

The document specifies it, hyperterminal eats it, and when my code
actually sent it the device just ignores the whole message ... Leave it
out and bingo! The message, no longer corrupt, produces a response.
What’s really odd is this: the device, when it replies, uses CRLF as its
line separator. This raises the horrible suspicion that the alleged
developers of this protocol wanted to send CRLF, found themselves
stumped by Hyperterminal, and just gave in and changed the
implementation instead of changing the protocol or using an non-broken
client ...

(if only it was a blood-pressure meter, that’d come in handy about now
...)
