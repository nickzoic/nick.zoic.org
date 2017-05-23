---
category: etc
date: '2015-10-02'
layout: article
redirect_from: '/etc/universal-authenticator/'
slug: 'universal-authenticator'
tags: crypto
title: Universal Authenticators
---

I was checking out of my hotel the other day, fumbling a
[magstripe](https://en.wikipedia.org/wiki/Magnetic_stripe_card) hotel
door key, a [proximity car
key](http://www.toyota.com.au/rav4/features/technology/keyless-entry)
and a wallet full of [Paywave
RFID](http://www.visa.com.au/cardholders/paywave/) cards, and it occured
to me that we're really doing this key thing all wrong.

*Would it not be nice if I could just have one device to do all of these
things?*

The proliferation of these devices is because each of them is
Authenticating *and* Authorizing me to use that particular system. How
about if we split these two jobs and let the key do the authentication
while the lock handles the authorization.

Devices
=======

Humans are not good at performing complex cryptographic operations in
their heads, so we'll still need to carry some kind of
[exobrain](http://www.urbandictionary.com/define.php?term=Exobrain)
around with us. This could be a smartphone app, or it could take the
form of a keytag, necklace,
[ring](http://www.javaworld.com/article/2076641/learn-java/an-introduction-to-the-java-ring.html),
brooch, [implant](https://en.wikipedia.org/wiki/Alien_implants),
whatever. You'd only need to carry one of them, so the sartorial options
are less limited than with the current proliferations of cards and keys.

Privacy
=======

The problem with systems like this is that at present, using my wallet,
I can choose which card(s) to hand over for a given situation. I don't
want to just have a single fixed identifier which is handed over to
anyone who asks, but neither do I want to have to set up a shared-secret
relationship with every possible user of the card system.

Prototyping
===========

Regular RFID tags won't do this, but it is possible to [make a DIY RFID
tag](http://scanlime.org/2008/09/using-an-avr-as-an-rfid-tag/) and thus
[customize the RFID
protocol](http://www.nycresistor.com/2012/12/27/rfid-multipass/) so this
should actually be practical.
