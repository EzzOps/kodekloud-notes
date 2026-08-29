# Turning up Security on Database Services

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/Migrations-Security/Turning-up-Security-on-Database-Services/page

Guidance on securing AWS managed databases like RDS focusing on IAM, logging and monitoring, Trusted Advisor, and encryption at rest and in transit

In this lesson we review practical security controls and design attributes for securing AWS-managed database services, with emphasis on Amazon RDS and related platform-managed database offerings. We cover responsibilities under the AWS shared responsibility model, centralized logging and monitoring, Trusted Advisor recommendations, and encryption (at rest and in transit) — all of which are core to a secure database posture.

<Frame>
  <img alt="A slide illustrating the AWS shared-responsibility model across Infrastructure (EC2), Container (RDS), and Managed (S3/KMS/DynamoDB) services, with blue blocks for customer responsibilities and orange for AWS. Arrows at the bottom show that moving to managed services reduces customer responsibility and customizability." />
</Frame>

Key takeaway: as you move from self-managed EC2-based databases to platform and fully managed services, your operational surface area shrinks — but IAM, logging/monitoring, and encryption remain essential controls you must implement and maintain.

> **lightbulb** Managed database services reduce operational burden, but you still control access (IAM), auditing (CloudTrail/Config), logging (CloudWatch/S3), and encryption (KMS/TDE/SSL). Treat these as non-optional security foundations.

## Database logs and monitoring

Database engines and RDS produce several types of logs that are vital for troubleshooting and security investigations:

* Error logs (engine-specific),
* General / connection logs,
* Slow query logs,
* Audit logs (where supported by the engine), and
* OS and process metrics (via Enhanced Monitoring).

Where to collect and analyze DB logs:

* RDS Console — quick ad-hoc viewing and downloads.
* Amazon CloudWatch Logs — centralized, near-real-time streaming, alerting, and retention.
* Amazon S3 — long-term archival and large-scale batch analytics.
* Automation / Pipelines — AWS Lambda or third-party collectors to push logs into SIEMs or dashboards.
* AWS CloudTrail & AWS Config — API and configuration auditing for RDS resources themselves.

Log destinations and use cases

| Destination           | Use case / benefits                                 | Example                                                          |
| --------------------- | --------------------------------------------------- | ---------------------------------------------------------------- |
| `RDS Console`         | Ad-hoc inspection, quick downloads                  | Inspect an error log or download a slow-query log from `jeffdb2` |
| `CloudWatch Logs`     | Real-time alerting, retained search, metric filters | Create metric filters for repeated auth failures                 |
| `S3`                  | Long-term retention, batch processing, compliance   | Export logs to S3 with lifecycle rules for archival              |
| `Lambda / SIEM`       | Enrichment, automated parsing, dashboards           | Lambda pushes logs from CloudWatch/S3 into a SIEM                |
| `CloudTrail / Config` | Audit API calls and configuration drift             | Track who altered DB parameter groups or snapshots               |

<Frame>
  <img alt="A screenshot of an RDS console showing the DB instance &#x22;jeffdb2&#x22; Logs tab with two MySQL error log files listed. Each log entry shows last written timestamps, sizes, and &#x22;view&#x22; / &#x22;watch&#x22; buttons." />
</Frame>

Best practices for database logging and monitoring:

* Enable Enhanced Monitoring and Performance Insights (where supported) to capture OS and database-level metrics.
* Publish database logs to Amazon CloudWatch Logs for centralized searching, metric extraction, and alerting.
* Export or snapshot logs to Amazon S3 for long-term retention and compliance; apply lifecycle rules to manage cost.
* Use CloudTrail and AWS Config to detect API actions and configuration changes on DB resources.
* Automate ingestion and analysis (e.g., Lambda -> SIEM / dashboard) for recurring or aggregated security monitoring.

Scenario — retail company analyzing DB logs:

1. Turn on Enhanced Monitoring and Performance Insights to gather metrics and slow-query data.
2. Stream DB logs to CloudWatch Logs for real-time alerts on suspicious patterns (e.g., repeated failed logins).
3. Export logs to S3 (with lifecycle rules to move to Glacier) for long-term retention and compliance audits.
4. Optionally build a Lambda pipeline to parse and forward logs to an external SIEM or dashboard for cross-system correlation.

## Trusted Advisor and RDS recommendations

AWS Trusted Advisor provides automated checks and recommendations across cost, performance, security, fault tolerance, and service limits. For RDS, common recommendations include underutilized instances and configuration suggestions, but Trusted Advisor does not take operational actions for you.

Trusted Advisor overview for RDS:

| Area                 | What Trusted Advisor provides                               | What it does not do                                 |
| -------------------- | ----------------------------------------------------------- | --------------------------------------------------- |
| Cost / Performance   | Identifies underutilized instances, suggestions to downsize | Does not change instance types automatically        |
| Security             | Highlights certain insecure configurations                  | Does not apply patches or enforce changes           |
| Operational guidance | Points to best practice checks                              | Does not provide application code optimization tips |

