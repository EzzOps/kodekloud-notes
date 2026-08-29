# SageMaker Security and Compliance Features

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Solution-Monitoring-Maintenance-and-Security/SageMaker-Security-and-Compliance-Features/page

Practical security and compliance controls for Amazon SageMaker workloads using IAM, KMS encryption, VPC isolation, CloudTrail auditing, and automated compliance to protect ML data and deployments

In this lesson we cover the primary security and compliance controls you should apply when running Amazon SageMaker workloads. We focus on practical, foundational controls that integrate SageMaker with core AWS security services to protect ML data, control access, isolate network traffic, and support regulatory requirements.

> **lightbulb** This article highlights actionable controls and patterns for securing ML workloads on SageMaker, including identity and access management (IAM), encryption (KMS), network isolation (VPC & endpoints), auditing (CloudTrail), and secure deployment (multimodel & edge scenarios).

SageMaker operates within the broader AWS security ecosystem. Complement SageMaker controls with account-level protections such as [AWS Shield](https://aws.amazon.com/shield/) for DDoS mitigation and centralized account governance.

<Frame>
  <img alt="The image illustrates &#x22;SageMaker Security and Compliance Features&#x22; by showing Amazon SageMaker and AWS Shield icons connected by a plus sign." />
</Frame>

Why this matters

ML systems process sensitive inputs (PII, PHI) and produce valuable models. Applying the correct controls preserves confidentiality, integrity, and availability, and helps meet regulations such as [HIPAA](https://www.hhs.gov/hipaa/index.html) and [GDPR](https://gdpr.eu/).

<Frame>
  <img alt="The image is a flowchart explaining the benefits of SageMaker Security and Compliance, showing the progression from ML Workloads to Security Controls and Compliance Outcomes." />
</Frame>

Core AWS services to use with SageMaker

| Service        | Primary use with SageMaker                                                                                      | Reference                                                                |
| -------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| AWS KMS        | Encrypt data, model artifacts, and secrets using customer-managed keys (CMKs)                                   | [https://aws.amazon.com/kms/](https://aws.amazon.com/kms/)               |
| AWS IAM        | Provide fine-grained access control via roles and policies (execution roles for training, endpoints, notebooks) | [https://aws.amazon.com/iam/](https://aws.amazon.com/iam/)               |
| AWS CloudTrail | Audit API activity to capture who did what and when                                                             | [https://aws.amazon.com/cloudtrail/](https://aws.amazon.com/cloudtrail/) |
| Amazon VPC     | Isolate network access; use interface and gateway endpoints to avoid public internet                            | [https://aws.amazon.com/vpc/](https://aws.amazon.com/vpc/)               |

IAM integration with SageMaker

SageMaker requires permissions to access resources such as S3 buckets or ECR images. You grant these permissions by supplying an execution role to SageMaker resources (training jobs, processing jobs, endpoints, notebooks). SageMaker assumes that role to perform AWS API calls on your behalf, so keep the role scoped to least privilege.

<Frame>
  <img alt="The image shows a flowchart illustrating IAM integration with SageMaker, detailing the process from Amazon SageMaker to AWS IAM, and then to Amazon S3." />
</Frame>

Example: minimal IAM policy (allow GetObject from a specific S3 bucket and create a SageMaker training job)

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "sagemaker:CreateTrainingJob"
      ],
      "Resource": "*"
    }
  ]
}
```

> **warning** Do not use `"Resource": "*"` in production. Scope permissions to specific ARNs (for example, the S3 bucket and prefix your training jobs use) and apply least-privilege principles. Consider separate roles per environment (dev/stage/prod).

Recommended scoped example (replace placeholders):

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::ml-secure-bucket/training-data/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sagemaker:CreateTrainingJob",
        "sagemaker:DescribeTrainingJob"
      ],
      "Resource": "arn:aws:sagemaker:us-east-1:123456789012:training-job/*"
    }
  ]
}
```

Encrypting ML data with AWS KMS

Encrypt data at rest and enforce TLS in transit. Use AWS KMS to generate and manage encryption keys and configure services (S3, EBS, SageMaker) to use those KMS keys for server-side encryption. Example S3 bucket encryption (server-side KMS):

```json theme={null}
{
  "ServerSideEncryptionConfiguration": {
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "aws:kms",
          "KMSMasterKeyID": "alias/ml-key"
        }
      }
    ]
  }
}
```

Best practices:

* Use customer-managed CMKs for separation of duties and auditability.
* Define KMS key policies to restrict who can use or manage keys.
* Rotate keys where applicable and monitor KMS CloudTrail events.

Securing SageMaker within a VPC

Place SageMaker resources in your VPC to prevent egress over the public internet. Use VPC Subnet configuration for notebooks, training jobs, and endpoints, and use VPC endpoints to access AWS services privately:

* Use interface VPC endpoints (AWS PrivateLink) for service APIs (SageMaker control plane, ECR, Secrets Manager).
* Use gateway VPC endpoints for S3 to route traffic privately to buckets.
* Configure security groups and network ACLs to allow only necessary ENI traffic.

<Frame>
  <img alt="The image shows a diagram of VPC configurations for SageMaker, illustrating a connection between SageMaker and a VPC Endpoint." />
</Frame>

Auditing with CloudTrail

Enable CloudTrail for all regions and centralize logs in a logging/account. CloudTrail records SageMaker API calls (CreateTrainingJob, CreateEndpoint, etc.) so you can:

* Query events with Athena for forensics and periodic review.
* Create CloudWatch metrics and alerts for anomalous activity.
* Retain logs per your compliance retention requirements.

Securing multimodel endpoints

Multimodel endpoints load models from S3 on-demand. Control access with IAM policies on the SageMaker execution role so the endpoint can only read specific S3 keys. Combine role restrictions with S3 bucket policies and server-side encryption (SSE-KMS) for defense in depth.

<Frame>
  <img alt="The image depicts a diagram of security for multi-model endpoints, showing an IAM policy and models in S3 connected to a multi-model endpoint." />
</Frame>

Securing edge deployments

When deploying compiled models to edge devices (for example, via SageMaker Neo), follow these controls:

* Grant the device identity the minimal IAM permissions to download model artifacts and send telemetry.
* Use TLS for all downloads and telemetry.
* Prefer short-lived credentials or presigned URLs for model artifact access.
* Rotate device credentials and use device identity lifecycle management.

<Frame>
  <img alt="The image shows a flow diagram titled &#x22;Security for Edge Deployments,&#x22; detailing a process involving IAM Policy, an Edge Device, and a Compiled Model (Neo)." />
</Frame>

Automating compliance checks with AWS Config

Use AWS Config to continuously record resource configurations and evaluate them against defined rules. Config enables you to:

* Detect drift from your security baseline.
* Produce compliance reports for auditors.
* Trigger automated remediation via Systems Manager Automation or Lambda.

<Frame>
  <img alt="The image is a flowchart showing &#x22;Compliance With SageMaker Features,&#x22; illustrating the process from &#x22;AWS Config&#x22; to &#x22;Evaluate Security Rules&#x22; and ending with a &#x22;Compliance Report.&#x22;" />
</Frame>

Anti-patterns to avoid

* Over-permissive IAM policies (e.g., `"Resource": "*"` or overly broad actions)
* Leaving data unencrypted at rest or in transit
* Exposing endpoints to the public internet without necessity
* Not enabling CloudTrail or failing to retain audit logs for required periods

Key action items for securing SageMaker

| Task                                            | Why it matters                                             |
| ----------------------------------------------- | ---------------------------------------------------------- |
| Use IAM roles with least privilege              | Limits blast radius and enforces separation of duties      |
| Encrypt data and artifacts with KMS             | Protects confidentiality and enables key-level auditing    |
| Isolate resources in VPCs and use VPC endpoints | Avoids public internet egress and reduces attack surface   |
| Enable CloudTrail and AWS Config                | Provides audit trails and continuous compliance monitoring |

Adopting these practices establishes a strong security baseline for SageMaker-based ML workloads and helps meet common regulatory requirements.

Links and references

* [AWS KMS](https://aws.amazon.com/kms/)
* [AWS IAM](https://aws.amazon.com/iam/)
* [AWS CloudTrail](https://aws.amazon.com/cloudtrail/)
* [Amazon VPC](https://aws.amazon.com/vpc/)
* [AWS Config](https://aws.amazon.com/config/)
* [AWS Shield](https://aws.amazon.com/shield/)
* [SageMaker Neo](https://aws.amazon.com/machine-learning/sagemaker/neo/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/e07ceb86-4976-4c8e-a6f8-3518534ec115/lesson/92d5b34c-e617-45e7-a653-00f98166ba1c)
