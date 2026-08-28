# Cloud Dataprep by Trifacta

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Integration-Transformation-Tools/Cloud-Dataprep-by-Trifacta/page

Serverless, ML-guided, visual data preparation tool on Google Cloud for interactive profiling, cleaning, and transforming datasets with connectors to BigQuery and Cloud Storage

Welcome — in this lesson we explore Cloud Dataprep by Trifacta, Google Cloud’s managed, serverless service for interactive data preparation. Cloud Dataprep helps analysts and engineers clean, normalize, and validate incoming data with an intuitive visual interface and ML-driven suggestions, so data is analysis-ready without extensive ETL engineering.

## What is Cloud Dataprep?

Cloud Dataprep (built jointly with Trifacta) is a self-service data preparation tool on Google Cloud that focuses on interactive profiling, discovery, and transformation. It’s serverless — you pay only for jobs that run — and it leverages machine learning to suggest transformations, detect patterns, and infer schema. While heavy-duty execution typically runs on Google Cloud Dataflow, Dataprep’s primary value is its visual UI and intelligent assistant that accelerate routine cleaning tasks.

Key benefits:

* Serverless execution and automatic scaling.
* ML-guided recommendations for parsing, casting, splitting, and normalization.
* Visual, self-service interface with immediate previews and profiling.
* Integrations with common sources and sinks across Google Cloud and external systems.

## Typical user flow

1. Connect or upload a dataset (CSV, JSON, BigQuery, Cloud Storage, Google Sheets, etc.).
2. Profile and explore the data to surface distributions, nulls, outliers, and detected patterns.
3. Review and accept or refine suggested transformations (e.g., parse dates, split columns, fill or flag nulls).
4. Run a job to write a clean dataset to the chosen destination (BigQuery, Cloud Storage, Cloud SQL, etc.).

<Callout icon="lightbulb">
  Cloud Dataprep’s suggestions can identify null-heavy columns, inconsistent formats, and parsing problems. It accelerates routine cleaning but highly custom transformations or complex logic may still be better implemented in code (for example using Apache Beam/Dataflow or Spark).
</Callout>

## Core features and capabilities

* Automatic schema detection and interactive data profiling (distributions, null rates, outliers).
* Pattern recognition and ML-driven transformation suggestions.
* One-click or guided operations: parse, split, trim, cast, detect date/time, standardize formats, and more.
* Side-by-side preview of transformations before running jobs at scale.
* Connectors for common data sources and sinks.

<Frame>
  <img alt="An infographic titled &#x22;Dataprep Capabilities and Core Features&#x22; showing three main sections—Data Discovery, Smart Transformations, and Visual Interface—with bullet-point features for each. Below it is a typical pipeline flow listing data sources like CSV/JSON, BigQuery, Cloud SQL, Sheets, Cloud Storage, and APIs." />
</Frame>

## Common sources and destinations

| Source / Sink                    | Typical use case                                                           |
| -------------------------------- | -------------------------------------------------------------------------- |
| BigQuery                         | Read raw tables for profiling or write cleaned datasets back for analytics |
| Cloud Storage (CSV/JSON/Parquet) | Upload raw files, export transformed outputs                               |
| Cloud SQL                        | Extract or load relational data for smaller datasets                       |
| Google Sheets                    | Quick uploads or collaboration with business users                         |
| Web APIs                         | Ingest external datasets via API connectors                                |

## When Dataprep is a good fit

* Small teams or organizations that want fast, low-maintenance data cleaning without building a full ETL codebase.
* Analysts who prefer an interactive, visual UI with immediate feedback and ML-guided suggestions.
* Use cases that prioritize quick turnaround, ad-hoc exploration, and self-service data preparation.

## When to choose a code-first or orchestration solution

If your requirements include large-scale programmatic workflows, version-controlled ETL, complex logic best expressed in code, or tight CI/CD integration, you may prefer solutions like Apache Beam/Dataflow, Spark, or an orchestration platform such as Data Fusion or Airflow.

| Requirement                             | Dataprep             | Data Fusion / Dataflow / Spark |
| --------------------------------------- | -------------------- | ------------------------------ |
| Interactive profiling & visual cleaning | Excellent            | Limited                        |
| ML-suggested transformations            | Yes                  | No (requires custom work)      |
| Programmatic, version-controlled ETL    | Limited              | Strong                         |
| Complex, custom transformation logic    | Possible but awkward | Preferred                      |
| Orchestration and pipeline CI/CD        | Basic                | Designed for it                |

<Callout icon="warning">
  Dataprep is optimized for interactive, self-service prep. For production-grade, code-first pipelines that require advanced orchestration, versioning, or very complex transformations, prefer programmatic ETL (e.g., Apache Beam/Dataflow, Spark) or an orchestration platform (e.g., Data Fusion, Airflow).
</Callout>

## How Dataprep complements other Google Cloud services

* Execution: Jobs can run on Dataflow for scalable, server-side execution.
* Storage and analytics: Integrates smoothly with BigQuery and Cloud Storage for downstream analytics and BI.
* Orchestration: Use Dataprep for the data-cleaning stage and Data Fusion or Cloud Composer (Airflow) to orchestrate end-to-end pipelines.

## Quick comparison summary

* Use Dataprep when you need fast, low-code, ML-assisted cleaning with interactive previews.
* Use Data Fusion or Dataflow when you need programmatic, version-controlled, and highly orchestrated ETL at scale.

## Links and references

* [Cloud Dataprep documentation](https://cloud.google.com/dataprep)
* [Trifacta](https://www.trifacta.com/)
* [Google Cloud Dataflow](https://cloud.google.com/dataflow)
* [Cloud Data Fusion](https://cloud.google.com/data-fusion)

That’s an overview of Cloud Dataprep by Trifacta — a serverless, ML-guided, self-service tool for preparing data quickly and interactively.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/36c7f00a-93ef-43ff-8baa-7d73914196ca/lesson/e8f26a76-357a-487f-92e7-054324d34a54" />
</CardGroup>
