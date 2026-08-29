# FinOps Maturity Framework Key Phases

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/FinOps-Framework/FinOps-Maturity-Framework-Key-Phases/page

Describes the FinOps maturity journey through Crawl Walk Run phases to improve cloud cost allocation, tagging, automation, governance, and forecasting.

Hello and welcome back.

This lesson expands on the FinOps framework overview by describing how organizations typically adopt FinOps in practice. Understanding the maturity journey helps you prioritize tooling, processes, and culture to reduce cloud spend and improve forecasting.

At a high level, organizations tend to fall into two broad states:

* Basic state — You receive a cloud bill but cannot reliably allocate that spend to teams, services, or projects.
* Advanced state — You can allocate nearly every line item of your cloud bill to owners, identify overspend, and forecast with higher accuracy.

For example: if your organization receives a single cloud bill of \$100K, an advanced-state organization might allocate 99% of that cost to internal owners and services, identify which services are overspending, and forecast future costs with much tighter bounds.

Most organizations do not move directly from Basic to Advanced. Instead, they progress through three common maturity phases: Crawl, Walk, and Run.

<Frame>
  <img alt="The image is a diagram of the FinOps Maturity Framework with three key phases: Crawl, Walk, and Run, indicating progressive capability levels from basic to advanced. Each phase includes descriptions of capability follow-through and automation requirements." />
</Frame>

Below is a concise, practical description of each phase — what it looks like, the capabilities you should expect, typical goals or KPIs, and common gaps to address.

## Crawl phase

* What it looks like: Reporting is limited. Teams rely on manual scripts, spreadsheet exports, or ad hoc cost reviews. Tagging and allocation policies may exist but are not consistently applied.
* Capabilities: Basic cost visibility, ad hoc investigations, limited automation.
* Typical goals (aspirational): Begin allocating at least a portion of spend; reduce forecasting variance (for example, target forecasting within \~20%).
* Common gaps: Inconsistent tagging, few automated policies, low organizational adoption of cost ownership or chargeback.

## Walk phase

* What it looks like: Practices are becoming repeatable. Teams adopt tagging and allocation more consistently and automation begins to reduce manual effort. Reporting and anomaly detection are in place and acted upon.
* Capabilities: Consistent tagging and allocation for a majority of resources, automated reporting, routine cost reviews, and some cost-optimization workflows.
* Typical outcomes: Many organizations allocate 50–80% of spend, achieve forecasting within \~20% variance, and utilize a significant portion of discounts (for example, \~70% coverage where applicable).
* Why it matters: Walk is a scalable, stable stage where you can detect spikes, embed cost-awareness into engineering practices, and demonstrate measurable savings.

## Run phase

* What it looks like: FinOps operates as an organizational operating model across engineering, finance, and product. Governance, automation, and proactive management are embedded.
* Capabilities: Near-complete allocation of spend, centralized and automated governance, aggressive use of discounts/commitments, and tight forecasting.
* Typical KPIs: 90%+ allocation of spend, 80%+ utilization of commitment/discount programs when applicable, and forecasting accuracy often within \~12%.
* Cultural impact: Cost KPIs are broadly understood; teams design with cost in mind and collaborate on optimization and vendor negotiations.

<Frame>
  <img alt="The image shows the &#x22;FinOps Maturity Framework: Key Phases&#x22; focusing on the &#x22;Run&#x22; phase, highlighting the overview, performance goals, and community goals/KPIs, aimed at advanced maturity." />
</Frame>

## Phase comparison at a glance

| Phase | Visibility & Reporting                        |                       Allocation & Tagging |                         Automation & Governance | Typical Allocation KPI |
| ----- | --------------------------------------------- | -----------------------------------------: | ----------------------------------------------: | ---------------------: |
| Crawl | Manual or sparse reports; periodic exports    |                  Partial or ad hoc tagging |                              Minimal automation |   Low (early adoption) |
| Walk  | Automated reports; anomaly detection          | Majority of resources tagged and allocated |            Automated reporting & some workflows |                 50–80% |
| Run   | Real-time/centralized reporting & forecasting |                   Near-complete allocation | Centralized governance and proactive automation |                   90%+ |

## Why understanding phases matters (exam and practice)

Knowing the differences among Crawl, Walk, and Run helps you:

* Select the right tooling: lightweight reporting in Crawl vs. full FinOps platforms in Run.
* Prioritize work: tagging and repeatable reporting in Crawl/Walk; governance and commitment strategies in Run.
* Align stakeholders: different phases require different levels of finance, engineering, and product engagement.

<Callout icon="lightbulb">
  Tip: Most organizations are in the Walk phase. Prioritize repeatable reporting, consistent tagging, and automation for anomaly detection to achieve fast ROI.
</Callout>

## Actionable next steps by phase

* If you’re in Crawl:
  * Formalize tagging taxonomy and ownership.
  * Build repeatable cost reports (daily/weekly exports).
  * Start small: allocate a subset of spend to test processes.
* If you’re in Walk:
  * Automate reporting and anomaly alerts.
  * Standardize allocation rules and share cost KPIs with teams.
  * Improve discount coverage and begin commitment planning.
* If you’re in Run:
  * Centralize governance and bake cost checks into CI/CD.
  * Optimize across teams, refine forecasting, and lead negotiation strategies with providers.
  * Continuously measure and publish KPIs across the organization.

## References and further reading

* [FinOps Foundation](https://finops.org) — resources, maturity models, and community best practices.
* [Cloud cost management basics](https://cloud.google.com/products/operations) — vendor-specific cost tools and documentation.
* [Kubernetes cost allocation guide](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) — practical approaches for containerized workloads.

That’s it for this lesson. Apply the checklist above to identify your organization’s current phase and focus the next sprint on the highest-impact improvements. Speak with you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/77e6b2c4-f9cd-410f-a396-178e2aa962bb/lesson/14320dfb-37e8-4cc8-a5f7-a786dd2b03c6" />
</CardGroup>
