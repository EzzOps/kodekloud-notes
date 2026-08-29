# Set Metadata
$headers = @{
    "x-ms-version"            = "2021-04-10"
    "x-ms-date"               = (Get-Date).ToString("R")
    "x-ms-meta-owner"         = "admin"
    "x-ms-meta-environment"   = "production"
}

$authHeader = "SharedKey $accountName:$([Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($accountKey)))"
Invoke-RestMethod -Uri "$baseUri?restype=container" -Method Put -Headers $headers -Header @{Authorization = $authHeader}

# Get Properties
$response = Invoke-RestMethod -Uri "$baseUri?restype=container&comp=metadata" -Method Get -Headers $headers
Write-Host "Owner: $($response.Headers.'x-ms-meta-owner'), Env: $($response.Headers.'x-ms-meta-environment'), Last Modified: $($response.Headers.'Last-Modified')"
```

> **lightbulb** When using the account key for authorization, ensure it is properly encoded to Base64 to secure your API calls.

## Example in Visual Studio Using .NET

The following example demonstrates how to work with container properties and metadata within a .NET console application. In this demonstration, you will create a new console project, add the necessary NuGet packages, and write code to connect to your storage account using a connection string.

1. Create a new Console Application project in Visual Studio (targeting .NET 6) and name it "Container Metadata Demo".

![The image shows a software development environment with a dialog box for configuring a new console application, where you can enter a project name, solution name, and set the location. The left panel displays a project structure with dependencies and a program file.](https://kodekloud.com/kk-media/image/upload/v1752866782/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-Managing-Container-Properties-and-Metadata/software-development-console-application-config.jpg)

2. Open the NuGet Package Manager and install the required Azure Storage libraries. Once added, replace the default code with the following:

```csharp theme={null}
using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        // Replace with your connection string and container name from the Azure portal.
        string connectionString = "your_connection_string";
        string containerName = "your_container_name";

        // Initialize the BlobServiceClient and BlobContainerClient.
        BlobServiceClient blobServiceClient = new BlobServiceClient(connectionString);
        BlobContainerClient containerClient = blobServiceClient.GetBlobContainerClient(containerName);
        await containerClient.CreateIfNotExistsAsync();

        // Define metadata to set on the container.
        var metadata = new Dictionary<string, string>
        {
            { "user", "admin" },
            { "env", "lab" }
        };

        // Set the metadata for the container.
        await containerClient.SetMetadataAsync(metadata);

        // Retrieve and display the container's metadata.
        BlobContainerProperties properties = await containerClient.GetPropertiesAsync();
        foreach (var item in properties.Metadata)
        {
            Console.WriteLine($"{item.Key}: {item.Value}");
        }
    }
}
```

This code initializes the Azure Blob Storage client, creates the container if it doesn't already exist, and sets metadata with the keys "user" and "env". It then retrieves the container properties and prints the metadata to the console.

For quick reference, here is a summarized version of the key operations:

```csharp theme={null}
var metadata = new Dictionary<string, string>
{
    { "user", "admin" },
    { "env", "lab" }
};

await containerClient.SetMetadataAsync(metadata);

