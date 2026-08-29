# python
from sagemaker import Session
from sagemaker.session import TrainingInput
from sagemaker.estimator import Estimator
from sagemaker import image_uris

# Set up session and names
session = Session()
role = "arn:aws:iam::123456789012:role/SageMakerExecutionRole"  # replace with your role ARN
bucket = "my-sagemaker-bucket"  # replace with your S3 bucket
region = session.boto_region_name

# Choose a built-in algorithm image (example: linear-learner)
training_image = image_uris.retrieve("linear-learner", region)

# S3 locations
input_s3_uri = f"s3://{bucket}/data/processed.csv"
output_s3_uri = f"s3://{bucket}/models/"

# Define the Estimator
estimator = Estimator(
    image_uri=training_image,
    role=role,
    instance_count=1,
    instance_type="ml.c5.12xlarge",
    volume_size=50,  # GB
    output_path=output_s3_uri,
    sagemaker_session=session,
    hyperparameters={
        "feature_dim": "10",
        "predictor_type": "regressor",
        "mini_batch_size": "100"
    },
)

# Specify training data (as a single file or channel)
train_input = TrainingInput(s3_data=input_s3_uri, content_type="text/csv")

# Start training (creates a managed SageMaker training job)
estimator.fit({"train": train_input})
```

Tips:

* For framework containers (TensorFlow, PyTorch), you typically provide a training script and use a Framework estimator.
* Increase instance\_count and use framework-specific distributed configurations for multi-node training.

## Monitoring progress and viewing logs

The SDK integrates with CloudWatch and can stream logs into your notebook session.

* estimator.fit() prints logs to the notebook while the job runs (if invoked interactively).
* You can describe a training job via the SageMaker API to poll status.

```python theme={null}
# python
import boto3
sm = boto3.client("sagemaker", region_name=region)

