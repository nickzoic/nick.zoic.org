---
category: etc
date: '2014-06-27'
layout: article
redirect_from: '/etc/selfish-secret-logins-without-passwords/'
slug: 'selfish-secret-logins-without-passwords'
title: 'The Selfish Secret: Logins Without Passwords'
tags:
    - crypto
    - backend
    - www
summary: |
    Perhaps instead of looking at cookies as a proxy for passwords, we
    should be looking at passwords as a transport mechanism for secrets!
    The desired result is to share a secret key between the server and one
    or more browsers, and the password is merely a mechanism to prove the
    browser worthy of the secret ...
---

## 1. The Selfish Secret

There's a concept in evolutionary biology called the [Gene-centered view
of
evolution](http://en.wikipedia.org/wiki/Gene-centered_view_of_evolution)
which considers evolution to be best considered from the perspective of
the gene rather than the invidviduals who carry it.

This mental inversion was popularized by [Richard
Dawkins](http://en.wikipedia.org/wiki/Richard_Dawkins) in his 1976 book
[The Selfish Gene](http://en.wikipedia.org/wiki/The_Selfish_Gene).

> We are survival machines -- robot vehicles blindly programmed to
> preserve the selfish molecules known as genes. This is a truth which
> still fills me with astonishment.
>
> -- Richard Dawkins, The Selfish Gene

Rather than thinking of genes as a way of creatures making successive
creatures, you can think of creatures as a mechanism for carrying genes
about. This may seem like a trick of terminology, but it proves helpful
when thinking about the problems of altruism and group selection in
evolution.

It occured to me the other day that the same trick applies to the thorny
issue of internet security, specifically passwords and secrets.

Generally, when communicating with Internet servers, you hand over a
username and password, which are then checked, and your web browser is
issued a "cookie" or a "token" or a "ticket" ... some kind of shared
secret which can be used in lieu of your username/password for the next
little while at least. This avoids having to store or pass around the
password itself with every transaction.

Traditionally, websites tended to use short lived "session cookies", but
these days these shared secrets tend to be longer lived, to avoid having
to remember your password yet again. And passwords are getting more like
shared secrets: most security minded people would recommend using
randomly generated passwords, stored in some kind of password storage
system and locked with a single "master key".

Perhaps instead of looking at cookies as a proxy for passwords, we
should be looking at passwords as a transport mechanism for secrets! The
desired result is to share a secret key between the server and one or
more browsers, and the password is merely a mechanism to prove the
browser worthy of the secret ...

## 2. Logins without Passswords

The mechanism is simple:

1.  If the user arrives with a valid cookie, they're already logged in.
2.  If they user arrives without a valid cookie, have them enter an
    email address.
3.  If that email address isn't known, this is a new user. Make them up
    a new secret. Otherwise, retrieve their old secret.
4.  Send the secret to the email address, in the form of a URL which can
    be followed. Clicking on the URL causes the browser to remember the
    secret as a persistent cookie.
5.  They can connect up more machines / browsers by opening the email
    link with those browsers instead.
6.  To connect devices without email access, the secret can be [entered
    by hand](http://en.wikipedia.org/wiki/Type-in_program), or
    transferred by [QR code](http://en.wikipedia.org/wiki/QR_code).
7.  To protect against losing access to the email account, the email can
    be [printed and stored
    securely](https://www.schneier.com/blog/archives/2005/06/write_down_your.html)
    and the secret can thus be retrieved and used to change the email
    address used.

This of course is just the same sort of mechanism currently used
everywhere to recover passwords, but without a password ever actually
getting a look in. So while there are weaknesses in the security of
doing it this way, they already exist in the password-based schemes more
typically used.

(see also [You've got NO MAIL](/etc/youve-got-no-mail/))

## 3. ... but there's a problem

But there's a problem. Cookies are not really treated as sensitive
information by most browsers, they're just thrown into a file in your
home directory, and even if you have set a Master password, they aren't
encrypted. So unless you're using an operating system which [encrypts
your files by default](https://help.ubuntu.com/community/EncryptedHome)
they may be quite easy to steal.

It would be awfully nice if the browsers would start taking cookie
security a bit more seriously. However, since session cookies are
generally quite long-lived, your sessions weren't really very secure in
the first place, so using passwordless cookies isn't necessarily much
worse.

## 4. UPDATE

I put together a little demo of this principle at
kringle.zoic.org (now defunct), not exactly a high
security application but I thought a nice demo.

I invited a bunch of friends to try it out for our annual "Christmas in
July" party, and it worked pretty well, but interestingly only one
person *noticed* that there was no way to set a password!
