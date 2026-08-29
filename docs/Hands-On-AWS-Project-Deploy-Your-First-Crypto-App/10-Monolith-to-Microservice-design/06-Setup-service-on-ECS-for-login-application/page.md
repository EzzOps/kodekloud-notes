# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run flask application
CMD ["flask", "run"]
```

<Frame>
  <img alt="This image shows an AWS Cloud9 development environment with a file directory on the left, a code editor in the center displaying a Dockerfile, and a terminal at the bottom." />
</Frame>

What the Dockerfile does

* Uses an official Python slim base image.
* Establishes `/usr/src/app` as the working directory.
* Copies your source into the image.
* Installs Python dependencies from `requirements.txt`.
* Exposes port `5000` and configures Flask environment variables.
* Launches the Flask app using `flask run`.

Create the buildspec.yml
Create `buildspec.yml` at the repo root. This file controls CodeBuild phases: authenticate to ECR, build and tag the image, push tags, and produce `imagedefinitions.json` for downstream deploy steps.

Note: Replace the example ECR repository URI and account ID with your own. In this example, `666234783044.dkr.ecr.eu-central-1.amazonaws.com/kodekloud-login-page` is used as a placeholder.

```yaml theme={null}
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.8
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws --version
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin 666234783044.dkr.ecr.eu-central-1.amazonaws.com/kodekloud-login-page
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG="$COMMIT_HASH-latest"
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...
      - docker build -t $REPOSITORY_URI:latest .
      - docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker image...
      - docker push $REPOSITORY_URI:latest
      - docker push $REPOSITORY_URI:$IMAGE_TAG
      - printf '[{"name":"kodeKloud-login-page","imageUri":"%s"}]' $REPOSITORY_URI:$IMAGE_TAG > imagedefinitions.json

artifacts:
  files:
    - imagedefinitions.json
