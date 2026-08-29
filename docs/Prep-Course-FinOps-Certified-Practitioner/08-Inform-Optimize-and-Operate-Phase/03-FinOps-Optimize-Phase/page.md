# FinOps Optimize Phase

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/Inform-Optimize-and-Operate-Phase/FinOps-Optimize-Phase/page

FinOps Optimize phase turning cost visibility into actions to reduce cloud waste, enable real time decisions, set KPIs, and embed continuous cross functional cost optimization

Before diving in: a common misconception is that optimization means endlessly tweaking infrastructure for its own sake. Optimization must be purpose-driven: know why you’re optimizing, what outcome you want, and when the effort is worth the cost.

> **lightbulb** Optimization is the process of turning visibility into deliberate action. Focus on business outcomes and measurable goals rather than continuous micro-adjustments.

The Inform phase (building visibility into cloud spend) is the foundation. The Optimize phase converts those insights into actions that reduce waste, improve unit economics, and align spend to business value. Shift the team mindset from passive monitoring to active response: monitoring describes what happened; optimization changes what happens next. Faster responses to cost signals mean smaller incidents, quicker recovery, and less wasted spend.

<Frame>
  <img alt="The image outlines the &#x22;Optimize Phase,&#x22; consisting of three steps: moving from monitoring to action, making real-time decisions, and eliminating wastes, each with a corresponding icon and number." />
</Frame>

Common, high-impact optimization actions are simple:

* Remove unused resources (orphaned volumes, idle load balancers).
* Rightsize over-provisioned instances and containers.
* Shut down or schedule non-production environments (stale test/dev workloads).

Every eliminated waste item reduces budget pressure and improves margin.

Three primary priorities in the Optimize phase

* Real-time (or near real-time) decisions — act quickly on cost signals so incidents are smaller and recovery is faster.
* Anomaly detection — surface unusual spend or usage (runaway queries, misconfigured batch jobs) and remediate early.
* Spend efficiency — make sure every dollar bought drives measurable business value.

<Frame>
  <img alt="The image shows a diagram with a highlighted &#x22;Primary Focus&#x22; tab, detailing three main points: decisions in near real-time, identifying anomalies, and spending efficiently." />
</Frame>

Core activities (the nuts and bolts)

|                         Activity | Purpose                                           | Examples / Actions                                                                                                                                                                           |
| -------------------------------: | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|            Resource optimization | Reduce wasted capacity and lower unit costs       | Rightsize VMs and containers, tune autoscaling, delete unattached volumes                                                                                                                    |
|                Rate optimization | Lower price per unit by committing or negotiating | Use commitment discounts: [Savings Plans](https://aws.amazon.com/savingsplans/), [Reserved Instances](https://aws.amazon.com/ec2/pricing/reserved-instances/); choose cost-efficient regions |
| Modern architecture & automation | Improve utilization and eliminate recurring waste | Adopt serverless, containers, Spot/Preemptible instances; automate cleanup and retention policies                                                                                            |

<Frame>
  <img alt="The image explains the &#x22;Optimize Phase&#x22; focusing on three core activities: resource optimization, rate optimization, and leveraging modern architectures with automated waste elimination." />
</Frame>

Collaboration and process

Optimization is cross-functional: finance, engineering, and operations must share visibility and responsibility. Make cost reporting part of the operational heartbeat (daily/weekly dashboards, integrated alerts), not just an annual finance exercise. Define clear management processes so optimization becomes continuous practice rather than a one-off project:

* Assign ownership for cost anomalies and remediation actions.
* Run regular cost review cadences aligned with release cycles.
* Embed cost checks in CI/CD pipelines (deployment guardrails).

<Frame>
  <img alt="The image is a flowchart-like diagram titled &#x22;What is the Optimize Phase?&#x22; highlighting three core activities: Visibility, Reporting, and Management Processes, with a focus on Collaboration Element." />
</Frame>

KPIs, OKRs, and measurable goals

You can’t improve what you don’t measure. KPIs create accountability and focus. Example OKR/KPI pairings:

| Goal / OKR                   | Example KPI                                          | Measurement approach                                             |
| ---------------------------- | ---------------------------------------------------- | ---------------------------------------------------------------- |
| Rightsize production compute | Achieve 50% effective discount on production compute | Mix of Savings Plans / Reserved Instances and workload placement |
| Reduce waste in staging      | Decrease idle resource hours by 80%                  | Track scheduled shutdowns and idle metrics                       |
| Improve anomaly detection    | Mean time to detect (MTTD) \< 5 minutes              | Alerts, automated anomaly scoring, and incident logs             |

Use commitment discounts and placement choices to reach rate goals; track utilization and idle time for resource targets.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;Setting KPIs and Measuring Success,&#x22; featuring a real example about an organization setting an OKR for a cloud environment to achieve a 50% discount on compute workloads." />
</Frame>

Ensure you can measure success

1. Measure the baseline and the after-state — record before/after impact for every optimization effort.
2. Identify behaviors that drive outcomes — examples: early anomaly detection, regular cost reviews, deployment guardrails.
3. Set measurable indicators that make progress visible and keep teams motivated.
4. Define outcomes clearly: is success 20% cost reduction, same cost with faster time-to-market, or another metric?

<Frame>
  <img alt="The image is an infographic illustrating steps to ensure organizational success, including defining outcomes, establishing KPIs, measuring accomplishment, and identifying behaviors, represented in a question mark shape." />
</Frame>

An incremental approach

Optimization is a continuous cycle of small improvements. Use a repeatable cadence:

* Review objectives — confirm goals remain relevant.
* Evaluate achievements — what worked, what didn’t.
* Decide — continue, pivot, or stop underperforming strategies.
* Implement changes — automate and repeat.

Small, repeatable improvements reduce risk and create predictable progress.

<Frame>
  <img alt="The image illustrates the &#x22;Incremental Approach&#x22; through a cyclical workflow involving reviewing objectives, evaluating achievement, deciding actions, and implementing changes. It emphasizes small steps and continuous optimization." />
</Frame>

Trade-offs and the iron triangle

Optimization always involves trade-offs. The “iron triangle” (cost, speed, quality) reminds us that saving money at the expense of customer experience or revenue is counterproductive. Make cost decisions that are strategically aligned and ensure accurate cost allocation so teams are accountable.

> **warning** Beware of over-optimizing: aggressive cost cuts that reduce reliability or slow development can harm customer experience and revenue. Always validate trade-offs against business objectives.

<Frame>
  <img alt="The image depicts a pyramid illustrating the &#x22;Iron Triangle and Trade-offs&#x22; in project management, detailing different aspects like cost savings, strategic alignment, the iron triangle (good, fast, cheap), and cost allocation. It conveys the concept of optimization involving trade-offs between cost, speed, and quality." />
</Frame>

Summary

The Optimize phase moves teams from passive observers to proactive cost managers. Act on signals quickly, detect and remove waste, set measurable KPIs and OKRs, and align cost decisions with business goals. This is an ongoing discipline—small, continuous improvements keep cloud spend lean and effective.

<Frame>
  <img alt="The image is a pyramid diagram depicting the Iron Triangle and trade-offs, emphasizing concepts like cost savings, strategic alignment, iron triangle, and cost allocation for effective optimization." />
</Frame>

The FinOps Operate phase embeds these optimization practices into daily operations and makes them part of the organization’s routine.

That is it for this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/5dec4577-7276-4a7a-8040-c172cd00f341/lesson/5ca9a821-59ce-4b24-a570-f80d7403bf6e)
