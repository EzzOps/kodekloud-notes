# buildspec.yml
version: 0.2

phases:
  pre_build:
    commands:
      - echo "Starting pre_build..."
      - export REPOSITORY_URI=666234738044.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject
      - export REGISTRY=$(echo $REPOSITORY_URI | cut -d'/' -f1)
      - aws --version
      - echo "Logging in to Amazon ECR..."
      - $(aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $REGISTRY)
      - export COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - export IMAGE_TAG=${COMMIT_HASH:-latest}
      - export CONTAINER_NAME="kodekloud-crypto-coin"

  build:
    commands:
      - echo "Build started on $(date)"
      - docker build -t $REPOSITORY_URI:$IMAGE_TAG .
      - docker push $REPOSITORY_URI:$IMAGE_TAG
      - docker tag $REPOSITORY_URI:$IMAGE_TAG $REPOSITORY_URI:latest
      - docker push $REPOSITORY_URI:latest
      - echo "Build finished on $(date)"

  post_build:
    commands:
      - echo "Writing image definitions file..."
      - printf '[{"name":"%s","imageUri":"%s"}]' "$CONTAINER_NAME" "$REPOSITORY_URI:$IMAGE_TAG" > imagedefinitions.json
      - sed -i "s|REPOSITORY_URI_PLACEHOLDER|$REPOSITORY_URI:${IMAGE_TAG}|g" task-definition.json
      - aws ecs register-task-definition --cli-input-json file://task-definition.json

artifacts:
  files:
    - imagedefinitions.json
```

<Callout icon="lightbulb">
  The ECS deploy action expects `imagedefinitions.json` to be an array of objects with `name` (container name) and `imageUri` (image URI including the tag). Example: `[{"name":"your-container-name","imageUri":"<registry>/<repo>:<tag>"}]`.
</Callout>

## 3) Commit, push, and validate the pipeline run

After editing your app (for example, changing the login page text), commit and push the changes to trigger the pipeline:

```bash theme={null}
git add .
git commit -m "CodePipeline deployment change"
git push origin master
```

CodePipeline will automatically start a new execution and progress through Source → Build → Deploy.

<Frame>
  <img alt="The image shows an AWS CodePipeline interface for a project named &#x22;crypto-app,&#x22; displaying two stages: &#x22;Source,&#x22; which has succeeded, and &#x22;Build,&#x22; which is in progress." />
</Frame>

### What to look for in CodeBuild logs

In the Build stage logs you should see entries that indicate the `imagedefinitions.json` file is created and the task definition is registered, similar to:

```text theme={null}
[Container] 2024/03/24 13:46:02.036 Running command echo 'Writing image definitions file...'
[Container] 2024/03/24 13:46:02.036 Running command printf '[{"name":"kodekloud-crypto-coin","imageUri":"%s"}]' $REPOSITORY_URI:$IMAGE_TAG > imagedefinitions.json
[Container] 2024/03/24 13:46:02.043 Running command sed -i "s|REPOSITORY_URI_PLACEHOLDER|${REPOSITORY_URI}:${IMAGE_TAG}|g" task-definition.json
[Container] 2024/03/24 13:46:02.052 Running command aws ecs register-task-definition --cli-input-json file://task-definition.json
```

## 4) Observe ECS deployment and health

Once the Deploy stage starts, ECS will create a new deployment and start tasks using the pushed image. Monitor the ECS console for task activity, health checks, and load balancer status.

<Frame>
  <img alt="This image shows the AWS Elastic Container Service (ECS) console displaying details for a crypto-app, including task information and container details." />
</Frame>

<Frame>
  <img alt="The image is a screenshot of the Amazon Elastic Container Service (ECS) console, showing the health and metrics of a service named &#x22;crypto-app&#x22; within a production cluster. The service is active, with tasks running and a load balancer in place." />
</Frame>

<Frame>
  <img alt="The image shows the Amazon Elastic Container Service (ECS) interface with a focus on deployments for a service named &#x22;crypto-app.&#x22; It lists deployment details, statuses, events, and associated tasks." />
</Frame>

Open the Tasks view to confirm new tasks are launching and old ones are draining. ECS’s rolling update strategy will replace tasks gradually and — if configured — automatically roll back failed deployments. After deployment completes, retrieve the load balancer DNS and verify the app (for example, confirm the updated login text).

## 5) Inspect the imagedefinitions.json artifact and commits

The `imagedefinitions.json` produced by the Build stage is stored in the CodePipeline artifact S3 bucket. You can download the artifact from the pipeline’s artifacts to inspect it. The file contains entries with container names and the image URIs (including commit tag). Example:

```json theme={null}
[
  {
    "name": "kodekloud-crypto-coin",
    "imageUri": "666234738044.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject:59bee47"
  }
]
```

Validate the commit hash in CodeCommit by viewing the repository’s commits:

<Frame>
  <img alt="The image shows the AWS CodeCommit interface displaying a list of commits for the &#x22;aws-microservice-project&#x22; repository. It includes details like commit IDs, messages, dates, and author information." />
</Frame>

## Quick reference

| Item                                     | Purpose                                                      | Example / Note                                                                  |
| ---------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| Artifact consumed by ECS deploy          | Informs CodePipeline/ECS which container to update           | `imagedefinitions.json`                                                         |
| `imagedefinitions.json` format           | Array of container objects                                   | `[{"name":"kodekloud-crypto-coin","imageUri":"<registry>/<repo>:<tag>"}]`       |
| Task definition registration             | Optional step in buildspec to register a new task definition | `aws ecs register-task-definition --cli-input-json file://task-definition.json` |
| Recommended provider for rolling updates | Use Amazon ECS provider in CodePipeline                      | Do not use ECR Blue/Green unless you intend that model                          |

