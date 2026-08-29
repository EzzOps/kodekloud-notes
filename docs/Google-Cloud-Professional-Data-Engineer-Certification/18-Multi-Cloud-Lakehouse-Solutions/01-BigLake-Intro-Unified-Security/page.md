# BigLake Intro Unified Security

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Multi-Cloud-Lakehouse-Solutions/BigLake-Intro-Unified-Security/page

Introduction to BigLake, a unified storage layer enabling cross‑cloud analytics, unified governance, fine‑grained security, and multi‑engine access to open-format data without data duplication

Welcome back. In this lesson we introduce BigLake, a unified storage engine that's rapidly becoming central to Google Cloud analytics. BigLake helps data teams manage security, governance, and performance across heterogeneous storage systems (BigQuery, GCS, and external object stores on AWS/Azure) while enabling analytics and AI on the same data without duplicating it.

## What is BigLake?

BigLake is a unified storage layer that enables analytics and AI workloads to access data in open formats without forcing migration to a proprietary store. Key points include:

* Support for open data formats such as Parquet, Avro, and ORC.
* Cross-cloud capability: access data in Google Cloud Storage (GCS) and supported external object stores on AWS and Azure.
* Single-copy Lakehouse architecture: let multiple engines consume the same data without creating duplicate copies.
* Simplifies pipelines and infrastructure by enabling multi-engine access to the same storage layer.

## Core features

* Fine-grained access control: enforce row-level filters and column-level restrictions so users only see permitted data.
* Multi-engine support: BigQuery, Spark (Dataproc), Presto/Trino, and other engines can query the same data layer.
* Unified governance: integrates with Dataplex for centralized policy, metadata, and discovery.
* Performance optimizations: predicate pushdown and engine-level caching where supported reduce query scan costs and runtime.
* Cost savings: fewer data copies and simplified processing reduce storage and compute costs.

## High-level architecture

BigLake sits between storage and compute:

* Storage: data remains in object storage (GCS or external cloud object stores).
* Compute: engines (BigQuery, Dataproc/Spark, Presto/Trino, Vertex AI) connect through BigLake to read and process data.

This design allows policies and governance to be enforced consistently while data remains in place.

## Security and policy enforcement

BigLake provides consistent controls across storage and engines. Common capabilities, how they’re enforced, and where to configure them are summarized below.

| Control                   | How it’s enforced                                           | Where to configure / notes                                                                         |
| ------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Table-level access        | IAM permissions (`roles/bigquery.dataViewer`, custom roles) | Use BigQuery IAM and Cloud IAM bindings; Dataplex can help centralize policies                     |
| Row-level security        | Row-level filters (access policies)                         | Implement via BigQuery row access policies or Dataplex-managed policies; engine support varies     |
| Column-level restrictions | Column masking / policy tags                                | Use BigQuery column-level security, Data Catalog policy tags, or Dataplex for centralized metadata |
| Cross-engine consistency  | Unified policy evaluation and metadata                      | Dataplex + BigLake integration ensures consistent metadata and policy propagation                  |
| Audit & compliance        | Cloud Audit logs, Dataplex reports                          | Enable audit logs and Dataplex monitoring for compliance evidence                                  |

Example: create a BigQuery external table that points at Parquet files on GCS

```sql theme={null}
CREATE EXTERNAL TABLE `my_project.my_dataset.sales_parquet`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://my-bucket/sales/*.parquet']
);
```

For row-level access and column masking, use BigQuery row access policies and Data Catalog policy tags respectively — see the references below for exact syntax and examples.

## Integrations

BigLake integrates across the Google Cloud ecosystem and with external engines:

* BigQuery (native query and governance)
* Dataproc / Apache Spark
* Presto and Trino
* Vertex AI for ML workflows
* Dataplex for centralized governance and metadata
* External object stores on AWS and Azure (for multi-cloud lakehouse scenarios)

The slide below summarizes these security benefits:

<Frame>
  <img alt="A slide titled &#x22;Security Benefits&#x22; showing five colored boxes that list advantages: &#x22;Eliminates file-level access grants,&#x22; &#x22;Consistent security across engines,&#x22; &#x22;Simplified access management,&#x22; &#x22;Compliance-ready policies,&#x22; and &#x22;Reduced security overhead.&#x22; The layout is a clean presentation-style graphic with gradient-colored rounded rectangles." />
</Frame>

<Callout icon="lightbulb">
  We will include a hands-on BigLake example and an important comparison — BigLake versus external tables — to make the differences and trade-offs much clearer.
</Callout>

## BigLake vs. External Tables — quick comparison

* BigLake (unified storage engine): Focuses on providing a consistent storage layer and metadata/policy integration across multiple engines and clouds. Ideal when you need centralized governance, multi-engine access, and single-copy consumption.
* External tables (BigQuery external table): Lets BigQuery query data stored outside of BigQuery (GCS, Cloud Storage). Good for ad-hoc analytics without importing data; policy enforcement is primarily BigQuery-focused unless combined with Dataplex.

Use cases:

* Lakehouse with many engines and centralized governance → BigLake + Dataplex.
* Quick query of CSV/Parquet on GCS from BigQuery → BigQuery external tables.

## Next steps and references

* BigLake overview and best practices: [https://cloud.google.com/biglake](https://cloud.google.com/biglake)
* BigQuery external tables: [https://cloud.google.com/bigquery/docs/external-tables](https://cloud.google.com/bigquery/docs/external-tables)
* Dataplex governance & metadata: [https://cloud.google.com/dataplex](https://cloud.google.com/dataplex)
* Row-level and column-level security in BigQuery: [https://cloud.google.com/bigquery/docs/security](https://cloud.google.com/bigquery/docs/security)

That concludes this lesson on BigLake. In the next session we’ll walk through a hands-on example that sets up a BigLake table, demonstrates policy enforcement via Dataplex, and compares query plans between an external table and a BigLake-managed dataset.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/c354d782-20e6-4961-a282-071b52a4013d/lesson/bcae7426-ebb1-48d9-9ff1-f0da23ba2273" />
</CardGroup>
