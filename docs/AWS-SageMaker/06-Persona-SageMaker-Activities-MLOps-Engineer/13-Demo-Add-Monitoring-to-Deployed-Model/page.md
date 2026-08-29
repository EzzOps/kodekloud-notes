# Processing Step: Data Preprocessing
sklearn_processor = SKLearnProcessor(
    framework_version="1.0-1",
    role=role,
    instance_type="ml.m5.xlarge",
    instance_count=1,
    sagemaker_session=pipeline_session,
)

processing_step = ProcessingStep(
    name="DataPreprocessing",
    processor=sklearn_processor,
    inputs=[],     # e.g., ProcessingInput(source=input_data, destination="/opt/ml/processing/input")
    outputs=[],    # e.g., ProcessingOutput(source="/opt/ml/processing/output", destination=f"s3://{bucket}/processed")
    code="preprocessing.py",
)

# Training Step: Model Training
xgb_estimator = Estimator(
    image_uri=sagemaker.image_uris.retrieve(
        framework="xgboost",
        region=boto3.Session().region_name,
        version="1.5-1",
    ),
    role=role,
    instance_count=train_instance_count,
    instance_type=train_instance_type,
    output_path=f"s3://{bucket}/output",
    sagemaker_session=pipeline_session,
)

training_step = TrainingStep(
    name="ModelTraining",
    estimator=xgb_estimator,
    inputs={"train": TrainingInput(input_data, content_type="text/csv")},
)

# Model Evaluation Step (Processing job running evaluation.py)
evaluation_processor = ScriptProcessor(
    image_uri="763104351884.dkr.ecr.us-west-2.amazonaws.com/sklearn-processing:1.0-1",
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    command=["python3"],
    sagemaker_session=pipeline_session,
)

evaluation_step = ProcessingStep(
    name="ModelEvaluation",
    processor=evaluation_processor,
    inputs=[],   # e.g., use training_step.outputs for model artifacts
    outputs=[],
    code="evaluation.py",
)

# Register Model Step
register_model_step = RegisterModel(
    name="RegisterModel",
    estimator=xgb_estimator,
    model_data=training_step.properties.ModelArtifacts.S3ModelArtifacts,
    content_types=["text/csv"],
    response_types=["text/csv"],
)

# Create Pipeline (order defines execution sequence)
pipeline = Pipeline(
    name="MySageMakerPipeline",
    parameters=[input_data, train_instance_type, train_instance_count],
    steps=[processing_step, training_step, evaluation_step, register_model_step],
)

