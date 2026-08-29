# AWS Glue and Glue DataBrew for Data Transformation

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/AWS-Glue-and-Glue-DataBrew-for-Data-Transformation/page

Overview of AWS Glue and Glue DataBrew for scalable ETL and visual data preparation to clean, transform, and catalog datasets for analytics and machine learning pipelines

In this lesson we'll cover how AWS Glue and AWS Glue DataBrew streamline data preparation for machine learning (ML). ML workflows depend on clean, consistent, and well-structured datasets. AWS Glue and DataBrew automate extraction, cleaning, transformation, and cataloging at scale—ingesting raw data from multiple sources, converting it into analytics-ready formats, and persisting results to targets such as Amazon S3 for downstream analytics and ML training.

<Frame>
  <img alt="The image is an infographic explaining why to use AWS Glue services for machine learning, outlining a workflow from data source extraction to transformation and loading into data targets, with steps like connecting to data sources and storing results." />
</Frame>

## ETL pattern for ML data preparation

The data preparation flow typically follows the ETL pattern:

* Extract: Ingest raw data from sources such as Amazon S3, Amazon Redshift, Amazon OpenSearch, relational databases, or streaming sources.
* Transform: Use AWS Glue or AWS Glue DataBrew to clean, normalize, deduplicate, convert types, parse dates, and otherwise prepare data for analytics and ML.
* Load: Persist processed datasets back to Amazon S3, a data warehouse, or another storage layer for model training and analytics.

This ETL pipeline ensures ML models receive high-quality, reproducible training data.

## What is AWS Glue?

