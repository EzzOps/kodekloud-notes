# from your repo root
git status
git add .
git commit -m "Add task definition"
git push origin main
```

## Trigger a build and inspect results

Start a build in CodeBuild (or let your CI trigger it). When the build completes, the logs will show the `aws ecs register-task-definition` call and the CLI will return the registered task definition metadata similar to this example:

```json theme={null}
{
  "name": "kodeklud-crypto-coin",
  "image": "666234783044.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject:latest",
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
  "secretOptions": [],
  "family": "aws-crypto-app",
  "executionRoleArn": "arn:aws:iam::666234783044:role/ecsTaskExecutionRole",
  "networkMode": "awsvpc",
  "revision": 2,
  "volumes": [],
  "status": "ACTIVE",
  "requiresAttributes": [
    {
      "name": "com.amazonaws.ecs.capability.logging-driver.awslogs"
    },
    {
      "name": "com.amazonaws.ecs.capability.execution-role.awslogs"
    },
    {
      "name": "com.amazonaws.ecs.capability.ecr-auth"
    },
    {
      "name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"
    }
  ]
}
```

## Verify in the ECS console

Open the ECS console, navigate to **Task Definitions**, and confirm that a new revision (for example, revision 2) has been created. To deploy the new revision, update your ECS service to use the latest revision and perform a deployment.

<Frame>
  <img alt="The image shows the AWS Elastic Container Service (ECS) console, displaying information about a cluster named &#x22;ProductionCluster&#x22; with 1 running service and task status." />
</Frame>

Storing the task definition in source control and registering it during CI achieves two main goals:

* The task definition becomes part of your codebase and change history.
* Any change to the task definition can automatically produce a new ECS revision that you can deploy by updating the service.

Automating the service update to trigger a deployment (for example via `aws ecs update-service`) is possible and commonly done in CD pipelines, but is outside the scope of this lesson.

That’s it for this lesson — thank you for reading.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/87867a08-358d-4890-933e-f6b072182388/lesson/1f09d93c-d5e9-44da-84e4-e44ac74f5925" />
</CardGroup>


# Role of image tags in production

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Task-definition-Image-tags-in-production-and-Load-Balancer/Role-of-image-tags-in-production/page

Explains Docker image tagging best practices for CI/CD, using both human-friendly tags and immutable commit-hash tags with an AWS CodeBuild example for traceability and safe rollbacks.

Welcome — in this lesson we'll cover the role image tags play when building and deploying containerized applications. You’ll learn a practical tagging strategy that balances convenience and traceability, and see an example CodeBuild buildspec that implements it.

## Why tags matter

When you push images to a registry (for example, Amazon ECR), tags determine how images are referenced by deployments and teams. Two complementary tagging patterns are common:

* `latest` (or a human-friendly semantic version): convenient for quick testing and ad-hoc deployments, but mutable — each push retags `latest`.
* Immutable identifier (short commit hash, full digest, or CI build number): provides traceability and safe rollbacks because it points to a specific build artifact.

Adopting both patterns gives you the convenience of `latest` plus the safety of an immutable reference for production and auditability.

## Typical CI flow

In this example we use AWS CodeBuild to:

1. Log into ECR.
2. Derive an image tag from the commit hash (fallback to `latest`).
3. Build the image and tag it as both `latest` and the commit-hash tag.
4. Push both tags to ECR and register the ECS task definition.

Here’s a representative CodeBuild `buildspec.yml`:

```yaml theme={null}
version: 0.2
phases:
  pre_build:
    commands:
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin 666234783044.dkr.ecr.eu-central-1.amazonaws.com
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=${COMMIT_HASH:-latest}

  build:
    commands:
      - echo "Build started on $(date)..."
      - echo "Building the Docker image..."
      - docker build -t $REPOSITORY_URI:latest .
      - docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG

  post_build:
    commands:
      - echo "Build completed on $(date)..."
      - echo "Pushing the Docker image..."
      - docker push $REPOSITORY_URI:latest
      - docker push $REPOSITORY_URI:$IMAGE_TAG
      - aws ecs register-task-definition --cli-input-json file://task-definition.json
