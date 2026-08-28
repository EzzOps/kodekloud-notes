# Building an SRE Team

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Fundamentals-of-SRE/Building-an-SRE-Team/page

Guide to structuring SRE teams, comparing embedded centralized consulting and hybrid models, roles, sizing, skills, and hiring guidance for organizations at different growth stages

This lesson explains how to structure a Site Reliability Engineering (SRE) function, the trade-offs for common team models, role definitions, sizing guidelines, and the skills that make SREs effective. Use this as a practical guide when deciding how to staff reliability work and evolve SRE practices as your organization grows.

## Quick overview

* What to choose: the right SRE model depends on organization size, product complexity, culture, and growth plans.
* Practical trade-offs: embedded SREs give product context; centralized teams deliver consistency; consulting scales knowledge; hybrid blends the benefits.
* People and skills: SRE teams combine technical depth (programming, systems, observability) with strong communication and incident leadership.

## Common SRE team models (with trade-offs)

| Model       | How it works                            | Key benefits                                                              | Main trade-offs                                                          |
| ----------- | --------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Embedded    | SREs sit inside product teams           | Deep service knowledge, faster reliability improvements, strong ownership | Inconsistent practices across teams, harder to scale tooling & standards |
| Centralized | One SRE team supports multiple products | Consistent tooling, shared standards, efficient resource use              | May lack product context, can become a throughput bottleneck             |
| Consulting  | SREs act as advisors/coaches            | Scales knowledge, lightweight ownership, accelerates capability adoption  | Effectiveness depends on product teams adopting guidance                 |
| Hybrid      | Mix of central tooling + embedded SREs  | Flexible; balances consistency and context                                | Requires clear role boundaries and strong coordination                   |

Embedded model

* SREs live in product teams, influence design choices, and deliver rapid reliability improvements.
* Best when product teams must own both feature and reliability work; promotes collaboration and faster feedback loops.

<Frame>
  <img alt="A presentation slide titled &#x22;SRE Team Models&#x22; describing the &#x22;Embedded Model&#x22; where SREs are embedded within product teams, with icons and benefits: gain knowledge of service, influence technical decisions, and accelerate reliability efforts. A footer note reads &#x22;Promotes collaboration but lacks consistency and scalability.&#x22;" />
</Frame>

Centralized model

* A single SRE organization maintains cross-product platforms, shared monitoring, and common practices.
* Works well for enforcing standards and building platform-level automation.

Consulting model

* SREs operate as coaches or consultants, advising product teams, building blueprints, and delivering training.
* Scales SRE ideas without owning each service directly; requires adoption by product teams to succeed.

<Frame>
  <img alt="A presentation slide titled &#x22;SRE Team Models&#x22; describing the &#x22;Consulting Model&#x22; and noting that SREs act as advisors rather than owners. It shows an illustration of a person presenting to two seated people and two callout boxes stating it advises teams without managing systems directly and that it scales SRE culture but relies on team buy-in." />
</Frame>

Hybrid model

* Blends embedded SREs for high-impact services with a centralized team that builds shared tooling, libraries, and standards.
* Allows organizations to combine scale and context while evolving engagement models as teams mature.

<Frame>
  <img alt="A slide titled &#x22;SRE Team Models&#x22; illustrating a Hybrid Model that combines a centralized SRE team and embedded engineers (icons with a green plus) feeding into &#x22;High-impact services.&#x22; A footer banner reads &#x22;Works well in growth but demands clarity and coordination.&#x22;" />
</Frame>

<Callout icon="lightbulb">
  There is no single "best" model. Choose based on your organization's size, maturity, product complexity, and culture — and be prepared to evolve the model as you scale.
</Callout>

## Real-world examples and how organizations apply the models

* Embedded: Netflix and Amazon follow "you-run-it" philosophies where product teams own reliability. Spotify also embeds reliability into product squads.
* Centralized: Google historically used dedicated SRE teams; LinkedIn and Microsoft have centralized functions to enforce consistency.
* Consulting: Dropbox uses SREs mainly as coaches; Google also places SREs in advisory roles where appropriate.
* Hybrid: Meta, Google (in many domains), IBM, and Uber combine central tooling with embedded engineers aligned to product needs.

These examples illustrate how companies adapt SRE models to their culture, scale, and operational goals.

## Core SRE roles (typical team composition)

| Role                     | Primary focus                                                   | When to introduce                                                   |
| ------------------------ | --------------------------------------------------------------- | ------------------------------------------------------------------- |
| SRE Generalist           | Toil reduction, automation, on-call, partnering with developers | From day one for small teams                                        |
| Reliability Architect    | System design, capacity planning, fault domains                 | Mid-stage onward for complex systems                                |
| Observability Specialist | Metrics, logging, tracing, SLIs/SLOs                            | When you need consistent instrumentation and platform observability |
| Incident Commander       | Incident coordination, communications, postmortems              | As on-call rotations scale beyond a few people                      |
| SRE Manager              | Strategy, team development, engagement models                   | When multiple SREs or subteams need alignment                       |

<Frame>
  <img alt="A slide titled &#x22;Core SRE Roles&#x22; showing five colored boxes for SRE Generalist, Reliability Architect, Observability Specialist, Incident Commander, and SRE Manager. Each box gives a short description of that role's responsibilities (automation and incident response, scalable design, observability/SLIs, incident coordination, and team/strategy leadership)." />
