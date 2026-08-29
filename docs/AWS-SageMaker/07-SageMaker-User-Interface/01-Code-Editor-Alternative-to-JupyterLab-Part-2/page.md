# Create a SageMaker session (handles S3 bucket defaults and boto3 session)
session = sagemaker.Session()
role = "arn:aws:iam::123456789012:role/SageMakerExecutionRole"

estimator = sagemaker.estimator.Estimator(
    image_uri="683313688378.dkr.ecr.us-east-1.amazonaws.com/linear-learner:latest",
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    volume_size=10,
    max_run=3600,
    output_path="s3://your-bucket/path/to/output/",
    sagemaker_session=session
)

# Set hyperparameters via a dedicated method (clear separation of concerns)
estimator.set_hyperparameters(feature_dim=10, mini_batch_size=32, predictor_type="regressor")

# Start training; fit() mirrors scikit-learn's API for familiarity
# By default fit() blocks until completion; pass wait=False to run asynchronously.
estimator.fit({"train": "s3://your-bucket/path/to/training-data.csv"})
```

This approach separates configuration (Estimator construction), hyperparameters (set\_hyperparameters), and inputs (fit). Small changes—like swapping datasets or hyperparameters—become single-line edits in iterative experiments.

SageMaker SDK integrations with AWS services

The SageMaker SDK wraps and integrates with common ML services and patterns to simplify workflows:

<Frame>
  <img alt="A presentation slide titled &#x22;SageMaker SDK – Interacting With AWS Services&#x22; showing three cards for Amazon S3, AWS Identity and Access Management (IAM), and AWS Step Functions with brief descriptions of their purposes (storage, execution role management, and pipeline orchestration)." />
</Frame>

* Amazon S3: dataset storage, model artifact destinations, and checkpointing.
* IAM: execution roles for training, processing, and inference.
* AWS Step Functions: orchestration of multi-step pipelines integrating SageMaker and other services.

<Frame>
  <img alt="A presentation slide titled &#x22;SageMaker SDK – Interacting With AWS Services&#x22; showing three feature cards: SageMaker Feature Store (ingesting, managing, querying features), Amazon CloudWatch (automatic logging and monitoring for jobs and endpoints), and Amazon SageMaker Model Registry (registering, managing, and deploying models). The slide has a dark blue background with each service icon and brief description inside rounded white cards." />
</Frame>

Other integrations include:

* Feature Store: consistent feature ingestion, storage, and retrieval.
* CloudWatch: automatic logging, metrics, and monitoring for jobs and endpoints.
* Model Registry: versioning, approvals, and controlled deployment workflows.

Hybrid approach: use the right SDK for the right task

The SageMaker SDK focuses on SageMaker and a curated set of ML-relevant services. For other AWS needs—messaging (SNS), email (SES), custom databases (DynamoDB), or custom infra—you should continue to use Boto3. In practice, Jupyter notebooks commonly use both: SageMaker SDK for ML operations, and Boto3 for peripheral services.

<Frame>
  <img alt="A presentation slide titled &#x22;SDK Hybrid Approach&#x22; showing three numbered steps about using boto3: sending data to an SNS destination, modifying DynamoDB entries, and enabling access to various AWS services. The slide has a dark background with teal rounded boxes for each step." />
</Frame>

Hybrid example: start training with SageMaker SDK and send an SNS notification via Boto3

```python theme={null}
import boto3
import sagemaker

session = sagemaker.Session()
role = "arn:aws:iam::123456789012:role/SageMakerExecutionRole"

# Construct an Estimator (same pattern as before)
estimator = sagemaker.estimator.Estimator(
    image_uri="683313688378.dkr.ecr.us-east-1.amazonaws.com/linear-learner:latest",
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path="s3://your-bucket/path/to/output/",
    sagemaker_session=session
)

estimator.set_hyperparameters(feature_dim=10, mini_batch_size=32, predictor_type="regressor")

# Start training asynchronously so the notebook can continue
job_name = "linear-learner-house-prices-001"
estimator.fit({"train": "s3://your-bucket/path/to/training-data.csv"}, job_name=job_name, wait=False)