```

> **lightbulb** Use `aws ecr get-login-password` (AWS CLI v2) instead of the deprecated `aws ecr get-login`. Ensure environment variables such as `AWS_DEFAULT_REGION` and `REPOSITORY_URI` are provided in the CodeBuild project settings or as build environment variables.

Environment variables used by the build

| Variable                            | Purpose                                                        | Example                                                                |
| ----------------------------------- | -------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `REPOSITORY_URI`                    | ECR repository URI used for tagging and pushing images         | `666234783044.dkr.ecr.eu-central-1.amazonaws.com/kodekloud-login-page` |
| `AWS_DEFAULT_REGION`                | AWS region for `aws` CLI commands and login                    | `eu-central-1`                                                         |
| `CODEBUILD_RESOLVED_SOURCE_VERSION` | Provided by CodeBuild; used to create a short commit-based tag | (auto-provided by CodeBuild)                                           |

Create the ECR repository
If you don't have an ECR repo yet, create one in the ECR console:

1. Open the Amazon ECR service in the AWS Console.
2. Click "Create repository".
3. Enter the repository name (for example, `kodekloud-login-page`) and create it.
4. Copy the repository URI (for example, `666234783044.dkr.ecr.eu-central-1.amazonaws.com/kodekloud-login-page`) and set it as the `REPOSITORY_URI` environment variable for your CodeBuild project.

Commit and push your changes to CodeCommit
From your Cloud9 environment or a local terminal, add the new files and push to your CodeCommit repository:

```bash theme={null}
git status
git add .
git commit -m "Add Dockerfile and buildspec.yml"
git push origin master
```

Go to CodeCommit to verify the files
Open the AWS CodeCommit console and confirm `Dockerfile` and `buildspec.yml` appear in the repository.

<Frame>
  <img alt="The image shows an AWS CodeCommit console displaying a list of repositories, including details like name, last modified date, and cloning options. The interface has navigation options for different AWS developer tools like CodeArtifact, CodeBuild, and CodePipeline on the left." />
</Frame>

Create the CodePipeline
Steps to create a simple pipeline that builds and pushes your image:

1. Open AWS CodePipeline.
2. Click "Create pipeline".
3. Provide a pipeline name such as `login-page-microservice`.
4. For Source provider choose `CodeCommit`, select your repository (e.g., `login-page-microservice`) and branch (e.g., `master`).
5. For Build provider choose `AWS CodeBuild` and select (or create) a CodeBuild project. Ensure the project references the repository and has `REPOSITORY_URI` and `AWS_DEFAULT_REGION` configured as environment variables.
6. (Optional) Skip the Deploy stage for now — you can add an ECS/EKS/CloudFormation/CodeDeploy stage later.
7. Create the pipeline.

When configuring the source stage, select the repository and branch. The UI appears like this:

<Frame>
  <img alt="The image shows an AWS CodePipeline interface where the &#x22;Add source stage&#x22; step is being set up, allowing the user to select a source provider, repository name, branch name, and set change detection options." />
</Frame>

When creating or selecting the build stage, verify the build project and configure environment variables and the buildspec if necessary:

<Frame>
  <img alt="The image shows an AWS CodePipeline interface with a form to add a build stage, allowing users to select a build provider and configure options for a build project. It includes the option to add environment variables and choose between a single or batch build." />
</Frame>

Pipeline execution and build
After pipeline creation, CodePipeline will detect the source change and trigger the pipeline automatically. The sequence:

* Source stage: CodeCommit triggers when you push changes.
* Build stage: CodeBuild runs `buildspec.yml` to build, tag, and push Docker images to ECR.
* (Optional) Deploy stage: consume `imagedefinitions.json` to update tasks or manifests.

You can view pipeline progress in the console and stream CodeBuild logs to see build output and Docker push progress. The pipeline UI shows the status for each stage:

<Frame>
  <img alt="The image shows an AWS CodePipeline interface with a project named &#x22;login-page-microservice.&#x22; The pipeline has successfully completed the source stage and is currently in progress on the build stage." />
</Frame>

Validate the image in ECR
When the build completes successfully:

1. Open the Amazon ECR console.
2. Navigate to your repository and verify that the pushed image tags exist (for example, `latest` and a commit-based tag like `abc1234-latest`).
3. Use the image URI when deploying to ECS, EKS, or EC2.

Next steps and deployment options
With images available in ECR you can deploy via:

* Amazon ECS (Fargate or EC2 launch types) using a task definition and service.
* Amazon EKS by updating your Kubernetes Deployment image.
* EC2 / Docker by pulling the image on an instance and running it.

Refer to the documentation for detailed deployment steps for your chosen platform.

Links and References

* [AWS CodePipeline User Guide](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html)
* [AWS CodeBuild User Guide](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html)
* [Amazon ECR User Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
* [Flask Documentation](https://flask.palletsprojects.com/)
* [AWS CLI v2 ECR Login](https://docs.aws.amazon.com/cli/latest/reference/ecr/get-login-password.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/d14608f9-c900-4ec7-9bdd-ed8e215da540/lesson/c61d3e28-3677-45d9-a020-41a463ff65ba)


# Setup service on ECS for login application

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Monolith-to-Microservice-design/Setup-service-on-ECS-for-login-application/page

Deploying a Flask login app to AWS ECS using an Application Load Balancer, creating task definitions and services, validating health, and fixing redirect and networking issues.

Now that the container image is built and pushed to Amazon ECR, deploy the login application as a service on Amazon ECS. This guide walks through creating a task definition, configuring a service with an Application Load Balancer (ALB), validating the deployment, and fixing a common redirect issue in the Flask app.

## Prerequisites

* Image pushed to ECR (copy its image URI).
* An ECS cluster (here, a production cluster).
* Appropriate VPC, subnets, and security groups configured for the ALB and ECS tasks.
* Port 5000 used by the Flask application.

## 1. Create the Task Definition

1. Open the AWS Console and navigate to **ECS**.
2. Click **Task Definitions → Create new task definition**.
3. Give the task definition a descriptive name.
4. Scroll down to add a container:
   * Paste the image URI you copied from ECR into the container image field.
   * Add a port mapping: container port `5000`.
   * Leave other settings at their defaults unless you need resource limits or environment variables.
5. Click **Create**.

<Frame>
  <img alt="The image shows the Amazon Elastic Container Service (ECS) dashboard with a cluster named &#x22;ProductionCluster,&#x22; displaying details like one running service and no pending tasks. A green notification bar indicates a successful task definition creation for &#x22;login-app-microservice:1.&#x22;" />
</Frame>

## 2. Create the Service from the Cluster

1. Go to **Clusters** and select your production cluster.
2. Click **Create** to create a new service.
3. Select the task definition you created for the login app.
4. Give the service a name such as `login-app-microservice`.

## 3. Configure Load Balancing (Application Load Balancer)

* Under **Load balancing**, choose **Application Load Balancer (ALB)**.
* You can select an existing load balancer or create a new one:
  * If creating new, give the ALB a name and set the idle timeout to `30` seconds.
  * Configure a listener for port `5000` and map it to the target group used by the ECS service.
* Ensure the target group uses the correct port (`5000`) and a health check path that your app responds to (e.g., `/` or `/health`).

<Frame>
  <img alt="This image shows the AWS Management Console interface, specifically within the Elastic Container Service (ECS) section, focusing on configuring a service with options for load balancing." />
</Frame>

> **warning** If you encounter a subnet error while creating the load balancer, it typically means you selected subnets that are not reachable from the ALB (for example, private-only subnets). Remove private-only subnets or include public subnets that have routes to an Internet Gateway, then retry.

## 4. Wait for Deployment and Verify Health

* After creating the service, ECS launches tasks and registers them with the ALB target group.
* Wait until the service deployment becomes STABLE and the tasks report as *healthy*.
* If the deployment fails or stays unhealthy, check:
  * ECS service events for error messages.
  * Task logs in CloudWatch (or the container logs).
  * ALB target group health check results.
  * Security groups: ensure ALB can reach container port `5000` and the ALB has an inbound rule for the client port you will use.

<Frame>
  <img alt="This image shows the AWS Management Console for Amazon Elastic Container Service (ECS), indicating that the &#x22;login-app-microservice&#x22; is active and running with a healthy status." />
</Frame>

## 5. Validate the Application

1. In the ECS service page, click **View Load Balancer** for this service.
2. Copy the Load Balancer DNS name.
3. Open a browser and visit: `http://<LOAD_BALANCER_DNS>:5000` (wrap the DNS placeholder in backticks as shown).

