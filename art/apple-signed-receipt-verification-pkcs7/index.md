---
category: etc
date: '2015-09-11'
layout: article
redirect_from: '/etc/apple-signed-receipt-verification-pkcs7/'
slug: 'apple-signed-receipt-verification-pkcs7'
summary: |
    Apple uses a signing mechanism for in app purchases, but its behaviour
    is a bit weird. This post outlines how to confirm the validity of
    Apple's receipts in Python.
tags:
  - apple
  - payments
title: 'Verifying Apple''s Signed Receipts'
---

[Apple's receipt signing
mechanism](https://developer.apple.com/library/ios/releasenotes/General/ValidateAppStoreReceipt/Introduction.html)
allows your application to check the validity of an in-app purchase
either locally on the device or on your server.

The receipts are signed with
[PKCS7](https://tools.ietf.org/html/rfc2315) to ensure that they haven't
been forged or tampered with. Therefore your client can just pass them
to the server and the server can validate them and read their content.

Validating using Apple's verifyReceipt API
==========================================

The simplest way for your server to verify that the receipts are valid
is to pass them to Apple's API which verifies the signature validity and
unpacks the
[ASN1](https://en.wikipedia.org/wiki/Abstract_Syntax_Notation_One)
contents into a much friendlier JSON data structure.

The [Receipt Verification
API](https://developer.apple.com/library/ios/releasenotes/General/ValidateAppStoreReceipt/Chapters/ValidateRemotely.html#//apple_ref/doc/uid/TP40010573-CH104-SW1)
seems pretty simple, if a little willfully obscure, but there are some
tricks to using it.

1.  The receipt must be encoded into [Base
    64](https://en.wikipedia.org/wiki/Base64). Apple is fussier about
    Base64 than you might expect. The encoding is the standard one using
    the characters `+` and `/`, however no white space or other
    non-encoding characters are allowed.
2.  The receipt is then bundled up in a JSON document, which is easy
    enough
3.  However, when the receipt is POSTed to the API, it must be send with
    the header `Content-Type: application/x-www-form-urlencoded`, even
    though it is not actually encoded in this way.
4.  If it *is* [URL
    encoded](https://en.wikipedia.org/wiki/Percent-encoding) it won't
    work, because the `+` and `/` characters will be mangled.

This is all a bit strange, and if you make any mistakes you get back one
of these rather opaque error messages:

    {"status":21002}

    {"status":21002, "exception":"java.lang.IllegalArgumentException"}

But after much messing around, I found that the following works:

    import base64
    import json
    import requests

    def send_apple_receipt(receipt_data):
        receipt_base64 = base64.b64encode(receipt_data)
        receipt_json = json.dumps({"receipt-data": receipt_base64})

        response = requests.request(
            method='POST',
            url='https://sandbox.itunes.apple.com/verifyReceipt',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=receipt_json
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise SomeOtherException()

Validating the Receipt with PKCS7
=================================

The above treats the receipt as an opaque blob to be sent to Apple,
which is easy but it does seem a bit daft to use all this fancy crypto
and not even look at what's in it.

Unfortunately the APIs here are a bit weird, so we end up doing things
like wrapping up out PKCS7 receipts in ASCII so that OpenSSL can unwrap
them again ... I'd like to find a better way.

    from pyasn1.codec.der import decoder as decoder
    from M2Crypto import SMIME, X509, BIO
    import base64

    certfile = 'AppleIncRootCertificate.cer'

    def verify_apple_receipt(receipt):

        x509_cert = X509.load_cert(certfile, format=X509.FORMAT_DER)
    
        smime = SMIME.SMIME()
        smime.set_x509_stack(X509.X509_Stack())

        x509_store = X509.X509_Store()
        x509_store.add_x509(x509_cert)
        smime.set_x509_store(x509_store)

        receipt_cooked = (
            '-----BEGIN PKCS7-----\n' +
            base64.encodestring(receipt) +
            '-----END PKCS7-----\n'
        )
        receipt_bio = BIO.MemoryBuffer(receipt_cooked)
        receipt_smime = SMIME.load_pkcs7_bio(receipt_bio)
    
        receipt_asn1 = smime.verify(receipt_smime)
        return decoder.decode(receipt_asn1)

    with open('sandboxReceipt') as fh:
        receipt = fh.read()

    receipt_data = verify_apple_receipt(receipt)
    print receipt_data

What comes out? A parsed ASN1 structure which hopefully resembles the
structure in the Apple docco. On the other hand, perhaps it was easier
just to pass the problem off to Apple ...
