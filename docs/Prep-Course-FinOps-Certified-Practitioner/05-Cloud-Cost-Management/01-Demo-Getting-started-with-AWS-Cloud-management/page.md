# Demo Getting started with AWS Cloud management

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/Cloud-Cost-Management/Demo-Getting-started-with-AWS-Cloud-management/page

Guide for FinOps on using AWS Billing and Cost Management for cost visibility, governance, budgeting, anomaly detection, Savings Plans, CUR exports, and sustainability tools.

Welcome — this guide walks FinOps practitioners through the core areas of the AWS Billing and Cost Management console. Most capabilities for cost visibility, governance, and optimization live here: dashboards, Cost Explorer, budgets, anomaly detection, Savings Plans/reservations, exports for external analytics, and sustainability tools. Below you'll find a practical path to get started, where to click, and how to use the most commonly used tools.

Where to start

1. Sign in to your AWS account.
2. From the AWS Console, open the account menu (top-right) and choose Billing, or select the AWS Billing and Cost Management dashboard from the Services menu.

Dashboard overview
The Billing and Cost Management dashboard provides a high-level snapshot of your cloud spend: total and daily trends, top services by cost, recent activity, and any cost allocation tags in use. Use this view to validate high-level trends before drilling into finer details.

Keep in mind that access to the billing view is commonly restricted. The account that controls billing is normally the management (payer) account in AWS Organizations — not merely the account root user. If you manage FinOps activities, ensure you have the appropriate permissions on the management/payer account so you can access organization-level billing and run cross-account analyses.

> **warning** You must have access to the billing/management (payer) account to view organization-level billing data. Without this access you cannot perform many FinOps analyses.

The dashboard displays cost trends and a service breakdown. Even small accounts show line items (for example, Amazon Route 53, EC2, KMS, taxes). If you need more granular analysis, open Cost Explorer to break down spend by service, usage type, tag, or time window. Scrolling the dashboard also surfaces recent usage and any tags configured for cost allocation—so a consistent tagging strategy and enabling Cost Allocation Tags are important for slicing costs by team, project, or environment.

<Frame>
  <img alt="The image shows an AWS cost management dashboard with a cost and usage graph displaying a breakdown of service costs over time, alongside a menu for billing and usage reports." />
</Frame>

Cost anomaly detection and budgets
AWS Cost Anomaly Detection monitors spend patterns and alerts you to unusual increases. You can define monitors, set thresholds, and wire notifications (SNS, email) so teams are alerted to spikes quickly. Use anomaly detection for automated monitoring and root-cause investigation when unexpected costs appear.

<Frame>
  <img alt="The image is a screenshot of the AWS Cost Anomaly Detection page, outlining features and instructions for setting up automated cost anomaly detection and root cause analysis. It includes options for creating a cost monitor, pricing details, and additional resources." />
</Frame>

> **lightbulb** Start with budgets to set expected spend and receive alerts when you approach or exceed thresholds. Budgets are a foundational control for cost governance.

Data exports and third-party visualization
For advanced reporting or BI integration, export billing data with Cost and Usage Reports (CUR) to an S3 bucket. CUR files are the canonical source for raw usage and cost lines and are commonly consumed by external tools like Tableau or Looker for custom dashboards and cross-functional reporting.

Customer Carbon Footprint Tool
If sustainability metrics are part of your FinOps program, enable the Customer Carbon Footprint Tool (CCFT) to estimate your AWS carbon footprint. Use CCFT outputs for sustainability budgeting, reporting, or compliance work.

Cost allocation and pricing estimation
Under Billing, you’ll find Cost Categories, Cost Allocation Tags, and the AWS Pricing Calculator. Use the allocation tags and categories to map costs to business units or projects for showback/chargeback. Use the Pricing Calculator to estimate costs for new architectures or for procurement planning.

<Frame>
  <img alt="The image shows an AWS console page for the Pricing Calculator with sections explaining how to set account rates, select estimate types, and create bill estimates. The left sidebar contains menu options related to billing and savings plans." />
</Frame>

Savings Plans and recommendations
The Recommendations and Savings Plans areas analyze historical usage and surface potential savings with Savings Plans and Reserved Instances. You can:

* Review recommendations for Compute Savings Plans and Instance Savings Plans
* Explore term options (1-year, 3-year) and payment choices (all upfront, partial, no upfront)
* Use organization-level recommendations to pool utilization across multiple accounts

<Frame>
  <img alt="The image shows an AWS Savings Plans recommendations interface, displaying options for types of savings plans, term lengths, payment options, and analysis periods. It also includes a sidebar menu for billing and cost management features." />
</Frame>

If your organization runs many accounts (for example, 15–20), central reservation and Savings Plan evaluation can greatly increase savings by right-sizing commitments across workloads.

Reservations overview
The Reservations Overview lists current Reserved Instances and helps you manage purchases or view unused reservations. FinOps teams should centralize reservation inventory to avoid duplicate commitments and coordinate purchases to maximize utilization.

<Frame>
  <img alt="The image displays an AWS Billing and Cost Management dashboard in the Reservations Overview section, showing no active reservations or savings." />
</Frame>

Billing preferences and tax settings
At the bottom of the billing console you can configure billing preferences, tax settings, and currency options. These settings are important for correct invoicing, tax treatment, and localized billing views.

Quick reference table — console areas and purpose

| Console area                      | Purpose                                    | Example / Notes                                        |
| --------------------------------- | ------------------------------------------ | ------------------------------------------------------ |
| Dashboard                         | High-level cost trends and recent activity | Start point for exploratory analysis                   |
| Cost Explorer                     | Detailed spend and usage analysis          | Filter by service, tags, usage type, time range        |
| Budgets                           | Set expected spend and generate alerts     | Use for monthly or project-level governance            |
| Cost Anomaly Detection            | Automated monitoring for spend spikes      | Create cost monitors and notification actions          |
| Cost and Usage Reports (CUR)      | Raw billing data export to S3              | Ingest into BI or analytics pipelines                  |
| Savings Plans & Reservations      | Recommendations and purchase management    | Evaluate historical usage for commitments              |
| Cost Allocation Tags & Categories | Map costs to teams/projects                | Enable and propagate tags for showback/chargeback      |
| Customer Carbon Footprint Tool    | Sustainability estimates                   | Use for reporting and internal sustainability programs |

Summary
The AWS Billing and Cost Management console is the central hub for cost visibility, governance, and optimization. To implement effective FinOps practices:

* Ensure you have billing/management (payer) account access.
* Establish a tagging strategy and enable Cost Allocation Tags.
* Create budgets and alerts as primary cost controls.
* Enable Cost Anomaly Detection for automated monitoring.
* Export CUR data for advanced reporting and external BI ingestion.
* Regularly review Savings Plans and Reservations centrally to maximize utilization.
* Use CCFT when sustainability metrics are required.

Links and references

* [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
* [AWS Cost Anomaly Detection](https://aws.amazon.com/aws-cost-management/aws-cost-anomaly-detection/)
* [Cost and Usage Reports (CUR)](https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html)
* [Customer Carbon Footprint Tool (CCFT)](https://aws.amazon.com/aws-cost-management/customer-carbon-footprint-tool/)
* [AWS Pricing Calculator](https://calculator.aws/)
* [Savings Plans](https://aws.amazon.com/savingsplans/)

See you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/b623bd4d-2f47-4afb-a61b-f224315cfbe1/lesson/4d2e5f3e-2efb-4564-847c-f458b68faeb9)