Example: healthcare company using RDS for patient records — expectations

* Identifies underutilized instances and cost-optimization opportunities — True.
* Does not directly apply OS/database patches — True.
* Will not directly modify RDS instance types — True.
* Will not provide application code-level optimization tips — True.

## Encryption: at rest and in transit

RDS supports both encryption at rest and encryption in transit. Implementation details vary by engine, but the security objectives remain the same: protect data when stored and while it traverses the network.

Encryption at rest

* Enable encryption at DB instance creation by selecting encryption and a KMS key (AWS-managed or a customer-managed CMK). Snapshots, automated backups, and (same-region) read replicas inherit encryption.
* Some engines support database-native TDE (Transparent Data Encryption) — e.g., Oracle and SQL Server. Use TDE when regulatory or platform requirements mandate DB-native encryption.
* For engines such as MySQL, PostgreSQL, and MariaDB, disk encryption (KMS-backed) provides encryption-at-rest.
* You cannot enable encryption on an existing unencrypted RDS instance in-place. The recommended flow is:
  1. Create a snapshot of the unencrypted instance.
  2. Copy the snapshot and enable encryption on the copied snapshot.
  3. Restore a new DB instance from the encrypted snapshot.

> **warning** Encryption at rest must be enabled when creating the DB instance. To convert an existing unencrypted RDS instance to encrypted, snapshot it, copy the snapshot with encryption enabled, then restore a new encrypted instance from that snapshot.

Client-side encryption (encrypting data before sending it to the DB) is an option for defense-in-depth or strict compliance, but it increases complexity (key lifecycle, indexability, application changes). For most workloads, using AWS-managed encryption (KMS/TDE where appropriate) is the recommended approach unless a particular compliance use case requires client-side encryption.

Encryption in transit

* Use SSL/TLS to encrypt client-to-database connections. AWS provides CA-signed RDS certificates that you can validate on the client side.
* Implementation varies by engine and driver — some require connection-string flags, while others can be enforced via DB parameter settings. Always test client libraries and update connection settings to require TLS.
* Remember: KMS/TDE protect data at rest, but do not replace SSL/TLS for protecting traffic in transit.

<Frame>
  <img alt="A certificate chain diagram showing a Root CA issuing to three Intermediate CAs, each providing DB server certificates to individual Amazon RDS instances. It illustrates how RDS uses certificates to encrypt data in transit." />
</Frame>

Scenario — healthtech company ensuring encryption in transit:

* Action: Enable SSL/TLS on RDS instances and configure clients to verify server certificates and require encrypted connections.
* Note: KMS/TDE encrypt data at rest and are complementary to SSL/TLS, not replacements.

## Summary checklist

| Control area          | Recommended actions                                                                                                                                |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Identity & Access     | Use IAM with least privilege for who can manage DB instances and who can connect to data (use IAM DB authentication where supported).              |
| Logging & Monitoring  | Enable Enhanced Monitoring and Performance Insights; stream DB logs to CloudWatch Logs; use CloudTrail and AWS Config for auditing.                |
| Long-term retention   | Archive logs to S3 with lifecycle rules for compliance and cost savings.                                                                           |
| Encryption at rest    | Enable KMS-backed encryption at instance creation; use TDE for engines that support it when required.                                              |
| Encryption in transit | Enforce SSL/TLS for all client connections and validate server certificates.                                                                       |
| Automation & process  | Document and automate procedures (snapshot/copy/restore workflows for encryption conversions, certificate rotation, and log retention lifecycles). |

## Links and references

* AWS RDS documentation: [https://docs.aws.amazon.com/rds/](https://docs.aws.amazon.com/rds/)
* AWS CloudWatch: [https://learn.kodekloud.com/user/courses/aws-cloudwatch](https://learn.kodekloud.com/user/courses/aws-cloudwatch)
* AWS KMS: [https://docs.aws.amazon.com/kms/](https://docs.aws.amazon.com/kms/)
* Amazon S3: [https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* AWS Lambda: [https://learn.kodekloud.com/user/courses/aws-lambda](https://learn.kodekloud.com/user/courses/aws-lambda)
* AWS CloudTrail: [https://docs.aws.amazon.com/cloudtrail/](https://docs.aws.amazon.com/cloudtrail/)
* AWS Config: [https://docs.aws.amazon.com/config/](https://docs.aws.amazon.com/config/)
* Trusted Advisor: [https://aws.amazon.com/premiumsupport/technology/trusted-advisor/](https://aws.amazon.com/premiumsupport/technology/trusted-advisor/)

This lesson covered the essential security controls to "turn up" for RDS and similar managed database services: centralized logging and monitoring, encryption at rest and in transit, and strict IAM and auditing. Implement these consistently to reduce risk and simplify investigations.

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/79ca746d-b567-4dae-92cd-e572992ff80e/lesson/24b90001-3087-41ab-ae9f-df911aecd685)
