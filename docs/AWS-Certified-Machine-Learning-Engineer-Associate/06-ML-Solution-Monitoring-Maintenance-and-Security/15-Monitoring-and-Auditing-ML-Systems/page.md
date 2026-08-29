# Create a thing representing the edge device
iot.create_thing(
    thingName='FraudDetectorDevice',
    thingTypeName='EdgeMLDevice'
)

# Create a job that targets the thing and references a job document stored in S3
iot.create_job(
    jobId='update-fraud-model',
    targets=['arn:aws:iot:us-east-1:123456789012:thing/FraudDetectorDevice'],
    documentSource='s3://ml-bucket/neo-output/fraud-detector-neo.tar.gz'
)
```

The `documentSource` S3 URI references the job document containing device update instructions and artifacts. For full details on IoT jobs and device management, see the [AWS IoT documentation](https://docs.aws.amazon.com/iot/latest/developerguide/).

Security and compliance in anomaly monitoring

Best practices:

* Aggregate logs and metrics from databases, servers, and cloud services to a secure central store.
* Run detection engines and evaluate findings against compliance rules.
* Trigger incident workflows when anomalies are confirmed and persist evidence for audit.
* Secure stored data (encryption at rest and in transit) and maintain immutable logs for forensic analysis.
* Use historical findings to refine runbooks and incident playbooks.

<Frame>
  <img alt="The image is a flowchart illustrating &#x22;Security and Compliance in Anomaly Monitoring,&#x22; showing processes like anomaly detection, compliance verification, alerting, incident response, secure data storage, and reporting." />
</Frame>

Cost optimization via anomaly monitoring

Anomaly monitoring can reveal unexpected usage and inefficiencies. Dashboards can surface cost trends, flag cost anomalies, and quantify savings from remediation actions. The example below highlights both savings and improved mean response time.

<Frame>
  <img alt="The image is a dashboard displaying cost optimization through anomaly monitoring, featuring graphs and metrics like total savings, anomalies detected, and average response time." />
</Frame>

In this example, optimized monitoring produced \$24,500 in savings and reduced mean anomaly response time to 1.8 hours.

Anti-patterns to avoid

Common pitfalls:

* Alert fatigue due to excessive false positives
* Unmonitored gaps where anomalies go unnoticed
* Siloed detections that hinder root-cause analysis
* Poorly calibrated thresholds that cause missed incidents or noise
* Alerts that lack actionable remediation steps

<Callout icon="warning">
  Avoid alert fatigue by tuning detection thresholds, deduplicating noisy alerts, and ensuring every alert maps to a runbook or automated remediation.
</Callout>

<Frame>
  <img alt="The image lists anti-patterns to avoid in anomaly detection, including alert fatigue from false positives, unmonitored gaps, siloed detections, poor threshold calibration, and lack of actionable responses. It features a circular diagram with icons for each anti-pattern." />
</Frame>

Key takeaways

* Use native AWS tools (CloudWatch, SageMaker, Lambda, CodePipeline) for end-to-end anomaly monitoring and automated responses.
* Monitor all MLOps phases: data ingestion, preprocessing, training, validation, registry, and deployment (including multi-model and edge endpoints).
* Automate alerts and remediation to reduce manual work and improve MTTR.
* Deploy monitoring consistently across accounts/regions using IaC (CloudFormation & StackSets).
* Integrate anomaly detection with Auto Scaling and cost management to optimize resources.
* Ensure security and compliance via encrypted storage, audit reporting, and a clear incident response process.
* Proactively avoid alert fatigue, coverage gaps, and poor threshold calibration.

<Frame>
  <img alt="The image is a summary slide outlining the use of AWS tools for monitoring, covering phases such as data ingestion and model deployment, automating alerts, and deploying monitoring across regions." />
</Frame>

Further reading and references

* [Amazon CloudWatch](https://docs.aws.amazon.com/cloudwatch/)
* [SageMaker Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html)
* [SageMaker Clarify](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify.html)
* [AWS CodePipeline](https://docs.aws.amazon.com/codepipeline/)
* [AWS Lambda](https://docs.aws.amazon.com/lambda/)
* [AWS IoT Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html)
* [CloudFormation StackSets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html)

<Callout icon="lightbulb">
  Design monitoring as a feedback loop: detect → analyze → remediate → learn. Automate where possible and keep humans focused on high-impact investigations.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/e07ceb86-4976-4c8e-a6f8-3518534ec115/lesson/c7228f7f-76e5-4da1-a9c2-33180c8eafd0" />
</CardGroup>


# Monitoring and Auditing ML Systems

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Solution-Monitoring-Maintenance-and-Security/Monitoring-and-Auditing-ML-Systems/page

Monitoring and auditing production ML systems on AWS using CloudWatch, CloudTrail, SageMaker Model Monitor, AWS Config, IAM and KMS to detect drift, ensure observability, security, and compliance

In this lesson we cover a critical post-deployment phase of MLOps: monitoring and auditing machine learning systems so they remain reliable, secure, and compliant in production.

Monitoring focuses on runtime observability—metrics, logs, and alerts—while auditing provides an immutable record of actions and configuration changes that supports accountability and compliance. In AWS, common building blocks for these capabilities are CloudWatch for telemetry and CloudTrail for API audit trails, often combined with SageMaker Model Monitor and AWS Config for model-specific monitoring and compliance checks.

<Callout icon="lightbulb">
  Monitoring gives you runtime visibility to detect and respond to issues quickly; auditing preserves a historical record required for investigations, governance, and compliance.
</Callout>

<Frame>
  <img alt="The image is about monitoring and auditing ML systems using AWS CloudWatch to check system health and performance, and AWS CloudTrail to record actions for accountability and compliance." />
</Frame>

## Why monitor and audit ML systems?

Consider the full ML lifecycle: training pipelines, model artifacts, and inference endpoints. Continuous monitoring and auditing enable you to:

* Detect runtime issues (e.g., latency spikes, increased error rates).
* Detect data and concept drift that degrade model performance.
* Maintain a verifiable history of who did what and when for compliance, debugging, and reproducibility.
* Automate incident workflows to reduce mean time to detection and recovery.

To implement these capabilities on AWS, combine services designed for observability, model quality, and governance.

<Frame>
  <img alt="The image is a flowchart explaining the importance of monitoring and auditing machine learning systems, highlighting tools like CloudWatch, Model Monitor, and CloudTrail to ensure reliable and compliant ML." />
</Frame>

## Key AWS services and their roles

| Service                 |                                                                                                                                Role in ML monitoring & auditing | Useful links                                                                                                                             |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------: | ---------------------------------------------------------------------------------------------------------------------------------------- |
| AWS CloudWatch          | Collects metrics and logs from ML infrastructure and applications; supports alarms, dashboards, anomaly detection, and EventBridge integrations for automation. | [https://aws.amazon.com/cloudwatch/](https://aws.amazon.com/cloudwatch/)                                                                 |
| AWS CloudTrail          |                                           Records management- and data-plane API calls for a complete audit trail of actions and events across the AWS account. | [https://aws.amazon.com/cloudtrail/](https://aws.amazon.com/cloudtrail/)                                                                 |
| AWS Config              |                                         Continuously records resource configurations and evaluates them against rules for compliance reporting and remediation. | [https://aws.amazon.com/config/](https://aws.amazon.com/config/)                                                                         |
| SageMaker Model Monitor |                                    Captures inference data, establishes baselines, and detects distribution drift, schema violations, and model quality issues. | [https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html) |

<Frame>
  <img alt="The image lists AWS tools for monitoring and auditing ML systems, including AWS CloudWatch, AWS CloudTrail, AWS Config, and SageMaker Model Monitor." />
</Frame>

## Monitoring with CloudWatch (runtime telemetry)

A typical runtime monitoring flow:

1. Your ML endpoint (for example, a SageMaker endpoint) emits metrics—latency, request counts, error counts—and streams logs.
2. CloudWatch ingests those metrics and logs.
3. You define alarms (threshold or anomaly-based), dashboards, and automated responses using EventBridge and Lambda to handle incidents.

What to monitor (examples):

| Category      | Metrics to track                                              |
| ------------- | ------------------------------------------------------------- |
| Latency       | P50 / P95 / P99 latency percentiles                           |
| Errors        | Error rates, HTTP 4xx/5xx breakdown                           |
| Throughput    | Request volume, requests/sec                                  |
| Resources     | CPU, memory, GPU utilization of serving instances             |
| Model quality | Runtime-calculated quality metrics or custom inference scores |

When an alarm fires, route it to an incident playbook: create a ticket, trigger auto-scaling, block suspicious traffic, or route captured data to a drift analysis pipeline.

<Frame>
  <img alt="The image illustrates the process of monitoring machine learning systems with CloudWatch, showing the flow from an ML endpoint via SageMaker to CloudWatch, which then tracks metrics and alarms for latency and errors." />
</Frame>

## Detecting data drift with SageMaker Model Monitor

SageMaker Model Monitor helps you detect changes in input feature distributions and schema deviations by comparing production inference data to a baseline derived from training data.

Typical implementation steps:

1. Create a baseline from training data (or a validated representative sample).
2. Enable data capture on the endpoint or configure scheduled batch captures.
3. Configure Model Monitor jobs and alerts for distribution drift, missing values, and schema mismatches.
4. Feed Model Monitor reports and metrics into CloudWatch and your incident pipeline.
5. Investigate drift: decide whether to retrain, rollback, or correct upstream data issues.

This automation allows you to detect gradual or sudden drift and integrate the findings into retraining or data-quality workflows.

<Frame>
  <img alt="The image illustrates a process for detecting data drift using SageMaker Model Monitor, showing a flow from &#x22;Training Data Baseline&#x22; to &#x22;SageMaker Model Monitor&#x22; with accompanying icons." />
</Frame>

## Auditing with CloudTrail

CloudTrail records API activity (management and data-plane) and stores events in an S3 bucket (optionally encrypted). Those logs are searchable and analyzable with Athena, CloudWatch Logs Insights, or a SIEM.

Common audit use cases:

* Identify who deployed or updated a model artifact and when.
* Determine which principal invoked an endpoint at a specific time.
* Track changes to IAM policies and who authorized them.

Use the audit trail to produce compliance reports, conduct post-incident forensics, and prove reproducibility.

<Frame>
  <img alt="The image illustrates the process of auditing machine learning systems using CloudTrail, showing the flow from ML API calls to CloudTrail Logs and finally to an audit report using Athena/CloudWatch." />
</Frame>

## Security and compliance best practices

Adopt layered controls to protect telemetry, model artifacts, and audit evidence:

* IAM: enforce least privilege and use service roles instead of long-lived credentials when possible.
* KMS: encrypt logs, model artifacts, and captured data at rest using AWS KMS keys with strict key policies and rotation.
* AWS Config: continuously evaluate resource configurations against organizational rules (for example, CloudTrail enabled, S3 buckets encrypted, endpoints in approved VPC subnets).
* Logging integrity: ensure CloudTrail and CloudWatch logs are centralized, immutable, and protected from tampering.

These controls not only secure telemetry and artifacts but also provide the governance necessary for audits and investigations.

<Frame>
  <img alt="The image depicts a flow diagram illustrating security and compliance for monitoring and auditing using IAM for access control, KMS for encryption of logs/data, and AWS Config for compliance checks." />
</Frame>

<Callout icon="warning">
  Avoid these anti-patterns. They undermine observability, security, and compliance and make debugging or audits much harder.
</Callout>

## Anti-patterns to avoid

* No monitoring at all — you won’t be alerted when production degrades.
* Ignoring model and data drift — models degrade over time without detection.
* Not enabling CloudTrail — you lose the forensic history needed for investigations.
* Overly permissive IAM for monitoring — increases blast radius and insider risk.

Avoiding these anti-patterns preserves reliability and reduces security and compliance exposure.

<Frame>
  <img alt="The image lists four anti-patterns to avoid: no monitoring enabled, ignoring model/data drift, not enabling CloudTrail (no audit), and over-permissive IAM for monitoring." />
</Frame>

## Summary

* CloudWatch provides runtime telemetry, alarms, and dashboards for operational monitoring.
* SageMaker Model Monitor detects data and concept drift and reports model quality issues.
* CloudTrail records API activity to create an auditable history of actions.
* AWS Config enforces and reports on resource configuration compliance.
* IAM and KMS form the foundation for secure access control and encryption of telemetry and artifacts.

Use these components together to build a robust monitoring and auditing posture for production ML systems.

<Frame>
  <img alt="The image is a summary slide listing five cloud services: CloudWatch, Model Monitor, CloudTrail, Config, and IAM + KMS, each with a brief description of their function." />
</Frame>

## Links and references

* AWS CloudWatch — [https://aws.amazon.com/cloudwatch/](https://aws.amazon.com/cloudwatch/)
* AWS CloudTrail — [https://aws.amazon.com/cloudtrail/](https://aws.amazon.com/cloudtrail/)
* AWS Config — [https://aws.amazon.com/config/](https://aws.amazon.com/config/)
* SageMaker Model Monitor — [https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html)
* Amazon Athena — [https://aws.amazon.com/athena/](https://aws.amazon.com/athena/)
* AWS KMS — [https://aws.amazon.com/kms/](https://aws.amazon.com/kms/)
* AWS IAM — [https://aws.amazon.com/iam/](https://aws.amazon.com/iam/)

Further reading: combine CloudWatch alarms, EventBridge rules, and Lambda automation with Model Monitor reports to create closed-loop pipelines that trigger retraining or sandboxed investigations when drift or anomalies are detected.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/e07ceb86-4976-4c8e-a6f8-3518534ec115/lesson/72f706ca-a363-4eda-afbe-d4b3af47c6c2" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/e07ceb86-4976-4c8e-a6f8-3518534ec115/lesson/e7386c83-0542-43df-99c4-b0148fc85fbd" />
</CardGroup>
