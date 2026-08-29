# Automate task definition registration

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Task-definition-Image-tags-in-production-and-Load-Balancer/Automate-task-definition-registration/page

Automating registration of Amazon ECS task definitions in CI/CD using CodeBuild to version task-definition.json, push images to ECR, and register new revisions.

Welcome — in this lesson you'll learn how to register an Amazon ECS task definition as part of a CI/CD pipeline. Instead of configuring the task definition in the ECS console, keep a `task-definition.json` file in your repository and have CodeBuild register it on every push.

This approach ensures your task definition is versioned with your code and that each change can create a new ECS revision automatically.

## Overview

Steps covered here:

1. Build, tag, and push your Docker image to Amazon ECR using CodeBuild.
2. Keep an ECS task definition (Fargate example) in source control.
3. Register the task definition from CodeBuild using `aws ecs register-task-definition`.
4. (Optional) Inject the CI image tag into the task definition before registering.

Useful references:

* [Amazon ECS Task Definitions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)
* [AWS CodeBuild User Guide](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html)
* [Amazon ECR Getting Started](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html)

<Callout icon="lightbulb">
  Store your ECS task definition in source control so its changes are auditable and reproducible. Use the CI pipeline to register new revisions automatically.
</Callout>

## Example CodeBuild buildspec (build, tag, push)

This representative `buildspec.yml` logs into ECR, builds and tags the image, and pushes both `latest` and a short commit-hash tag. Note the use of `CODEBUILD_RESOLVED_SOURCE_VERSION` to derive a short commit hash for the image tag.

```yaml theme={null}
version: 0.2
phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin 666234738304.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=${COMMIT_HASH:-latest}
  build:
    commands:
      - echo Build started on `date`...
      - echo Building the Docker image...
      - docker build -t $REPOSITORY_URI:latest .
      - docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG
  post_build:
    commands:
      - echo Build completed on `date`...
      - echo Pushing the Docker image...
      - docker push $REPOSITORY_URI:latest
      - docker push $REPOSITORY_URI:$IMAGE_TAG
```

## Task definition file (task-definition.json)

Create a `task-definition.json` file in the repository. The example below is a basic Fargate task definition configured to use `awslogs`. Adjust `image` URI, container name, CPU/memory, and other values to match your environment.

```json theme={null}
{
  "family": "aws-crypto-app",
  "containerDefinitions": [
    {
      "name": "kodeduk-crypto-coin",
      "image": "666234738044.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject:latest",
      "memory": 512,
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80,
          "protocol": "tcp"
        },
        {
          "containerPort": 5000,
          "hostPort": 5000,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "environment": [],
      "mountPoints": [],
      "volumesFrom": [],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-create-group": "true",
          "awslogs-group": "/ecs/aws-microservice",
          "awslogs-region": "eu-central-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "secretOptions": []
    }
  ],
  "placementConstraints": [],
  "requiresCompatibilities": [
    "FARGATE"
  ],
  "cpu": "1024",
  "memory": "3072",
  "runtimePlatform": {
    "cpuArchitecture": "ARM64",
    "operatingSystemFamily": "LINUX"
  }
}
```

## Register the task definition from CodeBuild

To register the task definition as part of the build, call the AWS CLI `register-task-definition` in the `post_build` phase. The important command is:

```yaml theme={null}
- aws ecs register-task-definition --cli-input-json file://task-definition.json
```

A minimal `post_build` section with registration looks like this:

```yaml theme={null}
post_build:
  commands:
    - echo Build completed on `date`
    - echo Pushing the Docker image...
    - docker push $REPOSITORY_URI:latest
    - docker push $REPOSITORY_URI:$IMAGE_TAG
    - aws ecs register-task-definition --cli-input-json file://task-definition.json
```

### Inject the built image tag into the task definition (recommended)

If your `task-definition.json` contains a static `:latest` image, you can update the file in CI to reference the pushed commit-tagged image before registration. This ensures the registered task definition references the exact image pushed by the current build.

Example using `jq` to update the JSON and register:

```yaml theme={null}
post_build:
  commands:
    - echo Build completed on `date`
    - docker push $REPOSITORY_URI:latest
    - docker push $REPOSITORY_URI:$IMAGE_TAG
    - export IMAGE_URI="$REPOSITORY_URI:$IMAGE_TAG"
    - jq --arg img "$IMAGE_URI" '.containerDefinitions[0].image = $img' task-definition.json > taskdef.tmp.json
    - mv taskdef.tmp.json task-definition.json
    - aws ecs register-task-definition --cli-input-json file://task-definition.json
```

This pattern avoids registering a task definition that still points to `:latest` and gives you an explicit immutable image reference per revision.

<Callout icon="warning">
  Ensure the CodeBuild service role has permissions to call `ecs:RegisterTaskDefinition` and `ecr:GetAuthorizationToken` / `ecr:BatchCheckLayerAvailability` / `ecr:GetDownloadUrlForLayer` / `ecr:PutImage` as needed. Missing IAM permissions will cause the build to fail.
</Callout>

## Files in the repository

| File                   | Purpose                                                    | Example / Notes                                       |
| ---------------------- | ---------------------------------------------------------- | ----------------------------------------------------- |
| `buildspec.yml`        | CodeBuild pipeline definition — build, tag, push, register | See examples above                                    |
| `task-definition.json` | ECS task definition versioned in source control            | Update `image`, CPU, memory to match your environment |

## Commit and push

Commit the task definition and buildspec to your repository so CodeBuild picks up the changes:

```bash theme={null}