## Summary

* Add a Deploy stage in CodePipeline and select **Amazon ECS** as the provider.
* Update `buildspec.yml` so CodeBuild builds/pushes the image and emits `imagedefinitions.json`.
* Commit and push changes to your source repository to trigger an automated pipeline run.
* Inspect CodeBuild logs, the `imagedefinitions.json` artifact in S3, and ECS console to confirm rolling deployment.
* The full flow is automated: push → build → deploy, with ECS managing rolling updates and optional rollback.

Further reading and references:

* [AWS CodePipeline Documentation](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html)
* [Amazon ECS Deploy Action in CodePipeline](https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-ECS.html)
* [AWS CodeBuild Buildspec Reference](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html)

Congratulations — you now have an end-to-end automated deployment pipeline for your crypto-app using CodeCommit, CodeBuild, CodePipeline, ECR, and ECS.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/d608c5f9-ae0c-4023-864f-b30b3099cd6f/lesson/0387fdad-a933-4d9d-9565-6537af714e40" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/d608c5f9-ae0c-4023-864f-b30b3099cd6f/lesson/25cc15e2-afff-4cd8-98ae-8f3741deb216" />
</CardGroup>


# Overview of CodePipeline

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/CodePipeline-automated-deployment/Overview-of-CodePipeline/page

Overview of AWS CodePipeline automating CI/CD workflows to build, test, and deploy applications from source repositories to runtime environments like Amazon ECS.

Welcome — in this lesson you'll learn what AWS CodePipeline is and how it streamlines deployments for your applications using an automated CI/CD flow.

At a high level, CodePipeline orchestrates an ordered sequence of stages (source → build → test → deploy) so code changes flow from a repository to a runtime environment with minimal manual intervention. When integrated with CodeBuild, CodePipeline detects source changes, triggers builds, and advances build artifacts into deployment stages such as Amazon ECS to update running services.

Why use CodePipeline? It breaks the release process into observable, automatable steps so you can isolate failures quickly, enforce quality gates, and accelerate safe deliveries.

How CodePipeline typically works (high level):

