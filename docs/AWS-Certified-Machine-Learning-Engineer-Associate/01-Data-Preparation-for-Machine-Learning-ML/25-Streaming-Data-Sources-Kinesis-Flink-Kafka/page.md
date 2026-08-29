# X, y are your features and labels
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

smote = SMOTE(random_state=42, k_neighbors=5)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Train a classifier on X_resampled, y_resampled
```

References: [imbalanced-learn SMOTE documentation](https://imbalanced-learn.org/stable/over_sampling.html#smote)

Algorithm-level strategies

Algorithm-level methods modify how the model learns so it treats minority errors as more important without altering the dataset.

* Class weighting: increase the loss contribution of the minority class by assigning larger weights to its examples. Many libraries (e.g., scikit-learn) support a `class_weight` parameter.
* Cost-sensitive learning: implement a custom loss that penalizes different types of errors differently; useful when you know relative costs of false positives vs false negatives.
* Ensemble and sampling-aware models: balanced random forests, boosting with class weights, or bagging combined with resampling can improve minority detection by aggregating multiple models and controlling sampling or weighting. Libraries to explore: [XGBoost](https://xgboost.readthedocs.io/en/stable/), [LightGBM](https://lightgbm.readthedocs.io/en/latest/).

<Frame>
  <img alt="The image outlines an algorithm-level strategy for handling data by assigning class weights, giving high weight to the minority class and low weight to the majority class." />
</Frame>

Example: class weights in scikit-learn

```python theme={null}
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Option 1: let scikit-learn compute balanced weights automatically
clf = LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Option 2: provide manual weights, e.g., {0: 1.0, 1: 10.0}
clf = LogisticRegression(class_weight={0: 1.0, 1: 10.0}, random_state=42, max_iter=1000)
```

Choosing a strategy: quick guidance

* If you have plenty of majority examples and training time matters: consider undersampling or ensemble methods with sampling.
* If discarding majority data is risky: use oversampling (SMOTE or variants) or class weighting.
* If misclassification costs are known or asymmetric: use cost-sensitive models or manual class weights.
* For image/text data: prefer domain-specific augmentation over SMOTE.

Summary table of strategies

| Strategy type                                     | When to use                                         | Pros                                                 | Cons                                               |
| ------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------------- | -------------------------------------------------- |
| Random oversampling                               | Small to moderate imbalance, limited majority data  | Simple to apply, increases minority representation   | Can overfit due to duplicates                      |
| Random undersampling                              | Very large datasets where training time matters     | Reduces training time and storage                    | May remove useful information                      |
| SMOTE & variants                                  | Tabular data where synthetic examples are plausible | Generates diverse minority data, reduces duplication | Can create noisy/borderline samples; needs scaling |
| Class weighting / cost-sensitive                  | When you can alter loss or costs                    | No change to dataset; works with many models         | May need careful tuning of weights                 |
| Ensemble methods (balanced RF, weighted boosting) | Complex problems requiring robustness               | Combines models, can balance sampling & weighting    | More complex to tune and compute                   |

Validation and best practices

* Always split first: train/validation/test splits must be done before any resampling. Use stratified splitting to preserve class ratios in evaluation folds.
* Use appropriate metrics: precision, recall, F1, PR AUC, and ROC AUC. Select the metric that reflects business impact (e.g., recall for capturing fraud).
* Use stratified cross-validation when tuning hyperparameters to maintain class balance across folds.
* Monitor overfitting: when using oversampling, compare performance on validation/test sets to detect over-optimistic training results.
* For thresholded classifiers, tune decision thresholds using validation metrics that matter (e.g., maximize F1 or a weighted cost function).

Further reading and references

* [imbalanced-learn documentation (SMOTE and resampling)](https://imbalanced-learn.org/stable/)
* [scikit-learn model weighting and metrics](https://scikit-learn.org/stable/)
* [XGBoost documentation](https://xgboost.readthedocs.io/en/stable/)
* [LightGBM documentation](https://lightgbm.readthedocs.io/en/latest/)

In short: diagnose imbalance, pick metrics that reflect your objective, split data before resampling, and combine data-level and algorithm-level techniques as needed. Test thoroughly using stratified validation and the metrics that matter to your problem to avoid leakage and to get reliable performance estimates.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/29abbd70-ba8c-4a4e-a91b-a758fbe09112" />
</CardGroup>


# Streaming Data Sources Kinesis Flink Kafka

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Streaming-Data-Sources-Kinesis-Flink-Kafka/page

Comparing AWS Kinesis, Amazon Managed Flink, and Apache Kafka/MSK for building real-time streaming pipelines and ML feature processing, detailing components, trade-offs, and integration options.

Traditional ML relies on static datasets, but many modern applications—fraud detection, anomaly detection, and personalized recommendations—require decisions as data arrives. Streaming data enables models and systems to adapt quickly, delivering low-latency predictions and insights that batch processing cannot provide.

Streaming transforms

<Frame>
  <img alt="The image compares two approaches to using streaming data for machine learning: training the model periodically with delayed predictions and updating the model incrementally for real-time predictions." />
</Frame>

static insights into continuous, real-time intelligence. This lets models stay current, react to new patterns, scale to high input volumes, and enable use cases that require immediate action.

Overview: core streaming components

* Streaming backbones — transport continuous event data (examples: Kinesis Data Streams, Kafka).
* Processing engines — apply real-time logic, transformations, and feature engineering (examples: Flink, Lambda).
* Delivery & integrations — reliably deliver streams to storage or analytics targets (example: Kinesis Data Firehose).
* Analytics & consumers — dashboards, ML models, or downstream applications that consume processed streams.

<Frame>
  <img alt="The image is an overview of a streaming data pipeline, detailing steps from ingestion and transport to processing, delivery, and analytics. It mentions tools and services like Kinesis, Kafka, Flink, and Lambda." />
</Frame>

Below is a focused look at AWS-native streaming options (Kinesis family and Flink on AWS) and alternative open-source options (Apache Kafka and Flink). Each plays a distinct role in real-time ML pipelines.

AWS streaming services — components and roles

Kinesis overview

* Kinesis Data Streams and Kinesis Video Streams — ingest real-time telemetry, events, and media.
* Kinesis Data Firehose — serverless delivery for loading streaming data into S3, Redshift, Amazon OpenSearch Service, and other sinks.
* Kinesis Data Analytics — SQL-based stream processing for simple analytics and the ability to run Apache Flink applications for complex processing.

<Frame>
  <img alt="The image is an infographic showing Amazon Kinesis, an AWS-native streaming service, with icons representing its components: Video Streams, Data Streams, and Data Firehose." />
</Frame>

Kinesis Data Firehose — serverless delivery
Amazon Kinesis Data Firehose is a managed ETL-style delivery service that captures, transforms, buffers, and loads streaming data into data lakes and analytics stores with minimal operational overhead. Firehose supports lightweight transformations (including via AWS Lambda), format conversions (e.g., to Parquet/ORC), buffering and batching, and automated retries.

<Frame>
  <img alt="The image is a diagram showing the data flow of Amazon Kinesis Data Firehose, with inputs leading into Amazon Kinesis and outputting to Amazon S3." />
</Frame>

Kinesis Data Streams — key characteristics

* Real-time processing: ingest and analyze streaming data with minimal delay to enable timely detections and responses.
* Scalability: scale throughput by increasing the number of shards.
* Durability & availability: records are replicated across Availability Zones.
* AWS integration: native connectors to S3, Redshift, SageMaker, Lambda, and more for downstream ML and analytics.
* Custom applications: SDKs and client libraries enable bespoke consumer applications.

<Frame>
  <img alt="The image lists five features of Kinesis: real-time data processing, scalability, data durability and availability, integration with AWS services, and custom application building." />
</Frame>

Typical AWS-native streaming pipeline

* Producers (mobile apps, IoT devices, application logs) publish events to Kinesis Data Streams.
* Consumers (AWS Lambda, Flink, or custom applications) process events in real time.
* Kinesis Data Firehose handles delivery to storage and analytics with managed batching and retries.
* Final sinks commonly include Amazon S3, Amazon Redshift, and Amazon OpenSearch Service.

<Frame>
  <img alt="The image illustrates an AWS-native service data flow, showing how data moves from producers through Amazon Kinesis Data Streams to Amazon Kinesis Data Firehose, and finally into outputs like S3, Redshift, or OpenSearch." />
</Frame>

When to choose Amazon Kinesis

* You want a fully managed, AWS-native streaming backbone with low operational overhead.
* Your workload requires low-latency, high-throughput streaming on AWS.
* Tight integration with AWS analytics and ML services (S3, Redshift, SageMaker, Lambda) is important.

<Frame>
  <img alt="The image is a graphic explaining when to use Amazon Kinesis, highlighting three points: needing a fully managed AWS service, demanding low-latency high-throughput streaming, and wanting integration with other AWS services like S3, Redshift, and SageMaker." />
</Frame>

<Callout icon="lightbulb">
  A single Kinesis shard supports roughly 1 MB/second of data write throughput and about 2 MB/second of data read throughput, plus up to 1,000 PUT records/second. Use these figures to plan shard counts based on your ingest and consumer patterns.
</Callout>

Apache Flink — advanced stream processing
Apache Flink is an open-source, distributed engine for stateful stream processing over unbounded data. On AWS, Amazon Managed Service for Apache Flink simplifies deployment, scaling, and operations.

Flink is especially appropriate when you need advanced features such as event-time semantics, complex windowing, large stateful computations, and strong processing guarantees for ML feature engineering and analytics.

<Frame>
  <img alt="The image is a flow diagram showing data processing using Amazon Managed Service for Apache Flink, with data moving from producers to Amazon Kinesis Data Streams, then to Apache Flink for real-time processing, and finally to output services like Amazon S3, Redshift, and OpenSearch." />
</Frame>

Amazon Managed Service for Apache Flink — strengths

* Stream-first architecture: all data is treated as streams, enabling continuous processing.
* Event-time processing: watermarks and event-time semantics handle out-of-order events.
* Stateful computations: support for large application state across event streams for complex joins and aggregations.
* Exactly-once consistency: strong guarantees when configured with state backends and checkpointing.
* Rich connectors: integrate with Kafka, Kinesis, HDFS, Cassandra, Elasticsearch/OpenSearch, JDBC, and cloud storage.

Apache Kafka and Amazon MSK
Kafka is an open-source streaming platform focused on durability, replayability, and ordering semantics. It is a common choice for multi-cloud or hybrid architectures and for teams that depend on Kafka’s ecosystem.

Amazon Managed Streaming for Apache Kafka (Amazon MSK) provides a managed Kafka control plane while preserving the Kafka-compatible APIs and ecosystem.

Typical Kafka + Flink architecture

* Producers push events to Kafka topics (MSK).
* A stream processor (often Flink) consumes topics, applies business logic (filtering, aggregation, complex event patterns).
* Processed results are written to sinks such as Amazon S3, Redshift, or OpenSearch, or forwarded to downstream apps.

When to choose Kafka / Amazon MSK

* You operate Kafka on-premises or across clouds and need compatibility.
* You require explicit replay semantics, fine-grained partition control, or advanced ordering guarantees.
* You want the flexibility of Kafka’s ecosystem but prefer delegating infrastructure management to AWS.

High-level comparisons

| Aspect            | Amazon Kinesis                                               | Apache Kafka / Amazon MSK                                         |
| ----------------- | ------------------------------------------------------------ | ----------------------------------------------------------------- |
| Management        | Fully managed AWS-native service                             | Managed option via Amazon MSK; still Kafka-compatible             |
| Ecosystem         | Deep integration with AWS services (S3, Redshift, SageMaker) | Broader open-source ecosystem, many connectors and tools          |
| Replay & Ordering | Ordering per shard; replay within retention window           | Robust replay via offsets; fine-grained partitioning and ordering |
| Best fit          | AWS-centric, serverless-focused pipelines                    | Multi-cloud/hybrid setups, Kafka-dependent ecosystems             |

Purpose-focused comparison

| Purpose                | Kinesis Data Streams                       | Managed Flink (Amazon)                   | Kafka / MSK                                     |
| ---------------------- | ------------------------------------------ | ---------------------------------------- | ----------------------------------------------- |
| Ingestion backbone     | Yes — AWS-native ingestion                 | No (processing engine)                   | Yes — widely used ingestion backbone            |
| Stream processing      | Basic via Kinesis Data Analytics or Lambda | Primary — advanced stateful processing   | Works with Flink, Spark, etc. for processing    |
| Exactly-once semantics | Limited compared to Flink                  | Strong exactly-once when configured      | Depends on consumer/processing engine           |
| Integration            | Native AWS integrations                    | Integrates with Kinesis, Kafka, S3, etc. | Wide connector support; cross-cloud flexibility |

Summary
This guide covered the roles and trade-offs for:

* Streaming backbones: Amazon Kinesis Data Streams and Apache Kafka (Amazon MSK).
* Processing engines: Apache Flink (Amazon Managed Service for Apache Flink) for advanced stateful processing.
* Delivery services: Amazon Kinesis Data Firehose for serverless, reliable delivery to data lakes and analytics.

Choosing between these options depends on operational preferences (fully managed AWS vs. open-source flexibility), required processing semantics (event-time, stateful computations, exactly-once), and the need for tight AWS integration.

Links and references

* [Amazon Kinesis Data Streams](https://docs.aws.amazon.com/streams/latest/dev/introduction.html)
* [Amazon Kinesis Data Firehose](https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html)
* [Amazon Managed Service for Apache Flink](https://docs.aws.amazon.com/managed-flink/latest/developerguide/what-is.html)
* [Apache Kafka](https://kafka.apache.org/)
* [Amazon MSK (Managed Streaming for Apache Kafka)](https://aws.amazon.com/msk/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/6d1264a6-f345-403e-bce6-35d88208819f" />
</CardGroup>
