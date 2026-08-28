# Simplified example: create a SageMaker training job
aws sagemaker create-training-job \
  --training-job-name my-training-job \
  --algorithm-specification TrainingImage=123456789012.dkr.ecr.us-west-2.amazonaws.com/my-image:latest,TrainingInputMode=File \
  --role-arn arn:aws:iam::123456789012:role/SageMakerExecutionRole \
  --input-data-config '[{"ChannelName":"train","DataSource":{"S3DataSource":{"S3Uri":"s3://my-bucket/train","S3DataType":"S3Prefix","S3DataDistributionType":"FullyReplicated"}}}]' \
  --output-data-config '{"S3OutputPath":"s3://my-bucket/output/"}' \
  --resource-config '{"InstanceType":"ml.m5.xlarge","InstanceCount":1,"VolumeSizeInGB":50}'
```

(Adapt the JSON, ARNs, and S3 URIs to your environment.)

## Security, Cost, and Operations

Security: apply multiple layers of protection when defining infrastructure as code:

* IAM: enforce least privilege for training jobs, pipelines, and deployment roles.
* Encryption: enable KMS encryption for data at rest and TLS for data in transit.
* Network: restrict public access and use VPC endpoints for S3, ECR, and other services.
* Secrets: use AWS Secrets Manager or SSM Parameter Store—never hard-code credentials.
* Audit: enable CloudTrail and AWS Config to detect and alert on unexpected changes.

<Frame>
  <img alt="The image is a diagram titled &#x22;Security in IAC for ML&#x22; that outlines five key security components: Network, Secrets, Audit, IAM, and Encryption. Each component includes a brief description of its function in enhancing security." />
</Frame>

Cost optimization and resilience strategies:

* Right-size compute for each environment and use Spot Instances for training where appropriate.
* Enforce resource tagging in IaC to enable cost allocation and reporting.
* Disaster recovery: IaC enables automated rebuilds in another region—version control your recovery playbooks and data replication policies.
* CI/CD integration: automate infrastructure deployments and model promotions with pipelines; leverage ChangeSets for safe updates and rollbacks.

<Frame>
  <img alt="The image outlines &#x22;Cost Optimization With IaC,&#x22; featuring three sections: cost optimization, disaster recovery, and CI/CD versioning, each with associated strategies and actions." />
</Frame>

<Callout icon="lightbulb">
  When building production ML pipelines, combine IaC with CI/CD and observability: treat infrastructure code as part of the application lifecycle, run automated tests, and monitor deployments to detect drift or regressions early.
</Callout>

## Common Anti-Patterns to Avoid

Avoid these pitfalls when applying IaC to ML workloads:

* Hard-coding credentials or model artifacts directly into code or templates.
* Using wildcard IAM policies (for example, `*`) instead of least-privilege policies.
* Making manual, one-off configuration changes that cause drift from declared state.
* Over-provisioning resources that inflate costs.
* Ignoring ChangeSets and rollbacks—these help ensure safe production updates.

<Frame>
  <img alt="The image lists four anti-patterns to avoid: hardcoding credentials, wildcard IAM policies, manual configuration, and over-provisioning resources." />
</Frame>

<Callout icon="warning">
  Never embed secrets or model weights in IaC artifacts. Use managed secret stores and S3 references. Hard-coding sensitive data is the most common cause of costly security incidents.
</Callout>

## Key Takeaways

* IaC is essential for consistent, automated, and scalable ML deployments on AWS.
* Choose the right tool for the job: CloudFormation for declarative stacks, CDK for a code-first developer experience, and AWS CLI for quick prototypes and ad-hoc automation.
* Security practices: enforce least-privilege IAM, enable encryption, isolate resources in VPCs, and use managed secret stores.
* Operational best practices: right-size and tag resources to control cost; plan for disaster recovery; integrate IaC into CI/CD pipelines for traceability and safe rollbacks.
* Avoid anti-patterns like hard-coding secrets, wildcard permissions, and manual configuration drift.

<Frame>
  <img alt="The image is a summary slide about the importance of Infrastructure as Code (IaC) for AWS Machine Learning, covering tools, security, operations, and avoiding anti-patterns." />
</Frame>

## Links and References

* [AWS CloudFormation documentation](https://learn.kodekloud.com/user/courses/aws-cloud-formation)
* [AWS CDK documentation](https://docs.aws.amazon.com/cdk/latest/guide/home.html)
* [AWS CLI documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
* [Amazon SageMaker overview](https://learn.kodekloud.com/user/courses/aws-sagemaker)
* [Amazon S3 best practices](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)

Use these resources to deepen your knowledge and implement secure, repeatable IaC practices for your ML workloads on AWS.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/56180da9-9776-4634-b6d8-917f95932703" />
</CardGroup>


# Introduction to ML Deployment and Orchestration

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Deployment-and-Orchestration-of-ML-Workflows/Introduction-to-ML-Deployment-and-Orchestration/page

Guide to deploying and orchestrating ML models on AWS covering SageMaker deployment patterns, packaging, CI CD, monitoring, model registry, and automated retraining

This lesson explains choices and trade-offs for moving machine learning (ML) models from development into production on AWS. It covers exam-relevant services and tasks including endpoints (real-time, batch, async, serverless), model registry and versioning, packaging (ECR containers or model tar files), CI/CD and orchestration (SageMaker Pipelines, CodePipeline), and monitoring (CloudWatch, SageMaker Model Monitor).

We follow a typical ML deployment journey:
data and artifacts in Amazon S3 → model training in AWS SageMaker → model registration via Model Registry → packaging (ECR containers or `model.tar.gz`) → deployment (endpoints, batch, serverless) → monitoring and retraining automation.

<Frame>
  <img alt="The image outlines the stages of the machine learning deployment journey, including S3 data storage, SageMaker training, model registry, ECR packaging, and deployment." />
</Frame>

Monitoring after deployment is essential. Typical AWS tools include:

* AWS CloudWatch for infra, logs, and custom alarms.
* SageMaker Model Monitor for data and prediction quality checks (data drift, feature distribution changes).

<Callout icon="lightbulb">
  Tip: Treat the ML lifecycle as three versioned, monitored pillars — data, code, and infrastructure. Version artifacts, pipeline definitions, and infra templates to enable safe rollouts and fast rollback.
</Callout>

## Why ML deployment is different from traditional software

* Determinism: Traditional applications are typically deterministic — same inputs + same code = same outputs. ML models depend on data distributions and can produce different outcomes as data drifts.
* Non-stationary inputs: ML systems must handle changes in input distributions (data drift, concept drift).
* Continuous lifecycle: ML demands continuous monitoring, retraining, and reproducible pipelines to avoid performance regressions.
* Artifact heterogeneity: Deployable ML artifacts can be serialized model files, container images, or compiled binaries (e.g., Neo-compiled artifacts).

<Frame>
  <img alt="The image is a comparison between traditional software and machine learning (ML) deployment, highlighting key differences such as deterministic outputs versus data dependency, and versioned code releases versus frequent retraining and monitoring." />
</Frame>

## Deployment patterns — what to choose and when

Choose a deployment pattern that matches latency, throughput, cost, and payload characteristics.

| Pattern                                               | When to use                                                                    | Key considerations                                                                |
| ----------------------------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| Real-time endpoint (SageMaker real-time)              | Low-latency, synchronous inference (sub-second to low predictable latency)     | Persistent instances, autoscaling, cost for always-on endpoints                   |
| Batch (SageMaker Batch Transform / batch jobs)        | Offline scoring or bulk re-scoring on large datasets                           | Asynchronous, high throughput, cost-efficient for large jobs                      |
| Asynchronous Inference (SageMaker Async)              | Large payloads, long-running inference where client polls or receives callback | Handles large payloads, avoids blocking synchronous endpoints                     |
| Serverless inference (SageMaker serverless or Lambda) | Spiky or infrequent traffic                                                    | Lower management overhead, watch cold-starts, concurrency and payload size limits |

<Frame>
  <img alt="The image is an overview of deployment patterns, highlighting different request types including real-time, batch, asynchronous, and serverless inference using AWS SageMaker." />
</Frame>

<Callout icon="warning">
  Warning: Using a real-time endpoint for large-batch scoring or highly variable traffic patterns can be cost-inefficient. Match the workload to the correct pattern and validate with load tests.
</Callout>

## SageMaker deployment ecosystem — main components

* Model Registry: central store for model versions, metadata, and approval workflows (stages: Staging, Production).
* SageMaker model artifact: typically `model.tar.gz` (weights + inference code) or a container image in ECR.
* Endpoints: support real-time, asynchronous, serverless, and multi-model hosting.
* Multi-model endpoints: host multiple models in a single container for cost savings; consider cold-start and memory isolation trade-offs.
* SageMaker Neo: compiles/optimizes models for edge devices and varied hardware targets.

<Frame>
  <img alt="The image is a flowchart depicting the SageMaker Deployment Ecosystem, with elements like S3 (data and artifacts), ECR (containers), Model Registry, VPC/IAM, and Endpoints connected to SageMaker." />
</Frame>

## Integration and packaging considerations

* Amazon S3: store datasets and model artifacts (`model.tar.gz`). Apply lifecycle rules, enable KMS encryption, and limit access via IAM and VPC endpoints.
* Amazon ECR: store custom inference containers. Use immutable tags or digests for reproducibility.
* IAM and VPC: enforce least-privilege IAM roles for SageMaker, ECR, and S3. Use private VPC endpoints when required by compliance.
* Packaging options:
  * `model.tar.gz`: use SageMaker built-in containers or small inference scripts.
  * Docker container (ECR): required for custom runtimes or unsupported frameworks.
* Choosing pre-built containers vs BYOC (Bring Your Own Container): use pre-built for standard frameworks; use BYOC for custom dependencies, special runtimes, or system-level control.

<Frame>
  <img alt="The image illustrates the process of packaging model artifacts from S3 and ECR into SageMaker models, indicating either a direct model file or a custom container." />
</Frame>

## Deployment strategy patterns

Common rollout strategies for models deployed in production:

* Blue-Green: run two independent environments (blue=current, green=new). Validate green and switch traffic when ready — simplifies rollback.
* Canary: route a small percentage of traffic to the new model, monitor behavior, and progressively increase traffic if metrics are healthy.
* Shadow (Mirroring): duplicate production requests to the candidate model without changing responses — good for validating correctness and performance under real traffic.
* Rollback: keep models versioned in Model Registry and enable automated rollback in pipelines when monitoring detects regressions.

<Frame>
  <img alt="The image illustrates deployment strategies, showing a flowchart with client requests managed through an API Gateway/Load Balancer, splitting traffic between Blue (current) and Green (candidate) environments using Canary and Shadow flows." />
</Frame>

## CI/CD, orchestration, and retraining automation

A reliable ML CI/CD and automation pipeline ensures repeatability and safe rollouts.

Typical flow:

1. Code & pipeline definitions in source control (CodeCommit or GitHub).
2. Build & test in CodeBuild (unit tests, model validation).
3. Orchestrate with CodePipeline or third-party CI/CD.
4. Trigger SageMaker Pipelines to run data preprocessing, training, evaluation, and registration.
5. Register model to Model Registry and trigger deployment jobs (endpoint update, Canary, or Blue-Green).
6. Automate retraining via EventBridge (on new data arrival), schedules, or data-change triggers.

Infrastructure as Code:

* Use AWS CDK, CloudFormation, or Terraform to provision endpoints, autoscaling policies, IAM roles, and VPC configuration.

<Frame>
  <img alt="The image depicts a flowchart for MLOps and Deployment Automation, showcasing components like S3 Data storage, SageMaker Pipelines, Model Registry, Deployment (Endpoint/Batch), and Monitoring (CloudWatch/Model Monitor)." />
</Frame>

## Common pitfalls and exam-focused reminders

* No monitoring for drift: Without Model Monitor and CloudWatch alerts, model performance can silently degrade. Automate monitoring and alerting for prediction distributions and performance metrics.
* Insufficient versioning or rollback plans: Always register models in Model Registry and include automated rollback steps in your pipelines.
* Wrong deployment pattern: Matching workload-to-pattern matters — e.g., avoid using low-latency real-time endpoints for occasional, large-scale batch scoring.
* Security and IAM misconfiguration: Apply least privilege, enable KMS encryption for S3/model artifacts, and restrict network access via VPC endpoints when required.
* Cost traps: Persistent large instances or unused real-time endpoints drive costs. Consider autoscaling, multi-model endpoints, serverless hosting, and lifecycle policies to control spend.

<Frame>
  <img alt="The image lists four common deployment challenges and patterns: no monitoring, no versioning, wrong deployment pattern, and IAM misconfiguration, each with a brief explanation." />
</Frame>

## Summary — practical checklist

* Package artifacts reproducibly (`model.tar.gz` or container images with immutable tags).
* Register and stage models in Model Registry for approvals and traceability.
* Select the correct deployment pattern (real-time, batch, async, serverless) based on latency, throughput, and cost.
* Automate CI/CD and SageMaker Pipelines to make retraining and deployment repeatable.
* Monitor data and predictions (Model Monitor + CloudWatch) and trigger retraining or rollback when needed.
* Secure artifacts and infra using least-privilege IAM, KMS, and VPC controls.

This lesson covered the key considerations and AWS services for deploying and orchestrating machine learning models in production.

## Links and references

* [AWS SageMaker documentation](https://learn.kodekloud.com/user/courses/aws-sagemaker)
* [Amazon S3 basics](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [AWS CloudWatch](https://learn.kodekloud.com/user/courses/aws-cloudwatch)
* [AWS CodePipeline (CI/CD)](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline)
* [AWS Lambda](https://learn.kodekloud.com/user/courses/aws-lambda)
* [Terraform basics](https://learn.kodekloud.com/user/courses/terraform-basics-training-course)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/5fea0934-8bbf-435e-a575-d63a77f02a78" />
</CardGroup>
