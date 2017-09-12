---
date: '2017-08-19'
layout: article
tags:
- networking
- iot
title: L2IoT ... IoT Networks without IP
summary: IoT Networks without IP?  Madness.  But ... maybe ...
---

I've already discussed 
["The world in which IPv6 was a good design"](http://apenwarr.ca/log/?m=201708#10)
provides a lot of really good background on the evolution of modern networks too.

Much Ado about Lightbulbs ...
=============================

I've already discussed
[problems with IoT address resolution](/art/mac-address-resolution/)
but I think it's worth questioning a few more assumptions here.

We have [a few problems with IoT](/art/the-internet-of-not-shit-things/)  

* Use of backend services conflates IoT and Big Data.
* ... and dependent on the vendor to keep supporting it.
* Reliance on the Internet makes you dependent on your ISP.
* Crypto support on IoT devices is often very weak.
* No-one is ever going to flash a lightbulb.
* All software sucks.

There's different classes of IoT device, obviously: some devices have
fewer constraints as they have more power available, and perhaps they
are expensive and limited in number enough that putting a decent CPU 
on them isn't a problem.

But let's consider, for this article at least, things like lightbulbs and
lightswitches.  Normally, house mains wiring is quite complicated, with
individual mains wiring run down the walls to each lightswitch, and then
up to each lightbulb socket (or group thereof).  This is time-consuming 
to set up, hard to change once the house is finished, and uses a lot of
mains rated wiring.  In Australia at least, even a circuit with a single
10W LED lightbulb is wired with 8A rated wiring capable of delivering 
a couple of kilowatts.

So, we could replace this whole archaic system with a single circuit
daisy-chaining all the lights together and permanently on, and
battery powered light switches which just stick or velcro to the walls.
No in-wall wiring or big holes in the architraves required.
But now we've got a hell of a lot of devices.  Even in our relatively
modest suburban place there's about 20 switches and 30 light fittings.
Do I really want to give each of them an IP address and deal with its
software upgrades?

A quick review: What happens when I flick a lightswitch
=======================================================

* The lightswitch processor wakes up
* It switches on the WiFi radio
* It sends a DHCP request and/or Address Autoconfiguration messages
  to check that its IP address is still available and waits for confirmation.
* It sends a DNS (or mDNS) lookup for the target address and waits for a reply.
* It connects to the remote server, doing a TCP handshake.
* Now it does an HTTPS handshake (you're using HTTPS, right?), negotiate
  protocols and make up a session key.
* Now it can finally send the HTTP payload, and wait for the HTTP response.
* Now we finally get to go back to sleep.

Not only does all that take a while, it sends many WiFi frames each 
of which costs battery life.

Second Class Devices ...
========================

Sure, it's a nice idea that your lightbulbs are Real Internet Citizens,
but it's holding us back.  There's fundamental differences between a battery
powered lightswitch or temperature sensor and the servers the Internet was
designed to connect together!

Instead, lets allow a gateway, so that IoT devices don't have to do 
everything for themselves.  This could be 
a small piece of software running on your (probably Linux based)
router and using its authentication etc.  Or it could be a standalone 
widget along the lines of an RPi, or a piece of software running on a server
PC.  All it has to do is provide a simple "configuration app" interface.

Each IoT device then relies on it for configuration to provide a gateway
to the internet, and the app can route traffic within the house network.

Layer 2 Addressing
==================

So if our devices aren't Real Internet Computers what are they?

Eliminating DHCP / Duplicate Address Detection
----------------------------------------------

Devices on WiFi (and Ethernet) in general already have a unique address ...
their factory-assigned MAC address.  Sure, they can't use it on the real
Internet, but they can use it within a network segment.
([IPX](https://en.wikipedia.org/wiki/Internetwork_Packet_Exchange) used 
to work this way too, back in the day ...).

Eliminating DNS lookups
-----------------------

The gateway service can use a 
well known [Multicast MAC](https://en.wikipedia.org/wiki/Multicast_address#Ethernet)
to receive notifications from all L2IoT devices, thus no lookups need to be done.

Eliminating TCP handshake
-------------------------

Messages are limited to a single Ethernet frame, so segmentation and reassembly
isn't necessary anyway.  Messages are idempotent, so if they aren't acknowledged,
they can simply be resent.

Eliminating HTTPS handshake
---------------------------

Devices aren't connected directly to the Internet so risks are much reduced, but
there's still a need to protect them from eg: guests on your home WiFi.
Perimeter security is not a good idea!
 
Rather than negotiating session keys, each L2IoT device has a fixed secret key,
which is communicated to the gateway at configuration time.  It can then use this
key to encrypt each message in either direction using an appropriate algorithm.

Eliminating Wakefulness
-----------------------

Devices with limited power need to sleep much of the time, which means they can't
really be expected to respond to requests in a timely manner.  Instead, the
gateway can store-and-forward a single message per device ... when the device
periodically wakes it can request the stored message, respond to it, go back to 
sleep.

Configuring Devices
===================

So, you buy your new lightswitch, take it out of the box, put in a couple of AAA 
batteries.  How do you configure it?

WPS WiFi configuration
----------------------

Joining the WiFi network is easy enough, using pushbutton
[WPS](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Setup).  
If a the L2IoT device has no knowledge of a network on startup, it goes straight
into WPS mode, looking for routers ready to talk to it.

To prevent hijacking, the device must be physically reset before it will return to 
WPS mode and join a new router.

Secret Key Configuration
------------------------

The device comes supplied with a QR code or similar containing the MAC address
and the secret key.  This code is entered into the configuration app to begin
communication with the device, and causes the gateway to send a capabilities
detection message to the device (see below)

(Alternatively, a PIN and key-exchange protocol could be used, but I'm trying
to keep this super minimalist here.  More work necessary?)

Configuration App
-----------------

The app also records a human-readable description for the device
so you can records its purpose or location.  And the app can handle grouping
devices, etc, so that you can gang multiple lightbulbs together to always
have the same brightness, colour temperature, etc.

Capabilities
------------

The devices send a capabilities message explaining what they have to offer, and
the configuration app can then connect the devices together perhaps something like
[Node Red](https://nodered.org/) or [Flobot](/art/flobot-graphical-dataflow-language-for-robots/).
or just plain old Python :-)

Further Work
============

First step is to get raw sockets working on MicroPython and see if I can 
get a demo working on a couple of $1 ESP-01 modules ...
