# SSH into the Linux VM (from your local machine)
ssh kodekloud@20.242.246.105

# Install the stress tool (if not already installed)
sudo apt install stress -y
```

After installation, launch a CPU stress test. For example, to stress 4 CPU cores for 1000 seconds, run:

```bash theme={null}
# Switch to root if necessary
sudo -s

# Run the stress test
stress -c 4 -t 1000
```

You will see the CPU usage spike in real time on the monitoring dashboard. The next step is to monitor this spike until the five-minute average CPU usage exceeds 80%, which will trigger the alert rule.

![The image shows a Microsoft Azure monitoring dashboard displaying a line chart of CPU usage percentage for a virtual machine named "linux-ra-vm." The chart indicates fluctuations in CPU usage over a specified time period.](https://kodekloud.com/kk-media/image/upload/v1752881709/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Enable-Azure-monitor-Alerts/azure-monitoring-cpu-usage-chart.jpg)

Once the average CPU usage exceeds the threshold, you receive an email notification. For example, you might see an alert message indicating that the CPU usage is above 80%:

![The image shows an Azure alert notification for a virtual machine, indicating that the CPU percentage exceeded a threshold of 80%. The alert details include resource ID, metric name, and time aggregation.](https://kodekloud.com/kk-media/image/upload/v1752881710/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Enable-Azure-monitor-Alerts/azure-alert-cpu-threshold-exceeded.jpg)

Additionally, verify the alert by checking the Virtual Machine’s activity logs or the Alerts section in the Azure portal:

![The image shows a Microsoft Azure monitoring dashboard displaying a line chart of CPU usage for a virtual machine, with the CPU percentage reaching approximately 99.84%. A time range selection menu is open on the right side.](https://kodekloud.com/kk-media/image/upload/v1752881712/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Enable-Azure-monitor-Alerts/azure-monitoring-dashboard-cpu-usage.jpg)

***

## Managing and Closing Alerts

After an alert is triggered, you can manage it through the Azure portal. In the Alerts blade, update the user response status (for example, marking it as acknowledged if the team is investigating) or close the alert once the issue is resolved. You can also stop the stress test on the VM to allow the CPU usage to return to normal levels.

For example, to safely end the stress test, you might run the following command to stress the system briefly before the load drops:

```bash theme={null}
sudo stress --cpu 8 --io 4 --vm 2 --vm-bytes 128M --timeout 10s
```

This command runs the stress test for a short duration and then terminates it, letting the VM cool down. If the alert does not close automatically, you can manually close it in the Azure portal.

***

## Conclusion

This article demonstrated how to configure Azure Monitor Alerts for various scenarios, from Log Analytics to Virtual Machines. By defining the scope, condition, action group, and rule details, you can effectively monitor your resources, receive timely notifications, and automate responses. This setup is critical to maintaining a reliable and responsive environment, especially for production systems.

Another important topic is configuring diagnostic logging properties to further enhance your ability to monitor and troubleshoot your Azure resources.

Happy monitoring!

- [Watch Video](https://learn.kodekloud.com/user/courses/microsoft-azure-security-technologies-az-500/module/7b98ab58-5aa5-4f2b-9cfa-fdfef40ddc37/lesson/701187e4-29e5-4c38-9987-388a55cec2cf)


# Enable Log Analytics

Source: https://notes.kodekloud.com/docs/Microsoft-Azure-Security-Technologies-AZ-500/Azure-Monitor/Enable-Log-Analytics/page

This guide covers key features of Azure Log Analytics, workspace setup, and best practices for data collection, visualization, and retention.

Azure Log Analytics is a powerful service that stores, analyzes, and visualizes log data from a wide range of sources—including Azure resources, other cloud providers, and on-premises systems. This guide covers the key features of Log Analytics, how to set up a workspace, and best practices for data collection, visualization, and retention.

## Data Collection and Visualization

Azure Log Analytics collects log data by ingesting outputs from various resources into a centralized workspace. Once the data is stored, you can leverage the Kusto Query Language (KQL) to generate detailed reports and visualizations. For instance, the sample query below retrieves the count of successful SQL database authentications over time, then renders the results as a time chart:

```kusto theme={null}
AzureDiagnostics
| where Category == 'SqlSecurityAuditEvents' and action_page_s == 'DATABASE AUTHENTICATION SUCCEEDED'
| summarize count() by TimeGenerated, server_principal_name_s
| sort by TimeGenerated
| render timechart
```

The resulting time chart provides insights into user authentication activities, making it easier to monitor system access and detect anomalies.

> **lightbulb** For more information on crafting efficient queries with KQL, refer to the [Kusto Query Language documentation](https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/).

## Creating a Log Analytics Workspace

Before you can ingest data, you need to create a Log Analytics workspace in Azure. This workspace serves as the centralized repository where you collect, analyze, and visualize data from your resources. You can deploy multiple workspaces across different regions based on business needs or compliance requirements.

> **lightbulb** If your environment spans production and disaster recovery (DR) regions, consider setting up separate workspaces. This approach helps maintain data isolation and ensure that production data remains compliant with designated regional policies.

After creating a workspace using the Azure Portal—typically starting with the default "pay-as-you-go" pricing tier—data ingestion begins immediately. If your usage exceeds 100 GB per day, switching to a commitment tier can help reduce the per-gigabyte cost.

## Pricing and Data Retention

Log Analytics pricing is determined mainly by:

1. **Data Ingestion Costs** – billed per gigabyte of data ingested.
2. **Data Retention Costs** – based on the duration logs are retained.

By default, the service includes 30 days of free data retention. Should your requirements call for longer retention (for example, 180 days), you'll need to adjust the workspace settings accordingly. This may involve additional costs, particularly when extending retention for data types such as activity logs, which default to 90 days.

## Onboarding and Integrating Resources

A Log Analytics workspace can aggregate data from numerous sources including:

* Azure, AWS, GCP, and on-premises environments.
* Agents and services such as Azure Arc.
* Data collected from Application Insights and Microsoft Sentinel.

Keep in mind that if you integrate with Sentinel, additional charges apply to both Sentinel and the associated Log Analytics data ingestion.

## Setting Up a Workspace in the Azure Portal

To set up a new Log Analytics workspace, follow these steps:

1. Locate and click on "Log Analytics workspaces" in the Azure Portal.
2. Create a new workspace by specifying a resource group (e.g., "RG Monitoring") and a workspace name (e.g., "LAW Monitoring").
3. Choose the region where the workspace will reside (e.g., East US).
4. Confirm the pricing tier, which defaults to pay-as-you-go. Upgrade to a commitment tier if you expect high data ingestion volumes (greater than 100 GB per day).

After completing these steps, onboard your resources to begin collecting and analyzing log data.

![The image shows a setup interface for creating a Log Analytics workspace in Azure, alongside features like workspace, data isolation, and storage of insights and sentinel data.](https://kodekloud.com/kk-media/image/upload/v1752881712/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Enable-Log-Analytics/azure-log-analytics-workspace-setup.jpg)

This concludes the walkthrough on setting up and understanding the basics of Log Analytics. Stay tuned for more insights on managing connected sources and optimizing your log analytics strategy.

For further reading, consider exploring these resources:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/microsoft-azure-security-technologies-az-500/module/7b98ab58-5aa5-4f2b-9cfa-fdfef40ddc37/lesson/47dc7a06-c8b5-4a40-9448-62c31b4f2a75)
