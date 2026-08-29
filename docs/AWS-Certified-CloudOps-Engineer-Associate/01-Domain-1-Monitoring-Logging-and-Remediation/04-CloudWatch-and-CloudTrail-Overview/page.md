# CloudWatch and CloudTrail Overview

Source: https://notes.kodekloud.com/docs/AWS-Certified-CloudOps-Engineer-Associate/Domain-1-Monitoring-Logging-and-Remediation/CloudWatch-and-CloudTrail-Overview/page

This article provides an overview of AWS services CloudWatch and CloudTrail for monitoring, auditing, and ensuring the health of your AWS environment.

Welcome to this comprehensive guide on two essential AWS services: CloudWatch and CloudTrail. These services play a pivotal role in monitoring, auditing, and ensuring the overall health of your AWS environment. In this article, you will learn how CloudWatch offers in-depth observability of your resources, while CloudTrail provides a detailed audit trail of all API activities within your account.

## CloudWatch Overview

CloudWatch is a powerful monitoring service designed to collect and track metrics, logs, traces, and synthetic tests from AWS resources and on-premises applications. It acts as your centralized monitoring hub, ensuring that you maintain complete visibility over both your cloud and hybrid environments.

You can use CloudWatch to:

* Monitor system health and performance across AWS and on-premises resources.
* Collect various metrics including CPU usage, load average, disk I/O, network bandwidth, and burst credits.
* Configure alarms with set thresholds (e.g., alert when CPU usage exceeds 85%) and automatically trigger notifications via the Simple Notification Service (SNS).

<Frame>
  ![The image illustrates the working of AWS CloudWatch, showing how it collects metrics from AWS Cloud, custom applications, and on-premises logs, and then triggers alarms that are sent to SNS (Simple Notification Service).](../../../../images/kodekloud.com/kk-media/image/upload/v1752859850/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-CloudWatch-and-CloudTrail-Overview/aws-cloudwatch-metrics-illustration.jpg)
</Frame>

CloudWatch also enables you to analyze trends over time through:

* Trending graphs of key metrics.
* Log insights for querying and analyzing log streams.
* Tracing capabilities for modern observability across distributed systems.

<Frame>
  ![The image illustrates the working of AWS CloudWatch, showing how it collects metrics from AWS Cloud, custom applications, and on-premises logs, and then uses alarms and metrics insights to interact with SNS and a management console.](../../../../images/kodekloud.com/kk-media/image/upload/v1752859851/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-CloudWatch-and-CloudTrail-Overview/aws-cloudwatch-metrics-illustration-2.jpg)
</Frame>

### Key Components of CloudWatch

CloudWatch comprises several subservices that work together to provide comprehensive monitoring:

* **Metrics:** Collect data with specific namespaces, dimensions, and resolutions (for example, CPU metrics can be reported every 30 seconds or every minute).
* **Alarms:** Define thresholds and automatically trigger actions when those thresholds are breached.
* **Logs:** Organize log streams into groups (such as by application or service) and use Log Insights for detailed analysis.
* **Events:** Process AWS or third-party events using custom rules that trigger specific targets.
* **Dashboards:** Create visualizations like pie charts, line charts, and historical trend graphs.
* **Additional features:** Leverage Synthetics, real-time user metrics, Container Insights, Serverless Insights, Service Mapping, and more.

<Frame>
  ![The image is a diagram of CloudWatch components, including Metrics, Alarms, Logs, Events, Dashboards, and Insights, with subcategories listed under each component.](../../../../images/kodekloud.com/kk-media/image/upload/v1752859852/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-CloudWatch-and-CloudTrail-Overview/cloudwatch-components-diagram.jpg)
</Frame>

For example, when you launch an [EC2 instance](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2), it can automatically send default metrics to CloudWatch. For enhanced monitoring, you can install an agent on your [EC2 instance](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2) (or any system like Windows, macOS, or Linux) to collect more granular data. CloudWatch can then trigger automated responses such as initiating Auto Scaling to add additional [EC2 instances](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2) when necessary.

