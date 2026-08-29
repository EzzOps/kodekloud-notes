# TechNova Solutions AWS Cloud Adoption Journey

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/Inform-Optimize-and-Operate-Phase/TechNova-Solutions-AWS-Cloud-Adoption-Journey/page

FinOps guide for TechNova Solutions applying Inform Optimize Operate phases to improve AWS cost visibility, rightsizing, governance, and sustained cloud operations.

Welcome back. This lesson applies the Inform, Optimize, and Operate phases to a real-world FinOps scenario: TechNova Solutions. As the FinOps expert, your mission is to discover where they spend cloud budget, then optimize and operate those resources sustainably.

What follows is a concise, practical walkthrough of TechNova’s environment, challenges, and the phased FinOps approach (Inform → Optimize → Operate) to control AWS costs and improve operations.

## Company overview

TechNova Solutions is a mid-size software firm delivering SaaS products built on AWS. Their objectives are to remain scalable, agile, cost-optimized, and operationally resilient—seeking the best cost-to-service fit across workloads.

<Frame>
  <img alt="The image shows a person sitting on servers with a laptop, accompanied by a cloud icon, and text describing a company overview about a software firm specializing in SaaS products with cloud technologies." />
</Frame>

Primary services in use:

* AWS Lambda
* Amazon RDS
* Amazon S3
* Amazon ECS

Supporting platform components include VPC, EBS volumes, and standard networking / storage services.

<Frame>
  <img alt="The image displays icons and names of AWS services: AWS Lambda, Amazon RDS, Amazon S3, and Amazon ECS, under the title &#x22;AWS Cloud Architecture.&#x22;" />
</Frame>

## Business objectives

* Scalable infrastructure that supports growth
* Agile deployments and faster time-to-market
* Cost-optimized cloud spend
* Operational resilience and security

## Challenges

TechNova faces three core problems that FinOps must solve:

1. Visibility & cost allocation: No clear mapping of spend to teams, products, or environments.
2. Resource allocation & performance: Resources are created freely; many run at low utilization (e.g., 10%) with no corrective action.
3. Operational complexity & security: Over-permissive access and sparse tracking increase governance risks.

Infrastructure-as-code helps reproducibility, but it does not replace continuous monitoring, tagging, and governance.

<Frame>
  <img alt="The image outlines three challenges faced by TechNova Solutions: visibility and cost management challenges, resource allocation and performance issues, and operational complexity and security concerns." />
</Frame>

***

## The FinOps approach (Inform → Optimize → Operate)

Use the following phased approach to move from discovery to sustained cost governance.

| Phase    |                                     Goal | Key activities                                                                            | Example metrics                                   |
| -------- | ---------------------------------------: | ----------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Inform   |           Build visibility and consensus | Create cost dashboards, run stakeholder workshops, define KPIs and tagging policy         | Tag coverage (e.g., 90%), spend per team          |
| Optimize |    Reduce waste and right-cost resources | Rightsizing, Auto Scaling, Reserved Instances / Savings Plans, workload modernization     | % CPU/RAM utilization, monthly savings            |
| Operate  | Institutionalize governance & monitoring | Define roles/processes, run audits, incident & security processes, continuous improvement | Number of governance incidents, sustained savings |

### Inform phase — Build awareness and alignment

Primary goal: make cost and usage visible, and align stakeholders on KPIs and ownership.

Key activities:

* Implement visibility dashboards (AWS Cost Explorer, AWS Billing Console, or third-party tools) to track trends and anomalies.
* Run stakeholder alignment workshops that include CTO, finance, and engineering to agree on KPIs and ownership.
* Define a tagging strategy and remediation policy (target example: tag 90% of resources; review and remediate untagged resources regularly).

Ensure tagging is enforced so costs can be attributed to teams, products, and environments. Agree on a remediation cadence and ownership for untagged assets.

<Frame>
  <img alt="The image depicts a funnel diagram titled &#x22;Inform Phase – Building Awareness and Understanding&#x22; with three sections: Comprehensive Cloud Visibility, Stakeholder Alignment Workshops, and Baseline KPIs and Resource Analysis, each accompanied by brief descriptions." />
</Frame>

