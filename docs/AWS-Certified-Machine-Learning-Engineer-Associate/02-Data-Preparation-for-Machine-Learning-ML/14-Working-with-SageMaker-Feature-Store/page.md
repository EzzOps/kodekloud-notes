# Working with SageMaker Feature Store

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Working-with-SageMaker-Feature-Store/page

Overview of Amazon SageMaker Feature Store explaining centralized feature management, feature groups, online and offline stores, and best practices ensuring feature reuse and consistency across ML training

[Amazon SageMaker Feature Store](https://learn.kodekloud.com/user/courses/aws-sagemaker) is a managed AWS service that provides a centralized, versioned repository for the features used by your machine learning models. By defining and storing features once, teams can reuse them across projects, avoid duplicated transformation logic, and ensure consistency between training and production.

Common real-world scenario:

* Multiple ML teams consume the same core dataset (e.g., customer demographics, transactions, website activity) but build different models:
  * Team A: churn prediction
  * Team B: personalized product recommendations
  * Team C: suspicious login detection

When each team independently rebuilds transformations from raw data, the following issues typically occur:

* Duplicate feature-engineering logic across teams
* Training-serving skew (features used in training differ from those retrieved at serving)
* Inconsistent experiment and production results
* Increased maintenance costs for duplicated ETL/transformation code
* Reduced feature reuse and slower collaboration

A feature store solves these problems by centralizing feature definitions and computed values so all consumers read from a single source of truth.

<Frame>
  <img alt="The image illustrates a data pipeline using a feature store, showcasing engineers working on models, raw data feeding into a centralized feature store, and resulting models such as churn prediction, product recommendations, and fraud detection." />
</Frame>

Key benefits of using a feature store:

* Define features once and reuse them across teams and projects
* Eliminate training-serving skew through identical retrieval logic
* Improve collaboration and governance with a centralized catalog
* Reduce duplicated ETL and transformation maintenance

<Frame>
  <img alt="The image outlines the benefits of feature reuse, highlighting reduced feature duplication, improved collaboration and governance, and elimination of training-serving skew." />
</Frame>

Feature group fundamentals

* A feature group is a logical collection of related features for a specific use case (for example: churn prediction).
* Each record in a feature group represents an entity (e.g., a customer or transaction) and must include:
  * An entity identifier (primary key)
  * An event time or timestamp (for point-in-time correctness)
  * Feature columns with associated metadata (data types, descriptions, and transformation provenance)

This metadata enables consistent feature reuse across models and teams while preserving point-in-time correctness for model training and evaluation.

Typical architecture around a feature store:

* Raw data sources: databases, APIs, application logs, and streaming systems
* Ingestion/processing: ETL jobs, stream processors, or serverless functions that clean, transform, and compute features
* Feature Store: dual-storage system—an online store for low-latency serving and an offline store for large-scale batch access
* Consumers: live inference endpoints (real-time) and batch training/analytics jobs (historical / backfills)

<Frame>
  <img alt="The image is an architecture overview diagram explaining the flow from raw data sources to a feature store, which is then used for live inference and model training using services such as AWS Glue, Kinesis, Lambda, and SageMaker." />
</Frame>

Online vs Offline store — choose based on access patterns

| Store type    | Purpose                                                            | Typical latency            | Use cases                                               |
| ------------- | ------------------------------------------------------------------ | -------------------------- | ------------------------------------------------------- |
| Online store  | Low-latency, point-in-time feature retrieval for serving           | Millisecond-level          | Real-time inference, online features for APIs           |
| Offline store | Large-scale, historical feature storage for training and analytics | Seconds to minutes (batch) | Model training, backfills, feature engineering at scale |

Consumers select the appropriate store:

* Use the online store for real-time predictions requiring millisecond latency.
* Use the offline store for model training, backfills, and analytical queries that operate over historical snapshots.

Best practices (summary)

* Use feature groups to encapsulate entity keys, event timestamps, and feature metadata to ensure point-in-time correctness.
* Centralize feature transformations and lineage in the feature store to reduce duplication.
* Adopt consistent naming, typing, and documentation for features to enhance discoverability and governance.
* Automate ingestion and backfill pipelines to keep online and offline stores synchronized.

> **lightbulb** Use feature groups to encapsulate entity keys, event timestamps, and feature metadata. This ensures point-in-time correctness for training and consistent feature retrieval at serving time.

Links and references

* [AWS SageMaker Feature Store Developer Guide](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html)
* [Feature Store concepts and best practices](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-sagemaker-feature-store/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/66c19fc5-0e28-464b-aee4-52ef7f75b292)
