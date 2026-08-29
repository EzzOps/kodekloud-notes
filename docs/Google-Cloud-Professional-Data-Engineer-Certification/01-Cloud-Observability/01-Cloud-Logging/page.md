# Cloud Logging

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Cloud-Observability/Cloud-Logging/page

Overview of Google Cloud Logging, its components, workflow, configuration patterns, and guidance for ingesting, routing, storing, querying, exporting, and monitoring logs for data engineers.

Welcome back — in this lesson we'll cover Cloud Logging: what it is, how it works, and why it matters for data engineers maintaining pipelines and storage systems.

Think of Cloud Logging as the central nervous system of your Google Cloud environment. It ingests logs from applications, VMs, containers, and managed services; indexes and stores them in log buckets; and exposes them for searching, alerting, visualization, and export.

<Frame>
  <img alt="A teal-to-aqua gradient slide with the title &#x22;Cloud Logging&#x22; centered in white text. A small &#x22;© Copyright KodeKloud&#x22; notice appears in the bottom-left." />
</Frame>

Logging guarantees each entry is captured reliably, retained according to your policy, and accessible through tools like Logs Explorer for interactive investigation.

## How Cloud Logging works (high level)

* Every Google Cloud resource (Compute Engine VMs, GKE, Cloud Functions, App Engine, Cloud Storage, and managed services) can emit logs. Logs arrive via:
  * platform integrations,
  * agents (for VMs and some container setups), or
  * the Cloud Logging API and client libraries.
* Incoming logs are ingested into the Logging service, which provides:
  * A log router that filters and routes entries to sinks.
  * Sinks that export logs to destinations such as Cloud Storage, BigQuery, Pub/Sub, or other log buckets (including cross-project/organization sinks).
  * Log buckets where logs are stored and retention policies are applied.
* For interactive investigation, use Logs Explorer in the Cloud Console. It supports advanced queries, filters, and visualizations.

This pipeline captures console actions, API calls, service events, application logs, and audit events across your environment.

## Why Cloud Logging is powerful

* Low-latency ingestion: Logs appear quickly after they are emitted, enabling near real-time troubleshooting.
* Fully managed: Google handles scaling, availability, and the underlying infrastructure.
* Log-based metrics: Turn specific log patterns into metrics to power alerts and dashboards (e.g., count of failed jobs or application errors).
* Rich querying: Logs Explorer offers a powerful query language and UI for filtering, inspecting, and visualizing trends.
* Audit logs: Capture admin activity, data access, and system events—essential for security investigations and compliance.

<Callout icon="lightbulb">
  Note: Data Access audit logs are not enabled by default for many services due to volume and cost. Enable them intentionally if you need detailed access records for troubleshooting or compliance.
</Callout>

<Callout icon="warning">
  Warning: Log retention and export settings affect cost and compliance. Configure retention policies and export sinks to balance long-term storage needs against billing.
</Callout>

## Key components (at-a-glance)

| Component               | Purpose                                              | Example use-case                                        |
| ----------------------- | ---------------------------------------------------- | ------------------------------------------------------- |
| Log router & sinks      | Filter and route log entries to destinations         | Export deletes to Pub/Sub to trigger recovery workflows |
| Log buckets & retention | Store logs and enforce retention policies            | Archive logs for 365 days in a separate bucket          |
| Audit logs              | Track admin activity, data access, and system events | Identify who deleted objects from a bucket              |
| Log-based metrics       | Create metrics from log contents                     | Alert on repeated job failures                          |
| IAM roles               | Control access to view, write, and manage logs       | `roles/logging.viewer`, `roles/logging.logWriter`       |

## Configuration patterns important to data engineers

* Sinks: Use sinks to route audit or application logs to BigQuery for analysis, Cloud Storage for long-term retention, or Pub/Sub for streaming/real-time reaction.
* Retention: Set retention at the log-bucket level to enforce compliance and manage cost.
* Audit Logging: Admin Activity, Data Access, and System Event audit logs give different levels of visibility—enable Data Access selectively.
* Log-based metrics & alerts: Create metrics from log patterns and surface them in Cloud Monitoring to monitor pipeline health.
* IAM granularity: Apply least privilege using logging-specific roles.

## Quick examples

Logs Explorer query to find Cloud Storage object deletes:

```text theme={null}
resource.type="gcs_bucket"
protoPayload.methodName="storage.objects.delete"
protoPayload.resourceName:"your-bucket-name"
```

Create a sink to export delete events to BigQuery (replace `PROJECT_ID` and `DATASET`):

```bash theme={null}
gcloud logging sinks create export-deletes \
  bigquery.googleapis.com/projects/`PROJECT_ID`/datasets/`DATASET` \
  --log-filter='resource.type="gcs_bucket" protoPayload.methodName="storage.objects.delete"'
```

Example: read exported logs in BigQuery with SQL (simplified):

```SQL theme={null}
SELECT
  protoPayload.authenticationInfo.principalEmail AS principal,
  timestamp,
  protoPayload.requestMetadata.callerIp AS caller_ip,
  protoPayload.resourceName AS resource
FROM
  `PROJECT_ID.DATASET.cloudaudit_googleapis_com_activity_*`
WHERE
  protoPayload.methodName = "storage.objects.delete"
ORDER BY timestamp DESC
LIMIT 100;
```

## Example scenario: deleted CSV files in a Cloud Storage bucket

1. Cloud Storage emits audit logs for object create/delete/read operations.
2. Use Logs Explorer to locate `storage.objects.delete` events and see the principal (user or service account), timestamp, and API call.
3. For deeper analysis, export audit logs to BigQuery to run SQL queries over historical events.
4. For real-time reaction (e.g., automatic recovery), route delete events to Pub/Sub and trigger a Cloud Function or Dataflow pipeline.

## Troubleshooting checklist for data engineers

* Verify the relevant audit logs are enabled (Admin Activity vs Data Access).
* Check sink filters and destinations to ensure exports include the desired log entries.
* Confirm IAM: does the user or service account have `roles/logging.viewer` or proper sink writer permissions?
* Inspect log retention for the bucket where logs are stored—older logs may be expired.
* Use log-based metrics to detect recurring failures before they escalate.

## References

* [Cloud Logging overview](https://cloud.google.com/logging/docs)
* [Logs Explorer](https://cloud.google.com/logging/docs/explorer)
* [Cloud Audit Logs](https://cloud.google.com/logging/docs/audit)
* [Exporting logs to BigQuery](https://cloud.google.com/logging/docs/export/bigquery)

Closing

Cloud Logging is more than a repository: it's an integrated observability platform for troubleshooting, security investigations, monitoring, and analytics. For data engineers, mastering log routing, audit logs, and log-based metrics helps maintain reliable and observable data systems.

That’s it for this lesson. See you in the next one.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/d6a06810-5ad4-420a-8025-4b368685733c/lesson/75172213-ed10-4154-95a8-62514bfee068" />
</CardGroup>
