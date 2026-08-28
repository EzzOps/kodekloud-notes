# Demo Utilizing rollback triggers

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Deployment-Modes/Demo-Utilizing-rollback-triggers/page

Demonstrates using CloudFormation rollback triggers tied to CloudWatch alarms to prevent or roll back stack updates when monitored metrics indicate unhealthy states

In this walkthrough you'll learn how to use CloudFormation rollback triggers to prevent stack creates or updates when one or more CloudWatch alarms are in the ALARM state. Rollback triggers allow CloudFormation to monitor specified CloudWatch alarms for a configured monitoring window after a stack operation begins. If any monitored alarm enters ALARM during that window, CloudFormation marks the operation as failed and rolls back the change.

Key benefits:

* Prevents deploying changes when monitored metrics indicate an unhealthy state.
* Adds an automated safety net to stack updates and creates.
* Useful for production and critical systems where metric-driven protection is required.

Demo workflow

1. Create a stack from an EC2 instance template.
2. Confirm the EC2 instance is running and tagged for metric lookup.
3. Create a CloudWatch alarm that monitors the EC2 instance CPUUtilization.
4. Attach that alarm as a rollback trigger when updating the stack.
5. Observe the update failing when the alarm is in ALARM.
6. Clean up resources.

Create the stack from a template. Upload the EC2 instance template and pick the template that provisions a simple EC2 instance.

<Frame>
  <img alt="A dark-themed Windows file-open dialog showing a &#x22;cf-project&#x22; folder listing YAML files (e.g., simple-s3, s3-bucket, ec2-instance). The dialog is over an AWS web console page with a &#x22;Sync from Git&#x22; option visible." />
</Frame>

Enter a stack name and choose instance parameters. For this demo we use a t3.micro instance in the default VPC and leave other settings at their defaults. Proper tagging helps CloudWatch locate instance metrics and makes selecting the right instance easier when creating alarms.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation &#x22;Create stack&#x22; console showing the Parameters panel with an EC2 instance type dropdown open (options like t3.micro and t3.small) and navigation buttons (Cancel, Previous, Next). The browser window and Windows taskbar are also visible." />
</Frame>

Create a CloudWatch alarm to use as the rollback trigger:

* In the CloudWatch console go to Alarms → Create alarm.
* Select metric → EC2 → Per-Instance Metrics → CPUUtilization. If the list is long, type “CPU” to filter.
* Metric options: for example, Statistic = Average, Period = 5 minutes.
* Condition: choose a threshold that will trigger ALARM for demonstration (e.g., GreaterThanThreshold = 0.2).
* Skip SNS notification for the demo and set the alarm name to CloudWatchAlarm1.

<Frame>
  <img alt="A screenshot of the AWS CloudWatch &#x22;Create alarm&#x22; page showing a CPUUtilization metric for an EC2 instance (InstanceId i-07733807276ccf726, name SimpleWebServer) with the statistic set to Average and a 5-minute period, and a small chart showing near-zero CPU usage." />
</Frame>

Rollback trigger configuration requires two values: the monitoring time (minutes) and the alarm ARN. Add the RollbackConfiguration to your CloudFormation template or include it as part of the stack update parameters. Example snippet:

```yaml theme={null}
