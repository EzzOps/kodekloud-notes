# Enable and monitor database auditing

Source: https://notes.kodekloud.com/docs/Microsoft-Azure-Security-Technologies-AZ-500/Database-Security/Enable-and-monitor-database-auditing/page

Guide to enable and monitor Azure SQL database auditing, route logs to Log Analytics Storage or Event Hubs, analyze events with KQL, and set retention, alerts, and integrations

Database auditing for Azure SQL is a critical control for security, compliance, and incident investigation. Auditing captures detailed events about database activity — who did what, when, and from where — and helps teams detect threats, demonstrate compliance, and retain forensic evidence.

## Why enable auditing?

| Benefit                | Description                                                                                               |
| ---------------------- | --------------------------------------------------------------------------------------------------------- |
| Compliance & reporting | Produce tamper-evident audit trails to meet regulatory requirements and provide evidence for audits.      |
| Threat detection       | Spot anomalous or suspicious activity (privilege misuse, mass deletions, unusual logins).                 |
| Centralized analysis   | Send audit events to Log Analytics, Storage, or Event Hubs for long-term retention and broader analytics. |
| Retention control      | Configure retention policies to balance compliance needs against storage costs.                           |

## Auditing scope and where to send logs

Auditing can be configured at the server level (applies to all databases on that server) or at the individual database level (applies only to that database). When enabling auditing you can send logs to:

| Destination             | When to use                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------- |
| Log Analytics workspace | Best for fast querying, alerting, and integrating with Azure Monitor and workbooks. |
| Storage account         | Use for long-term retention, offline archiving, or regulatory storage requirements. |
| Event Hub               | Stream events to SIEMs or third-party analytics pipelines.                          |

> **lightbulb** Choose the target that matches your operational and compliance needs: Log Analytics for analysis and alerts, Storage for long-term retention, or Event Hubs for streaming to third-party systems.

## Configure auditing in the Azure portal

1. Open the Azure portal and navigate to your Azure SQL Server or the specific database you want to audit.
2. Select "Auditing" from the security settings.
3. Choose the scope: Server-level or Database-level auditing.
4. Select a target for audit logs — for this guide we use a Log Analytics workspace:
   * Pick the subscription and the Log Analytics workspace you want to use (for example, a workspace created for Microsoft Defender for Cloud).
5. Save the configuration.

I selected Log Analytics, chose the subscription and the Log Analytics workspace (I have a default workspace that was created for [Microsoft Defender for Cloud](https://learn.microsoft.com/azure/defender-for-cloud)), and saved the configuration. The auditing settings were saved successfully.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the SQL database &#x22;db‑adv‑works&#x22; Auditing settings page with Azure SQL Auditing enabled and Log Analytics selected. A pop-up notification in the top-right confirms the auditing settings were successfully saved." />
</Frame>

## Generate audit events (run queries)

To create auditable events, execute normal queries and modification statements from the Query Editor in the portal or from your preferred SQL client.

Example read queries:

```sql theme={null}
-- List all customers
SELECT * FROM [SalesLT].[Customer];

-- List all products
SELECT * FROM [SalesLT].[Product];
```

Example modification (will be captured by auditing — use caution on production data):

```sql theme={null}
-- Replace 'PRODUCT-NUMBER-123' with the actual ProductNumber you want to delete
DELETE FROM [SalesLT].[Product]
WHERE ProductNumber = 'PRODUCT-NUMBER-123';
```

> **lightbulb** When testing deletions or other destructive statements, run them in a development or staging environment, or ensure you have backups/snapshots in place before executing against production.

## Viewing audit logs

* The database Auditing blade in the portal includes a "View audit logs" option, but entries may take time to appear there.
* For faster access, richer searches, and alerting, use the Log Analytics workspace where you directed the audit logs.

> **lightbulb** Viewing audit logs from the database Auditing blade may show a delay. For more flexible analysis and faster querying, use the Log Analytics workspace where you sent the audit logs.

## Analyze audit events in Log Analytics (KQL)

Audit events are typically available in the AzureDiagnostics table and filtered by Category == "SQLSecurityAuditEvents". Use Kusto Query Language (KQL) to filter, aggregate, and visualize events.

Examples:

Count SELECT statements by statement text and user:

```kql theme={null}
AzureDiagnostics
| where Category == "SQLSecurityAuditEvents"
| where statement_s contains "SELECT"
| summarize count() by statement_s, server_principal_name_s
| order by count_ desc
```

Compact view showing recent SELECT statements with user and resource:

```kql theme={null}
AzureDiagnostics
| where Category == "SQLSecurityAuditEvents"
| where statement_s contains "SELECT"
| project TimeGenerated, server_principal_name_s, statement_s, Resource
| sort by TimeGenerated desc
```

Tips:

* Column names may vary with configuration; common fields include TimeGenerated, statement\_s, server\_principal\_name\_s, client\_ip\_s, Resource, and action\_name\_s.
* Extend queries to filter by TimeGenerated, Resource (database name), client\_ip\_s, or action\_name\_s for precise results.

## Notes

* Audit column names can differ depending on the version and configuration; use the Log Analytics schema viewer or run a broad query to inspect available fields.
* If you need long-term archival beyond Log Analytics retention, combine Log Analytics with a Storage account or export via Event Hub.

## Next steps (automation & scaling)

* Create alerts in Azure Monitor based on KQL queries to notify on suspicious actions (e.g., frequent failed logins or mass deletes).
* Integrate Event Hub to stream audit events to your SIEM or third-party analytics.
* Implement a retention and archival policy: store critical audit trails in Storage for compliance and keep shorter, queryable windows in Log Analytics for day-to-day operations.

## Links and references

* [Azure SQL Database auditing overview](https://learn.microsoft.com/azure/azure-sql/database/auditing-overview)
* [Log Analytics query language (Kusto Query Language)](https://learn.microsoft.com/azure/data-explorer/kusto/query/)
* [Microsoft Defender for Cloud](https://learn.microsoft.com/azure/defender-for-cloud)

- [Watch Video](https://learn.kodekloud.com/user/courses/microsoft-azure-security-technologies-az-500/module/d199f126-f1df-43a8-bd3d-68cd689d509d/lesson/55cf9378-e717-4960-b73b-320fc733c7af)
