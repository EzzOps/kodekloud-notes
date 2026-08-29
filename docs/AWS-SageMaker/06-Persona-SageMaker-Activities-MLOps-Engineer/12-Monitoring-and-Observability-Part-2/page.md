# Monitoring and Observability Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-MLOps-Engineer/Monitoring-and-Observability-Part-2/page

Guide to monitoring and observability for ML systems using AWS CloudWatch and SageMaker Model Monitor to detect infrastructure issues, model drift, bias, feature attribution changes, and enable automated remediation.

In this lesson we cover monitoring and observability for ML systems. Observability goes beyond collecting raw metrics and logs — it helps you determine whether your system and model are behaving normally and meeting business and technical expectations.

We focus on two complementary approaches:

* CloudWatch for infrastructure and service-level metrics and logs.
* SageMaker Model Monitor for model-centric monitoring: data quality, drift, bias, and feature-attribution changes.

Both are important to detect issues such as model drift, increased inference latency, and degraded accuracy. Below we outline concepts, concrete examples, and recommended workflows.

> **lightbulb** This article shows AWS-native approaches (CloudWatch + SageMaker Model Monitor) and how they complement each other. You can integrate CloudWatch metrics into third-party tools (Datadog, Sumo Logic) or trigger remediation (Lambda, CI/CD) from alarms.

## Two perspectives for monitoring

When deciding whether a deployed model is working well, separate monitoring into two perspectives:

1. Infrastructure health
   * Monitors compute resources where models run (managed endpoints). Undersized instances cause high latency and low throughput.
   * Track CPU/GPU/disk usage, memory, networking, and request latency.

2. Model health
   * Monitors prediction quality and data distribution changes that affect model behavior.
   * Verify production inputs are statistically similar to training/validation inputs, detect bias across subgroups, and monitor feature-attribution changes.

Quick comparison: CloudWatch vs SageMaker Model Monitor

|              Capability | Best for                                  | Example signals                                                                      |
| ----------------------: | ----------------------------------------- | ------------------------------------------------------------------------------------ |
|              CloudWatch | Infrastructure & service-level monitoring | CPU/GPU utilization, memory, invocation counts, 4xx/5xx errors, latency              |
| SageMaker Model Monitor | Model-centric monitoring                  | Data quality, input distribution drift, label drift, bias, feature-attribution drift |

## SageMaker Model Monitor — baseline example

A typical first step is to create a baseline from training or holdout data. The baseline produces statistics.json and constraints.json that Model Monitor uses to detect drift and data-quality issues.

Example: suggest a baseline using DefaultModelMonitor

```python theme={null}
from sagemaker import get_execution_role
from sagemaker.model_monitor import DefaultModelMonitor

role = get_execution_role()
baseline_job = DefaultModelMonitor(role=role, instance_count=1, instance_type="ml.m5.xlarge")

baseline_results_s3_uri = "s3://your-bucket/baseline-results/"
baseline_data_s3_uri = "s3://your-bucket/baseline-data/inference_data.csv"

baseline_job.suggest_baseline(
    baseline_dataset=baseline_data_s3_uri,
    dataset_format={"csv": {"header": False}},  # Adjust format to match your CSV/JSON layout
    output_s3_uri=baseline_results_s3_uri,
    wait=True
)

print("Baseline job completed. Results stored in:", baseline_results_s3_uri)
```

The job writes baseline outputs to S3 (statistics.json and constraints.json). Use these as the reference for scheduled monitoring jobs.

## CloudWatch: metrics and logs

CloudWatch collects metrics and logs from AWS services (Lambda, SageMaker, S3, etc.). SageMaker components (training, processing jobs, endpoints) emit both metrics and service logs to CloudWatch.

Key CloudWatch metrics for SageMaker endpoints

| Metric                               | Use case                              |
| ------------------------------------ | ------------------------------------- |
| CPUUtilization / GPUUtilization      | Detect underprovisioned instances     |
| MemoryUtilization                    | Identify memory pressure or OOM risks |
| InvocationCount                      | Throughput tracking                   |
| 4XXErrors / 5XXErrors                | Client vs server-side failures        |
| ModelLatency / p50, p90, p99 latency | SLA and tail-latency monitoring       |

### Enabling data capture on a SageMaker endpoint

Data capture is configured as part of the EndpointConfig. To enable capture for an existing endpoint, create a new EndpointConfig with DataCaptureConfig and update the endpoint to the new config.

