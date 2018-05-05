---
category: etc
date: '2015-11-17'
layout: article
redirect_from: '/etc/credit-gateway-policy/'
slug: 'credit-gateway-policy'
tags:
    - www
title: Credit Gateway Policies
---

Backstory
=========

[Jack Skinner](https://developerjack.com/) and I were talking at
[BuzzConf](https://buzzconf.io) on the weekend, and it turned out this
is something we've both noticed and been annoyed by.

[He
tweeted](https://twitter.com/developerjack/status/665372154968477697):

> Anyone at \#BuzzConf interested in adding permission scopes to token
> payments and drafting a standard? Hallway track with @mnemote & I tmz?

... but we never got around to actually having the conversation. My
thoughts on the matter don't conveniently fit into 140 character
messages, so I thought I'd post them here instead ...

Credit Card Tokens
==================

[Stripe](https://stripe.com/) and similar credit card gateways have an
API mechanism which allows your site to [save credit card details for
later](https://stripe.com/docs/tutorials/charges#saving-credit-card-details-for-later)
without ever seeing the actual credit card numbers.

You've probably noticed this when you go back to a site for another
purchase, and instead of the normal credit card form you get a little
`Use Visa ending in ...1234?` message ... that's how that works. The
site doesn't know your full details, but it has remembered the existence
of your previous card in the form of a token which it can use to apply
for further payments.

No Limitations
==============

The tokens can only be used by the merchant they were issued to, so
unlike having your actual credit card numbers stolen there's little risk
they can be abused by a third party.

However, there's no particular restriction beyond that. You can be under
the impression that you're paying once for a \$5 micropayment, but that
token can be kept for a lot longer and be billed for a lot larger
amounts, without your knowledge or permission.

A responsible merchant would avoid this like crazy ... credit card
reversals are costly, relatively simple to arrange and would very
rapidly put them out of business. But given the relatively lax
environment of micropayments, there's plenty of scope for abuse or at
the very least nasty surprises. Fluctuating exchange rates, increases in
usage and difficulties terminating contracts can all cause pain and
confusion to the consumer.

And this pain can become pain to the vendor, if the customers *do* get
cross enough to reverse payments. Or if an attacker gains access to the
system and bills every token in the system \$666.66, resulting in a
flood of reversals.

Payment Policies
================

I think what's needed is some kind of policy mechanism. To create a
token, the user passes not just the credit card numbers but also a
policy document which describes the allowed use of the card. When a
merchant goes to use a token, not only are the original card numbers
retrieved but also the policy document, and it is checked against recent
transactions.

For example, a policy document might specify that this merchant can only
bill this card twice a month for up to \$10 each time. Any more than
that, the gateway will refuse the transaction and the payment will have
to be performed with a new token (which can be obtained with the user's
specific approval)

This would work pretty easily in the open-an-iframe-to-the-gateway
method, but how about for more modern sites which do a little AJAX dance
instead? I'd argue that this is still a useful mechanism ... sending a
misleading policy is tantamount to fraud, and in the case of a bad actor
at least the stored tokens will all be limited.

Summary
=======

Including an explicit payment limitation policy in the credit card
tokenization process would protect customers from dubious business
practices and vendors from unnecessary reversals.

All we need to do now is standardize it ...

UPDATE 2016-02-05
=================

We had a (brief) BoF about this at LCA 2016 and a few people will
hopefully be collaborating on
[saferpayments.slack.com](https://saferpayments.slack.com/).
