# Billing 2FA

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/AWS-Fundamentals/Billing-2FA/page

This guide explains how to set up a budget in AWS to manage spending and receive alerts for budget thresholds.

In this guide, we detail how to set up a budget in your AWS account to manage your spending effectively. Establishing a budget not only helps you avoid unexpected charges but also triggers email alerts when your spending nears or exceeds defined limits. This way, you can proactively adjust your AWS services and avoid incurring undesired costs.

## Navigating to the Billing Dashboard

To begin, log in to your AWS console. Locate your account name in the top right corner and select it to access the billing dashboard. This dashboard is your central hub for reviewing payment methods, past invoices, previous monthly payments, and real-time estimates of your current month’s spend. In a new AWS account, the dashboard might initially appear empty; however, as you begin using AWS resources, various fields, columns, and charts will populate with your financial data.

## Setting Up a Budget

Follow these steps to create a budget:

1. In the billing dashboard, navigate to the budget section.
2. Click on **Create a budget**.

When creating a budget, you will be prompted to select a template that best fits your needs. AWS offers built-in templates, such as:

* **Zero Spend Budget:** This template monitors your free tier usage and triggers an alert immediately if your spending exceeds \$0.
* **Monthly Cost Budget:** This budget helps you manage a specific monthly dollar amount (for example, \$100 per month). An alert will be triggered once your cost exceeds this specified threshold.

<Callout icon="lightbulb">
  For this demonstration, we will use the *Monthly Cost Budget* template with a set budget of \$10.
</Callout>

Enter a descriptive name for your budget (e.g., "Monthly Budget \$10") and provide the email address where you would like to receive notifications. AWS sends alerts at milestones such as 85% and 100% of your budget, and also if the forecasted spend is expected to reach 100% of your budget. This proactive alert mechanism is key to preventing overages.

<Frame>
  ![The image shows the AWS Billing Management Console, specifically the "Choose budget type" section, where users can select budget templates like "Zero spend budget" or "Monthly cost budget."](https://kodekloud.com/kk-media/image/upload/v1752858149/notes-assets/images/AWS-Certified-Developer-Associate-Billing-2FA/aws-billing-management-console-budget-types.jpg)
</Frame>

After entering the necessary details, click **Create Budget** to finalize the process. Your newly created budget is now visible in the billing console, and you can revisit or modify its settings at any time by selecting **Edit**.

<Frame>
  ![The image shows an AWS Billing Management Console screen where a user is setting up a monthly cost budget with a budgeted amount of \$10 and an email recipient for notifications.](https://kodekloud.com/kk-media/image/upload/v1752858150/notes-assets/images/AWS-Certified-Developer-Associate-Billing-2FA/aws-billing-management-budget-setup.jpg)
</Frame>

<Callout icon="lightbulb">
  AWS notifies you in three scenarios:

  * When your actual spend reaches 85% of your budget.
  * When it hits 100% of your budget.
  * When the forecasted spend is expected to hit 100% of your budget.
    This system helps ensure that you remain in control of your AWS spending.
</Callout>

You can review your budget details at any time on the billing dashboard. Should you need to make any adjustments, simply click **Edit** and update the relevant settings.

<Frame>
  ![The image shows an AWS Billing Management Console screen displaying details of a budget named "MonthlyBudget10" with a budget amount of \$10.00 and no current spending.](https://kodekloud.com/kk-media/image/upload/v1752858151/notes-assets/images/AWS-Certified-Developer-Associate-Billing-2FA/aws-billing-monthlybudget10-details.jpg)
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/6d3acaeb-020a-4e1e-9bd0-5fc6c50eb164/lesson/f2a805f2-2969-4d82-a242-34eec91f36d5" />
</CardGroup>
