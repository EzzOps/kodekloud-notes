# Data Quality and Validation

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Data-Quality-and-Validation/page

Overview of data quality and validation for machine learning, covering quality dimensions, validation techniques, common issues, drift detection, and mitigation practices for reliable, fair, and robust models

Data quality and validation are foundational to reliable machine learning (ML). No matter how advanced the model architecture, poor input data will produce unreliable or biased predictions. Validation detects issues early in the pipeline so models train on accurate, consistent, and relevant data—reducing risk and improving model performance, fairness, and trustworthiness.

<Frame>
  <img alt="The image is an illustration emphasizing the importance of data quality in machine learning, showing two people interacting with a robot and lists the impacts of inaccurate, good, and poor-quality data on model predictions." />
</Frame>

Why this matters

* Models learn patterns from training data. If that data is inaccurate, incomplete, or inconsistent, models will learn wrong or biased patterns.
* High-quality data leads to better accuracy, fairness, and reliability in production.
* Validation reduces costly mistakes by preventing bad data from reaching training or inference stages.

## Key dimensions of data quality

Use these dimensions as a checklist when assessing any ML dataset:

| Dimension    |                                                What it checks | Typical question to ask                          |
| ------------ | ------------------------------------------------------------: | ------------------------------------------------ |
| Accuracy     |                   Is each value correct and free from errors? | "Does the data reflect reality?"                 |
| Completeness |                  Are required fields present for each record? | "Are any sensors or attributes missing?"         |
| Consistency  | Is the same information represented uniformly across sources? | "Do formats and units match across datasets?"    |
| Timeliness   |                  Is the data recent and relevant to the task? | "Is the data up to date for current conditions?" |
| Uniqueness   |                   Are there duplicate records or identifiers? | "Does each logical entity appear once?"          |

<Frame>
  <img alt="The image outlines the dimensions of data quality, including accuracy, consistency, uniqueness, completeness, and timeliness, with accompanying questions and icons for each." />
</Frame>

Concrete analogies help: imagine a spacecraft navigation system reporting 10,000 km to Mars when the true distance is 100,000 km. Decisions based on that inaccurate reading could result in mission failure—this illustrates how critical accuracy is for real-world outcomes.

<Frame>
  <img alt="The image illustrates the concept of data quality accuracy, showing a cartoon rocket incorrectly measuring its distance to Mars, emphasizing the impact of inaccurate data on real-world outcomes." />
</Frame>

Completeness covers missing values: if a dataset should include readings from five sensors but only three report values, analyses and models will be skewed by those gaps.

<Frame>
  <img alt="The image illustrates the concept of data quality in terms of completeness, showing five sensors, with three providing data and two not providing data, represented by check and cross symbols." />
</Frame>

Timeliness ensures the data reflects current conditions. In space missions, delayed asteroid alerts could be catastrophic; similarly, outdated training data can cause models to miss evolving trends and perform poorly.

<Frame>
  <img alt="The image depicts a concept of &#x22;Dimensions of Data Quality: Timeliness&#x22; with a rocket, an asteroid, and a note emphasizing the importance of real-time asteroid alerts during space travel." />
</Frame>

Other important dimensions include consistency, validity (data conforms to rules and allowed domains), and uniqueness. Together they help produce clean, standardized datasets ready for ML.

<Frame>
  <img alt="The image illustrates three dimensions of data quality: consistency, validity, and uniqueness, each with a brief explanation and an icon." />
</Frame>

Common raw-data issues

* Noise and random measurement errors
* Duplicates or repeated records
* Missing or incomplete fields
* Inconsistent formats and units across sources

These problems should be detected and remediated before training to avoid degraded model performance.

<Frame>
  <img alt="The image lists common data quality issues: noise and random errors, duplicates, missing values, incomplete fields, and inconsistencies across formats or sources." />
</Frame>

## Data validation in ML: purpose and workflow

Data validation verifies that the data used for training, validation, and testing is accurate, consistent, and fit for purpose. Because ML models are data-driven, validation is essential to avoid biased, misleading, or poorly performing systems.

Typical validation workflow:

1. Raw data ingests into a staging area or pipeline.
2. Run automated validation checks (schema, statistics, completeness).
3. Flag, correct, or remove problematic records.
4. Produce a validated dataset for training and evaluation.

<Frame>
  <img alt="The image presents four data validation techniques: schema validation, statistical validation, completeness checks, and cross-split validation. Each technique includes a brief description of its purpose." />
</Frame>

## Common validation techniques

