---
date: '2019-04-14'
layout: article
tags:
  - c
  - games
summary: |
    Never send a human to do a machine's job
title: DOOM Git Gud
---

If Nightmare mode is not enough of a challenge for you, you'd better just git gud:

[DOOM Git Gud](https://github.com/nickzoic/doom-git-gud/)

Possibly the dumbest thing I've actually bothered to do based on a joke tweet:

[![tweets](img/tweeters.png)](https://twitter.com/nickzoic/status/1115793964844507136)

This patch to Chocolate Doom challenges you to really stretch yourself 
by having the enemies actually shoot straight (and expresses its distaste
if you pick any other option):

![Screenshot 1](img/screenshot-1.png)

I was originally intending to patch the enemies' movement code to 
have them behave less stupidly than directly walking into fire,
but it turns out that just removing the randomization code which
causes them to rarely shoot straight is probably enough ...

```
-    angle += P_SubRandom() << 20;
+    angle += (gameskill < sk_gitgud ? P_SubRandom() << 20 : P_SubRandom() << 16);
```

![Screenshot 2](img/screenshot-2.png)