[AWS Glue](https://aws.amazon.com/glue/) is a serverless ETL service designed for large-scale, code-driven data processing. Key features include:

* Crawlers that scan data stores, infer schemas and types, and populate the Glue Data Catalog.
* A centralized Glue Data Catalog that becomes a shared metadata repository for tools like Amazon Athena and Amazon Redshift Spectrum.
* ETL jobs built on Apache Spark for scalable, programmatic transformations; jobs can be scheduled, chained, or triggered.
* Integration with the AWS analytics and ML ecosystems for automated production pipelines.

## AWS Glue DataBrew: visual, interactive data preparation

AWS Glue DataBrew is a visual, no-code/low-code tool for data profiling and interactive cleaning—ideal for analysts, data scientists, and data engineers who need rapid iteration.

* Profiling: Quickly analyze distributions, detect anomalies, and assess data quality.
* Clean & Normalize: Apply prebuilt transformations (fill/drop missing values, normalize formats, parse/standardize dates).
* Map Lineage: Track every transformation step in a recipe for reproducibility and auditing.
* Automate: Reuse recipes and schedule jobs to run transformations automatically on new data.

<Frame>
  <img alt="The image highlights the capabilities of AWS Glue DataBrew, including profile, clean and normalize, map data lineage, and automate, with brief descriptions and visual examples." />
</Frame>

## Typical DataBrew project workflow

A common DataBrew project follows these steps:

1. Import data from sources (Amazon S3, Amazon Redshift, databases).
2. Create a project to manage datasets and recipes.
3. Apply a recipe: a sequence of reusable transformation steps (formatting, deduplication, type conversions).
4. Profile the data to identify distributions, outliers, and quality issues.
5. Export the transformed dataset to Amazon S3 for analytics or ML.

<Frame>
  <img alt="The image outlines the AWS Glue DataBrew workflow in five steps: Import Data, Create Project, Apply Recipe, Profile Data, and Export to S3. Each step includes a brief description and an icon." />
</Frame>

## Glue vs DataBrew — when to use which

Choose the tool based on team roles, scale, and production needs. The table below summarizes core differences and recommended use cases.

| Dimension     | AWS Glue                                        | AWS Glue DataBrew                                    |
| ------------- | ----------------------------------------------- | ---------------------------------------------------- |
| Interface     | Code-first (PySpark/Scala)                      | Visual, interactive (no-code/low-code)               |
| Best for      | Large-scale automated ETL, production pipelines | Ad-hoc cleaning, fast prototyping, analyst workflows |
| Scalability   | High — Spark-based distributed processing       | Interactive sessions + job runs for batch processing |
| Output        | ETL jobs -> Data Catalog, S3, data warehouses   | Recipes -> Export to S3, integration with Glue jobs  |
| Billing model | Billed per DPU-hour for ETL jobs and crawlers   | Billed per session-hour and per data processing job  |
| Typical users | Engineers, DevOps, data platform teams          | Data analysts, data scientists, data engineers       |

<Frame>
  <img alt="The image depicts a data preparation workflow using Amazon Redshift, AWS Glue DataBrew, and Amazon S3." />
</Frame>

DataBrew can connect directly to Amazon Redshift and other sources, enabling analysts to clean warehouse data visually and export artifacts that feed into production ETL jobs or directly into ML training pipelines.

## How Glue and DataBrew fit into an ML pipeline

A typical ML data pipeline using Glue/DataBrew looks like:

* Raw data in Amazon S3 (or other sources) is imported into DataBrew for exploration or processed by Glue ETL jobs for large-scale transformations.
* Recipes or ETL jobs implement the cleaning and feature-preparation steps.
* Clean datasets are exported to Amazon S3 or a data warehouse.
* Prepared data is consumed by AWS SageMaker for model training and inference; visualization and ad-hoc queries use Amazon QuickSight and Amazon Athena.

<Frame>
  <img alt="The image is a flowchart illustrating the integration of Amazon S3, AWS Glue DataBrew, AWS Glue Data Catalog, Amazon Athena, and Amazon QuickSight, showing how these services interact for data processing and analytics." />
</Frame>

Glue crawlers monitor and discover new datasets to update the Glue Data Catalog, while Glue ETL jobs and DataBrew recipes perform the transformations that produce reproducible datasets for analytics and ML.

<Frame>
  <img alt="The image illustrates an AWS Glue workflow for machine learning pipelines, showing a process flow from detecting new data with a crawler to transforming it with AWS Glue DataBrew and storing it in Amazon S3." />
</Frame>

## Common transformation tasks supported

Both services support typical data preparation steps required for ML pipelines:

* Handling missing values: fill, impute, or drop rows/columns
* Normalizing and scaling numerical features
* Encoding categorical variables (one-hot encoding, label encoding)
* Parsing, normalizing, and standardizing dates/timestamps
* Filtering rows and validating value ranges or formats
* Aggregating and computing summary statistics (group-bys, sums, averages)

## Cost considerations

Both are pay-as-you-go but with different billing models:

* AWS Glue: billed per DPU-hour for ETL job runtime and for crawlers. See AWS Glue pricing: [https://aws.amazon.com/glue/pricing/](https://aws.amazon.com/glue/pricing/)
* AWS Glue DataBrew: billed per interactive session (per session-hour) and per data processing job run. See DataBrew pricing: [https://aws.amazon.com/databrew/pricing/](https://aws.amazon.com/databrew/pricing/)

<Frame>
  <img alt="The image compares the cost considerations of AWS Glue and AWS Glue DataBrew, highlighting their billing methods. AWS Glue is billed per DPU-hour for ETL jobs and per request for crawlers, while DataBrew is billed per session and per data processing job." />
</Frame>

Choosing between Glue and DataBrew depends on your workload and team needs: Glue is typically more cost-efficient and appropriate for large-scale, automated production ETL, while DataBrew is optimized for interactive, analyst-driven cleaning and fast iteration.

> **lightbulb** Use AWS Glue when you require programmatic, reproducible, and highly scalable ETL (Spark-based jobs and scheduled pipelines). Use AWS Glue DataBrew for fast, visual exploration and cleaning where analysts need to prototype transformations and export recipes into production workflows.

## References and further reading

* AWS Glue: [https://aws.amazon.com/glue/](https://aws.amazon.com/glue/)
* AWS Glue DataBrew: [https://aws.amazon.com/databrew/](https://aws.amazon.com/databrew/)
* AWS SageMaker: [https://aws.amazon.com/sagemaker/](https://aws.amazon.com/sagemaker/)
* Amazon S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)
* Amazon Athena: [https://aws.amazon.com/athena/](https://aws.amazon.com/athena/)
* Amazon QuickSight: [https://aws.amazon.com/quicksight/](https://aws.amazon.com/quicksight/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/b7fa089f-684e-40ab-88ac-2d954dfaa2ce)
