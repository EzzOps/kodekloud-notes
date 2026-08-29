# Dockerfile
# Step 1: Use the official ASP.NET Core 8.0 runtime as the base image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80

# Step 2: Use the .NET 8.0 SDK image to build the app
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["MyWebApp/MyWebApp.csproj", "MyWebApp/"]
RUN dotnet restore "MyWebApp/MyWebApp.csproj"
COPY . .
WORKDIR "/src/MyWebApp"
RUN dotnet build "MyWebApp.csproj" -c Release -o /app/build

# Step 5: Publish the application
FROM build AS publish
RUN dotnet publish "MyWebApp.csproj" -c Release -o /app/publish

# Step 6: Create the final image with the app
FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "MyWebApp.dll"]
```

Save the Dockerfile after pasting.

> **lightbulb** Ensure that the project structure matches the paths in the Dockerfile to avoid build errors.

***

### Step 3: Build the Container Image Using ACR Build

1. In the Cloud Shell, run the following ACR build command. Be sure to replace the placeholders with your actual registry name and resource group:

```bash theme={null}
az acr build -r acraz204kodekloud -g rg-az204-containers -t webapp .
```

This command builds your container image using the Dockerfile in the current directory and automatically pushes it to your specified Azure Container Registry.

2. Monitor the terminal output to confirm that both the build and push stages complete successfully. You should see messages confirming that each step was successful, along with details about the image layers and build duration.

Example output:

```plaintext theme={null}
2024/09/14 16:16:50 Step ID: build marked as successful (elapsed time in seconds: 38.975983)
2024/09/14 16:16:51 Step ID: push marked as successful (elapsed time in seconds: 9.423809)
2024/09/14 16:16:51 The following dependencies were found:
  registry: acraz204kodekloud.azurecr.io
  repository: webapp
  tag: sha256:2f44bd0f2c9d2303a4cd1c15b7bf489649e01718e21
