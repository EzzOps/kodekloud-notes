# What does a FinOps Practitioner do

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/Introduction-to-FinOps/What-does-a-FinOps-Practitioner-do/page

Summary of FinOps practitioner responsibilities across SaaS, licensing, private cloud, data center, and chargeback with emphasis on forecasting, reporting, AI cost management, and cross functional collaboration.

Hello and welcome back.

This article examines where FinOps practitioners focus their efforts and the core responsibilities they own. The role is organized into clear pillars so you can quickly map responsibilities to day-to-day activities. If you work as a DevOps engineer, SRE, or manager, many of these tasks will look familiar — FinOps is often a shared responsibility among engineering, finance, and product teams.

## Overview of the FinOps pillars

Below is a concise summary of the five primary pillars of FinOps. Each pillar highlights the primary focus and typical responsibilities.

| Pillar                              | Primary focus                                          | Typical responsibilities                                                                                                                                  |
| ----------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SaaS (Software as a Service)        | Subscription management and cost optimization for SaaS | Managing vendor subscriptions, negotiating terms, tracking seat counts and overages, setting subscription budgets and renewal forecasts                   |
| Licensing models                    | Planning and estimating software license needs         | Choosing license types (per-user, per-core, site), sizing licenses to usage, optimizing utilization and aligning licensing with budgets                   |
| Private cloud                       | Infrastructure forecasting and capacity planning       | Forecasting CPU/memory/storage needs, right-sizing VMs/containers, tracking amortized costs, producing stakeholder reports                                |
| Traditional data center operations  | On-prem capacity planning and resource allocation      | Planning rack, power, cooling, provisioning physical resources, forecasting growth to avoid under/over-provisioning                                       |
| Invoicing and chargeback / showback | Attributing costs to teams or products                 | Designing chargeback/showback models, implementing billing exports and allocation rules (tags/labels/accounts), producing transparent invoices or reports |

## Detailed pillar responsibilities

1. SaaS (Software as a Service)
   * Primary focus: subscription management and recurring spend control.
   * Key responsibilities:
     * Track vendor subscriptions, renewals, and seat counts.
     * Negotiate contract terms and volume discounts.
     * Forecast subscription budgets and enforce spend policies.

2. Licensing models
   * Primary focus: ensuring licensing is cost-efficient and compliant.
   * Key responsibilities:
     * Select appropriate license types (per-user, per-core, site license).
     * Right-size licenses to actual usage to avoid waste.
     * Include licensing costs in financial forecasts and engineering plans.

3. Private cloud
   * Primary focus: capacity planning and fair cost allocation across teams.
   * Key responsibilities:
     * Forecast resource demand (CPU, memory, storage).
     * Analyze utilization and right-size instances or containers.
     * Produce cost reports that amortize fixed infrastructure across services.

4. Traditional data center operations
   * Primary focus: physical capacity forecasting and resource allocation.
   * Key responsibilities:
     * Plan rack, power, and cooling capacity.
     * Allocate physical resources with growth forecasting.
     * Avoid both under-provisioning (risking outages) and over-provisioning (wasting capital).

5. Invoicing and chargeback / showback
   * Primary focus: building accountability through cost attribution.
   * Key responsibilities:
     * Design chargeback/showback models that reflect true consumption.
     * Implement billing exports and enforce tagging/labeling strategies.
     * Create transparent reports so teams understand and own their spend.

## Cross-cutting skills: forecasting, reporting, and analytics

* Forecasting: Predict SaaS growth, private cloud capacity needs, and AI compute consumption to enable proactive budgeting.
* Reporting & analytics: Build dashboards, KPIs, and reports that surface cost per service, per environment, or per model inference to guide optimization decisions.
* Communication: Translate technical consumption into business-facing cost narratives so stakeholders can act.

## AI use cases and FinOps

AI and ML workloads introduce different cost patterns:

* Heavy and variable compute (training, large-scale inference).
* Increased storage demands for datasets and model artifacts.
* Frequent experimentation and iteration that make unit economics (cost per training hour, cost per inference) crucial.

Practitioners must:

* Define cost-per-unit metrics (training hour, inference request).
* Forecast usage patterns across teams and projects.
* Implement allocation and monitoring to avoid undiscovered runaway spend.

## Example: managing an OpenAI API key across teams

* Scenario: multiple teams want to use a single OpenAI API key.
* Practitioner questions:
  * Which team consumed how much of the key?
  * What budgets or quotas should each team have?
  * How is usage tracked and how are budgets enforced?
* Typical solutions:
  * Enforce usage tagging or pass-through metadata so requests are attributable.
  * Proxy requests through per-team credentials or a gateway that enforces quotas.
  * Collect meter-level data and export billing for allocation and chargeback.

<Frame>
  <img alt="The image summarizes the roles of a FinOps practitioner across five areas: SaaS, Licensing, Private Cloud, Data Center, and AI, detailing activities like budgeting, forecasting, and reporting." />
</Frame>

## Summing up: skills every FinOps practitioner needs

* Forecast cloud and private cloud costs and assess licensing implications.
* Implement allocation, invoicing, and chargeback/showback methodologies.
* Build reporting and analytics to inform optimization and budgeting decisions.
* Adapt practices for modern workloads (especially AI/ML) where compute and experimentation can dominate costs.
* Collaborate across engineering, finance, product, and platform teams — FinOps is cross-functional.

> **lightbulb** FinOps is a team effort: engineers, finance, product, and platform teams must work together to keep organizational spend healthy and aligned with business goals.

## Certifications and learning paths

FinOps Foundation provides defined certification paths that validate knowledge across principles, tooling, and practices. Consider their offerings to standardize team knowledge and demonstrate competency: [FinOps Foundation certification](https://www.finops.org/certification/).

## References and further reading

* [FinOps Foundation](https://www.finops.org/)
* [OpenAI API keys documentation](https://platform.openai.com/docs/api-keys)

That completes this article.

- [Watch Video](https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/24982811-6142-4554-afd8-2b5f3b8a7f28/lesson/bb5a4eae-5eff-4f5c-b881-e431e5a421d5)
