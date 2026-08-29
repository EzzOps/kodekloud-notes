# Summary of Domain 1 Data Preparation for ML

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Bringing-it-all-together/Summary-of-Domain-1-Data-Preparation-for-ML/page

Overview of data preparation for machine learning, covering cleaning, transformation, feature engineering, labeling, validation, security, and AWS tools for scalable, reproducible pipelines and production-ready models.

This summary covers the essential steps to convert raw data into high-quality inputs for machine learning (ML) models. Effective data preparation improves model accuracy, reduces bias, and ensures reproducible, production-ready ML pipelines.

> **lightbulb** High-quality data is the foundation of reliable ML: "Garbage In, Garbage Out" — thorough data preparation is essential for meaningful results.

The data-preparation workflow is a sequence of stages that progressively refine raw data into training-ready datasets:

* Cleaning — remove or correct inaccuracies, duplicates, and inconsistent values.
* Transformation — reshape and encode data into formats suitable for models.
* Feature engineering — create, aggregate, and select informative signals.
* Labeling — provide ground-truth annotations for supervised learning.
* Validation — verify dataset quality, distributional assumptions, and readiness to train.

<Frame>
  <img alt="The image outlines the benefits of data preparation with a sequential process: Cleaning, Transformation, Feature Engineering, Labeling, and Validation, emphasizing the principle &#x22;Garbage In, Garbage Out.&#x22;" />
</Frame>

Feature engineering should be driven by the problem statement and the characteristics of available data. Typical activities include:

* Derive features from raw signals (e.g., time-window aggregations, ratios).
* Convert features into modeling-friendly representations (numeric, normalized).
* Perform feature selection to keep signals that improve predictive power.
* Validate features for stability over time and guard against data leakage.

Common transformation techniques used before training:

| Technique   | Typical methods / examples                                                |
| ----------- | ------------------------------------------------------------------------- |
| Scaling     | Min–max scaling, z-score (standard) normalization                         |
| Encoding    | One-hot encoding, label encoding, target/binary encoding for categoricals |
| Aggregation | Group-level statistics: sum, count, mean, median                          |
| Parsing     | Extract structured parts: day/month/hour from timestamps, JSON fields     |
| Binning     | Discretize continuous variables into ordinal ranges                       |

<Frame>
  <img alt="The image lists data transformation techniques before training machine learning models: scaling, encoding, aggregation, data parsing, and binning, each with specific methods." />
</Frame>

A practical feature engineering workflow:

1. Define the business problem and inventory data sources (logs, databases, events).
2. Clean and preprocess raw inputs (handle missing values, deduplicate, normalize).
3. Generate candidate features via derivation and aggregation.
4. Transform features into numeric, normalized, or encoded forms for modeling.
5. Select and validate the final feature set (cross-validation, importance, stability).
6. Deploy the model with a reproducible feature pipeline and maintain it in production.

<Frame>
  <img alt="The image is a diagram illustrating feature engineering with AWS using AWS Feature Store. It shows the process from raw data to training models for churn prediction, recommendations, and fraud detection." />
</Frame>

AWS Feature Store centralizes feature storage and enables consistent feature reuse across teams and environments. Raw source data is processed into feature values, stored in Feature Store, and then retrieved for training and inference — providing a single source of truth and reducing feature drift.

For data quality and validation on AWS, the following services are commonly used:

