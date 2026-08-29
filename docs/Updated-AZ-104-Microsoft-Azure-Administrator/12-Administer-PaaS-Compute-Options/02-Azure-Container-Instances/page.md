# Azure Container Instances

Source: https://notes.kodekloud.com/docs/Updated-AZ-104-Microsoft-Azure-Administrator/Administer-PaaS-Compute-Options/Azure-Container-Instances/page

Azure Container Instances provide a serverless approach to deploying containerized applications, simplifying management and enhancing scalability within the Azure ecosystem.

Azure Container Instances (ACI) offer a serverless, streamlined approach to deploying containerized applications. In this guide, we compare traditional virtual machines (VMs) with containers and explain how ACI simplifies container deployment and management within the Azure ecosystem, making it an ideal solution for modern cloud applications.

## Comparing Virtual Machines and Containers

In cloud computing, both traditional VMs and modern containers serve as ways to run applications, but they follow distinct models.

### Virtual Machines

Virtual machines are a well-established method of virtualization. A typical VM setup includes:

* **Hypervisor:** A server hosting the hypervisor.
* **Guest Operating System:** Each VM runs its own guest OS.
* **Application Environment:** The allocated OS contains the application along with its necessary binaries and libraries.

This architecture provides robust isolation and security, as each VM operates independently. However, the overhead of maintaining a full operating system often leads to increased resource usage and slower startup times.

### Containers

Containers deliver a more agile and lightweight solution by:

* **Sharing the Host Kernel:** Containers use the host OS kernel while running in isolated user mode environments.
* **Packaging Dependencies:** Each container packages the application and its dependencies (libraries and binaries) without bundling an entire operating system.
* **Efficient Runtime:** Managed by a container runtime, containers are significantly smaller and faster to start compared to VMs.

Think of VMs as separate houses—each with their own infrastructure—whereas containers are like apartments within a building that share common utilities but maintain distinct, secure spaces.

### Detailed Comparison

| Feature               | Virtual Machines                                                        | Containers                                                                                            |
| --------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Isolation & Execution | Hardware-level isolation using a hypervisor and guest OS                | OS-level isolation with the host OS kernel simplifies management                                      |
| Deployment            | Involves provisioning an entire OS, configuring storage, and networking | Image-based deployment that encapsulates all dependencies for rapid scaling                           |
| Storage               | Uses block storage with its own file system                             | Supports ephemeral storage or persistent storage via volumes                                          |
| Fault Tolerance       | Achieved through replication, failover clustering, or availability sets | Utilizes orchestration tools (e.g., [Kubernetes](https://kubernetes.io/docs/)) for automatic recovery |

![The image compares virtual machines and containers, illustrating their architecture layers, including applications, libraries, guest OS, hypervisor, container runtime, host OS, and server. It highlights key features like isolation, deployment, storage, and fault tolerance.](https://kodekloud.com/kk-media/image/upload/v1752884744/notes-assets/images/Updated-AZ-104-Microsoft-Azure-Administrator-Azure-Container-Instances/vm-vs-containers-architecture-comparison.jpg)

> **lightbulb** Containers provide faster startup times and efficient resource usage, which makes them ideal for dynamic scaling and microservices architectures compared to traditional VMs.

## Azure Container Instances Overview

Azure Container Instances abstracts the infrastructure complexity, allowing you to run containerized applications without managing VMs. Under the hood, ACI leverages a virtual network and container host, equipped with a container runtime that simplifies container execution.

Key advantages of ACI include:

* **Fast Startup:**\
  Containers on ACI start in seconds, enabling rapid deployments—ideal for web applications, APIs, and event-driven workloads.
* **Strong Isolation:**\
  Each container instance operates in an isolated environment, ensuring processes remain secure and independent.
* **Scalability:**\
  ACI supports dynamic scaling by increasing the number of container instances as workload demands rise.
* **Persistent Storage:**\
  ACI allows you to mount Azure Storage volumes (such as Azure Files or Azure Disk) to facilitate persistent storage even though container instances are typically ephemeral.
* **Flexible Networking:**\
  Configure ACI for public or private networking, with features like port mapping, public IP assignment, and integration with Azure Virtual Networks for secure communications.
* **Multi-OS Support:**\
  Depending on your container image, ACI supports both Windows and Linux containers.

![The image illustrates the features and network setup of Azure Container Instances, highlighting benefits like faster startup, scalability, and isolation, alongside a diagram showing a container host within a virtual network.](https://kodekloud.com/kk-media/image/upload/v1752884745/notes-assets/images/Updated-AZ-104-Microsoft-Azure-Administrator-Azure-Container-Instances/azure-container-instances-network-setup.jpg)

## Deploying a Container Instance in Azure

Follow these steps to deploy a container instance using the Azure Portal:

1. **Launch the Azure Portal and Search for Container Instances:**\
   Open the Azure Portal, type “Container Instances” in the search bar, and click **Create**.

2. **Configure Basic Settings:**
   * **Resource Group:** Choose an existing resource group or create a new one (e.g., "ACI Web 0.1").
   * **Availability Zone:** Optionally specify an availability zone (such as East US Availability Zones currently in preview).
   * **SKU:** Choose the appropriate SKU (standard or confidential containers; this example uses standard).

3. **Select Your Container Image:**\
   Use a preconfigured image like Hello World, or pull an image from Azure Container Registry, Docker Hub, or another registry. For this walkthrough, select the NGINX image.

4. **Set Container Sizing and Advanced Options:**\
   Determine the container size and configure additional settings, like enabling GPU support if necessary.

![The image shows a Microsoft Azure portal interface for creating a container instance, with fields for subscription, resource group, container details, and image selection.](https://kodekloud.com/kk-media/image/upload/v1752884747/notes-assets/images/Updated-AZ-104-Microsoft-Azure-Administrator-Azure-Container-Instances/azure-portal-container-instance-creation.jpg)

5. **Configure Networking Options:**
   * Decide on the networking type (public, private, or none).
   * Optionally set a DNS label and specify open port numbers.
   * Adjust the container restart policy based on your requirements.

![The image shows a Microsoft Azure portal interface for creating a container instance, specifically on the "Networking" tab, where options for networking type, DNS name label, and port settings are being configured.](https://kodekloud.com/kk-media/image/upload/v1752884748/notes-assets/images/Updated-AZ-104-Microsoft-Azure-Administrator-Azure-Container-Instances/azure-portal-container-networking.jpg)

6. **Override Commands (Optional):**\
   If necessary, customize startup commands or scripts to run when the container launches.

7. **Review and Create:**\
   Verify your settings and click **Review and Create**. Once validation is complete, click **Create** to deploy your container. Deployments typically complete within 15 to 20 seconds.

8. **Access the Container Instance:**\
   When the deployment finishes, select **Go to resource**. You'll find details of your container instance, including its public IP address for direct access. For example, visiting the NGINX welcome page confirms the container is running smoothly.

![The image shows a Microsoft Azure portal interface displaying details of a container instance named "aci-web-01," including its status, location, and resource usage metrics like CPU and memory.](https://kodekloud.com/kk-media/image/upload/v1752884749/notes-assets/images/Updated-AZ-104-Microsoft-Azure-Administrator-Azure-Container-Instances/azure-portal-aci-web-01-details.jpg)

9. **Interact with the Container:**\
   Review logs and connect to your container using the integrated terminal. For example, you can navigate directories within a running NGINX container as shown below:

```bash theme={null}