```python theme={null}
import boto3

sm_client = boto3.client("sagemaker")

endpoint_name = "your-endpoint-name"
data_capture_s3_uri = "s3://your-bucket/data-capture/"

new_endpoint_config_name = endpoint_name + "-config-with-capture"

sm_client.create_endpoint_config(
    EndpointConfigName=new_endpoint_config_name,
    ProductionVariants=[
        {
            "VariantName": "AllTraffic",
            "ModelName": "your-model-name",
            "InitialInstanceCount": 1,
            "InstanceType": "ml.m5.xlarge",
            "InitialVariantWeight": 1
        }
    ],
    DataCaptureConfig={
        "EnableCapture": True,
        "DestinationS3Uri": data_capture_s3_uri,
        "CaptureOptions": [{"CaptureMode": "Input"}, {"CaptureMode": "Output"}],
        "CaptureContentTypeHeader": {
            "CsvContentTypes": ["text/csv"],
            "JsonContentTypes": ["application/json"]
        }
    }
)

sm_client.update_endpoint(
    EndpointName=endpoint_name,
    EndpointConfigName=new_endpoint_config_name
)

print("Data capture enabled on endpoint:", endpoint_name)
```

> **warning** CloudWatch costs can grow significantly at enterprise scale (many models, many high-resolution metrics and logs, frequent data capture). Plan retention, metric resolution, sampling, and S3 lifecycle policies to control costs.

### CloudWatch console: metrics and dashboards

In the CloudWatch console browse All Metrics by namespace and service. For endpoints, monitor CPU/GPU/memory, invocations, error counts, and latency. Use dashboards to aggregate signals across endpoints and to correlate model health with infrastructure metrics.

When troubleshooting, distinguish:

* 4xx spikes -> malformed requests or client-side issues.
* 5xx spikes -> server-side failures or model runtime errors.

CloudWatch metrics can be exported to third-party monitoring tools (Datadog, Sumo Logic) or used to trigger alarms and automated remediation.

### CloudWatch logs

Service logs are organized into log groups. For SageMaker endpoints, search log groups for "endpoint" and inspect log streams. Filter for ERROR, exception, or failed to find root-cause messages. Logs often contain structured payloads (timestamp, message, inferenceId) useful for matching predictions to ground truth later.

Example of captured ground-truth records (attach to inference records for evaluation):

```json theme={null}
{"inferenceId": "abc123", "actualLabel": 1}
{"inferenceId": "def456", "actualLabel": 0}
{"inferenceId": "ghi789", "actualLabel": 1}
```

### Alarms and automated remediation

CloudWatch Alarms allow threshold-based detection and can invoke actions:

* SNS notifications (email/SMS) to alert teams.
* Invoke Lambda for automated remediation (scale-up, restart endpoint, toggle traffic).
* Trigger CI/CD pipelines to redeploy or roll back models.

Examples:

* Alert when p95 latency > 5s → notify MLOps team.
* If 5xx errors persist, run an automated workflow to scale the endpoint or redeploy a previous model version.
* When Model Monitor constraints fail, trigger a retraining pipeline.

Linking detection to remediation reduces mean time to repair.

## SageMaker Model Monitor (model-focused)

SageMaker Model Monitor detects model-data issues: data quality problems, distribution drift, bias, and changes in feature attribution. Typical workflow:

1. Create a baseline (statistics.json, constraints.json, optional attribution baselines).
2. Enable data capture on the endpoint to collect payloads.
3. Schedule monitoring jobs (hourly/daily) to compute runtime statistics and compare against baseline.
4. Trigger alerts or remediation when drift/bias is detected.

Example: create a monitoring schedule for data quality

```python theme={null}
from sagemaker.model_monitor import ModelMonitor

monitoring_schedule_name = "data-quality-monitoring-job"

monitor = ModelMonitor(
    role=role,
    image_uri=baseline_job.image_uri,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    volume_size_in_gb=20,
    max_runtime_in_seconds=3600,
)

monitor.create_monitoring_schedule(
    monitor_schedule_name=monitoring_schedule_name,
    endpoint_input=endpoint_name,
    output_s3_uri="s3://your-bucket/monitoring-results/",
    statistics_s3_uri=f"{baseline_results_s3_uri}statistics.json",
    constraints_s3_uri=f"{baseline_results_s3_uri}constraints.json",
    schedule_cron_expression="cron(0 * * * ? *)"  # Runs every hour
)
print("Monitoring schedule created:", monitoring_schedule_name)
```

## Feature attribution drift — concept and workflow

Feature attribution drift tracks whether feature importances (which features drive predictions) change over time. Changes in feature importance often indicate shifts in the relationship between inputs and the target and may require retraining or feature engineering.

Example scenario: a housing-price model initially uses Square Footage as the top driver and Location as a minor contributor. After a market shift, Location becomes the dominant factor — a clear attribution drift signal.

