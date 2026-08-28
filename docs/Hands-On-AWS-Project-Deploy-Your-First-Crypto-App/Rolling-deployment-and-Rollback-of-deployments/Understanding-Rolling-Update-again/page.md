# python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Default credentials
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "password123"

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Check if provided credentials match the default ones
        if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
            return redirect(url_for('welcome'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/welcome')
def welcome():
    return render_template('product.html')

@app.route('/place_order')
def place_order():
    # Code to place order
    return render_template('receipt.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Commit and push the faulty change
After deliberately introducing the fault, the source changes are committed and pushed from the Cloud9 environment:

```bash theme={null}
# bash
ec2-user:~/environment $ cd aws-microservice-project/
ec2-user:~/environment/aws-microservice-project (master) $ git add .
ec2-user:~/environment/aws-microservice-project (master) $ git commit -m "rolling deployment failure"
ec2-user:~/environment/aws-microservice-project (master) $ git push origin master
```

Trigger CodeBuild to create a new image
A push to the repository triggers a CodeBuild project which builds a new container image and pushes it to Amazon ECR. Wait for the build to complete and then verify the new image in your repository.

<Frame>
  <img alt="The image shows an AWS CodeBuild project management interface for a project named &#x22;aws-microservice-project,&#x22; displaying build configuration details and a history of successful build runs." />
</Frame>

Verify the image in ECR
Once CodeBuild finishes successfully, it pushes the image to ECR. Confirm the new image and its tag in your repository before updating ECS.

<Frame>
  <img alt="The image shows the Amazon Elastic Container Registry interface, displaying a list of images under the &#x22;cryptoproject&#x22; repository with details like image tags, artifact types, and sizes." />
</Frame>

Update the ECS service
Update the ECS service to point to the latest task definition revision (the one that references the newly built image). In the demo, we also reduce the desired task count to 1 so the effect of the broken deployment is easier to observe.

<Frame>
  <img alt="The image shows the AWS Elastic Container Service interface with settings to update the &#x22;crypto-app&#x22; service, including options for deployment configuration such as task definition, revision, service type, and desired tasks." />
</Frame>

Observed failure behavior
When the new task launches, the container image contains the intentional fault, so the task either crashes or fails load-balancer/container health checks. ECS will keep attempting to start replacement tasks, which results in a repeating failure cycle.

Common symptoms:

* New tasks never reach RUNNING + healthy state.
* Service desired count is not satisfied (for example, shows 0/1 or 0/N).
* Continuous restart attempts that consume compute and increase cost.
* End-user impact due to unavailable application.

Why ECS does not auto-rollback
By default, ECS persistently tries to deploy the requested task definition revision. ECS will not automatically revert to the previous working task definition unless you configure automatic rollback using the deployment circuit breaker or orchestrate rollback via external automation (CI/CD, CloudWatch alarms, or CodeDeploy).

Mitigation and best practices
Use one or more of the following features and practices to prevent or reduce the impact of failed rolling deployments:

| Feature / Practice             | Purpose                                                         | Example / How-to                                                                                                                                                                                             |
| ------------------------------ | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ECS Deployment Circuit Breaker | Automatically stop a failing deployment and optionally rollback | Enable `deploymentConfiguration` with `deploymentCircuitBreaker` set to `enable: true` and `rollback: true` ([docs](https://docs.aws.amazon.[AWS_SECRET_ACCESS_KEY]-type-replacement.html)) |
| Container & LB health checks   | Detect unhealthy tasks quickly so ECS can respond               | Define `healthCheck` in the task definition and configure target group health checks in the load balancer                                                                                                    |
| AWS CodeDeploy (Blue/Green)    | Safer traffic shifting and automated rollback for ECS           | Use CodeDeploy blue/green deployments to perform controlled traffic shifting and automatic rollback on failure ([docs](https://docs.aws.amazon.[SECRET_REDACTED]-steps.html))       |
| CI/CD gates and testing        | Catch application-level defects before images are published     | Add unit/integration tests, static analysis, and end-to-end checks in CodeBuild pipelines                                                                                                                    |
| CloudWatch alarms + automation | Trigger alerts or automated remediation/rollback                | Configure CloudWatch alarms on task failures or target group unhealthy counts and tie to Lambda or Systems Manager Automation runbooks                                                                       |

<Callout icon="lightbulb">
  Enable the ECS deployment circuit breaker and configure container and load-balancer health checks to automatically abort failed rolling updates and roll back to a previously stable task revision.
</Callout>

Next steps
We will next examine ECS deployment circuit breaker settings in detail and demonstrate an automatic rollback during a failed deployment. For further reading and to implement the suggestions above, see the links below.

Links and references

* Amazon ECS deployments and the deployment circuit breaker: [https://docs.aws.amazon.[AWS_SECRET_ACCESS_KEY]-type-replacement.html](https://docs.aws.amazon.[AWS_SECRET_ACCESS_KEY]-type-replacement.html)
* AWS CodeBuild: [https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html)
* Amazon ECR: [https://docs.aws.amazon.com/ecr/](https://docs.aws.amazon.com/ecr/)
* AWS CodeDeploy blue/green deployments: [https://docs.aws.amazon.[SECRET_REDACTED]-steps.html](https://docs.aws.amazon.[SECRET_REDACTED]-steps.html)
* Amazon CloudWatch alarms: [https://docs.aws.amazon.[SECRET_REDACTED].html](https://docs.aws.amazon.[SECRET_REDACTED].html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/acc69333-5a37-4353-a880-a86823fb1e93/lesson/0c91d33d-b137-4756-823d-f5f750526a1e" />
</CardGroup>


# Understanding Rolling Update again

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Rolling-deployment-and-Rollback-of-deployments/Understanding-Rolling-Update-again/page

A walkthrough reproducing and troubleshooting a failing AWS ECS rolling update, showing build and deploy steps, root causes, and recommendations like immutable image tags and deployment circuit breaker.

Welcome back. In this walkthrough we recreate a failing ECS rolling update and analyze what went wrong. We'll:

* Rebuild the Docker image and push a new task definition revision from CodeBuild.
* Deploy the new task definition revision to an ECS service and observe the failed rolling update.
* Manually roll back to the previously working revision and explain why ECS did not automatically restore the service.

This guide preserves the exact commands and configuration used in the reproduction, while clarifying the sequence and root causes so you can apply the same troubleshooting steps in your environment.

## 1) Build pipeline: CodeBuild buildspec

Below is the buildspec used in CodeBuild to build, tag, and push the Docker image. Note that the tagging was corrected so both `latest` and the commit-hash tag are pushed.

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
      - sed -i "s|REPOSITORY_URI|$REPOSITORY_URI:$IMAGE_TAG|g" task-definition.json
      - aws ecs register-task-definition --cli-input-json file://task-definition.json
```

Tips:

* Prefer using immutable tags (commit hash or image digest) in the task definition to avoid ambiguity during rollbacks.
* Pushing both `latest` and a commit-tag helps during development, but relying on `latest` for production rollbacks can cause recovered revisions to pull the same broken image.

## 2) Application change that caused the failure

We intentionally introduced a code change that caused the container to fail at runtime. The fixed snippet below shows the application after adding `app` and handling `error` in the login route while keeping the commented-out route and the commented blocks that originally introduced the issue.

```python theme={null}
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
