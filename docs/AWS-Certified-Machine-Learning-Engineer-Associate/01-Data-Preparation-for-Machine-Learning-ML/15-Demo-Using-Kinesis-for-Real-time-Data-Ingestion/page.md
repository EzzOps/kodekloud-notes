# Demo Using Kinesis for Real time Data Ingestion

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Demo-Using-Kinesis-for-Real-time-Data-Ingestion/page

Demonstration of using Amazon SageMaker Data Wrangler to import, inspect, clean, and export tabular datasets from S3 for machine learning workflows

Welcome to this lesson. Here we focus on using Amazon SageMaker Data Wrangler to import, explore, and prepare tabular data for machine learning workflows. Although the title references Kinesis, this demo demonstrates batch ingestion using a CSV stored in Amazon S3; real-time ingestion with Kinesis requires a different pipeline and is out of scope for this walkthrough.

What you will learn:

* Where to find Data Wrangler in the SageMaker console
* How to import a tabular CSV from Amazon S3
* How to inspect schema, distributions, and anomalies
* How to apply transforms (imputation) and review a dataset summary
* How to export a clean dataset for training

## Locate Data Wrangler in the SageMaker Console

AWS periodically reorganizes the console UI, so the first step is locating Data Wrangler inside the SageMaker product area.

<Frame>
  <img alt="The image shows an Amazon SageMaker AI dashboard webpage, promoting machine learning model building, training, and deployment at scale with setup options and documentation links." />
</Frame>

Search for “SageMaker” in the AWS console. You may see entries like Amazon SageMaker (data analytics and AI hub) and Amazon SageMaker AI (for building, training, and deploying models). Data Wrangler is accessible from SageMaker Studio and Canvas. In this example we launch SageMaker Canvas and wait for the UI to become available; Data Wrangler appears in the top-left of Canvas when ready.

Amazon SageMaker Data Wrangler is designed to streamline data import, exploration, and large-scale transformations. It provides hundreds of built-in transforms and supports many data sources for tabular datasets.

## Data Wrangler Interface — Import and Prepare

Open Data Wrangler to begin a new flow. The UI shows import, prepare, and analyze steps visually so you can build a reproducible data flow.

<Frame>
  <img alt="The image shows the interface of Amazon SageMaker Data Wrangler, highlighting steps for importing, preparing, and analyzing data with options such as &#x22;Import and prepare.&#x22; There are icons illustrating the data processing workflow and resources for getting started." />
</Frame>

## Import a CSV from Amazon S3

Data Wrangler supports many sources: local uploads, `Snowflake`, `Redshift`, `PostgreSQL`, `MySQL`, and `Amazon S3`. For this demo the raw dataset is stored in S3 under a bucket named "Machine Learning Demo". We navigate to that S3 location and select the Titanic CSV to import.

<Frame>
  <img alt="The image shows a data source selection interface for importing tabular data, with options like Amazon S3, Redshift, Canvas Datasets, and others. The interface is part of an AWS SageMaker session." />
</Frame>

After import completes, Data Wrangler auto-detects column types and provides quick visual summaries for each feature.

<Frame>
  <img alt="The image shows a screenshot of a data wrangling interface in AWS SageMaker's Data Wrangler, displaying columns from a &#x22;titanic.csv&#x22; dataset, including attributes like &#x22;Survived,&#x22; &#x22;Pclass,&#x22; &#x22;Name,&#x22; and &#x22;Sex.&#x22; There are visualizations representing data categories and column type options on the right side." />
</Frame>

Example: the `Survived` column is detected as numeric/binary with two classes, `0` and `1`. Data Wrangler shows distribution percentages (e.g., \~61.44% class `0`, 38.56% class `1`) when you hover over categories, which helps assess class balance before modeling.

## Apply a Transform — Imputation

Common preprocessing tasks are available as built-in transforms. One frequent action is imputing missing numeric values (replace `NaN` with mean, median, etc.).

<Callout icon="lightbulb">
  Imputation replaces missing numeric values using a chosen strategy (mean, median, mode, constant, etc.). The `median` is robust to outliers and is often a safe default when numeric distributions are skewed.
</Callout>