1. A change is pushed to the source repository (for example, CodeCommit or GitHub).
2. CodePipeline detects that change and pulls the latest code (Source stage).
3. The code moves into a Build stage (for example, CodeBuild) that compiles, tests, and produces artifacts.
4. Artifacts are passed forward to Test and Deploy stages; the Deploy stage updates the runtime environment (for example, an ECS service).
5. Optional Approval stages can require manual confirmation before progressing to production.

Key pipeline stages (typical):

| Stage               | Purpose                                          | Example actions / tools                          |
| ------------------- | ------------------------------------------------ | ------------------------------------------------ |
| Source              | Detects and retrieves the latest code            | `AWS CodeCommit`, `GitHub`, `Amazon S3`          |
| Build               | Compiles, runs unit tests, and creates artifacts | `AWS CodeBuild`, `Jenkins`                       |
| Test (optional)     | Runs integration or acceptance tests             | `CodeBuild`, third‑party testing tools           |
| Deploy              | Deploys artifacts to target environment          | `AWS CodeDeploy`, `Amazon ECS`, `CloudFormation` |
| Approval (optional) | Manual gate before proceeding                    | Manual approval via console or SNS               |

<Frame>
  <img alt="The image is an overview diagram of AWS CodePipeline showing the stages of the pipeline: Source Stage using AWS CodeCommit, followed by Build Stage, Deploy Stage, and ending with deployment to Amazon Elastic Container Service (Amazon ECS)." />
</Frame>

Core capabilities and behaviors of AWS CodePipeline

* CI/CD orchestration: Automates the flow from source to deployment, enabling continuous integration and continuous delivery (CI/CD).
* Pluggable actions: Orchestrates actions across AWS services (CodeBuild, Lambda, ECS, S3, CloudFormation) and third‑party tools (GitHub, Jenkins).
* Artifact passing: Artifacts produced in one stage are passed to downstream stages so each stage operates on the exact outputs of the previous step.
* Event-driven triggers: Pipelines can start automatically on source changes, be triggered manually, or started via scheduled or external events.
* Observability and notifications: Execution history, stage logs, and integration with CloudWatch, Amazon SNS, and other monitoring tools provide visibility and alerting for pipeline runs.
* Managed service: CodePipeline is serverless from the user perspective — no control plane infrastructure to provision or manage.

<Callout icon="lightbulb">
  Remember: CodePipeline orchestrates actions but does not replace them. Each action (for example, a CodeBuild project or an ECS deploy) executes with its own IAM permissions and configuration. Ensure actions have the required roles and access to the artifacts and resources they need.
</Callout>

<Frame>
  <img alt="The image is an overview of AWS CodePipeline, highlighting its features: continuous integration and delivery, integration with AWS and third-party tools, real-time monitoring, notifications, scalability, and flexibility. Each feature is represented in colorful boxes with icons." />
</Frame>

Scaling and usage patterns

* Small teams: Simple linear pipelines (Source → Build → Deploy) provide fast feedback and automated deployments.
* Complex enterprises: Pipelines can include parallel actions, multiple environments (dev/stage/prod), manual approvals, and cross-account deployments.
* Integration: CodePipeline integrates with your existing toolchain while giving you end-to-end visibility for every release.

Next steps

* Build a sample pipeline: Connect `CodeCommit` → `CodeBuild` → `ECS` to see artifacts flow automatically from source to running containers.
* Add testing and approval gates: Enforce quality checks and manual approvals before production rollouts.
* Monitor and iterate: Use CloudWatch and SNS to observe pipeline runs and alert on failures.

Links and references

* [AWS CodePipeline Documentation](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html)
* [AWS CodeBuild Documentation](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html)
* [Amazon ECS Documentation](https://docs.aws.amazon.com/ecs/latest/developerguide/)

That concludes this lesson — you now understand what CodePipeline is, its core stages, and how it helps automate deployments from CodeCommit to ECS.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/d608c5f9-ae0c-4023-864f-b30b3099cd6f/lesson/79de2cda-6b82-4c9d-a11e-82734b8f8347" />
</CardGroup>