job_name = estimator.latest_training_job.name
resp = sm.describe_training_job(TrainingJobName=job_name)
status = resp["TrainingJobStatus"]  # InProgress, Completed, Failed, Stopped
print(f"Training job '{job_name}' status: {status}")
```

* Stream logs programmatically or from the notebook:

```python theme={null}
# python
estimator.logs(wait=True)  # streams logs until completion
```

Operational notes:

* Prepare and validate input data in S3 before launching training (for example: processed.csv created by your preprocessing pipeline).
* Model artifacts are written back to S3 (e.g., model.tgz or model.tar.gz). Use the artifact to create a SageMaker model for real-time endpoints or to run Batch Transform jobs for offline inference.
* Use checkpointing and resume strategies for long-running jobs, especially when leveraging Spot instances.
* Enable distributed training by increasing instance\_count and configuring distributed strategies for your chosen framework.

> **warning** Spot instances can provide large cost savings but are interruptible. If you use spot instances for training, ensure your training code or framework supports checkpointing and automatic resumption, or be prepared to retry interrupted jobs.

## Quick decision guide

| Question                                    | SageMaker feature to use                                                     |
| ------------------------------------------- | ---------------------------------------------------------------------------- |
| Need repeatable, auditable training?        | Managed training jobs + S3 artifacts + Job metadata                          |
| Running many experiments?                   | Hyperparameter tuning jobs and multiple training jobs with consistent inputs |
| Need large compute or distributed training? | Choose larger instance types or increase instance\_count                     |
| Want to reduce costs?                       | Use Spot instances and tune job duration/checkpoints                         |
| Need to monitor models in production?       | Use SageMaker Model Monitor and CloudWatch metrics                           |

## Summary

* Use SageMaker training jobs to offload and scale training, reduce data movement, and manage compute costs.
* Define training jobs from a notebook using the SageMaker SDK; the heavy compute runs on separate managed instances.
* Monitor training via SDK methods, CloudWatch, or the SageMaker console and stream logs into notebooks for debugging.
* Store prepared training data and model artifacts in S3 for reproducible runs, deployment, and model tracking.

## Links and references

* [AWS SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* [SageMaker Python SDK](https://sagemaker.readthedocs.io/)
* [SageMaker Examples on GitHub](https://github.com/aws/amazon-sagemaker-examples)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/36db8fab-85cc-40f0-8594-573631b0425b/lesson/72e15bf2-cd09-44b0-96dd-19f8e005f5ec)


# Advanced Inference Options Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-MLOps-Engineer/Advanced-Inference-Options-Part-2/page

Explains serverless SageMaker inference for cost-efficient intermittent real-time workloads and using SageMaker Feature Store to precompute and serve consistent low-latency features for inference.

Let’s examine another inference scenario: real-time predictions where cost sensitivity is paramount.

With a classic SageMaker real-time endpoint the flow looks like:
data → SageMaker endpoint → instant prediction. This is ideal for steady traffic, but what happens during long idle periods followed by sudden spikes?

SageMaker endpoints run on one or more managed instances that incur charges while running. For unpredictable workloads with long idle times and occasional bursts, continuously running an endpoint can be cost-inefficient.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem 2: Real-Time Inference Cost&#x22; showing a simple flow diagram: Data -> SageMaker Endpoint -> Instant Prediction, and the question &#x22;How do we handle long periods of no inference requests?&#x22;" />
</Frame>

Solution: serverless inference

Serverless inference in SageMaker shifts the responsibility for provisioning and scaling compute to the cloud provider. There are no always-on instance charges — you pay only for the compute time your model actually uses. Instead of choosing instance types and counts, you configure:

* maximum memory per invocation (memory\_size\_in\_mb), and
* maximum concurrency (max\_concurrency).

This model is optimized for intermittent or bursty traffic patterns where avoiding idle-instance cost is more important than achieving the lowest possible latency.

<Frame>
  <img alt="A slide titled &#x22;Solution 2: Serverless Inference&#x22; listing four benefits: cost-efficient (pay only for compute time), scales automatically, ideal for intermittent/bursty workloads, and no need to specify instances (just set max concurrency and memory)." />
</Frame>

When to use — and when not to use — serverless inference

* Use serverless inference for cost-sensitive, unpredictable real-time workloads with modest concurrency needs.
* Avoid serverless for sustained high-throughput real-time inference — dedicated endpoints with provisioned instances (or autoscaling on real-time endpoints) are better for sustained heavy load.
* Avoid serverless when the application requires ultra-low latency (e.g., sub-100 ms) because cold-starts can add noticeable latency.
* For large offline or scheduled processing, Batch Transform is the appropriate, cost-optimized choice.

| Resource Type                    | Best for                                      | Notes                                               |
| -------------------------------- | --------------------------------------------- | --------------------------------------------------- |
| Serverless Inference             | Unpredictable, intermittent real-time traffic | No always-on instances; set memory and concurrency  |
| Real-time Endpoint (provisioned) | Sustained high throughput, low jitter         | You manage instance types and scaling policies      |
| Batch Transform                  | Large offline batch jobs                      | Optimized for throughput, not low-latency real-time |

<Frame>
  <img alt="A presentation slide titled &#x22;Solution 2: Serverless Inference&#x22; showing a &#x22;Constraints to note&#x22; panel with three cards. The cards state it is not suited for high-throughput real-time inference, not for large batch processing, and not for ultra-low latency (<100 ms) workloads." />
</Frame>

> **warning** Serverless inference can be throttled when concurrency is exceeded (clients may receive 429 TooManyRequests). For workloads that require guaranteed sustained throughput or strict low-latency SLAs, provisioned endpoints are usually a better fit.

Quick example: deploying a serverless endpoint

Below is a minimal Python example using the SageMaker SDK. We create a Model, configure a ServerlessInferenceConfig (memory and concurrency), and deploy.

```python theme={null}
import sagemaker
from sagemaker.serverless import ServerlessInferenceConfig
from sagemaker.predictor import Predictor
