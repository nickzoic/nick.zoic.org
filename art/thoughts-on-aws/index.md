---
category: etc
date: '2011-05-01'
layout: article
redirect_from: '/etc/thoughts-on-aws/'
slug: 'thoughts-on-aws'
tags: aws
title: Some thoughts on AWS
summary: The great EBS Outage of 2011
---

There have been a lot of very interesting articles posted recently about
the cause and effects of the April 2011 AWS outages. This article is an
attempt to tie some of them together.

The Great EBS Outage of 2011
============================

According to Amazon, the outage was caused by:

> **\[... H\]**igh error rates and latencies for EBS calls to these APIs
> across the entire US East Region. **\[...\]** This quickly led to a
> “re-mirroring storm,” where a large number of volumes were effectively
> “stuck” while the nodes searched the cluster for the storage space it
> needed for its new replica.
>
> -- <http://aws.amazon.com/message/65648/>

This is interesting, because this kind of "storm" is an *emergent
behaviour* of a very complex system masquerading as a very simple "block
device":

> The promise of network block storage is wonderful: Take a familiar
> abstraction (the disk), sprinkle on some magic cloud pixie dust so
> that it’s completely reliable **\[...\]** The reality, however, is
> that the disk has never been a great abstraction, and the long history
> of crappy implementations has meant that many behavioral workarounds
> have found their way far up the stack. **\[...\]** It’s commonly
> believed that EBS is built on DRBD with a dose of S3-derived
> replication logic. **\[...\]** Or maybe EBS is indeed bandaids and
> chicken wire. **\[...\]** Do we need block devices in the cloud?
>
> -- [Mark Mayo @
> Joyent](http://joyeur.com/2011/04/24/magical-block-store-when-abstractions-fail-us/)

Indeed, "network block storage" like [EBS](http://aws.amazon.com/ebs/)
is a good example of a ["Leaky
Abstraction"](http://www.joelonsoftware.com/articles/LeakyAbstractions.html):
from the outside, it is a nice simple block device, but in certain
situations it displays rather different behaviour.

(Actually, arguably, even a local block device has leaks in its
abstraction: if ask for block "A" then block "B" then block "C", that
may [take a lot longer](http://en.wikipedia.org/wiki/Elevator_algorithm)
than if I'd asked for block "A" then block "C" then block "B". Unless
you somehow know something about the disk geometry, that's not easy to
predict.)

Two Ways of Looking At AWS
==========================

There are two ways to look at the AWS offerings: either as a hosting
facility with [amazingly quick
provisioning](http://aws.amazon.com/ec2/faqs/#How_quickly_will_systems_be_running)
but [not very reliable
gear](http://www.migrate2cloud.com/blog/resolving-the-degraded-instance-scenario-of-aws-ec2),
or as a [PaaS](http://en.wikipedia.org/wiki/Platform_as_a_service) where
one element of the platform just happens to be an ephemeral but general
purpose Linux box.

EC2 as hosting facility
-----------------------

EC2 nodes come with "ephemeral storage" on board, eg: some local
physical block devices. The problem is, if your EC2 instance does get
reset, the data in these devices is gone for good, and so if you want to
treat EC2 instances like machines in a co-host, you need somewhere else
for the system discs to go. You can put `/tmp` on the ephemeral storage,
but that's about all it is good for.

The usual solution for this is [EBS](http://aws.amazon.com/ebs/). The
EBS volume can be mounted just like a normal block device, written to
like a normal block device, and if your instance dies, you can start a
new instance pointing at that EBS volume and it is equivalent to
rebooting a physical server: you've possibly lost *something*, but
assuming you're using journalling, it is likely recoverable.

Plenty of systems use this method -- including Amazon's own
[RDS](http://aws.amazon.com/rds/) product.

Sadly, however, [EBS latency can be a bit
unpredictable](http://www.reddit.com/r/blog/comments/g66f0/why_reddit_was_down_for_6_of_the_last_24_hours/c1l6ykx)
. Because you're just treating it like a block device, there's no easy
way to deal with this unpredictability: you're stuck waiting for the
device to get back to you. Collecting multiple EBS volumes into a RAID0
actually makes the problem worse, as performance will be degraded if
*any* of the volumes are running slow.

Additionally, if something goes wrong with EBS in a given AZ, and your
instance fails as a result of it, you'll probably try to replace it with
a new instance in a different AZ. To do this, the EBS image must be
"mirrored" across to the new AZ, which takes a lot of bandwidth. If many
systems are doing this at once, this causes the "mirroring storm"
mentioned in the Amazon quote above. This appears to be what caused the
AWS outage to take so long to resolve and why it affected multiple AZs.

EC2 as ephemeral server
-----------------------

On the other hand, if you embrace the ephemeral point of view, you can
dispense with EBS, and put all persistent state into the other
components of AWS instead, such as
[SimpleDB](http://aws.amazon.com/simpledb/) and
[S3](http://aws.amazon.com/s3/). Instances all boot on copies of an
image stashed in S3, maintaining their own local state as they run. If
an instance get hosed --*even if all of them get hosed at once* -- you
can just start up new ones from your image. Instances only use the local
ephemeral discs for caching and such.

By avoiding EBS, this may provide a more reliable service. For example,
Netflix:

> Our architecture avoids using EBS as our main data storage service,
> and the SimpleDB, S3 and Cassandra services that we do depend upon
> were not affected by the outage **\[...\]** One of the major design
> goals of the Netflix re-architecture was to move to stateless
> services.
>
> -- [Netflix Tech
> Blog](http://techblog.netflix.com/2011/04/lessons-netflix-learned-from-aws-outage.html)

All persistent state is still sent across the network, but the level of
abstraction is more appropriate. Instead of block reads/writes you have
requests and responses. This makes it easier to detect and deal with any
slowdown of the AWS internal network, and makes it easier for AWS to
respond to problems. Instead of trying to mirror a "black box" between
AZs, SimpleDB can use more intelligent replication strategies to be
available in multiple AZs at once.

(You may also have to avoid
[ELB](http://aws.amazon.com/elasticloadbalancing/). ELB instance seem to
use EBS for their disks. On the other hand, EBS slowdowns are unlikely
to affet ELB all that much, and it is relatively easy to roll your own
load balancer on an ephemeral server instance in any case.)

Quasi-ephemeral EC2
-------------------

**When is ephemeral storage not ephemeral? When it's redundant.**

The mention of Cassandra above brings up an interesting point: with
sufficient redundancy, the instance ephemeral storage can be used to
host a local database:

> at the moment we run at least 12 Cassandra instances, with replication
> factor of three, and the "RackAwareStrategy" which keeps copies of
> data in each AZ. If we lost instances across zones faster than repair
> could keep up we might lose newly written data. To deal with this we
> have full and incremental backups on each instance, with the data
> being written to S3.
>
> -- [Adrian Cockcroft @
> Netflix](http://techblog.netflix.com/2011/04/lessons-netflix-learned-from-aws-outage.html?showComment=1304134501506#c7311458724072175884)

When [configured in a
RAID0](http://www.gabrielweinberg.com/blog/2011/05/raid0-ephemeral-storage-on-aws-ec2.html),
the local ephemeral storage can offer ["extremely high throughput and an
acceptable random seek
performance"](https://victortrac.com/ec2-ephemeral-disks-vs-ebs-volumes-in-raid.html)
. so this may be an attractive option if SimpleDB is insufficiently
flexible for your needs.

Conclusions
===========

EBS is very popular on AWS because it lets you treat AWS as a hosting
facility. But this negates some of the great advantages AWS has to
offer. AWS took a huge pounding over the recent EBS outages, but EBS is
not all there is to AWS, and by avoiding EBS's "leaky abstraction" you
can get higher reliability and better performance out of AWS.

This quote from Netflix's Tech Blog sums it up nicely:

> We could have chosen the simplest path into the cloud, fork-lifting
> our existing applications from our data centers to Amazon's and simply
> using EC2 as if it was nothing more than another set of data centers.
> However, that wouldn't have given us the same level of scalability and
> resiliency that we needed to run our business. **\[Instead we\]** use
> S3 heavily as a durable storage layer and pretend that all other
> resources are effectively transient.
>
> -- [Netflix Tech
> Blog](http://techblog.netflix.com/2011/04/lessons-netflix-learned-from-aws-outage.html)

Also, I'd like to thanks the authors of Amazon's post-mortems and of all
the articles and blog posts mentioned and otherwise for sharing their
experiences!