| Technique                           |                                                              What it checks | Typical remediation                                               |
| ----------------------------------- | --------------------------------------------------------------------------: | ----------------------------------------------------------------- |
| Schema validation                   | Required columns exist, types match (e.g., float vs int, string vs numeric) | Reject or coerce records, enforce schema contracts                |
| Statistical validation              |                          Feature distributions, outliers, improbable values | Flag outliers, clip or impute extreme values, investigate sources |
| Completeness / Missing-value checks |                                   Presence of mandatory fields and coverage | Impute (mean/mode/ML), drop rows, or flag for review              |
| Cross-split (train/test) validation |                     Distribution differences between training and test sets | Rebalance sampling, collect more representative data, retrain     |

<Frame>
  <img alt="The image is a &#x22;Schema Validation&#x22; table showing sensor data, highlighting a type mismatch where a temperature value is a float instead of an integer. It includes columns for SensorID as strings and Temperature in Celsius as integers." />
</Frame>

Schema validation

* Verifies column names, types, nullability, and allowed ranges.
* Prevents runtime errors when training pipelines expect a specific structure.

<Frame>
  <img alt="The image shows a table titled &#x22;Statistical Validation&#x22; with sensor IDs and corresponding temperatures, highlighting a temperature of 999 as an outlier." />
</Frame>

Statistical validation

* Compares feature distributions (mean, variance, quantiles) against expected ranges.
* Detects outliers or improbable values (e.g., age = 999).
* Useful for automated alerts when distribution drift occurs.

<Frame>
  <img alt="The image is a data table labeled &#x22;Completeness/Missing Values,&#x22; showing entries for AstronautID, Age, and Country, with a missing value highlighted in the Country column for AstronautID 1002." />
</Frame>

Completeness / missing-value checks

* Identify absent mandatory fields and estimate coverage.
* Decide on imputation strategies (mean, median, mode, model-based) or exclusion policies depending on the use case.

<Frame>
  <img alt="The image illustrates a concept of cross-split validation, showing a comparison between train and test sets, with a focus on age distribution and highlighting a distribution shift." />
</Frame>

Cross-split validation

* Compare key statistics across train/validation/test splits to detect distribution shift.
* Example: a training-set average age of 49 vs. test-set average of 23.5 signals a problematic shift that can reduce generalization.

Categorical validation

* Ensure categories use only allowed or expected values.
* Strategies: map invalid entries to a special `unknown` category, replace with the mode, or consult domain experts when values indicate upstream issues.

## Tools and services (AWS examples)

| Service                                                                           | Purpose                                                                                                                           |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| [AWS Glue DataBrew](https://aws.amazon.com/databrew/)                             | No-code data preparation and profiling; detects missing values, duplicates, and anomalies; enforces schema rules.                 |
| [Amazon SageMaker Clarify](https://aws.amazon.com/sagemaker/clarify/)             | Bias detection and model explainability; helps validate fairness and detect dataset/model issues.                                 |
| [Amazon SageMaker Data Wrangler](https://aws.amazon.com/sagemaker/data-wrangler/) | Visual cleaning, transformation, and validation; profiles datasets and applies consistent transformations for training/inference. |

<Callout icon="lightbulb">
  Data validation is not a one-time activity. Integrate automated checks into ingestion and training pipelines and add production monitoring (metrics, alerts) to catch drift, schema changes, or emerging data-quality problems early.
</Callout>

## Data drift and model degradation

Data drift occurs when production data diverges from the data on which the model was trained. Types of drift:

* Covariate shift — Input feature distributions change.
* Prior-probability shift — Class priors (label proportions) change.
* Concept drift — The relationship between features and the target evolves.

Consequences include reduced accuracy, harmful biases, and unreliable predictions. Detection approaches:

* Monitor feature distributions and key statistics over time.
* Track model performance metrics (accuracy, precision/recall, calibration) on recent data.
* Implement alerting thresholds for significant distribution or performance changes.

Mitigations:

* Trigger automated retraining or fine-tuning pipelines when drift is detected.
* Ensure consistent feature engineering between training and inference.
* Keep a rolling or periodically refreshed validation dataset that reflects production conditions.
* Use incremental learning or continuous training for rapidly changing domains.

<Callout icon="warning">
  Without continuous validation and monitoring, even well-trained models will degrade as data and environments change. Implement automated drift detection, alerts, and retraining workflows to maintain model reliability.
</Callout>

Further reading and references

* [Kubernetes Documentation](https://kubernetes.io/docs/) — (general infra reference)
* [AWS Glue DataBrew](https://aws.amazon.com/databrew/)
* [Amazon SageMaker Clarify](https://aws.amazon.com/sagemaker/clarify/)
* [Amazon SageMaker Data Wrangler](https://aws.amazon.com/sagemaker/data-wrangler/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/d8809670-e614-4b8f-9d33-f53aa30526ed" />
</CardGroup>
