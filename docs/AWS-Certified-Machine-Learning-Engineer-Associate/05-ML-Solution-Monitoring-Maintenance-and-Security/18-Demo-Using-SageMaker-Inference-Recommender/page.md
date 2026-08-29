# Demo Using SageMaker Inference Recommender

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Solution-Monitoring-Maintenance-and-Security/Demo-Using-SageMaker-Inference-Recommender/page

Guide to using SageMaker Inference Recommender to automate benchmarking across instance types, compare latency, throughput, and cost, and provide recommendations for production model deployment.

Deploying a model to Amazon SageMaker for the first time often raises questions about which instance family, size, and configuration will hit your latency, throughput, and cost targets. Manually benchmarking every combination is slow and expensive.

Amazon SageMaker Inference Recommender automates this process: it runs standardized inference benchmarks across multiple instance types and configurations, and returns compact, actionable recommendations (latency, throughput, estimated cost, and diagnostic metrics) so you can pick the best trade-off for production.

This guide walks through the console flow, what inputs the service needs, how to interpret results, and practical validation tips.

> **lightbulb** SageMaker Inference Recommender automates model benchmarking across instance types and configurations. Use it to quickly compare latency, throughput, and cost trade-offs to select an appropriate deployment target.

## Console flow (step-by-step)

1. Open the [SageMaker Console](https://learn.kodekloud.com/user/courses/aws-sagemaker) and navigate to the AI section.
2. Go to Model Governance → Model Dashboard to see registered or deployed models.
3. Choose the model you want to evaluate to open its details page.
4. Locate the Inference Recommender section and click to create/run a new recommendation job.

When creating the evaluation job you will typically provide:

* An [S3](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3) location containing one or more sample request payloads.
* The request input format (for example, `text/csv` or `application/json`).
* Optional flags such as model compilation via SageMaker Neo.
* The instance families (or a broad search) to evaluate.
* A job name and any metadata.

| What you provide when starting a job | Typical values / examples                 |
| ------------------------------------ | ----------------------------------------- |
| S3 test payload location             | `s3://my-bucket/inference-samples/`       |
| Input format                         | `text/csv`, `application/json`            |
| Optional compilation                 | SageMaker Neo (yes/no)                    |
| Instance families to evaluate        | `ml.c5`, `ml.m5`, `ml.p3` (or full sweep) |
| Job name / metadata                  | `my-model-inference-reco-2026-07`         |

> **warning** Ensure the SageMaker execution role has read access to the S3 location with the test payloads and any model artifacts. Running a broad instance sweep will incur charges for every instance type evaluated.

## Optional: Model compilation with SageMaker Neo

SageMaker Neo can compile models into optimized artifacts for certain instances and edge targets, often improving latency and throughput. Consider these guidelines:

* Use Neo if you want to determine whether a compiled model improves performance on supported targets.
* Skip Neo if you need performance numbers for the model artifact exactly as deployed in your current pipeline.

Deciding whether to compile with Neo depends on your production target: if you plan to deploy to a Neo-supported target, include compilation in the evaluation.

## Example inputs and quick tips

* S3 location: `s3://my-bucket/inference-samples/` (a folder with representative payload files).
* Input format: `text/csv` or `application/json`.
* Representative payloads produce the most reliable recommendations — include edge cases and typical requests.

Practical tips:

* Start with a focused set of instance families (CPU-only or GPU-only) to reduce time and cost.
* If strict tail-latency is critical, emphasize p90/p99 metrics.
* Use the results to inform both instance selection and autoscaling thresholds.

## Interpreting results

When the job completes, the Recommender returns a results table. Key columns and their meaning:

| Column             | Purpose / How to use it                                                                      |
| ------------------ | -------------------------------------------------------------------------------------------- |
| Instance type      | Which EC2 instance was benchmarked (e.g., `ml.c5.xlarge`, `ml.p3.2xlarge`).                  |
| Status             | Whether the test completed successfully or failed with errors.                               |
| Instance count     | Number of instances used (useful when comparing single-node vs multi-node throughput).       |
| Latency            | Average and tail latency (p50, p90, p99) for the supplied sample requests.                   |
| Throughput         | Requests per second achieved during the benchmark.                                           |
| Cost per hour      | Estimated hourly cost for the evaluated configuration (based on instance pricing).           |
| Additional metrics | Memory/CPU/GPU utilization, error rates, and other diagnostics provided for deeper analysis. |

Use these metrics to evaluate trade-offs:

* Lower latency often requires larger or GPU-backed instances and costs more.
* Higher throughput may favor larger instances or horizontal scaling (more instances).
* Cost-per-request depends on instance cost and achieved throughput.

Recommended validation workflow:

1. Use the recommended instance(s) as the starting point.
2. Run production-like load tests with realistic payload distributions.
3. Validate autoscaling behavior and cost at target throughput.
4. Test under failure scenarios and cold-start conditions if applicable.

## Result interpretation examples

| Scenario                        | Recommendation                                                                                                  |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Low-latency API (tight p99 SLA) | Favor instances with lower p99 latency (often GPU or high-performance CPU instances).                           |
| High-throughput batch inference | Choose instance/instance-count combination with best cost-per-request at required throughput.                   |
| Cost-sensitive deployments      | Target instance types that give acceptable latency at the lowest cost-per-request; consider horizontal scaling. |

## Practical checklist before production rollout

* Provide representative payloads (coverage of typical and edge cases).
* Start with a narrow family list, expand if necessary.
* Prioritize p90/p99 if tail latency matters.
* Run larger-scale load tests and verify autoscaling configuration.
* Confirm that the SageMaker execution role has appropriate S3 access.

## Summary

SageMaker Inference Recommender simplifies benchmarking and decision-making for model deployment to SageMaker. By supplying an S3 location with representative payloads and optionally enabling Neo compilation, the service benchmarks multiple instance types and returns a concise comparison of latency, throughput, and cost. Use these recommendations as the basis for a validated production deployment, but always run additional production-like tests prior to final rollout.

## Links and References

* [SageMaker Console — SageMaker](https://learn.kodekloud.com/user/courses/aws-sagemaker)
* [Amazon S3 — Storage](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [Amazon EC2 — Instances and families](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/e07ceb86-4976-4c8e-a6f8-3518534ec115/lesson/a83b87bf-2396-47c2-b5c3-f09d9b20e72a)