# Use boto3 for notifications or peripheral services
sns = boto3.client("sns", region_name="us-east-1")
sns.publish(
    TopicArn="arn:aws:sns:us-east-1:123456789012:training-job-notifications",
    Message=f"Training job {job_name} started.",
    Subject="SageMaker Training Job Notification"
)
```

This pattern highlights a practical separation: SageMaker SDK handles ML operations and artifacts; Boto3 handles general AWS integrations (notifications, custom DB writes, etc.). Supplying a deterministic training job name helps downstream systems reference the job reliably.

<Callout icon="lightbulb">
  Use the SageMaker SDK for ML-centric operations in notebooks and combine it with Boto3 for services the SDK doesn’t cover. This hybrid approach keeps ML code concise while retaining full access to AWS features.
</Callout>

Security and permissions (important)

Always ensure the IAM role used by SageMaker (and any boto3 clients) has least-privilege permissions for S3, CloudWatch, SNS, and other resources your workflow touches. Misconfigured roles can cause training or deployment failures.

<Callout icon="warning">
  Make sure the SageMaker execution role grants access to S3 paths, logging destinations, and any other AWS resources the job requires. If using boto3 clients in your notebook, confirm your local AWS credentials and region configuration are correct.
</Callout>

Business results and adoption

Adopting the SageMaker SDK typically accelerates model development and simplifies maintenance by shifting focus away from low-level API plumbing to modeling. Organizations report faster time-to-value since data scientists can iterate on experiments rather than service payloads.

<Frame>
  <img alt="A presentation slide titled &#x22;Results: Accelerating ML Development With SageMaker SDK&#x22; showing four numbered benefits: Faster ML development, Easier code maintenance, Shorter time to value, and More efficient management, each with a simple icon." />
</Frame>

Real examples:

* AstraZeneca: used SageMaker and the SDK to spin up ML environments quickly so scientists could focus on modeling rather than infrastructure.
* NatWest Bank: built 30+ ML use cases in four months using SageMaker tooling to accelerate personalized marketing and fraud detection initiatives.

<Frame>
  <img alt="A presentation slide showing the NatWest logo and the heading &#x22;Results: Accelerating ML Development With SageMaker SDK.&#x22; It highlights building 30+ ML use cases in four months and enabling personalized marketing and fraud detection." />
</Frame>

Summary

* Two primary Python SDK choices:
  * Boto3: general-purpose AWS SDK exposing the full REST API surface.
  * SageMaker SDK: ML-focused, higher-level abstractions optimized for training, processing, inference, pipelines, and common ML integrations.
* Use the SageMaker SDK for ML tasks in notebooks to reduce boilerplate and improve reproducibility.
* Use Boto3 for services the SageMaker SDK does not cover (SNS, DynamoDB, SES, custom infra).
* Combine both in practice: SageMaker SDK for ML, Boto3 for peripheral AWS operations.

Further reading and references

* SageMaker SDK docs: [https://sagemaker.readthedocs.io/](https://sagemaker.readthedocs.io/)
* Boto3 docs: [https://boto3.amazonaws.com/v1/documentation/api/latest/index.html](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
* Amazon SageMaker overview: [https://aws.amazon.com/sagemaker/](https://aws.amazon.com/sagemaker/)

A hands-on, end-to-end training job example using the SageMaker SDK is available in a separate article to walk you through a complete notebook workflow.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/8dba4cbc-6eb7-4985-b97a-c5b7e6d23161/lesson/2d5e6b71-04ea-4f22-b0ac-5494ddd28244" />
</CardGroup>


# Code Editor Alternative to JupyterLab Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/SageMaker-User-Interface/Code-Editor-Alternative-to-JupyterLab-Part-2/page

Comparison of AWS SageMaker managed VS Code and JupyterLab, guiding when to use each, provisioning Code Editor spaces, debugging, refactoring notebooks into production scripts

If your work is focused on general software development—building applications, writing production code, and managing large code bases—the [AWS SageMaker](https://learn.kodekloud.com/user/courses/aws-sagemaker) Code Editor (managed VS Code) is generally a better fit. For exploratory workflows—data analysis, iterative visualization, experiment annotation, and fast prototyping—JupyterLab and Jupyter Notebooks remain the best choice.

<Frame>
  <img alt="A dark presentation slide titled &#x22;Solution: JupyterLab&#x22; showing four labeled boxes: Data analysis, Exploratory data science, Interactive visualization, and Notebook-based development. A small &#x22;© Copyright KodeKloud&#x22; notice appears in the lower-left corner." />
</Frame>

Creating a Code Editor space

To create a Code Editor space in SageMaker Studio, open the Applications panel and find the Code Editor application. Creating a space provisions a managed Amazon EC2 instance and launches an instance of Visual Studio Code inside a container. When provisioning you must provide a name for the space (for example, "My Code Editor Space").

When the Code Editor space is provisioned you can inspect:

* the EC2 instance type (CPU/memory),
* the container image used,
* and the attached storage size.

Once the space state is Running, click Open Code Editor to launch the VS Code environment. The interface behaves like standard Visual Studio Code: a left activity bar for files and extensions, a central editor area with tabs, and full support for debugging and version control.

<Frame>
  <img alt="A screenshot of a code editor provisioning interface titled &#x22;Workflow: Provisioning Code Editor Space.&#x22; It shows a codespace named &#x22;codespace1&#x22; with instance ml.t3.medium, a SageMaker image selection, and space settings (5 GB storage)." />
</Frame>

Key provisioning details

| Setting         | Default                      | Notes                                                                                                      |
| --------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Instance size   | ml.t3.medium                 | Change to larger instance types if you need more CPU or memory for heavy development tasks.                |
| Container image | SageMaker distribution image | Includes common libraries for Python/VS Code. You can select custom images for framework-specific tooling. |
| Storage         | 5 GB (EBS)                   | Can be increased up to 100 GB when provisioning. Use larger volumes for datasets and local artifacts.      |

Debugging and running scripts

One of the primary benefits of the Code Editor is the built-in debugger. You can set breakpoints, step line-by-line, inspect variables, and trace exceptions—capabilities that make debugging production-style scripts far easier than in many notebook environments.

Below is a concise, corrected example script that downloads a CSV from S3, preprocesses the data, and uploads the processed file back to S3. This example includes the required imports, an initialized S3 client, and robust handling for numeric-only median imputation and scaling.

```python theme={null}