# Create or update and start execution
pipeline.upsert(role_arn=role)
execution = pipeline.start()
print(execution.describe())
```

Key notes:

* Define steps first; the pipeline's step list dictates execution order.
* pipeline.upsert(...) creates or updates the pipeline resource in SageMaker.
* pipeline.start() launches an execution; use execution.describe() to inspect status.
* Parameterize S3 paths, instance types, and instance counts for flexible reuse.

<Frame>
  <img alt="A slide titled &#x22;Workflow: SageMaker Pipelines Using SDK&#x22; showing a four-step pipeline: Processing Step, Train Step, Evaluation Step, and Register Step. Each step maps downward to its corresponding job: Processing Job, Training Job, Processing Job, and Register to Model Registry." />
</Frame>

***

## Triggers: how pipeline executions start

You can start a pipeline directly with pipeline.start(), but production pipelines are usually triggered by external systems:

| Trigger Type                                          | Use Case / Notes                                                |
| ----------------------------------------------------- | --------------------------------------------------------------- |
| Managed Workflows for Apache Airflow (MWAA) / Airflow | Orchestrate complex DAGs across environments                    |
| AWS Step Functions                                    | Serverless orchestration and long-running workflows             |
| AWS Lambda                                            | Event-driven triggers (e.g., S3 object creation)                |
| CI/CD systems (Jenkins, CodePipeline, GitHub Actions) | Commit/push → CI checks → start SageMaker pipeline              |
| MLOps platforms (MLflow, Kubeflow)                    | Integrate pipeline runs with model tracking and lifecycle tools |

References:

* [MWAA Overview](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html)
* [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
* [AWS Lambda](https://learn.kodekloud.com/user/courses/aws-lambda)

<Frame>
  <img alt="A slide titled &#x22;Triggering Pipelines From Other Services&#x22; that shows services like Managed Workflows for Apache Airflow (MWAA), AWS Step Functions, AWS Lambda, CI/CD tools, and MLOps platforms triggering a pipeline. The pipeline (shown as a right-pointing arrow) lists steps: Clean Data, Feature Engineer, Train, Register, and Deploy." />
</Frame>

***

## Summary

* SageMaker Pipelines orchestrates ML workflows and moves teams from manual notebook-driven experimentation to automated, reproducible pipelines.
* You can author pipelines via the Studio Visual Editor (low-code) or, preferably, via the SageMaker Python SDK for full control and version-in-code.
* Common steps include processing, training, evaluation, model registration, and deployment.
* Pipelines are typically triggered by external orchestrators (CI/CD, Step Functions, Airflow, MLOps platforms).
* The objective is repeatability: given the same inputs, pipelines produce consistent outputs and provide traceable lineage.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; with five numbered items describing SageMaker Pipelines. The points cover orchestration of ML workflows, pipeline definitions via UI/SDK stored as JSON, flexible/customizable steps, invocation sources (CI/CD, git, ML platforms), and repeatability for retraining." />
</Frame>

***

## Next steps

Continue learning by exploring how to bootstrap new ML projects with predefined SageMaker pipelines that provide a reproducible starting point for experimentation and productionization. Consider creating a Git-backed project template that includes:

* Standardized scripts (clean.py, feature.py, train.py, evaluation.py, register.py)
* CI/CD pipeline definitions to validate and trigger SageMaker pipelines
* Terraform or CloudFormation templates for infrastructure reproducibility

For further reading and tutorials, refer to the official SageMaker documentation and AWS orchestration guides.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/772ec99e-54ee-4f4f-8b2a-08b5bc4d4a32/lesson/7adfb801-a099-4367-acd9-b6401c2de6a2)


# Demo Add Monitoring to Deployed Model

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-MLOps-Engineer/Demo-Add-Monitoring-to-Deployed-Model/page

Demonstrates adding SageMaker Model Monitor data quality monitoring to a deployed endpoint by creating a baseline, enabling data capture, scheduling monitoring, generating inference traffic, and inspecting results.

This hands-on demonstration shows how to add data-quality monitoring to a deployed SageMaker model using SageMaker Model Monitor. You'll create a baseline job that computes statistics and suggested constraints for a baseline dataset, enable data capture on an endpoint, schedule a monitoring job that compares captured inference data to the baseline, generate inference traffic to populate capture, and inspect results.

Goals:

* Create a baseline for data quality using Model Monitor.
* Deploy an endpoint with data capture enabled (sample inference requests/responses).
* Schedule a monitoring job that compares captured data with the baseline.
* Generate inference traffic to exercise data capture.
* Inspect results and clean up resources when finished.

This demo is designed to run inside a SageMaker Studio Jupyter notebook.

<Frame>
  <img alt="A screenshot of an Amazon SageMaker JupyterLab interface showing a file browser on the left and a launcher on the right with Notebook, Console, and Other options. A cursor hovers over a notebook file named &#x22;house_price_model_monitor_demo_with_capture.ipynb&#x22; in the file pane." />
</Frame>

> **lightbulb** Prerequisites: run this notebook inside SageMaker Studio or an environment with the SageMaker Python SDK, boto3, and pandas installed. Ensure the executing IAM role has permissions for SageMaker, S3, and IAM (to create model/endpoint and read/write S3).

## Overview of steps

1. Setup imports, session, and S3 locations.
2. Upload model artifact and prepare baseline data.
3. Create an endpoint with Data Capture enabled.
4. Create a DefaultModelMonitor and run a baseline job.
5. Create a monitoring schedule.
6. Generate inference traffic to produce captured data.
7. Inspect captured data in S3.
8. Clean up resources.

***

## 1) Setup: imports, session, S3 locations

Start by importing required SDKs and creating session/role variables. These values are used throughout the demo to manage S3 locations, create models/endpoints, and schedule monitoring.

```python theme={null}
