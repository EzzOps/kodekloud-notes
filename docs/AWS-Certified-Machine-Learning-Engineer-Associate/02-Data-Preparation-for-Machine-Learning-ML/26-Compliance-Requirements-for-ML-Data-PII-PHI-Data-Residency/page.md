# Compliance Requirements for ML Data PII PHI Data Residency

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Compliance-Requirements-for-ML-Data-PII-PHI-Data-Residency/page

Overview of compliance considerations and AWS tools for protecting sensitive ML data such as PII PHI and financial information, covering residency, access control, encryption, and monitoring.

This lesson describes the core compliance considerations for machine learning (ML) pipelines that process sensitive data. It explains the types of sensitive data (PII, PHI, financial), the consequences of mishandling them, common legal and regulatory frameworks, data residency implications, and AWS services and controls you can apply to help meet compliance obligations.

At a high level, ML pipelines ingest raw data, train models, and produce outputs used in applications or analytics. Because data is the foundation of ML, you must protect it—especially when it includes sensitive information. Typical categories of sensitive data include:

* Personally Identifiable Information (PII)
* Protected Health Information (PHI)
* Financial data

<Frame>
  <img alt="The image outlines critical factors in compliance for machine learning, highlighting PII (names, addresses, social security numbers), PHI (medical records, lab results, patient data), and financial data (credit card numbers, banking details, transaction histories)." />
</Frame>

## Why compliance matters: consequences of mishandling sensitive data

Failure to secure PII, PHI, or financial data can produce severe and lasting consequences:

* Financial penalties: Regulations such as the EU GDPR can impose fines up to 4% of global annual revenue; HIPAA violations also carry significant penalties.
* Legal actions and restrictions: Regulatory investigations, lawsuits, or operational constraints may follow non‑compliance.
* Reputation damage: Loss of customer trust can be costly and long-term.
* Data breaches: Inadequate controls on ML systems can leak sensitive records.
* Ethical risks: Biased models, opaque data usage, or misuse of sensitive data can lead to discriminatory or harmful outcomes.

<Frame>
  <img alt="The image outlines five critical compliance factors in machine learning: fines (GDPR, HIPAA), legal action, reputation damage, data breaches, and ethical risks in AI." />
</Frame>

> **lightbulb** Key compliance focus areas for ML: accurately identify sensitive data (PII/PHI/financial), enforce appropriate data residency, apply encryption and least-privilege access, and maintain robust auditing and logging.

## Sensitive data categories and examples

Below are concise definitions and examples that help guide classification and handling decisions.

PII (personally identifiable information)

* Data that can uniquely identify or be linked to an individual: full name, email, phone number, physical address, date of birth, Social Security number, passport or national ID.
* Technical identifiers and biometrics (IP addresses, device IDs, face scans) are often treated as PII.
* Protect PII to reduce risk of identity theft and misuse in ML training and inference.

<Frame>
  <img alt="The image displays a list of personally identifiable information (PII) for a fictional person, including name, email, phone number, and address. It also includes technical identifiers like IP address and biometric data." />
</Frame>

PHI (protected health information)

* Health-related personal data, including diagnoses, prescriptions, lab results, insurance identifiers, medical record numbers, and treatment/visit histories.
* PHI is tightly regulated (for example, by HIPAA in the United States); special handling and contractual protections are usually required.

<Frame>
  <img alt="The image is an example of Protected Health Information (PHI) that includes details such as a diagnosis of Type 2 Diabetes, a prescription for Metformin 500mg, lab results, health insurance information, visit date, and a medical record number." />
</Frame>

Financial data

* Examples include credit card and bank account numbers, transaction amounts and timestamps, routing numbers, employer and income details, and credit scores.
* Leakage of financial data can enable fraud and direct monetary loss.

<Frame>
  <img alt="The image displays financial information including a credit card number, bank account number, transaction details, routing number, employer income, and credit score." />
</Frame>

## Key regulations and where they apply

Common regulations that often affect ML data handling include:

| Regulation          | Region                    | Primary focus                                                                                       |
| ------------------- | ------------------------- | --------------------------------------------------------------------------------------------------- |
| GDPR                | European Union            | Personal data protection, lawful bases for processing, data subject rights (e.g., right to erasure) |
| HIPAA               | United States             | Protection of PHI; technical, administrative, and physical safeguards for healthcare data           |
| CCPA                | California, US            | Consumer rights over personal information and disclosure requirements for data sales                |
| LGPD                | Brazil                    | Data protection similar to GDPR for Brazil-based data subjects                                      |
| Data residency laws | Various (e.g., EU, India) | Rules requiring certain categories of data to be stored and processed within geographic boundaries  |

<Frame>
  <img alt="The image shows a table of common regulations affecting machine learning across different regions, including GDPR, HIPAA, CCPA, and LGPD, with their respective impacts." />
</Frame>

Many jurisdictions require that certain categories of data remain within defined geographic boundaries. Data residency rules directly affect where you provision storage and compute resources (for example, S3 buckets, RDS instances, or data-processing pipelines).

<Frame>
  <img alt="The image shows a world map highlighting the United States and Alaska in blue, labeled &#x22;HIPAA,&#x22; with a sidebar listing GDPR, HIPAA, CCPA, and LGPD under the title &#x22;Data Residency.&#x22;" />
</Frame>

> **warning** If data residency applies, avoid cross‑region transfers unless legally permitted and necessary. Ensure that backups, logs, and disaster‑recovery replicas also respect residency constraints.

## AWS services and features to help meet compliance

AWS offers many services and controls that support a compliant ML posture. The list below highlights commonly used tools and how they fit into ML workflows:

