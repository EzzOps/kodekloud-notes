# Managing Container Properties and Metadata

Source: https://notes.kodekloud.com/docs/AZ-204-Developing-Solutions-for-Microsoft-Azure/Working-With-Azure-Blob-Storage/Managing-Container-Properties-and-Metadata/page

Managing container properties and metadata in Azure Blob Storage for better data organization and security using .NET SDK and PowerShell with REST APIs.

Managing container properties and metadata in Azure Blob Storage is a crucial task for organizing data and controlling access. In this guide, you'll learn how to manage both system properties and user-defined metadata using the .NET SDK and PowerShell with REST APIs. This capability allows you to store important information alongside your containers, facilitating better data organization and enhanced security.

## Using the .NET SDK to Set Metadata and Retrieve Container Properties

In this example, we set custom metadata on a blob container using the `SetMetadataAsync` method, which accepts a dictionary of key-value pairs. After setting the metadata, the container's properties are retrieved to verify important details such as the last modified date and public access level.

```csharp theme={null}
using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;
using System;
using System.Threading.Tasks;

public class BlobContainerExample
{
    public static async Task SetMetadataAndGetPropertiesAsync(BlobContainerClient containerClient)
    {
        // Set metadata
        await containerClient.SetMetadataAsync(new Dictionary<string, string>
        {
            { "owner", "admin" },
            { "environment", "production" }
        });

        // Get properties
        BlobContainerProperties properties = await containerClient.GetPropertiesAsync();
        Console.WriteLine($"Container: {containerClient.Name}, Last Modified: {properties.LastModified}, Access: {properties.PublicAccess}");
    }
}
```

In the code above, the metadata keys "owner" and "environment" are set to "admin" and "production" respectively. Retrieving the container properties confirms that these updates have been successfully applied.

## Managing Metadata with PowerShell

For those who prefer using PowerShell, similar results can be achieved by leveraging REST APIs. Metadata is passed through HTTP headers using the format `x-ms-meta-<name>: <value>`. For instance, to set metadata with the key "owner" and value "admin", you would use the header `x-ms-meta-owner: admin`.

The following PowerShell script demonstrates how to set metadata via a PUT request and retrieve container properties using a GET request:

```powershell theme={null}
$accountName = "yourstorageaccount"
$containerName = "yourcontainer"
$accountKey = "youraccountkey"
$baseUri = "https://$accountName.blob.core.windows.net/$containerName"
