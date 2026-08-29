# What is AWS FIS

Source: https://notes.kodekloud.com/docs/Chaos-Engineering/Chaos-Engineering-Fundamentals/What-is-AWS-FIS/page

AWS Fault Injection Simulator is a managed service for running fault-injection experiments on AWS workloads to validate system resilience under failure scenarios.

In the world of Chaos Engineering, tools like Netflix’s [Chaos Monkey](https://github.com/Netflix/chaosmonkey) pioneered fault injection testing. Today, platforms such as Gremlin, Azure Chaos Studio, and **AWS Fault Injection Simulator (FIS)** help teams validate system resilience under real-world failure scenarios.

AWS FIS is a fully managed service that lets you run fault-injection experiments on AWS workloads. By deliberately introducing failures, you can:

* Identify weaknesses before they affect customers
* Validate auto-scaling, failover, and recovery processes
* Ensure SLAs are met under adverse conditions

<Callout icon="lightbulb">
  AWS FIS supports both simple and complex scenarios—from terminating individual EC2 instances to simulating an Availability Zone outage.
</Callout>

## Key Benefits

| Benefit                   | Description                                                         |
| ------------------------- | ------------------------------------------------------------------- |
| Fully Managed             | No need to provision infrastructure for fault injection             |
| Native AWS Integration    | Works with IAM, CloudWatch Alarms, AWS X-Ray, EventBridge, and more |
| Prebuilt & Customizable   | Use built-in templates or define your own experiments               |
| Multi-Environment Support | Inject faults in EC2, ECS, EKS, RDS, Lambda, and more               |

## AWS FIS Architecture

AWS FIS integrates seamlessly with your AWS environment:

* **CloudWatch Alarms**: Trigger experiments or remediation workflows when thresholds are crossed.
* **AWS X-Ray**: Correlate faults with distributed traces to pinpoint failures.
* **EventBridge**: Automate experiment scheduling and notifications.

<img alt="AWS FIS Architecture Diagram" />

You can leverage AWS FIS to simulate:

* EC2 instance terminations and CPU/network stress
* ECS and EKS pod failures
* RDS instance failovers
* Availability Zone outages
* Network latency and packet loss between resources

## Managing Experiments

AWS FIS experiments are defined as JSON documents. You can manage them through:

| Interface              | Command / Action                                      |
| ---------------------- | ----------------------------------------------------- |
| AWS Management Console | Create, configure, and run experiments via the web UI |
| AWS CLI                | `aws fis create-experiment-template`                  |
| AWS CloudFormation     | Use the `AWS::FIS::ExperimentTemplate` resource       |

```yaml theme={null}
