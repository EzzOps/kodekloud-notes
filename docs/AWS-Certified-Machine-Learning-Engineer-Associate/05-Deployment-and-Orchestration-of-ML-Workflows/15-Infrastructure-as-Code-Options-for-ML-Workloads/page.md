# tests/test_transform.py
from myml.transforms import normalize_features
import numpy as np

def test_normalize_features_zero_mean_unit_variance():
    X = np.array([[1.0, 2.0], [3.0, 4.0]])
    X_norm = normalize_features(X)
    # mean should be ~0 and std should be ~1 per column
    assert np.allclose(X_norm.mean(axis=0), 0, atol=1e-6)
    assert np.allclose(X_norm.std(axis=0), 1, atol=1e-6)
```

Integration testing in ML workflows

Purpose: validate interactions between components and ensure artifacts and interfaces are compatible.

Typical integration scenarios:

* Data ingestion → preprocessing → training → artifact storage.
* Verification that outputs from one step are valid inputs for downstream steps.
* Ensuring training jobs produce expected artifacts (model files, metrics, metadata).

Typical integration workflow:

1. Ingest or synthesize test data and run preprocessing.
2. Execute training jobs using CI (CodePipeline + CodeBuild or temporary SageMaker jobs).
3. Validate produced artifacts, metadata, and model formats before promotion.

<Frame>
  <img alt="The image illustrates a process flow for &#x22;Integration Testing in ML,&#x22; showing steps like Data Ingestion, Model Training, and Model Storage, with integration tests in AWS CI/CD." />
</Frame>

A successful integration test confirms:

* Data schemas and formats match expectations across steps.
* Artifacts are versioned and stored correctly.
* Downstream consumers can load and use artifacts without errors.

End-to-end (E2E) testing

Purpose: validate the complete pipeline from raw data to deployed model predictions and metrics on a test endpoint.

E2E validation typically includes:

* Ingesting raw or synthetic test data through the full pipeline.
* Running training and evaluation stages and generating model artifacts.
* Deploying the model to a test serving endpoint (e.g., SageMaker endpoint).
* Sending test requests to the endpoint and validating correctness, latency, and resource usage.

Passing E2E tests gives confidence that a pipeline is production-ready.

<Frame>
  <img alt="The image is a flowchart titled &#x22;End-to-End Testing in ML,&#x22; outlining steps from raw data ingestion to model deployment and validation, ensuring systems are reliable and production-ready." />
</Frame>

Test-Driven Development (TDD) for ML

Apply TDD to deterministic pipeline parts to make behavior explicit and prevent regressions:

1. Write a failing test that specifies desired behavior (e.g., transformation output).
2. Implement the minimal code to make the test pass.
3. Run tests and confirm success.
4. Refactor and improve the code while ensuring tests still pass.
5. Repeat for additional features and utilities.

Benefits: clearer requirements, documented expectations, and fewer regressions.

<Frame>
  <img alt="The image illustrates a cycle for Test-Driven Development (TDD) in Machine Learning, including steps: writing the test first, developing ML code, running the test, and refactoring/improving." />
</Frame>

<Callout icon="lightbulb">
  Test-Driven Development is especially valuable for deterministic parts of ML pipelines: data processing, validation logic, metric calculations, and infrastructure-as-code for reproducible deployments.
</Callout>

A/B testing in production

A/B testing compares multiple model versions on live traffic to empirically select the best performer:

1. Configure traffic splitting on a serving layer (e.g., a SageMaker endpoint or API Gateway + router).
2. Route a portion of requests to model variant A and the rest to variant B.
3. Collect predictions, latencies, and business metrics for both versions.
4. Analyze statistical differences to select the winning model.

This approach provides evidence of real-world performance under production distributions.

<Frame>
  <img alt="The image is a flowchart illustrating A/B testing in machine learning pipelines using SageMaker, with client requests being split between two model versions for comparison of results and metrics." />
</Frame>

Security for ML testing

Secure testing practices minimize risk and ensure compliance:

* Access control: use fine-grained [IAM roles](https://aws.amazon.com/iam/) and least-privilege policies.
* Encryption: protect data at rest with [AWS KMS](https://aws.amazon.com/kms/) and in transit with TLS.
* Data handling: use anonymized or synthetic datasets for tests; mask or transform any production-derived samples.

<Frame>
  <img alt="The image illustrates key components of security in ML testing, including IAM roles and policies, encryption (KMS, TLS), and data masking for test data, all contributing to a secure test environment." />
</Frame>

Monitoring, backups, and recovery

Design recoverable and observable test infrastructure:

1. Back up test datasets, pipeline definitions, and configs.
2. Replicate backups across regions for redundancy.
3. Automate restore procedures to rapidly recreate test pipelines.

These steps reduce downtime in CI/CD and keep validation processes resilient.

<Frame>
  <img alt="The image illustrates a flowchart for monitoring tests in ML pipelines, detailing steps like backing up test data/config, replicating across regions, and restoring test pipelines quickly." />
</Frame>

Anti-patterns to avoid

* Skipping unit or integration tests: increases the chance of costly regressions.
* Using raw production data in tests: creates privacy and compliance risks.
* Not monitoring test outcomes: failing tests that go unnoticed are worthless.

<Frame>
  <img alt="The image outlines three anti-patterns to avoid in software testing: skipping unit or integration tests, using production data in tests, and not monitoring test outcomes." />
</Frame>

<Callout icon="warning">
  Never use raw production data in test environments unless it has been appropriately anonymized and approved. Using production data in tests can lead to serious compliance and security violations.
</Callout>

Key takeaways

* Automated testing is essential to increase reliability, repeatability, and deployment velocity in ML pipelines.
* Test types:
  * Unit tests: validate isolated functions and logic.
  * Integration tests: validate interactions and artifact compatibility.
  * End-to-end tests: validate the full pipeline and deployed endpoint behavior.
* Apply TDD for deterministic pipeline components and use A/B testing to evaluate models under live traffic.
* Prioritize security (IAM, encryption), monitoring (Model Monitor, logging), backups, and automated recovery.
* Avoid anti-patterns: don’t skip tests, don’t use raw production data without safeguards, and monitor all test outcomes.

<Frame>
  <img alt="The image is a slide summarizing types of tests for machine learning pipelines, including automated, unit, integration, and end-to-end tests, emphasizing their roles in improving reliability and confirming production readiness." />
</Frame>

<Frame>
  <img alt="The image is a summary slide with two points: A/B testing compares model versions fairly, and security, monitoring, and disaster recovery are essential for resilience." />
</Frame>

Links and references

* [AWS CodePipeline](https://aws.amazon.com/codepipeline/)
* [AWS CodeBuild](https://aws.amazon.com/codebuild/)
* [Amazon SageMaker Processing Jobs](https://docs.aws.amazon.com/sagemaker/latest/dg/processing.html)
* [Amazon SageMaker Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html)
* [SageMaker Endpoints (Hosting)](https://docs.aws.amazon.com/sagemaker/latest/dg/hosting_endpoints.html)
* pytest documentation: [https://docs.pytest.org/](https://docs.pytest.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/32db372d-64c7-41fe-a996-c7b717ac10c5" />
</CardGroup>


# Infrastructure as Code Options for ML Workloads

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Deployment-and-Orchestration-of-ML-Workflows/Infrastructure-as-Code-Options-for-ML-Workloads/page

Overview of Infrastructure as Code options and best practices for provisioning, deploying, securing, and operating AWS machine learning environments using CloudFormation, CDK, and the AWS CLI

In this lesson, we review Infrastructure as Code (IaC) options for provisioning and operating machine learning (ML) environments on AWS. Defining infrastructure as code enables repeatability, automation, and scalability—critical for consistent training, testing, and production ML workflows. IaC helps automate complex training environments, standardize inference deployments, and improve observability and compliance across the ML lifecycle.

<Frame>
  <img alt="The image presents information about Infrastructure as Code (IaC) options for machine learning workloads, highlighting improvements in repeatability, scalability, and automation." />
</Frame>

IaC centralizes tasks such as provisioning training compute, configuring data stores and networking, and deploying inference endpoints and monitoring pipelines. This centralization reduces manual errors and accelerates delivery of ML systems into production.

<Frame>
  <img alt="The image is a slide titled &#x22;ML Mission Control: IaC Options for ML Workloads&#x22; highlighting how Infrastructure as Code (IaC) integrates with machine learning lifecycles, specifically in provisioning training environments and deploying inference endpoints." />
</Frame>

Common IaC tools you’ll encounter when building ML systems on AWS:

* [AWS CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation) — declarative templates (YAML/JSON) to provision resources.
* AWS Cloud Development Kit (CDK) — code-first approach using languages like Python or TypeScript; synthesizes to CloudFormation.
* AWS Command Line Interface (CLI) — direct API-level control for scripts and ad-hoc automation.

<Frame>
  <img alt="The image displays options for Infrastructure as Code (IaC) tools provided by AWS for machine learning workloads, including CloudFormation, CDK, and CLI." />
</Frame>

Why use IaC for ML? The primary benefits include:

* Consistency: identical environments across development, staging, and production.
* Automation: orchestrated SageMaker jobs, pipelines, and endpoints.
* Scalability: templates/constructs that adapt to load and resource needs.
* Reproducibility: recreate experiments and pipelines for debugging and compliance.

<Frame>
  <img alt="The image outlines four reasons for using Infrastructure as Code (IAC) for machine learning workloads: Consistency, Automation, Scalability, and Reproducibility. Each reason includes a brief description and an icon." />
</Frame>

Below is a concise comparison to help you choose the right IaC approach for ML workloads.

| Tool           | Best for                                 | Key advantages                                                      | Considerations                            |
| -------------- | ---------------------------------------- | ------------------------------------------------------------------- | ----------------------------------------- |
| CloudFormation | Declarative provisioning for full stacks | Native AWS support, change sets, drift detection, rollbacks         | Template complexity for large systems     |
| AWS CDK        | Dev-friendly, code-first infrastructure  | Reusable constructs, IDE/test integration, generates CloudFormation | Understand synthesis to CloudFormation    |
| AWS CLI        | Quick prototypes & ad-hoc automation     | Fast, scriptable, direct API calls                                  | No drift detection or automated rollbacks |

Below we review each option in more detail and show how it fits typical ML workflows on AWS.

## [AWS CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation)

[AWS CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation) uses declarative templates (YAML/JSON) to define and provision AWS resources. It’s a good fit when you need repeatable, auditable ML infrastructure such as SageMaker endpoints, training pipelines, and accompanying networking and IAM.

Typical workflow:

* Store CloudFormation templates in a deployment repository.
* Build a CI/CD pipeline (e.g., CodeCommit, CodeBuild, [CodePipeline](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline)) to automate stack deployments.
* CloudFormation reads templates and provisions resources (S3 buckets for artifacts, IAM roles, VPCs/security groups, SageMaker model and endpoint configuration, etc.).

CloudFormation pipelines can automate model promotion across environments (for example, dev → staging → prod) and enable controlled updates with ChangeSets.

<Frame>
  <img alt="The image presents key features of AWS CloudFormation for ML, including parameters and mappings, nested stacks/modules, change sets, and drift detection and rollbacks, with automation through CodeCommit/CodePipeline or CDK." />
</Frame>

Key CloudFormation features that help ML workflows:

* Parameters and mappings for reusable, environment-specific templates.
* Nested stacks or modular templates to decompose complex architectures.
* ChangeSets to preview and approve resource changes.
* Drift detection to find manual configuration changes outside IaC.
* Automated rollbacks for failed deployments.

Best practices for CloudFormation with ML:

* Enforce least-privilege IAM policies for SageMaker and execution roles.
* Store model artifacts and large binaries in [Amazon S3](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3) instead of embedding them in templates.
* Avoid launching long-running training jobs directly within stack deployments—trigger training from CI/CD pipelines to avoid stack timeouts and complicated rollbacks.
* Use KMS encryption for sensitive data and VPC endpoints for private access to S3 and ECR.

<Frame>
  <img alt="The image lists best practices for AWS CloudFormation in machine learning, including using least-privilege IAM, storing model artifacts in S3, avoiding long training in stacks, and enabling KMS encryption." />
</Frame>

## AWS CDK

AWS CDK provides a code-first developer experience: you define infrastructure using languages like Python or TypeScript, then the CDK synthesizes your code into CloudFormation templates and deploys them.

Typical flow:

* Write CDK constructs in your chosen language.
* Synthesize to CloudFormation with `cdk synth`.
* Deploy with `cdk deploy` which applies the generated CloudFormation templates to create SageMaker models, endpoints, VPCs, and other resources.

<Frame>
  <img alt="The image is a flowchart titled &#x22;AWS CDK for ML Workloads,&#x22; showing a process from developer to SageMaker model involving AWS CDK and CloudFormation execution." />
</Frame>

Common CDK use cases for ML:

* Define SageMaker Pipelines, training jobs, and inference endpoints directly in Python/TypeScript.
* Integrate infrastructure definitions into CI/CD pipelines for fully automated deployments.
* Create reusable, higher-level constructs to standardize architecture and reduce duplication across teams.

<Frame>
  <img alt="The image describes use cases for AWS CDK in machine learning workloads, highlighting the definition of SageMaker pipelines, CI/CD integration, and reuse of constructs for repeatable architectures." />
</Frame>

Advantages of AWS CDK for ML:

* Abstraction and reuse: encapsulate patterns (for example, a standard inference endpoint) into reusable constructs.
* Developer-friendly workflows: leverage standard languages, unit tests, and IDE tooling.
* Produces CloudFormation templates under the hood, so you retain CloudFormation features such as change sets and rollbacks.

<Frame>
  <img alt="The image highlights the advantages of AWS CDK for ML workloads: abstraction and reuse, software-friendly workflows, and CloudFormation generation." />
</Frame>

Operational and exam tips for CDK and ML:

* Treat CDK code like application code: use version control, code reviews, and unit tests.
* Never hard-code secrets or large model weights in CDK code; reference S3, AWS Secrets Manager, or SSM Parameter Store instead.
* Remember CDK synthesizes to CloudFormation—understand both layers when troubleshooting deployments.

<Frame>
  <img alt="The image provides exam tips for using AWS CDK with machine learning workloads, emphasizing code-based infrastructure, repeatable code over templates, using S3 and Secrets Manager over hardcoding, and synthesizing to CloudFormation." />
</Frame>

## AWS CLI

The AWS CLI maps directly to AWS APIs and is ideal for rapid prototyping, ad-hoc tasks, and simple automation scripts. Unlike CDK or CloudFormation, the CLI has no intermediate template layer.

<Frame>
  <img alt="The image is a flowchart illustrating the use of AWS CLI for infrastructure as code (IAC), showing how developers interact with AWS services via CLI to initiate API calls for creating a training job, a SageMaker model, and a SageMaker endpoint." />
</Frame>

Best uses for the CLI:

* Quickly prototype SageMaker training jobs and endpoints.
* Automate small ML workflows with shell or Python scripts.
* Validate CloudFormation/CDK resources by calling APIs directly before formalizing into templates or constructs.

<Frame>
  <img alt="The image outlines use cases for AWS CLI in Infrastructure as Code (IAC), highlighting rapid prototyping with SageMaker, automating ML workflows with shell scripts, and testing CloudFormation/CDK stacks." />
</Frame>

Strengths and limitations of the CLI:

* Strengths: fast, flexible, and scriptable—great for one-off tasks and experiments.
* Limitations: lacks drift detection, modularity, and automated rollbacks—so it’s less suitable for large, production-grade infrastructure compared to CloudFormation/CDK.

<Frame>
  <img alt="The image is a slide discussing AWS CLI for IAC, highlighting its strengths, such as flexibility and scriptability, and its limitations, like its unsuitability for large production ML infrastructure." />
</Frame>

Example: simplified AWS CLI command to create a SageMaker training job (illustrative):

```bash theme={null}
