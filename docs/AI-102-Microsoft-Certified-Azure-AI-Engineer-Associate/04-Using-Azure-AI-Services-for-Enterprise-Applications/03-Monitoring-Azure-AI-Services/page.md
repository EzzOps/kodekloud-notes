# Monitoring Azure AI Services

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Using-Azure-AI-Services-for-Enterprise-Applications/Monitoring-Azure-AI-Services/page

Guide to monitoring Azure AI services using metrics, logs, diagnostics, and alerts.

Monitoring Azure AI services ensures performance, reliability, and security for production workloads. Azure provides integrated monitoring features—Metrics, Diagnostic Settings, Logs, and Alerts—that help you track health, analyze behavior, and respond to incidents. This guide shows where to find those features in the Azure portal and how to use them effectively.

Key monitoring components at a glance:

| Component           | Purpose                                                                | Typical use case                                                               |
| ------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Alerts              | Notify or automate when conditions occur                               | Notify on usage spikes, trigger remediation runbooks                           |
| Metrics             | Numeric, time-series measurements (e.g., response time, request count) | Real-time dashboards and trend analysis                                        |
| Diagnostic Settings | Configure export of logs and platform metrics to destinations          | Centralize logs to Log Analytics, archive to Storage, or forward to Event Hubs |
| Logs                | Detailed, timestamped records for auditing and troubleshooting         | Forensics, compliance, and custom alerting with KQL                            |

<Frame>
  <img alt="A presentation slide titled &#x22;Monitoring Azure AI Services Activity&#x22; that shows four monitoring components—Alerts, Metrics, Diagnostic Settings, and Logs—each with an icon and a short bullet description. It summarizes how to track and analyze service performance, security, and operational insights." />
</Frame>

This article walks through the Azure portal to locate these features for an Azure AI (Cognitive) resource (for example, Language or Vision services), and explains how to combine them for operational monitoring and security posture.

## Locate Metrics in the Azure portal

Steps to view metrics for a Cognitive Services / Azure AI resource:

1. In the Azure portal, open your Cognitive Services or specific Azure AI resource (e.g., Language service).
2. In the left-hand menu navigate to Monitoring > Metrics.
3. Select a metric (Total Calls, Latency, Throttled Requests, etc.), choose aggregation (Sum, Average, Count), and set the time range.
4. Add additional metrics to the chart to compare trends and spot correlations.

Metrics are ideal for dashboards, real-time monitoring, and identifying sudden spikes or gradual performance degradation.

Example: viewing the "Total Calls" metric for a deployed language resource:

<Frame>
  <img alt="A screenshot of a metrics dashboard showing the &#x22;Total Calls&#x22; metric for the resource ai102cogservices909 with the aggregation set to Sum. The line chart below shows a flat/zero series across the day (no call activity)." />
</Frame>

Tips:

* Combine related metrics (e.g., Total Calls + Throttled Requests) to detect capacity or throttling issues.
* Pin metrics charts to Azure dashboards for consolidated operational views.
* Use appropriate aggregations for your scenario (Sum for totals, Average/Percentile for latency).

## Diagnostic settings and Logs

Diagnostic settings determine where resource logs and metrics are exported for deeper analysis, retention, or integration with SIEMs.

What diagnostic settings can export:

* Resource logs: request/response logs and resource-specific events.
* Platform metrics (where applicable).
* Activity and audit logs for Azure AI capabilities (for example, Azure OpenAI request usage).

Destinations supported:

| Destination             | Use case                                                                                       |
| ----------------------- | ---------------------------------------------------------------------------------------------- |
| Log Analytics workspace | Query and analyze logs with Kusto Query Language (KQL); build custom dashboards and log alerts |
| Storage account         | Long-term archival and compliance retention                                                    |
| Event Hub               | Stream logs to third-party analytics or SIEMs (Splunk, external systems)                       |
| Partner solutions       | Forward to available partner monitoring/analytics integrations                                 |

To configure diagnostic settings:

1. Open your resource in the Azure portal.
2. Select Diagnostic settings > Add diagnostic setting.
3. Choose the log categories you need (Audit Logs, Request and Response Logs, Trace Logs, Azure OpenAI Request Usage, etc.).
4. Select one or more destinations (Log Analytics, Storage, Event Hub, Partner).
5. Save the diagnostic setting.

