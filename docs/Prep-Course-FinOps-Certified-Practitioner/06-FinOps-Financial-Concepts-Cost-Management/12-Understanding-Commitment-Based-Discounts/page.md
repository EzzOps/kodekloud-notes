# Understanding Commitment Based Discounts

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/FinOps-Financial-Concepts-Cost-Management/Understanding-Commitment-Based-Discounts/page

Describes cloud commitment-based discounts, reserved instances, payment options, and strategies to trade flexibility for cost savings

Welcome back. Predicting cloud usage and spend is hard—so committing to planned, steady usage can unlock significant discounts. This lesson explains commitment-based discounts: what they are, how they work, and how to evaluate them strategically so you trade flexibility for savings without unnecessary risk.

## How commitment-based discounts work

* Providers offer deeper discounts in exchange for predictable, long-term commitments to usage or spend.
* The basic trade-off is commitment versus discount: larger commitments in capacity or duration typically yield larger percentage savings.
* Common commitment terms are 1 or 3 years; enterprise customers may negotiate multi-year or customized arrangements.
* Savings typically range from about 20% up to 70% off On‑Demand rates, depending on the product, term length, and payment option.
* Best practice: spread commitments across a portfolio (instance types, regions, or accounts) to balance risk and maintain flexibility.

When to consider commitments:

* Your workload runs continuously or is highly predictable.
* FinOps or engineering teams must lower cloud spend.
* You’ve already right-sized and optimized resources; commitments are the next lever.
* You require steady, predictable spend throughout the year.

> **lightbulb** Before committing, establish a clear baseline of usage and ensure workloads are stable and right-sized. Commitment discounts are most effective when you can forecast steady demand.

<Frame>
  <img alt="The image lists five factors to consider for commitments: stable workloads, cost optimization pressure, mature environments, budget certainty, and financial impact." />
</Frame>

## Reserved Instances (RIs): the classic model

Reserved Instances let you purchase a fixed commitment for a specific instance type and region (or Availability Zone) for a set term—typically 1 or 3 years. When a running instance matches the reservation attributes, the reservation automatically applies and reduces the effective hourly cost.

Key considerations:

* RIs provide predictable, high-percentage savings but reduce flexibility if your usage changes.
* They work best for baseline workloads you expect to run continuously.
* Monitor utilization: unused reserved capacity still incurs cost for the duration of the term.

### Payment options for RIs

Payment choice affects upfront cash flow, effective hourly rate, and total savings. Use the table below to compare common options and decide based on budget and risk tolerance.

| Payment Option  |                                  Upfront Cost |                                   Effective Hourly Charge | Best for                                                              |
| --------------- | --------------------------------------------: | --------------------------------------------------------: | --------------------------------------------------------------------- |
| All Upfront     |                High (full term paid up front) |                                  Lowest hourly equivalent | Organizations with capital to invest and desire for maximum % savings |
| Partial Upfront | Medium (some paid up-front, remainder hourly) |                                                    Medium | Teams balancing cash flow and higher savings                          |
| No Upfront      |                      Low (no initial payment) | Higher than All/Partial but still discounted vs On‑Demand | Teams with limited capital who still want committed savings           |

Note: Generally, paying more upfront yields larger percentage savings—but increases financial exposure if usage patterns change.

<Frame>
  <img alt="The image is a table comparing different types of reserved instances in terms of upfront cost, hours, and rate per hour. It details the cost and rate benefits for all upfront, partial upfront, and no upfront payment models." />
</Frame>

## RI types and typical use cases

Two common RI variants provide different flexibility/savings trade-offs:

* Standard RIs: deliver the highest savings but are the least flexible. They are ideal when instance attributes (family, OS, tenancy) are stable.
* Convertible RIs: provide lower discounts than Standard RIs but allow modification of attributes (instance family, OS, tenancy) within provider rules—useful when you expect some change in instance types.

Typical use cases:

* Database servers with predictable capacity requirements.
* Web servers supporting steady traffic patterns.
* Always-on development or CI environments that run continuously.

| RI Type        | Flexibility                         | Typical Use Cases                                        |
| -------------- | ----------------------------------- | -------------------------------------------------------- |
| Standard RI    | Low (high savings, limited changes) | Stable DBs, baseline web tiers                           |
| Convertible RI | Higher (swap families/attributes)   | Environments expecting growth or instance family changes |

Think of RIs as part of your cost foundation: identify baseline workloads and apply commitments strategically across a portfolio to reduce exposure.

<Frame>
  <img alt="The image provides a deep dive into Reserved Instances (RIs), detailing two types—Standard and Convertible—and their best use cases, including database servers, web servers, and development environments." />
</Frame>

## Summary — plan commitments strategically

* Commitment-based discounts exchange flexibility for cost savings. Only evaluate commitments after you have accurate baseline usage and have completed right-sizing and optimization.
* Use a portfolio approach (diversify across instance types, regions, and accounts) to mitigate risk.
* For organizations with large predictable spend, even single-digit percentage improvements can yield substantial dollar savings.

If you prefer more flexibility while still securing savings, consider modern alternatives (for example, Compute Savings Plans) that we’ll cover next: how they differ from Reserved Instances, when to choose them, and how they fit into a broader cloud cost optimization strategy.

Thanks for reading.

## Links and references

* [Cloud cost optimization basics](https://cloud.google.com/solutions/cost-optimization)
* [AWS Savings Plans and Reserved Instances](https://aws.amazon.com/ec2/pricing/reserved-instances/)
* [Kubernetes cost management and FinOps resources](https://finops.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/e2afb350-04ac-4d29-9094-9c32c6ce938e/lesson/a5847b9c-00af-403a-b144-97343882b209)
