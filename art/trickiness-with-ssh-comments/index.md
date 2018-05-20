---
category: Systems
date: '2011-04-29'
layout: article
redirect_from: '/Systems/trickiness-with-ssh-comments/'
slug: 'trickiness-with-ssh-comments'
tags:
    - systems
    - ssh
summary: the only useful blog post comments I ever got before I turned them off forever
title: More Trickiness With SSH (Comments)
---

[More Trickiness With SSH](../trickiness-with-ssh/) is my only blog post which has ever
received useful comments, so I'd hate to lose them while converting
files. Hopefully these comments aren't too mangled in transit. Thanks to
the original authors:

Juac Says:
==========

Here is a script that automates the whole process, eliminating the need
to touch config files. I wrote it today impulsed by the amazingness felt
when i knew you could do L2 tunnels with ssh %P. I wish more people were
using this technique, so strange it isn’t more widespread.

Script:

~~~
#!/bin/bash

# prereqs:
# remote host’s sshd_config must have “PermitRootLogin=no”, “AllowUsers user”, and “PermitTunnel=yes”
# “tunctl”, in debians it is found in uml-utils, redhats another (dont remember but “yum provides tunctl” must tell)
# remote user must be able to sudo-as-root
# can opt by routing as in this case or soft bridge with brctl and you get full remote ethernet segment membership :D
# that last i think i’ll implement later as an option
# other stuff to do is error checking, etcetc, this is just as came from the oven

userhost=’user@host’
sshflags=’-Ap 2020 -i /path/to/some/authkey’
vpn=’10.0.0.0/24′
rnet=192.168.40.0/24

# START VPN
if [ "$1" == "start" ]; then
echo setting up local tap …
ltap=$(tunctl -b)
ifconfig $ltap ${vpn%%?/*}2/${vpn##*/} up

