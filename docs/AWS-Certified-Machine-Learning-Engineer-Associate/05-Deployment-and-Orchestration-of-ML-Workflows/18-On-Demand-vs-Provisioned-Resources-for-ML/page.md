# On Demand vs Provisioned Resources for ML

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Deployment-and-Orchestration-of-ML-Workflows/On-Demand-vs-Provisioned-Resources-for-ML/page

Guide comparing on-demand versus provisioned cloud resources for ML, explaining trade-offs and hybrid strategies to balance cost, reliability, and scalability

When running machine learning workloads, you must decide how to allocate compute capacity. This guide compares on-demand (pay-as-you-go) resources with provisioned capacity, explains trade-offs, and gives practical guidance to choose the best option for your ML projects.

Agenda:

* Explore the on-demand, pay-as-you-go model and its flexibility.
* Compare provisioned models that reduce cost but add commitment.
* Show how to pick a strategy that balances cost, reliability, and scalability.

<Frame>
  <img alt="The image is an agenda slide highlighting three points about flexibility and cost-efficiency in services: on-demand, provisioned options, and choosing the right type for scaling efficiently." />
</Frame>

## Provisioning models to consider

Choose provisioning based on predictability, cost tolerance, and compliance needs.

| Model              | Description                                                          | Typical savings / trade-off                                        | Best fit                                                            |
| ------------------ | -------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------- |
| On-Demand          | Pay for compute by the hour/second with no long-term contract.       | No upfront costs; higher per-unit price but maximum flexibility.   | Experiments, development, unpredictable or spiky workloads.         |
| Reserved Instances | Commit to 1–3 years for specific instance class/region.              | Up to \~72% savings vs on-demand; requires commitment.             | Predictable, long-running services (steady inference).              |
| Savings Plans      | Commit to an hourly spend to get discounts across instance families. | Flexible across instance types; lower cost than on-demand.         | Teams needing flexibility across instances with predictable spend.  |
| Spot Instances     | Use spare capacity at steep discounts (interruptible).               | Up to \~90% savings; instances can be reclaimed with short notice. | Fault-tolerant large-scale training, batch jobs with checkpointing. |
| Dedicated Hosts    | An entire physical server for single-tenant use.                     | Higher cost but required for certain licenses or compliance.       | Workloads with licensing or regulatory isolation needs.             |

<Frame>
  <img alt="The image illustrates a &#x22;Resource Provisioning Landscape&#x22; featuring four types: On-Demand, Reserved, Spot, and Dedicated Hosts." />
</Frame>

## Match instance choice to workload patterns

Workloads typically follow two demand patterns:

* Spiky / variable — e.g., many training jobs, unpredictable experiments.
* Steady / predictable — e.g., production inference endpoints with consistent traffic.

Selecting the wrong model either wastes budget (overprovisioning) or causes capacity shortages (underprovisioning). Align choice to the workload’s predictability and fault-tolerance.

## On-demand resources: when flexibility matters

On-demand instances are ideal when you cannot predict timing or scale. They require no long-term commitment and are billed only for usage, making them excellent for iterative development and bursty workloads.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;On-Demand Resources Deep Dive,&#x22; discussing how unpredictable ML training workloads utilize on-demand instances, which are billed per usage with no upfront cost." />
</Frame>

When to prefer on-demand:

* Short or uncertain training runs where long-term commitment isn’t justified.
* Development, experimentation, and rapid iteration cycles.
* Handling sudden traffic spikes or unplanned compute needs.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;On-Demand Resources Deep Dive,&#x22; discussing how unpredictable ML training workloads utilize on-demand instances, which are billed per usage with no upfront cost." />
</Frame>

## Provisioned options: optimize for cost

When usage is predictable, provisioned models significantly lower costs. Use reserved commitments when you can forecast steady usage, and use spot for fault-tolerant workloads to maximize savings.

<Frame>
  <img alt="The image outlines four provisioned options for cloud services: Reserved Instances, Savings Plans, Spot, and Dedicated Hosts, each offering different savings and usage benefits." />
</Frame>

Provisioned use cases:

* Steady inference workloads: use Reserved Instances or Savings Plans to reduce long-term costs.
* Large-scale training: use Spot Instances plus checkpointing to keep costs low while tolerating interruptions.
* Compliance-sensitive workloads: use Dedicated Hosts when isolation or specific licensing is required.

