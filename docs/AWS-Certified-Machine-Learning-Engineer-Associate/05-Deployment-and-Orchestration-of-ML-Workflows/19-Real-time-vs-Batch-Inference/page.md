# Real time vs Batch Inference

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Deployment-and-Orchestration-of-ML-Workflows/Real-time-vs-Batch-Inference/page

Comparing real-time and batch ML inference on AWS SageMaker, covering deployment options, scaling, monitoring, cost optimization, CI/CD, model versioning, and security best practices.

This lesson explains the core decision when deploying machine learning models: choosing between real-time (online) and batch (offline) inference. You’ll learn how each approach works, when to use one over the other, and how to deploy and operate them on AWS — with a focus on Amazon SageMaker. We also cover model-versioning, CI/CD orchestration, scaling, monitoring, cost optimization, and security.

Agenda

* Quick [SageMaker](https://learn.kodekloud.com/user/courses/aws-sagemaker) overview as a core ML deployment service.
* Endpoint options: real-time (synchronous), asynchronous, serverless, and batch.
* Model Registry: versioning, approval workflows, and rollback.
* CI/CD and orchestration: [CodePipeline](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline), CodeBuild, SageMaker Pipelines, and [EventBridge](https://aws.amazon.com/eventbridge/).

<Frame>
  <img alt="The image is an agenda slide detailing topics related to machine learning deployment using AWS services, including SageMaker Overview, Endpoints, Model Registry, and CI/CD and Orchestration." />
</Frame>

Overview: two primary inference patterns

* Real-time (online) inference — handle single requests and return immediate predictions.
* Batch (offline) inference — process many records at once and return bulk outputs.

Choose real-time when low latency (milliseconds to sub-seconds) is required. Choose batch when latency can be higher and you need cost-efficient processing of large volumes.

<Frame>
  <img alt="The image outlines two paths to prediction: real-time inference, used for fraud detection, IoT, and personalization, and batch inference, used for reports and bulk processes." />
</Frame>

Real-time inference (synchronous)

* How it works: client sends an API request → request routes to a live SageMaker endpoint → hosted model returns a prediction with low latency.
* Typical use cases: fraud detection, live personalization, IoT telemetry processing, online recommendation engines.
* Trade-offs: low latency and high availability typically require always-on compute (higher cost). You must tune instance type and count, autoscaling policies, and consider cold-start behavior (especially for serverless).
* SageMaker deployment options:
  * Real-Time Endpoints (synchronous) — best for sub-second responses.
  * Serverless Inference — ideal for spiky or low-throughput workloads to avoid always-on costs.
  * Asynchronous Inference — decouples request submission and result retrieval for long-running inference.

<Frame>
  <img alt="The image is a diagram illustrating real-time inference using SageMaker, showing the flow from a user request API to a SageMaker endpoint and then to prediction with latency and cost considerations." />
</Frame>

Batch inference (offline)

* How it works: input data sits in S3 → start a SageMaker Batch Transform job (or other batch processor) → job processes the dataset in parallel and writes bulk predictions back to S3.
* Typical use cases: nightly aggregation and reporting, batch scoring of a customer base, large-scale image classification, or labeling pipelines.
* Trade-offs: run times can be minutes to hours depending on data size and parallelism, but batch is cost-efficient for large, non-time-sensitive workloads.
* SageMaker batch options:
  * Batch Transform — optimized for large, parallel, stateless inference jobs.
  * For heavy pre/post processing, integrate Batch Transform with EMR or Glue in your pipeline.

<Frame>
  <img alt="The image illustrates a process for batch inference using AWS SageMaker, with data coming from S3 to perform batch transformations and output predictions in bulk. It highlights use cases such as nightly reports and image classification." />
</Frame>

Comparison summary

| Aspect          | Real-time (Online)                                               | Batch (Offline)                                                                                     |
| --------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Trigger         | API/user requests (event driven)                                 | Dataset-driven or scheduled jobs                                                                    |
| Typical service | SageMaker real-time endpoints, serverless inference              | SageMaker Batch Transform                                                                           |
| Latency         | Milliseconds to sub-seconds (model & instance dependent)         | Minutes to hours                                                                                    |
| Output          | Single, immediate prediction                                     | Bulk predictions for large datasets                                                                 |
| Cost profile    | Higher for always-on endpoints (steady traffic)                  | Often cheaper for infrequent, large runs                                                            |
| Scaling model   | Autoscale instance count per endpoint (Application Auto Scaling) | Choose instance type/count per job, control parallelism (`split_type`, `max_concurrent_transforms`) |

<Frame>
  <img alt="The image is a comparison table between Real-Time Inference and Batch Inference, detailing differences in aspects like input, service, latency, and output." />
</Frame>

AWS deployment options beyond plain real-time vs batch

* Real-time:
  * SageMaker real-time endpoints for consistently low-latency needs.
  * Serverless Inference for intermittent traffic and to reduce always-on costs.
  * Asynchronous endpoints when inference runs long and clients can poll or receive callbacks.
* Batch:
  * SageMaker Batch Transform for large parallel inference.
  * Combine with EMR or Glue when distributed pre/post processing is required.
* Containerized custom serving:
  * Run model-serving containers on Fargate or ECS when you require full control over the serving stack or custom dependencies.
* Lightweight/event-driven:
  * Use Lambda for small, fast inference or as orchestration glue (be mindful of Lambda’s time and memory limits).

Operational considerations (monitoring, scaling, cost)

* Monitoring:
  * Use Amazon CloudWatch to capture latency (p95/p99), invocation counts, error rates, CPU/GPU utilization, and memory.
  * Record application-level signals such as model confidence distributions, prediction drift, and feature distribution changes.
* Scaling:
  * Real-time endpoints: configure Application Auto Scaling policies using CloudWatch metrics (e.g., `InvocationsPerInstance`, custom latency metrics). For GPU-backed workloads, scale by instance count and consider multi-model or multi-container endpoints for density.
  * Batch jobs: tune instance type, instance count, `split_type`, and `max_concurrent_transforms` to meet throughput goals.
* Cost optimization:
  * Choose lower-cost families for batch (compute-optimized, memory-optimized as needed).
  * Use Spot Instances for preprocessing or training where allowed.
  * Use serverless inference for low or spiky load and multi-model endpoints when serving many small models from a single instance.

Security best practices for ML deployments

* Principle of least privilege: assign narrowly scoped IAM roles and policies for each service and workflow.
* Encryption:
  * Encrypt data at rest (S3 SSE-KMS or SSE-S3) and in transit (HTTPS/TLS).
  * Use AWS KMS for key management and audit key usage.
* Network controls:
  * Place endpoints in VPCs when possible; use VPC endpoints for S3 to keep traffic off the public internet.
  * Apply security groups and NACLs to restrict network access.
* Secrets and credentials:
  * Store keys and secrets in AWS Secrets Manager or Systems Manager Parameter Store — not in code or images.
* Audit and compliance:
  * Enable CloudTrail for API auditing and ensure log retention and monitoring meet compliance requirements.

Links and references

* [Amazon SageMaker documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* [SageMaker Batch Transform](https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html)
* [SageMaker Real-Time Inference](https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html)
* [Serverless Inference](https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-inference.html)
* [Amazon EMR](https://aws.amazon.com/emr/)
* [AWS Glue](https://aws.amazon.com/glue/)
* [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
* [AWS KMS](https://aws.amazon.com/kms/)
* [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
* [Application Auto Scaling](https://aws.amazon.com/autoscaling/application-autoscaling/)

<Callout icon="lightbulb">
  Choose real-time inference for low-latency, user-facing scenarios and batch inference for cost-effective, large-scale scoring. Consider serverless or asynchronous options when you want to reduce always-on costs or handle long-running requests.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/10a2bd03-ec16-42c1-b5d7-d86bfe837fc2" />
</CardGroup>
