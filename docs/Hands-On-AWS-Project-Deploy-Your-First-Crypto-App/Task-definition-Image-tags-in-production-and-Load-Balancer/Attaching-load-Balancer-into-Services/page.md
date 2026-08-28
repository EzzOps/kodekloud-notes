# Example (run in post_build)
IMAGE="$REPOSITORY_URI:$IMAGE_TAG"
jq --arg image "$IMAGE" '.containerDefinitions[0].image = $image' task-definition.json > task-def-for-register.json
aws ecs register-task-definition --cli-input-json file://task-def-for-register.json
```

With this approach, every task definition revision will reference an immutable image tag. Rolling back to a previous task definition revision will instruct ECS to pull the specific image associated with that revision (the exact commit hash), allowing rollbacks to restore a working version reliably.

Further reading and references

* Amazon ECR: [https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
* Amazon ECS task definition registration: [https://docs.aws.amazon.[AWS_SECRET_ACCESS_KEY]\_definitions.html](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)

That is it for this article.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/acc69333-5a37-4353-a880-a86823fb1e93/lesson/f59043b3-0017-4f00-8785-727c41191e63" />
</CardGroup>


# Attaching load Balancer into Services

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Task-definition-Image-tags-in-production-and-Load-Balancer/Attaching-load-Balancer-into-Services/page

Guide to attaching an Application Load Balancer to an Amazon ECS service, configuring target groups and listeners, troubleshooting subnet Availability Zone errors, and verifying application access.

Hello and welcome back.

In this lesson we attach an Application Load Balancer (ALB) to an Amazon ECS service, validate traffic routing through the ALB, and troubleshoot a common subnet/Availability Zone error. This guide follows the ECS console workflow and explains the ALB, target group, and listener configuration used during deployment.

Overview

* Delete the existing service.
* Create a new ECS service and enable Application Load Balancer (ALB) integration.
* Create the ALB, target group, and listener from the ECS console.
* Troubleshoot a common subnet / Availability Zone error.
* Verify deployment and access the application through the ALB.
* (Optional) Map a DNS name in Route 53.

Quick reference: what gets created

|                        Resource | Purpose                                                     | Notes / Typical values                           |
| ------------------------------: | ----------------------------------------------------------- | ------------------------------------------------ |
| Application Load Balancer (ALB) | Distributes incoming HTTP(S) traffic to tasks               | Listener typically on port `80` or `443`         |
|                    Target Group | Registers ECS tasks as targets and performs health checks   | Target port = container port (e.g., `5000`)      |
|                        Listener | Receives traffic on a port and forwards to a target group   | HTTP listener on `80` or custom port like `5000` |
|                     ECS Service | Manages desired task count and connects to ALB target group | Uses task definition revision (e.g., rev 3)      |
|            CloudFormation Stack | Underlying infra provisioning when created via console      | Check stack events for progress                  |

Step-by-step

1. Delete the existing service

* Open your cluster in the ECS console and locate the running service.
* Click **Delete service**. If tasks are stuck, select **Force delete**, type `delete`, and confirm.
* Expect deletion to take 2–5 minutes. Wait until the service and its tasks are removed before proceeding.

2. Create the new ECS service

* Click **Create** in the ECS console.
* Select the task definition family and the latest revision (for example, revision `3`).
* Provide a service name (you may reuse the previous name).
* Set **Desired number of tasks** to `1` (or your desired scale).

3. Enable load balancing (ALB integration)

* Scroll to **Load balancing (optional)** and enable it.
* Select **Application Load Balancer (ALB)**.
* Choose the container port your application listens on (in this demo: `5000`). This is the target port the ALB’s target group will forward traffic to.
* Configure health checks in the target group—commonly an HTTP path like `/health`. Health checks may use port `80` or the target port depending on your setup.
* Set an appropriate **Health check grace period** (e.g., `30` seconds) to allow the application to start.

4. Configure the load balancer and listener

* Choose to create a new ALB and give it a descriptive name (for example `crypto-app-lb`).
* Configure the listener:
  * Use the default HTTP listener on port `80` (recommended for production with TLS offload on `443`), OR
  * Create a listener on the application port (e.g., `5000`) for testing.
* Create a new target group that uses the container port (e.g., `5000`) as the target.

Note: In production you will usually terminate TLS at the ALB (listener on `443`) and forward traffic to container ports such as `5000` on the target group.

5. Common subnet / Availability Zone error and resolution

* While creating the ALB you might see:
  "A load balancer cannot be attached to multiple subnets in the same Availability Zone."
* Cause: You selected multiple subnets that resolve to the same Availability Zone (for example, selecting both a public and a private subnet for the same AZ or otherwise picking redundant subnets).
* Resolution: Select one subnet per Availability Zone—typically choose public subnets across different AZs. In the demo we removed private subnets and selected three public subnets across three distinct AZs.

Troubleshooting summary

| Symptom                              | Likely cause                                 | Fix                                                                           |
| ------------------------------------ | -------------------------------------------- | ----------------------------------------------------------------------------- |
| ALB creation error about subnets/AZs | Multiple subnets from same AZ selected       | Choose one subnet per AZ (public subnets across AZs)                          |
| Targets report unhealthy             | Health check path/port misconfigured         | Verify target group health check path and port (e.g., `/health`, port `5000`) |
| Service never becomes Active         | ALB/target group not created or task failing | Check CloudFormation stack events and ECS task logs                           |

6. Create the service (start deployment)

* Click **Create** to begin deployment. The console will provision the ALB, target group, listener, and ECS service.
* The console displays a **View CloudFormation** link—ECS uses a CloudFormation stack to create these resources. You can monitor stack events for detailed provisioning progress.

7. Wait for deployment to complete

* Deployment with a new load balancer typically takes 5–10 minutes.
* After completion:
  * ECS service status should be **Active**.
  * Last deployment should show **Completed**.
  * CloudFormation should indicate the ALB, target group, listener, and ECS service were created successfully.

8. Verify access through the ALB

* In the ECS service details you will see the attached Application Load Balancer and the target group status (healthy/unhealthy).
* Click **View load balancer** to open the ALB in the EC2 console and copy the ALB DNS name.
* Access the app:
  * If you created a listener on port `5000` use: `http://<ALB_DNS>:5000`
  * If you used port `80` just use: `http://<ALB_DNS>`

