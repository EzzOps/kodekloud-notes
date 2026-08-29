# Demo Implementing Data Drift Detection

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Solution-Monitoring-Maintenance-and-Security/Demo-Implementing-Data-Drift-Detection/page

Guide to detecting and monitoring data drift with Amazon SageMaker Model Monitor, creating baselines, running statistical checks, and responding to drift in production.

Welcome back. In this lesson we cover data drift: what it is, why it matters, and how to configure a baseline and monitoring so Amazon SageMaker can detect drift in incoming requests. This guide explains the concepts, how SageMaker Model Monitor uses a baseline, and includes a minimal Python example to generate baseline statistics and constraints.

What you'll learn

* What data drift is and how it impacts model quality.
* How to create a representative baseline dataset.
* How SageMaker computes and compares statistics at runtime.
* How to view and act on drift detection results.

## What is data drift and why it matters

Data drift occurs when the distribution or characteristics of incoming data differ significantly from the data that a model was trained on. When requests fall outside the ranges or distributions the model expects, predictions can become unreliable, potentially harming business outcomes.

SageMaker Model Monitor uses a reference distribution — the baseline dataset — to represent expected feature statistics (e.g., ranges, histograms, percentiles). At runtime, Model Monitor computes the same statistics on incoming requests (or a sample) and compares them to the baseline using statistical checks. Significant deviations are flagged as drift so you can investigate and remediate.

<Frame>
  <img alt="The image shows the user interface of Amazon SageMaker, specifically the &#x22;Create monitor&#x22; section for configuring data quality monitoring settings. It includes options for setting the monitor type, baseline dataset S3 location, and S3 output location." />
</Frame>

## How SageMaker Model Monitor uses a baseline

When you provide a baseline dataset (typically an S3 CSV path), SageMaker computes per-feature statistics such as:

* Ranges and percentiles
* Histograms and distributions
* Categorical frequencies
* Missing-value counts

These statistics are stored as baseline statistics and optional constraint files. During monitoring, Model Monitor computes the same statistics on incoming records and runs statistical checks (e.g., population stability index, KS-test) to detect:

* Univariate shifts such as changes in mean or variance
* Categorical distribution shifts (new categories or frequency changes)
* Out-of-range values or increased missingness

If a statistic deviates beyond configured thresholds, Model Monitor marks the check as failed and logs the results.

> **lightbulb** Provide a representative baseline. The baseline should reflect the expected production distribution (for example, the final processed training data). If the baseline is not representative, Model Monitor will generate misleading drift signals.

## Typical outcomes of drift detection

| Outcome                       | What it detects                                            | Next steps                                                     |
| ----------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------- |
| Univariate shifts             | Mean, variance, or percentile changes for numeric features | Investigate data preprocessing or upstream data source changes |
| Categorical shifts            | New categories or changed frequency distributions          | Map new categories, update encoding, or retrain                |
| Out-of-range / missing values | Values falling outside expected ranges or increased nulls  | Validate input sanitation, check upstream pipelines            |
| Alerts / Logs                 | Failed checks emitted and results written to S3            | Configure CloudWatch alarms and incident response playbooks    |

## Create a baseline programmatically (minimal example)

Use the SageMaker Model Monitor Python SDK to suggest baseline statistics and constraints from an S3 CSV. The example below shows a minimal setup that generates the baseline output in S3.

```python theme={null}
from sagemaker import Session
from sagemaker.model_monitor import DefaultModelMonitor, DatasetFormat
