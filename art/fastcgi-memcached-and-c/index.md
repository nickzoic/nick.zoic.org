---
category: etc
date: '2013-04-16'
layout: article
redirect_from: '/etc/fastcgi-memcached-and-c/'
slug: 'fastcgi-memcached-and-c'
summary: |
    Mostly, getting stuff done fast in the web world requires doing things
    in parallel. However, every now and then you bump into a problem where
    this just doesn't work ...
tags: 'memcached, C, backend, python, tornado, atomic'
title: 'FastCGI and Memcached, all in C'
---

Mostly, getting stuff done fast in the web world requires doing things
in parallel, and splitting the problem up so that *this guy* doesn't
have to wait for *that guy*. However, every now and then you bump into a
problem where this just doesn't work.

Imagine you have a bunch of sequential tickets to hand out. Tickets in
the lucky dip, seats on the lifeboat, whatever. Normally, to make the
process faster, you'd allocate `N` processes, make each of them
responsible for `1/N` of the tickets, and off you go. However in this
case just imagine that it is important that the tickets are handed out
in order. Since our `N` processes aren't waiting for each other, one can
lag behind the others, and that's not fair.

There's no way around this, we're just going to have to have, somewhere
in the stack, an atomically incrementing counter.

In the following discussion I'm assuming two things:

-   We're going to have to deal with tens of thousands of overlapping
    inbound HTTP connections, as measured by the rather useful
    [ApacheBench](http://httpd.apache.org/docs/2.2/programs/ab.html).
-   If the server dies part way through the ticket issuing frenzy, so be
    it, as long as everything is logged.

Python / Tornado
================

My first approach was to use [Python](http://python.org/) and
[Tornado](http://www.tornadoweb.org/). The ticket counter just lives in
a global variable `ticket_number`, and whenever there is a request it
gets incremented and returned. Pretty simple:

``` {.sourceCode .python}
#!/usr/bin/env python

import sys

import tornado.web
import tornado.httpserver
import tornado.template


ticket_number = 0

class TicketHandler(tornado.web.RequestHandler):

    def get(self):

        global ticket_number

        ticket_number += 1

        self.finish("ticket number %010d" % ticket_number)

handlers = [
    (r"/$", TicketHandler),
]

def main():
    portnum = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    application = tornado.web.Application(handlers, template_path="template")   
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(portnum)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
```

It's also pretty quick, right up until you try to handle thousands of
simultaneous connections, at which point performance tapers off rapidly.
The problem is, there's no way to expand it ... if you fire up another
process, it gets its own `ticket_number`.

FastCGI / Memcached
===================

The amount of CPU time spent incrementing that counter is dwarfed by the
amount spent negotiating TCP handshakes, handling HTTP protocol options,
writing log files, etc. And really, if we want to get this thing moving
along, we shouldn't be doing all that in Python anyway.

[Nginx](http://nginx.org/) and [FastCGI](http://fastcgi.com/) to the
rescue. Nginx is a fast and reliable asynchronous HTTP server with
support for various protocols, including FastCGI. FastCGI is a very
simple improvement to the original
[CGI](http://en.wikipedia.org/wiki/Common_Gateway_Interface), allowing
many requests to be handled by each process. It has good library support
in all sorts of languages, including
[C](http://en.wikipedia.org/wiki/C_(programming_language)).

To get the best performance out of Nginx, we're going to end up with a
pool of worker processes running, about one per CPU core. And each of
those will be maintaining a pool of FastCGI daemons to handle its ticket
requests. So how do we get all these processes to handle one atomic
counter? One way would be to use shared memory and locks, and we might
get to that eventually, but for the moment I'd rather piggyback off
someone else's hard work.

[Memcached](http://memcached.org/) has done that hard work. It comes
with [increment/decrement
methods](http://docs.libmemcached.org/memcached_auto.html) which allow a
memcache record to act as an atomic counter. It also has a rather simple
C API, so it is easy to write a small piece of C to join FastCGI to
Memcached:

``` {.sourceCode .c}
// Based on http://www.fastcgi.com/devkit/doc/fastcgi-prog-guide/ch2c.htm

#include <fcgi_stdio.h>
#include <stdlib.h>
#include <libmemcached/memcached.h>


char key[] = "tick";

int main(int argc, char **argv)
{
    const char *mc_config = "--SERVER=127.0.0.1:11211 --BINARY-PROTOCOL";
    memcached_st *mc_handle = memcached(mc_config, strlen(mc_config));
    memcached_return rc;

    uint64_t ticket_number;

    while (FCGI_Accept() >= 0)   {

        rc = memcached_increment_with_initial(mc_handle, key, sizeof(key), 1, 1, 0x7FFFFFFF, &ticket_number);

        if (rc != MEMCACHED_SUCCESS) {
            printf("Status: 500 Server Error\r\n\r\nMemcache %d %s\r\n", rc, memcached_strerror(mc_handle, rc));
        } else {

            printf("Content-type: text/plain\r\n\r\nticket number %010d\r\n", ticket_number);
        }
    }

    return 0;
}
```

Using this method, my laptop was able to handle a hundred thousand
connections in ten seconds, which isn't too shoddy, and well and truly
fast enough to handle my original problem.

Nginx Module
============

It turns out that (I think since I originally wrote this code and
started on this article) someone has actually gone to the bother of
writing a [Nginx Memcached Module supporting
INCR](http://wiki.nginx.org/HttpMemcModule#incr_.24memc_key_.24memc_value).
I'll have to do some benchmarking, but frankly this is likely to be a
winner just because there are fewer moving parts.

Another option would be a Nginx module which uses shared memory and
locking to maintain the counter across the nginx processes. This would
be very fast, but would restrict the ticket issuer to a single machine.

Queueing
========

Another approach I think is really interesting is to use
[Mongrel2](http://mongrel2.org/) or the [Nginx 0MQ
module](https://github.com/FRiCKLE/ngx_zeromq) to just have the web
server queue requests, and then set up a single process to "own" the
ticket counter, answering queued requests as fast as it can.
