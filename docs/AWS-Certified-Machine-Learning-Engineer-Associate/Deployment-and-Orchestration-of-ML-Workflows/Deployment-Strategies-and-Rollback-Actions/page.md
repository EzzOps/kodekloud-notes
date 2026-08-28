# Deployment Strategies and Rollback Actions

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Deployment-and-Orchestration-of-ML-Workflows/Deployment-Strategies-and-Rollback-Actions/page

Overview of ML deployment strategies, automated rollback mechanisms, AWS tooling, security, monitoring, disaster recovery, and best practices for safe reproducible production MLOps.

In this lesson we cover deployment strategies and rollback actions that keep ML application and model updates safe, predictable, and repeatable. This article explains common patterns, automated rollback flows, and AWS-focused tooling for production-grade MLOps.

Agenda:

* Fundamentals of ML deployment strategies
* How rollback mechanisms work
* AWS deployment types: blue-green, canary, linear, and A/B testing
* How rollbacks resolve production issues
* Key concepts related to ML workflow orchestration

<Frame>
  <img alt="The image displays an agenda for a session on machine learning deployment, including topics like ML deployment strategies, rollback mechanisms, AWS deployment types, and production issue management." />
</Frame>

## Four-step process for safe ML deployments

To reduce downtime and customer impact, use a consistent, four-step deployment approach:

1. Validate the model: run tests and compare metrics against production-like datasets to verify accuracy and performance.
2. Controlled release: expose the new model incrementally rather than switching traffic all at once.
3. Continuous monitoring: collect metrics and logs in real time to detect regressions and drift.
4. Instant rollback: automate the ability to revert to the last known-good version when thresholds are breached.

This methodology reduces risk, enables reproducibility, and ensures releases remain auditable.

<Frame>
  <img alt="The image outlines a process for safe machine learning deployments, including steps like validating the model, controlled release, performance monitoring, and potential rollback, highlighting benefits such as reduced downtime, limited customer impact, and deployment readiness." />
</Frame>

## Example AWS-based deployment pipeline

A typical automated pipeline for ML on AWS:

* Source control: store model code, infra-as-code, and configs in a VCS such as AWS CodeCommit, GitHub, or GitLab.
* Orchestration: trigger CI/CD with AWS CodePipeline, GitHub Actions, or similar to run builds, tests, and deployments.
* Artifact: produce a trained model package or container image (ECR or model package in SageMaker).
* Hosting: serve the artifact with SageMaker real-time endpoints, batch transform jobs, or ECS/EKS containers.
* Observability: use CloudWatch, X-Ray, and SageMaker Model Monitor for metrics, traces, and drift detection.

These components give you clear rollback points and a repeatable MLOps workflow.

Helpful references:

* [Amazon SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/)
* [AWS CodePipeline](https://docs.aws.amazon.com/codepipeline/)
* [Amazon CloudWatch](https://docs.aws.amazon.com/cloudwatch/)

Table: AWS toolchain mapping

| Pipeline stage      |                             AWS service examples | Purpose                              |
| ------------------- | -----------------------------------------------: | ------------------------------------ |
| Source Control      |                           `CodeCommit`, `GitHub` | Store code, training/serving configs |
| CI/CD Orchestration |                      `CodePipeline`, `CodeBuild` | Run builds, tests, deploy steps      |
| Artifact Storage    |          `S3`, `ECR`, `SageMaker Model Registry` | Persist model artifacts and images   |
| Hosting / Serving   |              `SageMaker Endpoints`, `ECS`, `EKS` | Real-time inference or batch jobs    |
| Observability       | `CloudWatch`, `X-Ray`, `SageMaker Model Monitor` | Metrics, traces, drift detection     |

***

## Deployment strategies

Below are common deployment patterns used in MLOps. Each strategy balances risk, complexity, and speed differently.

### Blue–green deployment

Blue–green deploys a new version into an isolated environment (green), validates it, and then switches production traffic from blue to green for near-zero downtime.

<Frame>
  <img alt="The image illustrates a Blue/Green Deployment process, showing the transition from a current (Blue) environment to a new (Green) environment using AWS Load Balancer and AWS Route 53, with an emphasis on traffic switching." />
</Frame>

Key points:

* Route traffic with an Application Load Balancer or `Route 53`.
* Test the green environment in isolation before switching DNS or ALB target groups.
* Rollback is simple: direct traffic back to blue if problems appear.

### Canary deployment

Canary releases route a small fraction of production traffic to the new model to validate behavior under real load.

<Frame>
  <img alt="The image illustrates a Canary Deployment strategy, showing traffic gradually switching from an old model (90%) to a new model (10%) using SageMaker Endpoints. The diagram suggests that rollback diverts traffic back to the stable version." />
</Frame>

Typical flow:

* Start with a small percentage (e.g., `5–10%`) of traffic to the canary.
* Monitor latency, error rate, and business KPIs.
* Gradually increase traffic when metrics remain within thresholds, or revert immediately on regressions.

### Linear (incremental) deployment

Linear deployments shift traffic in fixed increments (e.g., 0 → 20 → 50 → 100), validating at each step.

* Increase traffic in controlled steps and validate at each stage.
* If any step shows regressions, rollback to the previous stable percentage or to 0% immediately.

### A/B testing

A/B testing runs two or more model variants in parallel and compares their real-world performance using predefined metrics.

<Frame>
  <img alt="The image depicts a flowchart of A/B testing deployments, showing user traffic split between Model A (Control) and Model B (Variant), followed by a comparison of metrics and a decision to promote the winner or rollback." />
</Frame>

Best practices:

* Define evaluation metrics and statistical significance thresholds before launching.
* Use consistent traffic splits (e.g., `50/50`) or business-driven ratios.
* Promote the winning model automatically or manually after validation.

Comparison of strategies

| Strategy    |           Risk |   Speed to 100% | Typical use case                            |
| ----------- | -------------: | --------------: | ------------------------------------------- |
| Blue–Green  | Low (isolated) |    Fast cutover | Major version changes                       |
| Canary      |         Medium |         Gradual | Validate behavior under production load     |
| Linear      |         Medium | Controlled pace | Incremental confidence increases            |
| A/B Testing |  Low to medium | Depends on test | Experimentation and metric-driven selection |

***

## Rollback mechanisms

A robust rollback reverts to a known-good state automatically when failures are detected.

<Frame>
  <img alt="The image is a flowchart illustrating rollback mechanisms, showing steps from deploying a new model to monitoring and detecting failures, with a rollback to a stable version if needed." />
</Frame>

Typical automated rollback flow:

1. Deploy new version and enable active monitoring.
2. Continuously evaluate health and metric thresholds (latency, errors, KPI deltas).
3. If thresholds are breached, trigger an automated rollback to the last stable version.
4. Log events and analyze root causes to prevent recurrence.

Example pseudocode for automated rollback logic:

```yaml theme={null}