Note: The UI may load but login or navigation might fail if the app issues redirects to a hard-coded IP address. The application should use relative paths or environment-aware base URLs so it works behind a load balancer.

## Common ECS/ALB settings (recommended)

| Resource                   | Recommended setting                                               | Notes                                                            |
| -------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------- |
| Container port             | `5000`                                                            | Map this in the task definition container settings.              |
| ALB idle timeout           | `30` seconds                                                      | Adjust if requests may take longer.                              |
| Target Group protocol/port | `HTTP` / `5000`                                                   | Health check path should match an endpoint that returns 200.     |
| Security groups            | ALB: inbound client port (e.g., 80/5000); ECS tasks: allow ALB SG | Ensure ALB SG can reach task SG on port `5000`.                  |
| Subnet selection           | Public subnets for ALB; tasks in private/public as appropriate    | ALB must be in public subnets with route to an Internet Gateway. |

## Troubleshooting checklist

* Subnet selection error: ensure ALB subnets are public or reachable.
* ALB target health failing: check health check path and container response.
* No response in browser: verify security group inbound rules and that ALB is listening on the expected port.
* Task keeps restarting: inspect container logs for exceptions and verify environment variables, database connectivity, and required secrets.

## 6. Fix the Flask redirect issue

If login UI loads but navigation or login redirects fail, inspect the Flask code. Avoid hard-coded external IP addresses in redirects. Use relative paths or configure the base URL via environment variables.

Example (app.py):

```python theme={null}
from flask import Flask, redirect

app = Flask(__name__)

@app.route('/product')
def product():
    # Original (hardcoded external IP):
    # return redirect("http://35.156.49.246:5000/welcomepage")
    # Recommended: use a relative path (keeps redirects within the same host/load balancer)
    return redirect('/welcomepage')
```

> **lightbulb** Do not hardcode IP addresses in redirects. Use relative paths (e.g., `redirect('/welcomepage')`), environment-configured base URLs, service discovery, or the load balancer DNS (`http://<LOAD_BALANCER_DNS>:5000`) so the application remains portable and resilient to infrastructure changes.

## Next steps and best practices

* Use environment variables for service URLs and external endpoints rather than hard-coded values.
* Configure health checks that match actual application endpoints and response times.
* Centralize logs in CloudWatch and set up alerts for unhealthy targets or repeated task restarts.
* Consider using HTTPS with a certificate on the ALB for secure traffic.
* For production, consider placing tasks in private subnets and using the ALB in public subnets only.

Useful references:

* [Amazon ECS documentation](https://docs.aws.amazon.com/ecs/latest/developerguide/what-is-ecs.html)
* [Amazon ECR documentation](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
* [ALB documentation and target groups](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)
* [Flask documentation](https://flask.palletsprojects.com/)

We will cover connecting the product page and login page across services and discuss best practices for environment variables and service discovery in a deployed environment in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/d14608f9-c900-4ec7-9bdd-ed8e215da540/lesson/860877dc-f67a-4dff-8ada-536691e7ece9)
