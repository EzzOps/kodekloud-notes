# The SageMaker SDK for Python Why not boto3

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/SageMaker-Introduction/The-SageMaker-SDK-for-Python-Why-not-boto3/page

Explains why the SageMaker Python SDK simplifies ML workflows compared to boto3 by offering higher level abstractions, notebook ergonomics, integrations, and recommends hybrid use for non-ML AWS services

In this lesson we introduce the Amazon SageMaker SDK for Python and explain why you might prefer it over the general-purpose AWS SDK for Python (Boto3). We'll cover which SDKs are available to automate AWS, why Boto3 can become verbose for ML workflows, what the SageMaker SDK provides, how it maps to notebook-driven development, and real-world benefits and customer examples.

Why choose a higher-level ML SDK? In short: productivity, readability, and reproducibility. The SageMaker SDK provides purpose-built abstractions for common ML operations (processing, training, tuning, and deployment) so you write less boilerplate and focus on model development.

Why Boto3 can be suboptimal for ML workflows

Boto3 is a powerful, general-purpose SDK that exposes the complete REST API surface of AWS services: EC2, S3, DynamoDB, SageMaker, and more. It converts Python function calls into REST API requests targeted at service endpoints. That flexibility makes Boto3 ideal for general automation, but for iterative ML development the raw API surface often means verbose, nested request payloads and more boilerplate.

<Frame>
  <img alt="A slide diagram showing that the AWS SDK for Python (boto3) lives inside a Python app and automatically generates REST API calls to AWS services. The right-hand box lists EC2, S3, DynamoDB and SageMaker, illustrating the SDK isn’t optimized for ML workflows." />
</Frame>

Creating a Boto3 client is simple and exposes every API method for the service. This generality is useful, but it means you often need to construct full, nested request payloads for ML operations.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: AWS SDK (Boto3) Not Optimized for ML Workflows&#x22; showing five numbered example tasks. The tasks are: creating an SNS topic; launching an EC2 instance; uploading an object to an S3 bucket; updating an Amazon Connect virtual call center; and downloading satellite data in Ground Station." />
</Frame>

Quick example: upload a file to S3 using Boto3

```python theme={null}
import boto3

s3_client = boto3.client('s3')

bucket_name = 'your-bucket-name'
upload_file_path = 'local_file.txt'     # Local file to upload
upload_key = 'uploaded_file.txt'        # Name to save in S3

s3_client.upload_file(Filename=upload_file_path, Bucket=bucket_name, Key=upload_key)
```

This S3 example is concise and readable. But ML tasks such as starting a SageMaker training job require many nested parameters in the API payload, which increases code verbosity and reduces clarity when experimenting.

Example: creating a SageMaker training job with Boto3 (explicit, nested payload)

```python theme={null}
import boto3

sagemaker = boto3.client("sagemaker")

response = sagemaker.create_training_job(
    TrainingJobName="linear-learner-house-prices",
    AlgorithmSpecification={
        "TrainingImage": "683313688378.dkr.ecr.us-east-1.amazonaws.com/linear-learner:latest",
        "TrainingInputMode": "File"
    },
    RoleArn="arn:aws:iam::123456789012:role/SageMakerExecutionRole",
    InputDataConfig=[{
        "ChannelName": "train",
        "DataSource": {"S3DataSource": {
            "S3DataType": "S3Prefix",
            "S3Uri": "s3://your-bucket/path/to/training-data.csv",
            "S3DataDistributionType": "FullyReplicated"
        }},
        "ContentType": "text/csv"
    }],
    OutputDataConfig={"S3OutputPath": "s3://your-bucket/path/to/output/"},
    ResourceConfig={"InstanceType": "ml.m5.large", "InstanceCount": 1, "VolumeSizeInGB": 10},
    StoppingCondition={"MaxRuntimeInSeconds": 3600},
    HyperParameters={"feature_dim": "10", "mini_batch_size": "32", "predictor_type": "regressor"}
)

print(f"Training job created: {response['TrainingJobArn']}")
```

Because Boto3 reflects the raw service API, it forces you to handle details (nested dictionaries, JSON shapes, and required fields) that are irrelevant to the core ML experiment you’re iterating on.

SageMaker SDK for Python: purpose-built, higher-level abstractions

The SageMaker SDK for Python is a separate, ML-focused library. It still issues REST API calls under the hood, but provides high-level constructs (Estimator, Model, Processor, Pipeline) and sensible defaults that match common data-science activities. This design reduces boilerplate, improves readability in notebooks, and speeds up experimentation.

<Frame>
  <img alt="A diagram titled &#x22;SageMaker SDK – Streamlining ML Workflows&#x22; showing a Python container with two components — &#x22;SageMaker SDK for Python&#x22; and &#x22;AWS SDK for Python (boto3)&#x22; — each pointing to corresponding services: the SageMaker REST API and general AWS services. The slide illustrates how the SDKs connect Python code to AWS/SageMaker APIs." />
</Frame>

Key benefits of the SageMaker SDK:

* High-level constructs that map to ML activities: Estimator, Model, Processor, Pipeline.
* Sensible defaults and helpers so you don’t supply every low-level API field.
* Cleaner, more readable notebook code that’s easier to reproduce and share.
* Built-in helpers for S3 paths, IAM role detection, CloudWatch logging, Feature Store and Model Registry integration.
* Native integration with SageMaker Pipelines for end-to-end automation.

Comparison: Boto3 vs SageMaker SDK

|            Capability |              Boto3              |                SageMaker SDK               |
| --------------------: | :-----------------------------: | :----------------------------------------: |
|          Surface area |        Full AWS REST API        |   SageMaker-centric + select integrations  |
| Verbosity for ML jobs |      High (nested payloads)     |     Low (Estimator/Model abstractions)     |
|    Good for notebooks |              Mixed              |    Excellent (notebook-first ergonomics)   |
|              Use case |         All AWS services        | Training, processing, inference, pipelines |
|       When to combine | Yes (Boto3 for non-ML services) |      Yes (SageMaker SDK for ML tasks)      |

Example: creating and starting a training job using the SageMaker Python SDK

```python theme={null}
import sagemaker
