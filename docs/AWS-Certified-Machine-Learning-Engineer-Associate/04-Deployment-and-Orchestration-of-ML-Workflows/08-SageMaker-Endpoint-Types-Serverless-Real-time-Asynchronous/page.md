# SageMaker Endpoint Types Serverless Real time Asynchronous

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Deployment-and-Orchestration-of-ML-Workflows/SageMaker-Endpoint-Types-Serverless-Real-time-Asynchronous/page

Overview comparing Amazon SageMaker endpoint types and trade offs across serverless, real time, multi model, and asynchronous deployments for latency, cost, scalability, monitoring, and security

In this lesson we compare the Amazon SageMaker endpoint types you can use to deploy machine learning models. Understanding the trade-offs between serverless, real-time (single- and multi-model), and asynchronous inference will help you choose the right deployment strategy for latency, cost, and scalability requirements.

We’ll cover:

* The types of SageMaker endpoints available for deploying models.
* How each endpoint type balances latency, cost, and scalability.
* Practical guidance for selecting the most suitable endpoint type for your workload.

<Frame>
  <img alt="The image displays an agenda for a presentation about SageMaker endpoints, discussing types of endpoints, balancing latency, cost, and scalability, and choosing the right endpoint type for use cases." />
</Frame>

When deploying models with Amazon SageMaker, you should match your endpoint choice to expected traffic patterns, payload sizes, and latency targets. Below is an overview of the primary endpoint options and how they differ.

SageMaker endpoint options at a glance:

* Single-model (dedicated real-time): one model per endpoint/instance.
* Multi-model (real-time shared): many models served from one endpoint; models loaded on demand from S3.
* Serverless (real-time): no infrastructure to manage; scales to zero and is billed per invocation.
* Asynchronous (batch-like): queue-based inference for large payloads or long-running jobs.

<Frame>
  <img alt="The image illustrates &#x22;The SageMaker Endpoint Ecosystem&#x22; with Amazon SageMaker at the center, highlighting four types: Single-Model, Multi-Model, Serverless, and Asynchronous." />
</Frame>

## Single-Model Endpoints (Dedicated Real-Time)

Each endpoint hosts one model (or one model container) that stays loaded in memory.

Key characteristics:

* Low and predictable latency because the model is resident in memory.
* Best when you need consistent, low-latency responses and have steady traffic.
* Simple operational model: one model = one endpoint.
* Cost model: you pay for provisioned instances continuously; this is cost-effective for steady, predictable traffic.

<Frame>
  <img alt="The image illustrates a &#x22;Single-Model Endpoints&#x22; setup with a user directing requests to &#x22;Model 1,&#x22; highlighting benefits such as low latency, steady traffic, simplicity, and predictable performance." />
</Frame>

## Multi-Model Endpoints (Shared Real-Time)

Multi-model endpoints let you host many models behind a single endpoint. Models are stored in S3 and loaded into the serving container when requested.

Important points:

* Very cost-effective when you have many models that are infrequently invoked.
* The first request for a model triggers a model load from S3 (cold start); subsequent requests benefit from the in-container cache until memory eviction.
* Best suited for workloads with many cold models rather than a few hot models requiring low latency.
* Operational considerations: less isolation, potential complications for per-model scaling, and instance-type constraints.

## Serverless Inference (Real-Time, No Infrastructure Management)

Serverless endpoints automatically provision compute when you receive requests and scale to zero when idle.

Flow:

* Client or API call requests prediction from a serverless endpoint.
* SageMaker provisions compute, loads the model, runs inference, and returns the response.
* Billing is based on the compute duration and memory used per invocation.

Benefits and trade-offs:

* Ideal for infrequent or unpredictable traffic—no infrastructure to manage.
* Best for lightweight models and typical real-time request sizes.
* Cold starts on the first invocation after idle periods can add latency; if strict low-latency is required, consider a dedicated single-model endpoint with provisioned capacity.

> **warning** Serverless endpoints can have noticeable cold-start latency on the first invocation after idle periods. If you require near-constant low latency, prefer single-model endpoints with reserved capacity or use warm-up strategies.

<Frame>
  <img alt="The image is a diagram illustrating serverless inference, showing a flow from a client/API to a serverless endpoint, and then to predictions. It highlights benefits such as no infrastructure management and automatic scaling with demand." />
