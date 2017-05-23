---
category: Systems
date: '2011-04-28'
layout: article
redirect_from: '/Systems/trickiness-with-ssh/'
slug: 'trickiness-with-ssh'
tags:
    - systems
    - crypto
title: More Trickiness With SSH
---

I saw an article on reddit about [SSH
trickery](http://codytaylor.org/?p=13988). SSH is a very subversive
protocol, able to work around many kinds of unwise security policies.
Here’s a couple more useful things to know.

1. Better Lurking Through .ssh/config-ery.
==========================================

Where you’ve got machines lurking behind other machines, inaccesible
from the Internet, you can add a clause like this to your `.ssh/config`
file:

    Host: lurker
    ProxyCommand: ssh gateway.work /bin/nc %h %p

This causes ‘ssh lurker’ to open an ssh connection to gateway.work, then
use nc (may be called netcat on your system, or you may have to install
it yourself) to connect on to lurker (the %h %p interpolates the target
hostname and port into the proxy command)

2. Reverse Tunnelling
=====================

So you’ve noticed the -L option, right, and you understand that by
running:

    ssh -L 3128:localhost:3128 gateway.home

you are establishing a tunnel home to your proxy server, and you can now
configure your web browser to use `localhost:3128` as its proxy server
to keep your web traffic private.

But did you know this one? Let’s say you’ve got a machine stuck out in
DMZ land and you want to apt-get upgrade the poor thing, pronto. You
can’t access the web from this box: security policy. You can’t access
your internal proxy: ditto. All you can do is ssh into it. Try this:

    ssh -R 3128:proxy.work:3128 dmzbox.work

From your shell on dmzbox, you can now configure the http proxy as
localhost:3128 and start sucking down packages via the reverse tunnel.

3. Tunnel Tunnelling
====================

Every now and then, you need to get control of a box which is sadly
hidden away behind a broken hotel NAT network or some kind of Get Smart
style VPN setup. You can’t even get an ssh in. It’s either read Unix
commands over an international phone line at 3am your time, or train a
pigeon to tap out the following:

    ssh -L 2222:localhost:22 gateway.work

which, when run on the remote box, opens an ssh tunnel back home,
through which you can ssh back into the remote box with ssh -p 2222
localhost

4. ssh tunnels with tap and -w
==============================

There's also a (newish) “-w” option, which turns ssh into a full-on VPN
solution rather than just a port-at-a-time port forwarder.

The useful piece of information which I haven’t seen elsewhere is this:
you don’t need to allow root ssh logins to use it. Instead, you can use
‘tunctl’ to preconfigure tun or tap devices on each end with the -u
option to set their permissions to a non-root user. The easiest place to
do this, on Debian/Ubuntu systems, is in /etc/network/interfaces, for
example, in `host1:/etc/network/interfaces`:

    auto tap9
    iface tap9 inet static
        pre-up tunctl -u nick -t $IFACE
        post-down tunctl -d $IFACE
        address 10.1.9.1
        netmask 255.255.255.0

and in `host2:/etc/network/interfaces`:

    auto tap9
    iface tap9 inet static 
        pre-up tunctl -u nick -t $IFACE
        post-down tunctl -d $IFACE
        address 10.1.9.2
        netmask 255.255.255.0

Now you can ‘ifup’ those interfaces, and then start the VPN by running:

    user@host2$  ssh -o Tunnel=Ethernet -w9:9 host1

And the tunnel will be up and running, without needing to create the
tunnel as root. You could easily take this one further for an automatic
tunnel, setting

Comments
========

This is my only blog post which has ever received useful comments, so
I've [reproduced them here](../trickiness-with-ssh-comments/).
