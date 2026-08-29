# Centralized Logging and Monitoring

Source: https://notes.kodekloud.com/docs/AWS-IAM/Configure-AWS-IAM-at-Scale/Centralized-Logging-and-Monitoring/page

This article explains how to implement centralized logging and monitoring in AWS using CloudTrail, CloudWatch, and Config services.

Centralized logging and monitoring are critical for maintaining security, compliance, and operational visibility in your AWS environment. By aggregating audit trails, metrics, and resource configurations into a single pane of glass, you can troubleshoot faster, detect anomalies early, and meet regulatory requirements.

In this guide, we’ll show you how to implement centralized logging and monitoring using three AWS services:

| Service           | Purpose                                                 | Key Features                                                              |
| ----------------- | ------------------------------------------------------- | ------------------------------------------------------------------------- |
| AWS CloudTrail    | Records API calls and user activity                     | Full audit trail, log file integrity validation, multi-region trails      |
| Amazon CloudWatch | Collects and visualizes logs and metrics                | Real-time dashboards, alarms, log aggregation, custom metrics             |
| AWS Config        | Assesses, audits, and evaluates resource configurations | Continuous compliance checks, resource change tracking, conformance packs |

## AWS CloudTrail

AWS CloudTrail provides governance, compliance, and risk auditing by capturing all API calls and delivering log files to an Amazon S3 bucket.

```bash theme={null}