<Frame>
  <img alt="A screenshot of an Azure &#x22;Diagnostic setting&#x22; configuration page showing log categories (Audit Logs, Request and Response Logs, Azure OpenAI Request Usage, Trace Logs) and metric options on the left, with destination checkboxes on the right (Send to Log Analytics workspace, Archive to a storage account, Stream to an event hub, Send to partner solution). The top toolbar includes Save, Discard, Delete and Feedback actions." />
</Frame>

<Callout icon="lightbulb">
  Diagnostic Settings do not automatically send logs anywhere — you must create a diagnostic setting and choose a destination (Log Analytics, Storage, Event Hub, etc.) to collect logs for analysis and retention.
</Callout>

Logs stored in Log Analytics are queryable using Kusto Query Language (KQL). Use KQL to:

* Perform forensics and investigations (who accessed what and when).
* Satisfy compliance and retention requirements.
* Create custom dashboards and log-based alert rules.

Useful references:

* [Diagnostic settings for Azure Monitor](https://learn.microsoft.com/azure/azure-monitor/essentials/diagnostic-settings)
* [Kusto Query Language (KQL)](https://learn.microsoft.com/azure/data-explorer/kusto/query/)
* [Azure Monitor Logs overview](https://learn.microsoft.com/azure/azure-monitor/logs/logs-overview)

<Callout icon="warning">
  Carefully consider data sensitivity before exporting request/response logs. Avoid sending Personally Identifiable Information (PII) or secrets to destinations unless you have proper data governance and encryption in place.
</Callout>

## Alerts: detect and respond

Azure Monitor alerts let you create rules that notify teams or trigger automation when metrics or logs meet defined conditions.

Alert types:

| Alert type          | Triggers on                         | Use case                                                           |
| ------------------- | ----------------------------------- | ------------------------------------------------------------------ |
| Metric alerts       | Numeric metric thresholds or trends | High error rates, CPU or request count thresholds                  |
| Log alerts          | Results of a KQL query              | Detect suspicious patterns in logs, failed authentication attempts |
| Activity Log alerts | Azure activity events               | Resource creation, role changes, subscription-level events         |

Typical alert rule workflow:

1. Define the scope (select the resource(s) to monitor).
2. Define the condition (metric threshold or KQL query and evaluation frequency).
3. Define actions by associating an Action Group (email, SMS, webhook, Logic App, Azure Function, Teams, PagerDuty, etc.).
4. Provide alert details (severity, description) and create the rule.

Use cases:

* Notify DevOps on usage spikes or quota exhaustion.
* Trigger automated remediation (e.g., scale-out, restart services).
* Escalate security incidents to on-call via PagerDuty or Teams.

Reference:

* [Azure Monitor alerts overview](https://learn.microsoft.com/azure/azure-monitor/alerts/alerts-overview)

## Putting it together

* Metrics: Best for real-time numeric monitoring and dashboards.
* Diagnostic Settings + Logs: Centralize and retain logs for deep analysis, compliance, and alerting using KQL.
* Alerts: Bridge monitoring and operations by notifying teams and invoking automated responses.

A recommended monitoring approach:

1. Enable Metrics and pin key charts to an Azure dashboard.
2. Configure Diagnostic Settings to send resource logs to a Log Analytics workspace (and archive critical logs to Storage).
3. Create log- and metric-based alerts for operational and security thresholds.
4. Automate common remediations via Action Groups connected to Logic Apps or Functions.
5. Regularly review dashboard trends, alert history, and log queries to refine detection and reduce noise.

Monitoring is the foundation for keeping Azure AI services reliable, performant, and secure. With metrics, diagnostics, logs, and alerts configured, you can build dashboards, runbooks, and automated responses to maintain service health.

## Links and further reading

* [Azure Monitor documentation](https://learn.microsoft.com/azure/azure-monitor/)
* [Diagnostic settings for Azure Monitor](https://learn.microsoft.com/azure/azure-monitor/essentials/diagnostic-settings)
* [Kusto Query Language (KQL) quickstart](https://learn.microsoft.com/azure/data-explorer/kusto/query/)
* [Azure Monitor alerts overview](https://learn.microsoft.com/azure/azure-monitor/alerts/alerts-overview)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/981568f6-848e-45c2-ae00-083b3975ecb5/lesson/5c4e445d-416b-4747-88c3-267e4350f2bc" />
</CardGroup>