</Frame>

## SRE at every stage of growth

SRE practices are adaptable — the principles remain the same while the approach changes with scale.

* Small / early-stage startups
  * Team size: 0–5 SREs or developer-led reliability.
  * Focus: generalists who automate, monitor, and own on-call duties. Keep tooling pragmatic.
* Mid-size organizations
  * Team size: \~5–15 SREs; specializations appear (observability, incident response, platform).
  * Focus: formalize SLOs, incident playbooks, error budgets, and internal standards.
* Large enterprises
  * Team size: 15+ SREs organized into domain-aligned subteams (e.g., storage, networking, data pipelines).
  * Focus: invest in platform services, training programs, and defined engagement/onboarding processes for product teams.

<Frame>
  <img alt="A slide titled &#x22;SRE at Any Stage&#x22; comparing Small Organization and Large Organization approaches, each with a people icon and bullet points. The small side lists developer-driven SRE, integrated practices, lean tooling and agile processes; the large side lists dedicated SRE teams, specialized roles, and comprehensive tooling." />
</Frame>

## Team-sizing and engagement guidance

* Early-stage: hire generalists who can iterate quickly and establish basic on-call, monitoring, and automation.
* Mid-stage: hire role owners for observability and incident response; codify SLOs and error budget policies.
* Large scale: create clear service-level engagement models so product teams know how to request SRE help and what to expect.

### Case study: Meta’s Production Engineering evolution

Meta’s Production Engineering (PE) demonstrates an SRE evolution:

1. Centralized beginnings — PE provided incident response and scaling help when product teams were small.
2. Shift to embedded — as Meta grew, PE embedded engineers in product teams for design-time reliability and better feedback loops.
3. Hybrid outcome — central PE functions (tooling and standards) remain while most reliability work is handled within product teams.

<Frame>
  <img alt="A presentation slide titled &#x22;A Closer Look at Real-World Evolution&#x22; showing a five-step timeline that describes how reliability/production engineering moved from a centralized team to embedded engineers within product teams (with some central functions remaining). To the right are three circular icons representing small product teams." />
</Frame>

## Skills and hiring signals

Technical skills

* Proficiency in at least one primary language (Go, Python, Java).
* Systems expertise: Linux internals, networking, containers.
* CI/CD and infrastructure-as-code experience (Terraform, GitOps).
* Observability tooling and instrumentation (metrics, tracing, logging).
* Troubleshooting distributed systems at scale.

Non-technical skills

* Calm and clear communication during incidents.
* Curiosity and continuous learning.
* Empathy for users and product teams.
* Root-cause thinking and a focus on long-term fixes.

<Frame>
  <img alt="A slide titled &#x22;Skills for a Successful SRE&#x22; showing two boxed lists: Technical Skills (proficiency in major programming languages, strong systems knowledge, CI/CD/infrastructure-as-code/monitoring experience, and debugging large-scale systems) and Non-Technical Skills (curiosity, calmness under pressure, empathy, and a passion for solving root causes). The layout has the technical box on the left, non-technical on the right, and a simple avatar illustration in the center." />
</Frame>

In-demand skills (market signals)

* Cloud-native observability (OpenTelemetry, Prometheus, Grafana).
* Kubernetes troubleshooting and automation.
* SLO design and error budget management.
* Incident leadership and cross-team communication.
* Collaboration for shared ownership and platform engagement.

<Frame>
  <img alt="A presentation slide titled &#x22;Skills for a Successful SRE&#x22; listing four in-demand skills: cloud-native observability (e.g., OpenTelemetry, Prometheus, Grafana), Kubernetes troubleshooting and automation, SLO implementation and error budget policies, and incident response leadership and communication. There's also a small newspaper-style &#x22;NEWS&#x22; icon on the left and a citation to LinkedIn Workforce Insights." />
</Frame>

## Pro tip

* Go deep before you go broad: build deep expertise in one area (observability, automation, or incident response) first. Depth builds intuition and technical muscle you can apply across the SRE discipline.

<Frame>
  <img alt="A presentation slide titled &#x22;SRE Beginners – A Pro Tip&#x22; featuring a podcast banner for &#x22;Episode 1 - IBM SRE Profession: Making of the SRE Omelette.&#x22; Below it is a tip that reads: &#x22;Go deep before going wide.&#x22;" />
</Frame>

Going deep in one area—whether diagnosing outages, building automation, or instrumenting systems—gives you a reliable foundation for learning the rest of the SRE skill set.

## Useful links and references

* [Site Reliability Engineering: How Google Runs Production Systems (Book)](https://sre.google/books/)
* [Kubernetes documentation — Concepts](https://kubernetes.io/docs/concepts/)
* [OpenTelemetry](https://opentelemetry.io/)
* [Prometheus](https://prometheus.io/) and [Grafana](https://grafana.com/)
* [Google SRE practices and SLO guidance](https://cloud.google.com/blog/products/observability/slo)
* [LinkedIn Workforce Insights — industry skills signals](https://www.linkedin.com/workforce-insights/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/df29fdca-b56b-4828-a8cc-abd0bb37ed70/lesson/7df8d16f-1729-453e-af67-3397c85c6fdd" />
</CardGroup>
