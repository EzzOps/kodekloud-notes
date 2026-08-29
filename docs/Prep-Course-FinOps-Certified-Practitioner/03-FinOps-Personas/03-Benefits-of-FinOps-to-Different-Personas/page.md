# Benefits of FinOps to Different Personas

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/FinOps-Personas/Benefits-of-FinOps-to-Different-Personas/page

Explains how FinOps delivers cross-functional cloud cost accountability and value for engineering, procurement, product, and leadership at a large company.

Welcome to this lesson. Here we'll explore how FinOps delivers measurable value across different personas in an organization — engineering, procurement, product, and leadership — by creating financial accountability and cross-functional collaboration around cloud spend.

Context: imagine Global Cargo Solutions, a large, global shipping company relying heavily on cloud infrastructure for tracking shipments, optimizing routes, managing logistics, and handling customer data. The company aims to improve efficiency, reduce costs, and accelerate innovation. FinOps becomes essential to meet these goals by aligning technical, financial, and product decisions.

Below we summarize how FinOps benefits each persona at Global Cargo Solutions, followed by a deeper look at what that means in practice.

## FinOps benefits — at a glance

|     Persona | Primary benefits                                                                  | Example outcomes / metrics                                                        |
| ----------: | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Engineering | Optimized cloud pricing, utilization accountability, cost-aware architecture      | Reduced spend via rightsizing, improved CPU/RAM utilization, fewer idle resources |
| Procurement | Unit-level cost visibility, contract/license optimization                         | Better-negotiated commitments, lower wasted licenses, improved cost-per-shipment  |
|     Product | Feature-level spend attribution, cost-driven prioritization                       | Prioritized features with best value-to-cost ratio, lower cost per user action    |
|  Leadership | Consolidated spend visibility, strategic transparency, cross-functional alignment | Predictable cloud budgets, data-driven investments, clearer ROI on cloud projects |

## Engineering persona

Engineers and platform teams gain concrete tools and practices that reduce waste and improve predictability:

* Optimized cloud pricing: Apply rightsizing, reserved/commitment plans, and spot/preemptible instances (e.g., reserved instances, committed use discounts, savings plans). Note that spot/preemptible instances are interruptible.
* Accountability for utilization: Use tagging/labels, billing exports, and cost-allocation tooling to provide per-team and per-application cost visibility. This links infrastructure choices to spend.
* Cost-aware architecture: Design decisions that consider storage classes, caching, and autoscaling reduce persistent cost drivers.
* Faster, more predictable delivery: Integrate cost metrics and optimization tooling into the CI/CD pipeline and deployment review process so teams ship quickly within budget.

Practical tips:

* Automate rightsizing recommendations into pull-request checklists.
* Add cost alarms to staging and production environments to avoid surprise overages.

## Procurement persona

Procurement teams use FinOps to convert raw cloud invoices into actionable purchasing decisions:

* Cost visibility and unit economics: Measure cost per shipment processed, per customer interaction, or other business-level units with attribution and allocation.
* Activity-based costing: Implement granular costing by activity/service to enable accurate internal chargebacks and reconciliation.
* Contract and license visibility: Centralize oversight of cloud contracts, licenses, and entitlements to avoid unused seats and penalties.
* Forward-looking negotiation: Leverage historical consumption and forecasts to negotiate better terms and commitment discounts with cloud providers.

Procurement-focused outputs:

* Forecasts and commitment recommendations based on usage trends.
* License utilization dashboards to retire unused entitlements.

## Product persona

Product managers make better trade-offs when they can map costs to features:

* Feature-level spend visibility: Attribute cloud costs to features or product lines (e.g., real-time shipment tracking vs. batch reporting).
* Cost-driven prioritization: Prioritize features with the best value-to-cost impact, re-scope or replace expensive components when needed.
* Experimentation with cost in mind: Use A/B experiments that include cost per transaction as a success metric.

Product playbook suggestions:

* Add cost per feature as a KPI in product planning.
* Include engineers and finance in feature cost reviews before large rollouts.

## Leadership persona

Leadership gains the visibility and governance needed to set strategy:

* Holistic spend accountability: Consolidated views across teams illuminate overages and optimization opportunities.
* Strategic transparency: Accurate spend and forecast data inform investment decisions and resource allocation.
* Data-driven decision making: Replace estimates with precise cloud metrics for planning and budgeting.
* Cross-functional alignment: FinOps fosters shared ownership among engineering, finance, procurement, and product.

Leadership actions:

* Use FinOps reports in board reviews and quarterly planning.
* Sponsor cross-functional FinOps rituals to maintain alignment and momentum.

<Frame>
  <img alt="The image is a diagram showing the benefits of FinOps for different personas, including Engineering, Procurement, Product, and Leadership, each linked to benefits like accountability, transparency, data-driven decisions, and alignment." />
</Frame>

If you are an engineering manager leading a DevOps team, a FinOps practice helps you coordinate and communicate with procurement, product, and leadership on the shared topics above. That coordination is the central benefit of FinOps across personas.

<Callout icon="lightbulb">
  FinOps is not just about cutting costs — it's about maximizing cloud value by aligning technical, financial, and product decisions across the organization.
</Callout>

We will discuss a real-world FinOps personas scenario and dive into a practical example to show how FinOps principles are applied in a large organization.

Key takeaways:

* FinOps creates measurable value for engineering, procurement, product, and leadership by tying cloud spend to business outcomes.
* The practice depends on telemetry, cost allocation, and cross-functional rituals that embed cost awareness into everyday work.
* Start small: prioritize high-impact areas (biggest spend or highest variability) and expand the practice iteratively.

Resources and further reading:

* [FinOps Foundation](https://www.finops.org/)
* [Kubernetes cost optimization patterns](https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/#resource-requests-and-limits)
* Cloud provider cost management docs (AWS, Azure, GCP) for provider-specific commitment and pricing options.

That is it for this lesson. See you in the next one.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/17116beb-dcd6-4099-9424-bcb9554af3f3/lesson/0290ebf0-d8dc-4a39-a4e1-64148871c777" />
</CardGroup>
