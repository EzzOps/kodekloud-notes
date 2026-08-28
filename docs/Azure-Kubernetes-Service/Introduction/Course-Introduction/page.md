# Course Introduction

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/Introduction/Course-Introduction/page

Learn to deploy, manage, and secure containerized applications on Microsoft Azure using Azure Kubernetes Service (AKS) in this comprehensive course.

Welcome to **Azure Kubernetes Service (AKS)**! I’m Pranav Holavanahalli, and in this course you’ll learn how to deploy, manage, and secure containerized applications on Microsoft Azure. As organizations embrace cloud-native architectures, proficiency with containers—and Kubernetes in particular—has become essential for DevOps, data, and cloud engineers.

Kubernetes powers a wide range of cloud workloads, from infrastructure and data services to machine learning and developer platforms. If you plan to specialize in Azure, mastering AKS is non-negotiable. This course covers core Azure concepts, containerization best practices, and end-to-end AKS operations.

***

## What You’ll Learn

| Module                           | Key Topics                                                                                                          |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Azure Fundamentals Refresher     | Compute, Storage, Networking, Identity, and Data Services on Azure                                                  |
| Containerizing a Web Application | Dockerfile authoring, image building, local testing, and publishing to Azure Container Registry (ACR)               |
| Deploying to AKS                 | Creating and configuring AKS clusters, scaling workloads, integrating with ACR, and rolling updates                 |
| Security & Networking in AKS     | Virtual Networking, Azure Active Directory integration, Azure Policy enforcement, and Azure Defender for containers |
| Monitoring & CI/CD for AKS       | Azure Monitor, Log Analytics, and building GitHub/Azure DevOps pipelines tailored to AKS deployments                |

<Callout icon="lightbulb">
  Hands-on practice is essential. We recommend using your own [Azure free account](https://azure.microsoft.com/free/) to follow along with the labs.
</Callout>

***

## Course Outline

### 1. Azure Fundamentals Refresher

We’ll begin with a concise review of Azure’s core services:

* **Compute**: Virtual Machines, VM Scale Sets, and App Services
* **Storage**: Blob, File, and Disk storage options
* **Networking**: Virtual Networks, Subnets, and Load Balancers
* **Data**: Azure SQL, Cosmos DB, and Data Lake Storage

### 2. Containerizing a Web Application

You’ll learn how to package your code into a container:

* Author and optimize a Dockerfile
* Build and test container images locally
* Publish images to Azure Container Registry

### 3. Deploying to AKS

Provision and manage your AKS cluster:

* Create and configure AKS clusters
* Scale pods and nodes to meet demand
* Integrate with Azure Container Registry for seamless image pulls
* Manage rolling updates to ensure zero-downtime deployments

### 4. Security & Networking in AKS

Protect your cluster and workloads:

* **Virtual Networks**: Isolate AKS in your VNet
* **Azure AD Integration**: Enable RBAC and pod identity
* **Azure Policy**: Enforce guardrails on namespaces and cluster add-ons
* **Azure Defender**: Runtime threat detection for containers

<Callout icon="triangle-alert">
  Always restrict API server access and enable network policies to prevent unauthorized lateral movement within your cluster.
</Callout>

### 5. Monitoring & CI/CD for AKS

Streamline observability and deployment:

* **Azure Monitor** & **Log Analytics**: Collect metrics, logs, and alerts
* **CI/CD Pipelines**: Set up GitHub Actions or Azure DevOps to build, test, and deploy your containers to AKS

***

## Links and References

* [Azure Kubernetes Service (AKS) Overview](https://docs.microsoft.com/azure/aks/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Azure Container Registry](https://docs.microsoft.com/azure/container-registry/)
* [Docker Documentation](https://docs.docker.com/)

Let's get started on your journey to mastering **Azure Kubernetes Service!**

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/azure-kubernetes-service/module/6a92f289-8fd3-4397-b8af-d48bf0da1186/lesson/79f986f4-5599-4d5a-a2d9-f8297739b4eb" />
</CardGroup>
