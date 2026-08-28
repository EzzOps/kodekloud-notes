# Demo Deploying a Model for Real time Inference

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Deployment-and-Orchestration-of-ML-Workflows/Demo-Deploying-a-Model-for-Real-time-Inference/page

Guide to deploying and managing AWS SageMaker real time inference endpoints, covering serverless versus provisioned hosting, model variants, encryption, invocation, monitoring, and operational best practices.

Welcome back. In this lesson we’ll walk through hosting a trained model as a real-time inference endpoint in AWS SageMaker. SageMaker streamlines the process — whether you’re deploying a JumpStart model or a model you trained and registered in SageMaker Studio — you can expose it as an endpoint for low-latency, real-time predictions.

Overview — high-level steps

1. Open SageMaker Studio and locate the model you want to deploy (JumpStart or a model you registered).
2. If required, train, register, and verify the model artifact and inference container/image.
3. From the SageMaker AI homepage, go to Deployments and inference → Endpoints.
4. Create a new endpoint: choose a name and select or create an endpoint configuration.
5. Pick hosting mode (serverless or provisioned), configure encryption/KMS if required, and define model variants (production/shadow).
6. Create the endpoint and call it via the InvokeEndpoint API, SDK, or AWS CLI for real-time predictions.

Quick comparison: hosting modes

| Hosting mode | Best for                                  | Key characteristics                                                      |
| ------------ | ----------------------------------------- | ------------------------------------------------------------------------ |
| Serverless   | Low/variable traffic, simpler ops         | No instance management, scales on-demand, lower idle cost                |
| Provisioned  | Consistent high throughput, GPU inference | Choose instance types and counts, predictable performance, supports GPUs |

Step-by-step details

1. Locate and prepare your model in SageMaker Studio

* If you used JumpStart, you can reuse that JumpStart model. If you trained a model in Studio, ensure it’s registered and shows up in the SageMaker model list.
* Verify the model artifact S3 location and the container image (inference specification) are correctly set on the model resource. Confirm that IAM roles used by SageMaker have access to the S3 artifact and ECR (if applicable).

2. Create an endpoint from SageMaker AI → Endpoints

* From the SageMaker AI homepage, open Deployments and inference → Endpoints.
* Click “Create endpoint” and provide a meaningful endpoint name (e.g., `my-model-prod-v1`).

3. Endpoint configuration: create or reuse

* If you don’t already have an endpoint configuration, create one. An endpoint configuration specifies how the model is exposed (compute settings, variants, encryption).
* Choose between hosting modes:
  * Serverless: SageMaker runs the model on-demand without instance management. Ideal for bursty or low-throughput workloads and quick deployments.
  * Provisioned: You select instance families and counts. Use this for predictable, sustained throughput or when you need GPU acceleration.

<Callout icon="lightbulb">
  Serverless endpoints reduce management overhead and are a good starting point for many applications. Choose provisioned endpoints when you need consistent low latency, predictable throughput, or custom instance types (for example, GPU instances).
</Callout>

4. Encryption (optional)

* If your security posture requires it, provide a KMS Customer Managed Key to encrypt model artifacts and endpoint resources at rest. If you don’t specify a KMS key, AWS-managed keys are used by default.

5. Configure model variants

* An endpoint can host one or more model variants. Variants let you run multiple model versions under a single endpoint — for example, a “production” variant and one or more “shadow” variants for testing or A/B evaluation.
* While creating the configuration you will:
  * Select the model(s) to include.
  * Assign each model to production or shadow roles.
  * (Provisioned only) assign instance types and instance counts to each variant.

<Frame>
  <img alt="The image shows the AWS SageMaker console, specifically the &#x22;Create endpoint configuration&#x22; page, where users can configure production and shadow variants. There are currently no resources listed under both sections." />
</Frame>

This variants model supports blue-green and canary deployments: run your current model as the production variant while routing a small percentage of traffic to shadow variants to validate new models. Once a shadow variant proves better, promote it to production.

6. Finalize and create the endpoint

* Review the endpoint configuration (variant assignments, serverless/provisioned settings, and encryption).
* Create the endpoint. Provisioned endpoints can take several minutes to spin up depending on instance types. Serverless endpoints deploy faster but still might need a moment to become available.
* When the endpoint status is `InService` you can call it using the AWS SDKs (e.g., boto3), AWS CLI, or the SageMaker console for real-time inference.

Example: invoke endpoint with boto3 (Python)

```python theme={null}
import boto3
import json

runtime = boto3.client("sagemaker-runtime")
endpoint_name = "your-endpoint-name"
