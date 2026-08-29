# Pseudocode for pipeline step that triggers rollback based on CloudWatch alarms
on_deploy:
  - enable_monitoring
  - wait: monitoring_window
  - if CloudWatchAlarm == ALARM:
      trigger_rollback(to: last_stable_model)
  - else:
      promote_traffic(step: next_percentage)
```

Automation options:

* Use `CloudWatch Alarms` + `EventBridge` to trigger Lambda/Runbook for rollback.
* Integrate alarms into CI/CD (CodePipeline) to stop promotions on failures.

***

## Security pillars for safe deployments

Combine access controls, encryption, and network isolation to harden your deployment platform.

<Frame>
  <img alt="The image outlines aspects of security in deployments, focusing on IAM roles and policies, encryption (KMS and TLS), and private networking (VPC)." />
</Frame>

* IAM roles and least-privilege policies to control access to model artifacts and endpoints.
* Encrypt data at rest with `AWS KMS` and in transit with TLS.
* Use VPCs, private subnets, and security groups to restrict access to inference endpoints and data stores.

> **lightbulb** Always apply the principle of least privilege for service roles and encrypt secrets and model artifacts at rest. Use private networking to reduce attack surface for inference endpoints.

***

## Monitoring and observability

Effective monitoring detects regressions, performance issues, and model drift early.

<Frame>
  <img alt="The image illustrates a process for monitoring deployments, including collecting metrics and logs, monitoring model drift, detecting anomalies, and taking alerts and actions." />
</Frame>

Recommended tooling and practices:

* Capture logs, metrics, and traces with `CloudWatch` and `X-Ray`.
* Detect model quality degradation and data drift with `SageMaker Model Monitor`.
* Implement automated alerts and runbooks for critical thresholds to trigger rollback or mitigation steps.
* Store historical metrics for trend analysis and postmortems.

Reference: [Amazon SageMaker Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html)

***

## Disaster recovery fundamentals

Plan for catastrophic failures via backups, replication, and tested restore procedures.

<Frame>
  <img alt="The image illustrates the disaster recovery basis, highlighting three key components: S3 Versioning, Cross-Region Replication, and Backups and Snapshots, all leading to Recovery and Restore." />
</Frame>

Core practices:

* Enable S3 versioning to protect model artifacts from accidental deletion or overwrite.
* Use Cross-Region Replication (CRR) to protect against regional outages.
* Take regular backups and snapshots (EBS, RDS) for point-in-time recovery.
* Regularly test restore procedures and document recovery time objectives (RTO) and recovery point objectives (RPO).

***

## Anti-patterns to avoid

Avoid practices that increase production risk and reduce reproducibility.

<Frame>
  <img alt="The image describes anti-patterns to avoid: no version control, manual deployment, and no monitoring, highlighting their respective issues." />
</Frame>

* No version control: experiments and production changes become unreproducible and hard to audit.
* Manual deployments: increase the chance of human error and inconsistent rollouts — prefer automated CI/CD.
* No monitoring: issues remain undetected until they cause business impact.

***

## Key takeaways

* Leverage blue–green, canary, linear, and A/B testing to stage and validate model releases.
* Secure deployments with least-privilege IAM, encryption (KMS/TLS), and VPC isolation.
* Instrument robust monitoring and automated rollback to recover quickly from regressions.
* Build backups, versioning, and cross-region replication into your disaster recovery plan.

<Frame>
  <img alt="The image is a summary slide outlining four strategies: using various deployment strategies, ensuring security and monitoring for compliance, applying rollback for resilience, and achieving reliable ML production aligned with exam goals. It is attributed to KodeKloud." />
</Frame>

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/514de4c1-d32d-4965-9fc2-69963084fae1)


# Edge Deployment with SageMaker Neo

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Deployment-and-Orchestration-of-ML-Workflows/Edge-Deployment-with-SageMaker-Neo/page

Deploying and optimizing trained machine learning models for resource constrained edge devices using AWS SageMaker Neo, including compilation, packaging, OTA updates, monitoring, and hardware specific optimization.

In this lesson we cover deploying machine learning models to resource-constrained edge devices using AWS SageMaker Neo. SageMaker Neo compiles and optimizes trained models so they run efficiently on a variety of hardware (laptops, smartphones, embedded accelerators). Neo is used after training—its focus is model compilation, device-specific optimization, and packaging for edge deployment.

<Frame>
  <img alt="The image illustrates &#x22;Edge Deployment With SageMaker Neo,&#x22; showing a setup where a trained machine learning model is deployed to various edge devices." />
</Frame>

Core deployment flow

* Train the model in a resource-rich environment (e.g., Amazon SageMaker).
* Compile and optimize the trained model with SageMaker Neo for a target hardware platform.
* Package and deploy the optimized artifact to edge devices for inference.

Why edge deployment?

* Lower latency by running inference locally (critical for robotics, autonomous systems, manufacturing, and healthcare).
* Reduce bandwidth and cloud costs by avoiding frequent raw data uploads.
* Maintain privacy and compliance by keeping sensitive data on-premises.

The trade-off is that edge hardware often has strict compute, memory, and storage constraints—models must be optimized to fit and still meet accuracy/latency requirements.

<Frame>
  <img alt="The image presents information on &#x22;The Edge Deployment Challenge,&#x22; highlighting the benefits and pitfalls of edge devices such as IoT, cameras, and drones. It emphasizes reducing latency by processing data locally and acknowledges constraints related to compute and storage." />
</Frame>

SageMaker Neo: end-to-end optimization

* Input: a trained model from SageMaker or another training environment.
* Process: Neo compiles and applies device-specific optimizations.
* Output: an optimized edge package ready for deployment.

Benefits: reduced latency, lower power consumption, and improved inference throughput on the target device. Important: always validate the compiled model on the actual hardware before production.

<Frame>
  <img alt="The image provides an overview of &#x22;SageMaker Neo,&#x22; illustrating the process from a trained model to optimization for edge devices. It highlights benefits such as reduced latency and improved performance, along with tips for validating performance on real devices." />
</Frame>

> **lightbulb** Validate optimized models early on the target hardware. Emulators help during development, but hardware differences (FP units, drivers, runtime libraries) can affect both performance and numeric results.

Supported frameworks and typical formats
SageMaker Neo supports major frameworks and common model formats—this lets you compile models trained in popular frameworks for deployment at the edge.

| Framework  | Typical model formats / notes                                             |
| ---------- | ------------------------------------------------------------------------- |
| TensorFlow | `SavedModel`, TensorFlow Lite conversions often used for quantized models |
| PyTorch    | `torchscript` or traced models for compilation                            |
| MXNet      | Gluon/Module artifacts supported                                          |
| XGBoost    | Serialized booster models (for tree-based inference)                      |

<Frame>
  <img alt="The image illustrates the supported frameworks for SageMaker Neo, including TensorFlow, PyTorch, and MXNet, highlighting its portability across diverse edge environments." />
</Frame>

Neo compilation workflow (high level)

* Trained model → Neo compiler (select target hardware/platform) → Optimized edge package.
* Test the optimized package on the actual device (or a high-fidelity emulator) before fleet rollout.

<Frame>
  <img alt="The image depicts a &#x22;Neo Compilation Workflow&#x22; diagram, illustrating the process from a &#x22;Trained Model&#x22; to &#x22;Neo Compiler&#x22; to &#x22;Optimized Edge Package,&#x22; with instructions to test the optimized model on target hardware." />
</Frame>

Deployment-at-edge (operational pattern)

* Package the compiled model as an edge application or container.
* Distribute and orchestrate deployments from a central management plane (for example, AWS IoT Core).
* Use staged rollouts: deploy to a small subset of devices for validation, then progressively expand to the entire fleet.

<Frame>
  <img alt="The image illustrates a process titled &#x22;Deployment at the Edge,&#x22; showing a flow from &#x22;Optimized Edge Package&#x22; to &#x22;Edge Devices (Fleet)&#x22; through &#x22;IoT Core,&#x22; suggesting a staged deployment strategy for devices." />
</Frame>

Selecting and targeting hardware

* Identify the target architecture: CPU, GPU, NPU, or a custom accelerator.
* Provide the trained model (for example, a PyTorch model compiled to TorchScript).
* Neo applies device-specific code generation and optimizations to match the runtime environment.

Model optimization techniques for edge

* Quantization: reduce precision (e.g., FP32 → INT8) to shrink model size and accelerate inference.
* Pruning: remove low-impact weights or channels to reduce computation.
* Compression: weight encoding and reduced-precision formats to lower storage and I/O.

These techniques increase throughput and reduce memory usage, but may impact accuracy—balance is key.

<Frame>
  <img alt="The image is a diagram illustrating model optimization and size reduction, showing the process from an original model to a smaller, faster model using techniques like quantization, pruning, and compression. It emphasizes the balance between accuracy and efficiency, warning that over-aggressive pruning can degrade accuracy." />
</Frame>

> **warning** Over-aggressive pruning or quantization can reduce model accuracy. Measure accuracy and latency trade-offs using representative datasets and run those tests on the target device before large-scale deployment.

Model lifecycle and OTA updates

* Maintain a central model repository in the cloud (Amazon S3 or SageMaker Model Registry).
* Use OTA (over-the-air) updates to push new model versions to devices, enabling continuous improvement without physical device access.
* Implement versioning, rollout policies, and rollback strategies to reduce risk during updates.

<Frame>
  <img alt="The image illustrates OTA (Over-The-Air) update strategies, showing a flow from an S3/SageMaker Model Repo to Edge Fleet Devices, emphasizing continuous improvement without direct device interaction." />
</Frame>

Monitoring and security

* Collect operational metrics and logs with Amazon CloudWatch (latency, error rates, invocation counts).
* Audit and enforce device security posture using AWS IoT Device Defender.
* Correlate telemetry (model metrics, device metrics, and security alerts) to detect model drift, anomalies, or hardware failures.

<Frame>
  <img alt="The image illustrates a monitoring and security flow involving Amazon CloudWatch and AWS IoT Device Defender, centered around edge devices for metrics, logging, and security policy enforcement." />
</Frame>

Service integration and cost considerations

* Train and compile models using SageMaker Training and SageMaker Neo.
* Orchestrate distribution and device management with AWS IoT Core.
* Store artifacts and model versions in Amazon S3 or the SageMaker Model Registry.

Primary cost drivers:

| Cost component   | What drives it                                                   |
| ---------------- | ---------------------------------------------------------------- |
| Training compute | Instance types, number of training epochs, hyperparameter search |
| Neo compilation  | Compilation time and target platform complexity                  |
| Storage          | S3 object storage for model artifacts and versions               |
| Data transfer    | Distribution of models to devices and telemetry ingestion        |

<Frame>
  <img alt="The image illustrates a workflow of service integrations and costs involving SageMaker Training + Neo, AWS IoT Core, and Amazon S3 (Model Repo), highlighting cost factors such as training, compilation, and data transfer." />
</Frame>

Recommended best practices

* Automate the compile-test-deploy pipeline: integrate Neo compilation into CI/CD and run device validation tests automatically.
* Start with conservative optimization (mild quantization), then iterate: measure accuracy and latency on-device after each change.
* Use staged rollouts with canary deployments and automated rollback on anomaly detection.
* Maintain clear model and device metadata (versions, target hardware, dependencies) in your model registry.

Summary workflow

1. Train the model in Amazon SageMaker (or another training environment).
2. Use SageMaker Neo to compile and optimize the model for your target hardware.
3. Package and deploy the optimized model to edge devices via AWS IoT Core (use staged rollouts).
4. Monitor device and model health using Amazon CloudWatch and secure the fleet with AWS IoT Device Defender.
5. Push updates via OTA from an S3 or SageMaker model repository and iterate on performance and accuracy.

This pattern enables low-latency, efficient inference at the edge while preserving centralized control for updates, monitoring, and security.

Links and references

* SageMaker Neo documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/neo.html](https://docs.aws.amazon.com/sagemaker/latest/dg/neo.html)
* AWS IoT Core: [https://docs.aws.amazon.com/iot/latest/developerguide/what-is-iot.html](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-iot.html)
* Amazon CloudWatch: [https://docs.aws.amazon.com/cloudwatch/](https://docs.aws.amazon.com/cloudwatch/)
* AWS IoT Device Defender: [https://docs.aws.amazon.com/iot/latest/developerguide/device-defender.html](https://docs.aws.amazon.com/iot/latest/developerguide/device-defender.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/2e0767fe-d3f8-4c90-a9fe-e202e11599b4)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/0e88addd-fa4a-4ec4-9929-ba9d50edc84d)
