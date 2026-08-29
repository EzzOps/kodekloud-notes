# IAM Roles Policies and Groups for ML Services

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Solution-Monitoring-Maintenance-and-Security/IAM-Roles-Policies-and-Groups-for-ML-Services/page

Managing IAM roles, policies, and groups to secure AWS machine learning workflows like SageMaker with least privilege, monitoring via CloudTrail, and encryption with KMS

In this lesson you’ll learn how to manage access and permissions for machine learning (ML) workloads on AWS. We cover essential IAM concepts—roles, policies, and groups—and show how they apply to Amazon SageMaker and supporting services (for example, CloudWatch for logging). All access control for SageMaker and other AWS services is managed centrally through AWS IAM so your ML pipelines operate securely and with least-privilege.

<Frame>
  <img alt="The image illustrates the role of IAM (Identity and Access Management) in ML (Machine Learning) services, highlighting how IAM control connects ML users and services to secure resource access." />
</Frame>

## Why identity and access management is critical for ML

* Ensures that only authorized users and applications access sensitive datasets, models, and artifacts—minimizing data leaks and model theft.
* Enforces compliance and governance across teams and environments (audit trails, separation of duties).
* Enables a least-privilege security model so every principal has only the permissions required to perform its tasks.

<Frame>
  <img alt="The image outlines four reasons for using IAM for ML services: only authorized access, no accidental leaks, compliance enforced, and least-privilege security." />
</Frame>

## Core IAM components used to secure ML workflows

Use the table below as a quick reference for IAM building blocks and common ML use-cases.

| Resource Type | What it is                                                           | Typical ML use-case                                            |
| ------------- | -------------------------------------------------------------------- | -------------------------------------------------------------- |
| Users         | Individual people or service identities                              | Interactive access for data scientists or CI users             |
| Groups        | Collections of users for centralized management                      | Apply team-wide permissions (e.g., `ml-data-science`)          |
| Roles         | Identities assumed by services or users to get temporary credentials | SageMaker training jobs, endpoints, or batch inference         |
| Policies      | JSON documents that explicitly allow or deny actions on resources    | Grant S3 access for datasets, CloudWatch logging, or ECR pulls |

<Frame>
  <img alt="The image displays icons representing AWS IAM components for ML services: Users, Groups, Roles, and Policies. Each component is accompanied by a colorful circular icon." />
</Frame>

## Configuring IAM roles for SageMaker

SageMaker requires an IAM role to perform actions on your behalf—reading training data from S3, writing logs to CloudWatch, or pulling container images from ECR. A SageMaker execution role has two main parts:

* A trust policy that allows the SageMaker service (or other principals) to assume the role.
* One or more permission policies that define allowed actions on AWS resources.

Example: minimal trust policy allowing SageMaker to assume the role:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "sagemaker.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Example: permission policy granting read access to a specific S3 bucket and write access to CloudWatch logs:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::example-training-bucket",
        "arn:aws:s3:::example-training-bucket/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

> **lightbulb** When creating SageMaker roles, scope S3 access to specific buckets and prefixes instead of using `*`. Use separate roles for different environments (dev, staging, prod) to reduce blast radius.

<Frame>
  <img alt="The image illustrates the configuration of IAM roles for machine learning services, showing the interaction between SageMaker Service, IAM Role, and S3 Training Data. It highlights the setup involving trust and permissions policies." />
</Frame>

## Managing permissions: patterns and workflow

Typical team/service permission workflow:

1. Define the minimal permissions required in IAM policies.
2. Attach those policies to roles (for services/automated jobs) or to groups (for human users).
3. Any principal that assumes a role or is in a group inherits the attached permissions.

This pattern simplifies audits and policy updates: change the policy once, and all associated roles or group members get the updated permissions.

<Frame>
  <img alt="The image illustrates a process for creating IAM policies for ML services, showing steps from defining an IAM policy to assigning a role/group and granting access." />
</Frame>

## Example: group-based workflow for ML teams

