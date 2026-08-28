# Demo Exploring Logs Explorer

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Cloud-Observability/Demo-Exploring-Logs-Explorer/page

Hands-on guide to creating and locating Cloud Logging entries in GCP using Cloud Shell and Logs Explorer, with resource and time filters, full-text and structured JSON queries for troubleshooting

Hello, and welcome back.

In this lesson we'll do a hands-on exploration of Logs Explorer in Google Cloud Platform (GCP). You'll generate a log entry from Cloud Shell and then locate and filter it using Logs Explorer.

Prerequisites:

* Access to the GCP Console.
* Permissions to open Cloud Shell and write logs in the project.

<Callout icon="lightbulb">
  If this is your first time opening Cloud Shell, it may take a couple of minutes to provision a temporary VM and workstation. Authorize when prompted.
</Callout>

## 1) Open Cloud Shell and create a log entry

1. In the GCP Console, open Cloud Shell (the terminal at the top-right).
2. If prompted, click Authorize and wait for the terminal to become ready.

Run this command to write a JSON payload into Cloud Logging. The example below creates a log named `my-test-log` with two JSON fields:

```bash theme={null}
gcloud logging write --payload-type=json my-test-log '{ "message": "My second entry", "weather": "partly cloudy" }'
```

Expected output:

```text theme={null}
Created log entry.
```

What this does:

* `gcloud logging write` writes a single log entry to Cloud Logging.
* `--payload-type=json` tells Cloud Logging the entry payload is structured JSON, so fields like `weather` are indexed in `jsonPayload`.
* `my-test-log` is the log name (appears under the Logs Explorer).
* The JSON string is the payload; here we include `message` and `weather` fields.

Logs are now ingested into the project's Logs Explorer.

<Callout icon="lightbulb">
  New log entries can take a few seconds to appear in Logs Explorer. If your entry does not show up immediately, wait a moment and refresh or re-run your query.
</Callout>

## 2) Open Logs Explorer and filter by resource

1. In the GCP Console search bar, search for "Logs Explorer" and open it.
2. Logs Explorer opens with a default time range (for example, the last hour). Adjust the time range if needed.

To narrow the scope of your search:

* Click the resource selector (it may show "All resources") and choose `global` when the log was written from Cloud Shell or the Cloud Console.
* Alternatively, pick a specific resource type (for example, `BigQuery`, `GCE VM Instance`, `Cloud Function`, etc.) to restrict results to that product.

After selecting the resource, click Apply.

Example display (Logs Explorer output):

```text theme={null}
Showing logs for last 1 hour from 2025-10-23 20:53 to 2025-10-23 21:53
2025-10-23 21:52:46.509  My second entry
```

Selecting the correct resource (such as `global`) ensures you're searching the right scope for the entry you created.

## 3) Filtering by other resources (network, VPC)

If you need to search for network-related logs, choose the relevant networking resource in the resource selector (for example, VPC). You can also use a structured filter in the query bar. Example:

```text theme={null}
resource.labels.network_id="6725867803041032465"
```

Note: If no logs exist for that network ID, Logs Explorer will return no results—this is expected if no service has emitted logs for that resource. For VPC flow logs specifically, ensure flow logging is enabled for the subnet or VM.

## 4) Using the search bar and full-text search

Logs Explorer lets you do both full-text searches and structured field queries.

* Full-text search example — find any log mentioning the word `weather`:

```text theme={null}
SEARCH("weather")
```

* Structured field filter example — search the indexed JSON field created by the `--payload-type=json` option:

```text theme={null}
jsonPayload.weather="partly cloudy"
```

Use full-text `SEARCH()` when you're unsure of exact field names; prefer structured filters like `jsonPayload.<field>` when you want precise matches and more performant queries.

## 5) Practical use case: Airflow (Cloud Composer) troubleshooting

For data engineers: when an Airflow job (Cloud Composer) has issues and the Airflow UI doesn't show logs, check Logs Explorer. Cloud Composer pushes task, scheduler, and worker logs to Cloud Logging, so error messages and stack traces are often available in Logs Explorer even if the UI is unavailable.

## Quick reference

| Task                         | Command / Filter                                                                                                      | Notes                                                     |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Write a JSON log entry       | `gcloud logging write --payload-type=json my-test-log '{ "message": "My second entry", "weather": "partly cloudy" }'` | Writes a single structured log entry to `my-test-log`.    |
| Full-text search             | `SEARCH("weather")`                                                                                                   | Finds the term anywhere in the log text or payload.       |
| Structured JSON field filter | `jsonPayload.weather="partly cloudy"`                                                                                 | Query the indexed `jsonPayload` fields for exact matches. |
| Filter by network ID         | `resource.labels.network_id="6725867803041032465"`                                                                    | Use when searching for VPC or network-related logs.       |

## Summary

* Use `gcloud logging write` to create test log entries or rely on services that send logs automatically.
* In Logs Explorer, set the time range and choose the correct resource (for example, `global`, `BigQuery`, `GCE VM Instance`, `VPC`).
* Use `SEARCH("...")` for full-text searches and `jsonPayload.<field>` for structured JSON fields.
* Logs Explorer is essential for debugging services (including Cloud Composer / Airflow) and locating error traces.

## Links and References

* [Cloud Logging overview](https://cloud.google.com/logging/docs)
* [gcloud logging write documentation](https://cloud.google.com/sdk/gcloud/reference/logging/write)
* [Cloud Shell documentation](https://cloud.google.com/shell/docs)
* [Cloud Composer (Airflow) logging](https://cloud.google.com/composer/docs/how-to/monitoring/logging)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/d6a06810-5ad4-420a-8025-4b368685733c/lesson/91ab97dc-be01-460b-9eb5-b10284187b1f" />
</CardGroup>
