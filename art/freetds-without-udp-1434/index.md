---
category: Systems
date: '2011-04-28'
layout: article
redirect_from: '/Systems/freetds-without-udp-1434/'
slug: 'freetds-without-udp-1434'
tags: Systems
title: FreeTDS without udp 1434
summary: a quick note for anyone trying to do FreeTDS through a tunnel or a firewall pinhole
---

Just a quick note for anyone trying to do FreeTDS through a tunnel or a
firewall pinhole or whatever: If you specify an Instance name, FreeTDS
goes and probes UDP 1434 to determine the port number for that instance,
even if you also explicitly specify the TCP port number you want it to
use. The problem being that often that UDP connection won’t get through,
and FreeTDS will just time out with a “Read from SQL server failed”:

~~~
[whatever]
host = whatever.example.com
port = 1433
instance = foo
~~~

This isn’t really documented anywhere, and seems very counterintuitive,
but if you look in the FreeTDS source, there it is in src/tds/login.c:

~~~
if (!IS_TDS50(tds) && !tds_dstr_isempty(&connection->instance_name))
    connection->port = tds7_get_instance_port(tds_dstr_cstr(&connection->ip_addr),tds_dstr_cstr(&connection->instance_name));
~~~

So now you know. If you don’t specify the instance name, it notices that
you’ve specified the port and just goes there directly. Filed it as [a
bug on
FreeTDS](https://sourceforge.net/tracker/index.php?func=detail&aid=3024141&group_id=33106&atid=407806)
just for fun, and they seem to have accepted a patch to:

~~~
if (!IS_TDS50(tds) && !tds_dstr_isempty(&connection->instance_name) && !connection->port)
    connection->port = tds7_get_instance_port(tds_dstr_cstr(&connection->ip_addr),tds_dstr_cstr(&connection->instance_name));
~~~

... which makes more sense to me, but may not have made it into whatever
version of FreeTDS you're struggling with.
