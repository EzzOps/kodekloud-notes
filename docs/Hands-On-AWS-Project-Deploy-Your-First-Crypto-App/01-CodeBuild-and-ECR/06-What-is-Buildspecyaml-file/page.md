# Authenticate Docker to ECR for the configured AWS CLI profile/region
aws ecr get-login-password --region eu-central-1 \
  | docker login --username AWS --password-stdin 012345678901.dkr.ecr.eu-central-1.amazonaws.com

# Tag a local image with the repository URI
docker tag my-local-image:latest 012345678901.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject:latest

# Push the tagged image to ECR
docker push 012345678901.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject:latest
```

For easier reuse in scripts and CI, replace the account and region with variables (example):

```bash theme={null}
ACCOUNT_ID=012345678901
REGION=eu-central-1
REPO=cryptoproject

aws ecr get-login-password --region $REGION \
  | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

docker tag my-local-image:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO:latest
```

<Callout icon="lightbulb">
  Ensure your AWS CLI is configured with credentials that have the required ECR permissions. Typical actions needed when pushing images include: `ecr:GetAuthorizationToken`, `ecr:BatchCheckLayerAvailability`, `ecr:InitiateLayerUpload`, `ecr:UploadLayerPart`, `ecr:CompleteLayerUpload`, and `ecr:PutImage`. Also verify your CLI region matches the repository's region.
</Callout>

Permissions summary

| Permission                        | Purpose                                                  |
| --------------------------------- | -------------------------------------------------------- |
| `ecr:GetAuthorizationToken`       | Retrieve Docker authentication token for ECR             |
| `ecr:BatchCheckLayerAvailability` | Check which image layers already exist in the repository |
| `ecr:InitiateLayerUpload`         | Start uploading a layer                                  |
| `ecr:UploadLayerPart`             | Upload a chunk of a layer                                |
| `ecr:CompleteLayerUpload`         | Finalize layer upload                                    |
| `ecr:PutImage`                    | Push image manifest to the repository                    |

<Callout icon="warning">
  For production images, enable "Scan on push" to automatically scan images for vulnerabilities. Also follow the principle of least privilege for credentials used by CI systems; prefer short-lived credentials or IAM roles where possible.
</Callout>

Next steps

* Build your Docker image locally (for example, `docker build -t my-local-image .`) and then follow the tag/push steps above.
* Or automate image builds and pushes from your CI pipeline (examples: AWS CodePipeline, GitHub Actions, GitLab CI). Configure the CI runner with appropriate IAM permissions or use an IAM role attached to the build environment.

Links and references

* AWS ECR documentation: [https://docs.aws.amazon.com/ecr/](https://docs.aws.amazon.com/ecr/)
* AWS CLI Command Reference — `get-login-password`: [https://docs.aws.amazon.com/cli/latest/reference/ecr/get-login-password.html](https://docs.aws.amazon.com/cli/latest/reference/ecr/get-login-password.html)
* Docker Hub: [https://hub.docker.com/](https://hub.docker.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/37195f61-a068-4f6c-9ccc-0bd66b358449/lesson/b78585c0-4b2d-45b6-b908-226eedb78a09" />
</CardGroup>


# What is Buildspecyaml file

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/CodeBuild-and-ECR/What-is-Buildspecyaml-file/page

Explains using a buildspec.yml for AWS CodeBuild to build and push Docker images to Amazon ECR, covering phases, env variables, privileged mode, and IAM requirements.

Well, now that we have set up our ECR repository, how do we actually build a Docker image programmatically? CodeBuild runs the build for us, but you need a build specification to tell CodeBuild which steps to execute.

<Frame>
  <img alt="The image features the AWS CodeBuild logo, which includes a crane graphic with code symbols and the text &#x22;AWS CodeBuild&#x22; beneath it." />
</Frame>

When building a Docker image locally, you run commands in a terminal. For automated builds with AWS CodeBuild, you define those steps in a build specification file named `buildspec.yml` (or `buildspec.yaml`). This YAML file describes the lifecycle of the build and the commands to run in each phase.

<Callout icon="lightbulb">
  Recommendation: Use the `buildspec.yml` filename (lowercase `.yml`) for consistency; `.yaml` is functionally equivalent.
</Callout>

<Frame>
  <img alt="The image displays the text &#x22;Buildspec.yml&#x22; and &#x22;create&#x22; with a gear icon, likely referring to creating a buildspec.yml file used in build configurations." />
</Frame>

Below is a typical `buildspec.yml` for building a Docker image and pushing it to Amazon ECR. The file is organized into sections: `version`, `env > variables`, and `phases` (including `pre_build`, `build`, and `post_build`).

```yaml theme={null}
version: 0.2
env:
  variables:
    IMAGE_REPO_NAME: "<Your-ECR-Repo-Name>"
    IMAGE_TAG: "<Your-Tag>"
phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
      - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker image...
      - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
```

Summary of the main `buildspec.yml` sections:

| Section           | Purpose                                                                         | Example / Notes                                                                         |
| ----------------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `version`         | Declares the buildspec schema version.                                          | `0.2` is current and recommended.                                                       |
| `env > variables` | Define static environment variables available during the build.                 | Replace placeholders like `"<Your-ECR-Repo-Name>"` and `"<Your-Tag>"` with your values. |
| `phases`          | Breaks the build into lifecycle stages: `pre_build`, `build`, and `post_build`. | Customize these phases for your language or workflow.                                   |

Phases explained:

* pre\_build: Preparation tasks such as authenticating to ECR, installing dependencies, or setting up credentials. The example uses `aws ecr get-login-password` to log Docker in to ECR.
* build: Core build steps — for Docker this includes `docker build` and `docker tag`.
* post\_build: Finalization steps such as pushing the image to ECR, uploading artifacts to S3, or notifying CI/CD systems.

Common requirements and best practices when using Docker with CodeBuild:

* Environment variables:
  * Ensure `AWS_ACCOUNT_ID` and `AWS_DEFAULT_REGION` are defined either in the CodeBuild project environment variables or replaced with literal values in the `buildspec.yml`. They are not injected automatically unless configured.
* Privileged mode:
  * To execute Docker commands inside CodeBuild, enable "Privileged" mode on the build environment and use an image that includes Docker (or supports Docker-in-Docker).
* Service role permissions:
  * The CodeBuild service role must include ECR permissions such as:
    * `ecr:GetAuthorizationToken`
    * `ecr:BatchCheckLayerAvailability`
    * `ecr:PutImage`
    * `ecr:InitiateLayerUpload`
    * `ecr:UploadLayerPart`
    * `ecr:CompleteLayerUpload`
  * Add any additional permissions required by your workflow (KMS, S3, CloudWatch Logs, etc.).

<Callout icon="warning">
  Important: Without Privileged mode enabled or the appropriate service-role IAM permissions, Docker commands and pushing to ECR will fail. Verify both the build environment settings and the IAM policy before running the build.
</Callout>

Example variations and tips:

* For language-specific projects (Java, Node, Python), use `pre_build` to install dependencies, `build` to compile/package artifacts, and `post_build` to upload artifacts or publish releases.
* Use environment variables to parameterize repository names and tags so a single `buildspec.yml` can work across environments (dev, staging, prod).
* If you use KMS-encrypted images or private S3 artifacts, ensure the service role has access to KMS/S3 as needed.

Links and References

* [AWS CodeBuild User Guide](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html)
* [Pushing a Docker container image to Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html)
* [CodeBuild buildspec reference](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html)

With this `buildspec.yml` in your repository and a configured CodeBuild project, CodeBuild will run the defined steps and produce your Docker image in ECR automatically.

That's it for this lesson. Speak with you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/37195f61-a068-4f6c-9ccc-0bd66b358449/lesson/2dd2b175-8bcd-4e14-9601-0a57f2ab8442" />
</CardGroup>