* AWS Identity and Access Management (IAM): implement least-privilege access using roles and policies.
* Amazon Macie: discovers and classifies PII in S3 buckets using ML and pattern matching.
* AWS Artifact: on-demand access to AWS compliance reports and security documentation to support audits.
* AWS Key Management Service (KMS): centralized key management for encryption at rest, envelope encryption, and client-side encryption scenarios.
* AWS CloudTrail: records API activity across AWS for auditing, forensics, and compliance reporting.

<Frame>
  <img alt="The image depicts a list of AWS compliance tools for ML workflows, which include Amazon IAM, Amazon Macie, AWS Artifact, AWS KMS, and AWS CloudTrail." />
</Frame>

AWS-managed services also provide native security features that, when configured correctly, help meet regulatory requirements:

* Amazon S3: server-side encryption (SSE-KMS), bucket policies, versioning, object lock, replication controls.
* Amazon RDS & DynamoDB: encryption at rest, automated backups, and fine-grained access controls.
* Amazon SageMaker: can be HIPAA-eligible when used under the appropriate Business Associate Addendum (BAA) and with correct configuration.
* AWS KMS: central key policies, key rotation, and audit trails that integrate across services.

<Frame>
  <img alt="The image outlines secure data storage techniques using Amazon services like S3, RDS, and DynamoDB, focusing on encryption, policies, and backups." />
</Frame>

## Access control and monitoring best practices

Strong access controls and monitoring are critical to limiting exposure:

* Implement least privilege via IAM policies and role separation—grant the minimum permissions needed for each task.
* Require multi-factor authentication (MFA) for privileged users.
* Instrument CloudTrail, Amazon GuardDuty, and AWS Config to detect unexpected behavior and configuration drift.
* Centralize logs for analysis and long-term retention (ensure log storage follows residency rules).

<Frame>
  <img alt="The image illustrates a diagram showing a user with access to Amazon S3, Amazon RDS, and Amazon DynamoDB through IAM policies for controlling data access." />
</Frame>

When you require automated detection and prevention, combine policy, monitoring, and automation to reduce exposure and block unauthorized attempts in real time.

<Frame>
  <img alt="The image illustrates a security concept where a malicious user is blocked from accessing Amazon S3, Amazon RDS, and Amazon DynamoDB through IAM policies." />
</Frame>

## Example automated workflow: Amazon Macie + EventBridge + Lambda

A common pattern for automated sensitive-data discovery and remediation:

1. Amazon Macie inspects S3 buckets to detect and classify sensitive objects (PII/PHI).
2. Macie emits findings when it identifies sensitive data.
3. Amazon EventBridge rules receive Macie findings and trigger AWS Lambda functions.
4. Lambda can execute automated remediation: quarantine objects, update bucket policies, tag or move objects, or notify the security/compliance team.
5. Notifications and incident management workflows ensure human review when required.

This pipeline enables rapid, auditable responses to sensitive-data discoveries and supports compliance with GDPR, HIPAA, PCI DSS, NIST, and other frameworks.

<Frame>
  <img alt="The image is a flow diagram illustrating the process of detecting and classifying sensitive data using Amazon Macie, involving Amazon S3, Amazon EventBridge, AWS Lambda, and a notification step." />
</Frame>

## AWS Artifact and compliance evidence

* AWS Artifact provides on-demand access to AWS compliance reports and security documentation (SOC, ISO, PCI, HIPAA guidance, etc.).
* Use Artifact during audits to obtain evidence of AWS’s control posture and to understand shared responsibilities for your ML workloads.

## AWS services and compliance posture (summary)

| AWS Service                  | Compliance considerations / examples                                                                                                                                  |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Amazon S3                    | SSE-KMS, bucket policies, versioning, object lock, replication controls; can be configured to meet GDPR/HIPAA requirements when combined with organizational controls |
| Amazon SageMaker             | HIPAA-eligible when used under a BAA and with correct configurations (VPC, encryption, logging)                                                                       |
| Amazon RDS / Amazon Redshift | Encryption at rest, automated backups, and compliance reports (PCI DSS, HIPAA with contractual arrangements)                                                          |
| AWS KMS                      | Centralized key management, rotation, and audit trails; integrates with storage, database, and ML services                                                            |

## Designing compliant ML pipelines: checklist

* Classify and inventory data: discover sensitive objects early (use Amazon Macie or similar tools).
* Apply data minimization and anonymization techniques where feasible.
* Enforce least privilege for access and isolate workloads using VPCs, IAM roles, and resource policies.
* Encrypt data at rest and in transit; manage keys with AWS KMS and enforce key usage policies.
* Implement logging, monitoring, and automated remediation (CloudTrail, GuardDuty, EventBridge, Lambda).
* Document controls and retain evidence for audits (use AWS Artifact to obtain AWS reports).
* Validate residency and sovereignty requirements for storage, processing, backups, and logs.

Keeping ML pipelines compliant requires a combination of data discovery/classification, controlled access, encryption, automated monitoring/remediation, and documentation. Use the AWS tools and best practices above to design ML systems that meet regulatory and organizational requirements while minimizing risk.

For more detailed guidance and service-specific docs, see:

* [AWS Identity and Access Management (IAM)](https://docs.aws.amazon.com/iam/)
* [Amazon Macie documentation](https://docs.aws.amazon.com/macie/)
* [AWS Key Management Service (KMS)](https://docs.aws.amazon.com/kms/)
* [AWS Artifact](https://aws.amazon.com/artifact/)
* [AWS CloudTrail](https://docs.aws.amazon.com/cloudtrail/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/fbd06f87-4da2-4c9e-96c0-2ad557a4187c)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/63f59cfb-851f-43f1-a2d3-dc591e2f7c84)
