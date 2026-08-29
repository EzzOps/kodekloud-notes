# Dataplex The Unified Governance Layer

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Management-and-Governance/Dataplex-The-Unified-Governance-Layer/page

Overview of Google Cloud Dataplex, a centralized governance layer that organizes, catalogs, and enforces policies and data quality across distributed assets without moving underlying data.

Welcome back.

In this lesson we’ll explore Google Cloud Dataplex — a unified data governance layer that organizes, governs, and builds trust on top of your existing data in Google Cloud without moving the underlying data. Your data remains where it lives (for example, in Google Cloud Storage or BigQuery), while Dataplex provides a centralized control plane to manage metadata, policies, and data quality consistently.

Why use Dataplex? In short:

* Centralized governance across heterogeneous storage and analytic systems.
* Apply policies and quality checks without migrating data.
* Improve discoverability and trust for data consumers.

Read more: [Google Cloud Dataplex](https://cloud.google.com/dataplex)

## How Dataplex models your data

Dataplex introduces a simple three-tier logical model to represent and govern an entire data estate: Lake → Zone → Asset. This hierarchy maps naturally to business domains and data lifecycles so teams can operate independently while following consistent governance.

* Lake: A logical grouping of data aligned to a domain (for example, customers, marketing, finance). Think of a lake as the top-level scope for governance and ownership.
* Zone: Subdivisions within a lake that represent lifecycle or quality stages (for example, `raw`, `curated`, `sandbox`). Zones help prevent accidental use of inappropriate data.
* Asset: A pointer to the underlying storage location (for example, a Cloud Storage prefix or a BigQuery dataset). Dataplex operates on assets to scan, collect metadata, apply policies, and run quality checks — without moving the data.

<Frame>
  <img alt="The image is a slide titled &#x22;Dataplex Data Hierarchy&#x22; with a stacked colored-cube diagram illustrating three levels: Lake (top), Zone (middle), and Asset (bottom). It briefly defines each: Lake as a logical data domain grouping, Zone as a subdivision by data quality/stage, and Asset as the pointer to the underlying storage (e.g., cloud bucket or BigQuery dataset)." />
</Frame>

Table: Dataplex logical model (quick reference)

| Concept | Purpose                                       | Example                                   |
| ------: | --------------------------------------------- | ----------------------------------------- |
|    Lake | Top-level domain for governance and ownership | `customers`, `marketing`                  |
|    Zone | Lifecycle or quality stage within a lake      | `raw`, `curated`, `sandbox`               |
|   Asset | Pointer to the actual storage location        | `gs://bucket/prefix/` or BigQuery dataset |

Because Dataplex manages assets (pointers), governance actions — scans, IAM enforcement, metadata collection, quality checks — apply to the underlying data sources in-place. This enables incremental adoption, reduces operational disruption, and preserves existing pipelines and downstream consumers.

## Dataplex governance capabilities

Structure alone doesn’t make data usable — governance does. Dataplex provides a consolidated set of governance features designed to make data discoverable, trusted, and secure across your Google Cloud environment.

| Capability                | What it does                                                                          | Example benefit                                                                       |
| ------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| IAM management            | Define and propagate access policies at lake/zone/asset granularity                   | Centralize access control so domain owners can manage who can read or modify datasets |
| Data quality              | Define validation rules and automated checks (e.g., `customer_email IS NOT NULL`)     | Prevent bad data from entering production analytics                                   |
| Profiling                 | Collect structural and statistical properties (row counts, null rates, distributions) | Understand data shape and anomalies before using datasets                             |
| Data discovery & metadata | Scan assets and build a unified metadata catalog (integration with Data Catalog)      | Enable self-service discovery and reduce manual onboarding                            |

Dataplex’s governance stack focuses on:

* Access control and IAM propagation
* Automated profiling and data quality checks
* Centralized metadata and discovery via the catalog

<Frame>
  <img alt="A slide titled &#x22;Data Governance Hierarchy&#x22; showing a four-level, color-striped pyramid labeled (bottom to top) Data Discovery, Data Profiling, Data Quality, and IAM Propagation. Each layer has a short description (scans assets, analyzes structure, defines validation rules, propagates access policies) with arrows pointing to the matching pyramid section." />
</Frame>

<Callout icon="lightbulb">
  Asset pointers enable centralized governance without moving data. Use lakes for domains, zones for lifecycle/quality stages, and assets to reference storage locations so governance can be applied consistently and non-invasively.
</Callout>

## Next steps

Now that you have a solid foundation in how Dataplex organizes and governs data, the next deep dive will examine Dataplex’s data catalog: how discovery, classification, and metadata management work together to surface trusted datasets for analytics and ML.

## Links and references

* Dataplex product page: [https://cloud.google.com/dataplex](https://cloud.google.com/dataplex)
* Google Cloud Storage: [https://cloud.google.com/storage](https://cloud.google.com/storage)
* BigQuery: [https://cloud.google.com/bigquery](https://cloud.google.com/bigquery)
* Data Catalog: [https://cloud.google.com/data-catalog](https://cloud.google.com/data-catalog)
* Data mesh principles (background reading): [https://martinfowler.com/articles/data-mesh-principles.html](https://martinfowler.com/articles/data-mesh-principles.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/a6bc07ab-e352-4400-a7da-0fb08345a658/lesson/65ec422d-543b-4cb8-a866-6108acc66944" />
</CardGroup>
