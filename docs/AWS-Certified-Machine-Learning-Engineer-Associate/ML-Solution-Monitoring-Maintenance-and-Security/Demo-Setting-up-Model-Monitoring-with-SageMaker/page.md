# Demo Setting up Model Monitoring with SageMaker

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Solution-Monitoring-Maintenance-and-Security/Demo-Setting-up-Model-Monitoring-with-SageMaker/page

Guide to enabling and configuring Amazon SageMaker Model Monitor for real-time endpoints, including deployment, data capture to S3, baseline setup, scheduling monitoring jobs, and viewing results.

Welcome — this walkthrough shows how to enable Amazon SageMaker Model Monitor for a deployed real-time endpoint. You'll learn how to deploy a small model from JumpStart, enable data capture to S3, configure monitoring types and baselines, schedule monitoring jobs, and inspect results.

First, open SageMaker Studio.

<Frame>
  <img alt="The image shows the Amazon SageMaker Studio interface, highlighting it as a fully integrated development environment for machine learning, with options to open the studio and view what's new." />
</Frame>

1. Choose a JumpStart model to deploy

* In SageMaker Studio, open JumpStart and pick a small, easy-to-deploy model (good candidates: XGBoost classification/regression, small scikit-learn models).
* For this demo we deploy an XGBoost classification model.

<Frame>
  <img alt="The image shows the AWS SageMaker Studio interface, specifically the &#x22;Models&#x22; section, where various machine learning models are displayed. There is a search bar and options to filter models by different criteria like input modality, publisher, and use case." />
</Frame>

Select the XGBoost classification model and click Deploy. Use the console options to review model details and invocation examples.

<Frame>
  <img alt="The image shows a web interface for Amazon SageMaker Studio, displaying the XGBoost Classification model with options for evaluation, deployment, and training, along with a description of the model and usage instructions." />
</Frame>

2. Choose instance type for the endpoint