### Optimize phase — Reduce waste and lower run costs

With visibility and KPIs in place, apply targeted optimization techniques:

* Rightsizing & Auto Scaling: Match instance sizes to historical utilization and use Auto Scaling to handle variability.
* Reserved capacity / Savings Plans: Buy predictable capacity for steady-state workloads (Reserved Instances, Savings Plans).
* Automation & modernization: Use managed services and automation to reduce operational overhead (e.g., migrate long-running EC2 workloads to managed databases or serverless platforms).

Optimization typically yields immediate savings, but without governance these gains can erode. Make optimization repeatable and measurable.

<Frame>
  <img alt="The image illustrates the &#x22;Optimize Phase&#x22; focusing on enhancing efficiency and reducing costs, highlighting three areas: rightsizing and auto scaling, cost savings with reserved instances, and automation and workload modernization." />
</Frame>

### Operate phase — Sustain and evolve improvements

The Operate phase embeds processes and ownership so optimizations stick:

* Define roles & process flows: Who audits, who remediates, who approves budget/infra changes. Schedule quarterly audits and daily monitoring for anomalies.
* Security & incident response: Triage cost spikes (for example, expected cost 1000 → observed 1600 implies a 600 delta); investigate whether a feature rollout, misconfiguration, or attack caused it and document findings.
* Continuous monitoring & innovation: Evaluate new managed services and features; run POCs and adopt those that demonstrably reduce cost or improve resilience.

<Frame>
  <img alt="The image illustrates three components of sustaining and scaling cloud operations: the objective of the operate phase, security and incident management, and continuous monitoring and innovation." />
</Frame>

> **lightbulb** Continuously measure cost and performance against the KPIs established in the Inform phase. Optimization must be recurring—embedded into daily operations and quarterly reviews—not a one-off project.

> **warning** Automation or modernization without clear ownership and governance will not sustain savings. Always pair automation with accountability, tagging, and audit practices.

## Example: migrating databases (EC2 → Amazon RDS)

A common modernization pattern: migrate a self-managed database on EC2 to Amazon RDS for PostgreSQL.

Benefits:

* Managed backups, patching, and automated failover
* Easier scaling and reduced operational overhead
* Lower long-term operational cost in many cases

Recommended approach:

1. Run a POC to measure operational overhead, recovery point objective (RPO), and total cost of ownership.
2. Validate performance and compatibility.
3. Migrate incrementally and monitor cost/performance post-cutover.

RDS is often a good fit for databases that require standard availability, backups, and lifecycle management without custom OS-level administration.

## Final adoption outcomes

Applying the three phases produces this progression for TechNova:

* Structured adoption: standardized tagging, clear ownership, and meaningful dashboards.
* Operational efficiency: rightsizing, capacity commitments (Reserved Instances / Savings Plans), and targeted modernization reduce recurring costs.
* Sustained operations: governance, monitoring, and a FinOps culture ensure continuous improvement.

All of this is driven by the FinOps team collaborating with engineering, finance, and product stakeholders.

<Frame>
  <img alt="The image presents a flow diagram illustrating a phased approach to AWS cloud adoption, highlighting three key stages: Sustained Operations, Operational Efficiency, and Structured Adoption." />
</Frame>

## Next steps & resources

Apply this pattern to your organization:

1. Start with Inform: build dashboards, agree KPIs, and enforce tagging.
2. Move to Optimize: run rightsizing, scaling, and capacity commitment experiments.
3. Institutionalize Operate: define roles, schedule audits, and embed FinOps into daily work.

Selected references:

* [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
* [AWS Auto Scaling](https://aws.amazon.com/autoscaling/)
* [EC2 Reserved Instances and Savings Plans](https://aws.amazon.com/ec2/pricing/reserved-instances/)
* [Amazon RDS for PostgreSQL](https://aws.amazon.com/rds/postgresql/)

That is it for this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/5dec4577-7276-4a7a-8040-c172cd00f341/lesson/5165ce79-f44d-4312-ad73-ffa274539d13)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/5dec4577-7276-4a7a-8040-c172cd00f341/lesson/d0baabf0-25c6-453e-9587-8e7e3362696b)
