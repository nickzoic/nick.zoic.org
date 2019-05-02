---
category: Systems
date: '2013-04-11'
layout: article
redirect_from: '/Systems/pseudo-ca/'
slug: 'pseudo-ca'
tags:
    - systems
    - crypto
    - ssl
title: 'Make your own Client-side Certificates with a Pseudo CA'
summary: |
    I've used this authentication method on a couple of different client
    projects so far, so I thought it might be useful to write up a quick
    explanation of how it works.
---

Client-side Certificates
========================

The webserver can be configured to ask for a client-side certificate,
for example in apache:

    SSLCACertificateFile /the/trusted-ca.crt
    SSLVerifyClient optional
    SSLVerifyDepth 1

or in nginx:

    ssl_client_certificate /the/trusted-ca.crt;
    ssl_verify_client optional;

Pseudo-CA
=========

It is important to note that the CA certificate used for doesn't have to
be in any way related to the CA which issued the server-side
certificate. It doesn't even have to be trusted by anyone but us! So we
can make up our own CA certificate, self-sign it, and use that:

    #!/bin/bash
    # Generate and self-sign a pseudo-CA certificate

    openssl genrsa -out pseudo-ca.key 1024
    openssl req -batch -new -key pseudo-ca.key -subj "Pseudo CA" | \
        openssl x509 -req -days 3650 -out pseudo-ca.crt -signkey pseudo-ca.key

Issuing client-side certificates
================================

You can do this with a shell script:

    #!/bin/bash
    # Generate and sign a client certificate

    NAME="$1"
    SERIAL=`date "+%s%N"
    KEYFILE=`tempfile`
    CRTFILE=`tempfile`

    openssl genrsa -out $KEYFILE 1024
    openssl req -batch -new -key $KEYFILE -subj "$NAME" | \
    openssl x509 -req -sha1 -CA $pseudo-ca.crt -CAkey $pseudo-ca.key -set_serial $SERIAL -days 3650 -out $CRTFILE
    openssl pkcs12 -in $CRTFILE -export -clcerts -inkey $KEYFILE -name "$NAME" -passout pass: -out $NAME-sa.p12

    rm $KEYFILE $CRTFILE

But creating tempfiles is a bit ugly, so I'd rather do it in Python
using the OpenSSL library:

    #!/usr/bin/env python

    import sys
    import OpenSSL
    import time
    import datetime
    import pytz

    with open("pseudo-ca.key", "r") as fh:
        ca_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, fh.read())
    with open("pseudo-ca.crt", "r") as fh:
        ca_crt = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, fh.read())

    def create_certificate(common_name, serial_number):

        key = OpenSSL.crypto.PKey()
        key.generate_key(OpenSSL.crypto.TYPE_RSA, 1024)
    
        x509 = OpenSSL.crypto.X509()

        subj = x509.get_subject()
        subj.countryName = 'AU'
        subj.organizationName = 'zoic.org'
        subj.commonName = common_name

        x509.set_issuer(ca_crt.get_subject())
        x509.set_pubkey(key)
        x509.set_serial_number(serial_number)

        now = datetime.datetime.now(tz=pytz.UTC)
        sooner = now - datetime.timedelta(days=1)
        later = now + datetime.timedelta(days=3650)

        x509.set_notBefore(sooner.strftime("%Y%m%d%H%M%SZ"))
        x509.set_notAfter(later.strftime("%Y%m%d%H%M%SZ"))

        x509.sign(ca_key, 'sha1')

        p12 = OpenSSL.crypto.PKCS12()
        p12.set_privatekey(key)
        p12.set_certificate(x509)
        p12.set_ca_certificates([ca_crt])    
        return p12.export(passphrase="")

    common_name = ' '.join(sys.argv)
    serial_number = time.time() * 1000000
    print create_certificate(sys.argv[0], sys.argv[1])

Either way, you've just created a new client-side certificate for your
user. All you've got to do is serve it up to the user with the
appropriate MIME type, and the user should be able to install it!

Problems
========

Sadly, both the clients who tried to use client-side certificates had
problems. [Older Android phones don't support client-side
certificates](https://code.google.com/p/android/issues/detail?id=11231#c107),
and fail silently. Many PC users struggle to understand them, which is
not great surprise since the way they are stored in the OS is confusing
and not universal across browsers. Lastly, users have little idea how to
keep their certificates safe, often using no keychain password or a very
poor one.

Unfortunately, client-side certificates are caught in a bit of a
chicken-and-egg situation: OS support is poor, so they never really
caught on, and because they never really caught on, OS suppport is poor.
Which is a pity, because they have great potential for eliminating
passwords and for preventing SSL MITM attacks.
