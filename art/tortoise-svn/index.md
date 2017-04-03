---
category: etc
date: '2012-08-22'
layout: article
redirect_from: '/etc/tortoise-svn/'
slug: 'tortoise-svn'
tags: 'windows, svn, revision control'
title: 'Quick guide to setting up TortoiseCVS / TortoiseSVN'
---

[TortoiseCVS](http://www.tortoisecvs.org/) and
[TortoiseSVN](http://tortoisesvn.tigris.org/) are nifty tools for using
[CVS](http://www.nongnu.org/cvs/) and
[Subversion](http://subversion.tigris.org/) from
[Windows](http://microsoft.com/windows/). From time to time I have to
deal with The Beast Of Redmond in its various forms, and this makes it a
lot easier ...

Throughout, this example will refer to `repohost`, meaning the machine
you’ve got the repository on.

PuTTY and Pageant
=================

1.  Install PuTTY
2.  Copy your private key for repohost somewhere
3.  Use PuTTYgen to import your private key and save it as a PuTTY .ppk
    file
4.  Run Pageant and check that you can select that key and put in your
    passphrase and it works.
5.  Run PuTTY and make a session for your repo host:

    -   Host Name: repohost.example.com
    -   Port: 22
    -   Connection&gt;&gt;Data&gt;&gt;Auto-login username: yourlogin

    then put ‘repohost‘ under “Saved Sessions” and hit “save”.
6.  Check that you can open this session now without a password (because
    pageant is caching your private key)

TortoiseCVS / TortoiseSVN
=========================

1.  Install TortoiseCVS and/or TortoiseSVN
2.  From the directory where you want to check out the project, right
    click and select CVS / SVN checkout
3.  Properties:
    -   Protocol “Secure Shell (:ext:)”
    -   Server “repohost“
    -   Repo Folder “/home/cvs” (or whatever)

4.  Then hit Fetch List down on the bottom right, and a list of repos
    should appear. Select the one you want, then OK.
5.  It’ll now create a directory for that repo, you can access CVS/SVN
    commands with right click.

Hope that helps!

There’s also a [TortoiseGit](http://code.google.com/p/tortoisegit/) and
a [TortoiseHG](http://tortoisehg.bitbucket.org/), but I haven’t used
them.

UPDATE
======

It seems that the helpful dialog box used to set up the repo is gone,
and now you just have to enter in a URL. Something like:

    svn+ssh://repohost/home/svn/whatever

seems to work ...
