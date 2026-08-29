# Example (not applicable for ECS)
docker run -p 80:3000
```

In ECS, however, the external and internal ports must match (e.g., both being 3000). The advanced container configuration also allows you to set up health checks, environment variables, and volumes through a graphical interface. Click "Update" when the container configuration is complete.

### Defining Your ECS Service

After setting up the container:

* **Service Name:** For instance, "ECS-project1-service".
* **Load Balancer:** Optionally add one—select "none" for now.

The wizard creates a cluster that groups all underlying resources, provisioning a new VPC along with subnets automatically.

![The image shows a setup screen for defining a service in Amazon ECS, including a diagram of ECS objects and fields for service name, number of tasks, security group, and load balancer type.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858512/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/amazon-ecs-service-setup-diagram.jpg)

Review the configuration details including container definition, task definition, service details, and cluster settings. Then click "Create." Wait a few minutes for provisioning and click "View Service" when ready.

## Understanding the ECS Task Wizard Components

### 1. Task Definitions

Task definitions store all container configurations, including port mappings, volumes, and environment variables. Revision numbers help track changes, with the latest revision reflecting the current configuration.

![The image shows an AWS Management Console screen for creating or managing a task definition in Amazon ECS. It includes fields for task definition name, task role, network mode, operating system family, and compatibility settings.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858514/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-ecs-task-definition-console.jpg)

### 2. Cluster

The ECS cluster represents the infrastructure—whether EC2 instances when using the EC2 launch type, or a managed Fargate environment. The default cluster, set up by the wizard, includes a newly created VPC and subnets.

![The image shows an AWS ECS cluster dashboard with details about a cluster named "default." It displays information about tasks and services, including an active service named "ecs-project1-service" using Fargate.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858515/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-ecs-cluster-dashboard-default.jpg)

### 3. Service and Tasks

The service, "ECS-project1-service", is created with a desired task count (initially one). You can inspect network settings, including VPC, subnets, and security groups. The running task receives a public IP address which you can use to access the deployed application.

![The image shows an AWS ECS service dashboard for "ecs-project1-service," indicating its active status, task definition, and network access details, including VPC, subnets, and security groups. There are no load balancers configured.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858516/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-ecs-service-dashboard-ecs-project1-2.jpg)

![The image shows details of an AWS ECS task, including its status, network configuration, and container information. The task is running on Fargate with a public IP address of 44.211.129.14.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858517/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-ecs-task-fargate-details.jpg)

After obtaining the task’s public IP address and accessing it in a browser, you should see the demo HTML page served on port 3000, confirming the application deployment.

### Cleaning Up the Quick Start Environment

After verification, delete the environment created by the quick start wizard in order to redeploy from scratch:

1. In your cluster, select the service and delete it. Confirm with "delete me." Ensure that all tasks are removed.
2. Delete the cluster.

![The image shows a dialog box for deleting an AWS ECS cluster, with a progress bar indicating the deletion of resources and a text field requiring confirmation by typing "delete me."](../../../../images/kodekloud.com/kk-media/image/upload/v1752858518/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-ecs-cluster-delete-dialog.jpg)

With the ECS environment cleared, you are now ready to deploy the application manually.

## Creating a New ECS Cluster

1. In the ECS Console, click **Create Cluster**.
2. Choose **Networking only** if using Fargate. (For EC2, you can choose between Linux and Windows options.)
3. Name your cluster (for example, "cluster1") and create a new VPC with default CIDR and subnet settings.
4. Click **Create**.

![The image shows an AWS interface for configuring a new cluster, including options for setting up a VPC, CIDR block, subnets, and enabling CloudWatch Container Insights.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858520/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-cluster-configuration-interface.jpg)

![The image shows an AWS ECS launch status page, indicating that an ECS cluster named "cluster1" has been successfully created, with CloudFormation stack resources being set up and various cluster resources listed.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858521/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-ecs-cluster1-launch-status.jpg)

## Creating Task Definitions for Your New Cluster

1. Navigate to **Task Definitions** and click **Create new Task Definition**.
2. Select **Fargate** as the launch type.
3. Name the task definition (e.g., "ECS-Project1") and assign the appropriate task execution role.
4. Choose Linux as the operating system and allocate modest CPU and memory resources for the demo.
5. Add a container:
   * **Container Name:** (e.g., "node app")
   * **Image:** Use "KodeKloud/ECS-Project1"
   * **Port Mapping:** Set to 3000

![The image shows a configuration screen for creating a new task definition in AWS, specifically for setting up task and container definitions with options like task name, network mode, and task role.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858522/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-task-definition-configuration.jpg)

After configuring the task definition, click **Add** and then **Create**.

## Creating the ECS Service

1. In your new cluster ("cluster1"), go to the **Services** tab and click **Create Service**.
2. Configure the following:
   * **Launch Type:** Fargate
   * **Operating System:** Linux
   * **Task Definition:** Select "ECS-Project1" (latest revision)
   * **Service Name:** (e.g., "project1-service")
   * **Number of Tasks:** For demonstration purposes, choose 2 tasks.
3. Set up networking:
   * Select the VPC created earlier.
   * Choose the appropriate subnets.
   * Configure the security group: Change the default setting (typically allowing traffic on port 80) to allow Custom TCP traffic on port 3000 from anywhere.

![The image shows a configuration screen for creating a service in AWS, specifically focusing on network settings such as VPC, subnets, and security groups. Options for enabling public IP assignment and health check grace periods are also visible.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858523/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-service-configuration-network-settings.jpg)

4. Proceed without a load balancer by selecting **No load balancer** (this will be discussed later).
5. Optionally configure auto scaling, then click **Next** to review all configurations.
6. Finally, click **Create Service**.

![The image shows an AWS console screen for creating a service, displaying configuration details such as cluster, launch type, task definition, and network settings. It includes options for reviewing and editing service parameters.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858525/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-console-service-creation-screen.jpg)

Initially, the console may show no tasks until refreshed; you should then notice two tasks being provisioned. Each task receives its own public IP address which requires tracking if not behind a load balancer. A load balancer is recommended for production environments to provide a consistent endpoint and handle traffic distribution.

![The image shows an AWS ECS console displaying details of a service named "project1-service" within a cluster. It includes information about task definitions, status, and launch type, with tasks currently in the "PROVISIONING" state.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858526/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-ecs-console-project1-service.jpg)

Click on a task to view its details, then copy its public IP address and open it in your browser at port 3000. The expected output is the simple HTML page served by the application. Note that each new deployment generates new public IP addresses, which underscores the importance of using a load balancer in production.

![The image shows an AWS ECS task details page, displaying information about a running task, including cluster details, network configuration, and container status.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858528/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-ecs-task-details-page.jpg)

## Updating Your Application

Suppose you modify the HTML file by adding extra exclamation marks to the H1 tag. The updated HTML might look like this:

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
  <h1>ECS Project 1!!!!</h1>
</body>
</html>
```

