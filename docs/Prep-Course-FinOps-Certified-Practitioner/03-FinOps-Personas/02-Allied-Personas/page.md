# Allied Personas

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/FinOps-Personas/Allied-Personas/page

Cross-functional allied personas for autonomous driving that embed cost, asset, sustainability, security, and process controls into cloud cost management

Welcome to the session on Allied Personas. To make this concrete, imagine we work for a cutting-edge autonomous driving company. Our mission: build the safest, most efficient self-driving vehicles on the planet. That requires massive cloud usage — AI model training, sensor-data processing, large-scale simulations, and many SaaS tools. Managing cloud cost and optimizing resources therefore becomes a company-wide responsibility, not just an IT task.

> **lightbulb** Allied personas are cross-functional teams that embed cost-awareness into day-to-day operations. They provide asset visibility, financial controls, sustainability metrics, operational checks, and security cost-tracking so FinOps and core cost-management teams can make informed decisions.

Below we describe the main allied personas, their responsibilities, and why each is essential for effective cloud cost management in an autonomous-driving organization.

## IT Asset Management (ITAM)

ITAM is the inventory backbone. Their primary responsibility is discovering and inventorying all cloud-consumed assets.

* What they do: track virtual machines used for simulations, containers for onboard software, SaaS licenses for dev tools, and other digital assets.
* Why it matters: ITAM gives a single source of truth for what exists, when it was created, and where potential inefficiencies (idle VMs, orphaned storage, duplicate licenses) are hiding.
* How they support cost-management: by surfacing actionable inventory data that FinOps and engineering teams use to reduce waste and align resources with budget goals.

<Frame>
  <img alt="The image is about IT Asset Management (ITAM) under &#x22;Allied Personas,&#x22; highlighting its key responsibility to manage cloud-consumed assets for cost control, and why it's important for cost-awareness in IT operations." />
</Frame>

Every change request or new deployment—whether a sensor driver update or a large-scale simulation—has a financial implication. ITAM ensures those implications are visible and managed.

## IT Financial Management (ITFM)

ITFM takes the financial lens on top of asset data.

* What they do: analyze invoices, track departmental cloud spend, negotiate rates, and map costs to organizational units and projects.
* Why it matters: ITFM translates asset and usage data into firm financial controls and forecasts, spotting expensive regions, inefficient instance selections, and contract opportunities.
* How they support cost-management: they ensure cloud spend maps to business value, and they enforce budgetary guardrails that guide technical decisions.

<Frame>
  <img alt="The image compares IT Asset Management (ITAM) and IT Financial Management (ITFM), highlighting their key responsibilities and reasons for being allied with cloud cost management." />
</Frame>

Together, ITAM and ITFM form the foundation for understanding cloud resources from both asset and financial perspectives.

## Sustainability / Environmental Team

As model training and simulation grow, so does our energy footprint. The sustainability team measures and reports environmental impact alongside cost KPIs.

* What they do: quantify carbon emissions (e.g., kg CO2 per workload), recommend greener instance types, and suggest scheduling strategies to use lower-carbon energy periods.
* Why it matters: aligning environmental metrics with cost metrics helps balance financial efficiency and corporate sustainability goals.
* How they support cost-management: they drive decisions that can reduce energy consumption and often reduce cost (for example, by recommending more efficient instance families or optimized scheduling).

<Frame>
  <img alt="The image outlines the role of sustainability in allied personas, highlighting key responsibilities such as measuring carbon footprint alongside cost KPIs for guiding green choices, and its importance in connecting environmental metrics to FinOps dashboards for efficient cloud usage." />
</Frame>

For an autonomous vehicle company, responsible innovation means optimizing both cost and carbon — often these goals are complementary.

## IT Service Management (ITSM / ITIL)

ITSM embeds process and change control into deployments.

* What they do: perform cost-impact checks during change requests, ensure deployment approvals include financial considerations, and manage capacity for on-prem or hybrid systems that affect cloud usage.
* Why it matters: ITSM prevents surprise costs by gating changes with operational and financial context.
* How they support cost-management: by making cost-awareness part of standard change and incident workflows, ensuring decisions are reviewed for both technical and budget impact.

## Security

Security is non-negotiable in autonomous systems, and it has measurable cloud costs.

* What they do: tag and track security-related cloud spends (WAFs, IDS/IPS, IAM, logging and detection pipelines), and evaluate cost vs. protection level.
* Why it matters: security teams balance risk mitigation with cost-efficiency, ensuring protection measures are effective without excessive spend.
* How they support cost-management: by aligning security controls to budget priorities and identifying opportunities to achieve protection more efficiently.

> **warning** Security spending must be tracked and optimized — cutting costs at the expense of protection can introduce unacceptable risk, especially in safety-critical systems like autonomous vehicles.

<Frame>
  <img alt="The image displays a comparison between IT Service Management (ITSM/ITIL) and Security, highlighting their key responsibilities and reasons for alignment concerning cost-awareness and financial efficiency in cloud operations." />
</Frame>

## Quick Reference Table

| Allied Persona                 |                               Key Responsibility | Why Allied to Cloud Cost Management                                    |
| ------------------------------ | -----------------------------------------------: | ---------------------------------------------------------------------- |
| IT Asset Management (ITAM)     |     Discover and inventory cloud-consumed assets | Provides authoritative inventory to eliminate waste and optimize usage |
| IT Financial Management (ITFM) |    Invoice analysis, budgeting, rate negotiation | Maps spend to business value and enforces financial controls           |
| Sustainability                 | Measure & report carbon, recommend green options | Aligns environmental metrics with cost KPIs to drive efficient choices |
| IT Service Management (ITSM)   |             Change approvals, cost-impact checks | Embeds cost review in operational workflows to prevent surprises       |
| Security                       |           Tag/track security-related cloud spend | Ensures protective controls are both effective and cost-efficient      |

## How these personas work together

* ITAM provides the inventory.
* ITFM overlays financial context and budgets.
* Sustainability adds environmental KPIs to the dashboards.
* ITSM enforces process checks that include cost considerations.
* Security ensures protective measures are optimized for cost and effectiveness.

This coalition enables FinOps and core cost-management teams to make data-driven decisions: right-sizing compute, choosing the best-priced regions, optimizing instance types, scheduling workloads for cost or carbon benefit, and balancing security investment with risk.

## Further reading

* [FinOps Foundation](https://www.finops.org/)
* [Kubernetes cost optimization guides](https://kubernetes.io/)
* [IT Asset Management best practices](https://en.wikipedia.org/wiki/IT_asset_management)

In a dynamic environment like autonomous driving, allied personas are essential partners in delivering technology that is safe, performant, and cost-effective. Thanks for watching — see you in the next video.

- [Watch Video](https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/17116beb-dcd6-4099-9424-bcb9554af3f3/lesson/597263a0-4189-48f3-8503-07051635a4b4)
