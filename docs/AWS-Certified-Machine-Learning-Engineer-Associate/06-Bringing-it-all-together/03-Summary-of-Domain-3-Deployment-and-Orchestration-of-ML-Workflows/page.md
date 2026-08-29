# Summary of Domain 3 Deployment and Orchestration of ML Workflows

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Bringing-it-all-together/Summary-of-Domain-3-Deployment-and-Orchestration-of-ML-Workflows/page

Overview of deploying and orchestrating machine learning workflows on AWS, covering deployment patterns, containers, security, IaC, CI CD, edge optimization, and production monitoring

This lesson summarizes the recommended patterns and operational practices for deploying and orchestrating machine-learning workflows on AWS. It covers the end-to-end journey from data storage and training to packaging, deployment, and production monitoring, while emphasizing security, cost, and operational trade-offs.

A typical ML deployment journey on AWS follows these stages:

* Store data and model artifacts in [Amazon Simple Storage Service (Amazon S3)](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3).
* Run training jobs with [Amazon SageMaker](https://learn.kodekloud.com/user/courses/aws-sagemaker) using stored data.
* Register and version the trained model in the SageMaker Model Registry.
* Package the model and inference code into a container image and push it to [Amazon Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/).
* Choose the deployment pattern (real-time endpoint, batch transform, serverless, or asynchronous processing) and host the model.
* Monitor production behavior with [AWS CloudWatch](https://learn.kodekloud.com/user/courses/aws-cloudwatch) and SageMaker Model Monitor to detect performance regressions or data/model drift.

For low-latency, on-demand predictions, a real-time SageMaker endpoint is typically appropriate.

<Frame>
  <img alt="The image illustrates &#x22;The ML Deployment Journey&#x22; using AWS services, including S3, SageMaker Training, Model Registry, ECR (for packaging), Deployment, and CloudWatch/Model Monitor." />
</Frame>

Deployment pattern selection depends on request characteristics, throughput, latency tolerance, payload size, operational complexity, and cost. Common patterns:

* Real-time (low-latency, synchronous): online endpoints for single-request predictions.
* Batch (asynchronous bulk): transform jobs for large datasets with no strict latency constraints.
* Async (long-running or large payloads): de-coupled request/response using queues or asynchronous endpoints to avoid timeouts.
* Serverless (bursty or low-traffic): cost-effective for infrequent traffic with automatic scaling.

Use the following table to compare patterns at a glance:

| Pattern    |                             Best for |                            Latency | Typical AWS Service                                            |
| ---------- | -----------------------------------: | ---------------------------------: | -------------------------------------------------------------- |
| Real-time  | Low-latency, interactive predictions |                                Low | SageMaker real-time endpoints                                  |
| Batch      |      Large datasets, offline scoring |                       High (batch) | SageMaker Batch Transform                                      |
| Async      |      Large payloads / long inference |               Variable; de-coupled | SageMaker async endpoints or SQS + Lambda                      |
| Serverless |         Infrequent or bursty traffic | Low–Medium; subject to cold starts | Lambda with container images or SageMaker Serverless Inference |

<Frame>
  <img alt="The image illustrates deployment patterns categorized into Real-Time, Batch, Async, and Serverless, highlighting different request types. It also considers factors like latency, throughput, payload size, and cost." />
</Frame>

Container strategy and orchestration choices

Container options range from managed runtimes and pre-built SageMaker containers to BYOC (bring-your-own-container) and fully self-managed orchestration (ECS/EKS). The trade-off is simple: more control increases operational overhead (security, updates, image size, tuning).

Key container best practices:

* Apply least-privilege [IAM](https://learn.kodekloud.com/user/courses/aws-iam) roles for SageMaker, ECR, S3, and other services.
* Encrypt artifacts and images using [AWS KMS](https://aws.amazon.com/kms/).
* Scan container images for vulnerabilities and maintain a Software Bill of Materials (SBOM).
* Use VPC endpoints and run endpoints inside VPCs when private network access is required.
* Choose smaller base images and managed runtimes to reduce cold-starts and maintenance.

> **lightbulb** Container choice affects security, cost, and operational complexity. Prefer managed runtimes when possible and minimize image surface area to reduce vulnerabilities and cold starts.

<Frame>
  <img alt="The image outlines &#x22;Containers – Security Best Practices&#x22; focusing on IAM, KMS, image scanning, and VPC endpoints, with recommendations for least-privilege roles, encryption, and private network access." />
</Frame>

Edge deployment with SageMaker Neo

For on-device inference, SageMaker Neo compiles and optimizes trained models for specific hardware targets. Typical workflow:

* Start with a trained model artifact from SageMaker or another training environment.
* Use SageMaker Neo to compile and optimize the model for the target edge device.
* Deploy the compiled artifact to the device.

Benefits include reduced latency, lower power usage, and improved runtime performance on constrained hardware.

<Frame>
  <img alt="The image is a diagram titled &#x22;Edge Deployment With SageMaker Neo,&#x22; outlining steps from a trained model to deployment on an edge device, highlighting benefits like reduced latency, lower power usage, and improved performance." />
</Frame>

Infrastructure as Code (IaC) for ML

When you apply IaC to ML, evaluate these four categories:

| Category               | What to consider                                                                                            |
| ---------------------- | ----------------------------------------------------------------------------------------------------------- |
| Tools                  | Declarative templates (CloudFormation), AWS CDK constructs, or scripted CLI for simple flows                |
| Security               | Enforce IAM least privilege, KMS encryption, network isolation, and secure secret management                |
| Operational excellence | Cost optimization, disaster recovery, CI/CD automation, and artifact/version management                     |
| Anti-patterns to avoid | Hard-coding secrets, wildcard IAM permissions, manual drift, over-provisioning, missing rollback strategies |

> **warning** Avoid anti-patterns such as embedded secrets, overly broad IAM permissions, and manual configuration changes that bypass IaC. These lead to security and reliability problems.

<Frame>
  <img alt="The image is a diagram titled &#x22;IAC for ML&#x22; outlining categories and considerations for machine learning infrastructure as code, including tools, security, operational excellence, and anti-patterns to avoid. Each category lists relevant items like CloudFormation, IAM least privilege, cost optimization, and avoiding hardcoding secrets." />
</Frame>

CI/CD and MLOps automation

A robust ML CI/CD pipeline on AWS commonly uses:

* [AWS CodePipeline](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline) to orchestrate end-to-end automation and trigger runs on code or data changes.
* [AWS CodeBuild](https://aws.amazon.com/codebuild/) to compile, run unit tests, build artifacts, and package models.
* [AWS CodeDeploy](https://aws.amazon.com/codedeploy/) or other deployment mechanisms to automate rollouts.
* [Amazon SageMaker](https://learn.kodekloud.com/user/courses/aws-sagemaker) for training jobs, model registration, and serving.

These services enable repeatable, auditable automation that integrates build, test, and deploy stages for MLOps workflows.

Recommended security layers for pipelines:

* Identity and access control with scoped IAM roles and policies.
* Encryption of code, data, and model binaries using KMS.
* Network isolation using VPCs and private endpoints.
* Audit logging and monitoring using [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) and CloudWatch.

<Frame>
  <img alt="The image illustrates the process of implementing machine learning CI/CD using AWS services: CodePipeline, CodeBuild, CodeDeploy, and SageMaker. It shows the flow from building and testing to deployment and managing ML jobs." />
</Frame>

Testing and secure environments

Testing should occur in protected, representative environments. Key practices:

* Apply strict IAM scoping and role separation for test workloads.
* Encrypt test data at rest (KMS) and in transit (TLS).
* Use data masking, pseudonymization, or synthetic datasets to avoid exposing production-sensitive information.
* Automate test environment provisioning via IaC to avoid configuration drift.

<Frame>
  <img alt="The image details components of security in machine learning testing, including IAM roles and policies, encryption, and data masking, all contributing to a secure test environment." />
</Frame>

Key takeaways

* ML deployment is a continuous lifecycle: train → register → package → deploy → monitor.
* Pick the deployment pattern (real-time, batch, async, serverless, edge) based on latency, throughput, payload size, cost, and operational constraints.
* Use containers and ECR for consistent, portable deployments; prefer small, scanned images and managed runtimes to reduce operational overhead.
* Build security around least-privilege IAM, KMS-based encryption, VPC isolation, and centralized auditing/logging.
* Automate delivery with CI/CD (CodePipeline, CodeBuild, CodeDeploy and SageMaker) for repeatability and traceability.
* Optimize for edge with SageMaker Neo when on-device performance and power efficiency are priorities.
* Avoid anti-patterns: do not hard-code secrets, do not use wildcard IAM permissions, prevent configuration drift, and include rollback and disaster recovery plans.

A secure, resilient ML system combines strong identity controls, encryption, private networking, automated pipelines, and continuous monitoring to maintain model performance and compliance through production.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/dd1231df-ce1b-453d-92d6-e6250b5d45cf/lesson/9756112a-ae67-4ef5-88e5-6d50f54cb5fa)
