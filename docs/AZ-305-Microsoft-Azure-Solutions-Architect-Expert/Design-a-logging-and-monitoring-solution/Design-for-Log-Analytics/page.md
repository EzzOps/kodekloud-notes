# VM Performance
```

After clicking "Done Editing," the heading will be displayed on the canvas.

### Step 2: Adding a Parameter for VM Selection

Next, add a parameter to create a drop-down menu for VM selection. This parameter can be set up using options such as drop-down, time range, resource picker, resource type picker, or location picker.

<Frame>
  ![The image shows a Microsoft Azure Monitor interface with a "New Parameter" window open, allowing users to configure settings for a VM Performance Workbook.](https://kodekloud.com/kk-media/image/upload/v1752866995/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-Azure-workbooks-and-Insights/azure-monitor-new-parameter-vm-settings.jpg)
</Frame>

You can choose between a subscription picker or a resource picker. For our example, we’ll use the resource picker with a Resource Graph query to list all available Virtual Machines.

### Step 3: Setting Up the Resource Graph Query

Utilize the Kusto Query Language (KQL) to list all Virtual Machines with a concise query. Instead of using multiple repetitive queries, implement the refined query below:

```kusto theme={null}
resources
| where type == 'microsoft.compute/virtualmachines'
```

Running this query with all subscriptions selected will populate the drop-down with all Virtual Machines. Click "Save" and then "Done Editing" to apply the configuration.

### Step 4: Adding Performance Metrics

Now, add performance metrics to visualize the data for the selected VMs. Follow these steps:

1. Click "Add Metric" and configure the resource type to Virtual Machine, linking it to the previously defined parameter for dynamic selection.
2. Choose the metric you want to display (e.g., CPU percentage) and set the aggregation method (such as Average).
3. Click "Run Metrics" to generate the visualization. You can adjust the visualization type (bar chart, area chart, etc.) and the graph size as needed.

<Frame>
  ![The image shows a Microsoft Azure Monitor Workbook interface, where a user is editing a metric item and selecting a resource type related to virtual machines. The interface includes options for settings, visualization, and time range.](https://kodekloud.com/kk-media/image/upload/v1752866996/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-Azure-workbooks-and-Insights/azure-monitor-workbook-virtual-machines.jpg)
</Frame>

For additional insights, try adding another metric related to the disk performance. If a selected metric does not show data, switch to another metric with available values.

<Frame>
  ![The image shows a Microsoft Azure Monitor workbook interface displaying a line chart for "Data Disk Bandwidth Consumed Percentage, Average" over time. The left panel includes navigation options like Overview, Activity log, Alerts, and more.](https://kodekloud.com/kk-media/image/upload/v1752866999/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-Azure-workbooks-and-Insights/azure-monitor-workbook-line-chart.jpg)
</Frame>

Once satisfied with your metrics, click "Done Editing" to finalize your workbook. You can also modify parameter settings to enable multi-selection if required.

<Frame>
  ![The image shows a Microsoft Azure portal interface displaying a "VM Performance Workbook" with options to edit parameters and settings. The left sidebar includes navigation options like Overview, Activity log, Alerts, and Workbooks.](https://kodekloud.com/kk-media/image/upload/v1752867004/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-Azure-workbooks-and-Insights/azure-portal-vm-performance-workbook.jpg)
</Frame>

<Frame>
  ![The image shows a Microsoft Azure Monitor dashboard displaying a VM Performance Workbook with a graph of CPU usage over time for selected virtual machines. The sidebar includes options like Overview, Activity log, Alerts, and more.](https://kodekloud.com/kk-media/image/upload/v1752867006/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-Azure-workbooks-and-Insights/azure-monitor-vm-performance-dashboard.jpg)
</Frame>

<Callout icon="lightbulb">
  Remember to save and share your workbook when you’re done to enable team-wide collaboration.
</Callout>

***

## Designing for Azure Insights

Azure Insights extends your monitoring capabilities by providing telemetry data for a broad range of services. In the Azure Monitor, Insights are available for services such as applications, virtual machines, storage accounts, containers, networks, and SQL databases. For exam purposes, focus on the following three core services:

* Application Insights
* VM Insights
* Container Insights

### Application Insights

Application Insights is designed to help you monitor and troubleshoot your application's performance and health. It enables you to track:

* Query and request volumes along with their sources.
* Metrics like availability, performance, latency, and dependency health.
* User behavior and engagement patterns to identify areas for improvement.
* Overall application stack performance through in-depth telemetry data.

### VM Insights

VM Insights offers a detailed overview of the health and performance of your virtual machines. With VM Insights, you can:

* Compare the performance of multiple VMs across different environments.
* Access information on VM properties, running processes, dependencies, and network topology.

### Container Insights

Tailored for Kubernetes workloads, Container Insights monitors containerized environments by providing:

* Detailed performance and memory usage metrics for controllers, nodes, and pods.
* Centralized log collection to facilitate troubleshooting and analysis.

<Frame>
  ![The image is a presentation slide from KodeKloud about "Design for Azure Insights," detailing how to monitor resources using telemetry data, with sections on Application, VM, and Container Insights. It also includes a screenshot of the Azure Monitor Insights Hub, listing various services and features.](https://kodekloud.com/kk-media/image/upload/v1752867007/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-Azure-workbooks-and-Insights/design-for-azure-insights-slide.jpg)
</Frame>

To access these insights, navigate to the Monitor section in the Azure portal. For Virtual Machines, ensure they are onboarded to send telemetry data to the configured workspace. For storage accounts, you can monitor metrics such as transactions, latency, errors, and capacity.

<Frame>
  ![The image shows a Microsoft Azure portal interface displaying a monitoring dashboard for storage accounts, with metrics such as transactions, latency, and errors. The dashboard includes a list of subscriptions and their corresponding performance data.](https://kodekloud.com/kk-media/image/upload/v1752867009/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-Azure-workbooks-and-Insights/azure-portal-storage-monitoring-dashboard.jpg)
</Frame>

Azure Insights provides a rich, holistic view of your resource performance through detailed telemetry.

***

With these guidelines and steps, you now understand how to design robust Azure Workbooks and implement Azure Insights for monitoring resource performance and gathering actionable telemetry data. This approach not only enhances visibility into your environment but also empowers your team to make informed decisions based on real-time metrics and trends.

Next, we will move on to the final topic: Design for Azure Data Explorer.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-305-microsoft-azure-solutions-architect-expert/module/2c624b73-c0ae-4e37-862b-7e9cacbc645b/lesson/1f4861de-33e3-4da0-95cb-33af80e513be" />
</CardGroup>


# Design for Log Analytics

Source: https://notes.kodekloud.com/docs/AZ-305-Microsoft-Azure-Solutions-Architect-Expert/Design-a-logging-and-monitoring-solution/Design-for-Log-Analytics/page

This article outlines design and best practices for Log Analytics, covering data collection, querying, pricing models, data retention, and access control for workspaces.

This article outlines the design and best practices for Log Analytics, a key component of Azure Monitor. It details topics such as data collection, querying, pricing models, data retention, and access control for Log Analytics workspaces.

## What is Log Analytics?

Log Analytics is a fully managed service within Azure Monitor that empowers you to collect, analyze, and visualize data from Azure resources, on‑premises systems, and non‑Azure environments. By onboarding your resources to a Log Analytics workspace, data from diagnostic settings and configurations is centralized and stored in tables, which can then be queried using the powerful Kusto Query Language (KQL).

## Data Collection

Data from a wide range of resources—whether hosted on Azure, on‑premises, or in other environments—can be ingested into a Log Analytics workspace. Any diagnostic settings configured in Azure Monitor send their collected data to the designated workspace. For instance, performance logs from hundreds of virtual machines could be stored in a table named `perf`, while syslogs from Linux systems would be held in a `syslog` table.

## Querying and Consolidation

Kusto Query Language (KQL) is the tool used to query and analyze this collected data, facilitating the creation of detailed reports and visualizations. Consider the following example, which queries the `perf` table to extract performance data related to SQL-related resources:

```kql theme={null}
perf
| where Computer contains "SQL" and ObjectName == "LogicalDisk"
| where CounterName == "% Free Space" and InstanceName == "C:"
| extend TimeInEST = TimeGenerated - 5h
| project TimeInEST, CounterName, CounterValue
```

<Callout icon="lightbulb">
  Learning KQL is highly recommended as it equips you with a powerful tool for troubleshooting, diagnostics, and generating rich workbooks.
</Callout>

## Data Residency

To meet specific data residency requirements, you can create multiple Log Analytics workspaces in different Azure regions. This functionality is particularly useful for organizations that must comply with regulatory mandates or prefer localized data storage.

## Pricing and Data Retention

When designing a Log Analytics solution, it's essential to consider both the pricing model and data retention policies:

* **Pricing:**\
  Choose between per-gigabyte pricing—where you pay based on data ingestion volume—or capacity pricing, which involves pre-purchasing a fixed daily data ingestion capacity (e.g., 100 GB per day). For high-volume environments, capacity pricing may offer significant cost advantages.

* **Data Retention:**\
  By default, data is retained for 30 days at no additional charge. Extended retention beyond 30 days incurs additional costs.

## Data Capping

If you need to restrict the volume of ingested data, data capping rules can be applied. For instance, if you want to limit data ingestion to 1 GB per day, you can configure your data mapping rules to enforce this cap.

## Access Control and Data Mapping

Log Analytics workspaces structure data into various tables for different log types such as Windows event logs, Linux syslogs, performance counters, custom logs, and alerts. You can query these tables with KQL. For example:

```plaintext theme={null}
Syslog
| union Event
| where SeverityLevel == "Error"
```

### Designing Workspace Access Control

Access control for a Log Analytics workspace can be managed using one of the following models:

1. **Centralized:**\
   All data from various resources is collected into a single workspace. This central repository is managed by a dedicated team with access to all data, ensuring streamlined administration.

2. **Decentralized:**\
   Individual teams manage their own workspaces within their respective resource groups, gathering data solely from resources under their control. Although billing is based on overall ingestion volume and retention requirements, each team is responsible for managing their own data.

3. **Hybrid:**\
   For organizations with stringent security and compliance requirements, a hybrid model is ideal. In this configuration, all resource logs are forwarded to a centralized workspace, while critical or sensitive workloads also have their logs ingested into separate, dedicated workspaces.

The following diagram illustrates these different access control designs:

<Frame>
  ![The image illustrates three designs for workspace access control: centralized, decentralized, and hybrid, each with a brief description and diagram.](https://kodekloud.com/kk-media/image/upload/v1752867010/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-Log-Analytics/workspace-access-control-designs.jpg)
</Frame>

### Detailed Access Control Models

* **Centralized Model:**\
  With workspace-level access, you can run queries across all tables within the workspace. This model is ideal for central administration of data.

* **Decentralized Model:**\
  Query scopes are limited to specific resources for which you have read access. This approach suits application teams managing their own resources.

Permissions and scopes are defined at the workspace level for centralized models, whereas decentralized environments use permissions defined at the individual Azure resource level.

## Onboarding Resources to Log Analytics

Onboarding resources to a Log Analytics workspace is well-documented in our [AZ-104: Microsoft Azure Administrator](https://learn.kodekloud.com/user/courses/az-104-microsoft-azure-administrator) course. For a practical demo environment that allows you to test Log Analytics and practice KQL, visit [aka.ms/LA-demo](https://aka.ms/LA-demo).

The diagram below, courtesy of KodeKloud, compares the centralized and decentralized models, detailing access, permissions, and scope:

<Frame>
  ![The image is a diagram from KodeKloud illustrating workspace access control, comparing centralized and decentralized models, including aspects like access, permissions, and scope.](https://kodekloud.com/kk-media/image/upload/v1752867011/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-Log-Analytics/workspace-access-control-diagram.jpg)
</Frame>

This demo workspace is managed by Microsoft and ingests a significant volume of data from various demo workloads—providing numerous tables for you to explore and query even if you do not operate a production environment.

## Configuring Log Analytics Workspaces in the Azure Portal

Log Analytics workspaces can be easily managed and configured directly from the Azure portal. Upon opening your workspace, you'll notice an "access mode" setting that allows you to choose between resource-level permissions or workspace-level permissions.

The screenshot below shows the Azure portal interface for a Log Analytics workspace, displaying key details such as the workspace name, ID, status, location, and subscription information. The left-hand sidebar provides access to various settings and options:

<Frame>
  ![The image shows a Microsoft Azure portal interface displaying details of a Log Analytics workspace, including its name, ID, status, location, and subscription information. The sidebar on the left lists various settings and options related to the workspace.](https://kodekloud.com/kk-media/image/upload/v1752867012/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-Log-Analytics/azure-portal-log-analytics-workspace.jpg)
</Frame>

Both resource-level and workspace-level permissions are available:

* Selecting "workspace permissions only" means that access to the workspace alone is sufficient for viewing data.
* Opting for "resource or workspace permissions" requires permission for both the specific resource and the workspace.

## Next Steps

With the fundamentals of Log Analytics design covered, the next step is to dive deeper into Azure Workbooks and Insights to extract more valuable insights and create advanced visualizations.

Happy querying!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-305-microsoft-azure-solutions-architect-expert/module/2c624b73-c0ae-4e37-862b-7e9cacbc645b/lesson/0a0c8f3e-e780-4e40-a050-1c8313598da8" />
</CardGroup>
