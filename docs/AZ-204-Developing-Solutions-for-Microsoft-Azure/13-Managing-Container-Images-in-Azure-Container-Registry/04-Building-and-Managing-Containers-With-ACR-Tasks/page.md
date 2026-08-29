# Building and Managing Containers With ACR Tasks

Source: https://notes.kodekloud.com/docs/AZ-204-Developing-Solutions-for-Microsoft-Azure/Managing-Container-Images-in-Azure-Container-Registry/Building-and-Managing-Containers-With-ACR-Tasks/page

This article explores building and managing containers using Azure Container Registry Tasks to automate the container lifecycle and streamline development workflows.

In this article, we explore the key phases of building and managing containers using Azure Container Registry (ACR) Tasks. ACR Tasks allow you to automate the entire container lifecycle—from building and testing to pushing and deploying container images—thereby streamlining your development and CI/CD workflows.

***

## Overview of the Container Lifecycle

Container lifecycle operations generally follow these steps:

1. **Build:** Package your application and its dependencies into a Docker image. A Dockerfile defines the build process, and ACR Tasks help automate this step to ensure consistency and efficiency.
2. **Test:** Integrate automated testing within ACR Tasks to validate the container image before deployment.
3. **Push:** After successful testing, push the validated image to ACR, making it accessible in a centralized registry across development, staging, and production environments.
4. **Deploy:** Deploy the containerized application to a live environment. ACR integrates seamlessly with Azure services such as Azure Kubernetes Service (AKS), Azure Container Instances (ACI), Azure Container Apps, and Azure App Service.

![The image illustrates the process of building and managing containers with ACR tasks, featuring four steps: Build, Test, Push, and Deploy, each represented by an icon.](https://kodekloud.com/kk-media/image/upload/v1752866700/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-Building-and-Managing-Containers-With-ACR-Tasks/acr-tasks-container-management-diagram.jpg)

ACR Tasks essentially function as a continuous integration and continuous deployment (CI/CD) pipeline for container images, significantly reducing manual intervention.

***

## Task Scenarios with ACR Tasks

ACR Tasks are flexible and support different workflows. Here are some common task scenarios:

### Kube-Task

A kube-task is ideal for one-time builds or immediate tasks. It allows you to build a container image without setting up a complex CI/CD pipeline—perfect for rapid development or prototyping.

### Automatically Triggered Tasks

Automatically triggered tasks execute based on specific events. For example, you can configure a trigger to start a new build whenever changes are detected in your source code repository. This integration with tools like [Azure Pipelines](https://azure.microsoft.com/en-us/services/devops/pipelines/) ensures your container images remain up to date.

### Multi-Step Tasks

Multi-step tasks enable you to design a comprehensive pipeline that includes additional steps such as testing or security scanning. By specifying a sequence of actions for your container image before it is pushed or deployed, you gain greater flexibility and control over your container management strategy.

![The image illustrates three types of task scenarios for building and managing containers: Quick Task, Automatically Triggered Task, and Multi-Step Task, each represented by a distinct icon.](https://kodekloud.com/kk-media/image/upload/v1752866701/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-Building-and-Managing-Containers-With-ACR-Tasks/container-task-scenarios-icons.jpg)

***

## Creating and Deploying a Container Image with ACR Tasks

This section demonstrates how to build a container image using a Dockerfile and then push that image to the Azure Container Registry.

### Step 1: Create the Azure Container Registry

1. Log into the [Azure Portal](https://portal.azure.com) and search for "Container Registry" in the search box.

![The image shows the Microsoft Azure portal with a search bar displaying results for "container," listing services like Container Apps and Container Instances. Below, there is a list of resources with their types and last viewed dates.](https://kodekloud.com/kk-media/image/upload/v1752866703/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-Building-and-Managing-Containers-With-ACR-Tasks/azure-portal-container-search-results.jpg)

2. Click **Create**.
3. Create a new resource group (e.g., `azr-az204-containers`).

![The image shows the Azure portal interface for creating a container registry, with a pop-up window prompting for a new resource group name.](https://kodekloud.com/kk-media/image/upload/v1752866705/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-Building-and-Managing-Containers-With-ACR-Tasks/azure-portal-container-registry-popup.jpg)

4. Provide a unique name for your registry (e.g., `azr-az204`). If the name is already taken, consider modifying it (for example, appending "KodeKloud" to ensure uniqueness).

![The image shows the "Create container registry" page on Microsoft Azure, where a user is attempting to set up a new container registry. An error message indicates that the chosen registry name is already in use.](https://kodekloud.com/kk-media/image/upload/v1752866708/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-Building-and-Managing-Containers-With-ACR-Tasks/create-container-registry-error-azure.jpg)

5. Select your preferred location (e.g., East US) and choose the Standard tier. Note that networking options such as private access are limited to the Premium plan.
6. Click **Review and Create** to deploy the registry.

Once deployment is complete, the Azure portal will confirm the registry creation.

![The image shows a Microsoft Azure portal page indicating that a deployment of "Microsoft.ContainerRegistry" is complete. It includes options to view deployment details, next steps, and a button to go to the resource.](https://kodekloud.com/kk-media/image/upload/v1752866709/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-Building-and-Managing-Containers-With-ACR-Tasks/azure-portal-container-registry-deployment.jpg)

***

### Step 2: Build Your Container Image Locally Using Cloud Shell

For this demonstration, we will use the Azure Cloud Shell. You can also perform these steps locally if preferred.

1. First, verify that the necessary .NET runtimes are installed:

```bash theme={null}
rithin [~] $ dotnet --list-runtimes
Microsoft.AspNetCore.App 8.0.0 [/usr/share/dotnet/shared/Microsoft.AspNetCore.App]
Microsoft.NETCore.App 8.0.0   [/usr/share/dotnet/shared/Microsoft.NETCore.App]
```

2. Create a directory for your application and navigate into it:

```bash theme={null}
rithin [~] $ mkdir App
rithin [~] $ cd App
```

3. Generate a new ASP.NET Core web application:

```bash theme={null}
rithin [~/App] $ dotnet new webapp -n MyWebApp
```

4. Navigate to the application's Pages directory to verify the landing page:

```bash theme={null}
rithin [~/App/MyWebApp] $ cd Pages
rithin [~/App/MyWebApp/Pages] $ ls
Error.cshtml  Error.cshtml.cs  Index.cshtml  Privacy.cshtml  Shared  _ViewImports.cshtml  _ViewStart.cshtml
```

5. Display the content of the landing page:

```bash theme={null}
rithin [~/App/MyWebApp/Pages] $ cat Index.cshtml
@page
@model IndexModel

<h1 class="display-4">Welcome</h1>
<p>Learn about <a href="https://learn.microsoft.com/aspnet/core">building Web apps with ASP.NET Core</a>.</p>
```

6. If you wish to edit the page, use an editor like nano, then return to the parent directory:

```bash theme={null}
rithin [~/App/MyWebApp/Pages] $ nano Index.cshtml
```

7. Change back to the project root and create a Dockerfile:

```bash theme={null}
rithin [~/App/MyWebApp] $ cd ../..
rithin [~/App] $ nano Dockerfile
```

8. Paste the following content into your Dockerfile, which uses .NET 8.0:

```dockerfile theme={null}
