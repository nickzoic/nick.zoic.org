---
category: etc
date: '2016-11-29'
layout: article
redirect_from: '/etc/mac-address-resolution/'
slug: 'mac-address-resolution'
summary: 'Why can''t I just ping this widget?'
tags:
    - networks
    - iot
    - c
title: MAC address resolution
---

I've been messing with
[mDNS](https://en.wikipedia.org/wiki/Multicast_DNS) for
[MicroPython](https://micropython.org/) recently, and while mDNS does
what I need it seems rather overblown for what I'm using it for, which
is configuring IoT widgets temporarily so they can be configured
properly over the local network. Specifically, I don't need nice names
or service discovery which is what mDNS is really good at ... I just
want something I can print on a [QR
Code](https://en.wikipedia.org/wiki/QR_code) which will let me find the
device.

Background
==========

MAC Addresses
-------------

Ethernet, WiFi and many other kinds of interfaces are assigned a unique
[MAC Address](https://en.wikipedia.org/wiki/MAC_address) which is used
to identify them on the local network segment. These addresses are
generally assigned at the time of manufacture and barring manufacturer
error are unique.

Link-local Addresses
--------------------

In IPv6 land, this would be easy enough ... use a link-local address
based on the device's MAC address. In IPv4 land, link-local addresses
are [selected at
random](https://tools.ietf.org/html/rfc3927#section-2.1), so you can't
know what address it will have ahead of time. In addition, most networks
are set up to allow DHCP and devices which have received a DHCP address
generally won't have a IPv4 link local address as well.

dnsmasq
-------

This idea is somewhat inspired by
[DNSmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html) which provides
DNS and DHCP services to a network segment. It is capable of handing out
an address to a device with DHCP and then making the registered names of
those devices available on DNS. dnsmasq is very commonly found on
consumer grade routers based on
[BusyBox](https://en.wikipedia.org/wiki/BusyBox).

.local TLD
----------

The [.local TLD](https://en.wikipedia.org/wiki/.local) allows DNS
resolution to resolve names over mDNS. It is a pseudo TLD rather than a
real one, name resolution is done by the DNS client directly using mDNS.
mDNS requires the client to send, and the device to receive, multicast
UDP packets.

Resolving MAC addresses
=======================

A DHCP server receives a DHCP request from a specific MAC address and
responds with an IPv4 address. It is therefore in a position to make a
connection between the two forms of addressing. Where, like in the case
of dnsmasq, it it also a DNS server, it can make this information
available to a client.

.mac TLD
--------

A '.mac' TLD would make this information available. A device
manufactured with address (eg) AA:BB:CC:DD:EE:FF and exposing a web
configuration interface could be labeled with a URL
`http://aabbccddeeff.mac` which can be used to look up what its IP
address is.

When it joins a network, the DHCP server issues it an address ... say
192.168.221.238. When a user enters the .mac URL (perhaps by scanning a
QR code), the client will try to resolve the address by passing it to
the DNS server. The DNS server checks with the DHCP server and can
return a DNS A record for 192.168.221.238 to allow the device to be
contacted in the usual way.

The devices don't have to be on the same link-local network as each
other, so long as they share their DNS/DHCP server and can route packets
at the IP layer.

Implementation
--------------

Implementation in 'dnsmasq' looks trivial, as both DNS and DHCP are
implemented in the one program.

There's already a function `src/lease.c:lease_update_dns()` which calls
`src/cache.c:cache_add_dhcp_entry()` to create DNS entries from DHCP, so
creating one more entry each time shouldn't be a problem. [Time to try
it out!](https://github.com/nickzoic/dnsmasq/tree/feature/mac-tld).

For less integrated DNS/DHCP servers, there'd need to be a mechanism to
pass this information between them. The DHCP server could be set up with
a very limited DNS interface capable of answering queries for .mac
addresses only, and the DNS server could delegate such queries to it.