<Frame>
  ![The image is a flow diagram showing an example of Amazon CloudWatch integration, with Amazon EC2 feeding into CloudWatch, which then connects to Autoscaling.](../../../../images/kodekloud.com/kk-media/image/upload/v1752859856/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-CloudWatch-and-CloudTrail-Overview/amazon-cloudwatch-ec2-autoscaling-diagram.jpg)
</Frame>

<Callout icon="lightbulb">
  CloudWatch not only collects and analyzes built-in metrics but also allows you to:

  * Submit custom application metrics.
  * Set alarms to automate response actions.
  * Build detailed dashboards for containerized, serverless, and other service-specific insights.
</Callout>

## CloudTrail Overview

While CloudWatch focuses on real-time operational monitoring, CloudTrail specializes in recording API calls to deliver a detailed audit log of activities within your AWS account. This is critical for security analysis, compliance, and troubleshooting. CloudTrail tracks:

* API calls made via the AWS CLI, SDKs, and Console actions.
* API events associated with managed services, such as those from Systems Manager.
* Changes to your AWS infrastructure, like launching or stopping an [EC2 instance](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2) or updating an [RDS instance](https://learn.kodekloud.com/user/courses/aws-rds).

CloudTrail logs enable you to export data to [Amazon S3](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3) for long-term analysis, or analyze logs directly using CloudWatch Logs and Log Insights—ideal for compliance and forensic investigations.

<Frame>
  ![The image is a diagram illustrating AWS CloudTrail's process of capturing API calls and account activity from various AWS services, storing the logs in Amazon S3 for analysis and auditing.](../../../../images/kodekloud.com/kk-media/image/upload/v1752859858/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-CloudWatch-and-CloudTrail-Overview/aws-cloudtrail-api-calls-diagram.jpg)
</Frame>

CloudTrail can be accessed via the AWS Management Console, CLI, or SDKs and requires appropriate [IAM](https://learn.kodekloud.com/user/courses/aws-iam) permissions to configure and maintain its settings.

<Frame>
  ![The image illustrates the working of AWS CloudTrail, showing how account activity from SDK, CLI, Console, and IAM is processed by CloudTrail and stored in an S3 Bucket and monitored by CloudWatch.](../../../../images/kodekloud.com/kk-media/image/upload/v1752859859/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-CloudWatch-and-CloudTrail-Overview/aws-cloudtrail-account-activity-diagram.jpg)
</Frame>

### Key Components of CloudTrail

CloudTrail is built around several core components:

* **Events:** Capture every API call including management, data, and insight events.
* **Trails:** Store the captured events. Trails can be set up globally, per account, or organization-wide, covering single or multiple regions.
* **CloudTrail Lake:** A feature designed for efficient storage and analysis of large volumes of CloudTrail log data.

<Frame>
  ![The image is a diagram of CloudTrail components, showing sections for Events, Trails, and Lake, each with specific features like Management Events, Account Trails, and CloudTrail Lake.](../../../../images/kodekloud.com/kk-media/image/upload/v1752859860/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-CloudWatch-and-CloudTrail-Overview/cloudtrail-components-diagram.jpg)
</Frame>

For instance, if an operation such as making an S3 bucket public is attempted, CloudTrail logs the API call, which could then trigger a CloudWatch alarm to prompt immediate remediation or notification.

## Summary

* **CloudWatch** delivers a robust observability suite by collecting and analyzing metrics, logs, and traces from AWS and on-premises resources. It supports automated alarms, detailed dashboards, and rich insights into system performance.
* **CloudTrail** provides a thorough audit trail by logging all API calls across your AWS environment. This ensures that you can track changes, monitor user actions, and maintain security and compliance.

<Callout icon="lightbulb">
  CloudWatch and CloudTrail complement each other: while CloudWatch offers real-time insights into performance and health, CloudTrail ensures a complete and verifiable audit trail of all API activities in your AWS environment.
</Callout>

With this guide, you should now have a clearer understanding of how to leverage CloudWatch and CloudTrail to monitor your infrastructure and secure your AWS environment effectively. For further details, consult the official [AWS Documentation](https://aws.amazon.com/documentation/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-sysops-administrator-associate/module/e7f728df-5d8d-4dbb-80f6-33c15cde3034/lesson/3dc25b81-e96f-4fb0-aba9-788e035897aa" />
</CardGroup>