BlobContainerProperties properties = await containerClient.GetPropertiesAsync();
foreach (var item in properties.Metadata)
{
    Console.WriteLine($"{item.Key}: {item.Value}");
}
```

Expected console output:

```plaintext theme={null}
user:admin
env:lab
```

## Summary

In this guide, we demonstrated how to manage Azure Blob Storage container properties and metadata using both the .NET SDK and PowerShell with REST APIs. Key takeaways include:

* Using GET (or `GetPropertiesAsync` in .NET) to retrieve container properties and metadata.
* Using PUT (or `SetMetadataAsync` in .NET) to set metadata and properties.
* Ensuring the account key is properly Base64-encoded for secure API calls.
* Leveraging the .NET SDK to simplify container management tasks.

> **lightbulb** For more information on Azure Blob Storage and managing metadata, visit the [Azure Blob Storage Documentation](https://docs.microsoft.com/en-us/azure/storage/blobs/).

By following this guide, you'll be able to efficiently organize and manage your Azure Blob Storage containers, ensuring your data is effectively maintained and secured.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-204-developing-solutions-for-microsoft-azure/module/bd8aef3d-3583-45c6-a1a8-8161e7578cbb/lesson/c7b1dda0-8826-45c1-9035-a8dd08a2ece4)


# Change Feed in Azure Cosmos DB

Source: https://notes.kodekloud.com/docs/AZ-204-Developing-Solutions-for-Microsoft-Azure/Working-With-Azure-Cosmos-DB/Change-Feed-in-Azure-Cosmos-DB/page

Azure Cosmos DBs change feed tracks modifications in real time, enabling applications to process updates sequentially through push or pull models.

Azure Cosmos DB's change feed is a robust feature that maintains a persistent record of all modifications made to items within a container. By leveraging the change feed, applications can track updates in real time and process them sequentially, ensuring that no changes are overlooked.

There are two primary models for utilizing the change feed: the push model and the pull model.

* In the **push model**, changes are immediately sent to consumers as soon as they occur. This approach is ideal for event-driven architectures where continuous polling is not desirable.
* In the **pull model**, the application periodically polls the change feed to retrieve changes. This method offers greater control over when and how frequently changes are processed, making it suitable for scenarios where immediate reaction is not required. However, it does demand additional management of the polling infrastructure to maintain consistency.

For most real-time processing scenarios, the push model is often preferred as it eliminates the need for constant polling and simplifies the overall process.

![The image illustrates the change feed in Azure Cosmos DB, showing a flow from Azure Cosmos DB to push and pull models, with Azure Functions triggers and a change feed processor library.](https://kodekloud.com/kk-media/image/upload/v1752866783/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-Change-Feed-in-Azure-Cosmos-DB/azure-cosmos-db-change-feed-diagram.jpg)

Azure recommends two native options for implementing the push model:

1. **Azure Functions with Cosmos DB triggers**\
   Automatically trigger functions when changes occur. This option removes the need for continuous polling and simplifies scaling within event-driven architectures.

2. **Change Feed Processor Library**\
   Available as part of the Cosmos DB SDK for .NET and Java, this library facilitates reading the change feed and distributing events across multiple consumers, ensuring horizontally scalable processing.

![The image explains the use of Azure Functions and Change Feed Processor in Azure Cosmos DB. It highlights how Azure Functions are triggered by new events in the change feed, and how the Change Feed Processor simplifies event processing across multiple consumers.](https://kodekloud.com/kk-media/image/upload/v1752866785/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-Change-Feed-in-Azure-Cosmos-DB/azure-functions-change-feed-processor.jpg)

## Key Components of the Change Feed Processor Architecture

The change feed processor architecture comprises four main components:

* **Monitored Container:** The source container where changes occur.
* **Lease Container:** Manages distributed processing by coordinating leases.
* **Compute Instance:** Processes the changes.
* **Delegate:** Contains custom logic to handle each change.

Together, these components enable you to build scalable and resilient systems that respond to changes in real time.

> **lightbulb** For optimized processing and scalability, ensure that your lease container is appropriately provisioned to handle the expected throughput.

## Sample Code: Setting Up the Change Feed Processor

The following C# code snippet demonstrates how to set up the change feed processor using the Cosmos DB SDK. In this example, the processor is initialized with the source container, lease container, and a delegate function that processes the changes.

```csharp theme={null}
private static async Task<ChangeFeedProcessor> StartChangeFeedProcessorAsync(
    CosmosClient cosmosClient,
    IConfiguration configuration)
{
    string databaseName = configuration["SourceDatabaseName"];
    string sourceContainerName = configuration["SourceContainerName"];
    string leaseContainerName = configuration["LeasesContainerName"];
    
    Container leaseContainer = cosmosClient.GetContainer(databaseName, leaseContainerName);
    
    ChangeFeedProcessor changeFeedProcessor = cosmosClient.GetContainer(databaseName, sourceContainerName)
        .GetChangeFeedProcessorBuilder<ToDoItem>(
            processorName: "changeFeedSample",
            onChangesDelegate: HandleChangesAsync)
        .WithInstanceName("consoleHost")
        .WithLeaseContainer(leaseContainer)
        .Build();
        
    Console.WriteLine("Starting Change Feed Processor...");
    await changeFeedProcessor.StartAsync();
    Console.WriteLine("Change Feed Processor started.");
    
    return changeFeedProcessor;
}
```

In this sample:

* Configuration values define the database, source container, and lease container names.
* The change feed processor is constructed using the `GetChangeFeedProcessorBuilder` method. The delegate `HandleChangesAsync` is provided to process the incoming changes.
* The processor starts asynchronously, continuously monitoring and handling changes without requiring manual polling.

> **lightbulb** This sample demonstrates how to leverage Azure Cosmos DB’s change feed functionality to create efficient, real-time data processing systems. The underlying infrastructure manages scaling and consistency, allowing you to focus on processing the data.

This guide has covered the foundational concepts and provided a practical example of implementing a change feed processor in Azure Cosmos DB. For further reading and best practices in managing cloud-based data workflows, explore additional resources such as [Azure Cosmos DB Documentation](https://docs.microsoft.com/azure/cosmos-db/).

- [Watch Video](https://learn.kodekloud.com/user/courses/az-204-developing-solutions-for-microsoft-azure/module/9b20db07-78f4-4774-8a8c-8c2c182ebd0e/lesson/76179776-b51b-4260-8d55-2cbe8b471f30)