```

Notes about the script:

* `COMMIT_HASH` extracts a short commit ID from the CodeBuild environment variable `CODEBUILD_RESOLVED_SOURCE_VERSION`.
* `IMAGE_TAG` becomes the short commit hash when available; otherwise, it falls back to `latest`.
* Two tags are pushed so you can reference images by `latest` for quick tests and by commit-hash for production rollbacks and audits.

Why push both tags? `latest` makes iterative testing easier; the commit-hash tag provides an immutable reference for deployments and rollbacks.

Below is an example ECR view where an image has both a commit-hash tag (e.g., `EB7245DB`) and the `latest` tag.

<Frame>
  <img alt="The image shows a screenshot of the Amazon Elastic Container Registry (ECR) interface, displaying a list of container images under the repository &#x22;cryptoproject,&#x22; including details such as image tags, push dates, sizes, and vulnerabilities." />
</Frame>

If you inspect your source repository you can confirm the commit hash used to tag the image. In this case the CodeCommit commit `EB7245DB` matches the image tag in ECR.

<Frame>
  <img alt="The image shows an AWS CodeCommit page for a repository named &#x22;aws-microservice-project,&#x22; displaying a list of commits with details such as commit ID, message, date, author, and committer." />
</Frame>

## Benefits of tagging with commit hashes

* Traceability: Identify the exact source commit that produced a deployed image.
* Rollbacks: To revert, update the ECS task definition to reference the `REPOSITORY_URI:EB7245DB` tag (or whichever commit tag you want) and redeploy. This ensures ECS pulls the image built from that commit.
* Auditing: Correlate images in ECR with repository history and CI runs to support compliance and incident investigations.

## Quick reference: tag types

| Tag type             | Use case                                    | Example                        |
| -------------------- | ------------------------------------------- | ------------------------------ |
| Human-friendly       | Fast testing, ad-hoc deploys                | `latest`, `v1.2.3`             |
| Immutable identifier | Production deployments, rollbacks, auditing | `EB7245DB` (short commit hash) |

## Example rollback instructions

To roll back an ECS service to an image tagged with a specific commit:

1. Edit the task definition to reference the exact image tag, e.g. `123456789012.dkr.ecr.us-east-1.amazonaws.com/myrepo:EB7245DB`.
2. Register the new task definition revision:
   * `aws ecs register-task-definition --cli-input-json file://task-definition.json`
3. Update the service to use the new task definition revision:
   * `aws ecs update-service --cluster my-cluster --service my-service --task-definition my-task:3`

This ensures the cluster pulls the image built from the commit you specified.

<Callout icon="lightbulb">
  Best practice: Tag each build with both a human-friendly tag (for example, `latest` or a semantic version) and an immutable identifier (for example, the short commit hash). Push both tags to your registry so you get the convenience of `latest` plus the traceability and safety of an immutable tag.
</Callout>

<Callout icon="warning">
  Do not rely solely on `latest` in production. `latest` is mutable and can make rollbacks or incident investigations difficult because it does not uniquely identify a build artifact.
</Callout>

## Links and references

* AWS Elastic Container Registry (ECR): [https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
* Docker image tag best practices: [https://docs.docker.com/engine/reference/commandline/tag/](https://docs.docker.com/engine/reference/commandline/tag/)
* AWS CodeBuild buildspec reference: [https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html)
* AWS ECS task definitions: [https://docs.aws.amazon.[AWS_SECRET_ACCESS_KEY]\_definitions.html](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)

Thanks for reading — use immutable tags alongside human-friendly tags to balance convenience, safety, and auditability in your CI/CD pipelines.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/87867a08-358d-4890-933e-f6b072182388/lesson/50c99233-5785-47d2-a2d7-7bef11c8c576" />
</CardGroup>
