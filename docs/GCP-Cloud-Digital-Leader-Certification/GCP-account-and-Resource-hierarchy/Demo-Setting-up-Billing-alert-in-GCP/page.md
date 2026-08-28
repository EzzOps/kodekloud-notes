# Show the active project ID
gcloud config get-value project

# Describe the current project (returns project number, name, and more)
gcloud projects describe $(gcloud config get-value project)
```

Dashboard overview
Clicking Dashboard opens a project-centric page that aggregates resource summaries, usage charts, and quick links to common services.

<Frame>
  <img alt="A screenshot of the Google Cloud Console dashboard showing project info and service panels (Compute Engine, APIs, Resources, Billing, Monitoring, and Cloud Platform status). The project name &#x22;Learning Google cloud&#x22; and various widgets and charts are visible." />
</Frame>

Key dashboard panels and what they show

| Panel                 | Purpose                                  | Typical actions                                        |
| --------------------- | ---------------------------------------- | ------------------------------------------------------ |
| Project details       | Name, project ID, project number         | Copy IDs for CLI/API use                               |
| Resource summaries    | Recently used services and top resources | Jump to specific services (Compute, Storage, BigQuery) |
| Compute Engine        | VM status and quick-create links         | Create, stop, or connect to VMs                        |
| Billing overview      | Spend, alerts, and billing account links | Review charges and set budgets/alerts                  |
| Monitoring            | Uptime checks and metric charts          | Open Cloud Monitoring dashboards                       |
| Cloud Platform status | Service incidents and outages            | Check current platform health                          |

Activity, audit logs, and recommendations

* Activity: lists who performed which actions in the Console—useful for operational auditing and troubleshooting.
* Recommendations: GCP analyzes your resources and suggests improvements (security, cost optimization, performance).

<Frame>
  <img alt="A screenshot of the Google Cloud Console &#x22;Recommendations&#x22; page showing a card advising to change project-level IAM role grants with a link to remove a role and an estimated &#x22;11,297 excess permissions.&#x22; The top navigation and search bar (Dashboard, Activity, Recommendations) plus export/history/send feedback icons are visible." />
</Frame>

Using Recommendations effectively

* Typical suggestions include reducing overly broad IAM role grants (excess permissions) or rightsizing compute resources to save costs.
* Treat recommendations as starting points—review the details and test changes in a non-production environment before applying them at scale.

Quick links and further reading

* GCP Console documentation: [https://cloud.google.com/docs/overview](https://cloud.google.com/docs/overview)
* Managing projects and resources: [https://cloud.google.com/resource-manager/docs/overview](https://cloud.google.com/resource-manager/docs/overview)
* Cloud Shell: [https://cloud.google.com/shell/docs](https://cloud.google.com/shell/docs)
* Recommendations and optimization: [https://cloud.google.com/recommender/docs](https://cloud.google.com/recommender/docs)

Summary
The GCP Console dashboard is your central navigation hub for inspecting project metadata, launching Cloud Shell, reviewing activity/audit logs, and discovering Recommendations. Use the dashboard to quickly access common services and to get high-level operational and billing insights for your project. We’ll use this dashboard later to demonstrate resource hierarchy and hands-on examples.

That’s it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gcp-cloud-digital-leader-certification/module/b66b4a7d-3fda-4a71-880a-e91e7a6f4afa/lesson/94accd11-01ff-43ac-a673-67cccf4f6f67" />
</CardGroup>


# Demo Setting up Billing alert in GCP

Source: https://notes.kodekloud.com/docs/GCP-Cloud-Digital-Leader-Certification/GCP-account-and-Resource-hierarchy/Demo-Setting-up-Billing-alert-in-GCP/page

Learn to set up billing alerts in GCP to monitor and control your spending effectively.

Welcome to this lesson! In this guide, you'll learn how to set up billing alerts for your Google Cloud Platform (GCP) account to monitor and control your spending effectively. Before you begin, ensure that your GCP account is configured correctly and that you are familiar with its billing details.

<Callout icon="lightbulb">
  Billing alerts are an essential tool for staying within your budget and avoiding unexpected charges.
</Callout>

## Why Set Up Billing Alerts?

When using GCP, especially with a personal account for learning and development, it's easy to leave resources running—like compute instances—that may exceed your free usage limits. Billing alerts notify you when your spending approaches specific thresholds, helping you avoid unforeseen charges.

## Accessing the Billing Console

1. Log in to your GCP Console and verify you’re in the correct project.
2. Use the top search bar to type “billing” and select the billing option, which will open the billing console.
3. In the left-hand panel, click on **Budgets & Alerts**.

## Creating Your First Budget Alert

1. If you don't have any budgets yet, select **Create a Budget**.
2. Name your new budget.
3. Choose the budget period. In this example, we will select a **Monthly** budget that applies to all services within your project.

<Frame>
  ![The image shows a Google Cloud billing interface where a budget is being created. It includes options for setting the budget scope, time range, projects, and services, along with a cost trend graph.](https://kodekloud.com/kk-media/image/upload/v1752875307/notes-assets/images/GCP-Cloud-Digital-Leader-Certification-Demo-Setting-up-Billing-alert-in-GCP/google-cloud-billing-budget-interface.jpg)
</Frame>

4. Click **Next** and set your desired budget amount. For this example, input 10 US dollars. The interface displays historical cost trends on the left, and you may notice that recent spending (e.g., around 0.4 US dollars in previous months) is well below your \$10 threshold.

<Frame>
  ![The image shows a Google Cloud billing interface where a user is setting a monthly budget of 10. A cost trend graph displays actual costs, with a tooltip indicating an actual cost of 0.43 for October 2022.](https://kodekloud.com/kk-media/image/upload/v1752875308/notes-assets/images/GCP-Cloud-Digital-Leader-Certification-Demo-Setting-up-Billing-alert-in-GCP/google-cloud-billing-budget-graph.jpg)
</Frame>

5. Click **Next** to proceed to the alerts configuration. By default, three alert thresholds are set:

   * 50% of the budget (5 US dollars)
   * 90% of the budget (9 US dollars)
   * 100% of the budget

   If the 50% alert threshold is not necessary, remove it by clicking the delete option.

<Frame>
  ![The image shows a Google Cloud billing interface where a user is setting budget alert thresholds. It includes options for setting percentage thresholds and amounts, with a cost trend graph displayed on the right.](https://kodekloud.com/kk-media/image/upload/v1752875309/notes-assets/images/GCP-Cloud-Digital-Leader-Certification-Demo-Setting-up-Billing-alert-in-GCP/google-cloud-billing-budget-alerts.jpg)
</Frame>

6. Define your alert method. Email notifications will be sent to the email address linked to your GCP account—so keep an eye on that inbox.
7. Click **Finish** to create your billing alert.

After completing these steps, you will receive an email notification whenever your spending exceeds the thresholds set for the budget.

<Frame>
  ![The image shows a Google Cloud Billing dashboard with a budget named "learning\_budget" set to a specified amount of \$10.00, with no credits used.](https://kodekloud.com/kk-media/image/upload/v1752875310/notes-assets/images/GCP-Cloud-Digital-Leader-Certification-Demo-Setting-up-Billing-alert-in-GCP/google-cloud-billing-learning-budget.jpg)
</Frame>

## Creating a Resource-Level Budget Alert

In addition to a general account-level budget, you can create a budget alert specifically for a service, such as Compute Engine.

1. Click on **Create Budget** again.
2. Select **Resource-level Budget**.
3. Under services, choose all services by default, then filter by typing "Compute" and select **Compute Engine**.
4. Set your budget amount specifically for Compute Engine usage. For example, set it to 5 US dollars.
5. Click **Next**. If alert thresholds appear, remove any unnecessary ones (like the 50% threshold) and then click **Finish**.

This process creates a second budget alert focused on monitoring Compute Engine consumption.

<Frame>
  ![The image shows a Google Cloud Billing dashboard with a "Budgets & alerts" section, listing two budgets with specified amounts and alert triggers.](https://kodekloud.com/kk-media/image/upload/v1752875311/notes-assets/images/GCP-Cloud-Digital-Leader-Certification-Demo-Setting-up-Billing-alert-in-GCP/google-cloud-billing-budgets-dashboard.jpg)
</Frame>

## Summary

In this lesson, you learned how to set up two types of billing alerts in GCP:

* **Overall Account-Level Alert:** Monitors total spending across all services.
* **Resource-Level Alert:** Focuses on specific services such as Compute Engine.

These billing alerts are crucial for ensuring you remain within your budget and maintain control over your cloud expenditures.

<Callout icon="lightbulb">
  For more detailed GCP billing insights and configurations, check out the [Google Cloud Billing Documentation](https://cloud.google.com/billing/docs).
</Callout>

Thank you for following along. You now have the knowledge to manage your GCP costs more efficiently while safeguarding against unexpected charges.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gcp-cloud-digital-leader-certification/module/b66b4a7d-3fda-4a71-880a-e91e7a6f4afa/lesson/daa36abd-97f8-4ee4-ba43-9dbe39a09b18" />
</CardGroup>
