# ECS Demo Part 1

Source: https://notes.kodekloud.com/docs/AWS-Solutions-Architect-Associate-Certification/Services-Compute/ECS-Demo-Part-1/page

This lesson covers deploying a simple Node.js application to AWS ECS using Docker and the AWS Console.

In this lesson, you will deploy a simple Node.js application to [AWS ECS](https://learn.kodekloud.com/user/courses/amazon-elastic-container-service-aws-ecs). Before working with ECS using the AWS Console, review the two public demo projects available on Docker Hub:

• [https://kodekloud.com/ecs-project1](https://kodekloud.com/ecs-project1)\
• [https://kodekloud.com/ecs-project2](https://kodekloud.com/ecs-project2)

Pull these images to follow along with the lesson.

***

## Project 1 Overview

Project 1 features a basic Node.js application using the Express framework to serve a simple HTML file. A GET request to the root path returns the HTML document.

### index.html

```html theme={null}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="css/style.css" />
    <title>Document</title>
  </head>
  <body>
    <h1>ECS Project 1</h1>
  </body>
</html>
```

```text theme={null}
user1 on user1 in ecs-project1 is v1.0.0 via ⎊
```

### Express Server Code

The Express server is configured to render the HTML page. The application listens on port 3000.

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

```bash theme={null}
user1 on user1 in ecs-project1 is 🧱 v1.0.0 via []
```

***

## Dockerfile

The Dockerfile below packages the application and exposes port 3000. When configuring your ECS container, ensure that port 3000 is specified.

```dockerfile theme={null}
FROM node:16
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD [ "node", "index.js" ]
```

***

## Deploying with the ECS Console

Navigate to the AWS Console and search for [Elastic Container Service (ECS)](https://learn.kodekloud.com/user/courses/amazon-elastic-container-service-aws-ecs). When you first use ECS, you will encounter a quick-start wizard. Although the wizard includes sample apps, choose a custom configuration to understand each underlying component.

### Step 1 – Using the Quick Start Wizard

When prompted by the wizard:

1. Click the **Get started** button.
2. Instead of selecting one of the example applications, choose *Custom* to provide your own configurations.

<Frame>
  <img alt="The image is a webpage for Amazon Elastic Container Service (ECS), highlighting features like running containers at scale, flexible container placement, and integration with other services. It includes a video thumbnail and a &#x22;Get started&#x22; button." />
</Frame>

<Frame>
  <img alt="The image shows a webpage from Amazon Web Services (AWS) for getting started with Amazon Elastic Container Service (ECS) using Fargate, featuring a diagram of ECS objects and container definitions." />
</Frame>

Configure the container using the following settings:

* **Container Name:** ECS-Project1
* **Image:** kodekloud/ECS-Project1 (public repository; no credentials required)
* **Memory Limits:** Adjust as needed.
* **Port Mapping:** Specify port 3000 (TCP). As the Express app listens on port 3000, set the container port to 3000.

> **lightbulb** Unlike a typical Docker run command (e.g., `-p 80:3000`), in ECS the external port must match the container port (e.g., 3000 mapped to 3000).

For example, your Docker run command would look like:

```bash theme={null}
docker run -p 3000:3000
```

Advanced container settings like health checks can also be configured. For example, add the following health check command:

```plaintext theme={null}
CMD-SHELL, curl -f http://localhost/ || exit 1
```

These settings are similar to options found in a Docker Compose file, allowing you to specify environment variables, volumes, resource limits, and labels.

<Frame>
  <img alt="The image shows a configuration interface for setting up AWS CloudWatch Logs, resource limits, and Docker labels, with fields for entering key-value pairs and limits." />
</Frame>

Click **Update** to complete the container configuration.

***

## Service and Cluster Setup

After the container configuration, click **Next** to proceed to the service definition. ECS will generate a service named *ECS-project1-service*. You may choose to attach a load balancer (for this demo, select *None*). The wizard will automatically provision a new cluster and VPC along with the required subnets.

<Frame>
  <img alt="The image shows a diagram explaining ECS objects and their relationships, along with a form for defining a service in an ECS cluster, including fields for service name, desired tasks, security group, and load balancer type." />
</Frame>

<Frame>
  <img alt="The image shows a configuration screen for setting up an AWS ECS cluster, including a diagram illustrating the relationship between ECS objects like container definition, task definition, service, and cluster. It also includes fields for entering a cluster name and options for VPC and subnets." />
</Frame>

Review the configuration details for your container, task definition, service, and cluster, then click **Create**. After a few minutes, select **View Service** to verify that your application has been deployed.

Before verifying, let’s review some ECS components that were created in the background.

***

## Exploring ECS Components

### Task Definitions

Task definitions serve as blueprints for your container configurations (including port mappings, environment variables, and volumes). Under **Task Definitions** in the ECS Console, locate the task definition for this project, noting that revisions indicate configuration changes.

<Frame>
  <img alt="The image shows the Amazon ECS console displaying a list of task definitions, all with an &#x22;ACTIVE&#x22; status. The interface includes options to create a new task definition and manage existing ones." />
</Frame>

Select the relevant task definition (for example, “first-run-task-definition”). The highest revision number indicates the latest configuration.

<Frame>
  <img alt="The image shows an Amazon ECS console page displaying task definitions with the name &#x22;first-run-task-definition&#x22; and three active revisions." />
</Frame>

Upon reviewing the configuration, you will notice settings such as Fargate usage, memory/CPU allocations, and the host-to-container mapping (port 3000 to port 3000).

<Frame>
  <img alt="The image shows an AWS management console interface for configuring a task execution IAM role and task size, including memory and CPU allocation. It also includes container definitions with details like port mappings and environment variables." />
</Frame>

### Clusters and Services

Within **Clusters**, the wizard-created cluster displays the active service *ECS-project1-service*. This service is associated with one desired task and, later, one running task.

<Frame>
  <img alt="The image shows an AWS ECS cluster dashboard with details about a cluster named &#x22;default,&#x22; including active services and tasks. It lists one active service, &#x22;ecs-project1-service,&#x22; using the Fargate launch type." />
</Frame>

Click on the service to review the network details (VPC, subnets, and security groups).

<Frame>
  <img alt="The image shows an AWS ECS service dashboard for &#x22;ecs-project1-service,&#x22; indicating its active status, task definition, and network access details. It includes information about the cluster, service type, and security groups." />
</Frame>

Under **Tasks**, you will find the running task. The details page displays a public IP address that can be used to access the application.

<Frame>
  <img alt="The image shows a task details page from a cloud service, displaying information about a running task, including network settings and container status. It includes details like the task ID, cluster, launch type, IP addresses, and container information." />
</Frame>

When you access the public IP on port 3000, the browser shows the simple HTML page served by your application.

> **lightbulb** If multiple tasks are running, each task will have a unique IP address. This dynamic nature is why a load balancer is crucial—it provides a stable endpoint for clients.

***

## Tearing Down the Quick Start Deployment

After confirming a successful deployment, delete the resources created via the quick start wizard. Delete the ECS service by navigating to the cluster, selecting the service, and confirming deletion (type “delete me” when prompted). Then, delete the cluster.

<Frame>
  <img alt="The image shows a dialog box for deleting a cluster in a cloud management interface, with a progress bar indicating the deletion of cluster resources. The user is prompted to enter &#x22;delete me&#x22; to confirm the deletion." />
</Frame>

Now that the ECS configuration is removed, you can deploy the application from scratch.

***

## Deploying from Scratch Using Fargate

### Creating a New Cluster

1. In the ECS Console, click **Create Cluster**.
2. Choose the "Networking only" option (Fargate).
3. Provide a cluster name (e.g., "cluster1"). Leave the default VPC CIDR block and subnets intact.
4. Click **Create**.

<Frame>
  <img alt="The image shows an AWS console interface for creating a cluster, with options to configure networking settings such as VPC, CIDR block, and subnets. It also includes a section for enabling CloudWatch Container Insights." />
</Frame>

Select **View Cluster** to inspect the new cluster.

***

### Creating a Task Definition

1. In the ECS Console, navigate to **Task Definitions** and click **Create new Task Definition**.
2. Select **Fargate** as the launch type.
3. Name the task definition (e.g., "ECS-Project1-taskdef") and choose the appropriate IAM role (this may have been auto-created if you previously ran the quick start wizard).
4. Choose Linux as the operating system and keep the default execution role.
5. Specify a minimal task size for this demo.

<Frame>
  <img alt="The image shows a configuration screen for creating a new task definition in AWS, specifically for setting up task and container definitions with options like task definition name, network mode, and task role." />
</Frame>

6. Add a container with these settings:
   * **Container Name:** node app
   * **Image:** kodekloud/ECS-Project1
   * **Health Check Command:**
     ```plaintext theme={null}
     CMD-SHELL, curl -f http://localhost/ || exit 1
     ```
   * **Port Mapping:** 3000

Click **Add** and then **Create** to finalize the task definition.

<Frame>
  <img alt="The image shows an AWS management console interface for configuring a task, including options for operating system family, task execution IAM role, and task size with a dropdown for selecting task memory in GB." />
</Frame>

***

### Creating a Service from the Task Definition

1. Within your cluster ("cluster1"), go to the **Services** tab and click **Create**.
2. Set the **Launch type** to Fargate and the **Operating system** to Linux.
3. Select the latest revision of your task definition ("ECS-Project1-taskdef").
4. Name your service (e.g., "project1-service") and choose the desired number of tasks (for instance, 2 to demonstrate scaling).
5. Click **Next**.

<Frame>
  <img alt="The image shows an AWS management console screen for configuring a service deployment, with options for service type, number of tasks, deployment type, and task tagging configuration. The &#x22;Next step&#x22; button is highlighted at the bottom." />
</Frame>

6. For the network configuration:
   * Select the VPC created for ECS.
   * Choose the two subnets.
   * Edit the default security group to permit incoming traffic on port 3000 (instead of port 80).
7. Skip the load balancer configuration for this demo.
8. Optionally disable autoscaling and click **Next**.

<Frame>
  <img alt="The image shows a configuration screen for setting up a network in AWS, specifically focusing on VPC and security groups. It includes options for selecting subnets, security groups, and enabling auto-assign public IP." />
</Frame>

<Frame>
  <img alt="The image shows an AWS console interface for configuring load balancing options, including choices for Application, Network, and Classic Load Balancers." />
</Frame>

<Frame>
  <img alt="The image shows an AWS management console screen for creating a service, displaying configuration details such as cluster, launch type, operating system, and network settings. It includes sections for reviewing service settings and configuring network and auto-scaling options." />
</Frame>

Finally, click **Create Service**. ECS will begin provisioning the two tasks. They may initially show a "PENDING" status until transitioning to "RUNNING."

<Frame>
  <img alt="The image shows an AWS ECS console displaying details of a task with a &#x22;PENDING&#x22; status, including network information and container details for a &#x22;node-app.&#x22;" />
</Frame>

Once the tasks are running, each will receive a unique public IP. Note that manually tracking these changing IPs is not ideal; hence a load balancer is recommended, as it establishes a consistent endpoint.

<Frame>
  <img alt="The image shows an AWS ECS console displaying details of a running task, including network information and container status." />
</Frame>

Click on a task to view its details and copy its public IP. Visiting this IP on port 3000 will display the simple HTML page of your application.

<Frame>
  <img alt="The image shows an AWS ECS task details page, displaying information about a running task, including network settings and container status." />
</Frame>

***

## Updating the Application

Suppose you decide to update the application by modifying the HTML. For example, you can add extra exclamation points to the H1 tag.

### Updated index.html

```html theme={null}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="css/style.css" />
    <title>Document</title>
  </head>
  <body>
    <h1>ECS Project 1!!!!!</h1>
  </body>
</html>
```

Rebuild your Docker image and tag it:

```bash theme={null}
docker build . -t kodekloud/ecs-project1
```

Push the updated image to Docker Hub. The output may look like:

```bash theme={null}
8cba2b7a5a3d: Layer already exists
2713d962e94: Layer already exists
72140ff0de3: Layer already exists
93a6676ff620: Layer already exists
c77311ff52e: Layer already exists
ba9804f7abed: Layer already exists
a5186a09280: Layer already exists
1e69438976e4: Layer already exists
47b6660a2b9b: Layer already exists
5cbc21d19fb: Layer already exists
07b905e91599: Layer already exists
20833a96725e: Layer already exists
latest: digest: sha256:98216dd964fd5bb910fb23a527ed9d804b5cedacaa47fb45264cebe664006b size: 3261
user1 on user1 in ecs-project1 [!] is v1.0.0 via ⬢ took 4s
```

The ECS service must be notified of this update. In the ECS Console, update the service by selecting **Update** and then opting for **Force new deployment**. This command instructs ECS to pull the latest image and deploy new tasks. Alternatively, if you modify the task definition (even if only the image tag changes), create a new revision and update your service to use this latest revision.

<Frame>
  <img alt="The image shows an AWS ECS configuration screen for setting up a service with options for task definition, launch type, operating system, and other deployment settings." />
</Frame>

If you create a new revision of the task definition, update the service appropriately.

<Frame>
  <img alt="The image shows a screenshot of the AWS console, specifically the &#x22;Create new revision of Task Definition&#x22; page for Amazon ECS. It includes fields for task definition name, task role, network mode, and other configuration options." />
</Frame>

After the update, the ECS Console will display both the old and new tasks running side by side until the health checks pass and the old tasks are terminated. The new tasks will receive different public IP addresses:

<Frame>
  <img alt="The image shows an Amazon ECS (Elastic Container Service) dashboard displaying cluster information, including one Fargate service with two running tasks and no data for CPU or memory utilization." />
</Frame>

Refreshing the service confirms that the new tasks are active with the updated application. This dynamic change of IPs further reinforces the necessity of a load balancer to provide a stable endpoint.

<Frame>
  <img alt="The image shows an Amazon ECS task details page, displaying information about a running task, including network settings and container status." />
</Frame>

***

## Cleanup and Next Steps

After verifying the updated deployment, you can delete the application resources if desired. In the ECS Console, delete the service (confirm by entering “delete me”) and ensure all tasks are terminated.

<Frame>
  <img alt="The image shows an AWS ECS (Elastic Container Service) dashboard displaying details of a cluster named &#x22;cluster1,&#x22; including task statuses and configurations. It lists two running tasks with their respective details such as task definition, status, and launch type." />
</Frame>

<Frame>
  <img alt="The image shows an AWS ECS console with a pop-up window asking for confirmation to delete a service named &#x22;project1-service.&#x22; The user is prompted to enter &#x22;delete me&#x22; to confirm the deletion." />
</Frame>

Next, we will demonstrate how to deploy a more complex application that includes a database, persistent storage (volumes), and a load balancer to ensure a single, stable endpoint for your front-end applications.

Happy deploying!

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-solutions-architect-associate-certification/module/afe0c951-fe76-47f2-9fc4-18858721be70/lesson/939c7164-d6d4-41ee-b16f-d7089a8c2c86)
