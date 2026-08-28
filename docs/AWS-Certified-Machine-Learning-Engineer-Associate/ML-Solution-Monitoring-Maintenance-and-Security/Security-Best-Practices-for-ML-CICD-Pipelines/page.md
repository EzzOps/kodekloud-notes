# Security Best Practices for ML CICD Pipelines

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Solution-Monitoring-Maintenance-and-Security/Security-Best-Practices-for-ML-CICD-Pipelines/page

Practical security best practices for protecting ML CI CD pipelines and artifacts using AWS services such as IAM, KMS, VPC, CloudTrail, GuardDuty, and AWS Config.

In this lesson we describe practical security controls for building and operating Machine Learning CI/CD pipelines. The guidance focuses on protecting pipeline artifacts, training data, model artifacts, and deployed endpoints by combining Amazon SageMaker-driven ML workflows with AWS security services such as IAM, KMS, VPC, CloudTrail, AWS Config, GuardDuty, and AWS Shield.

<Frame>
  <img alt="The image discusses ML CI/CD pipelines and security best practices, featuring Amazon SageMaker and AWS Shield." />
</Frame>

Why secure ML CI/CD pipelines?

A CI/CD pipeline automates build, test, and deployment steps for models. Each stage—data ingestion, feature engineering, model training, artifact storage, model packaging, and endpoint deployment—can expose sensitive information or be abused if not secured. Implementing layered protections (identity, encryption, network isolation, and monitoring) ensures confidentiality, integrity, and availability across the pipeline lifecycle.

High-level security goals:

* Enforce least privilege for every pipeline component and service account.
* Encrypt data both at rest and in transit.
* Keep build and deployment traffic off the public internet using private connectivity.
* Maintain immutable audit trails and continuous compliance checks.
* Protect real-time endpoints from volumetric and application-layer attacks.

Here’s a conceptual view of those security layers and tools.

<Frame>
  <img alt="The image outlines the importance of securing ML CI/CD pipelines, emphasizing the flow from ML CI/CD Pipelines through Security Controls (IAM, KMS, VPC) to Trustworthy Deployment." />
</Frame>

Core services and responsibilities

Use the table below to map responsibilities to AWS services commonly used in ML pipelines.

| Responsibility             |                      AWS Service(s) | Example / Notes                                                                              |
| -------------------------- | ----------------------------------: | -------------------------------------------------------------------------------------------- |
| Orchestration              |        CodePipeline, Step Functions | Coordinate build → test → deploy steps and trigger SageMaker jobs.                           |
| Identity & Access Control  |                            IAM, STS | Stage-specific roles and short-lived credentials (`sts:AssumeRole`).                         |
| Network Isolation          | VPC, VPC Endpoints, Security Groups | Use Interface/Gateway endpoints to access S3, ECR, Secrets Manager privately.                |
| Encryption                 |                          KMS (CMKs) | Encrypt S3 buckets, ECR images, EBS volumes, SageMaker artifacts with customer-managed keys. |
| Auditing & Detection       |   CloudTrail, CloudWatch, GuardDuty | Centralized logging, alerts, and threat detection.                                           |
| Compliance & Configuration |                          AWS Config | Continuous evaluation of resource configurations and compliance reporting.                   |

<Frame>
  <img alt="The image is a diagram titled &#x22;AWS Tools for ML CI/CD Pipeline Security,&#x22; showing how CodePipeline/Step Functions orchestrates IAM for access control, VPC for isolation, CloudTrail for auditing, KMS for encryption, and AWS Config for compliance." />
</Frame>

IAM: Designing roles for CI/CD

Good IAM design reduces blast radius and protects secrets/artifacts.

Recommendations

* Create a dedicated pipeline execution role (CodePipeline role or Step Functions execution role).
* Define fine-grained roles for pipeline stages (build, test, deploy) and for SageMaker tasks (training, processing, endpoint creation).
* Scope permissions to specific ARNs and actions: avoid `*` whenever possible.
* Use role chaining or `sts:AssumeRole` so pipeline orchestration can assume short-lived credentials for downstream services.
* Add conditions in policies (e.g., `aws:SourceIp`, `aws:SourceVpc`, or encryption context checks) where applicable.

