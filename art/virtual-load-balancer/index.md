---
category: etc
date: '2016-06-08'
layout: article
redirect_from: '/etc/virtual-load-balancer/'
slug: 'virtual-load-balancer'
tags:
  - architecture
  - systems
  - networks
title: a Virtual Load Balancer
---

So I was at [this AWS
meeting](http://www.meetup.com/melbourneaws/events/231457195/) this
evening, and Harvo Jones from the CloudFront group gave an interesting
presentation about failover in CloudFront which got me thinking.

Failover in CloudFront
======================

So, as I understood it [^1], they used to use ARP-spoofing failover to
let machines pinch each other's addresses in case of failure. However,
if Machine A fails, and Machine B takes over ARP and takes all its
traffic, then Machine B may become overloaded in turn, causing a cascade
of failures. So what they did was to spread services across many IP
addresses, to spread the impact of a single failure. However, with the
rise of 'vanity SSL' everyone wants proper IP addresses to call their
own, which doesn't scale with that solution.

So instead they've moved to a BGP based approach, which sounds pretty
cool although I'm a little unclear on the details. I think what they're
doing is pushing BGP routes for each server, and then altering this map
in the case of server failure. Using routing gets around the 1:1 nature
of ARP, which is really clever.

But it requires BGP-capable routers out the front of the network, which
is a potential bottleneck and expense. And something has to update the
routes.

Cross-over Routing
==================

I like ARPish approaches and I have some prior experience with
[manipulating Address Detection](http://tools.ietf.org/html/rfc4429) so
on the way home I had a bit more of a think about this [^2].

-   The solution has to work on unmodified ingress routers, because if
    we're going to go around modifying them we might as well just write
    our own *Multiway ARP* [^3] and be done with it. And in a lo of
    circumstances those routers might be out of our
    administrative control.
-   Higher-layer proxying likewise. Getting the kind of network
    performance we're looking at out of commodity Linux boxes would be
    tricky anyway.
-   On the other hand, the web servers are ours, so we can mess with
    their network stack if we want and change ARPs behaviour.
-   Each 'external' IP address has to be passed through to the servers,
    so they can handle HTTPS-without-SNI.
-   Servers need to fail over in a distributed manner, to avoid the
    failure cascade case.

Routing Tables Revisited
========================

I really like the routing table based approach, because routing tables
offer up a many-to-many relationship where ARP is many-to-one. And
flow-based routing gives us a hashed lookup table for free. What I don't
like is *dynamic* routing tables. So I had a think about this.

Ideally, we wouldn't need any smarts at the router at all. *Most* of the
time, *most* of the servers are going to be available. So lets optimize
for the usual case.

Imagine a server cluster for an external IP range A.B.C.0/24. We've got
254 addresses to serve up, and let's say 6 servers. If we push six
routes, one for each server, and each covering the whole external range,
we'll now get our traffic distributed across all six servers, with
flow-based routing maintaining TCP connections etc.

But if one of the six servers goes down, there's no way to redistribute
those routes without disturbing all the other flows. We could replace
dead server route \#4 with live server route \#3, but now we have an
overloaded server \#3.

So instead, let's make up some more routes. Let's say 30 of them. Each
server now has 5 'primary' internal IP addresses to which the ingress
routers can send traffic. Each server also has 5 'secondary' addresses,
which it is prepared to start serving if one peer fails. Because the
addresses are spread around all the servers, the failover load will also
be spread around.

The following address assignments are arbitrary but illustrative:

    Server   Primary         Secondary
    ======   ==============  =============
    A        1,2,3,4,5       6,11,16,21,26
    B        6,7,8,9,10      1,12,17,22,27
    C        11,12,13,14,15  2,7,18,23,28
    D        16,17,18,19,20  3,8,13,24,29
    E        21,22,23,24,25  4,9,14,19,30
    F        26,27,28,29,30  5,10,15,20,25

Specifically, each of the N(N-1) address has exactly one primary server
and exactly one secondary server, and they aren't the same server. Each
of the N servers has N-1 primary addresses, and N-1 secondary addresses,
and no server has the same address as primary and secondary.

This could be extended to tertiary addresses to handle double failures.
We'd need N(N-1)(N-2) routes & addresses:

    Server   Primary         Secondary      Tertiary
    ======   ==============  =============  =========
    A        1,2             3,5            4,6 
    B        3,4             1,6            2,5
    C        5,6             2,4            1,3

'A' normally responds to address 1 and 2. If 'A' fails, 'B' picks up
address 1 and 'C' picks up address 2. If 'B' fails as well, 'C' picks up
addresses 4, 1 and 3.

This is starting to add up to a lot of routes, especially if N is larger
than 6, but remember that these intermediate addresses don't have to be
'real' internet addresses, they can be private addresses. The only limit
is the size of routing and ARP tables.

ARP Spoofing for Fun and Profit
===============================

So, each of our servers now has multiple tiers of addresses. Primary
addresses it can use as per normal, responding immediately to ARP
requests.

For secondary addresses, the server listens for ARP requests and
responses, and if it doesn't hear another backend 'claim' the address
within a timeout, perhaps a few hundred ms, it figures that the primary
server for that address has failed and claims it instead. The way the
addresses are distributed means that a failure of a single server will
see each of that server's addresses claimed by exactly one other server.

Tertiary (and so on) addresses can have longer timeouts, so if an
address is not claimed by either the primary or the secondary it will
eventually get claimed by the tertiary.

If a server sees another server's ARP response for one of it's
non-primary address, it deconfigures that address, assuming the failed
server is now back in service.

Summary
=======

So, this post proposes a way to do multi-way serving of many IP
addresses with many servers, using only unmodified commodity routers and
no separate load balancer. Only a small amount of modification to the
server IP stack would be necessary.

UPDATE 2016-06-09
=================

I just had a quick squiz at the Linux 4.4.0 sources ... the term
'secondary' (and the flag IFA\_F\_SECONDARY) [^4] is already in use to
mean 'address on the same subnet as another address', so I might need to
change the terminology used above.

But the good news is, the changes required for the above look pretty
simple:

-   create an IFA\_F\_FAILOVER flag (or two)
-   modify the appropriate interface programs like 'ip' to be able to
    set/clear this flag on addresses
-   modify arp.c to implement the primary/secondary/tertiary logic
    described above.
-   Set up your addresses and routes and go bananas.

Drawbacks & Limitations
=======================

-   this is only going to work on a single L2 network, so the servers
    can hear each others' ARP requests & responses.
-   N (number of servers) is limited, because we need approx N\^3
    internal routes. I suspect you'll hit the limits of commodity
    routers before N=10.
-   It's pretty common for servers to be stuck in a state where they
    work fine at a kernel level, so ARP is still okay, but userland is
    not responding. This doesn't help in that circumstance.

[^1]: obDisclaimer: Just a satisfied customer.

[^2]: Perhaps I need to drink less coffee.

[^3]: I also got to squee at the sight of IFA\_F\_OPTIMISTIC there in
    the kernel

[^4]: I also got to squee at the sight of IFA\_F\_OPTIMISTIC there in
    the kernel
