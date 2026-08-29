# BigQuery Core Components

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Warehouse-Analytics-Options/BigQuery-Core-Components/page

Overview of BigQuery core components, supported data types, query execution lifecycle, and practical tips for organizing data, controlling access, optimizing queries, and reducing costs.

Hello and welcome back.

In this lesson we explore the core components of BigQuery. Earlier in this series we covered what BigQuery is and why teams choose it. Now we'll examine the building blocks that make BigQuery work so you can understand how data is organized, secured, and processed inside the platform.

When working with BigQuery, a clear resource hierarchy helps with access control, organization, and billing. We'll walk each level step by step and show the practical implications for querying and cost control.

## Resource hierarchy

At the top of the hierarchy are projects, then datasets, and finally tables/views. The table below summarizes each level and its purpose.

| Resource Level | Purpose                                                                                                             | Quick tip                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Project        | Container for BigQuery resources (datasets, jobs, etc.). Billing, IAM, and quotas are applied at the project level. | Use separate projects to isolate billing and access boundaries for teams or environments. |
| Dataset        | Logical grouping for tables and views. Acts like a folder for organizing resources and applying dataset-level IAM.  | Group tables by team, domain, or retention policy.                                        |
| Table          | Stores rows and columns (columnar storage optimized for analytics).                                                 | Use partitioning and clustering to reduce scanned data.                                   |
| View           | Saved SQL query; does not store data. Queries the underlying tables when accessed.                                  | Use views to encapsulate business logic or present filtered datasets.                     |

* Projects: A project is the top-level container. Every BigQuery dataset, table, and job belongs to a project. Billing is associated with the project and IAM permissions/quotas are evaluated at this level.
* Datasets: Datasets group related tables and views. Think of a dataset as a folder that lets you manage access and organize artifacts by purpose, application, or team.
* Tables: Tables store the actual data. BigQuery uses columnar storage and is optimized for analytical queries (scans across columns rather than rows).
* Views: Views are saved SQL statements. They don’t store data — when you query a view, BigQuery executes the underlying query and returns results. Use views to hide complexity, expose curated projections, or implement row/column-level filters.

## Data types supported in BigQuery

BigQuery supports primitive and complex data types so you can represent traditional relational data and modern nested/semi-structured formats.

| Type                                    | Description                                                                                                                         | When to use                                                                           |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `NUMERIC` / `BIGNUMERIC`                | Exact decimal types: `NUMERIC` supports up to 38 digits of precision; `BIGNUMERIC` supports extended precision (up to \~76 digits). | Currency, financial calculations, or any scenario requiring exact decimal arithmetic. |
| `INT64`                                 | 64-bit signed integers.                                                                                                             | Counts, IDs, and integer arithmetic.                                                  |
| `FLOAT64`                               | 64-bit floating point numbers.                                                                                                      | Approximate numeric computations where performance is important.                      |
| `STRING`                                | UTF-8 text.                                                                                                                         | Text fields, descriptive data, identifiers.                                           |
| `BYTES`                                 | Raw binary data.                                                                                                                    | Images, binary blobs, or encoded payloads.                                            |
| `BOOLEAN`                               | True/false values.                                                                                                                  | Flags and binary conditions.                                                          |
| `DATE`, `TIME`, `DATETIME`, `TIMESTAMP` | Date and time types. Use `TIMESTAMP` for timezone-aware instants (absolute points in time).                                         | Temporal data and time-series.                                                        |
| `ARRAY`                                 | Ordered list of a single element type (repeated fields).                                                                            | Events, tags, or lists inside a single record.                                        |
| `STRUCT` / `RECORD`                     | Nested records with named fields (hierarchical data).                                                                               | Nested JSON-like objects, denormalized schemas.                                       |
| `JSON`                                  | Semi-structured JSON values with native JSON functions.                                                                             | Raw event payloads or flexible schema data that benefits from JSON parsing.           |

These complex types (`ARRAY`, `STRUCT`, `JSON`) let BigQuery natively store nested and semi-structured data such as logs, events, and clickstreams without prior normalization.

> **lightbulb** Using columnar storage with nested types allows BigQuery to read only the required columns (and nested fields), which reduces query I/O and cost when you query selectively.

## How queries run in BigQuery

Understanding the query execution lifecycle helps you write efficient and cost-effective queries. Typical steps:

1. Parsing and validation
   * BigQuery parses SQL, checks syntax, validates table/column references, and resolves data types.
2. Query planning and optimization
   * The planner converts SQL into an execution plan and applies optimizations (predicate pushdown, projection pruning, join ordering, etc.).
3. Resource allocation
   * BigQuery assigns compute resources called slots. For on-demand customers, the service manages slots automatically; flat-rate customers consume slots from their purchased pool.
4. Data reading (scanning)
   * BigQuery reads the minimum data required. Columnar storage means only referenced columns and relevant partitions/clusters are scanned. Billing is by bytes processed (unless using flat-rate).
5. Execution and processing
   * Distributed workers perform join, aggregation, window functions, and UDF execution.
6. Results delivery
   * Results are returned to the console, exported, or written to a destination table.

Be mindful: queries like `SELECT * FROM table` can be expensive on wide or large tables because they scan all columns. Always select only the columns you need and leverage partitioning and clustering to limit scanned data.

Example — prefer selecting specific columns:

```sql theme={null}
-- Prefer this: reads only the referenced columns and uses a date filter
SELECT order_id, customer_id, order_total
FROM `project.dataset.orders`
WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31';

-- Avoid this on very large tables unless you need every column
SELECT *
FROM `project.dataset.orders`;
```

## Practical tips to reduce cost and improve performance

* Partition tables by date (or ingestion time) to limit scanned partitions for time-range queries.
* Cluster on frequently filtered columns to co-locate similar values and reduce read I/O.
* Project only the columns you need—avoid `SELECT *`.
* Use approximate functions (e.g., `APPROX_COUNT_DISTINCT`) when exact precision is not required.
* Leverage cached query results when the same query is run and underlying data hasn’t changed.
* For large predictable workloads, consider flat-rate slots to stabilize cost and performance.

> **lightbulb** Remember: on-demand billing charges by bytes processed for queries and by bytes stored for tables. Partitioning, clustering, and projecting columns are the most effective levers to reduce query cost.

## Summary

This lesson covered BigQuery’s core components: projects, datasets, tables, and views. We reviewed primary data types (primitive and complex) and walked through the query execution lifecycle. With this foundation you can better organize data, control access and billing, and write queries that are both performant and cost-efficient.

Further lessons will dive deeper into partitioning, clustering, IAM best practices, and advanced query optimization.

## Links and references

* [BigQuery overview (Google Cloud)](https://cloud.google.com/bigquery/docs)
* [Partitioned tables](https://cloud.google.com/bigquery/docs/partitioned-tables)
* [Clustering tables](https://cloud.google.com/bigquery/docs/clustered-tables)
* [BigQuery pricing](https://cloud.google.com/bigquery/pricing)
* [Query optimization best practices](https://cloud.google.com/bigquery/docs/best-practices-performance)

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/5918fa46-3bfb-4bd1-a53b-41f2a2a77532/lesson/6787287c-ae44-4c0a-8f6c-d242fdb88bb0)