Example test with curl (replace the placeholder with your ALB DNS):

```bash theme={null}
curl http://<ALB_DNS>:5000/
```

Notes on access patterns

* Previously, you might have accessed the app by opening the task endpoint directly (via network bindings). With the ALB in place, users should access the ALB endpoint instead.
* The ALB endpoint remains stable across deployment updates and task replacements, so end users don’t need to change URLs when you redeploy the application.

<Callout icon="lightbulb">
  If you have a Route 53 hosted zone, create an alias or CNAME record pointing to the ALB DNS name so users can access the application with your own domain.
</Callout>

<Callout icon="warning">
  Ensure your ALB subnets span at least two Availability Zones (one subnet per AZ). Selecting multiple subnets in the same AZ will cause ALB creation to fail.
</Callout>

Checklist (before you finish)

* [ ] Service deleted and old tasks removed.
* [ ] Task definition revision selected.
* [ ] ALB enabled and container port correctly specified (e.g., `5000`).
* [ ] Target group health check path and grace period configured.
* [ ] One subnet selected per Availability Zone for the ALB.
* [ ] CloudFormation stack completed without errors.
* [ ] ALB DNS is reachable and target group shows healthy.

That covers attaching an Application Load Balancer to an ECS service, verifying traffic routing, and resolving a common subnet/AZ error. See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/87867a08-358d-4890-933e-f6b072182388/lesson/3e26d709-cea5-4cab-bceb-09a0c9c25a8c" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/87867a08-358d-4890-933e-f6b072182388/lesson/51f34f0b-7fc7-4b7c-809c-0e798496ac77" />
</CardGroup>