Example minimal trust policy for a pipeline role:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "codepipeline.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Example inline permission policy for a build/deploy stage (replace ARNs with your values):

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "ecr:BatchGetImage",
        "sagemaker:CreateTrainingJob",
        "sagemaker:CreateModel",
        "sagemaker:CreateEndpointConfig",
        "sagemaker:CreateEndpoint"
      ],
      "Resource": [
        "arn:aws:s3:::my-pipeline-artifacts/*",
        "arn:aws:ecr:us-east-1:123456789012:repository/my-repo",
        "arn:aws:sagemaker:us-east-1:123456789012:*"
      ]
    }
  ]
}
```

<Frame>
  <img alt="The image depicts a flowchart showing IAM configurations for CI/CD pipelines, consisting of CodePipeline, IAM Role, and SageMaker." />
</Frame>

Encryption with KMS

Encryption protects artifacts, datasets, and model parameters—especially in multi-tenant and regulated environments.

Best practices

* Use customer-managed KMS keys (CMKs) for S3 buckets, ECR repositories, EBS volumes, and SageMaker artifacts so you control key rotation and access.
* Limit use and management of keys via IAM policies and KMS key policies, and consider policy conditions like `aws:SourceVpc` or `kms:EncryptionContext`.
* Enable automatic rotation for symmetric CMKs and maintain a key lifecycle policy.
* Apply encryption-at-rest and enforce TLS for all in-transit communications.

Example KMS key policy snippet (granting usage to the pipeline role):

```json theme={null}
{
  "Version": "2012-10-17",
  "Id": "key-default-1",
  "Statement": [
    {
      "Sid": "Allow use of the key",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::123456789012:role/MyPipelineRole" },
      "Action": [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:GenerateDataKey"
      ]
    }
  ]
}
```

<Frame>
  <img alt="The image illustrates a flowchart for &#x22;Encryption With KMS in CI/CD Pipelines,&#x22; showing pipeline data being encrypted with a KMS key and stored in encrypted storage solutions like S3 and ECR." />
</Frame>

VPC and private connectivity

Network design limits exposure and reduces attack surface.

Guidelines

* Run sensitive tasks in private subnets inside a VPC. Use VPC endpoints (Gateway or Interface) to access S3, ECR, Secrets Manager, and other AWS services without public internet egress.
* If internet access is required (for downloads, container registries, etc.), route through NAT Gateways or tightly controlled proxy instances; avoid assigning public IPs to worker nodes.
* Apply least-privilege security group rules and minimal, audited network ACLs.
* Consider using PrivateLink for secure integrations with partner services or cross-account endpoints.

<Frame>
  <img alt="The image illustrates VPC configurations for CI/CD pipelines, showing a pipeline connecting to a VPC endpoint." />
</Frame>

Auditing and monitoring with CloudTrail

Observability and alerting enable detection and response.

Checklist

* Enable CloudTrail across all regions and deliver logs to a centralized, encrypted S3 bucket with restricted access.
* Integrate CloudTrail events with CloudWatch Events / EventBridge to trigger alerts on suspicious or risky actions (e.g., public policy changes, KMS key policy updates, creation of public endpoints).
* Use Amazon Athena or a SIEM to query and analyze CloudTrail logs over time.
* Add GuardDuty for threat detection and Amazon Detective for investigation workflows.

Audit flow summary:

1. Pipeline triggers actions (training, model packaging, endpoint updates).
2. CloudTrail records API calls across the account as events.
3. Use Athena, CloudWatch, EventBridge, or a SIEM to analyze events and produce alerts/reports.

AWS Config for continuous compliance

AWS Config continuously evaluates resource configuration and supports automated remediation.

How to use AWS Config

* Implement rules that reflect your baseline (e.g., `s3-bucket-server-side-encryption-enabled`, `kms-key-rotation-enabled`, `sagemaker-endpoint-public-access`).
* Evaluate resources that matter to your pipeline: IAM roles/policies, KMS keys, VPC settings, S3/ECR configurations, SageMaker resources.
* Integrate Config remediation or pipeline gating so deployments are blocked or flagged when non-compliant resources are detected.

<Frame>
  <img alt="The image is a diagram illustrating a process for security and compliance in CI/CD pipelines, involving AWS Config, evaluation of pipeline resources (IAM, VPC, KMS), and generating a compliance report." />
</Frame>

Anti-patterns to avoid

Avoid common mistakes that increase risk and complicate incident response:

* Granting broad admin permissions instead of scoped, stage-specific roles.
* Leaving datasets, model artifacts, or logs unencrypted.
* Exposing pipeline components or endpoints to the public internet without authentication and network controls.
* Skipping logging, auditing, or automated compliance checks—visibility is critical for incident detection.

<Frame>
  <img alt="The image lists four anti-patterns to avoid in security: granting overly broad admin permissions, failing to encrypt datasets, leaving pipelines open to the internet, and skipping auditing/logging." />
</Frame>

<Callout icon="lightbulb">
  Always apply the principle of least privilege: give pipeline stages and SageMaker jobs only the permissions they require. Combine least privilege with KMS-backed encryption and VPC isolation to build a layered, defense-in-depth posture.
</Callout>

Key action items (summary)

* Create dedicated pipeline execution roles and stage-specific IAM roles; scope permissions to needed actions and ARNs.
* Encrypt sensitive data and artifacts with KMS-managed keys and enforce encryption context / policy conditions where possible.
* Run pipeline workloads inside a VPC and use VPC endpoints to avoid public network exposure.
* Centralize CloudTrail logs, enable GuardDuty, and analyze events using Athena, CloudWatch, or a SIEM.
* Use AWS Config rules to continuously assess resource posture and gate deployments on compliance.

References and further reading

* [Amazon SageMaker documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* [AWS Identity and Access Management (IAM)](https://docs.aws.amazon.com/iam/latest/UserGuide/introduction.html)
* [AWS Key Management Service (KMS)](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)
* [Amazon VPC endpoints (Interface and Gateway)](https://docs.aws.amazon.com/vpc/latest/privatelink/endpoint-services-overview.html)
* [AWS CloudTrail user guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html)
* [AWS Config developer guide](https://docs.aws.amazon.com/config/latest/developerguide/what-is-aws-config.html)
* [Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html)

Following these patterns reduces risk across your ML CI/CD lifecycle—making pipelines more secure, auditable, and resilient to threats.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/e07ceb86-4976-4c8e-a6f8-3518534ec115/lesson/0403d403-6181-45b6-91ad-cb4692efe1bd" />
</CardGroup>