To build and push the changed Docker image, use the following commands:

```bash theme={null}
docker build -t KodeKloud/ECS-project1 .
```

```bash theme={null}
docker push KodeKloud/ECS-project1
```

Even after pushing the updated image, the running ECS service continues to use the old image until you force a new deployment. To do this, go to the ECS Console, select your service in the cluster, click **Update**, and then choose **Force new deployment**. This instructs ECS to pull the latest image and deploy updated tasks.

Alternatively, if you update the task definition, create a new revision (e.g., revision 2) and update the service to use it. ECS will then start tasks with the latest configuration, and once health checks pass, the old tasks are terminated.

![The image shows a web interface for creating a new revision of a task definition in Amazon ECS. It includes fields for task definition name, task role, network mode, and other configuration options.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858529/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/amazon-ecs-task-definition-revision.jpg)

When new tasks are deployed, they will obtain new public IP addresses. While this confirms the update, it also illustrates why a load balancer is essential—it provides a stable endpoint and manages traffic distribution automatically.

![The image shows an AWS ECS dashboard for "project1-service" with tasks running on Fargate. It displays details like task definitions, status, and platform version.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858531/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-ecs-dashboard-project1-service.jpg)

Refresh the ECS console to verify that only the desired number of tasks (in this example, two) are running, and that the deployment process has gracefully terminated the old tasks.

![The image shows an AWS ECS console displaying details of a running task, including cluster information, network settings, and container status.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858532/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-ecs-console-running-task-details.jpg)

## Final Notes

This demonstration has shown how to deploy and update a basic application on ECS using both the quick start wizard and manual configuration. Although each ECS task gets a unique IP address, a load balancer is recommended for production to provide a single, stable endpoint and to manage IP changes seamlessly.

After completing the demo, remember to delete the entire service before moving to more complex environments that involve databases, volumes, and load balancing.

![The image shows an AWS ECS console displaying details of a cluster named "cluster1," including task statuses and configurations. It lists two running tasks with their respective details such as task definition, status, and launch type.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858535/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/aws-ecs-cluster1-task-status.jpg)

