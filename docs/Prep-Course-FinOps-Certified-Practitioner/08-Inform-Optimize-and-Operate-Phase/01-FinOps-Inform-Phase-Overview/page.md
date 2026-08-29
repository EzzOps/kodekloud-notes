# FinOps Inform Phase Overview

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/Inform-Optimize-and-Operate-Phase/FinOps-Inform-Phase-Overview/page

Guide to the FinOps Inform phase, establishing cloud cost visibility, tagging, allocation, reporting, and iterative processes to enable data-driven financial decisions and continuous optimization.

Welcome back.

In this lesson we cover three central FinOps phases—Inform, Optimize, and Operate—with a focus on how to adopt each phase across your organization using the FinOps framework. This page drills into the Inform phase: why it matters, the common challenges organizations face, and practical patterns for moving from visibility to actionable cost intelligence.

Inform Phase — five critical pillars

The Inform phase is the foundation of cloud financial management. Its goal is to create visibility and context for cloud spend so teams can make accountable, data-driven decisions. Organizations commonly encounter five critical challenges when standing up the Inform phase:

* Cloud cost obscurity\
  Missing or inconsistent tagging, lack of cost allocation rules, and fragmented reporting make it hard to know what teams and projects are spending.

* Near-real-time visibility\
  Timely insights are crucial. Using tags and hierarchical reporting enables slicing costs by business unit, project, environment, or other dimensions for proactive cost control.

* Accurate allocation\
  A consistent allocation methodology is required to attribute shared resources, reserved/spot instances, and cross-team services to the correct owners.

* Timely evaluation\
  Evaluation should extend beyond budgets and ROI to include sustainability (carbon impact) and other non-financial metrics that influence cloud strategy.

* Data-driven improvements\
  Visibility must be paired with continuous refinement—reporting, tagging, and allocation rules must evolve to stay relevant and actionable.

Often organizations begin with no formal FinOps function and ad-hoc cost work spread across teams. Establishing a dedicated FinOps team is typically the first formal step: centralizing efforts to close cost leakages, standardize tagging, and build governance and reporting practices. That is the core purpose of the Inform phase.

| Pillar                    | Problem                             | Recommended first actions                                                    |
| ------------------------- | ----------------------------------- | ---------------------------------------------------------------------------- |
| Cloud cost obscurity      | Inconsistent tags and unknown spend | Define a minimal mandatory tag set; map existing resources to business units |
| Near-real-time visibility | Slow or noisy reports               | Deploy automated cost exports and streaming metrics where possible           |
| Accurate allocation       | Shared resources with no rules      | Create and document allocation rules (by CPU, usage, seats)                  |
| Timely evaluation         | Narrow KPIs (only spend)            | Add sustainability and utilization KPIs to financial reviews                 |
| Data-driven improvements  | Stale or irrelevant data            | Establish cadence for report review and tag/metric refinement                |

<Frame>
  <img alt="The image presents a guide titled &#x22;Achieving FinOps Success,&#x22; outlining five key areas: Cloud Cost Obscurity, Real-time Visibility, Accurate Allocation, Transparent Evaluation, and Data-Driven Improvements. Each area includes a brief description and an icon." />
</Frame>

Quality Report Improvement Cycle

To progress from raw visibility to operational intelligence, implement a repeatable Quality Report Improvement Cycle. Follow these steps to ensure reports remain accurate, useful, and tailored to their audience:

1. Prioritize consistency\
   Standardize reporting metrics, naming conventions, and data collection across teams and cloud providers. Consistent inputs enable meaningful comparisons over time.