<Frame>
  <img alt="A slide titled &#x22;Workflow: Feature Attribution Drift Monitor&#x22; showing two tables of house data (House, Square Footage, Bedrooms, Location, Predicted Price) for initial model predictions and after a market shift. Initially Square Footage is highlighted as the highest-attribution feature and Location the lowest, but after the shift Location becomes the new highest attribution." />
</Frame>

When attribution drift is detected, the monitor will indicate which features changed and by how much, and suggest actions such as investigating the data shift, retraining the model, or revisiting feature selection and preprocessing.

<Frame>
  <img alt="A slide titled &#x22;Workflow: Feature Attribution Drift Monitor&#x22; showing a report that flags Square Footage attribution down 16.67% and Location attribution up 66.67% with a prominent &#x22;Drift Detected!&#x22; alert. To the right are recommended steps: Investigate data shift, Retrain the model with updated data, and Enhance feature selection." />
</Frame>

A baseline attribution job computes attribution statistics from training or holdout data and stores outputs (statistics.json, constraints.json, attribution\_data.csv, model\_metadata.json) in S3.

<Frame>
  <img alt="A diagram titled &#x22;Workflow: Feature Attribution Drift Monitor&#x22; showing training data fed into a &#x22;Model Monitor — Attribution Drift Baseline Job.&#x22; The monitor writes output files (statistics.json, constraints.json, attribution_data.csv, model_metadata.json) to a storage bucket." />
</Frame>

### Creating a feature-attribution baseline (processing job)

Example: compute feature attributions and store baseline in S3

```python theme={null}
from sagemaker.model_monitor import FeatureAttributionMonitor
from sagemaker import get_execution_role

role = get_execution_role()

feature_attribution_monitor = FeatureAttributionMonitor(role=role)

baseline_input = "s3://path-to-baseline-inference-data/"
output_s3_uri = "s3://path-to-store-baseline-output/"

feature_attribution_monitor.create_processing_job(
    baseline_input=baseline_input,
    output_s3_uri=output_s3_uri,
    baseline_name="feature-attribution-baseline"
)
```

After creating the baseline, schedule a monitoring job to compare runtime attributions against the baseline:

```python theme={null}
from sagemaker.model_monitor import FeatureAttributionMonitor
from sagemaker import get_execution_role

role = get_execution_role()

feature_attribution_monitor = FeatureAttributionMonitor(role=role)

feature_attribution_monitor.create_monitoring_schedule(
    monitoring_schedule_name="feature-attribution-drift-monitoring-schedule",
    endpoint_input="s3://path-to-captured-inference-data/",
    baseline_input="s3://path-to-baseline-data/",
    output_s3_uri="s3://path-to-monitoring-results/",
    schedule_cron_expression="cron(0 12 * * ? *)"  # Runs daily at 12 PM
)
```

## Bias monitoring example

Detect differences in model performance across sensitive subgroups by scheduling bias monitoring. Provide captured inference data, ground truth labels, and baseline expectations.

```python theme={null}
from sagemaker.model_monitor import BiasMonitor
from sagemaker import get_execution_role

role = get_execution_role()

bias_monitor = BiasMonitor(role=role)

bias_monitor.create_monitoring_schedule(
    monitoring_schedule_name="bias-monitoring-schedule",
    endpoint_input="s3://path-to-captured-inference-data/",
    ground_truth_input="s3://path-to-ground-truth-data/",
    baseline_input="s3://path-to-baseline-data/",
    sensitive_features=['gender', 'age'],
    output_s3_uri="s3://path-to-monitoring-results/",
    schedule_cron_expression="cron(30 * * * ? *)"  # Run every 30 minutes
)
```

This schedule periodically evaluates predictions against ground truth for specified sensitive features and writes the results to S3 for review and alerting.

## Closing notes and best practices

* Use CloudWatch for infrastructure and service-level health: CPU/GPU/memory, invocation counts, latency, logs, dashboards, and alarms.
* Use SageMaker Model Monitor for model-specific signals: data quality, input distribution drift, label/ground-truth drift, bias, and feature-attribution changes.
* Combine signals from CloudWatch and Model Monitor to trigger alerts and automated remediation: notify teams, retrain models, or redeploy as needed.
* Optimize costs: manage CloudWatch resolution and retention, use S3 lifecycle policies, and sample or aggregate high-frequency telemetry.
* Maintain a clear runbook: define thresholds, alert routing, and remediation steps for each detected condition to reduce mean time to repair.

Further reading:

* [Amazon CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/)
* [SageMaker Model Monitor Documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html)
* [AWS Lambda Documentation (automation hooks)](https://aws.amazon.com/lambda/)
* [Amazon SNS Documentation (notifications)](https://aws.amazon.com/sns/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/772ec99e-54ee-4f4f-8b2a-08b5bc4d4a32/lesson/d16e843b-ac03-441a-b6e1-7995716e6ad0)
