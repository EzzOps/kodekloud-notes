# Initialize session and role
session = Session()
role = "arn:aws:iam::123456789012:role/SageMakerExecutionRole"  # replace with your role

# Input baseline CSV and output S3 locations
baseline_input_s3 = "s3://your-bucket/path/to/baseline.csv"
baseline_output_s3 = "s3://your-bucket/path/to/baseline-output/"

# Create a default Model Monitor instance
monitor = DefaultModelMonitor(
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    sagemaker_session=session,
)

# Suggest baseline statistics and optional constraint files
monitor.suggest_baseline(
    baseline_dataset=baseline_input_s3,
    dataset_format=DatasetFormat.csv(header=True),
    output_s3_uri=baseline_output_s3,
)
```

This call writes baseline statistics and constraints to the specified `baseline_output_s3` location. Use those artifacts when configuring a Monitor Schedule so Model Monitor compares incoming data against this baseline.

## Monitoring schedules and viewing results

Once a monitor runs (scheduled or continuous for streaming), failed checks and drift summaries are visible in the SageMaker console and Model Monitor dashboard. Open your model’s Monitor Schedule to inspect results and any failed checks. The dashboard also surfaces endpoint health and monitoring schedule status.

<Frame>
  <img alt="The image shows an Amazon SageMaker dashboard for a model named &#x22;xgboost-classification-102920.&#x22; It includes details such as endpoints, where one endpoint has a failed status, and options for monitoring schedules." />
</Frame>

## Practical tips and best practices

* Use a baseline derived from final, post-processed training data or a stable production sample.
* Choose monitoring frequency based on traffic and tolerance for drift: hourly, daily, or custom cron.
* Tune thresholds for each check to balance sensitivity and false positives.
* Store monitor outputs in S3 and configure CloudWatch alarms for important violations.
* Mask, hash, or avoid storing PII. Use aggregation or synthetic data when possible.

> **warning** Be careful with sensitive data. If monitoring real user data, ensure compliance with privacy regulations (PII handling, encryption at rest/in transit, least privilege IAM) and consider anonymizing or aggregating fields before storing or analyzing them.

## Where to go from here

* Inspect baseline constraint files and refine checks to fit your production tolerance.
* Automate alarms and remediation: trigger retraining, disable automated decisions, or notify data engineers.
* Combine data drift signals with model performance metrics (ground-truth labels) for end-to-end quality monitoring.

## Links and references

* [Amazon SageMaker Model Monitor documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html)
* [SageMaker Model Monitor Python SDK (readthedocs)](https://sagemaker.readthedocs.io/en/stable/amazon_sagemaker_model_monitor.html)
* [Amazon S3 documentation](https://docs.aws.amazon.com/s3/index.html)
* [Amazon CloudWatch documentation](https://docs.aws.amazon.com/cloudwatch/)
* [Kubernetes and monitoring best practices — general reference](https://kubernetes.io/docs/concepts/)

By configuring a reliable baseline and a monitoring schedule, SageMaker Model Monitor will report where incoming requests deviate from expected distributions so you can investigate, retrain, or gate predictions to maintain model quality.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/e07ceb86-4976-4c8e-a6f8-3518534ec115/lesson/59f5487a-8b3f-4e3a-86ce-8644792fdbe1)


# Demo Setting up AB Testing with SageMaker

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Solution-Monitoring-Maintenance-and-Security/Demo-Setting-up-AB-Testing-with-SageMaker/page

Guide to deploying a second XGBoost model in SageMaker, configuring endpoint variants for A/B and shadow testing, enabling data capture, and using Model Monitor for evaluation and drift detection

In this demo we’ll add a second variant of an existing XGBoost model and configure a SageMaker endpoint to perform A/B testing (traffic splitting) and/or shadow testing. This walkthrough shows how to deploy a second model variant using SageMaker JumpStart, create or update an endpoint configuration, enable data capture, and use Model Monitor to analyze captured data.

1. Deploy a second model variant with SageMaker JumpStart

* Open SageMaker JumpStart and choose the XGBoost classification solution.
* Deploy a new model, selecting an appropriate instance type such as `ml.m5.2xlarge`.
* Complete the deployment process and wait for the model to be created.

<Frame>
  <img alt="The image shows a screenshot of AWS SageMaker Studio's deployment interface, specifically the &#x22;Deploy model to endpoint&#x22; section where an instance type is being selected." />
</Frame>

2. Confirm models in the SageMaker console

* Navigate to SageMaker Console → Dashboard → Models to see all model artifacts.
* You should see the newly created model alongside your previously deployed model(s).

<Frame>
  <img alt="The image shows the Amazon SageMaker console with a list of machine learning models, including xgboost-classification and xgboost-regression, along with their creation times." />
</Frame>

3. Create or update an endpoint configuration

* Select the model you want to expose and click Create endpoint.
* If you don’t have an existing endpoint configuration, create a new one with a descriptive name.
* Choose a provisioned endpoint (recommended for real-time inference).
* Configure encryption and data capture as needed. Enabling data capture here will automatically record request/response payloads for Model Monitor to consume later.

When configuring endpoint variants you’ll see entries labeled Production (often shown as “P”) and Shadow (often shown as “S”). Production variants serve live traffic and return responses to clients. Shadow variants receive mirrored requests for testing; their responses are not returned to the caller.

<Frame>
  <img alt="The image displays an Amazon SageMaker console screen showing the configuration of an endpoint, with a model named &#x22;xgboost-classification-102920&#x22; under the Production variant." />
</Frame>

Summary of variant types and when to use them:

| Variant Type | Behavior                                                                     | When to use                                                                    |
| ------------ | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Production   | Serves live inference traffic and returns responses to callers.              | Use for models you want to include in an A/B test or full production roll-out. |
| Shadow       | Receives a mirrored copy of requests; responses are not returned to callers. | Use for offline evaluation of candidate models without impacting users.        |

4. Configure traffic splitting (A/B testing)

* Add both models as production variants in the endpoint configuration and assign traffic weights.
* Example for a 50/50 split:

```text theme={null}
Variant A weight: 50
Variant B weight: 50
```

* Alternatively, add one model as a production variant and the other as a shadow variant if you only want to mirror traffic for testing.

Data capture is set on the endpoint configuration (you choose sampling percentage and S3 destination). Model Monitor uses the captured requests/responses for drift detection, distribution checks, and other analyses.

<Frame>
  <img alt="The image shows an Amazon SageMaker console dashboard displaying the details of an XGBoost classification model, including endpoints and a monitor schedule section." />
</Frame>

5. Configure data capture (sampling and destination)

* When creating the endpoint configuration, enable data capture and set the sampling percentage to control what fraction of requests/responses are stored.
* Captured data is what Model Monitor consumes to detect data drift, feature distribution changes, and other issues.

<Frame>
  <img alt="The image shows an Amazon SageMaker interface for setting up a data capture configuration. It includes options for entering an endpoint configuration name, selecting data capture for prediction requests/responses, and setting a sampling percentage." />
</Frame>

6. Evaluate and iterate using captured data and Model Monitor

* Compare latency, input/output distributions, error rates, and other telemetry between variants using the captured data.
* To compare accuracy (or other label-dependent metrics), you need ground-truth labels — for example, delayed feedback or a labeled validation dataset.
* Use Model Monitor to generate reports and schedules that continuously evaluate production data and trigger alerts when anomalies or drift are detected.
* Based on these analyses, decide to promote a candidate variant to full production or iterate on the model.

> **lightbulb** Use production variants with traffic weights for controlled live A/B tests and shadow variants to mirror traffic for safe offline evaluation. Always enable data capture if you plan to use Model Monitor — captured payloads are the foundation for drift detection, distribution comparisons, and model promotion decisions.

Links and references

* Amazon SageMaker: [https://aws.amazon.com/sagemaker/](https://aws.amazon.com/sagemaker/)
* SageMaker Model Monitor: [https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html)
* SageMaker JumpStart: [https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart.html](https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/e07ceb86-4976-4c8e-a6f8-3518534ec115/lesson/57bd43a5-2ac8-4938-8eb5-b0e657499fcb)
