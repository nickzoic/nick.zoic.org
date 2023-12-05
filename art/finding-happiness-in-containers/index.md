---
date: '2023-11-23'
title: "Finding happiness in containers"
summary: "Best practices for using containers simply and effectively"
tags:
  - containers
  - systems
  - linux
layout: draft
---

# Finding Happiness in Containers

Quite a few of my recent clients have used [docker containers](https://docker.org/)
to make their lives easier.

This article is a quick summary of what I think are the best ways 
to do so.  Not necessarily the only ways, but 

## State Considered Harmful

Don't containerize anything which has to hold state.

There's ways you can do this, but there's a squillion
[DBaaS](https://en.wikipedia.org/wiki/Cloud_database)
options which will make you happier.
If you're in the [AWS](https://aws.amazon.com/) universe, consider
[RDS](https://aws.amazon.com/rds/) for example.

## Containers, self contained.

A revision of a container should get built they same way every time.

By which I mean, don't have a production build, a test build, etc, etc, where
you pass the configuration into the build process and build the container separately each time.
This is just an opportunity for errors to creep in between testing,
staging and production.

## Environmental Concerns