In this demo we add an imputation transform with the `median` strategy and target numeric columns such as `Pclass`, `Fare`, and `Age`. After applying the transform, Data Wrangler runs the step and updates the preview.

<Frame>
  <img alt="The image shows a summary of dataset statistics for &#x22;titanic.csv&#x22; in AWS SageMaker's Data Wrangler, including details on features, rows, and data validity. It also indicates that no high severity warnings were detected in the data." />
</Frame>

## Review Data Flow and Dataset Summary

The Data Flow diagram visualizes each node: original source → inferred types → added transforms (imputation, formulas, filters, etc.). This makes your preparation pipeline reproducible and auditable.

After running the analysis Data Wrangler produces a dataset summary. For the Titanic demo the summary shows:

| Metric           | Value                     |
| ---------------- | ------------------------- |
| Features         | 8                         |
| Validity         | 100% (all features valid) |
| Missing values   | 0% (imputation applied)   |
| Rows             | 887                       |
| Duplicate rows   | 0%                        |
| Numeric features | 5                         |

<Frame>
  <img alt="The image is a screenshot from AWS Data Wrangler showing a feature summary for the Titanic dataset with columns such as &#x22;Survived,&#x22; &#x22;Pclass,&#x22; &#x22;Name,&#x22; &#x22;Sex,&#x22; &#x22;Age,&#x22; and &#x22;Siblings/Spouses Aboard,&#x22; all with 100% validity and no missing data." />
</Frame>

This summary indicates the dataset is suitable for further feature engineering or for export to a model training pipeline.

## Inspect Anomalies and Feature-Level Analysis

Data Wrangler highlights anomalous samples and their anomaly scores so you can review outliers, data quality issues, or edge cases that may affect modeling.

<Frame>
  <img alt="The image shows a table from a data analysis tool displaying anomalous samples from a Titanic dataset. It includes fields for anomaly scores, survival status, class, name, sex, and age of individuals." />
</Frame>

For any feature (for example, `Survived`) you can drill down to view:

* Histograms and distributions
* Validity and missing-value percentages
* Value counts or percentiles for numeric columns

These visual diagnostics inform decisions on encoding, scaling, binning, or additional cleaning before export.

<Frame>
  <img alt="The image shows a data analysis interface from AWS Data Wrangler featuring details about a binary feature named &#x22;Survived,&#x22; including its type, validity, and missing data percentage, alongside a histogram displaying the frequency of the feature's values." />
</Frame>

## Quick Step-by-Step Summary

1. Open SageMaker Canvas / Studio and launch Data Wrangler.
2. Import your dataset (e.g., CSV from `Amazon S3`).
3. Inspect inferred schema, distributions, and missing values.
4. Add transforms (imputation, encoding, normalization, custom formulas).
5. Run the flow and review the dataset summary and anomaly table.
6. Export the cleaned dataset to your training pipeline or notebook.

## Common Data Sources (examples)

| Source                 | Typical Use Case                                   |
| ---------------------- | -------------------------------------------------- |
| `Amazon S3`            | Batch CSV/Parquet files for bulk preprocessing     |
| `Redshift`             | Large data warehouse queries for ML-ready extracts |
| `Snowflake`            | Cloud data warehouse integrations                  |
| `PostgreSQL` / `MySQL` | Operational databases for feature extraction       |
| Local Upload           | Quick experimentation with small CSV files         |

## Links and References

* [Amazon Kinesis](https://aws.amazon.com/kinesis/) — real-time data streaming (for streaming ingestion pipelines)
* [Amazon SageMaker Data Wrangler](https://aws.amazon.com/sagemaker/data-wrangler/) — product page
* [SageMaker Studio documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html)
* [SageMaker Canvas](https://aws.amazon.com/sagemaker/canvas/)
* [Amazon S3 documentation](https://aws.amazon.com/s3/)

SageMaker Data Wrangler streamlines data import, visualization, cleaning, and transformation so you can prepare high-quality datasets for downstream model training and evaluation.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/9ddd44b0-7c9c-41a5-a515-cbb48405b70b" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/bdbe13ed-d6d2-400b-9562-b6e958004dc0" />
</CardGroup>
