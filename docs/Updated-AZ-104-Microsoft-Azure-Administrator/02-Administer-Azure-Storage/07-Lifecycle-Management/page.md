# Save Credential Information
cmd.exe /c "cmdkey /add:demooza0735533.file.core.windows.net /user:Azure\demooza0735533 /pass:YourPasswordHere"

# Mount the File Share
New-PSDrive -Name Z -PSProvider FileSystem -Root "\\demooza0735533.file.core.windows.net\files-01" -Persist
```

Once executed, you should observe the "demo" file or folder you created reflected in the Azure Portal.

## Securing Your Storage Account

Currently, the file share is accessible over the public internet. If you require enhanced security, Azure provides several options to restrict access. Consider using Azure P2S VPN or ExpressRoute to tunnel SMB traffic through an alternative port.

> **lightbulb** For improved security and compliance, always review and configure your storage account's network settings according to your organization's best practices.

This guide has demonstrated how to create an Azure File Share, mount it on your computer, and troubleshoot connectivity issues. Enjoy exploring the robust capabilities of Azure File Share and streamline your file storage solutions in the cloud!

- [Watch Video](https://learn.kodekloud.com/user/courses/az-104-microsoft-azure-administrator/module/48d08f66-feb9-4bae-83b0-2e6aa34e24ae/lesson/b5a6ca91-86a6-46bd-8e03-f0b6ec3ccac4)


# Lifecycle Management

Source: https://notes.kodekloud.com/docs/Updated-AZ-104-Microsoft-Azure-Administrator/Administer-Azure-Storage/Lifecycle-Management/page

Lifecycle management in Azure Storage optimizes costs by automatically transitioning data between access tiers based on usage patterns, reducing storage expenses without manual intervention.

Lifecycle management in Azure Storage optimizes costs by automatically transitioning data between different access tiers—such as hot, cool, cold, and archive—based on usage patterns. When data remains unmodified for a defined period, policies automatically move blobs between tiers, reducing storage expenses without manual intervention.

This capability is available for Blob Storage and General Purpose v2 storage accounts only. If you're still using a General Purpose v1 storage account, you'll need to upgrade to General Purpose v2 to take advantage of lifecycle management.

Lifecycle management is based on policy-driven transitions. You can configure policies to:

* Automatically move blobs to cooler tiers based on their last modified date.
* Delete blobs and snapshots that haven’t been modified after a specified number of days.
* Filter policies to target specific file types (e.g., PDF or MP4 files).

Additionally, these policies support multiple blob types. Rules can be applied to Block Blobs, Append Blobs, and even target specific subtypes such as blob versions and snapshots.

Below is an example of a JSON lifecycle policy definition. In this example:

* Blobs not modified for 60 days are moved to the cool tier.
* Blobs not modified for 180 days are moved to the archive tier.
* Blobs not modified for 365 days are deleted.

```json theme={null}
{
  "rules": [
    {
      "enabled": true,
      "name": "rule",
      "type": "Lifecycle",
      "definition": {
        "actions": {
          "baseBlob": {
            "tierToCool": {
              "daysAfterModificationGreaterThan": 60
            },
            "tierToArchive": {
              "daysAfterModificationGreaterThan": 180
            },
            "delete": {
              "daysAfterModificationGreaterThan": 365
            }
          }
        }
      },
      "filters": {
        "blobTypes": [
          "blockBlob"
        ]
      }
    }
  ]
}
```

The policy above illustrates how a blob transitions to the cool tier after 60 days, to the archive tier after 180 days, and is ultimately deleted after 365 days.

> **lightbulb** You do not need to write this JSON manually. The Azure portal offers a graphical interface to create these rules without any coding. Simply navigate to your storage account, select the Lifecycle Management option, and use the list view to add and configure your rule.

Returning to your storage account, select the Lifecycle Management option. Click "Add Rule" and enter a name (for example, "Policy 1"). Then you can set up filters to limit the policy to specific blob types—such as append blobs or block blobs—and even include snapshots and versions.

![The image shows a Microsoft Azure portal interface for adding a rule in lifecycle management. It includes options for rule name, rule scope, and blob type selections.](https://kodekloud.com/kk-media/image/upload/v1752884380/notes-assets/images/Updated-AZ-104-Microsoft-Azure-Administrator-Lifecycle-Management/azure-portal-lifecycle-management-rule.jpg)

After naming the rule, click "Next" to define the policy conditions. For example:

* If a blob was last modified more than 60 days ago, move it to the cool tier.
* If it was last modified 90 days ago, move it to cold storage.
* If modified over 180 days ago, move it to the archive tier, while skipping blobs that have been rehydrated in the last seven days.
* Finally, delete the blob after 365 days.

Each condition can be added using the "Add" button. Once you have finalized these settings, the policy will be created, and you can review its JSON representation directly within the portal.

![The image shows a Microsoft Azure interface for adding a rule in lifecycle management, where users can set conditions to move blobs to cooler storage or delete them based on their last modified or created date.](https://kodekloud.com/kk-media/image/upload/v1752884381/notes-assets/images/Updated-AZ-104-Microsoft-Azure-Administrator-Lifecycle-Management/azure-lifecycle-management-rule-interface.jpg)

Below is another example JSON policy that demonstrates executing multiple actions within a single rule. In this scenario, besides the cool and archive transitions, there is also a transition to the cold tier:

```json theme={null}
{
  "rules": [
    {
      "enabled": true,
      "name": "policy-1",
      "type": "lifecycle",
      "definition": {
        "actions": {
          "baseBlob": {
            "tierToCold": {
              "daysAfterModificationGreaterThan": 90
            },
            "tierToCool": {
              "daysAfterModificationGreaterThan": 60
            },
            "tierToArchive": {
              "daysAfterLastTierChangeGreaterThan": 7,
              "daysAfterModificationGreaterThan": 180
            },
            "delete": {
              "daysAfterModificationGreaterThan": 365
            }
          }
        },
        "filters": {
          "blobTypes": [
            "blockBlob"
          ]
        }
      }
    }
  ]
}
```

After you create the policy, you have the flexibility to enable or disable it as needed from the portal.

![The image shows the Microsoft Azure portal, specifically the "Lifecycle management" section of a storage account, with a policy named "policy-1" that is enabled for block blob type.](https://kodekloud.com/kk-media/image/upload/v1752884382/notes-assets/images/Updated-AZ-104-Microsoft-Azure-Administrator-Lifecycle-Management/azure-portal-lifecycle-management-policy1.jpg)

## Azure File Share Lifecycle Management

Now, let's focus on how lifecycle management applies to Azure File Share. (Content regarding Azure File Share lifecycle management continues here.)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-104-microsoft-azure-administrator/module/48d08f66-feb9-4bae-83b0-2e6aa34e24ae/lesson/7dddf5a5-609c-47a0-aea2-276dc2af440b)
