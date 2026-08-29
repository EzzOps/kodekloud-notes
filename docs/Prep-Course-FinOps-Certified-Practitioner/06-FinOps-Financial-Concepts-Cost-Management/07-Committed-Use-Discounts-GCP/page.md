# Committed Use Discounts GCP

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/FinOps-Financial-Concepts-Cost-Management/Committed-Use-Discounts-GCP/page

Explains Google Cloud Committed Use Discounts, how spend-based and resource-based commitments lower compute costs, best practices, and interactions with other GCP cost-saving options

Welcome back. This lesson explains Committed Use Discounts (CUDs) on Google Cloud Platform (GCP): what they are, how they work, when to use them, and how they interact with other cost-saving options. If you can predict some of your compute needs, CUDs are one of the most effective tools to reduce cloud spend and improve FinOps practices.

<Frame>
  <img alt="The image illustrates &#x22;Committed Use Discounts (GCP)&#x22; with an icon of a person using a laptop and highlights benefits like cost savings, better FinOps practice, and support for maturity models." />
</Frame>

What are CUDs?

* Committed Use Discounts let you lock in lower prices for a defined set of Google Cloud resources by committing to a consistent level of usage over a fixed term (1 or 3 years).
* In exchange for a commitment, Google applies a discounted rate to matching usage automatically—no manual tagging required.
* CUDs are particularly useful for predictable, steady-state compute requirements and are a core FinOps lever for predictable cost control.

How CUDs work — the simple flow

1. Choose a commitment term (1 year or 3 years) and select the commitment model (spend-based or resource-based).
2. Commit to a minimum hourly spend or a specific resource quantity (vCPUs, memory, etc.) for the term.
3. Google Cloud automatically applies the discount to eligible usage that matches your commitment; any excess usage remains at regular on‑demand pricing.

<Frame>
  <img alt="The image explains how Google Cloud Committed Use Discounts (CUDs) work, detailing the commitment period, applicable resources, and automatic application to matching resources." />
</Frame>

Where CUDs apply

* Compute vCPUs and memory (primary targets).
* GPUs and some local SSD usage (coverage varies by offering).
* CUDs can apply across VM families and regions—GCP automatically matches commitments to eligible resources.

Two primary commitment models

| Commitment model           |                              What you commit | Flexibility                                                |                      Typical discount | Best for                                 |
| -------------------------- | -------------------------------------------: | ---------------------------------------------------------- | ------------------------------------: | ---------------------------------------- |
| Spend-based commitments    |       A minimum hourly spend (e.g., \$/hour) | High — not tied to specific machine types or regions       |                Moderate (up to \~25%) | Variable workloads that need flexibility |
| Resource-based commitments | Specific resource quantities (vCPUs, memory) | Medium — applies across types/regions but targets capacity | Deep (up to \~57% for some resources) | Predictable, steady-state compute needs  |

Spend-based commitments

* You commit to a minimum spend per hour rather than particular machine types or regions.
* Because it’s a financial commitment, you retain maximum flexibility to change instances, families, or regions while still receiving discounts.
* Discounts are generally lower than resource-based CUDs but can combine with other discounts (e.g., sustained use discounts).

<Frame>
  <img alt="The image is a table detailing spend-based commitments, highlighting key responsibilities like commitment, flexibility, discount, and best use cases with associated computations." />
</Frame>

Resource-based commitments

* You commit to specific quantities of resources (for example, a number of vCPUs and a set amount of memory).
* These commitments target capacity and typically deliver much larger discounts compared with spend-based offers.
* Resource-based commitments are flexible across machine types and regions in how the committed capacity is applied, making them suitable for predictable, long-running workloads.

<Frame>
  <img alt="The image is an infographic titled &#x22;Resource-Based Commitments&#x22; showing key responsibilities and computation benefits, such as specific vCPU and memory amounts, flexibility in regions, discounts, and suitability for predictable compute requirements." />
</Frame>

How CUDs fit with other GCP cost-saving options

* Sustained Use Discounts: Automatically applied when an instance runs for a large portion of the billing month—no commitment required.
* Preemptible Instances: Very low-cost, short-lived VMs for batch and fault-tolerant workloads; pair well with autoscaling and CUDs for mixed workloads.
* Pricing and planning tools: Use GCP calculators and recommendations to model spend-based vs resource-based choices based on historical usage.

> **lightbulb** Choose spend-based commitments for maximum flexibility (variable workloads) and resource-based commitments for maximum discount (predictable workloads). Use GCP planning tools and historical usage to decide which is best.

<Frame>
  <img alt="The image lists three unique features: Sustained Use Discounts, Preemptible Instances, and a Planning Tool, each represented by different colored icons." />
</Frame>

Practical considerations and best practices

* Term lengths: Most CUDs are available for 1-year or 3-year commitments—longer terms usually yield larger discounts.
* Historical analysis: Review historical usage patterns and forecast near-term growth before committing. Model scenarios (e.g., `+10% usage`, `migration to different families`) to understand risk.
* Billing and contractual obligations: Commitments are contractual—you are billed for the committed amount regardless of actual consumption.
* Hybrid strategies: Combine CUDs with sustained use discounts, preemptible instances, and autoscaling to optimize both cost and resilience.
* Comparable offerings: CUDs are similar to savings plans or reserved instances in other clouds—see `AWS Savings Plans` and `Azure Reserved VM Instances` for concept parallels:
  * [https://aws.amazon.com/savingsplans/](https://aws.amazon.com/savingsplans/)
  * [https://learn.microsoft.com/en-us/azure/virtual-machines/reserved-vm-instances/](https://learn.microsoft.com/en-us/azure/virtual-machines/reserved-vm-instances/)

> **warning** CUDs are contractual commitments. If your usage drops below the committed level, you will still be billed for the commitment. Always analyze historical usage and run “what-if” scenarios before committing.

Summary

Committed Use Discounts are a powerful FinOps tool on GCP when you can predict compute needs. Use resource-based commitments for the deepest discounts on consistent workloads and spend-based commitments when you need flexibility. Combine CUDs with other GCP cost controls (sustained use discounts, preemptible instances, autoscaling) and leverage GCP planning tools to maximize savings and minimize risk.

Thanks — that’s it for this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/e2afb350-04ac-4d29-9094-9c32c6ce938e/lesson/d59ac29e-f2a2-46c7-a491-d53ae2023b21)
