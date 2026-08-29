# FinOps Framework

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/Introduction-to-FinOps/FinOps-Framework/page

Guide to the FinOps Framework for aligning finance and engineering to manage cloud spending through personas, domains, capabilities, and practical adoption steps to measure, optimize, and govern cloud costs

Welcome — in this lesson we'll explain the FinOps Framework: the practical structure of principles, personas, domains, and capabilities that enables organizations to manage cloud spend and drive business value. If you’ve already learned what FinOps is and why it matters, this guide shows how to put it into practice.

The FinOps Framework is a people-process-technology model that aligns finance and engineering to ensure cloud investments support business strategy. It is not a checklist to be followed rigidly; it’s a set of modular components you can adapt to your organization’s size, maturity, and goals.

## Framework diagram

The diagram below (sourced from the FinOps Foundation) illustrates how business strategy and technology strategy flow into personas, domains, and capabilities — the building blocks of a successful FinOps practice.

<Frame>
  <img alt="The image is a diagram of the FinOps Framework, illustrating the integration of business and technology strategies with scopes, personas, domains, and capabilities for managing usage, cost, and business value in cloud financial operations. It highlights core and allied personas, as well as various operations and governance functions essential to FinOps practice." />
</Frame>

Key takeaway: FinOps is about aligning cloud spending to business objectives — not just cutting costs. Effective FinOps requires finance and technology collaboration from strategy through day-to-day operations.

## Personas: who does FinOps work with

The Framework distinguishes between core personas (those directly responsible for cloud and financial outcomes) and allied personas (stakeholders who influence cost and consumption).

| Persona Type    | Role examples                                                  | Typical responsibilities                                                                                |
| --------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Core personas   | Engineering teams, Finance teams, Product managers, Leadership | Day-to-day cloud operations, cost allocation, budgeting, prioritizing spend against product outcomes    |
| Allied personas | Procurement, Security, Sales, HR                               | Licensing decisions, contractual negotiations, security controls, consumption policies that affect cost |

Understanding who owns decisions, who influences them, and how they interact is essential when designing governance and tooling.

## Domains and capabilities

Below the personas are the Framework’s domains — functional pillars that describe how to achieve measurable FinOps outcomes. Each domain bundles practical capabilities you can implement.

| Domain                    | Purpose                                                           | Example capabilities                                                                    |
| ------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Understand usage and cost | Establish accurate, timely consumption and billing data           | Data ingestion, normalization, tagging, cost allocation (chargeback/showback)           |
| Measure business value    | Tie cloud spend to product and customer outcomes                  | Cost attribution, ROI analysis, benchmarking, cost-per-feature/customer metrics         |
| Optimize usage and cost   | Reduce waste and increase efficiency while preserving performance | Rightsizing, reservations/commitments, workload placement, architectural optimization   |
| Manage FinOps practice    | Build governance, processes, and continuous improvement           | Reporting, forecasting, policy enforcement, capability maturity, stakeholder enablement |

Each capability maps to specific activities: for example, “Optimize usage and cost” includes architecting for efficiency and ongoing workload optimization to minimize waste without degrading service.

## How to adopt the Framework

FinOps adoption is a pragmatic journey — there is no one-size-fits-all. Keep these three guiding ideas in mind as you plan:

1. There is no one-size-fits-all approach
   * Tailor the Framework to your organization’s size, industry, culture, and cloud maturity. Large enterprises and startups will prioritize different domains and processes.

2. Treat the Framework as flexible building blocks
   * Select domains and capabilities that match current priorities and capacity. Focus on high-impact outcomes rather than trying to implement every element at once.

3. Start small and scale smart
   * Target high-value, low-effort wins (the 80/20 principle). A common early win: improve cost visibility by centralizing billing and providing a shared dashboard for engineering and finance.

<Callout icon="lightbulb">
  Start with the highest-value, lowest-effort items (for example, a unified billing dashboard or a basic cost attribution model). Use quick wins to build momentum and secure stakeholder buy-in.
</Callout>

## First practical steps

If your organization has no formal cloud cost practices yet, follow this starter checklist:

* Centralize billing and usage data into a single view or dataset.
* Apply a consistent tagging and resource naming strategy for allocation.
* Create a shared dashboard for engineering and finance to view cost and trends.
* Run a short pilot on one team or product to measure and demonstrate impact.
* Establish a simple governance loop: measure → allocate → optimize → report.

These initial steps unlock capabilities like forecasting, forecasting-linked budgeting, and optimization programs (e.g., rightsizing, commitments).

## Measuring progress and scaling

Adopt metrics that demonstrate business impact, not just cost reduction. Examples include cost per customer, cost per feature, or cloud spend as a percentage of ARR. Use these signals to prioritize optimization work and to justify investment in automation and tooling.

Consider a maturity roadmap that progresses from basic visibility and allocation to automated optimization, predictive forecasting, and integrated financial processes spanning engineering and finance.

## Summary and next lessons

The FinOps Framework gives you a structured, adaptable approach to manage cloud financials by aligning people, processes, and technology. Start with visibility, measure business value, iterate on optimization, and build governance that scales.

In the next lesson we’ll examine the current state of FinOps: trends, common challenges, and practical patterns organizations use to overcome them. Stay tuned.

## Links and references

* FinOps Foundation: [https://www.finops.org/](https://www.finops.org/)
* Recommended reading: FinOps best practices for cost allocation, optimization, and governance.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/24982811-6142-4554-afd8-2b5f3b8a7f28/lesson/77233fc6-2d13-4b7f-b844-23f17bad3988" />
</CardGroup>
