# AWS CodePipeline CodeBuild and CodeDeploy for ML

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Deployment-and-Orchestration-of-ML-Workflows/AWS-CodePipeline-CodeBuild-and-CodeDeploy-for-ML/page

Automating MLOps CI/CD on AWS using CodePipeline, CodeBuild, SageMaker, and CodeDeploy with secure practices, testing, model registry, and safe rollout strategies.

In this lesson we’ll apply DevOps principles to machine learning by building an automated MLOps CI/CD pipeline on AWS. The pipeline uses AWS CodePipeline for orchestration, CodeBuild for building and testing, and CodeDeploy for controlled rollouts where appropriate. Amazon SageMaker is the primary runtime for training, model registry, and serving endpoints.

Key goals:

* Automate reproducible model training and delivery.
* Validate models with automated tests and metrics gates.
* Deploy models safely using traffic-shifting or rollout strategies.
* Secure the pipeline and artifacts using least-privilege IAM, KMS, and network controls.

High-level workflow:

* CodePipeline orchestrates stages from source to deployment.
* CodeBuild installs dependencies, runs tests, and creates artifacts or container images.
* SageMaker runs training jobs, registers models, and hosts endpoints.
* CodeDeploy provides controlled rollouts for compute targets it supports (ECS, Lambda, EC2).

The following diagram shows the overall concept of an ML CI/CD pipeline using AWS developer tools.

<Frame>
  <img alt="The image is a flowchart demonstrating the implementation of ML CI/CD using AWS services: CodePipeline, CodeBuild, CodeDeploy, and Amazon SageMaker." />
</Frame>

Why automate ML with CI/CD?

* Manual workflows are error-prone, slow to iterate, and hard to reproduce.
* CI/CD enforces automated builds, tests, and structured deployments so results are repeatable and delivery is faster.

Compare manual ML workflows with CI/CD automation:

<Frame>
  <img alt="The image compares the use of AWS Code Services for ML automation with and without CI/CD. It highlights issues like manual steps and frequent errors without CI/CD and benefits of automation with it." />
</Frame>

Core pipeline orchestration

* CodePipeline coordinates stages such as Source → Build → Train → Validate → Deploy → Monitor.
* It triggers CodeBuild to run unit tests, data checks, packaging, and container image builds.
* Pipeline stages call SageMaker to run training jobs and register models in a model registry.
* For serving, prefer SageMaker native endpoint features; for other compute targets use CodeDeploy for blue/green or canary rollouts.

The architecture below shows how CodePipeline integrates CodeBuild, CodeDeploy, and SageMaker.

<Frame>
  <img alt="The image illustrates how AWS services support ML CI/CD, featuring CodeDeploy, CodeBuild, SageMaker, and CodePipeline as key components in the process." />
</Frame>

End-to-end flow example

1. Developer or data engineer pushes code or data to the source repo.
2. CodePipeline detects the commit and starts the pipeline.
3. CodeBuild bundles dependencies, runs tests, and produces an artifact or container image.
4. The pipeline triggers a SageMaker training job or uses the built image for training.
5. After validation, the model is registered and deployed to an endpoint or compute target.
6. Monitoring and automated rollback gates ensure safety.

Visual flow of this sequence:

<Frame>
  <img alt="The image illustrates how AWS services support ML CI/CD, featuring CodeDeploy, CodeBuild, SageMaker, and CodePipeline as key components in the process." />
</Frame>

CodeBuild: packaging, testing, and artifacts

* Install dependencies, run unit/integration tests, and execute data validation.
* Create model packages or build container images pushed to ECR.
* Produce artifacts consumed by SageMaker training or later deployment stages.

<Frame>
  <img alt="The image illustrates a workflow for automating model packaging using AWS CodeBuild, starting with source code and leading to build artifacts or an ML container." />
</Frame>

Deployment strategies for ML models

* Blue/Green: provision a parallel environment and switch traffic once tests pass.
* Canary: route a small % of traffic to the new model, then increase if metrics are healthy.
* Shadow Testing: mirror production traffic to the new model without affecting user responses.

Use SageMaker variant-weighting and traffic-shifting for endpoint deployments, or orchestrate the rollout from CodePipeline. For other compute types, leverage CodeDeploy’s strategies.

<Frame>
  <img alt="The image is a flowchart showing how AWS CodeDeploy manages model releases using deployment strategies, specifically Blue/Green and Canary." />
</Frame>