<Frame>
  <img alt="The image outlines three provisioned use cases: Reserved/Savings Plans for steady inference workloads, Spot for large-scale, fault-tolerant training jobs, and Dedicated (which is not described)." />
</Frame>

## Hybrid strategy: balance cost and reliability

A hybrid approach often yields the best balance:

* Run the majority (for example, 70–90%) of non-critical distributed training on Spot Instances to maximize cost savings.
* Keep a minority (for example, 10–30%) as On-Demand capacity to ensure critical tasks complete when spot nodes are reclaimed.
* Use Reserved Instances or Savings Plans for long-running inference services to lock in discounts.

This mix captures most cost benefits of spot capacity while preserving enough stable capacity for reliability.

## Cost optimization best practices

* Right-size instances: choose instance families and sizes that match CPU, memory, GPU, and I/O needs.
* Build fault-tolerance: use managed spot training, frequent checkpoints, and job retries for distributed jobs.
* Apply Savings Plans or Reserved Instances where usage is consistent.
* Monitor utilization and adjust commitments regularly (e.g., [AWS CloudWatch](https://learn.kodekloud.com/user/courses/aws-cloudwatch) or your provider’s monitoring tools).
* Automate lifecycle: use autoscaling and orchestration to spin instances up and down based on demand.

<Frame>
  <img alt="The image outlines four cost optimization best practices for cloud computing: right-sizing instances, using managed spot training, applying savings plans, and tracking utilization with CloudWatch." />
</Frame>

<Callout icon="lightbulb">
  Design distributed training to tolerate spot interruptions: use frequent checkpoints, incremental saves of model state, and reliable job retry logic so progress persists when capacity is reclaimed.
</Callout>

## Common pitfalls and how to avoid them

* Expect spot interruptions: implement checkpointing, graceful shutdown handling, and orchestration that supports retries.
* Over-commitment risk: avoid locking too much capacity in Reserved Instances if usage patterns can change.
* Oversizing: measure actual utilization and right-size to prevent unnecessary spend.
* Mismatched choices: always align instance type to workload pattern — flexibility for variable workloads, provisioned capacity for predictable workloads.

## Real-world example — Acme AI Corp.

Acme AI operates large model training pipelines and production inference:

* Training: 80% of training capacity runs on Spot Instances to minimize cost. 20% runs on On-Demand to guarantee completion for critical jobs.
* Inference: steady, long-running endpoints are covered by Savings Plans to capture predictable discounts and reduce per-hour costs.

<Frame>
  <img alt="The image depicts a flowchart illustrating a real-world scenario where ACME AI Corp uses training jobs with a mix of 80% Spot instances for cost-saving and 20% On-Demand instances to ensure job completion, culminating in inference endpoints with savings plans." />
</Frame>

## Recap — key takeaways

* On-demand: maximum flexibility, higher cost; ideal for experimentation and unpredictable workloads.
* Provisioned (Reserved / Savings Plans): lower cost for predictable workloads; trade flexibility for savings.
* Spot: biggest cost savings, but interruptible; perfect for fault-tolerant, large-scale batch or training jobs.
* Hybrid strategies (mix of Spot + On-Demand + Savings Plans) typically balance cost and reliability best.

<Frame>
  <img alt="The image presents key takeaways about different computing options, describing them as On-Demand, Provisioned, Spot, and RIs Savings Plans, with corresponding benefits and drawbacks." />
</Frame>

## Links and references

* [AWS EC2 Pricing & Instance Types](https://aws.amazon.com/ec2/pricing/)
* [Amazon EC2 Spot Instances](https://aws.amazon.com/ec2/spot/)
* [AWS Savings Plans](https://aws.amazon.com/savingsplans/)
* [AWS Reserved Instances](https://aws.amazon.com/ec2/pricing/reserved-instances/)
* [AWS CloudWatch monitoring](https://learn.kodekloud.com/user/courses/aws-cloudwatch)

Use these resources to validate cost assumptions and automate optimizations for production ML workflows.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/cfe6b9e5-e080-4d13-bb60-468e0cdf3239" />
</CardGroup>