...
Run ID: ca2 was successful after 52s
```

3. To verify the published image, you can pull it from your registry using the following command:

```bash theme={null}
docker pull acraz204kodekloud.azurecr.io/webapp:v1
```

This command retrieves the version one (`v1`) of your image from the registry.

> **lightbulb** Always verify your built image in the Azure portal or via CLI to ensure successful deployment.

***

## Conclusion

In this article, we demonstrated how to build a containerized application using a Dockerfile, leverage Azure Container Registry Tasks to automate building and testing, and push the container image to the Azure Container Registry for further deployment. Next, we will cover deploying container images using Azure Container Instances to run your containerized application in a live environment.

Happy containerizing!

***

For additional details and Azure best practices, refer to the [Azure Documentation](https://docs.microsoft.com/azure/container-registry/) and enhance your container strategy with ACR Tasks.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-204-developing-solutions-for-microsoft-azure/module/21b47c50-0b14-4f95-b6ee-a219b7b1993f/lesson/a7b2452a-9bb5-4130-9a17-9f5382f5c1f5)


# Discovering Azure Container Registry

Source: https://notes.kodekloud.com/docs/AZ-204-Developing-Solutions-for-Microsoft-Azure/Managing-Container-Images-in-Azure-Container-Registry/Discovering-Azure-Container-Registry/page

This article covers Azure Container Registry, its use cases, service tiers, supported image types, and storage capabilities for managing container images.

Azure Container Registry (ACR) is a fully managed Docker registry that allows you to securely store and manage container images for both Azure deployments and other environments. It caters to a wide range of scenarios, from small-scale containerized applications to large-scale enterprise solutions.

In this lesson, you'll learn about ACR's key use cases, service tiers, supported artifact types, and robust storage capabilities.

## Key Use Cases

### Scalable Orchestration Systems

ACR seamlessly integrates with scalable orchestration platforms like Azure Kubernetes Service and Azure Container Apps. These systems manage containerized applications across clusters, enabling efficient scaling and workload distribution. This integration simplifies the management of high container volumes in dynamic environments.

### Integration with Azure Services

Deeply integrated with various Azure services, ACR is perfect for automating DevOps workflows and deploying containerized applications across multiple regions. Its tight integration within the Azure ecosystem streamlines operations, making it an excellent choice for enterprises leveraging cloud-native solutions.

![The image is an infographic about the Azure Container Registry, highlighting its use cases in scalable orchestration systems and Azure services. It describes managing containerized applications across clusters and supporting application building and running at scale.](https://kodekloud.com/kk-media/image/upload/v1752866710/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-Discovering-Azure-Container-Registry/azure-container-registry-infographic.jpg)

These use cases illustrate the flexibility and strength of Azure Container Registry for a wide range of deployment scenarios—from managing container orchestration systems to integrating with broader Azure services.

## Service Tiers

ACR offers multiple service tiers designed to accommodate different needs, ranging from development and testing to high-demand production environments.

### Basic Tier

The Basic tier is targeted primarily at development and testing environments. It delivers a cost-effective solution with limited storage and throughput, ideal for small-scale operations or early-stage projects.

### Standard Tier

Designed for production workloads, the Standard tier provides enhanced performance and more storage capacity. It fits mid-sized teams and organizations needing reliable performance, though it lacks some of the advanced features available in the Premium tier.

### Premium Tier

For high-demand environments, the Premium tier offers advanced features such as geo-replication. This ensures rapid, reliable access to container images across different regions, making it suitable for global deployments where performance and redundancy are critical.

![The image illustrates the service tiers of Azure Container Registry: Basic, Standard, and Premium, each represented by different icons.](https://kodekloud.com/kk-media/image/upload/v1752866711/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-Discovering-Azure-Container-Registry/azure-container-registry-tiers.jpg)

Selecting the right service tier allows you to align ACR's capabilities with your project requirements, whether you're in development, running production workloads, or managing large-scale deployments.

## Supported Image Types and Artifacts

Azure Container Registry supports a variety of image types and artifacts, ensuring versatility in managing different workloads. Key formats and features include:

* **Immutable Image Snapshots:** Images are stored as read-only snapshots, providing consistency during deployments and ensuring reliable rollouts.
* **Cross-Platform Support:** ACR supports both Linux and Windows container images, making it suitable for diverse development teams.
* **Helm Charts:** Manage Kubernetes applications efficiently with Helm charts stored directly in ACR.
* **OCI Compliance:** ACR adheres to Open Container Initiative (OCI) standards, ensuring interoperability with other tools and platforms.

![The image describes features of the Azure Container Registry, highlighting its support for Docker-compatible images, both Windows and Linux images, and storage of Helm charts and OCI-compliant images.](https://kodekloud.com/kk-media/image/upload/v1752866713/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-Discovering-Azure-Container-Registry/azure-container-registry-features.jpg)

These features ensure that you have a versatile and fully compliant platform for managing a wide variety of container workloads.

## Storage Capabilities

ACR not only stores container images but also guarantees that they are secure and available when needed. Its key storage capabilities include:

* **Encryption at Rest:** All images are encrypted while stored, protecting your data from unauthorized access.
* **Geo-Redundant Storage:** Container images are replicated across multiple regions using Azure's geo-redundant storage, enhancing availability and ensuring reliability during regional outages.
* **Geo-Replication in Premium Tier:** With the Premium tier, ACR supports geo-replication, reducing latency for global teams and ensuring high availability for rapid deployments.

![The image outlines three storage capabilities: Encryption at Rest, Geo-Redundant Storage, and Geo-Replication, with brief descriptions for each.](https://kodekloud.com/kk-media/image/upload/v1752866715/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-Discovering-Azure-Container-Registry/storage-capabilities-encryption-geo-redundant.jpg)

These robust storage capabilities make sure that your container images are secure and readily available whenever and wherever they are needed.

## Next Steps: Exploring Dockerfile Elements

Now that you have a comprehensive understanding of the benefits, use cases, service tiers, supported formats, and storage capabilities of Azure Container Registry, it's time to dive deeper into Dockerfile fundamentals. In the next part of our lesson, we will walk you through the elements of a Dockerfile and explain how to build container images and push them to ACR.

> **lightbulb** Stay tuned for our upcoming sections where we explore the practical aspects of Dockerfile syntax and usage, ensuring smooth container image management with ACR.

Happy learning!

- [Watch Video](https://learn.kodekloud.com/user/courses/az-204-developing-solutions-for-microsoft-azure/module/21b47c50-0b14-4f95-b6ee-a219b7b1993f/lesson/bff2a88a-0b71-4358-b2c6-7ab6c93d7c12)
