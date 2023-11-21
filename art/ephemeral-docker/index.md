---
title: 'Ephemeral Docker'
tags:
  - linux
  - containers
date: '2023-11-21'
summary: "How to run docker in an ephemeral filesystem (for fun and profit)"
layout: "article"
---

## Problem

[Docker](https://docker.org/) is mighty handy for development
but there's three issues I've bumped into a lot:

1. Old images take up a vast amount of disk space which you
   forget to clean out, even if they're quite small images you
   end up with a lot of them, and then it takes forever to 
   `docker system prune` them away.

2. Builds use up a huge amount of disk
   [IOPS](https://en.wikipedia.org/wiki/IOPS)
   which slows your builds down especially if you have whole
   disk encryption on `/var/lib/docker`, which most people
   probably don't, which brings me to ...

3. Sometimes images, layers or volumes contain stuff they shouldn't,
   often accidentally, and those end up hanging around in
   the probably not encrypted l`/var/lib/docker` for far longer
   than they should.

## Solution

1. Buy a whole lot of RAM, perhaps 64 GB or whatever you can fit in your computer.

2. Purge any old images / containers, they're probably in `/var/lib/docker`.

3. Add this to your `/etc/fstab` to create a 16 GB RAM filesystem:

        tmpfs /tmp/ramdisk tmpfs rw,nosuid,nodev,size=16G 0 0

   Mount this volume with `mount /tmp/ramdisk`
   (it'll automatically remount at restart).

4. Tell docker to write its stuff there by creating `/etc/docker/daemon.json`,
   or adding this clause to it if it already exists:

        { "data-root": "/tmp/ramdisk/docker" }

   Docker will create that directory when it starts.

5. Restart docker using `service docker restart`.

## Result

You've now got all of docker's shenanigans saved under `/tmp/ramdisk/docker`,
which will cease to exist when you power down or reboot, greatly reducing the
risk of insecure information being left laying around.

The ramdisk is limited to 16 GB (see step 3 above) which is plenty for a bunch of small 
containers, if your containers are bigger than that you are, in my opinion,
doing it wrong.

Enjoy your faster and more secure container builds, and remember, running out 
of disk space is the systems way of reminding you to run `docker system prune`
more often.