* Pick an instance class suitable for real-time inference and expected throughput. For CPU‑based, compute‑optimized instances such as `ml.c5.*` are common.
* In this demo we used `ml.c5.2xlarge` (8 vCPUs, 16 GiB memory). Check cost estimates on the SageMaker pricing page: [https://aws.amazon.com/sagemaker/pricing/](https://aws.amazon.com/sagemaker/pricing/).

<Frame>
  <img alt="The image displays a webpage from AWS, specifically the pricing details for Amazon SageMaker AI, showing on-demand pricing for different instance types and their respective costs." />
</Frame>

3. Wait for deployment and review the endpoint summary

* Deployment typically completes quickly. After deployment, review: inference type (real-time), logs, endpoint ARN, and the invocation URL for client requests.

<Frame>
  <img alt="The image shows a screenshot of AWS SageMaker Studio with an endpoint summary for a classification model being created. It includes details like inference type, creation time, and endpoint URL." />
</Frame>

Important notes about the endpoint summary:

* Inference type: real-time inference.
* Endpoint logs can be routed to CloudWatch for tracing and debugging (see [https://learn.kodekloud.com/user/courses/aws-cloudwatch](https://learn.kodekloud.com/user/courses/aws-cloudwatch)).
* Endpoint ARN and invocation URL are available for direct testing.

4. Deployment variants and traffic routing

* You can create multiple variants (for example, `production` and `canary`). Each variant can receive a percentage of traffic.
* In this demo a single production variant receives 100% of traffic.

<Frame>
  <img alt="The image shows an Amazon SageMaker Studio interface, specifically displaying details of a deployed endpoint for a machine learning model, with sections for settings and security details. On the left, there are various applications like JupyterLab and MLflow listed." />
</Frame>

You can also invoke the endpoint directly from the console (sample Python SDK snippets or example JSON are available in the UI) to validate the deployed model before enabling monitoring.

5. Open Model Governance (Model Monitor)

* In SageMaker Studio, open the Model Governance / Model Monitor tab to see deployed endpoints and those in progress.
* Select your endpoint and click Create Monitor to configure Model Monitor for the selected endpoint. This will enable data capture (requests/responses) and create monitoring schedules.

<Frame>
  <img alt="The image shows a configuration screen on the Amazon SageMaker console for creating a monitoring endpoint. It includes fields for endpoint configuration, data capture options, S3 storage location, and sampling percentage settings." />
</Frame>

Model Monitor configuration — key steps and recommended settings

1. Endpoint config name and data capture
   * Enable data capture for both requests and responses so captured records are persisted to S3.
   * Provide an S3 location (URI) for captured records. Use an existing bucket or create a new one in the S3 console.

Example S3 URI format:

```text theme={null}
s3://your-bucket-name/path/to/captured-records/
```

To create or choose an S3 bucket, open the Amazon S3 console and copy the S3 URI of the folder you will use (examples often include folders such as `models`, `predictions`, `raw-data`).

<Frame>
  <img alt="The image shows an AWS S3 bucket named &#x22;machine-learning-demo-ak&#x22; with several folders, including &#x22;models,&#x22; &#x22;predictions,&#x22; &#x22;processed-data,&#x22; &#x22;raw-data,&#x22; and &#x22;training-data,&#x22; in the bucket's interface." />
</Frame>

* Configure the sampling percentage to control how much traffic is captured. Use sampling for A/B tests or multi-variant endpoints (e.g., 20% capture for canary). In this demo we capture 100% because a single variant serves all traffic.

<Frame>
  <img alt="This image shows a setup screen from the AWS SageMaker console, where the user is configuring prediction data collection settings, including S3 storage location and sampling percentage." />
</Frame>

2. Monitoring types and baseline dataset

* Select the monitoring types appropriate for your use case:

| Monitoring type      | Purpose                                       | Notes                                                   |
| -------------------- | --------------------------------------------- | ------------------------------------------------------- |
| Data quality         | Detects data drift and integrity issues       | No ground-truth labels required                         |
| Model quality        | Evaluates prediction performance              | Requires labeled ground-truth (labels must be supplied) |
| Model explainability | Computes feature attributions for predictions | Useful for feature importance and debugging             |
| Model bias           | Monitors fairness and class imbalance         | May require protected-attribute metadata                |

* In this demo we enable Data Quality to detect drift between captured data and your baseline.
* Provide a baseline dataset (usually the training data) to compute baselines and constraints. Example baseline file:

```text theme={null}
s3://your-bucket-name/raw-data/titanic.csv
```

* Provide an S3 output location where baselines and reports will be written (e.g., `s3://your-bucket-name/predictions/`).

For monitoring compute, you can choose a lower-cost instance because monitoring jobs often run periodically rather than continuously. In this walkthrough we selected `ml.c4.xlarge` for the monitoring analysis job.

3. Schedule and job configuration

* Choose how often the monitoring job runs (e.g., hourly, daily). Scheduling is important to aggregate sufficient data (for example, daily after business hours).
* Configure:
  * Schedule expression (cron or rate). Example daily cron:
  ```cron theme={null}
  cron(0 2 * * ? *)
  ```
  * Stopping condition (max runtime).
  * Monitoring job instance type and IAM role (the role must have S3 write access).
* When specifying input/output locations for the job, select the S3 folders for captured input and monitoring outputs.

<Frame>
  <img alt="The image shows the Amazon SageMaker console, specifically the job configuration page for setting up schedule parameters like IAM role, schedule expression, stopping condition, and instance type." />
</Frame>

Use the S3 selector in the console to browse and assign buckets/folders:

<Frame>
  <img alt="The image shows an Amazon SageMaker interface with a dialog for selecting an S3 resource. It lists several S3 buckets with their creation dates." />
</Frame>

Optional: post-analytics / custom processors

* You may provide a post-analytics processor or record processor URI to run custom code on captured records or analytics outputs.
* In this demo we reused the `predictions` folder to store analytics artifacts.

<Frame>
  <img alt="The image shows the Amazon SageMaker console, specifically the &#x22;Additional configuration&#x22; step for creating a model monitor, with fields to enter S3 locations for post analytics and record processor source URIs." />
</Frame>

Summary of configuration steps

* Step 1: Enable data capture for the endpoint (requests and responses to S3).
* Step 2: Select monitoring types and provide a baseline dataset to compute baselines/constraints.
* Step 3: Configure the monitoring job schedule, instance type, input/output S3 locations, and optional post-processing.

After submission, SageMaker creates the monitoring schedule and begins capturing/analyzing data according to your configuration. Raw outputs and reports are written to the S3 output location you specified.

Where to view results

* Raw monitoring artifacts: check the S3 output path you configured.
* Interactive view: open the Model Dashboard in SageMaker Studio to see consolidated visualizations including risk rating, model quality, data quality (drift), bias metrics, and feature attribution drift — an operational view of model health.

<Callout icon="lightbulb">
  Ensure the IAM role used by SageMaker has permissions to read/write the S3 locations you choose (see [https://learn.kodekloud.com/user/courses/aws-iam](https://learn.kodekloud.com/user/courses/aws-iam)). If you use KMS‑encrypted buckets, confirm the KMS key policy grants SageMaker permission to use the key ([https://aws.amazon.com/kms/](https://aws.amazon.com/kms/)).
</Callout>

<Callout icon="lightbulb">
  If you plan to enable Model Quality (prediction performance), you must provide ground-truth labels. Plan how labeled feedback will be collected and where it will be stored so the monitoring job can access it.
</Callout>

That completes the end-to-end flow for enabling SageMaker Model Monitor on a real-time endpoint and where to inspect the resulting metrics and artifacts. For more details, refer to the official SageMaker Model Monitor documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/e07ceb86-4976-4c8e-a6f8-3518534ec115/lesson/e2c85cca-4ef4-4689-840e-c72f644708aa" />
</CardGroup>
