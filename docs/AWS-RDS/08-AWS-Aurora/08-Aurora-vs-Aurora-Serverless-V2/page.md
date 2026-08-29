# Aurora vs Aurora Serverless V2

Source: https://notes.kodekloud.com/docs/AWS-RDS/AWS-Aurora/Aurora-vs-Aurora-Serverless-V2/page

Comparison of Amazon Aurora provisioned versus Aurora Serverless v2, covering architecture, autoscaling, pricing, migration, and guidance for choosing based on workload patterns and operational needs.

Welcome back. This lesson explains the differences between Amazon Aurora (provisioned) and Aurora Serverless v2 to help you choose the right option based on workload patterns, cost, and operational preferences. We cover architecture, autoscaling and capacity management, pricing, migration considerations, and practical guidance for selecting the best fit.

## Overview

* Amazon Aurora (provisioned)
  * You provision DB instances (instance classes) and can scale compute by resizing instances or adding read replicas.
  * Storage autosizes automatically, but compute scaling is typically manual or scheduled unless you automate it.
  * Provides predictable capacity and control—preferred when you need deterministic performance and instance-level configuration.

* Aurora Serverless v2
  * Offers fine-grained, on-demand compute scaling that automatically matches capacity to workload demand.
  * Billing is based on actual consumed capacity (measured in fractional capacity units such as Aurora Capacity Units or equivalent).
  * Ideal for variable, spiky, or unpredictable workloads and teams that prefer reduced operational overhead.

## Feature Comparison

| Feature              | Aurora (provisioned)                        | Aurora Serverless v2                                                |
| -------------------- | ------------------------------------------- | ------------------------------------------------------------------- |
| Compute model        | Provisioned instances (vCPU, memory)        | On-demand, fine-grained capacity (fractional units)                 |
| Scaling              | Manual, scheduled, or custom automation     | Automatic, transparent, near-instant adjustments                    |
| Billing              | Instance-based (full provisioned capacity)  | Usage-based (pay for consumed capacity)                             |
| Best for             | Steady, predictable workloads; full control | Variable/spiky traffic; dev/test; unpredictable workloads           |
| Read replicas        | Supported (Aurora Auto Scaling available)   | Supported (scales compute for writer/reader as needed)              |
| Operational overhead | Higher (capacity management)                | Lower (hands-off scaling)                                           |
| Feature parity       | Full DB engine capabilities                 | Broad parity with provisioned, but verify specific extensions/tools |

## Autoscaling and Capacity Management

Autoscaling is a core differentiator between provisioned Aurora and Serverless v2.

* Provisioned Aurora
  * Compute capacity is tied to DB instance classes and replicas.
  * You control scaling through instance resizing, adding replicas, or automation like [Amazon Aurora Auto Scaling](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-auto-scaling.html) for read replicas.
  * Best when you require predictable throughput, reserved capacity, or fine control over instance configurations.

* Aurora Serverless v2
  * Automatically adjusts compute in fine-grained increments to match workload demand, reducing latency from capacity changes.
  * Removes much of the guesswork in capacity planning and lowers operational overhead.
  * Cost-effective for intermittent or spiky workloads because you pay only for actual usage.

<Frame>
  <img alt="A comparison slide showing features of Aurora versus Aurora Serverless V2. Aurora highlights autoscaling configuration and capacity-based billing, while Serverless V2 emphasizes on‑demand, automated workload monitoring and automatic capacity adjustments for variable workloads." />
</Frame>

## Pricing and Cost Considerations

* Provisioned Aurora
  * Billed by instance class (vCPU and memory) plus storage and I/O; you pay for the full provisioned compute even when idle.
  * Often more cost-efficient for consistently heavy workloads or when using reserved instances.

* Aurora Serverless v2
  * Billed on actual compute capacity used (fractional units) along with storage and I/O charges.
  * Can reduce costs for workloads with variable or low utilization by avoiding payment for idle provisioned instances.

Tips to control cost:

* For provisioned Aurora, use reserved instances or Savings Plans for predictable workloads.
* For Serverless v2, monitor usage patterns and set appropriate min/max capacity to avoid unexpected spikes.

## When to Choose Which

Choose provisioned Aurora when:

* Your workload is steady and predictable.
* You need strict control over instance types, network setup, or specialized configurations.
* You prefer reserved capacity or can optimize costs with long-term commitments.

Choose Aurora Serverless v2 when:

* Workloads are variable, spiky, or hard to predict.
* You want automated, fine-grained scaling and lower operational overhead.
* You’re building prototypes, dev/test environments, or early-stage products where simplicity matters.

> **lightbulb** Aurora Serverless v2 provides near-instant, fine-grained scaling with usage-based billing—great for intermittent or unpredictable workloads. Provisioned Aurora offers more predictable, instance-level control for steady production traffic.

## Other Considerations

* Feature parity: Aurora Serverless v2 has broad feature support, but always validate specific extensions, tools, or networking requirements before migrating.
* Operational model: Serverless v2 reduces capacity-management tasks, allowing teams to focus on application development.
* Migration path: Many organizations move from legacy RDS engines → provisioned Aurora → (evaluate) Serverless v2 once usage patterns and cost/benefit align.

## Quick Decision Guide

| Question                                                                           | If yes — prefer…     |
| ---------------------------------------------------------------------------------- | -------------------- |
| Is traffic steady and predictable?                                                 | Provisioned Aurora   |
| Is traffic spiky, unpredictable, or low-volume most of the time?                   | Aurora Serverless v2 |
| Do you need fine control over instance configuration or reserved capacity pricing? | Provisioned Aurora   |
| Do you prefer a hands-off, usage-based billing model?                              | Aurora Serverless v2 |

## Links and References

* [Amazon Aurora (provisioned)](https://aws.amazon.com/rds/aurora/)
* [Aurora Serverless v2 documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.html)
* [Aurora Auto Scaling (read replicas)](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-auto-scaling.html)
* [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)

## Summary

Selecting between Aurora (provisioned) and Aurora Serverless v2 depends on workload patterns, cost objectives, and operational preferences. Provisioned Aurora is best for predictable, high-throughput production workloads requiring explicit control and instance-level tuning. Aurora Serverless v2 is tailored for variable, spiky, or early-stage workloads that benefit from automated, fine-grained scaling and usage-based billing. Evaluate performance needs, traffic characteristics, and team priorities to choose the optimal model.

I hope this lesson clarified the main differences and use cases for Aurora vs Aurora Serverless v2.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-rds/module/dbfb72c4-207e-424e-ac83-55f55758740a/lesson/e3f04afe-c020-48f9-a5e0-5ca775eb80e0)