Delete the service and confirm that all tasks are removed. The cluster will remain, allowing you to deploy your next application.

> **lightbulb** This guide detailed the process of setting up, deploying, updating, and cleaning up an ECS-based application. For production-grade deployments, always consider integrating a load balancer to manage traffic effectively.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/c28ddfac-bdff-4566-b056-f6c6391a0d11/lesson/3140dd13-31c2-4c5a-8e18-9a962e7866c7)


# ECS Demo Part 2

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Containers-on-AWS/ECS-Demo-Part-2/page

This guide explains setting up a multi-container application on Amazon ECS using an Express API and MongoDB.

In this guide, we will walk through setting up a multi-container application on Amazon ECS. The application consists of two containers: an Express API container built with Node.js and a MongoDB container. The following Docker Compose file demonstrates the basic architecture:

```yaml theme={null}
version: "3"
services:
  api:
    build: .
    image: kodekloud/ecs-project2
    environment:
      - MONGO_USER=mongo
      - MONGO_PASSWORD=password
      - MONGO_IP=mongo
      - MONGO_PORT=27017
    ports:
      - "3000:3000"
  mongo:
    image: mongo
    environment:
      - MONGO_INITDB_ROOT_USERNAME=mongo
      - MONGO_INITDB_ROOT_PASSWORD=password
    volumes:
      - db:/data/db
volumes:
  db:
```

The API container hosts a simple CRUD application for managing notes. It connects to MongoDB using environment variables defined in both containers. For example, the API constructs a connection URL similar to:

```javascript theme={null}
const mongoURL = `mongodb://${process.env.MONGO_USER}:${process.env.MONGO_PASSWORD}@${process.env.MONGO_IP}:${process.env.MONGO_PORT}/?authSource=admin`;
```

Key RESTful endpoints include the following:

1. **Retrieve All Notes**\
   A GET request to `/notes`:

   ```javascript theme={null}
   app.get("/notes", async (req, res) => {
     try {
       const notes = await Note.find();
       res.status(200).json({ notes });
     } catch (e) {
       console.log(e);
       res.status(400).json({});
     }
   });
   ```

2. **Retrieve a Specific Note**\
   A GET request to `/notes/:id`:

   ```javascript theme={null}
   app.get("/notes/:id", async (req, res) => {
     try {
       const note = await Note.findById(req.params.id);
       if (!note) {
         return res.status(404).json({ message: "Note not found" });
       }
       res.status(200).json({ note });
     } catch (e) {
       console.log(e);
       res.status(400).json({ status: "fail" });
     }
   });
   ```

3. **Create a New Note**\
   A POST request to `/notes`:

   ```javascript theme={null}
   app.post("/notes", async (req, res) => {
     console.log(req.body);
     try {
       const note = await Note.create(req.body);
       return res.status(201).json({ note });
     } catch (e) {
       console.log(e);
       return res.status(400).json({ status: "fail" });
     }
   });
   ```

4. **Update an Existing Note**\
   A PATCH request to `/notes/:id`:

   ```javascript theme={null}
   app.patch("/notes/:id", async (req, res) => {
     try {
       const note = await Note.findByIdAndUpdate(req.params.id, req.body, {
         new: true,
         runValidators: true,
       });
       if (!note) {
         return res.status(404).json({ message: "Note not found" });
       }
       res.status(200).json({ note });
     } catch (e) {
       console.log(e);
       res.status(400).json({ status: "fail" });
     }
   });
   ```

5. **Delete a Note**\
   A DELETE request to `/notes/:id`:

   ```javascript theme={null}
   app.delete("/notes/:id", async (req, res) => {
     try {
       const note = await Note.findByIdAndDelete(req.params.id);
       if (!note) {
         return res.status(404).json({ message: "Note not found" });
       }
       res.status(200).json({ status: "success" });
     } catch (e) {
       console.log(e);
       res.status(400).json({ status: "fail" });
     }
   });
   ```

The application leverages the Mongoose library to manage MongoDB connections. A simplified example of the setup is shown below:

```javascript theme={null}
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const Note = require("./models/noteModel");

const app = express();
app.use(cors({}));
app.use(express.json());

const mongoURL = `mongodb://${process.env.MONGO_USER}:${process.env.MONGO_PASSWORD}@${process.env.MONGO_IP}:${process.env.MONGO_PORT}/?authSource=admin`;

// Alternative for local development:
// const mongoURL = 'mongodb://localhost:27017/?authSource=admin';

