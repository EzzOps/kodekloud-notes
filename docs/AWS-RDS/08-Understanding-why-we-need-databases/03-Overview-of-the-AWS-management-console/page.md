# Overview of the AWS management console

Source: https://notes.kodekloud.com/docs/AWS-RDS/Understanding-why-we-need-databases/Overview-of-the-AWS-management-console/page

Introduction to the AWS Management Console, navigating services, managing regions, service limits, and creating cost budgets to monitor and control cloud spending.

Welcome back. This lesson includes several demos and labs, so start with a quick orientation to the AWS Management Console to follow along confidently.

When you sign in to AWS, the first page you see is the AWS Management Console — the central landing page for discovering and navigating AWS services. Key things to verify right away:

* Region: Confirm the active region in the top-right (for example, Frankfurt). When following demos in your own account, choose a region geographically close to you to reduce latency and, when applicable, costs.
* Navigation: Use the Services menu or the search bar to find services quickly. For example, go to Database → [Amazon RDS](https://learn.kodekloud.com/user/courses/aws-rds) to open the RDS console.

If you open a service and want to return to the console home, click the AWS logo at the top-left. Recently visited services also appear on the console home, so you can click a recently visited [RDS](https://learn.kodekloud.com/user/courses/aws-rds) link to jump straight back to the RDS dashboard.

Note about service limits: AWS enforces default service quotas (limits). For example, many accounts start with a default quota of 40 [RDS](https://learn.kodekloud.com/user/courses/aws-rds) DB instances per region. If you need higher limits, request a quota increase through the AWS Support Center.

<Callout icon="lightbulb">
  Always clean up resources you create during practice (stop/delete instances, snapshots, clusters, etc.). Unused resources can still incur charges.
</Callout>

## Monitoring spend with Budgets

If you’re new to AWS or using the Free Tier, create an AWS Budget to receive alerts before costs grow unexpectedly. Budgets let you track costs by account, service, and tags, and can notify you when thresholds are reached.

Quick steps to create a cost budget:

1. In the AWS Management Console search bar type "budgets" and open the Budgets page (under Billing).
2. Click Create budget.
3. Choose Cost budget. For more granular control (accounts, services, tags) select the advanced/custom options; otherwise use the default cost budget.
4. Choose recurrence — select Recurring for ongoing monitoring and set a start date (for example, the start of the month).
5. Set the budget amount and currency (for example, enter 25 for a \$25/month budget).
6. Click Next and add alert thresholds (for example, 80% to receive a notification when spend reaches $20 on a $25 budget).
7. Enter the email address that should receive alerts.
8. Review the budget settings and click Create budget.

Budget settings at a glance:

| Setting                 | Purpose                      | Example                                     |
| ----------------------- | ---------------------------- | ------------------------------------------- |
| Budget type             | Defines what you're tracking | Cost budget                                 |
| Recurrence              | How often the budget resets  | Recurring — monthly                         |
| Amount & currency       | Spending limit to monitor    | \$25 USD                                    |
| Alert thresholds        | When notifications are sent  | 80% (notify at \$20)                        |
| Notification recipients | Who receives alerts          | [team@example.com](mailto:team@example.com) |

<Callout icon="lightbulb">
  Tip: Use tags and service filters when creating budgets to monitor specific projects or resources (for example, only RDS or only a particular project tag).
</Callout>

<Frame>
  <img alt="A screenshot of the AWS Billing &#x22;Budgets&#x22; page for a budget named &#x22;RDS Course,&#x22; showing budget health with current spend (0.94 of 25.00) and forecasted spend (2.27 of 25.00). The details panel lists a $25.00 monthly cost budget with a start date of 2023-08-01." />
</Frame>

Setting a budget helps you track project spend and receive email alerts when thresholds are reached so you can take action before unexpected charges appear.

Links and further reading

* AWS Budgets documentation: [https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)
* AWS Billing and Cost Management: [https://aws.amazon.com/aws-cost-management/](https://aws.amazon.com/aws-cost-management/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/bfb32eae-f423-4a2e-9ca1-60adc0ac3ff0/lesson/dfeb170f-7f77-434d-8155-e5a291198e9d" />
</CardGroup>