echo setting remote configuration and enabling root login …
rtap=”ssh $sshflags $userhost sudo ‘bash -c \”rtap=\\\$(tunctl -b); echo \\\$rtap; ifconfig \\\$rtap ${vpn%%?/*}1/${vpn##*/} up; iptables -A FORWARD -i \\\$rtap -j ACCEPT; iptables -A FORWARD -o \\\$rtap -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -s ${vpn%%?/*}2 -j SNAT –to \\\$(ip r | grep $rnet | sed \\\”s/^.*src \\\(.*\\\$\\\)/\1/g\\\”); sed -i -e \\\”s/\\\(PermitRootLogin\\\).*\\\$/\1 without-password/g\\\” -e \\\”s/\\\(AllowUsers.*\\\)\\\$/\1 root/g\\\” /etc/ssh/sshd_config; /usr/sbin/sshd -t\”‘”
rtap=$(sh -c “$rtap”)

echo setting up local routes …
# since my ISP sucks with transparent filters (i can’t opt for another where i live), i’ll just use my work net as gateway
ip r a $(ip r | grep default | sed “s/default/${userhost##*@}/”)
ip r c default via ${vpn%%?/*}1 dev $ltap

echo bringing up the tunnel and disabling root login …
ssh $sshflags -f -w ${ltap##tap}:${rtap##tap} -o Tunnel=ethernet -o ControlMaster=yes -o ControlPath=/root/.ssh/vpn-$userhost-l$ltap-r$rtap root@${userhost##*@} bash -c “\”sed -i -e ‘s/\(PermitRootLogin\).*\$/\1 no/g’ -e ‘s/\(AllowUsers.*\) root\$/\1/g’ /etc/ssh/sshd_config; /usr/sbin/sshd -t\”"

echo connected.

# STOP VPN
elif [ "$1" == "stop" ]; then
echo searching control socket and determining configuration …
controlpath=$(echo /root/.ssh/vpn-$userhost*)
ltap=${controlpath%%-rtap*} && ltap=tap${ltap##*-ltap}
rtap=${controlpath##*rtap} && rtap=tap${rtap%%-*}

echo bringing the tunnel down …
ssh $sshflags -o ControlPath=$controlpath -O exit $userhost

echo restoring local routes …
ip r c default $(ip r | grep ${userhost##*@} | sed “s/${userhost##*@}\(.*$\)/\1/g”)
ip r d ${userhost##*@}

echo restoring remote configuration …
sh -c “ssh $sshflags $userhost sudo ‘bash -c \”tunctl -d $rtap; iptables -D FORWARD -i $rtap -j ACCEPT; iptables -D FORWARD -o $rtap -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -s ${vpn%%?/*}2 -j SNAT –to \$(ip r | grep $rnet | sed \”s/^.*src \(.*\$\)/\1/g\”)\”‘”

echo deleting local tap …
tunctl -d $ltap

echo disconnected.
fi
~~~

Halil Baysal replies:
=============================================

Hi,

Just a quick reaction to “Juac”, This is a L3 tunneling system. SSH with
-w option that is.

And btw you can even take it a little bit further by,

My Setup:

~~~
    Work Network = 172.16.x.x / Work Computer ( mac-mini ) = 172.16.x.x
    Home Network = 192.168.0.x / Home Server = 192.168.0.10
    ( VPN Network = 10.0.0.x ) Server = 10.0.0.254 / Client = 10.0.0.1
~~~

So i ssh to my server, who has ip-forwarding on, i give my work computer
the ip 10.0.0.1 and my server 10.0.0.254. Now i can communicate with
private L3 scheme with my server at home. I Add to my router the
following static route “ip route 10.0.0.0 255.255.255.0 192.168.0.10 1 ”

If the ssh server isn’ the machine that is doing the routing for you on
the remote network, you must then add a static route on the router so
the packets destined to the vpn-client from your home network know the
route back. This means you can communicate with every other computer on
the remote network. And no, ip-forwarding does not do this.

Because the host on the remote network gets a request from an ip he
doens’t know the path back to on L2, ( your ip from the remote location,
in my case 10.0.0.1, there is no natting ;) since arp is only for the
local configured subnet ) and sends the reply to the default route he
has, to be routed on L3 , because 10.0.0.0 is a different subnet. And
your router sends it back to your server, and your server exactly knows
where the packets should go and you got a fully working vpn. I Can do
natted routing on my work computer with iptables, so that i can reach
not only my workstation at work but every node on the network from home
over the tunnel. But for me this isn’t necessary.

you can now add static routes on your client ( which is my work computer
), which will be tunneled ( encrypted ) to the internet and back from
your home. Meaning if i add specific ip routes to specific sites the sys
admins at work can’t know what i’m doing, they only see encrypted ssh
packets. I also even use the google dns server and also have a static
route for that through the tunnel ( 8.8.8.8 ). DNS requests are open and
unencrypted, everyone with a sniffer can see what you are requesting, so
by statically routing your dns server’s traffic through the tunnel they
also won’t know which sites you are visiting EXCEPT the ones you WANT
them to see which are routed NOT through the tunnel.

Halil Baysal Network Engineer

Juac replies:
=============

Good suggestions, it’s good to have information on routing for other
scenarios.

“This means you can communicate with every other computer on the remote
network. And no, ip-forwarding does not do this.”

I understand this as “setting net.ipv4.ip\_forward=1 does not do this in
itself”, so you have to setup the routing or nat as necessary.

In my case i ssh’ed into a machine that also routes, so i had (after
setting up my local tunnel as gateway for the remote net and snat on the
remote server) full access too. These are all different alternatives.

However, this is what most amazes me: if you use “-w -o Tunnel=ethernet”
ssh does send ethernet packets over a tap device, and if you bridge with
brtcl the tap devices at both endpoint you’ll have full ethernet
bridging over IP (EoIP) more exactly over the ssh tunnel, which is
remarcable to have in ssh and few people knows that ssh+tap+brctl are
capable of that.
