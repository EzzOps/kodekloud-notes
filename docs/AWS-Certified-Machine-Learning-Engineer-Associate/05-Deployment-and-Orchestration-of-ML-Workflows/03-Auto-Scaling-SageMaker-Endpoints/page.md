# Auto Scaling SageMaker Endpoints

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Deployment-and-Orchestration-of-ML-Workflows/Auto-Scaling-SageMaker-Endpoints/page

How to automatically scale Amazon SageMaker endpoints using CloudWatch and Application Auto Scaling to balance latency, cost, security, and observability

This guide explains how to automatically scale Amazon SageMaker endpoints to handle variable workloads while balancing performance and cost. It covers the request flow, metrics that drive scaling decisions, common scaling strategies (target tracking, step scaling, scheduled), monitoring, security, and operational best practices.

Overview: client requests arrive via an API or load balancer and are routed to a SageMaker endpoint hosting your model. The endpoint distributes requests across inference containers or instances. SageMaker and the instances emit performance metrics to Amazon CloudWatch. Application Auto Scaling consumes those metrics and enforces scaling policies to add or remove capacity as needed.

<Frame>
  <img alt="The image illustrates the process of auto scaling SageMaker endpoints, showing the flow from client requests through an API/load balancer, SageMaker endpoint, inference containers/instances, application auto scaling, and CloudWatch metrics." />
</Frame>

## Why auto scaling matters

When traffic patterns change—such as sudden spikes—CloudWatch metrics capture the increased activity and trigger Auto Scaling. The endpoint scales out to preserve latency and throughput, then scales in when traffic subsides to reduce cost. Scaling decisions trade off short-term cost increases for sustained SLA compliance.

<Frame>
  <img alt="The image is a flowchart explaining the importance of auto-scaling, showing the process from traffic pattern spikes through CloudWatch metrics, leading to either scaling out or scaling in, which affects cost." />
</Frame>

## Auto Scaling toolkit and policy types

CloudWatch collects metrics (latency, CPU, memory, invocation count). Application Auto Scaling evaluates those metrics against your configured policies and then changes endpoint capacity.

* Target tracking: automatically adjusts capacity to maintain a metric at a target value (recommended for SLA-driven latency targets).
* Step scaling: triggers discrete scaling actions at defined thresholds (recommended when you need staged changes).
* Scheduled scaling: pre-allocates capacity at predictable times (useful for known traffic patterns).

Use target-tracking for simple SLA goals and step scaling for finer control of scale increments or when you want multiple thresholds.

<Frame>
  <img alt="The image is a flowchart illustrating an auto-scaling toolkit, including components like CloudWatch Metrics, Application Auto Scaling, Scaling Policies, SageMaker Endpoint/Instances, and Scheduled Scaling." />
</Frame>

Table — common scaling policies and when to use them:

| Policy type       | When to use                                     | Example metric          |
| ----------------- | ----------------------------------------------- | ----------------------- |
| Target tracking   | SLA-driven latency or steady-state goals        | `p95` latency           |
| Step scaling      | Gradual capacity changes or multiple thresholds | Invocation count        |
| Scheduled scaling | Predictable daily/weekly traffic patterns       | Business hours schedule |

## Monitoring metrics and alarms

Key metrics to monitor:

* Latency percentiles: `p95`, `p99` (use for SLA targets)
* Invocation count / requests per second
* CPU / memory utilization
* Model-specific indicators (e.g., batch queue length)

When a metric crosses a threshold, CloudWatch can trigger an alarm or a target-tracking policy. Auto Scaling computes capacity changes and applies them. Use cooldown/stabilization windows to prevent rapid oscillation.

<Callout icon="lightbulb">
  Use latency percentiles like `p95` or `p99` for SLA-driven targets. Set conservative thresholds and reasonable cooldown/stabilization windows to reduce scaling oscillation.
</Callout>

<Frame>
  <img alt="The image is a flowchart titled &#x22;Maintaining Optimal Performance,&#x22; illustrating the process of using CloudWatch Metrics to trigger alarms and auto-scaling actions for SageMaker endpoints. A tip advises using p95/p99 for latency SLAs and setting conservative thresholds and cooldowns to reduce oscillation." />
</Frame>

## Automatic response to demand changes

CloudWatch evaluates metrics continuously. Application Auto Scaling compares the observations to your policies and scales out when load rises or scales in when demand falls. Scheduled scaling handles predictable adjustments. Always configure cooldown periods so the system stabilizes before another scaling action occurs.

<Callout icon="warning">
  Avoid very short cooldown windows; they can cause rapid scale-in/scale-out oscillations. Tune cooldowns and aggregation periods for the metric you rely on.
</Callout>

<Frame>
  <img alt="The image is a flowchart illustrating the process of responding to demand changes, involving traffic spikes, CloudWatch metrics, auto scaling evaluation, scaling in or out, scheduled scaling, and cooldown stabilization." />
</Frame>

## Time-based (scheduled) scaling

Scheduled scaling is useful for predictable load patterns (for example, scale up every weekday at 08:00). Combine scheduled scaling with dynamic policies to cover both predictable and unexpected spikes.

