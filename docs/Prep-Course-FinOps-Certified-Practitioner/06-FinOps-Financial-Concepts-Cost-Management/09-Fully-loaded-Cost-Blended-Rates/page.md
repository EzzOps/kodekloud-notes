# Fully loaded Cost Blended Rates

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/FinOps-Financial-Concepts-Cost-Management/Fully-loaded-Cost-Blended-Rates/page

Explains fully loaded cloud costs and blended rates to improve budgeting, chargebacks, and decisions using examples and implementation tips

Welcome. In this lesson we cover two essential FinOps concepts for understanding cloud spend: fully loaded cost and blended rates. These help you see the full economic impact of running services, improve budgeting, and enable fair chargebacks across teams.

To make this tangible, imagine you run a cloud-based pizza delivery app. The app uses compute, databases, storage, and many supporting services. Your cloud bill includes more than just CPU minutes — to understand the true cost you must consider the fully loaded cost: every layer that contributes to the service.

In the pizza-shop analogy, monthly costs don’t stop at ingredients. You also pay rent, salaries, software subscriptions, and training.

<Frame>
  <img alt="The image shows an iceberg diagram labeled as &#x22;Fully Loaded Cost and Blended Rates&#x22; with &#x22;Pizza Ingredients&#x22; above the water and &#x22;Rent&#x22; and &#x22;Staff&#x22; below the water, indicating visible and hidden costs." />
</Frame>

Cloud costs follow the same layered structure. Below is a concise comparison you can reference when categorizing your expenses.

| Cost Category  |                                      What it includes | Example (pizza analogy / cloud)                                            |
| -------------- | ----------------------------------------------------: | -------------------------------------------------------------------------- |
| Direct costs   |    Resources directly billed for running the workload | Pizza ingredients / Compute, Storage, Network, Databases                   |
| Indirect costs |       Supporting infrastructure and platform services | Ovens, maintenance / Monitoring, Backups, Security services                |
| Overhead       | Organizational and shared expenses allocated to teams | Rent, staff, training / Support plans, Governance, Tooling, Certifications |

<Frame>
  <img alt="The image is a diagram titled &#x22;Fully-loaded Cost Components,&#x22; categorizing costs into Direct, Indirect, and Overhead Costs with examples like Compute, Support Plans, and Training." />
</Frame>

Why fully loaded cost matters

* Teams that only measure raw compute will often underestimate the true cost of running a service.
* Including indirect and overhead costs gives product owners and finance a realistic unit cost to evaluate ROI and pricing decisions.
* Fully loaded cost enables defensible internal chargebacks or showbacks and reduces cross-team disputes.

## Blended rates: definition and example

A blended rate is the weighted average unit cost (for example, cost per hour or cost per vCPU-hour) across different purchase types and instance families. If your pizza app runs On‑Demand, Reserved, and Spot instances, each has a different hourly price. The blended rate answers: what is the average cost per hour across all of that usage?

Example scenario (rounded for clarity):

| Purchase type |  Total cost |     Hours used |         Implied unit cost |
| ------------- | ----------: | -------------: | ------------------------: |
| On‑Demand     |     \$4,000 |      4,000 hrs |               \$1.00 / hr |
| Reserved      |     \$2,400 |      4,000 hrs |               \$0.60 / hr |
| Spot          |       \$400 |      2,000 hrs |               \$0.20 / hr |
| **Total**     | **\$6,800** | **10,000 hrs** | **Blended = \$0.68 / hr** |

Blended rate calculation (Python example):

```python theme={null}