</Frame>

## Asynchronous Inference (Queue-Based, Large Payloads & Long Jobs)

Asynchronous inference is designed for large payloads or long-running inference jobs that are not suitable for synchronous real-time endpoints.

Typical flow:

* Client uploads input data to an input S3 bucket or posts a request to the asynchronous endpoint.
* SageMaker queues the job and processes it when compute is available.
* When processing completes, the results are saved to an output S3 bucket or made available for retrieval.

Use cases:

* Large request/response payloads (e.g., high-resolution images, long documents).
* Models that require long processing times or would exceed HTTP timeout limits.
* Batch-style or offline workflows where immediate responses are not required.
* Decoupling client and processing lifecycles to avoid blocking client threads during heavy compute.

<Frame>
  <img alt="The image illustrates an asynchronous inference process, showing data flow from a client to an Input S3 bucket, then to asynchronous inference, and finally to an Output S3 bucket. Additionally, it highlights the suitability of this method for handling long-running requests and batch-style jobs." />
</Frame>

## Endpoint Types Comparison

Use this high-level summary to choose the right endpoint type based on latency tolerance, traffic pattern, payload size, and cost sensitivity.

| Endpoint Type | Latency                                         | Cost Model                                 | Best For                                                       |
| ------------- | ----------------------------------------------- | ------------------------------------------ | -------------------------------------------------------------- |
| Single-model  | Lowest, most predictable                        | Pay for provisioned instances continuously | Steady traffic, strict low-latency requirements                |
| Multi-model   | Variable (cold start possible)                  | Cost-efficient for many models (S3-backed) | Many infrequently used models, reduced per-model cost          |
| Serverless    | Variable (cold starts)                          | Pay per invocation (compute & memory time) | Unpredictable or low traffic, avoid infra management           |
| Asynchronous  | Higher end-to-end latency, tolerant of queueing | Cost based on jobs and storage             | Large payloads, long-running models, offline/queued processing |

<Frame>
  <img alt="The image is a comparison table of endpoint types, detailing latency, cost, and use case for Single-Model, Multi-Model, Serverless, and Asynchronous endpoints." />
</Frame>

> **lightbulb** Choose the endpoint type based on request volume, latency requirements, payload size, and cost sensitivity. For predictable, low-latency needs use single-model endpoints; for many cold models use multi-model; for unpredictable short bursts use serverless; and for large or long-running tasks use asynchronous.

## Monitoring, Scaling, and Cost Optimization

To operate endpoints effectively, focus on observability, auto-scaling, and right-sizing:

* CloudWatch monitoring: track latency, invocation count, error rates, and instance metrics to detect anomalies and guide scaling.
* Auto-scaling: use target-tracking or custom policies to match capacity to demand and reduce over-provisioning.
* Right-sizing: periodically review instance families (CPU/GPU/memory) to align cost with performance needs.
* Use multi-model or serverless endpoints where appropriate to reduce costs for many infrequently used models or sporadic traffic.

## Security Best Practices

Apply these controls across deployments to protect models and data:

* IAM least privilege: grant only required permissions to users and services.
* Encrypt data: use AWS KMS to encrypt data at rest and TLS for data in transit.
* Network isolation: place endpoints in a VPC when private connectivity or tightened egress control is required.
* Secure by design: include security checks during CI/CD and model lifecycle management.

<Frame>
  <img alt="The image lists four security and best practices: applying IAM least privilege, encrypting data with KMS, securing endpoints in VPC, and ensuring security alignment with deployment." />
</Frame>

Finally, integrate monitoring, automated scaling, cost reviews, and security checks into your deployment process to meet performance, cost, and compliance objectives across the model lifecycle.

## Links and references

* Amazon SageMaker documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/what-is-sagemaker.html](https://docs.aws.amazon.com/sagemaker/latest/dg/what-is-sagemaker.html)
* SageMaker serverless inference: [https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-inference.html](https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-inference.html)
* SageMaker asynchronous inference: [https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html](https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html)
* AWS CloudWatch: [https://aws.amazon.com/cloudwatch/](https://aws.amazon.com/cloudwatch/)
* AWS IAM best practices: [https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
* AWS KMS: [https://aws.amazon.com/kms/](https://aws.amazon.com/kms/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/715d91dc-7ae5-4c3e-bc49-9ea5558ab93d)
