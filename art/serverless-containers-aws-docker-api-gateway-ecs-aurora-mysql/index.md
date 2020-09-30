---
date: '2020-09-30'
layout: draft
title: 'Serverless Containers in AWS (with Docker, API Gateway, ECS and Aurora)'
tags:
    - architecture
    - aws 
    - mysql
    - postgres
    - systems
summary: |
    I've quite often wanted to host "stupid toys" based on a Python/Django/Postgres
    stack but having to think about a bunch of Linux VMs really doesn't cheer me 
    up any more.

    So I've been looking into the Serverless options from AWS and here's what I've
    worked out so far ...
---

# An example Docker Container


# Serverless Containers

The 

# AWS Stack

## API Gateway

*I'd never even heard of this service until [FunkyBob](https://twitter.com/BunkyFob) pointed it out on twitter.
Thanks also to [Massimo](https://twitter.com/mreferre) for replying pointing me to this document:
[Field Notes: Serverless Container-based APIs with Amazon ECS and Amazon API Gateway](https://aws.amazon.com/blogs/architecture/field-notes-serverless-container-based-apis-with-amazon-ecs-and-amazon-api-gateway/)*

## Route 53 Service Discovery

You probably know of Route 53 as Amazon's DNS service.

But it's also provides "Service Discovery", allowing internal services to register their availability.

### SRV records

You need to create SRV records as well as A records.  The API gateway needs the SRV records, and if it 
doesn't have them it'll return status 500, `{"message": "Internal Server Error"}`.
If you also log a somewhat more helpful message starting with:

        No target endpoints found for integration arn:aws:servicediscovery:

### Alternative: Load Balancer

## Elastic Container Registry

## Elastic Container Service

## Aurora


