# Compute Savings Plans

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/FinOps-Financial-Concepts-Cost-Management/Compute-Savings-Plans/page

Explains AWS Compute Savings Plans, differences versus EC2 Instance plans, usage, procurement and FinOps guidance to model, purchase, monitor, and optimize cost savings.

Welcome — in this lesson we focus on AWS Savings Plans for compute: what they are, how they work, when to use each type, and practical steps for applying them in an organization. If you want to reduce your cloud compute bill without refactoring workloads, Savings Plans are one of the most effective levers available.

What you’ll learn

* What Savings Plans are and how AWS applies them
* Differences between Compute Savings Plans and EC2 Instance Savings Plans
* Practical procurement and FinOps guidance to maximize savings

What are Savings Plans?
Savings Plans let you commit to a steady hourly compute spend (measured in \$/hour) for a 1- or 3‑year term in exchange for lower rates than on‑demand pricing. After purchase, AWS automatically applies the Savings Plan to eligible usage across your accounts — prioritizing the lowest-cost application first to maximize your discount.

Key points:

* You commit to an hourly spend for 1 or 3 years.
* The commitment is automatically applied to eligible usage; no tagging or manual allocation is required.
* Usage above the commitment is billed at on‑demand rates.
* There are two main Savings Plan types with different coverage and discount characteristics.

<Frame>
  <img alt="The image explains how savings plans work, outlining two steps: committing to consistent compute spending and automatically applying to the lowest cost resources first." />
</Frame>

How Savings Plans work (high level)

1. Commit to a consistent hourly compute spend for a 1- or 3-year term.
2. AWS automatically applies the Savings Plan to matching usage across services and accounts, selecting the most cost-effective match first.
3. Any usage beyond the commitment is billed at standard on‑demand rates.

Types of Savings Plans
AWS offers two primary Savings Plan types with distinct trade-offs between flexibility and discount depth.

| Savings Plan Type          |                                     Coverage | Flexibility                                             |    Typical Discount Range | Best use case                                                                             |
| -------------------------- | -------------------------------------------: | ------------------------------------------------------- | ------------------------: | ----------------------------------------------------------------------------------------- |
| Compute Savings Plans      |                     EC2, AWS Fargate, Lambda | High — across regions and instance families             | Up to \~66% off on‑demand | Dynamic or multi‑region workloads, shifting instance families, or cross-service workloads |
| EC2 Instance Savings Plans | Specific EC2 instance family within a region | Medium — within an instance family (sizes, OS, tenancy) | Up to \~72% off on‑demand | Stable, predictable usage in a specific EC2 family and region                             |

<Frame>
  <img alt="The image shows a comparison between Compute Savings Plans and EC2 Instance Savings Plans, highlighting aspects like coverage, flexibility, discount rates, and ideal usage scenarios." />
</Frame>

Practical guidance and recommendations

* Start with Compute Savings Plans when you need broad coverage and minimal operational change. They typically capture the majority of possible savings quickly.
* After several months, re-evaluate usage patterns. If large portions of spend are steady and concentrated in one EC2 instance family and region, layer in EC2 Instance Savings Plans for deeper discounts.
* Use historical cost and usage reports to model commitments. Target commitments to realistic baselines — avoid committing to peak or very spiky usage.
* Monitor two metrics regularly:
  * Utilization: percent of Commitment that is actually used.
  * Coverage: percent of eligible compute spend covered by Savings Plans.
* Combine Savings Plans with other levers (rightsizing, spot instances, instance refresh strategies) to maximize overall savings.

<Frame>
  <img alt="The image describes types of savings plans, highlighting key advantages of automatic optimization across compute portfolios and recommending using Compute Savings Plans for flexibility alongside EC2 Instance Savings Plans." />
</Frame>

> **lightbulb** Start with Compute Savings Plans to capture quick wins and maintain flexibility. After observing usage for a few months, evaluate whether targeted EC2 Instance Savings Plans will deliver incremental savings.

> **warning** Savings Plans are a financial commitment (hourly spend for 1 or 3 years). Regularly monitor utilization to avoid committing to unused capacity.

Applying Savings Plans as a FinOps or engineering practitioner

* Inventory: review compute spend across accounts and identify steady, recurring hourly spend. Use Cost Explorer and detailed billing reports.
* Model: run “what‑if” scenarios using 1- and 3‑year terms and mix of Compute vs EC2 Instance Savings Plans. Report expected savings, breakeven, and utilization sensitivity.
* Procure incrementally: consider phased purchases (e.g., commit 50–75% of steady baseline initially) to reduce risk.
* Operate: add Savings Plan monitoring to your FinOps dashboards. Track utilization, coverage, and unused commitments by account, team, and workload.
* DevOps/SRE actions: prioritize rightsizing and instance family consolidation where possible to make EC2 Instance Savings Plans more effective.

Checklist for implementation

* Collect 3–12 months of compute usage data.
* Identify steady baseline spend and spikes.
* Test models for 1- and 3‑year terms and different commitment sizes.
* Purchase commitments incrementally and monitor utilization.
* Reassess quarterly and rebalance purchases when needed.

Next steps and references

* AWS Savings Plans documentation: [https://aws.amazon.com/savingsplans/](https://aws.amazon.com/savingsplans/)
* Cost analysis and modeling: use AWS Cost Explorer reserved instance/Savings Plans reports.
* For multi-cloud comparison, evaluate GCP Committed Use Discounts: [https://cloud.google.com/compute/docs/committed-use-discounts](https://cloud.google.com/compute/docs/committed-use-discounts)

Thanks for reading — see you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/e2afb350-04ac-4d29-9094-9c32c6ce938e/lesson/a9022431-d3d5-45f7-af6e-cdc1c52fdbf6)