Orchestrating stages and artifacts
A well-structured pipeline produces artifacts and test outputs at each stage so downstream stages can validate automatically and make branching decisions (promote, rollback, or notify).

Security practices for ML CI/CD

* Use least-privilege IAM roles for CodePipeline, CodeBuild, SageMaker, and CodeDeploy.
* Encrypt artifacts and model packages with AWS KMS.
* Run SageMaker (and other compute) in a private VPC and restrict network access.

<Frame>
  <img alt="The image outlines steps for securing ML CI/CD on AWS, including CI/CD services, IAM roles with KMS encryption, and secure SageMaker deployment using a private VPC." />
</Frame>

Choosing the right rollout from your model registry

<Frame>
  <img alt="The image outlines safe deployment strategies for ML models, including Blue/Green, Canary, and Shadow Testing, starting from a Model Registry." />
</Frame>

Automated validation and gating

* Build automated checks into the pipeline: unit tests, data schema validations, data drift checks, and model evaluation metrics compared against baselines.
* Only promote models that meet the acceptance criteria; on failure, the pipeline should stop and notify the team.

<Frame>
  <img alt="The image is a flowchart showing automated testing and validation in a CI/CD pipeline. It outlines steps from the pipeline to automated tests, leading to deployment if tests pass, or stopping and fixing if tests fail." />
</Frame>

Common CI/CD anti-patterns to avoid

* Skipping automated tests to save time.
* Hardcoding secrets into pipeline scripts or artifacts.
* Failing to version control code and model artifacts, preventing reliable rollbacks.

<Frame>
  <img alt="The image lists common CI/CD pitfalls: &#x22;Skipping Tests,&#x22; &#x22;Hardcoding Secrets,&#x22; and &#x22;No Version Control.&#x22; It includes icons for each issue and suggests how to avoid them." />
</Frame>

<Callout icon="warning">
  Avoid these pitfalls: always include automated tests, store secrets in a secrets manager (for example, AWS Secrets Manager (`https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html`) or `Systems Manager Parameter Store`), and keep all code and model artifacts in versioned storage.
</Callout>

Quick reference: AWS components and responsibilities

| Component       |                                Primary role in ML CI/CD | Examples                                                       |
| --------------- | ------------------------------------------------------: | -------------------------------------------------------------- |
| CodePipeline    |               Orchestrates stages and connects services | Replaceable stages: Source → Build → Train → Validate → Deploy |
| CodeBuild       |  Builds artifacts, runs tests, creates container images | Buildspec runs unit tests, data checks, pushes image to ECR    |
| SageMaker       | Training, model registry, hosting, and traffic shifting | Training jobs, Model Registry, Endpoint variant-weighting      |
| CodeDeploy      |       Controlled rollouts for supported compute targets | Blue/Green or Canary for EC2, ECS, Lambda                      |
| KMS / IAM / VPC |                          Security and network isolation | KMS for artifact encryption, IAM least-privilege roles         |

Recommendations and best practices

* Automate packaging, validation, and deployment steps; ensure observability and monitoring at each stage.
* Enforce security using IAM least-privilege, KMS encryption, and VPC isolation for compute.
* Gate deployments with robust automated tests and model-metric thresholds.
* Use blue/green, canary, or shadow testing to minimize risk during rollouts.
* Maintain versioned storage for code, artifacts, and models to enable safe rollbacks.

<Callout icon="lightbulb">
  Automate packaging, validation, and deployment as part of your pipeline and monitor each stage. This reduces risk, improves reproducibility, and enables faster, safer model delivery.
</Callout>

Links and references

* CodePipeline: [https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline)
* SageMaker: [https://learn.kodekloud.com/user/courses/aws-sagemaker](https://learn.kodekloud.com/user/courses/aws-sagemaker)
* CodeBuild docs: [https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html)
* CodeDeploy: [https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline) (see CodeDeploy module)
* IAM best practices: [https://learn.kodekloud.com/user/courses/aws-iam](https://learn.kodekloud.com/user/courses/aws-iam)
* AWS KMS overview: [https://docs.aws.amazon.com/kms/latest/developerguide/overview.html](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)
* AWS Secrets Manager: [https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)

By combining CodePipeline, CodeBuild, SageMaker, and CodeDeploy with secure practices and automated validation, you can build an MLOps pipeline that enables repeatable training, safe deployments, and rapid model iteration.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/bc6cf425-9e53-4e1d-8a25-eaf702c637d4" />
</CardGroup>
