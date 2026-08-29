# Understanding why manual rollback is failing

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Rolling-deployment-and-Rollback-of-deployments/Understanding-why-manual-rollback-is-failing/page

Explains why ECS manual rollbacks fail when task definitions use mutable image tags like latest and how to use immutable tags in pipelines for reliable rollbacks

Hello and welcome back.

Earlier we attempted a rolling update, and that rolling update failed. Here we attempt to roll back the service manually and explain why the rollback keeps failing.

First, in the service console I click Update service and select revision three — the revision that previously worked and that we expect to restore. I then scroll down and click Update.

<Frame>
  <img alt="This image shows a user interface for updating a service within Amazon Elastic Container Service (ECS) on the AWS management console, displaying various optional configurations like Service Connect, Service Discovery, and Auto Scaling." />
</Frame>

You would expect this rollback to succeed. However, when observing the deployment (task set), the number of failed tasks keeps increasing (ten failed tasks in my example). The service repeatedly tries to start tasks but they never become healthy.

We rolled back to the previous task definition (revision three), yet the service still fails to start the tasks. Why?

The root cause is how the container image tags were used when building and registering task definitions. Let’s inspect the task definitions.

Here is task definition revision 4 (the most recent), showing the container image pointing to the `latest` tag:

```json theme={null}
{
  "taskDefinitionArn": "arn:aws:ecs:eu-central-1:666234783044:task-definition/aws-crypto-app:4",
  "containerDefinitions": [
    {
      "name": "kodekloud-crypto-coin",
      "image": "666234783044.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject:latest",
      "cpu": 0,
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
      }
    }
  ]
}
```

And here is task definition revision 3 (the earlier revision we attempted to roll back to), which also points to the `latest` tag:

```json theme={null}
{
  "taskDefinitionArn": "arn:aws:ecs:eu-central-1:666234783044:task-definition/aws-crypto-app:3",
  "containerDefinitions": [
    {
      "name": "kodekloud-crypto-coin",
      "image": "666234783044.dkr.ecr.eu-central-1.amazonaws.com/cryptoproject:latest",
      "cpu": 0,
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
      "environment": []
    }
  ]
}
```

Because both revisions reference the mutable `latest` tag, rolling back to revision 3 still causes ECS to pull whatever image is currently labeled `...:latest` in ECR. If `latest` has been overwritten by a newer (possibly broken) build, the rollback will not restore the known-good image. This explains why the rollback did not fix the problem.

> **lightbulb** Avoid using a mutable tag like `latest` in production task definitions. Always reference an immutable tag (for example, a commit hash or build number) in the task definition so that each revision pulls the exact image you expect.

What caused this in our pipeline?

Our build produced two tags in ECR — a `latest` and a commit-hash tag — but the task definitions we registered used `:latest`. Below is the buildspec we used during the demo (updated to a modern, recommended login flow):

```yaml theme={null}
version: 0.2
phases:
  pre_build:
    commands:
      - echo "Logging in to Amazon ECR..."
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $REPOSITORY_URI
  build:
    commands:
      - echo "Build started on `date`"
      - docker build -t $REPOSITORY_URI:$IMAGE_TAG .
      - docker tag $REPOSITORY_URI:$IMAGE_TAG $REPOSITORY_URI:latest
  post_build:
    commands:
      - echo "Build completed on `date`"
      - echo "Pushing the Docker images..."
      - docker push $REPOSITORY_URI:$IMAGE_TAG
      - docker push $REPOSITORY_URI:latest
      - echo "Registering ECS task definition..."
      - aws ecs register-task-definition --cli-input-json file://task-definition.json
```

Note: the example above tags both `:$IMAGE_TAG` (typically a commit hash) and `:latest` and pushes both to ECR. The important detail is what gets written into `task-definition.json` when registering the task definition. If `task-definition.json` contains `...:latest`, each revision will still point to the mutable `latest` image — making rollbacks ineffective.

How to fix this

Summary of recommended changes:

| Problem                                       | Recommended fix                                                                               | Example                                                                                       |
| --------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Task definitions reference `latest` (mutable) | Register task definitions that reference an immutable tag (e.g., commit hash or build number) | Update the image field to `"$REPOSITORY_URI:$IMAGE_TAG"` before registration                  |
| Task definition file hardcodes `latest`       | Template or inject the image tag during the pipeline post-build step                          | Use `jq`, `sed`, or your templating tool to replace the image value in `task-definition.json` |

Step-by-step approach

1. Ensure your pipeline builds and pushes an immutable tag (for example, the commit hash).
2. Do not register a task definition that hardcodes `:latest`. Instead, update the task definition to reference the immutable tag produced by the build.
3. Replace the image field in the task definition during the pipeline (post-build) before calling `aws ecs register-task-definition`.

Here is a sample post-build sequence that updates the task definition file with the exact image tag and then registers it:

```bash theme={null}
