# Demo Work on Buildspecyaml file Part 01

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/CodeBuild-and-ECR/Demo-Work-on-Buildspecyaml-file-Part-01/page

Guide to creating and committing a buildspec.yml that builds and tags Docker images with CodeBuild and pushes them to Amazon ECR, plus required environment variables and IAM permissions.

Welcome back. In this lesson you'll create and commit a `buildspec.yml` that builds a Docker image with CodeBuild and pushes it to Amazon ECR. We'll cover a recommended, minimal buildspec, explain the important lines, show how to commit the file from Cloud9, and how to verify the commit in CodeCommit.

Prerequisites

* An ECR repository already created in your AWS account.
* A Cloud9 environment with your source repository checked out.
* A CodeBuild project (or CodePipeline) that will use this `buildspec.yml`.
* The CodeBuild environment image must support Docker and have "Privileged" mode enabled (so Docker can run inside the build container).
* The CodeBuild service role must have permissions to interact with ECR.

Open your Cloud9 editor and the repository you want to build.

<Frame>
  <img alt="The image shows the Amazon Elastic Container Registry interface with a private repository named &#x22;cryptoproject&#x22; listed. It includes details like the repository URI, creation date, and encryption type." />
</Frame>

Create a new file named `buildspec.yml` in the repository and paste the following content. This buildspec:

* Logs in to ECR using the modern `get-login-password` method.
* Computes a short commit SHA to use as an image tag.
* Builds and tags the Docker image.
* Pushes both `latest` and the commit-tagged image to ECR.

```yaml theme={null}
version: 0.2

phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws --version
      # Login to ECR (replace or set AWS_ACCOUNT_ID and AWS_DEFAULT_REGION in project environment)
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=${COMMIT_HASH:-latest}

  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...
      # REPOSITORY_URI should be set in the CodeBuild project environment, e.g. 123456789012.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject
      - docker build -t $REPOSITORY_URI:latest .
      - docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG

  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker images...
      - docker push $REPOSITORY_URI:latest
      - docker push $REPOSITORY_URI:$IMAGE_TAG
```

Key lines explained

* `aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com`\
  Uses the supported way to authenticate Docker to ECR. Do not use the deprecated `aws ecr get-login`.
* `COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)`\
  `CODEBUILD_RESOLVED_SOURCE_VERSION` is set by CodeBuild and typically contains the full commit SHA. The `cut` extracts a short 7-character tag.
* `REPOSITORY_URI`\
  Should be provided as an environment variable in your CodeBuild project and typically looks like `123456789012.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject`.
* Pushing both `latest` and the commit-tagged image gives you a stable `latest` for deployments and a traceable commit history in ECR.

> **lightbulb** Use `aws ecr get-login-password` with `docker login --password-stdin` because `aws ecr get-login` is deprecated and may not be available in newer AWS CLI versions.

Required environment variables and IAM permissions

| Item                         | Purpose                                                    | Example / Notes                                                                                                                                             |
| ---------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `REPOSITORY_URI`             | Target ECR repository (used by `docker tag`/`docker push`) | `123456789012.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject`                                                                                             |
| `AWS_ACCOUNT_ID`             | Used to construct the ECR login endpoint                   | `123456789012`                                                                                                                                              |
| `AWS_DEFAULT_REGION`         | Region for ECR operations                                  | `eu-central-1`                                                                                                                                              |
| CodeBuild privileged mode    | Allows Docker daemon to run inside the build container     | Enabled in CodeBuild project settings                                                                                                                       |
| IAM permissions (ECR)        | Allow build role to push images                            | `ecr:GetAuthorizationToken`, `ecr:BatchCheckLayerAvailability`, `ecr:InitiateLayerUpload`, `ecr:UploadLayerPart`, `ecr:CompleteLayerUpload`, `ecr:PutImage` |
| Source & logging permissions | Allow access to source repo and CloudWatch logs            | `codecommit:GetCommit`, `logs:CreateLogStream`, `logs:PutLogEvents`, etc.                                                                                   |

> **warning** Ensure the CodeBuild project runs in "Privileged" mode (required for Docker-in-Docker) and that the CodeBuild service role includes the ECR-related permissions listed above. Without these, your build will fail when attempting to build or push images.

Commit and push `buildspec.yml` from Cloud9

1. Save the file (Ctrl+S or File → Save).
2. From the Cloud9 terminal run the following commands:

```bash theme={null}
