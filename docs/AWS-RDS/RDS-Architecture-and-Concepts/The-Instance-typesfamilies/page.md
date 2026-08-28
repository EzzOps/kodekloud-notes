# The Instance typesfamilies

Source: https://notes.kodekloud.com/docs/AWS-RDS/RDS-Architecture-and-Concepts/The-Instance-typesfamilies/page

Guide to Amazon RDS instance families and selection, comparing burstable T, general purpose M, and memory optimized R with use cases, monitoring tips, and resizing advice.

Welcome back. Now that you’ve deployed an application and understand how it interacts with a database, this article explains Amazon RDS instance types and how to choose between them. We’ll cover the common instance families, typical use cases, operational trade-offs, and monitoring tips so you can match instance choice to application workload and cost constraints.

## Overview

Amazon RDS provides multiple instance classes optimized for different workloads and resource profiles. The most common families are:

* Burstable performance instances (T classes) — cost-effective for workloads with mostly low CPU usage but occasional bursts.
* General purpose instances (M classes) — balanced CPU, memory, and network; good default for steady workloads.
* Memory-optimized instances (R classes) — for memory-heavy workloads such as in-memory caches or analytics.

Choosing the right family is a balance between performance requirements and cost. Match instance class to your workload pattern (steady vs. spiky vs. memory intensive) and validate with monitoring metrics over time.

## Instance family details

General purpose instances

* Provide balanced CPU, memory, and networking.
* Recommended for moderate and consistent workloads, such as OLTP or small-to-medium web applications.
* Cost-effective when you need predictable capacity across multiple resource dimensions.

Burstable performance instances (T classes)

* Designed for workloads that are mostly idle or low-utilization but occasionally require short CPU bursts.
* Use a CPU credits model: when CPU utilization is below the baseline, credits accumulate; when utilization exceeds the baseline, credits are consumed to permit bursts.
* Best for workloads with unpredictable spikes where sustained high CPU is not common.

Memory-optimized instances (R classes)

* Offer high memory capacity and memory throughput.
* Ideal for large in-memory caches, high-performance databases, and analytics workloads that are memory-bound.

When an application experiences increased traffic and needs more compute, the instance uses accumulated CPU credits to serve that traffic, enabling short-term higher performance without permanently provisioning a larger instance.

<Frame>
  <img alt="A slide titled &#x22;RDS Instances Types&#x22; comparing two instance classes. The left box describes Balanced Performance as a compromise between CPU, memory, and network for apps not receiving heavy traffic; the right box describes Burstable Performance, which accumulates CPU credits during low utilization to use during spikes." />
</Frame>

## Example scenario

Consider a coupon-generation service that normally sees low traffic but experiences large spikes when a campaign launches or when a partner integration triggers many requests. For this workload:

* A burstable instance (T-class) can be economical because it handles short spikes by consuming CPU credits and keeps baseline costs low.
* If the spikes become frequent or prolonged, re-evaluate and consider a general purpose (M) or memory-optimized (R) instance depending on the bottleneck.

## Quick decision table

| Instance family      | Typical use case                        | When to choose                                                              |
| -------------------- | --------------------------------------- | --------------------------------------------------------------------------- |
| Burstable (T)        | Low baseline CPU with occasional spikes | Low-cost option for unpredictable, short spikes; not for sustained high CPU |
| General purpose (M)  | Balanced CPU, memory, network           | Default choice for steady, moderate workloads                               |
| Memory-optimized (R) | Memory-intensive workloads              | Large caches, in-memory DBs, analytics                                      |

## Practical tips for choosing and validating

* Start with the family that matches your workload pattern. Use M for steady workloads, T for low baseline with spikes, and R for memory-bound workloads.
* Monitor these CloudWatch metrics to validate instance sizing:
  * CPUUtilization
  * FreeableMemory
  * ReadIOPS / WriteIOPS
  * DiskQueueDepth / BurstBalance (for burstable storage)
* If your T-class instance frequently runs out of CPU credits and performance degrades, migrate to an M-class or scale vertically.
* Consider storage type and IOPS separately — instance class handles compute and memory; storage choices (General Purpose SSD, Provisioned IOPS, Magnetic) affect disk throughput and latency.

<Callout icon="warning">
  Burstable T instances are not suitable for sustained high CPU workloads. If CPU credits are exhausted repeatedly, you will see degraded performance. Monitor credits and CPU metrics and plan a resize or family change if credits run low.
</Callout>

## Example: list available DB instance classes (AWS CLI)

Use this AWS CLI command to list available RDS instance classes for a specific engine and region:

```bash theme={null}
aws rds describe-orderable-db-instance-options \
  --engine mysql \
  --query 'OrderableDBInstanceOptions[].DBInstanceClass' \
  --output text | tr '\t' '\n' | sort -u
```

Adjust `--engine` to your database engine (postgres, aurora, sqlserver, etc.).

<Callout icon="lightbulb">
  Beyond instance class, tune storage type and provisioned IOPS for I/O-sensitive workloads. Always validate choices with production-like load tests and CloudWatch metrics before committing to long-term provisioning.
</Callout>

## Summary

* Use M for balanced, steady workloads.
* Use T for low baseline, occasional spikes — but monitor CPU credits.
* Use R for memory-intensive workloads with high memory throughput.
* Monitor CloudWatch metrics to validate sizing and catch issues early.

## Links and references

* [Amazon RDS instance classes — AWS Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html)
* [Amazon RDS pricing and instance types](https://aws.amazon.com/rds/instance-types/)
* [Amazon CloudWatch metrics for RDS](https://docs.aws.amazon.[SECRET_REDACTED]-cloudwatch.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/e87c8f86-0a01-4b91-ad95-23e570a8bb2e/lesson/d2156646-db93-4256-9643-83f5d28bb181" />
</CardGroup>
