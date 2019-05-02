---
category: etc
date: '2014-08-21'
layout: article
redirect_from: '/etc/youve-got-no-mail/'
slug: 'youve-got-no-mail'
title: 'You''ve got NO MAIL'
tags:
    - speculation
summary: |
    From the "Ideas I'm Never Going To Implement Myself" bucket:
    
    NoMail is an email service which doesn't store anything. Anything at
    all. Email received by NoMail is ephemeral and exists only in your
    client.
---

If you'd told me a year ago that email was dead, I wouldn't have
believed you. This year, I just might believe it. My mailbox is
perpetually full of notifications from other services and most of my
actual work has moved onto various managed systems ...

Anyway, so here's one from the Ideas I'm Never Going To Implement Myself
bucket.

NO MAIL
=======

NoMail is an email service which doesn't store anything. Anything at
all. Email received by NoMail is ephemeral and exists only in your
client. While you don't have the client open, email sent to your NoMail
address bounces.

NoMail may be useful for a few different things: password recovery,
signing up to overly intrusive services, avoiding contact from humans.
Any sense of security it brings is totally dependant on the server's
willingness to forget things, so it probably isn't a good way to avoid
Echelon.

Logging In
----------

NoMail doesn't have usernames or passwords. It doesn't even remember
which email addresses exist.

Instead, the user just enters in a pass phrase, and NoMail uses a
[KDF](http://en.wikipedia.org/wiki/Key_derivation_function) to calculate
a key. The key is then hashed and used to derive an anonymous email
address using one of the umpteen pronouncable password generation
algorithms.

The key is used by the client to connect to the server and open a
[WebSocket](https://www.websocket.org/) connection over which it can
receive email.

Receiving Email
---------------

When an incoming email arrives at the NoMail server, it first checks if
a matching user is currently connected. It can do this by keeping an
in-memory lookup table of the derived emails of all logged in users.

If the address is not found, it refuses the email. Generally the mail
will then get spooled on the sending server and retried a few times
before giving up and being bounced back.

But if a matching client *is* connected, the NoMail server will accept
the email, and shuttle it straight through to the client on their
Websocket in classic "mbox" format: headers, attachments and all. The
client can then parse the message for display.

(Alternatively, attachments could be removed and stored somewhere
briefly for retrieval over HTTP ... but that seems to defeat the purpose
somewhat)

Sending Email
-------------

The NoMail server can also relay outbound email with DKIM signature etc,
using the derived key. The address can be calculcated from the key, but
the key can't easily be calculated from the address, so knowledge of the
key proves ownership of the email address.
