# Module Introduction

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Creating-a-Knowledge-Store/Module-Introduction/page

Explains designing and configuring an Azure AI knowledge store to persist enriched pipeline outputs, map projections for analytics, and enable consumption by BI, Synapse, and automation tools.

Creating a knowledge store

Welcome to this module on creating a knowledge store in [Azure AI Services](https://learn.microsoft.com/azure/ai-services/). This lesson explains how a knowledge store organizes, transforms, and persists enriched content produced by your enrichment pipeline so downstream systems can report on, analyze, and automate using that data.

You will learn how to extract structured information from unstructured documents, represent that information for analysis, and expose it to other services for reporting and automation.

## What you'll learn (learning objectives)

* Understand what a Knowledge Store is and where it fits in an enrichment pipeline\
  Learn how the knowledge store captures outputs from enrichment—such as extracted text, entities, key-value pairs, tables, metadata, and OCR output—and persists them in structured forms.

* Understand why a Knowledge Store is essential for persisting structured information\
  See how storing enriched outputs enables auditability, re-use, and downstream analytics without re-running costly enrichment steps.

* Organize enriched data using projections (table and file projections)\
  Learn common projection types (relational-style tables and file formats like JSON and Parquet) and when to use each for querying, analytics, or bulk processing.

* Configure a Knowledge Store within your enrichment pipeline and access its output\
  Walk through configuring the store so enriched artifacts are written to persistent targets, and learn how to consume those outputs from tools like [Power BI](https://powerbi.microsoft.com/), [Azure Synapse](https://learn.microsoft.com/azure/synapse-analytics/), and [Logic Apps](https://learn.microsoft.com/azure/logic-apps/).

By the end of this lesson you will be able to design a knowledge store that captures key structured outputs from your enrichment pipeline and exposes them for reporting, analytics, and integration scenarios.

<Callout icon="lightbulb">
  A knowledge store is not just storage — it's the bridge between enrichment (extracting meaning from documents) and downstream systems that need structured, queryable, and analyzable data.
</Callout>

## What is a Knowledge Store?

A Knowledge Store is a structured persistence layer that receives enrichment outputs and writes them into formats suitable for downstream consumption. Instead of only storing raw documents, a knowledge store preserves the enriched artifacts—entities, relationships, tables, and metadata—so you can query, audit, and analyze results without re-running enrichment.

Key benefits:

* Persistent, auditable enriched outputs
* Reuse across analytics, reporting, and automation
* Reduced compute cost by avoiding repeated enrichment runs
* Flexible outputs for BI tools, data warehouses, and data lakes

## How a Knowledge Store fits into the enrichment pipeline

An enrichment pipeline takes raw documents (PDFs, images, Office files, etc.), applies extractors and cognitive skills, and emits enriched artifacts. The knowledge store captures those artifacts and projects them into target structures (tables, JSON, Parquet, or file hierarchies) for long-term use.

Typical flow:

1. Ingest documents into the enrichment pipeline.
2. Run cognitive skills to extract text, OCR, entities, key-value pairs, and tables.
3. Persist enriched outputs to the knowledge store.
4. Consume persisted outputs from BI or analytics tools.

## Common projection types and when to use them

Choosing the right projection type affects query, analytics, and storage goals. Use the following table to decide which projection best fits your use case.

| Projection Type                 | Use Case                                                      | Best for                                      |
| ------------------------------- | ------------------------------------------------------------- | --------------------------------------------- |
| Table projection                | Relational queries and reporting                              | Power BI, SQL-based analysis, Azure Synapse   |
| JSON file projection            | Flexible, nested document storage and event-driven processing | Data lakes, downstream ETL, ad-hoc processing |
| Parquet file projection         | Columnar, compressed storage for large-scale analytics        | Batch analytics, Spark, Synapse Analytics     |
| File projection (raw artifacts) | Store original enriched artifacts and metadata                | Auditability, backup, document-level replay   |

## Configuring a Knowledge Store

When configuring a knowledge store:

* Define projections that map enrichment outputs to target formats (tables, JSON, Parquet, or file hierarchies).
* Map fields and relationships so relational projections preserve entity context.
* Select storage targets (Azure Storage accounts, Data Lake, or Synapse).
* Configure access and retention policies to support audit and compliance needs.

Recommended steps:

1. Identify the outputs you need (entities, tables, KV pairs).
2. Choose projection types for each output based on query and processing needs.
3. Configure mappings and storage targets in the enrichment pipeline.
4. Validate persisted data using sample queries or BI tooling.

## Consuming Knowledge Store outputs

Persisted outputs can be consumed by a variety of tools and services:

* Power BI: Connect to table projections or Synapse for visualization and dashboards.
* Azure Synapse: Query Parquet or table projections for large-scale analytics.
* Logic Apps / Power Automate: Trigger workflows based on new files or metadata writes.
* Custom apps: Use SDKs or REST endpoints to query or download persisted artifacts.

Useful references:

* [Azure AI Services](https://learn.microsoft.com/azure/ai-services/)
* [Power BI](https://powerbi.microsoft.com/)
* [Azure Synapse Analytics](https://learn.microsoft.com/azure/synapse-analytics/)
* [Azure Logic Apps](https://learn.microsoft.com/azure/logic-apps/)

## Design considerations and best practices

* Model projections for common query patterns to avoid expensive joins or transformations at query time.
* Prefer Parquet for large-scale analytical workloads due to columnar storage and compression.
* Use table projections when you need relational querying with BI tools.
* Keep raw enriched artifacts for auditability and reprocessing scenarios.
* Apply retention policies and role-based access control to secure persisted outputs.

## Next steps

* Review your enrichment pipeline outputs and decide which artifacts to persist.
* Map those artifacts to projection types that match your analytics and reporting needs.
* Configure a Knowledge Store in your pipeline and validate with sample data.
* Connect Power BI, Synapse, or other services to begin consuming and visualizing your enriched data.

By following these steps you'll have a knowledge store that reliably bridges the gap between extraction and downstream analytics, reporting, and automation.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/e7fb804b-f0e4-48cb-9a9f-756ea9bf2386/lesson/356cce9e-f59a-4b51-b5fd-91465210b2a0" />
</CardGroup>
