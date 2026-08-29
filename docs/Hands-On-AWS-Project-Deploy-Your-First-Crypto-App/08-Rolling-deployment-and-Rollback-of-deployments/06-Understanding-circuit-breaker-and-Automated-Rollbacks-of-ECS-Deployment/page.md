# Default credentials
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "password123"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if provided credentials match the default ones
        if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
            return redirect(url_for('welcome'))
        else:
            error = 'Invalid Credentials. Please try again.'
    
    return render_template('login.html', error=error)

# @app.route('/welcome')
def welcome():
    return render_template('product.html')

@app.route('/place-order')
def place_order():
    product_id = request.args.get('product')
    return render_template('place_order.html', product_id=product_id)
```

This is the exact runtime state that CodeBuild packaged and pushed.

## 3) Git commands used to prepare the image

Commands executed to amend a commit and push a new change (output examples included):

```bash theme={null}
git add .
git commit --amend --reset-author
# Example output:
# 3 files changed, 7 insertions(+), 6 deletions(-)
# Enumerating objects: 9, done.
# Counting objects: 100% (9/9), done.
# Compressing objects: 100% (6/6), done.
# Writing objects: 100% (5/5), 213.80 KiB | 16.00 KiB/s, done.
# Total 5 (delta 3), reused 0 (delta 0)
# To https://git-codecommit.eu-central-1.amazonaws.com/v1/repos/aws-microservice-project
#    87216782..e1389e2  master -> master
```

Then a new commit and push:

```bash theme={null}
git commit -m "Understand rolling update"
git push origin master
# Example push output:
# Enumerating objects: 5, done.
# Counting objects: 100% (5/5), done.
# Compressing objects: 100% (3/3), done.
# Writing objects: 100% (3/3), 367.00 KiB | 0 bytes/s, done.
# Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
# remote: Validating objects...
# To https://git-codecommit.eu-central-1.amazonaws.com/v1/repos/aws-microservice-project
#    52afb79..3769762  master -> master
```

## 4) Task definition registration

When CodeBuild completed, it updated the `task-definition.json` and registered a new task definition revision. The relevant portion of the registered task-definition (revision 6) is shown below:

```json theme={null}
{
    "taskDefinition": {
        "taskDefinitionArn": "arn:aws:ecs:eu-central-1:666234783044:task-definition/aws-crypto-app:6",
        "containerDefinitions": [
            {
                "name": "kodeklud-crypto-coin",
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
        ],
        "family": "aws-crypto-app",
        "executionRoleArn": "arn:aws:iam::666234783044:role/ecsTaskExecutionRole",
        "networkMode": "awsvpc",
        "revision": 6,
        "status": "ACTIVE"
    }
}
```

The build pipeline substituted the commit hash into the `task-definition.json`, so the task definition revision is correlated with the image tag.

## 5) Deploying the new revision in ECS

From the ECS console we updated the service to use revision 6. On the Update Service page we selected revision 6 and clicked Update.

<Frame>
  <img alt="The image shows a webpage interface of the Amazon Elastic Container Service (ECS) with various optional service configurations like Service Connect, Service Discovery, Load Balancing, and more. There are buttons for actions like &#x22;Cancel&#x22; and &#x22;Update&#x22; at the bottom." />
</Frame>

What happened after the update:

* ECS started tasks for revision 6, but they failed to reach a RUNNING state.
* The deployment hung in a loop: tasks were repeatedly started and stopped due to container start errors caused by the introduced change.
* ECS kept trying to bring up the failing revision instead of returning to the previously working revision.

## 6) Manual rollback performed

To recover we manually reverted the service back to the last-known working revision:

1. Open the service in the ECS console and click Update service.
2. Select the previous working task definition revision (revision 5).
3. Click Update.

After that:

* ECS started tasks using revision 5 and the corresponding image.
* The new failing deployment was drained and the service returned to a healthy RUNNING state.

## Why ECS did not automatically roll back

> **lightbulb** Automatic rollback in ECS is not guaranteed by default. Two common blockers are:

  1. No automatic detection and abort: ECS will continue attempting a deployment until it either succeeds or you enable the deployment circuit breaker or external automation to stop it.
  2. Non-immutable image tags: If both the old and new task definitions reference a moving tag like `latest`, rolling back the task definition may still pull the same broken image.

  Best practices: use immutable image tags (commit-hash or image digest like `repo@sha256:...`) and enable the ECS deployment circuit breaker or monitoring automation to detect and recover from faulty deployments.

## Quick reference: Common causes and mitigation

| Problem                          | Why it causes failed rollouts                                                                           | Mitigation                                                                                                                |
| -------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Using `latest` or mutable tags   | Rollback to a previous task definition can still pull the same broken image if `latest` was overwritten | Use immutable tags (`<commit-hash>` or image digest).                                                                     |
| No deployment circuit breaker    | ECS will keep trying a failing deployment indefinitely                                                  | Enable the ECS deployment circuit breaker or add health checks/alarms to trigger rollback automation. See AWS docs below. |
| Application runtime errors       | The container exits during startup, causing new tasks to fail                                           | Add container-level logging and health checks; test images locally before pushing.                                        |
| Missing logging or observability | Hard to determine why tasks fail                                                                        | Configure CloudWatch logs and structured logs in the container.                                                           |

Note: In the table cell above `latest` is shown as inline code to avoid parsing/ambiguity.

## Recap and recommended hardening steps

* Reproduced a failing rolling update by pushing a new task definition revision with a runtime error.
* ECS attempted the rolling update, but the deployment repeatedly failed and did not auto-rollback.
* Manual rollback to the previous task definition revision restored the service.
* Root cause: mutable image tags (`latest`) and lack of an automatic deployment abort mechanism.

Recommended actions:

* Use immutable image tags (commit-hash tags or digests) in task definitions.
* Enable the ECS deployment circuit breaker to automatically stop unhealthy deployments:
  * AWS docs: [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html)
* Implement health checks (load balancer and container-level) and CloudWatch alarms to detect failed deployments quickly.
* Ensure CI/CD injects the immutable image identifier into the task definition that you register.

Further reading and references:

* Amazon ECS task definitions: [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task\_definitions.html](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)
* ECS deployment circuit breaker: [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html#deployment-circuit-breaker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html#deployment-circuit-breaker)
* Amazon ECR best practices for image tags and immutability: [https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-tag-mutability.html](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-tag-mutability.html)

That's all for now—apply immutable tagging and circuit-breaker protections to avoid similar deadlock-style failures in rolling updates.

- [Watch Video](https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/acc69333-5a37-4353-a880-a86823fb1e93/lesson/823629ba-66f6-4276-9596-ac00cff42e8d)


# Understanding circuit breaker and Automated Rollbacks of ECS Deployment

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Rolling-deployment-and-Rollback-of-deployments/Understanding-circuit-breaker-and-Automated-Rollbacks-of-ECS-Deployment/page

Explains Amazon ECS deployment circuit breaker and automated rollback to stop failing rolling updates, prevent endless restarts, and restore previous healthy task revisions.

Hello and welcome back.

This article explains how to avoid a deadlock during a rolling update—especially when a new application revision fails to start or pass health checks—and how Amazon ECS's deployment circuit breaker combined with automated rollback helps recover safely.

<Frame>
  <img alt="The image shows an AWS Elastic Container Service (ECS) console with an active &#x22;ProductionCluster,&#x22; displaying details like cluster status, services, and a running crypto-app service." />
</Frame>

What the circuit breaker solves

* When you push code (for example, to [CodeCommit](https://aws.amazon.com/codecommit/)) and your CI/CD pipeline (for example, [CodePipeline](https://aws.amazon.com/codepipeline/) or [CodeDeploy](https://aws.amazon.com/codedeploy/)) deploys a new ECS task definition revision, ECS performs a rolling update by replacing old tasks with new ones.
* If the new revision crashes on startup, fails container-level health checks, or cannot register with an associated load balancer, ECS will repeatedly try to start tasks in an attempt to meet the desired count. That can cause repeated restarts, resource waste, longer outages, and potentially leave the service in a non-working state.
* The ECS deployment circuit breaker detects repeated, consecutive failures and halts further restarts. If automatic rollback is enabled, ECS then reverts the service to the last known good task set (previous revision). See Amazon ECS deployments for details: [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployments.html](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployments.html)

High-level deployment flow

1. Code change (e.g., to CodeCommit) triggers the pipeline; CodePipeline/CodeDeploy updates the service with a new task definition revision.
2. ECS launches the new tasks (e.g., v0.2) while draining/replacing the old tasks (v0.1).
3. ECS monitors tasks and their health status during the rollout. Deployment state-change events are emitted and can be consumed via [EventBridge](https://aws.amazon.com/eventbridge/).
4. If the new tasks repeatedly fail beyond the configured detection conditions, the circuit breaker marks the deployment as failed, stops further restarts, and (if configured) automatically rolls back to the previous stable revision.

<Frame>
  <img alt="This image shows the Amazon Elastic Container Service (ECS) interface, specifically the update configuration page for a service named &#x22;crypto-app,&#x22; where deployment settings like task definition and revision can be modified." />
</Frame>

How the ECS deployment circuit breaker works (details)

* Monitoring: ECS expects tasks to reach and stay in the RUNNING state. It observes status transitions and health-check results during the deployment window.
* Failure detection: ECS counts repeated failures or consecutive unhealthy transitions for the new task set. When failures match the configured detection behavior, ECS stops attempting further restarts for that revision.
* Health checks taken into account:
  * Elastic Load Balancer (target group) health checks — see [target group health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)
  * AWS Cloud Map registration failures — see [AWS Cloud Map](https://aws.amazon.com/cloud-map/)
  * Container-level health checks defined in the task definition
    Accurate and meaningful health checks are critical; misconfigured checks can cause false positives or false negatives.
* Circuit action: Once ECS determines the deployment is failing, it halts restart attempts. If automatic rollback is enabled on the service, ECS reverts to the previous task set (the last known good revision) so the service returns to a working state.

Failure-threshold calculation (example)

* Example setup: desired task count = 10.
* For demonstration, this article uses a simple illustrative rule: threshold = ceil(0.5 \* desiredCount). This is an explanatory example, not an official AWS formula.
* For desiredCount = 10: threshold = ceil(0.5 \* 10) = 5.
* Some demo materials show an upper cap (for example, 200) on the computed threshold. Treat that as a presentation detail rather than a strict platform guarantee.
* Result in this example: if 5 consecutive tasks fail health checks, the deployment is considered failed and ECS would roll back to the previous revision. In your environment, actual detection behavior depends on health-check configuration, deployment parameters, and ECS scheduler behavior—always verify against current AWS documentation and your environment.

> **lightbulb** Always verify the exact failure-count behavior and limits in your environment and cloud provider documentation. Threshold formulas and caps can change with platform updates—review and peer-review these settings before applying them in production.

Practical considerations and recommendations

* Define accurate health checks:
  * Container health checks in the task definition should reflect readiness and not just liveness.
  * ELB target group health checks should confirm the application is responding correctly at the intended path and port.
  * If you use AWS Cloud Map for service discovery, ensure registration and health status are validated.
* Enable the deployment circuit breaker and automatic rollback for production services where you want faster, safer recovery from bad releases.
* Capture deployment events:
  * Use [EventBridge](https://aws.amazon.com/eventbridge/) or CloudWatch Events to receive deployment state-change notifications and trigger alerts or automated remediation.
* Peer review deployment settings: failure thresholds, health-check intervals, and rollback policies should be agreed upon by your team.
* Test in staging: simulate failing revisions to verify rollback behavior before enabling automatic rollback in production.

Recommended checklist (quick reference)

| Concern                    |                                                             Why it matters | Recommendation                                                                              |
| -------------------------- | -------------------------------------------------------------------------: | ------------------------------------------------------------------------------------------- |
| Health-check accuracy      | Prevents false positives/negatives that trigger rollbacks or mask failures | Define container and ELB checks that reflect readiness; include retries and proper timeouts |
| Circuit breaker + rollback |             Stops endless restarts and returns service to known good state | Enable both for production; test behavior in staging                                        |
| Event notifications        |                           Detect and respond to failed deployments quickly | Subscribe to EventBridge/CloudWatch Events and integrate alerts or automation               |
| Threshold tuning           |                                        Avoid premature or delayed rollback | Agree on thresholds (team-reviewed) and document rationale                                  |

> **warning** Warning: Automatic rollback recovers the service to the previous task set, but it does not fix the underlying code or configuration issue. Use automated rollback to reduce downtime, but follow up with diagnostics, logs, and remediation to resolve the root cause.

Summary

* The ECS deployment circuit breaker prevents continuous task restarts by halting a failing deployment and (when enabled) automatically rolling back to the last healthy task set.
* ECS evaluates failures using configured health checks, counts consecutive failures, and triggers the circuit action when those conditions are met.
* Use accurate health checks, instrument EventBridge for deployment events, tune thresholds thoughtfully, test rollback behavior in staging, and peer-review settings before enabling in production.

Links and references

* Amazon ECS deployments: [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployments.html](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployments.html)
* AWS CodeCommit: [https://aws.amazon.com/codecommit/](https://aws.amazon.com/codecommit/)
* AWS CodePipeline: [https://aws.amazon.com/codepipeline/](https://aws.amazon.com/codepipeline/)
* AWS CodeDeploy: [https://aws.amazon.com/codedeploy/](https://aws.amazon.com/codedeploy/)
* Elastic Load Balancing target group health checks: [https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)
* AWS EventBridge: [https://aws.amazon.com/eventbridge/](https://aws.amazon.com/eventbridge/)

That is it for this article.

- [Watch Video](https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/acc69333-5a37-4353-a880-a86823fb1e93/lesson/b7fd03ec-58b4-4cb3-92b8-d73de63d06c9)
