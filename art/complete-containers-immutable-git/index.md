---
category: etc
date: '2016-02-05'
layout: article
redirect_from: '/etc/complete-containers-immutable-git/'
slug: 'complete-containers-immutable-git'
subtitle: Immutable Servers with all their state in Git
summary: |
    I like the idea of ephemeral, immutable servers in light containers but
    what I really want is to put the entire state in a Git repo ...
tags:
    - conference
    - linux
    - systems
    - containers
title: Complete Containers
---

So I've been at [Linux Conf AU](https://linux.conf.au/) all this week
and this is the first of a series of articles based on the ideas
bouncing around there. There's been lots of talk about lightweight
containers and about the ways implement, manage and roll them out, from
the relatively well established [Docker](https://www.docker.com/) to
more far-out things like [Unikernels](http://unikernel.org/) and
[CloudABI](https://nuxi.nl/).

I'm a bit leery of a few of these things -- "Interestingly Wrong" is my
initial feeling --but I feel that it isn't really right to say that
without putting on the table a proposal of my own, so here goes:

1.  Get all your state into Git

    Every bit of state, be it code or config, has to be available in the
    repo so it can all be checked out at once.

2.  All the dependencies too ...

    This is possible using [Git
    Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
    which pull an external repo into a sub-tree of your repo. I haven't
    worked with this myself, and it looks a little fraught ("you must be
    careful or Git will get angry at you"). (( If it turns out submodule
    doesn't really work here, you could always just put all the repos
    side by side )).

    But assuming that the gods smile upon you, you should now submodule
    in every dependency of your project, including languages, libraries,
    webservers, init, the kernel, everything.

3.  Now build that repo

    Your git repo is now the total state of your server.

    You'll need a script which can build everything together into a
    container of some kind. At this point, I'm thinking an
    [LXC](https://linuxcontainers.org/) image.

4.  Boot, test, run, kill.

    These machines are ephemeral and immutable. Don't even bother
    putting opensshd on there. They should pass logging off to a log
    server and they shouldn't write anything back to their filesystems.
    Ephemeral machines are crash-only ... there's no need to turn them
    off carefully.

Right, so there's my modest proposal. As time permits, I'm going to have
an experiment with LXC and see how it works ...