* Create a group representing the team (for example, `ml-data-science`).
* Add users to that group.
* Attach policies to the group to grant access to S3, Lambda, EC2, SageMaker, etc.
* All members inherit the group policies, making permission management scalable and auditable.

<Frame>
  <img alt="The image is a flowchart diagram illustrating the management of IAM (Identity and Access Management) groups for ML (Machine Learning) teams, showing the relationship between IAM groups, users, and policies." />
</Frame>

## IAM considerations for specialized ML scenarios

* Multi-model endpoints: create a dedicated endpoint role with narrowly scoped S3 access (only required buckets/prefixes). This prevents a broad service role from having excessive permissions and isolates endpoint access to the artifacts it needs.

<Frame>
  <img alt="The image is a flowchart illustrating IAM for Multi-Model Endpoints, showing the sequence from &#x22;IAM Policy&#x22; to &#x22;Multi-Model Endpoint Role&#x22; to &#x22;Loads models from S3 securely.&#x22;" />
</Frame>

* Edge deployments: for devices that pull Neo-compiled models from S3, attach a narrowly scoped policy to the device identity (or IoT role) granting only the necessary S3 or IoT permissions. Limiting permissions reduces the blast radius if device credentials are compromised. See SageMaker Neo docs for details: [https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-neo.html](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-neo.html).

<Frame>
  <img alt="The image is a flowchart illustrating IAM for Edge Deployments, showing a flow from an IAM Policy to an Edge Device, and then to Access to Neo-Compiled ML Resource." />
</Frame>

## Monitoring IAM activity with CloudTrail

* Every IAM operation—user sign-in, role assumption, API call—generates events.
* AWS CloudTrail captures these events and records them as logs.
* CloudTrail can deliver logs to Amazon S3 for long-term, tamper-evident storage and enable querying via CloudWatch Logs or Athena.
* Use these logs for auditing, alerting on suspicious behavior, and forensic analysis.

<Frame>
  <img alt="The image illustrates a flowchart for monitoring IAM access using CloudTrail, showing the sequence from IAM Actions to CloudTrail Logs, and then to S3 Storage." />
</Frame>

## Security posture: combine IAM with KMS

For a robust security posture combine IAM with AWS Key Management Service (KMS):

* Encrypt S3 buckets, EBS volumes, and model artifacts with KMS customer-managed keys (CMKs).
* Use IAM policies to control which principals can use or decrypt CMKs.
* This ensures data at rest remains encrypted and unreadable even if stored artifacts are accessed without the proper key permissions.

For EBS details: [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs.html)

## Common IAM anti-patterns to avoid

* Granting overly broad admin privileges when not necessary.
* Attaching policies directly to many individual users instead of using groups/roles.
* Operating without monitoring (no CloudTrail, no alerts), which leaves you blind to misuse.

> **lightbulb** Apply least privilege: scope policies tightly (avoid wildcards), prefer role-based access for services, and manage team access via groups.

## Key takeaways for securing ML workloads

* Use IAM roles for ML services (SageMaker endpoints, training jobs, inference containers) to grant controlled access to resources such as S3 and EC2.
* Apply least-privilege policies: avoid wildcards; scope access to specific buckets, prefixes, or resource ARNs.
* Manage team access at the IAM group level instead of assigning permissions to individual users.
* Continuously monitor access and activity with CloudTrail for auditing and anomaly detection.
* Protect datasets, models, and artifacts with encryption (KMS) plus fine-grained IAM controls.

<Frame>
  <img alt="The image summarizes five best practices for managing machine learning services, including using IAM roles, applying least-privilege policies, managing teams with IAM groups, monitoring access with CloudTrail, and encrypting data with KMS." />
</Frame>

## Links and references

* AWS IAM overview: [https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
* SageMaker documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* CloudTrail user guide: [https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html)
* SageMaker Neo: [https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-neo.html](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-neo.html)
* AWS KMS overview: [https://docs.aws.amazon.com/kms/latest/developerguide/overview.html](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/e07ceb86-4976-4c8e-a6f8-3518534ec115/lesson/60808782-efb0-475d-a785-68d40697c676)
