# Demo Dataset Creation Data Uploads Tables

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Warehouse-Analytics-Options/Demo-Dataset-Creation-Data-Uploads-Tables/page

Guide to using the BigQuery console to create datasets, tables, insert and query data, build views, inspect job details, and follow best practices

Hello and welcome back.

In this lesson we explore the BigQuery console — the primary interface data engineers use to query and manage analytical data. You will commonly use BigQuery alongside related services such as Google Cloud Storage (GCS) and BigQuery Data Transfer Service.

Key areas to explore in the BigQuery console:

* Left navigation: project explorer, datasets, tables, Data Transfer, Dataform, Scheduled Queries, Monitoring, Job Explorer, and Assets.
* Center: SQL editor where you author and run queries.
* Right / details pane: schema, metadata, job details, and execution graphs.

Open the GCP Console and navigate to BigQuery. Expand the left-hand explorer to view your project resources. You may already have a dataset (for example, `demo_dataset`) with tables such as `sales`. You can delete datasets from the UI — deletion is permanent (subject to BigQuery time travel retention). Be cautious.

<Callout icon="lightbulb">
  Deleting a dataset permanently removes its objects. BigQuery supports time travel for a limited retention period (by default 7 days), which can allow recovery of recent changes, but it's best to treat deletions as irreversible unless you have appropriate backups or export copies.
</Callout>

## Creating a dataset

You can create a dataset via the UI (select your project → Create dataset) or directly with SQL in the editor. Replace `kodekloud-gcp-training` with your GCP project ID if different.

```sql theme={null}
CREATE SCHEMA IF NOT EXISTS `kodekloud-gcp-training.demo_dataset`
OPTIONS(
    location='US',
    description='Demo dataset for BigQuery tutorial'
);
```

Run the statement in the editor. After execution, review job details and the execution graph if you need query diagnostics. Refresh the left pane to confirm the `demo_dataset` appears — it will initially contain no tables.

## Creating a table (employees)

Create an `employees` table with the following schema:

```sql theme={null}
CREATE TABLE `kodekloud-gcp-training.demo_dataset.employees` (
    employee_id INT64 NOT NULL,
    first_name STRING NOT NULL,
    last_name STRING NOT NULL,
    email STRING NOT NULL,
    department_id INT64 NOT NULL,
    salary INT64,
    hire_date DATE
);
```

After running the `CREATE TABLE` statement, click the table in the left explorer to inspect:

* Schema
* Last modified timestamp
* Data location
* Row count
* Table properties

Use the "Last modified" timestamp to verify when data was last changed.

## Inserting sample rows

Insert sample employee records:

```sql theme={null}
INSERT INTO `kodekloud-gcp-training.demo_dataset.employees`
(employee_id, first_name, last_name, email, department_id, salary, hire_date)
VALUES
(1, 'John', 'Doe', 'john.doe@company.com', 101, 75000, '2023-01-15'),
(2, 'Jane', 'Smith', 'jane.smith@company.com', 102, 82000, '2022-11-20'),
(3, 'Bob', 'Johnson', 'bob.johnson@company.com', 101, 68000, '2023-03-10'),
(4, 'Alice', 'Williams', 'alice.williams@company.com', 103, 95000, '2021-09-05'),
(5, 'Charlie', 'Brown', 'charlie.brown@company.com', 102, 72000, '2023-06-01');
```

After the INSERT completes, refresh the table in the left pane. The row count and "Last modified" timestamp should reflect the inserted data.

## Querying the table

Run a simple query to return all rows ordered by employee ID:

```sql theme={null}
SELECT * FROM `kodekloud-gcp-training.demo_dataset.employees`
ORDER BY employee_id;
```

Result panel options:

* Visualize — create charts from query results
* View as JSON — inspect rows as JSON objects
* Save results — download as CSV, save to Google Drive, or export to Google Cloud Storage

## Creating and using views

Views are virtual representations of queries — they do not duplicate data and always return up-to-date results because they run the underlying query at query time. Views are useful to simplify complex logic, encapsulate transformations, and control field exposure.

Create a view that concatenates first and last name and computes days employed:

```sql theme={null}
CREATE OR REPLACE VIEW `kodekloud-gcp-training.demo_dataset.employee_summary` AS
SELECT
    employee_id,
    CONCAT(first_name, ' ', last_name) AS full_name,
    email,
    department_id,
    salary,
    hire_date,
    DATE_DIFF(CURRENT_DATE(), hire_date, DAY) AS days_employed
FROM `kodekloud-gcp-training.demo_dataset.employees`;
```

After creating the view, you'll see a distinct view icon in the left explorer. Click Details to inspect the defining query.

Query the view just like a table:

```sql theme={null}
SELECT * FROM `kodekloud-gcp-training.demo_dataset.employee_summary`
ORDER BY salary DESC;
```

This returns the `full_name` and the computed `days_employed` column alongside other fields.

## Quick reference table

| Action         | Console / SQL | Example                                                                         |
| -------------- | ------------- | ------------------------------------------------------------------------------- |
| Create dataset | UI or SQL     | `CREATE SCHEMA IF NOT EXISTS \`\<project>.demo\_dataset\`\`                     |
| Create table   | SQL           | `CREATE TABLE \`\<project>.demo\_dataset.employees\` (...)\`                    |
| Insert data    | SQL           | Use `INSERT INTO` with `VALUES` or `SELECT` from other sources                  |
| Query data     | SQL           | `SELECT * FROM \`\<project>.demo\_dataset.employees\`\`                         |
| Create view    | SQL           | `CREATE OR REPLACE VIEW \`\<project>.demo\_dataset.employee\_summary\` AS ...\` |
| Export results | Console UI    | Save results to CSV, Drive, or GCS from the query results pane                  |

## Best practices and tips

* Use descriptive dataset and table names and include metadata (descriptions) for discoverability.
* Inspect job details and the execution graph for expensive or long-running queries.
* Prefer views to expose consistent business logic without duplicating data.
* Use GCS and BigQuery Data Transfer Service for scheduled imports and external data loads.
* Monitor "Last modified" and row counts to validate DML operations.

## Links and references

* BigQuery console overview: [https://cloud.google.com/bigquery/docs](https://cloud.google.com/bigquery/docs)
* Google Cloud Storage (GCS): [https://cloud.google.com/storage](https://cloud.google.com/storage)
* BigQuery Data Transfer Service: [https://cloud.google.com/bigquery-transfer](https://cloud.google.com/bigquery-transfer)
* BigQuery time travel: [https://cloud.google.com/bigquery/docs/time-travel](https://cloud.google.com/bigquery/docs/time-travel)
* Dataform on Google Cloud: [https://cloud.google.com/dataform/docs](https://cloud.google.com/dataform/docs)

Summary:

* Use the BigQuery editor to create datasets, tables, and views either via SQL or the UI.
* Check job details and execution graphs for query diagnostics.
* Use the table "Last modified" metadata to confirm data changes.
* Views provide virtual, up-to-date representations of underlying data and are useful for sharing reusable logic across teams.

That covers the fundamentals demonstrated in this lesson. See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/5918fa46-3bfb-4bd1-a53b-41f2a2a77532/lesson/c78d3f58-5a37-4fec-a9b8-f02b1da95e30" />
</CardGroup>
