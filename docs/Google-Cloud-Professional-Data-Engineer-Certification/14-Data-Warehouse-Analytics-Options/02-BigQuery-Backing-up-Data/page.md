# BigQuery Backing up Data

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Warehouse-Analytics-Options/BigQuery-Backing-up-Data/page

Guide to BigQuery Time Travel for querying and restoring historical table snapshots, configuring retention, using bq CLI, and best practices to prevent accidental data loss

Accidents happen — someone runs the wrong query or accidentally drops a production table. That scenario is common and can cause significant downtime if production data is lost. BigQuery Time Travel recovery helps you access historical snapshots and restore deleted or modified tables with simple SQL or CLI commands.

In this article you'll learn:

* What BigQuery Time Travel is and how its retention window works
* How to query historical snapshots
* How to restore data into a new or existing table using SQL and the `bq` CLI
* Best practices to reduce the risk of accidental data loss

## How BigQuery Time Travel works

BigQuery keeps historical snapshots of table data for a configurable retention window. This enables you to query a table as it existed at a previous point in time and recover data without complex backups.

* The active table is the live version used by your applications.
* If that table is deleted or modified accidentally, Time Travel lets you go back to any point in time within the table's retention window and restore the table to that state.
* By default, the retention window is 7 days. You can extend this up to 90 days per table.

Picture this: someone drops the payroll table. Using Time Travel you identify the correct point-in-time snapshot and recreate the table from that snapshot — payroll is back online and people get paid.

<Frame>
  <img alt="An infographic titled &#x22;BigQuery – Time Travel Recovery&#x22; showing a four-step flow: Table (active data) → Delete (table removed) → Time Travel (point-in-time) → Recover (restore table). It also notes retention is typically 7 days by default and can be extended up to 90 days." />
</Frame>

## Quick exam-style question

A common exam question is: What is the default time travel retention period in BigQuery?

* Options might include: 24 hours, 7 days, 30 days, 90 days.
* Correct answer: 7 days by default. You can increase this to up to 90 days by configuring the table's time travel retention.

<Callout icon="lightbulb">
  Time Travel retains snapshots only for the table's configured retention window (default 7 days). Once that window expires, historical snapshots are no longer available for recovery.
</Callout>

## Accessing historical data and restoring tables

Note: Time Travel can be used even if the table was deleted, provided the required point-in-time snapshot is still within the retention window.

Below are the most common, practical approaches to access historical data and recover tables.

### 1) Query a table as of a past time (SQL)

Use `FOR SYSTEM_TIME AS OF` to query the table state at a specific timestamp or relative time.

Example — query the table as it existed 1 day ago:

```sql theme={null}
SELECT *
FROM `myproject.mydataset.mytable`
FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY);
```

You can supply an explicit timestamp (UTC) instead of `TIMESTAMP_SUB(...)` to target an exact point in time.

### 2) Create a new table from a historical snapshot (SQL)

If you need a permanent restoration, create a new table from the historical snapshot:

```sql theme={null}
CREATE TABLE `myproject.mydataset.recovered_table` AS
SELECT *
FROM `myproject.mydataset.mytable`
FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY);
```

This avoids re-running expensive transformations and gives you a full copy of the table as of that point.

### 3) Copy a historical snapshot using table decorators and the `bq` CLI

BigQuery supports table decorators to refer to a table at a specific timestamp (milliseconds since epoch) or a relative time. Use `bq cp` to copy a decorated snapshot to a new table.

Example using an absolute timestamp (milliseconds since epoch):

```bash theme={null}
bq cp --location=US \
  'myproject:mydataset.mytable@1625097600000' \
  myproject:mydataset.recovered_table
```

Example using a relative decorator (copy snapshot from 1 day ago — `-86400000` milliseconds):

```bash theme={null}
bq cp --location=US \
  'myproject:mydataset.mytable@-86400000' \
  myproject:mydataset.recovered_table
```

## Methods summary

| Method                     | Use case                                                                      | Example                                                                                                                                                                                 |
| -------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Query historical snapshot  | Inspect data as of a past point in time without creating a new table          | `SELECT * FROM \`myproject.mydataset.mytable\` FOR SYSTEM\_TIME AS OF TIMESTAMP\_SUB(CURRENT\_TIMESTAMP(), INTERVAL 1 DAY);\`                                                           |
| Create table from snapshot | Permanently restore data into a new table                                     | `CREATE TABLE \`myproject.mydataset.recovered\_table\` AS SELECT \* FROM \`myproject.mydataset.mytable\` FOR SYSTEM\_TIME AS OF TIMESTAMP\_SUB(CURRENT\_TIMESTAMP(), INTERVAL 1 DAY);\` |
| `bq cp` with decorator     | Fast copy of a historical snapshot to another table (good for large restores) | `bq cp --location=US 'myproject:mydataset.mytable@-86400000' myproject:mydataset.recovered_table`                                                                                       |

## Notes and best practices

* Act quickly if a table is accidentally deleted: recovery is only possible while the required point-in-time snapshot remains inside the retention window.
* Extend retention for critical production tables if your recovery policy needs more than the default 7 days (configurable up to 90 days).
* For large restores, copying a snapshot into a new table (`CREATE TABLE ... AS SELECT` or `bq cp`) is typically faster and avoids re-running expensive queries.
* Use IAM controls, audit logs, and dataset/table-level policies to reduce the likelihood of accidental deletions.
* Combine Time Travel with regular export snapshots (e.g., export to GCS) for long-term archival beyond 90 days.

<Callout icon="warning">
  If your recovery window requires more than 90 days of historical data, you must implement an external archival or backup strategy (for example, scheduled exports to Cloud Storage). Time Travel retention cannot exceed 90 days.
</Callout>

## Hands-on demo idea

Try this workflow in a sandbox project:

1. Create a table and insert sample rows.
2. Delete or overwrite some rows (or delete the table).
3. Query the table using `FOR SYSTEM_TIME AS OF` to confirm historical data availability.
4. Restore the data by creating a new table from the snapshot or using `bq cp`.

## Links and references

* [BigQuery Time Travel (official docs)](https://cloud.google.com/bigquery/docs/time-travel)
* [bq command-line tool reference](https://cloud.google.com/bigquery/docs/bq-command-line-tool)
* [Managing table-level properties (retention)](https://cloud.google.com/bigquery/docs/partitioned-tables#time_travel_and_row_access_policies)

By understanding and using BigQuery Time Travel, you can recover from accidental data changes quickly and reduce downtime for production workloads.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/5918fa46-3bfb-4bd1-a53b-41f2a2a77532/lesson/4eae0eab-b35f-487e-ba4a-0d32a23ca217" />
</CardGroup>