2. Automate reports\
   Remove manual processes by building automated dashboards, scheduled exports, and alerts. Use native provider tools like [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/) and [Azure Cost Management](https://azure.microsoft.com/en-us/services/cost-management/), or third-party platforms such as [CloudHealth](https://www.vmware.com/products/cloudhealth.html) or [CloudCheckr](https://www.cloudcheckr.com/).

3. Differentiate reports\
   Tailor the same underlying dataset for different audiences: executives need trend and variance insights, while engineering teams need resource-level drill-downs and optimization recommendations.

4. Engage core personas\
   Collaborate with engineering, finance, and business leaders on report design and cadence to ensure relevance and encourage responsible consumption.

5. Tailor external outputs when required\
   When third parties (consultants, auditors, or partners) need access, deliver automated, pre-formatted reports and define secure delivery channels.

Keep reports simple, focused, and actionable: highlight top drivers, then enable drill-downs so users can trace root causes without sifting through noise.

<Frame>
  <img alt="The image depicts a cycle diagram titled &#x22;Quality Report Improvement Cycle,&#x22; highlighting five steps: Prioritize Consistency, Automate Reports, Differentiate Reports, Engage Core Personas, and Tailor Reports." />
</Frame>

FinOps cost visibility spectrum

Understanding cost across multiple layers helps reconcile differences between list prices, prices you pay, and the economic cost to the business. Use this spectrum to interpret and present cost information accurately.

| Visibility layer                     | What it represents                                                   | Practical use                                                                           |
| ------------------------------------ | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Baseline pricing (list cost)         | Published on-demand rates from cloud providers                       | Useful for quick comparisons and identifying pricing options                            |
| Negotiated pricing (contracted cost) | Enterprise agreements, reserved instances, Savings Plans             | Use when modeling committed spend and negotiating renewals                              |
| Invoice amount (billed cost)         | Cash outflow on invoices including taxes and fees                    | Required for accounting and cash flow reporting                                         |
| True economic cost (effective cost)  | Allocated cost after discounts, shared resources, and usage patterns | Best for product-level decisions, ROI and per-unit costing (e.g., cost per transaction) |

Understanding each layer enables more accurate forecasting, chargeback/showback, and product-level profitability analysis.

<Frame>
  <img alt="The image illustrates FinOps cost visibility with three sections: Baseline Pricing (List Cost), Negotiated Pricing (Contracted Cost), and Invoice Amount (Billed Cost)." />
</Frame>

Two fundamental best practices

* Start with effective cost calculations\
  From the outset, model effective cost rather than relying solely on list or billed prices. Effective cost includes reserved-instance amortization, allocation of shared services, and contract discounts—this gives teams an actionable baseline for optimization.

* Use additional metrics beyond cost\
  Combine cost with performance, utilization, efficiency ratios, and business outcomes. This multi-dimensional view enables trade-offs between cost, reliability, and speed of delivery.

<Frame>
  <img alt="The image displays two illustrations: one of a person using a smartphone for payment with the text &#x22;Start with Effective Cost,&#x22; and the other of a person analyzing data charts with the text &#x22;Use other Metrics.&#x22;" />
</Frame>

Bottom line

The Inform phase is about measurement and clarity—not perfection. Collect broad metrics, then iterate: refine tagging, reporting standards, and allocation rules so the data becomes progressively more accurate and actionable. Good FinOps begins with visibility, then builds governance and processes that enable continuous optimization.

> **lightbulb** Measure broadly and iteratively: initial measurements may be imperfect, but they are essential to enable optimization and accountability.

What’s next

The Optimize phase uses the visibility and allocations you established in Inform to identify and implement cost-saving actions—right-sizing, purchasing strategies, workload schedule changes, and platform improvements. We will cover those tactics and how to prioritize them in the next lesson.

Links and references

* [FinOps Foundation](https://www.finops.org/) — FinOps framework and community resources
* [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/) — native AWS cost reporting and forecasting
* [Azure Cost Management](https://azure.microsoft.com/en-us/services/cost-management/) — Azure cost analysis and optimization tools
* [CloudHealth by VMware](https://www.vmware.com/products/cloudhealth.html) — multi-cloud cost management platform
* [CloudCheckr](https://www.cloudcheckr.com/) — cloud cost, security, and compliance tooling

- [Watch Video](https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/5dec4577-7276-4a7a-8040-c172cd00f341/lesson/afcf443f-48f5-4ccc-948e-7388835c2b4e)
