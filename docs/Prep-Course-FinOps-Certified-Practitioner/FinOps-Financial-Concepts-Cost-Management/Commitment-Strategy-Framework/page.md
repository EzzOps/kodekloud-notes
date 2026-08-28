# Commitment Strategy Framework

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/FinOps-Financial-Concepts-Cost-Management/Commitment-Strategy-Framework/page

Framework to reduce cloud costs by analyzing 12 months of usage, classifying workloads, building gradual commitment portfolios, managing risk, and tracking utilization coverage and savings metrics

Welcome back. This lesson explains a practical, repeatable Commitment Strategy Framework you can use immediately to reduce cloud spend. With a disciplined process you can often cut costs by 20–40% (and in some cases more) by choosing the right mix of commitments and on-demand capacity.

Quick overview:

* Establish accurate baselines from historical usage.
* Classify workloads by predictability and risk.
* Build a balanced commitment portfolio (Savings Plans, Reserved Instances, On-demand, Spot).
* Implement commitments gradually with regular reviews and clear exit plans.

## Where to start: Baseline analysis

Start by understanding how your environment actually runs. Committing without reliable baselines is like buying a year-long gym membership before you know how often you'll work out.

Key steps:

* Analyze usage history
  * Pull at least 12 months of historical usage and billing data from your cloud provider (for Azure, see [Azure Cost Management](https://learn.microsoft.com/en-us/azure/cost-management-billing/) and [billing export](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/export-usage-and-charges)).
  * Identify seasonality, recurring patterns, and sustained baselines versus short spikes.
* Identify workloads
  * Separate predictable, long-running production workloads (databases, core web services, analytic clusters) from dev/test, feature branches, and bursty workloads.
  * Mark resources that are safe to commit to (steady-state) and those that should remain on-demand or spot.
* Calculate commitment opportunity
  * For each candidate, compute a reliable sustained baseline (e.g., 95th percentile over a steady period or a verified guaranteed baseline).
  * Translate sustained baseline into Savings Plans / Reserved Instances vs on-demand spend to estimate projected savings.

<Frame>
  <img alt="The image is a diagram illustrating the &#x22;Baseline Analysis&#x22; process with three steps: Analyze Usage History, Identify Workloads, and Calculate Commitment Opportunity. Each step is represented by colored arrows and includes a brief explanation." />
</Frame>

Why this matters

* Committing against verified usage reduces the risk of over- or under-buying.
* Discount programs such as [Azure Reserved Instances](https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/) and [Savings Plans](https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/savings-plans) can produce very large discounts (in some scenarios up to \~72% versus on-demand). That makes a solid baseline analysis highly impactful for cost optimization.

## Designing a compute commitment portfolio

A well-designed portfolio balances discount depth and operational flexibility. Below are common commitment categories and how they’re typically used.

* Savings Plans (flexible commitments)
  * Flexible across machine sizes and regions in some providers/plans.
  * Best for environments that may change instance families but still have steady compute spend.
* Reserved Instances (RIs)
  * Deeper discounts for specific instance sizes/regions/terms.
  * Best for truly stable, long-running VMs or managed databases.
* On-demand
  * Preserves agility for new projects, spikes, and migrations.
* Spot / Preemptible
  * Lowest cost but interruptible—ideal for batch jobs and fault-tolerant workloads.

Example portfolio (illustrative allocation):

| Commitment Type          | Typical Use Case                          | Example Allocation |
| ------------------------ | ----------------------------------------- | ------------------ |
| Savings Plans / Flexible | Evolving VM families with steady spend    | 45–60%             |
| Reserved Instances       | Stable, mission-critical workloads        | 20–30%             |
| On-demand                | New services, seasonal spikes, migrations | 10–25%             |
| Spot / Preemptible       | Batch, CI workloads, fault-tolerant jobs  | 5–10%              |

Note: Percentages vary by organization. Conservative enterprises may bias toward higher RI commitments; startups often keep more on-demand to preserve agility. The important part is intentionality: set targets, implement, and iterate.

## Risk management and implementation timeline

Commitments lower cost but add risk if workloads change. Use a staged, measurable approach:

* Start conservative
  * Only buy commitments for usage levels you are confident in.
  * Avoid speculating on newly changed or recently deployed workloads.
* Phased rollout
  * Spread purchases across months (e.g., 3–6 months).
  * Begin with the most predictable services (databases, core services) and expand as you validate assumptions.
* Review cadence
  * Establish monthly (or more frequent) reviews to validate utilization and coverage.
  * If reserved capacity utilization falls below thresholds (e.g., \~80%), investigate idle instances, topology changes, or opportunity to reassign workloads.
* Exit / transition strategy
  * Budget for migrations (containers, different DB tech) and keep some on-demand capacity to smooth transitions.

<Frame>
  <img alt="The image outlines Step 3 of a Risk Management process, detailing a strategic implementation and review timeline with four stages: Start Conservative, Phase Approach, Review Cadence, and Exit Strategy. Each stage includes a brief description of the actions to be taken." />
</Frame>

<Callout icon="warning">
  Commitments can become sunk cost quickly if left unmanaged. Put automation and alerts in place to surface low-utilization reserved capacity and unexpected topology changes.
</Callout>

<Callout icon="lightbulb">
  Monthly reviews are essential—buying commitments and forgetting them is the fastest route to wasted spend. Use automated reports and dashboards to track utilization and coverage.
</Callout>

## Success metrics — how you know you’re winning

Use these three KPIs together; they form a balanced view of portfolio health:

1. Commitment utilization (target >95%)
   * Percentage of committed capacity actually used.
   * Low utilization (\<50%) usually indicates overcommitment.
2. Coverage ratio (recommended 60–80%)
   * Portion of steady compute spend protected by commitments.
   * Aim for a balance: capture savings without freezing flexibility.
3. Cost optimization (target 20–40% reduction versus all on-demand)
   * The real business outcome: measurable dollar savings compared to baseline on-demand spend.

Interpretation guide:

* High utilization + low coverage → you should buy more commitments.
* High coverage + low utilization → you’re likely wasting money; re-evaluate.
* Balanced coverage + high utilization → optimal state: predictable budgets and strong cost efficiency.

<Frame>
  <img alt="The image shows key success metrics related to cloud computing, focusing on commitment utilization, coverage ratio, and cost optimization. Each metric has specific targets, such as a >95% utilization rate, 60-80% compute coverage by commitments, and a 20-40% cost reduction compared to on-demand pricing." />
</Frame>

## Wrapping up

Commitments are not a gamble when you apply a structured framework:

* Build baselines from at least 12 months of data.
* Classify workloads into commit / on-demand / spot categories.
* Implement commitments gradually and conservatively.
* Monitor utilization and coverage together with a regular review cadence.
* Iterate: start small, measure results, and expand commitments where they demonstrably reduce cost without harming agility.

Start with the lowest-risk workloads, validate outcomes, and expand. With discipline, you can significantly reduce cloud costs, improve budget predictability for engineering teams, and deliver clear savings to finance leadership.

See you in the next lesson.

## Links and references

* [Azure Cost Management](https://learn.microsoft.com/en-us/azure/cost-management-billing/)
* [Azure billing export](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/export-usage-and-charges)
* [Azure Reserved Instances](https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/)
* [Azure Savings Plans](https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/savings-plans)
* [Azure Spot VMs / Preemptible](https://learn.microsoft.com/en-us/azure/virtual-machines/spot-vms)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/e2afb350-04ac-4d29-9094-9c32c6ce938e/lesson/bd955480-276f-44e3-9c9a-b9f0194f84ff" />
</CardGroup>