<Frame>
  <img alt="The image is a flowchart illustrating time-based (scheduled) scaling, showing the process from scheduling (CRON/CALENDAR) and Amazon CloudWatch to an Amazon SageMaker Endpoint, impacting cost." />
</Frame>

## Multi-model scaling pattern

In multi-model endpoints, the request flow often looks like:

1. Client sends a prediction request via API Gateway or a load balancer.
2. Model loader retrieves the required model from central storage (e.g., Amazon S3).
3. The model is loaded onto an inference instance (optionally with accelerators like Elastic Inference).
4. Inference is executed and a response is returned to the client.
5. CloudWatch collects operational metrics and Auto Scaling adjusts capacity based on policy.

This pattern enables many models to share infrastructure while auto scaling matches model demand.

<Frame>
  <img alt="The image is a flowchart depicting multi-model scaling architecture, showing the process from client requests, through API gateways, model loading, inference instances, and prediction responses, with components like elastic inference accelerators and application auto-scaling." />
</Frame>

## Observability and operations

* Emit CloudWatch metrics from containerized ML workloads.
* Surface alarms and dashboards for latency, error rates, and instance utilization.
* Log scaling actions to CloudTrail for auditability.
* Use SageMaker Model Monitor to detect data drift, prediction skew, or model quality regressions.
* Consolidate infra and model-monitoring into a single ops dashboard for faster incident response.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Monitoring for Effective Scaling,&#x22; showing the process from Amazon CloudWatch through containerized ML workloads to SageMaker monitoring and alerts." />
</Frame>

## Security and compliance

Apply these three core controls for secure scaling:

1. Least-privilege IAM roles for SageMaker, Application Auto Scaling, and any service integrations.
2. Private VPCs and VPC endpoints to isolate traffic; encrypt data and model artifacts at rest and in transit.
3. Scan container images (Amazon ECR) and enforce image provenance and vulnerability checks before deploying scaled instances.

<Frame>
  <img alt="The image outlines secure scaling configurations, highlighting IAM roles for least privilege and the use of private VPCs to encrypt data and models." />
</Frame>

## Cost and automation best practices

Three practical steps to optimize automated scaling:

* Right-size instances: choose instance families and sizes that match CPU, memory, and accelerator requirements.
* Use Reserved capacity or Savings Plans where appropriate; consider Spot instances for non-critical batch workloads (account for preemption risk).
* Automate everything with infrastructure-as-code (CloudFormation, CDK for Terraform with TypeScript, Terraform) to ensure repeatability and reduce manual mistakes.

<Frame>
  <img alt="The image outlines three steps for efficient and automated scaling: choosing the right instance type, using spot or reserved capacity, and automating scaling setup with CloudFormation/CDK." />
</Frame>

## Patterns and anti-patterns

Follow resilient scaling patterns:

* Conservative thresholds and gradual step-scaling
* Robust monitoring and observability
* Reasonable cooldown windows

Avoid anti-patterns:

* Aggressive thresholds that force unnecessary scaling
* No cooldowns or stabilization (causes oscillation)
* Unchecked scheduled scaling that misaligns with real demand

<Frame>
  <img alt="The image compares &#x22;Resilient Patterns&#x22; and &#x22;Anti-Patterns&#x22; in scaling processes. Resilient Patterns lead to healthy scaling and reliable endpoint performance, while Anti-Patterns result in broken scaling." />
</Frame>

## Common use case — real-time fraud detection

A fraud detection endpoint receives a stream of transactions. Auto Scaling adjusts inference capacity to match volume, ensuring low-latency predictions and real-time flagging of suspicious transactions.

<Frame>
  <img alt="The image illustrates a flowchart for a fraud detection endpoint, starting with incoming transactions, using SageMaker for fraud detection, adjusting instances through application auto scaling, and ending with real-time fraud predictions." />
</Frame>

## Key takeaways

* Choose the right metrics: latency percentiles (`p95`/`p99`), invocation counts, resource utilization.
* Pick the appropriate scaling policy: target tracking for SLAs, step scaling for staged control, scheduled scaling for predictable traffic.
* Secure your stack with least-privilege IAM, VPC isolation, and encryption.
* Automate deployments and scaling config with infrastructure-as-code for consistency and faster recovery.
* Continuously monitor infra, application, and model health (CloudWatch, CloudTrail, SageMaker Model Monitor) and tune thresholds and cooldowns to prevent oscillation.

<Frame>
  <img alt="The image is a summary slide listing key points about service and metrics selection, autoscaling policies, stack security, and infrastructure automation using tools like CloudFormation and Terraform." />
</Frame>

## Links and references

* [Amazon SageMaker documentation](https://docs.aws.amazon.com/sagemaker/)
* [Amazon CloudWatch documentation](https://docs.aws.amazon.com/cloudwatch/)
* [Application Auto Scaling](https://docs.aws.amazon.com/autoscaling/application/userguide/what-is-application-auto-scaling.html)
* [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
* [SageMaker Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/0c3a9951-696d-40f8-88a8-e3dccbf381b1" />
</CardGroup>