* [AWS Glue DataBrew](https://docs.aws.amazon.com/databrew/latest/userguide/what-is-databrew.html) — interactive data cleaning and visual transformations.
* [Amazon SageMaker Clarify](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify.html) — bias detection, feature importance, and explainability.
* [Amazon SageMaker Data Wrangler](https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html) — interactive and automated data preparation for ML.

<Frame>
  <img alt="The image is a list of AWS tools for data quality and validation, including AWS Glue DataBrew, Amazon SageMaker Clarify, and Amazon SageMaker Data Wrangler, each with a corresponding icon." />
</Frame>

Security and privacy must be incorporated through the entire data lifecycle:

* Encrypt data at rest (S3, EBS, RDS) and in transit (HTTPS, service endpoints).
* Protect data during processing and training (for example, when using Amazon SageMaker).
* Apply fine-grained access controls (IAM), auditing, and monitoring to prevent unauthorized access.
* Use masking or tokenization to remove or obscure sensitive fields for development and testing.

<Frame>
  <img alt="The image outlines the encryption lifecycle in ML pipelines, showing data at rest (Amazon S3, EBS, RDS), data in transit (services, HTTPS, endpoints), and data during processing (Amazon SageMaker)." />
</Frame>

Data masking (redaction or tokenization) helps preserve dataset utility while protecting sensitive values. Masking replaces critical parts of values (for example, credit card or account numbers) so teams can develop and test without exposing real PII.

<Frame>
  <img alt="The image illustrates a &#x22;Data Marking&#x22; process where sensitive information, such as a credit card and bank account numbers, is masked or redacted." />
</Frame>

Detecting and automating responses to sensitive data can be implemented using AWS services like Amazon Macie. A typical automated workflow:

1. Macie scans S3 buckets and detects PII or other sensitive content.
2. Macie sends findings to Amazon EventBridge.
3. EventBridge triggers an AWS Lambda to notify or remediate (notify data protection/compliance teams).

<Frame>
  <img alt="The image illustrates a process using Macie to detect and classify sensitive data in an S3 bucket, activate a Lambda function via EventBridge, and notify the Data Protection team." />
</Frame>

Training workflows with Amazon SageMaker commonly use Amazon S3 as the central data and artifact store:

* Store processed training datasets and feature artifacts in S3.
* SageMaker pulls training data and executes training jobs (single-node or distributed).
* Save model artifacts (checkpoints and final models) back to S3 for deployment and reproducibility.

<Frame>
  <img alt="The image illustrates a process flow for training machine learning models using Amazon SageMaker, showing interaction between Amazon S3 and SageMaker for data and model artifacts." />
</Frame>

For large-scale or distributed training, SageMaker can provision multiple instances (EC2 nodes) running in parallel and rely on shared storage such as Amazon EFS to host datasets, checkpoints, and logs.

<Frame>
  <img alt="The image is a diagram showing distributed training with Amazon SageMaker, illustrating connections between EC2 training nodes and shared storage using Amazon EFS." />
</Frame>

For real-time and streaming data ingestion, consider the Amazon Kinesis family:

* Kinesis Video Streams — capture and process video streams.
* Kinesis Data Streams — ingest and store real-time records.
* Kinesis Data Firehose — reliably load streaming data into AWS destinations.
* Kinesis Data Analytics — run SQL or Apache Flink applications on streaming data.

You can build streaming pipelines using Amazon Kinesis Data Analytics (Apache Flink): consume from Kinesis or Kafka, run real-time transformations with Flink, and write results to sinks such as S3, Redshift, or OpenSearch.

<Frame>
  <img alt="The image is a flow diagram showing the process of Amazon Managed Services for Apache Flink, including stages for data ingestion, real-time processing, and output/sinks. It involves Kinesis/Kafka Streams, Amazon MSF (Flink App), and various storage solutions like S3, Redshift, and OpenSearch." />
</Frame>

Labeling is a critical step for supervised ML. Amazon SageMaker Ground Truth streamlines labeling by combining human labelers with automated model-assisted labeling to generate high-quality labeled datasets stored in S3.

<Frame>
  <img alt="The image illustrates the workflow of Amazon SageMaker Ground Truth, showing the process from input data to labeled dataset using human labelers and auto-labeling machine learning." />
</Frame>

Because ML datasets often contain sensitive or regulated information, implement security and compliance controls appropriate to your domain. Common standards include:

* PCI DSS — payment card data protection.
* HIPAA — protected health information (PHI) controls.
* GDPR — data protection and subject rights for EU personal data.

<Frame>
  <img alt="The image highlights the importance of data security in machine learning, referencing compliance standards like PCI DSS, HIPAA, and GDPR." />
</Frame>

Key takeaways

* Data preparation is critical: careful preprocessing and validation directly improve model performance and reliability.
* Feature engineering concentrates modeling effort on the most informative and stable signals.
* AWS offers services that support local experimentation, managed pipelines, distributed training, streaming analytics, and reusable features to scale from prototypes to production.

<Frame>
  <img alt="The image is a summary slide that outlines three points about machine learning: the importance of data preprocessing, the role of feature engineering, and the capabilities of AWS in scaling model training." />
</Frame>

Amazon SageMaker Ground Truth supports human-in-the-loop labeling for many supervised tasks. In addition to labeling, AWS provides integrated tooling across the data lifecycle to help maintain security, ensure compliance, and automate feature reuse and streaming analytics.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/dd1231df-ce1b-453d-92d6-e6250b5d45cf/lesson/ae508a07-737e-4428-8037-a3cd0a24fc96)
