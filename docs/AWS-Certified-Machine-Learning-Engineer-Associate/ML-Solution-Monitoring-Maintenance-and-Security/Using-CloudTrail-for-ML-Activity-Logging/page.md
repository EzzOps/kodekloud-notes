# Using CloudTrail for ML Activity Logging

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Solution-Monitoring-Maintenance-and-Security/Using-CloudTrail-for-ML-Activity-Logging/page

Using AWS CloudTrail with S3, Athena, CloudWatch, EventBridge and Lambda to log, monitor, analyze, secure, and automate ML activity such as Amazon SageMaker

This guide shows how to use AWS CloudTrail to log, monitor, and act on machine-learning (ML) activity across your AWS environment. Comprehensive CloudTrail logging is essential for security, operational troubleshooting, resource tracking, and compliance when running ML workloads such as Amazon SageMaker.

AWS CloudTrail records API activity for services like Amazon SageMaker and delivers logs to Amazon S3. Those logs can be queried with Amazon Athena, monitored with Amazon CloudWatch, and evaluated by Amazon EventBridge to trigger alerts or automated responses. Together these services give you the visibility and tooling you need to detect suspicious behavior, investigate incidents, and meet regulatory requirements.

Why use CloudTrail for ML activity?

* Produce a complete audit trail of SageMaker and other AWS API activity.
* Retain and protect logs to help meet compliance frameworks (HIPAA, GDPR, PCI).
* Detect unusual or unauthorized API calls for security monitoring.
* Support troubleshooting and post-incident forensics.

<Frame>
  <img alt="The image lists three reasons to use CloudTrail for ML activity logging: providing an audit trail for SageMaker actions, supporting compliance with regulations like HIPAA and GDPR, and enabling security monitoring." />
</Frame>

CloudTrail is indispensable for root-cause analysis when ML pipelines fail—whether due to failed deployments, a spike in failed API calls, unauthorized configuration changes, or edge-device anomalies.

<Frame>
  <img alt="The image presents four reasons to use CloudTrail for ML activity logging: providing an audit trail, supporting compliance, enabling security monitoring, and aiding in troubleshooting." />
</Frame>

Key services typically combined for ML activity logging

