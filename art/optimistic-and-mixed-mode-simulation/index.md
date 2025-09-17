---
date: '2025-09-17'
layout: article
title: 'Optimistic Event Driven Simulation / Mixed Mode Simulation'
tags:
    - networks
    - old-stuff
summary: |
    Two from the lost-to-the-sands-of-time drawer.
---

I was looking at publications recently and realized it's been 20 years since
[RFC4429](https://www.rfc-editor.org/info/rfc4429) and [Virtual Localization](/art/virtual-localization) and the other stuff I was working on at Monash.
The centre I worked for [no longer really exists](https://www.ctie.monash.edu.au/) and
with it went all the technical reports and stuff we wrote which is a shame
really.

So this is work from 2003 or so but since I don't know if it exists anywhere any
more I figured I should write it up from memory.

## Event Driven Simulation

What is an event-driven simulator?

It's a simulator which uses an event queue to work out what to do next.
The event queue is a [priority queue](https://en.wikipedia.org/wiki/Priority_queue),
where events are pushed on with an associated 'time', and the simulator
picks the earliest 'time' event to run next, and that event can push more 
events into the queue.
When the queue is empty, or some predetermined time has elapsed or number of events
have occurred, the simulation stops.

### Network Simulators

Event driven simulators are particularly well suited to simulting communications
networks.
The main network simulator we were using was [OmNet++](https://omnetpp.org/)
although some projects used [opnet](https://opnetprojects.com/opnet-network-simulator/)

### Avoiding Anachronism

Some checks can be added to ensure correctness of the simulation and allow
a little parallelization:

* splitting state into independent nodes
* only allowing one event per node per time
* only allowing events to be added in the future (`event.time > current.time`)

### Time Quantization & Parallel Programming

Time is generally represented as a fixed point value.
Because the speed of light is finite, about a foot per nanosecond, we can be 
assured that an event can't cause an event any sooner than that.

Generally there's only one event which can be run at a time, since if you were
running two events wih different times the earlier one could interpose an event
before the later one, causing anachronisms.
This severely limits the parallelization of simulations across multi CPUs.

### Partitioning

If you know all nodes are at least time `N` apart then you can allow several
events to be processed in parallel so long as they are on different nodes
and are within time `N` of each other.

If our simulation spans large distances, we can partition the problem into 
multiple queues. 

For example, Melbourne and Sydney are 713km apart which at the speed of light
is over 2ms or to put it another way 2,000,000ns.
So we can run multiple partitions, one for each city, each with its own nodes
and queue, and allow the clocks to get up to 2ms out of sync before one has
to wait for other other.

If there's a lot of partitions, we can use a lot of cores.
But there's an organizational overhead to working out which nodes belong to
which queues.

## Optimistic Event Driven Simulation

Imagine we have a simulation of a complex network.
We'd like to use severl CPU cores for the simulation, in parallel,
but our nodes are too close together to effectively partition.
If we have a mechanism to *rewind* events, we can still run
successive events in parallel and just rewind if an anachronism occurs.

We go ahead and optimistically process events from the queue as processors
become available.
Each node has its own state, and we keep a backlog of old states and events.
If an event causes a new event to be scheduled before an event which has already
been processed, we can use this information to rewind the
node to before the new event and replay.
The backlog of states and events can be trimmed as the oldest
clock passes.

A maximum 'window' time can be tuned to get a good amount of parallelization
without too my retrying.
This matters more when the simulation events are "heavy", which brings us to ...

## Mixed Mode Simulation

... another thing I spent some time looking at, "Mixed Mode Simulation".

We were using [User Mode Linux](https://en.wikipedia.org/wiki/User-mode_Linux)
to work on [HMIPv6](https://www.rfc-editor.org/rfc/rfc4140) and
[Optimistic DAD](https://www.rfc-editor.org/rfc/rfc4429) ...
basically because it let us do network development without having to restart the
whole machine, instead the linux kernel and its network stack all ran as a user-mode
process. 
Or processes!  You could run several kernels and have them talk to each other.

The problem with this was that it ran in real time. 
Simulating ten minutes of network traffic took ... ten wall-clock minutes.
During which time the computer was mostly idle.
Unless you were trying to run a really big simulation in which case your
simulated machines maybe couldn't keep up.

Simulating the network between the machines was also very limited.
On the other hand, network simulators generally implemented very simple nodes,
rather than something as complicated as a web request over a TCP/IP stack.

So what I wanted to do was to run some UML instances to model real network
devices, and connect them via a network simulation.
The User Mode Linux clocks would be synced to the network simulator clock and
the UML kernel timer "tick" would be an event in the simulator event queue.

This would require a few changes to the UML timing and the UML network stack.

### Gone without a trace

The only trace I can find of any of this work is from 2002 in this thread about
[using SIGHUP to ctrl-alt-del the UML process](https://sourceforge.net/p/user-mode-linux/mailman/user-mode-linux-devel/thread/20020221180223.F6398%40dwerryhouse.com.au/#msg9365841).

```
I've been playing with virtual networks of UML hosts, and
one thing that's been annoying me is that it's difficult to shut
the network down cleanly. Here's a patch which catches a SIGHUP
to the tracing thread and calls the kernel ctrl_alt_del() procedure.
```
[...]
```
Hopefully something useful should come out of all this mucking around:
I'm setting up IPv6 virtual networks & trying to do simulation and
conformance testing using UML. There's probably a paper in it :-)
```
