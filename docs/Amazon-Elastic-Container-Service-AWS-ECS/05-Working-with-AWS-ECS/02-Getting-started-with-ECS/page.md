# Getting started with ECS

Source: https://notes.kodekloud.com/docs/Amazon-Elastic-Container-Service-AWS-ECS/Working-with-AWS-ECS/Getting-started-with-ECS/page

Guide to deploying demo Node.js containers to Amazon ECS using Fargate, covering container configuration, task and service creation, networking, logging, health checks, and cleanup.

Before you begin deploying to Amazon ECS, review the two public demo images used in this lesson. Both images are published by KodeKloud and are available on Docker Hub as `kodekloud/ecs-project1` and `kodekloud/ecs-project2`.

Demo web pages:

* [https://kodekloud.com/ECS-project1](https://kodekloud.com/ECS-project1)
* [https://kodekloud.com/ECS-project2](https://kodekloud.com/ECS-project2)

Project 1 is a minimal Node.js + Express app that serves a simple HTML page.

## Project 1 — application files

Example HTML served at the root (views/index.ejs or similar):

```html theme={null}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="css/style.css" />
    <title>ECS Project 1</title>
  </head>
  <body>
    <h1>ECS Project 1</h1>
  </body>
</html>
```

Server code (index.js):

```javascript theme={null}
const express = require("express");
const path = require("path");

const app = express();

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
  res.render("index");
});

app.listen(3000, () => {
  console.log("Server is running on port 3000");
});
```

Note: This server listens on port 3000 inside the container. When configuring ECS make sure to expose that container port.

Dockerfile (production-focused):

```dockerfile theme={null}
FROM node:16
WORKDIR /usr/src/app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
EXPOSE 3000
CMD [ "node", "index.js" ]
```

## Launching the app using the ECS console (Quick Start wizard)

1. Sign in to the AWS Management Console and search for "ECS" → Elastic Container Service.
2. If you're new to ECS, use the "Get started" (quick start) wizard to bootstrap resources — it speeds up the initial deployment. After the wizard completes, you can delete the created resources and re-deploy manually to learn each component in detail.
3. In the wizard choose:
   * "Custom" for container configuration.
   * Container name: e.g. `ecs-project1`
   * Image: `kodekloud/ecs-project1`
   * Container port: 3000 (TCP) — this matches the port the app listens on inside the container.

Because the image is public, no repository credentials are required.

<Callout icon="lightbulb">
  When using Fargate with awsvpc networking, the host port is effectively the same as the container port you configure. If you need to expose the container on a different external port or run multiple containers that would otherwise require the same host port, use a load balancer or choose a different networking mode/EC2 setup and configure host ports accordingly.
</Callout>

<Frame>
  <img alt="Screenshot of the AWS Elastic Container Service container configuration page. It shows a container named &#x22;ecs-project1&#x22; using image &#x22;kodekloud/ecs-project1&#x22; with memory settings and a port mapping for container port 3000/tcp." />
</Frame>

## Advanced container settings to consider

Open the advanced container configuration to set:

* Health checks (container-level probes)
* Environment variables
* Volumes and mount points
* Logging (awslogs for CloudWatch)
* Resource limits (CPU/memory)
* Docker labels

Example health check you can add in the console:

```bash theme={null}
CMD-SHELL curl -f http://localhost:3000/ || exit 1
```

For centralized logs, configure the awslogs (CloudWatch) driver and provide:

* awslogs-group
* awslogs-region
* awslogs-stream-prefix

These settings mirror what you might put in a Docker Compose file or pass into `docker run`.

<Frame>
  <img alt="A screenshot of an AWS console form for container/task configuration showing Log configuration (awslogs keys and values like awslogs-group, awslogs-region us-east-1, awslogs-stream-prefix ecs), along with sections for Resource Limits and Docker Labels." />
</Frame>

## Service and cluster creation (wizard)

Continue the wizard to define the service:

* The wizard proposes a service name, e.g. `ecs-project1-service`.
* For this quick-start, leave the load balancer option set to "None" (you can add a load balancer later for external traffic or blue/green deployments).
* The wizard creates a cluster and supporting networking resources by default.

Important notes about the wizard-created cluster:

* Cluster: logical grouping of the compute resources where tasks run.
* Wizard-created cluster typically includes a dedicated VPC and subnets (it does not use your default VPC unless you opt in).

Review the launch summary. The wizard will create:

* Container definition
* Task definition
* Service
* Cluster
* Networking (VPC, subnets, security group)

Click Create to provision. Resource creation may take a few minutes.

<Frame>
  <img alt="A screenshot of the AWS Management Console showing the &#x22;Getting Started with Amazon Elastic Container Service (Amazon ECS) using Fargate&#x22; launch status and progress, with a list of resources being created (cluster, task definition, service) and related AWS integrations like VPC, subnets, and security group. The page indicates several items completed and some still pending." />
</Frame>

## Post-deployment: verify, test, and clean up

* Inspect running tasks in the cluster to verify status and task logs.
* If your tasks are in private subnets, you may need a load balancer, NAT, or a public subnet with correct security group rules to access the app externally.
* Test the application by hitting the task ENI (if public) or the load balancer DNS (recommended for production traffic).

Once you understand the defaults created by the wizard, tear down those resources and repeat the deployment manually to learn:

* How task definitions map to container settings
* How services maintain desired task counts and perform deployments
* How networking (VPC, subnets, security groups) and load balancers connect external traffic to tasks

## Quick reference table

| Resource Type   | Purpose                                     | Example / Notes                                               |
| --------------- | ------------------------------------------- | ------------------------------------------------------------- |
| Task Definition | Describes one or more containers for a task | Contains container image, port mappings, CPU/memory, env vars |
| Service         | Runs and maintains desired number of tasks  | Use to attach load balancer or update deployments             |
| Cluster         | Logical group for tasks and services        | Wizard creates a dedicated VPC/subnets by default             |
| Load Balancer   | Distributes external traffic to tasks       | Recommended for production and multiple tasks on same port    |
| CloudWatch Logs | Centralized logging for containers          | Configure awslogs-group & stream prefix in task definition    |

## Links and references

* Amazon ECS documentation: [https://docs.aws.amazon.com/ecs/](https://docs.aws.amazon.com/ecs/)
* AWS Fargate overview: [https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY].html](https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY].html)
* awsvpc networking mode: [https://docs.aws.amazon.[AWS_SECRET_ACCESS_KEY]-networking.html](https://docs.aws.amazon.[AWS_SECRET_ACCESS_KEY]-networking.html)
* AWS CloudWatch Logs: [https://docs.aws.amazon.com/cloudwatch/index.html](https://docs.aws.amazon.com/cloudwatch/index.html)
* Docker Compose reference: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)

<Callout icon="warning">
  Public container images are convenient for demos, but avoid using unvetted public images in production. Always validate or build your own images, scan for vulnerabilities, and control image sources via private registries or IAM-based access.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/amazon-elastic-container-service-aws-ecs/module/fb45f65b-b11f-447c-9a22-ae6eae5bfc9d/lesson/16a4ba52-de32-4f38-adbb-3ce39b2cfbd2" />
</CardGroup>
