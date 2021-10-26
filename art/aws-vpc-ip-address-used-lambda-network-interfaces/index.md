---
date: '2021-10-26'
layout: article
tags:
  - networks
  - aws
title: 'AWS ... VPCs, IP addresses, Lambdas, Network Interfaces and Security Groups'
---

So this is just a tiny note to mention that if you've got an AWS VPC subnet,
and it seems to be running out of address space even though it's got nothing
much in it but a bunch of Lambda functions, you can find out what's 
using the addresses by going to ...

* NOT the AWS VPC subnet console
* NOT the AWS Lambda console
* NOT whatever other resources you're using
* YES! OF COURSE!  The EC2 Network Interfaces console, even though you have 
  exactly no EC2 instances.

This will actually give you a list of all the things using IP addresses in
your subnet(s).  Lambdas use an IP address per subnet per security group,
because security groups are a IP-level construct like a firewall routing table.

So if each lambda has its own SG then it'll also have it's own IP, even if all
the SGs rules are the same, just in case they change.

So either get yourself some bigger subnets, or share that SG between lambdas.