app.get("/notes", async (req, res) => {
  try {
    const notes = await Note.find();
    res.status(200).json({ notes });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});
```

***

Before deploying the containerized app on ECS, several AWS components must be configured.

## Creating a Security Group

Begin by creating a security group for your ECS application. In the EC2 console, navigate to "Security Groups" and create a new group named "ECS SG" with a description like "ECS security group." For testing purposes, add a rule to allow all traffic from any IP (note that this is not recommended for production). Ensure that the security group is associated with the correct VPC.

![The image shows an AWS EC2 dashboard displaying a list of security groups with details such as security group ID, name, VPC ID, description, and owner. The left sidebar includes navigation options for various EC2 and AWS services.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858538/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-2/aws-ec2-dashboard-security-groups.jpg)

After configuring the security group, proceed to create your ECS task definition.

***

## Creating an ECS Task Definition

In the ECS console under "Task Definitions," create a new Fargate task definition (for example, "ECS-project-one"). Configure the following settings:

* **Task Role:** Use the ECS task execution role.
* **Memory:** Choose minimal memory options for testing.
* **Containers:** Add both containers to the task definition.

### Configuring the MongoDB Container

For the MongoDB container, use the following configuration:

* **Name:** Mongo
* **Image:** Use the default Mongo image from Docker Hub.
* **Port Mapping:** Map port 27017.
* **Environment Variables:** Set up the MongoDB root username and password (e.g., mongo/password).
* **Volume:** Mount a persistent volume.

![The image shows an AWS security group configuration screen with sections for inbound and outbound rules, both set to allow all traffic. There is also an optional tags section at the bottom.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858540/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-2/aws-security-group-configuration.jpg)

Add the following environment variables to mirror the Docker Compose file:

```yaml theme={null}
environment:
  - MONGO_USER=mongo
  - MONGO_PASSWORD=password
  - MONGO_IP=mongo
  - MONGO_PORT=27017
```

![The image shows a configuration interface for configuring a container, including fields for entry point, command, environment variables, container timeouts, and network settings. It appears to be part of a cloud service management platform.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858542/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-2/container-configuration-ui-cloud-service.jpg)

### Configuring the Express API Container

For the API container:

* **Name:** Web API (or similar)
* **Image:** Use your pre-built image from Docker Hub (e.g., kodekloud/ecs-project2).
* **Port Mapping:** Map container port 3000.
* **Environment Variables:** Supply the four variables required for MongoDB connectivity.

Because ECS does not offer DNS-based inter-container resolution like Docker Compose, the API must use localhost to reach the Mongo container within the same task. With Mongo listening on port 27017, ensure your connection string matches that configuration.

![The image shows a configuration screen for adding a container, with fields for CPU units, entry point, command, and environment variables related to MongoDB settings.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858544/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-2/mongodb-container-configuration-screen.jpg)

### Defining Volumes

Next, add a volume (e.g., "Mongo-DB") using AWS Elastic File System (EFS) to persist MongoDB data. In the ECS task definition, navigate to the "Volumes" section and create a new volume. You must first create an EFS from the AWS console.

![The image shows a dialog box for adding a volume in an AWS interface, with options for configuring volume type, file system ID, access point ID, and other settings.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858545/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-2/aws-volume-add-dialog-box.jpg)

Follow these steps for setting up EFS:

1. Create a new file system in the EFS console. Provide a name (e.g., MongoDB) and ensure it is within the same VPC as your ECS cluster.
2. Customize mount targets by choosing appropriate subnets and update the default security group to one that allows NFS (typically port 2049). For enhanced security, create a dedicated security group for EFS that permits inbound NFS traffic only from the ECS security group.

![The image shows an AWS console screen for setting up network access for Amazon EFS, including options for selecting a Virtual Private Cloud (VPC), availability zones, subnet IDs, and security groups.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858547/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-2/aws-console-efs-network-setup.jpg)

Once your EFS is created and secured, update the Mongo container’s storage settings:

* Under "Mount Points," set the source to the created volume (e.g., MongoDB) and mount it to `/data/db` as required by MongoDB.

![The image shows a configuration interface for adding a container, including options for log configuration, resource limits, and Docker labels. It appears to be part of a cloud service management dashboard.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858549/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-2/docker-container-configuration-interface.jpg)

After configuring the volumes, create or update the task definition and verify that both containers (API and Mongo) display the correct settings.

![The image shows a configuration screen for editing a container in AWS, with options for storage, logging, and service integration settings. It includes fields for mount points, volumes, and log configuration with CloudWatch Logs.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858550/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-2/aws-container-edit-configuration.jpg)

***

## Creating the ECS Service and Load Balancer

After finalizing your task definition, create an ECS service with the following steps:

1. Navigate to your ECS Cluster (e.g., Cluster One) and create a new Fargate service.
2. Select the newly created task definition (e.g., ECS-project-two) and specify a service name (e.g., "notes app service"). Set the desired number of tasks (typically one for testing).
3. Ensure you select the proper VPC and subnets, and attach the previously created "ECS SG" security group.

![The image shows a configuration screen for setting up an AWS ECS service, including fields for operating system, task definition, cluster, service name, and deployment options.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858551/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-2/aws-ecs-service-configuration-screen.jpg)

### Configuring the Application Load Balancer

To distribute traffic and provide a static endpoint for the application:

1. Choose an Application Load Balancer and open its configuration in a new tab.
2. Provide a name (e.g., "notes lb"), set it as internet-facing, and select the IPv4 address type. Ensure that it is associated with the same VPC.
3. Create a dedicated security group for the load balancer (e.g., "lb-SG"). Although opening port 3000 might be an initial thought, it is preferable to have the load balancer listen on the default HTTP port (80) and forward traffic to the container’s port (3000). Configure the rule to allow HTTP traffic from any source.

![The image shows an AWS EC2 dashboard displaying a list of security groups, including details like security group IDs, names, VPC IDs, descriptions, and permission entries. A notification at the top indicates that two security groups have been successfully deleted.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858552/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-2/aws-ec2-dashboard-security-groups-2.jpg)

4. Next, create a target group (e.g., "notes-targetgroup1"). For ECS tasks, select the target type as IP. Configure the health check settings—by default, the health check is set to `/`, but since application endpoints reside under `/notes`, update the health check path to `/notes` (or set up a dedicated health check endpoint).

![The image shows a configuration screen for setting up an Application Load Balancer on AWS, including fields for target group name, protocol, IP address type, VPC, and health checks.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858553/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-2/aws-application-load-balancer-configuration.jpg)

5. In the ECS service configuration, link the load balancer by selecting the Application Load Balancer and mapping it to the API container (listening on port 3000). The load balancer will listen on port 80 and forward traffic to the target group.

![The image shows a configuration screen for setting up an Application Load Balancer in AWS, with options for load balancer name, listener port, protocol, and target group settings.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858554/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-2/aws-application-load-balancer-setup.jpg)

Review all settings and create the service. Initially, the ECS console will show tasks in a provisioning state until they run.

***

## Verifying the Deployment

Once the tasks are running, test the setup by either accessing the container’s public IP or, preferably, using the load balancer’s DNS name. For example, sending a GET request to:

http\://\<load-balancer-dns>/notes

should return the list of notes. Tools like Postman can be used to verify the RESTful API endpoints.

A sample POST request body to create a new note:

```json theme={null}
{
  "title": "second note",
  "body": "remember to do dishes!!!!"
}
```

A successful GET request may return a response similar to:

```json theme={null}
{
  "notes": [
    {
      "_id": "6321a3c034fd55dce212834",
      "title": "second note",
      "body": "remember to do dishes!!!!",
      "__v": 0
    }
  ]
}
```

Once the deployment is verified, update your ECS security group ("ECS SG") to restrict inbound traffic. Instead of allowing all traffic, configure a custom TCP rule for port 3000 that permits traffic only from the load balancer’s security group. This ensures that only load-balanced traffic reaches the API container.

![The image shows an AWS security group configuration screen, displaying details and inbound rules for a specific security group named "ecs-sg."](../../../../images/kodekloud.com/kk-media/image/upload/v1752858556/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-2/aws-security-group-ecs-sg-config.jpg)

> **lightbulb** After confirming that your application is functioning as expected, consider tightening your security group rules and reviewing best practices for production deployments.

***

This article demonstrated how to deploy a multi-container application on ECS using Docker Compose as a reference. We covered the configuration of ECS task definitions, setting up persistent storage with EFS, and configuring an Application Load Balancer to securely distribute traffic among containers.

For additional resources and detailed AWS documentation, please refer to:

* [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
* [Docker Hub](https://hub.docker.com/)
* [Amazon EFS Documentation](https://docs.aws.amazon.com/efs/)

Happy deploying!

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/c28ddfac-bdff-4566-b056-f6c6391a0d11/lesson/019d9960-feaf-4517-acd1-6f280498618f)
