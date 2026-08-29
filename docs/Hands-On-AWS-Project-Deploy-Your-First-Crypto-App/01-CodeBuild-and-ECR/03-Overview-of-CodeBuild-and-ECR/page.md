# Overview of CodeBuild and ECR

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/CodeBuild-and-ECR/Overview-of-CodeBuild-and-ECR/page

Overview of AWS CodeBuild and ECR explaining managed CI builds, Docker image storage, and steps to build and push images with buildspec.yml

Hello and welcome to a focused overview of two essential AWS developer tools: AWS CodeBuild and AWS Elastic Container Registry (ECR). This lesson explains how CodeBuild automates builds and tests in a managed CI service and how ECR stores and manages Docker/OCI images used across your deployment pipelines.

We'll cover:

* What CodeBuild does and when to use it
* What ECR provides and why it's helpful
* A practical next step with a sample `buildspec.yml` to build and push Docker images to ECR

## CodeBuild

AWS CodeBuild is a fully managed continuous integration service that compiles source code, runs tests, and produces deployable artifacts. Because AWS manages the build infrastructure, scaling, and maintenance, you can focus on writing build steps and test logic instead of operating CI servers.

CodeBuild at a glance:

| Capability            | Description                                                                | Example                                      |
| --------------------- | -------------------------------------------------------------------------- | -------------------------------------------- |
| Source integrations   | Connects to CodeCommit, S3, GitHub, GitHub Enterprise, Bitbucket           | Push code to GitHub and trigger CodeBuild    |
| Build configuration   | Uses a `buildspec.yml` to define phases, commands, env vars, and artifacts | `buildspec.yml` in repository root           |
| Build environments    | Use managed images or your custom Docker images                            | `aws/codebuild/standard:6.0` or custom image |
| Logging & artifacts   | Sends logs to CloudWatch Logs and artifacts to S3                          | Build logs in CloudWatch; artifacts in S3    |
| Scalability & pricing | Runs builds in parallel and billed per build-minute                        | Pay-as-you-go for build minutes              |

Key benefits:

* Fully managed build infrastructure and scaling
* Native integration with AWS services (CodePipeline, S3, CloudWatch)
* Flexible build environments including custom Docker images

<Frame>
  <img alt="The image is an overview of CodeBuild, highlighting its features: automated CI/CD, scalability, integration with AWS services, and pay-as-you-go pricing." />
</Frame>

## Elastic Container Registry (ECR)

AWS Elastic Container Registry (ECR) is a fully managed container image registry for storing, versioning, and sharing Docker and OCI images. ECR integrates with Amazon ECS, Amazon EKS, and CodeBuild so you can push/pull images as part of CI/CD workflows.

ECR highlights:

| Feature                  | Benefit                                                |
| ------------------------ | ------------------------------------------------------ |
| Private repositories     | Secure, private image storage for your account         |
| ECR Public               | Option to host public images for community consumption |
| Access control           | Repository policies + IAM for fine-grained access      |
| Image scanning           | Find vulnerabilities via integrated scanning tools     |
| Encryption               | Images encrypted at rest with AWS KMS                  |
| Lifecycle policies       | Automatically prune older or unused images             |
| Cross-region replication | Replicate images to other regions for resilience       |

Note: ECR repositories are regional by default. Use cross-region replication to copy images to other AWS Regions for higher availability and multi-region deployments.

<Frame>
  <img alt="The image provides an overview of ECR, highlighting its features: container image storage, support for private repositories, security and compliance, and high availability and durability." />
</Frame>

## Next steps — build and push image to ECR

A practical next step is to create an ECR repository and configure a CodeBuild project that builds your Docker image and pushes it to ECR. The typical flow in `buildspec.yml` is:

1. Authenticate to ECR
2. Build the Docker image
3. Tag the image for the target ECR repository
4. Push the image to ECR

Example `buildspec.yml` (simplified):

```yaml theme={null}
version: 0.2

phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws --version
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
  build:
    commands:
      - echo Build started on `date`
      - docker build -t my-app:latest .
      - docker tag my-app:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/my-repo:latest
  post_build:
    commands:
      - echo Pushing the Docker image...
      - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/my-repo:latest

artifacts:
  files:
    - '**/*'
```

Replace the placeholders with your environment values:

* `AWS_ACCOUNT_ID` — your AWS account ID
* `AWS_DEFAULT_REGION` — the region of your ECR repository
* `my-repo` — your ECR repository name

<Callout icon="lightbulb">
  Tip: Use a `buildspec.yml` to automate Docker build, tag, and push steps. Ensure CodeBuild has an IAM role with permissions for ECR (push/pull), S3 (if storing artifacts), and CloudWatch Logs for build logs.
</Callout>

<Callout icon="warning">
  Warning: Grant least-privilege permissions to the CodeBuild service role. Do not attach overly broad policies (like `AdministratorAccess`) to CodeBuild — limit actions to only the ECR and S3 resources the build requires.
</Callout>

## References and further reading

* AWS CodeBuild Documentation: [https://docs.aws.amazon.com/codebuild/](https://docs.aws.amazon.com/codebuild/)
* Amazon ECR Documentation: [https://docs.aws.amazon.com/ecr/](https://docs.aws.amazon.com/ecr/)
* AWS CodePipeline (CI/CD Pipeline): [https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline)
* AWS CloudWatch Logs: [https://learn.kodekloud.com/user/courses/aws-cloudwatch](https://learn.kodekloud.com/user/courses/aws-cloudwatch)

## Wrapping up

AWS CodeBuild and ECR together provide a managed, scalable, and secure way to build application artifacts and store container images inside AWS. After configuring ECR and a CodeBuild project, integrate CodeBuild into CodePipeline to automate the full CI/CD flow. See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/37195f61-a068-4f6c-9ccc-0bd66b358449/lesson/27aa2751-3bb5-4736-9f18-116ef640790c" />
</CardGroup>