| Service            | Role in ML logging                                                | Reference                                                                                                                                                                |
| ------------------ | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AWS CloudTrail     | Capture API calls and user activity across accounts               | [https://docs.aws.amazon.[SECRET_REDACTED]-user-guide.html](https://docs.aws.amazon.[SECRET_REDACTED]-user-guide.html) |
| Amazon S3          | Durable, encrypted storage for raw CloudTrail logs                | [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)                                                                                                                 |
| Amazon Athena      | SQL queries against logs in S3 for ad-hoc forensics and reporting | [https://aws.amazon.com/athena/](https://aws.amazon.com/athena/)                                                                                                         |
| Amazon CloudWatch  | Extract metrics, build dashboards, and create alarms              | [https://aws.amazon.com/cloudwatch/](https://aws.amazon.com/cloudwatch/)                                                                                                 |
| Amazon EventBridge | Pattern matching and routing of events for automation             | [https://aws.amazon.com/eventbridge/](https://aws.amazon.com/eventbridge/)                                                                                               |
| AWS Lambda         | Execute automated remediation or orchestration actions            | [https://aws.amazon.com/lambda/](https://aws.amazon.com/lambda/)                                                                                                         |

<Frame>
  <img alt="The image displays four AWS tools for ML activity logging: AWS CloudTrail, Amazon CloudWatch, Amazon Athena, and Amazon S3, each with a brief description of their function." />
</Frame>

Architecture overview

A simple end-to-end workflow:

1. SageMaker (and other AWS services) emits API calls.
2. AWS CloudTrail records those events.
3. CloudTrail delivers log files to an S3 bucket for secure storage.
4. CloudWatch and EventBridge consume events for monitoring or automation.
5. Athena queries S3-stored logs for forensic and operational analysis.

<Frame>
  <img alt="The image shows a flow diagram for setting up CloudTrail for ML activity logging, involving SageMaker, AWS CloudTrail, and Amazon S3." />
</Frame>

Monitoring and alerting

* Send CloudTrail events to CloudWatch Logs so you can create metric filters and dashboards.
* Use EventBridge rules to match suspicious patterns and route to SNS, Lambda, or other targets.
* Typical alerts: anomalous access, spikes in failed API calls, sudden increases in latency, or unexpected configuration changes.

<Frame>
  <img alt="The image outlines a process for monitoring CloudTrail logs using CloudWatch, illustrating a sequence of CloudTrail Logs, CloudWatch, and Alarm/Notification, and highlighting issues like suspicious access, failed API calls, and latency issues." />
</Frame>

Athena for analysis and forensics

Point Amazon Athena at CloudTrail logs in S3 to run SQL queries that answer questions such as:

* Who invoked a given SageMaker endpoint and when?
* What IP addresses were used to access management APIs?
* Which model served a given request on a multi-model endpoint?

Example Athena query to find recent InvokeEndpoint calls for a specific endpoint:

```sql theme={null}
SELECT eventTime, userIdentity.userName, sourceIPAddress, requestParameters
FROM cloudtrail_logs
WHERE eventName = 'InvokeEndpoint'
  AND requestParameters LIKE '%EndpointName\":\"my-endpoint\"%'
ORDER BY eventTime DESC
LIMIT 100;
```

<Frame>
  <img alt="The image illustrates a flowchart outlining how CloudTrail logs are analyzed using AWS Athena, starting with S3 (CloudTrail Logs), moving through the Athena Query Engine, and resulting in Query Results/Insights." />
</Frame>

Automation and incident response

Route CloudTrail events through EventBridge to Lambda for automated remediation. Example use cases:

* A rule detects a compromised endpoint and invokes a Lambda to isolate it (update security groups, remove endpoint).
* A detected drift in configuration triggers a CodePipeline job to rollback or redeploy.
* Re-training jobs are queued automatically when data-access anomalies are detected.

<Frame>
  <img alt="The image illustrates a process for mitigating issues using CI/CD and Lambda with a flow from a CloudTrail Event to a Lambda Function, followed by a CodePipeline/Auto Action, indicating automation of retraining." />
</Frame>

Infrastructure-as-code (IaC)

Provision and maintain CloudTrail and supporting resources with IaC (CloudFormation, AWS CDK, or Terraform). Your IaC templates should create and enforce:

* CloudTrail trail(s) that capture management and chosen data events.
* CloudWatch Log groups with metric filters and dashboards.
* An S3 bucket with server-side encryption (SSE-KMS), lifecycle rules, and strict access policies.
* IAM roles and KMS keys scoped to least privilege.
* EventBridge rules and Lambda functions for automated responses.

<Frame>
  <img alt="The image is a flowchart illustrating &#x22;Infrastructure as Code for CloudTrail&#x22; using CloudFormation/CDK, connecting to CloudTrail, CloudWatch, and an S3 Log Bucket." />
</Frame>

SageMaker specifics: InvokeEndpoint and multi-model endpoints

CloudTrail logs SageMaker InvokeEndpoint API calls. For multi-model endpoints, developers often include a `TargetModel` parameter in request parameters. When CloudTrail records that parameter, Athena queries can identify which model served the request—useful for per-model usage, billing allocation, or incident investigation.

<Frame>
  <img alt="The image illustrates the process of using CloudTrail logs for multi-model endpoints, with Athena queries being employed to identify which model was invoked." />
</Frame>

Edge and IoT devices

CloudTrail also captures AWS API activity generated by edge devices interacting with AWS services. These logs flow into S3 and can be analyzed with Athena to understand edge behavior, troubleshoot failures, and investigate suspicious activity.

<Frame>
  <img alt="The image illustrates the process of using CloudTrail logs for multi-model endpoints, with Athena queries being employed to identify which model was invoked." />
</Frame>

Security, compliance, and log protection

Combine CloudTrail with the following controls to build a secure, compliant logging environment:

* Deliver logs to an encrypted S3 bucket (enable SSE-KMS).
* Enforce IAM least privilege—use roles and avoid long-lived credentials.
* Use AWS Config to continuously audit resource configuration and detect drift.
* Trigger alerts on non-compliance and use Lambda for automated remediation (e.g., revert risky changes).
* Use S3 features like bucket policies, object lock, and MFA Delete when required by policy.

<Frame>
  <img alt="The image illustrates a flowchart for security and compliance with AWS CloudTrail, detailing processes involving log storage, encryption, roles and policies, alerting mechanisms, compliance checks, and automated remediation using AWS services like CloudTrail, S3, IAM, Lambda, and Config." />
</Frame>

<Callout icon="lightbulb">
  Always enable server-side encryption (SSE-KMS) on the S3 bucket that stores CloudTrail logs. Grant access using IAM roles scoped to least privilege. Consider S3 bucket policies, object lock, and MFA Delete when compliance requires immutability and stronger protection.
</Callout>

Cost optimization

Apply S3 lifecycle policies to manage storage costs:

* Keep recent logs in S3 Standard for fast access.
* Transition older logs to S3 Glacier or Glacier Deep Archive for long-term retention.
* Delete or archive logs only after meeting your compliance retention requirements.

Anti-patterns to avoid

* Not enabling CloudTrail or leaving gaps for SageMaker and other critical services.
* Leaving logs in standard storage indefinitely without lifecycle rules.
* Ignoring alerts—unseen notifications can allow incidents to escalate.
* Hard-coding IAM credentials or using overly permissive roles without periodic audits.

Recommended action checklist

* Enable CloudTrail to capture all SageMaker and relevant API activity.
* Deliver logs to an encrypted S3 bucket and apply lifecycle policies to archive older logs.
* Use CloudWatch metric filters and alarms for anomalous activity.
* Use Athena to run queries for forensic analysis and operational investigations.
* Automate incident responses with EventBridge + Lambda + CI/CD where appropriate (e.g., retrain a model or isolate a compromised endpoint).
* Enforce IAM least privilege, use KMS for key management, require TLS in transit, and isolate resources in VPCs when necessary.
* Optimize costs by retaining only required logs and archiving old data per retention policies.

<Frame>
  <img alt="The image outlines summary and action items related to cloud services, including enabling CloudTrail, delivering logs to S3, monitoring with CloudWatch, using Athena for queries, and automating responses." />
</Frame>

<Frame>
  <img alt="The image outlines two action items: securing systems using IAM, KMS encryption, and VPC isolation, and optimizing costs by managing logs, archiving data, and monitoring retention." />
</Frame>

Further reading and references

* AWS CloudTrail User Guide: [https://docs.aws.amazon.[SECRET_REDACTED]-user-guide.html](https://docs.aws.amazon.[SECRET_REDACTED]-user-guide.html)
* Amazon SageMaker: [https://aws.amazon.com/sagemaker/](https://aws.amazon.com/sagemaker/)
* Amazon S3 storage classes and lifecycle: [https://aws.amazon.com/s3/storage-classes/](https://aws.amazon.com/s3/storage-classes/)
* Amazon Athena: [https://aws.amazon.com/athena/](https://aws.amazon.com/athena/)
* Amazon CloudWatch: [https://aws.amazon.com/cloudwatch/](https://aws.amazon.com/cloudwatch/)
* Amazon EventBridge: [https://aws.amazon.com/eventbridge/](https://aws.amazon.com/eventbridge/)
* AWS Lambda: [https://aws.amazon.com/lambda/](https://aws.amazon.com/lambda/)
* AWS KMS: [https://aws.amazon.com/kms/](https://aws.amazon.com/kms/)
* AWS Config: [https://aws.amazon.com/config/](https://aws.amazon.com/config/)

Use this guide as a baseline for implementing a secure, auditable, and cost-effective ML logging strategy using CloudTrail and the AWS analytics and monitoring ecosystem.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/e07ceb86-4976-4c8e-a6f8-3518534ec115/lesson/5be73b7b-5a79-4b22-8925-fafcd8c9a19b" />
</CardGroup>
