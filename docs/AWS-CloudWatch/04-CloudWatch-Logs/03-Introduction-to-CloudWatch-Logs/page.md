# Introduction to CloudWatch Logs

Source: https://notes.kodekloud.com/docs/AWS-CloudWatch/CloudWatch-Logs/Introduction-to-CloudWatch-Logs/page

This article introduces AWS CloudWatch Logs and Agent for collecting, monitoring, and storing log files from AWS resources and on-premises servers.

AWS CloudWatch Logs is a fully managed service for collecting, monitoring, and storing log files from AWS resources and on-premises servers. When paired with the CloudWatch Agent, you gain deep visibility into system-level metrics (CPU, memory, disk) and custom application logs.

Together, these capabilities help you:

* Maintain application health
* Simplify troubleshooting
* Support security and compliance audits

## Key Capabilities of CloudWatch Logs

| Capability       | Description                                                      | AWS CLI Example                                                                                                                                                                                                                                                                               |
| ---------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Retention        | Store logs indefinitely or for a custom retention period         | `aws logs put-retention-policy --log-group-name MyGroup --retention-in-days 30`                                                                                                                                                                                                               |
| Real-time search | Search and filter log data on the fly                            | `aws logs filter-log-events --log-group-name MyGroup --filter-pattern "ERROR"`                                                                                                                                                                                                                |
| Metric Filters   | Convert log patterns into CloudWatch metrics                     | `aws logs put-metric-filter --filter-name ErrorCount --log-group-name MyGroup --filter-pattern "ERROR" --metric-transformations metricName=ErrorCount,metricNamespace=AppMetrics,metricValue=1`                                                                                               |
| Alarms & Actions | Trigger alarms or automated actions based on log-derived metrics | `aws cloudwatch put-metric-alarm --alarm-name HighErrorRate --metric-name ErrorCount --namespace AppMetrics --statistic Sum --period 60 --threshold 1 --comparison-operator GreaterThanOrEqualToThreshold --evaluation-periods 1 --alarm-actions arn:aws:sns:us-east-1:123456789012:NotifyMe` |

<Callout icon="triangle-alert">
  Defining an **indefinite retention** policy can increase storage costs. Always monitor your log volume and set a realistic retention period.
</Callout>

## Installing and Configuring the CloudWatch Agent

You install the CloudWatch Agent on EC2 instances or on-premises servers to collect metrics and logs:

```bash theme={null}
