# AWS RDS Storage

Source: https://notes.kodekloud.com/docs/AWS-RDS/RDS-Architecture-and-Concepts/AWS-RDS-Storage/page

Guide to Amazon RDS storage types, behavior, use cases, performance tradeoffs, and selection guidance for General Purpose SSD gp2 gp3 Provisioned IOPS and legacy magnetic storage

In this lesson we cover Amazon RDS storage types, how they behave, and which workloads each is best suited for. Choosing the right storage affects latency, throughput, cost, and long-term scalability for your relational databases on AWS.

RDS storage options are generally grouped into three categories:

* General Purpose SSD
* Provisioned IOPS SSD
* Magnetic (legacy)

Below we explain each type, typical behavior, common use cases, and selection guidance.

## General Purpose SSD (GP)

General Purpose SSD volumes are designed to balance cost and performance. They are a common choice for development, testing, and small- to medium-sized production workloads.

Key characteristics:

* Cost-effective for many database workloads where ultra-low latency isn’t required.
* Flexible and suitable for backend services, small to medium databases, and development/test systems.
* Historically (`gp2`) these volumes provided a baseline of `3 IOPS/GiB` and could burst to higher IOPS when I/O credits were available.
* Newer generation (`gp3`) lets you provision IOPS and throughput independently of volume size, enabling better cost-performance optimization. See the EC2/EBS volume types docs for details: [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)

Typical use cases:

* Medium-traffic web apps and backend services
* Development, staging, and smaller production databases
* Workloads where predictable but not extreme IOPS are sufficient

> **lightbulb** If you need more predictable IOPS or higher throughput without increasing storage size, consider `gp3` (when available for your RDS engine/region) to provision IOPS and throughput independently of capacity.

## Provisioned IOPS SSD (IO)

Provisioned IOPS (PIOPS) SSD volumes are built for I/O-intensive applications that demand consistent low latency and predictable throughput. You explicitly provision the IOPS required to meet your performance SLAs.

Key characteristics:

* Designed for high I/O database workloads and critical production applications that require low latency and steady performance.
* You provision the IOPS level separately from storage size, enabling consistent throughput for transactional systems.
* Typical RDS constraints include a minimum size (commonly 100 GB) and a maximum (often up to 16 TB); limits vary by engine and region—check the latest AWS RDS documentation: [https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)

Typical use cases:

* High-traffic transactional databases (e.g., e-commerce checkout systems)
* Latency-sensitive production workloads requiring predictable performance
* Databases where burst capacity is insufficient and steady IOPS are mandatory

## Magnetic (Legacy)

Magnetic storage (HDD-based) was one of the original RDS storage types. It offers lower cost per GB but significantly lower IOPS and higher latency compared to SSD options.

Key points:

* Uses HDD technology, providing lower cost per GB at the expense of latency and IOPS.
* Largely phased out in favor of SSDs due to SSD cost-efficiency and superior performance.
* Typically not available when creating new RDS instances in most regions and engines.

> **warning** Magnetic storage is legacy technology and has been phased out for most new RDS deployments. For any new instance, prefer SSD options (`gp2`/`gp3` or Provisioned IOPS) to ensure better performance and long-term support.

## Quick comparison

| Storage Type                        | Best For                                                 | Cost Profile                           | When to Choose                                                                   |
| ----------------------------------- | -------------------------------------------------------- | -------------------------------------- | -------------------------------------------------------------------------------- |
| General Purpose SSD (`gp2` / `gp3`) | Moderate workloads, development, small–medium production | Mid-range cost                         | Most general-purpose databases where balanced cost and performance are needed    |
| Provisioned IOPS SSD (`io`)         | High-traffic transactional DBs, latency-sensitive apps   | Higher cost (provisioned IOPS)         | Mission-critical production workloads requiring predictable, low-latency I/O     |
| Magnetic (HDD)                      | Legacy, archival or extremely cost-sensitive cold data   | Lowest cost per GB, lowest performance | Generally avoid for new deployments — only for legacy or very specific use cases |

## Selection guidance

* Use General Purpose SSD (`gp2`/`gp3`) for most moderate workloads and environments where cost and decent performance are balanced.
* Use Provisioned IOPS for production, high-throughput, or latency-sensitive applications where predictable performance is required.
* Avoid Magnetic storage for new deployments; migrate legacy instances to SSDs where possible.

Practical tips:

* If your workload spikes occasionally and can tolerate short bursts, `gp2` may be sufficient.
* If you require consistent performance regardless of storage size, prefer `gp3` or Provisioned IOPS and provision IOPS/throughput explicitly.
* Monitor metrics (IOPS, latency, throughput) via Amazon CloudWatch to validate that your chosen storage meets performance targets, and adjust storage type or IOPS as necessary.

## Summary

* General Purpose SSD (`gp2` / `gp3`): Good balance of cost and performance for many workloads; `gp3` supports independent provisioning of IOPS and throughput.
* Provisioned IOPS (`io`): Built for I/O-intensive, latency-sensitive production databases that need predictable performance. Typical RDS size range is commonly 100 GB–16 TB (verify per engine/region).
* Magnetic: Legacy HDD-based storage with lower performance; generally not recommended for new deployments.

Choose the storage type that matches your workload’s performance profile and budget:

* Use General Purpose for most moderate workloads.
* Use Provisioned IOPS for high-performance, production, or latency-sensitive systems.
* Avoid Magnetic for new deployments.

## Links and references

* [Amazon RDS Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
* [EBS Volume Types (gp2/gp3) — AWS EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)
* [AWS CloudWatch — Monitoring RDS Metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-rds/module/e87c8f86-0a01-4b91-ad95-23e570a8bb2e/lesson/bbce7821-5c7c-47ff-9ab6-9a086da4c0b0)
