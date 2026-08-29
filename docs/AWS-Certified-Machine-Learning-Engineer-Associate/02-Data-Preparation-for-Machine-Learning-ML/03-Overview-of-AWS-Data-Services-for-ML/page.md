# Drop rows with any missing values
df_dropped = df.dropna()

# Fill missing Age with median (robust to skew)
median_age = df["Age"].median()
df_filled = df.copy()
df_filled["Age"] = df_filled["Age"].fillna(median_age)
```

<Frame>
  <img alt="The image shows a comparison of tables labeled &#x22;Before&#x22; and &#x22;After&#x22; addressing missing values in the &#x22;Age&#x22; column, where a missing age value is filled with the median (37)." />
</Frame>

Inconsistent formats
Canonicalizing formats (especially dates and numeric strings) prevents parsing errors and ensures consistent sorting, filtering, and aggregation. Use robust parsing functions that can coerce invalid values to null for later inspection.

Example — parse dates and format as ISO 8601 with pandas:

```python theme={null}
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", infer_datetime_format=True)
# To format as ISO string:
df["timestamp_iso"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")
```

Duplicates
Duplicates inflate counts and skew model training. Remove exact duplicates or deduplicate using a subset of columns (e.g., id + timestamp), depending on the domain.

```python theme={null}
# Remove exact duplicate rows
df_unique = df.drop_duplicates()

# Remove duplicates based on subset of columns (e.g., id and timestamp)
df_unique_subset = df.drop_duplicates(subset=["id", "timestamp"])

# In-place single-line usage
df.drop_duplicates(inplace=True)
```

<Frame>
  <img alt="The image shows a table highlighting spelling/typo inconsistencies for country names associated with employee IDs. It suggests mapping these values to a controlled vocabulary for uniformity." />
</Frame>

Typos and inconsistent categorical values
Create a controlled vocabulary (mapping table) to normalize synonyms, abbreviations, and typos into a single canonical value. This improves feature consistency and reduces cardinality.

Example mapping:

```python theme={null}
mapping = {
    "US": "United States",
    "USA": "United States",
    "United States of America": "United States",
    "U.S.": "United States"
}
df["country_clean"] = df["country"].replace(mapping)
```

Outliers
Outliers can be legitimate or erroneous. Detect with domain thresholds, Z-score, or IQR. Handling strategies include removing, capping, or transforming the values.

Example — winsorization by clipping to 1st and 99th percentiles:

```python theme={null}
low, high = df["value"].quantile([0.01, 0.99])
df["value_clipped"] = df["value"].clip(lower=low, upper=high)
```

<Frame>
  <img alt="The image shows a table with &#x22;Before&#x22; and &#x22;After&#x22; columns illustrating how a temperature outlier (999°C) for SensorID S2 is replaced with a more realistic value (25°C). It suggests flagging and replacing extreme values using domain thresholds." />
</Frame>

Data type mismatches
Numeric values sometimes contain currency symbols, commas, or other non-numeric characters. Strip those characters and cast to numeric or datetime types. Coerce invalid parses to NaN for later handling.

Example — clean dollar amounts and convert to numeric:

```python theme={null}
import pandas as pd

# Remove non-numeric characters and convert to numeric (coerce errors to NaN)
df["price_clean"] = pd.to_numeric(
    df["price"].astype(str)
        .str.replace(r"[^\d\.\-]", "", regex=True)
        .replace("", pd.NA),
    errors="coerce"
)
```

<Frame>
  <img alt="The image shows a before-and-after comparison of a data table where non-numeric characters are stripped from a temperature column, converting it to a consistent float format." />
</Frame>

Data transformation
Cleaning fixes errors; transformation prepares features for learning algorithms. Typical transformations include scaling, encoding, aggregation, parsing, and binning.

<Frame>
  <img alt="The image describes four common data transformation techniques: scaling, encoding, aggregation, and date parsing. Each technique includes a brief explanation and an associated icon." />
</Frame>

Key transformation techniques

* Scaling / Normalization\
  Rescale numeric features so ones with large ranges don’t dominate models. Use Min-Max scaling to rescale to \[0, 1], or standardization (Z-score) to center to mean 0 and unit variance.

Example with scikit-learn:

```python theme={null}
from sklearn.preprocessing import MinMaxScaler, StandardScaler

scaler = MinMaxScaler()
df[["feature1_scaled"]] = scaler.fit_transform(df[["feature1"]])

std = StandardScaler()
df[["feature1_std"]] = std.fit_transform(df[["feature1"]])
```

<Frame>
  <img alt="The image illustrates data normalization using Min-Max Scaling, converting a range from 20-100 to a standardized range of 0-1." />
</Frame>

* Encoding categorical variables\
  Choose encoding based on model and cardinality:
  * One-hot encoding: creates binary columns per category (good for nominal features).
  * Label encoding: assigns integer codes (useful for ordinal or tree-based models).

Examples:

```python theme={null}
# One-hot (pandas)
df = pd.get_dummies(df, columns=["color"])

# Label encoding (scikit-learn)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df["color_label"] = le.fit_transform(df["color"].astype(str))
```

<Frame>
  <img alt="The image illustrates the process of encoding categorical variables by converting text labels (Red, Green, Blue) into numerical form (2, 1, 0)." />
</Frame>

* Binning (discretization)\
  Binning converts continuous variables into discrete intervals to reduce noise or improve interpretability. Use pd.cut for fixed bins or pd.qcut for quantiles.

Example — bin ages into categories:

```python theme={null}
bins = [0, 18, 35, 60, 200]
labels = ["Teen", "Young Adult", "Adult", "Senior"]
df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=True)
```

Note: pd.cut's `right` parameter controls whether the bins include the right edge; adjust `right=True`/`False` or bin edges to match your intended inclusive boundaries.

<Frame>
  <img alt="The image explains binning (discretization) of ages into categories: Teen (0-18), Young Adult (19-35), Adult (36-60), and Senior (60+), illustrating conversion of continuous variables into discrete intervals." />
</Frame>

Binning simplifies patterns and improves interpretability at the cost of some granularity. Choose bins with domain knowledge or data-driven methods.

AWS tools for cleaning and transformation
AWS offers managed services that streamline cleaning and transformation within ML workflows:

| Service                 | Purpose                                                               |
| ----------------------- | --------------------------------------------------------------------- |
| AWS Glue DataBrew       | Visual, no-code/low-code data cleaning and profiling                  |
| AWS Glue                | Serverless ETL for automated, scalable transformations                |
| Amazon EMR              | Distributed processing (Spark/Hadoop) for large-scale transformations |
| SageMaker Data Wrangler | Integrated data preparation and visualization inside SageMaker        |

* [AWS Glue DataBrew](https://aws.amazon.com/databrew/)
* [AWS Glue](https://aws.amazon.com/glue/)
* [Amazon EMR](https://aws.amazon.com/emr/)
* [SageMaker Data Wrangler](https://aws.amazon.com/sagemaker/data-wrangler/)

<Frame>
  <img alt="The image provides an overview of AWS tools for cleaning and transforming data, featuring AWS Glue DataBrew, AWS Glue, Amazon EMR, and Amazon SageMaker Data Wrangler." />
</Frame>

A typical AWS data-preparation workflow

1. Ingest raw data into Amazon S3 as the storage layer.
2. Use AWS Glue or AWS Glue DataBrew to profile, clean, and transform data.
3. For very large-scale processing, run jobs on Amazon EMR (Spark) or Glue ETL.
4. Load transformed data into SageMaker Data Wrangler or directly into SageMaker for feature engineering and model training.
5. Pass clean, transformed data to the model training environment or downstream analytics.

Summary and best practices

* Start with profiling to identify missing values, duplicates, inconsistent formats, outliers, and type issues.
* Prefer reproducible cleaning steps (notebooks, pipelines, or ETL jobs) so preprocessing can be audited and rerun.
* Use domain rules and statistical methods (imputation, deduplication, type conversion) for cleaning.
* Transform features to match algorithm expectations (scaling, encoding, binning, aggregation, parsing).
* Leverage managed tools (DataBrew, Glue, EMR, SageMaker Data Wrangler) to scale and standardize preparation steps.
* Document every transformation and preserve raw data to enable traceability and robust production deployments.

Further reading and references

* [Pandas Documentation](https://pandas.pydata.org/)
* [Scikit-learn Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
* [AWS Glue](https://aws.amazon.com/glue/)
* [Amazon EMR](https://aws.amazon.com/emr/)
* [SageMaker Data Wrangler](https://aws.amazon.com/sagemaker/data-wrangler/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/420acee5-f32e-423b-824d-a60fcf62f151)


# Overview of AWS Data Services for ML

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Overview-of-AWS-Data-Services-for-ML/page

Overview of AWS services for building end-to-end machine learning data pipelines including ingestion, storage, preparation, labeling, feature management, training, and orchestration.

AWS provides a comprehensive set of services to build end-to-end machine learning (ML) data pipelines. These services cover the common lifecycle stages: ingestion, storage, preparation, labeling, feature engineering, and training/orchestration. This article reviews each stage, highlights the most commonly used AWS services, and provides guidance to choose the right tool for your ML workloads.

Start-to-finish, a typical ML data pipeline includes:

* Ingestion — bringing data into AWS from devices, applications, or other systems.
* Storage — persisting raw and processed data in an appropriate store.
* Preparation — cleaning, transforming, and enriching data for ML.
* Labeling — annotating data for supervised learning.
* Feature engineering — creating and storing features for training and inference.
* Training and orchestration — running model training at scale and managing the ML workflow.

<Frame>
  <img alt="The image illustrates an ML Data Pipeline on AWS, outlining steps from data ingestion and storage to preparation, labeling, feature engineering, and training." />
</Frame>

Service summary: mapping pipeline stages to AWS offerings

| Pipeline Stage               | Purpose                                                 |                                                           Common AWS Services | When to choose                                                                                                                        |
| ---------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------------------------------- |
| Ingestion                    | Collect streaming or batch data from sources            |      Amazon Kinesis (Data Streams, Firehose), AWS IoT Core, AWS Data Pipeline | Low latency or streaming => Kinesis; device telemetry => IoT Core; scheduled batch workflows or legacy orchestration => Data Pipeline |
| Storage                      | Persist raw and processed data                          | `Amazon S3`, Amazon Redshift, Amazon RDS, Amazon DynamoDB, AWS Lake Formation | Data lake & artifacts => `S3`; analytical warehousing => Redshift; transactional => RDS; low-latency key-value => DynamoDB            |
| Preparation & Transformation | Clean, profile, and transform datasets for ML           |                                       AWS Glue, AWS Glue DataBrew, Amazon EMR | Serverless ETL & metadata catalog => Glue; interactive visual cleaning => DataBrew; large-scale Spark/Hadoop workloads => EMR         |
| Labeling                     | Create ground-truth annotations for supervised learning |                                                 Amazon SageMaker Ground Truth | Human-in-the-loop and auto-labeling support for scalable labeling workflows                                                           |
| Feature Management           | Store, serve, and share features across teams           |                                                Amazon SageMaker Feature Store | Ensure consistency between training and inference; provide low-latency online access                                                  |
| Training & Orchestration     | Run training jobs and manage ML pipelines               |                                   Amazon SageMaker (Training Jobs, Pipelines) | Managed training infrastructure, model management, and CI/CD integration                                                              |

Data ingestion on AWS

Choose ingestion services based on latency/throughput needs and destination targets (S3, Redshift, Feature Store, etc.):

* Amazon Kinesis (Data Streams and Data Firehose) — real-time streaming ingestion and delivery to targets such as `Amazon S3`, Redshift, or Elasticsearch.
* AWS Glue — ETL movement and transformation between stores when building batch pipelines.
* AWS Data Pipeline — orchestration for scheduled data movement and long-running or legacy workflows.
* AWS IoT Core — secure ingestion of telemetry and messages from connected devices.

Consider throughput, ordering guarantees, and the downstream target when selecting among these options.

<Frame>
  <img alt="The image shows icons representing different AWS data ingestion services: AWS Glue, Amazon Kinesis, AWS Data Pipeline, and AWS IoT Core." />
</Frame>

Storage: choose the right store for data type and access pattern

* `Amazon S3` — scalable object storage and the de facto data lake for raw and processed datasets, model artifacts, and feature export.
* Amazon Redshift — columnar data warehouse for analytical queries and BI workloads at scale.
* Amazon RDS — managed relational databases for structured OLTP workloads.
* Amazon DynamoDB — fully managed NoSQL key-value and document store for low-latency, high-scale access patterns.
* AWS Lake Formation — simplifies building, securing, and managing a centralized data lake on `S3` with fine-grained access control.

These options cover structured, semi-structured, and unstructured data. Use Lake Formation to centralize governance and fine-grained permissions.

<Frame>
  <img alt="The image lists different data storage services: Amazon S3, Amazon Redshift, Amazon RDS, Amazon DynamoDB, and AWS Lake Formation, each with their respective icons." />
</Frame>

Processing and transformation

Prepare data for ML by cleaning, profiling, and transforming at the required scale:

* AWS Glue — serverless ETL that discovers schemas, generates PySpark or Scala code, runs ETL jobs, and catalogs metadata in AWS Glue Data Catalog.
* AWS Glue DataBrew — a no-code/low-code visual tool for data cleaning, profiling, and exploration; great for analysts and data scientists collaborating on data prep.
* Amazon EMR — managed Hadoop/Spark cluster platform for large-scale distributed processing and custom Spark jobs where fine control and ecosystem tools are required.

Select Glue/DataBrew for serverless, fast development and EMR for heavy custom distributed processing or when you need advanced Spark/Hadoop control.

<Frame>
  <img alt="The image displays three AWS services for data processing and transformation: AWS Glue, AWS Glue DataBrew, and Amazon EMR, with a brief description of each." />
</Frame>

Labeling, feature management, and orchestration

* Amazon SageMaker Ground Truth — scalable labeling with human labelers, private workforces, and automated/ML-assisted labeling (active learning) to reduce cost and improve label quality.
* Amazon SageMaker Feature Store — centralized feature repository with both offline (batch) and low-latency online stores; supports consistent feature retrieval for training and inference.
* Amazon SageMaker Pipelines — orchestrate, automate, and version end-to-end ML workflows: data processing, training jobs, evaluation, and deployment. Pipelines integrates tightly with SageMaker components and other AWS services.

For training, use Amazon SageMaker training jobs (managed infrastructure) within SageMaker Pipelines to scale model training and track run metadata.

Integrated flow example

A common integrated flow looks like this:

1. Ingest streaming events with Kinesis or batch files into `Amazon S3`.
2. Catalog and transform data with AWS Glue (or run Spark jobs on EMR for large-scale processing).
3. Use SageMaker Ground Truth to label a representative subset of data.
4. Store engineered features in SageMaker Feature Store for reuse and consistent serving.
5. Orchestrate data processing, training, and deployment with SageMaker Pipelines and run managed SageMaker training jobs.

> **lightbulb** Select services based on data velocity, scale, and required SLAs: use streaming services (Kinesis) for real-time pipelines, EMR for heavy custom distributed processing, and serverless Glue/DataBrew for most ETL and interactive cleaning tasks.

Links and references

* [Amazon S3 — Object Storage](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [Amazon SageMaker — Managed ML Platform](https://learn.kodekloud.com/user/courses/aws-sagemaker)
* [AWS Glue — Serverless ETL](https://aws.amazon.com/glue/)
* [Amazon Kinesis — Real-time Data Streaming](https://aws.amazon.com/kinesis/)
* [Amazon EMR — Managed Hadoop/Spark](https://aws.amazon.com/emr/)
* [AWS Lake Formation — Data Lake Management](https://aws.amazon.com/lake-formation/)
* [Amazon RDS & DynamoDB — Managed Databases](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases)

Use this guide as a starting point to design ML-ready data pipelines on AWS. Choose services according to latency, throughput, operational model (serverless vs. managed clusters), and governance needs.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/13c68156-e0c4-47a0-b071-8cdd4d64d03a)
