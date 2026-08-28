# Implement a deployment that includes database tasks

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-Deployments/Implement-a-deployment-that-includes-database-tasks/page

Learn to design and execute Azure deployments that include critical database operations for data integrity and minimized downtime.

In this guide, you’ll learn how to design and execute Azure deployments that include critical database operations. Handling schema changes, data migrations, performance tuning, and backups as part of your CI/CD pipeline ensures data integrity, minimizes downtime, and keeps your application and database versions in sync.

## Why Database Tasks Matter in Deployments

Database updates often accompany application code changes—whether modifying table structures, migrating existing data, or tuning performance. Properly sequencing and automating these tasks in your pipeline reduces risk and ensures smooth rollouts.

<Frame>
  ![The image is an introduction slide about deployments involving database tasks, featuring a person with a laptop standing next to a server rack and a cloud icon. A text box explains the importance of database tasks in application deployments.](https://kodekloud.com/kk-media/image/upload/v1752867633/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Implement-a-deployment-that-includes-database-tasks/database-tasks-deployments-introduction-slide.jpg)
</Frame>

## Balancing Safety and Speed

DevOps strives for fast, reliable releases. When database changes are involved, you must prevent data loss or corruption while keeping downtime to a minimum. Automate every step—from generating migration scripts to running post-deployment checks—to strike the right balance.

<Frame>
  ![The image illustrates a DevOps cycle involving database tasks, emphasizing safe updates and efficient processes.](https://kodekloud.com/kk-media/image/upload/v1752867634/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Implement-a-deployment-that-includes-database-tasks/devops-cycle-database-tasks-updates.jpg)
</Frame>

## Four Key Database Task Types

Plan your deployment by categorizing database work into these four areas:

1. **Schema Updates**\
   Add or modify tables, columns, indexes, and constraints.
2. **Data Migration**\
   Move or transform existing data to fit the new schema.
3. **Performance Tuning**\
   Optimize indexes, queries, or database configurations.
4. **Backup and Restoration**\
   Create and validate backups; prepare rollback procedures.

<Frame>
  ![The image outlines four types of database tasks in Azure deployments: Schema Updates, Data Migration, Performance Tuning, and Backup and Restoration Processes, each with a brief description.](https://kodekloud.com/kk-media/image/upload/v1752867636/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Implement-a-deployment-that-includes-database-tasks/azure-database-tasks-schema-migration.jpg)
</Frame>

## Azure Tools for Database Deployments

Use these Azure-native tools to streamline database operations:

| Tool                         | Purpose                                                                | Documentation                      |
| ---------------------------- | ---------------------------------------------------------------------- | ---------------------------------- |
| Azure DevOps                 | CI/CD pipelines that build, test, and deploy code and database changes | [Azure DevOps][azure-devops]       |
| SQL Server Data Tools (SSDT) | Define and version database schemas; produce DACPACs                   | [SQL Server Data Tools][ssdt]      |
| Azure Data Studio            | Lightweight SQL editor and management UI                               | [Azure Data Studio][ads]           |
| Entity Framework Migrations  | Code-based migrations for .NET projects                                | [Entity Framework Migrations][efm] |

<Frame>
  ![The image is a diagram showing tools for database deployment in Azure, featuring Azure DevOps, SQL Server Data Tools (SSDT), Azure Data Studio, and Entity Framework migrations.](https://kodekloud.com/kk-media/image/upload/v1752867638/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Implement-a-deployment-that-includes-database-tasks/azure-database-deployment-tools-diagram.jpg)
</Frame>

## Real-World Example: SSDT + Azure DevOps

Follow this workflow to add a new table and index to an Azure SQL Database using SSDT and Azure Pipelines:

1. **Create or Update SSDT Project**\
   In Visual Studio, define schema changes (new table, index).
2. **Commit to Version Control**\
   Push your SSDT project to Azure Repos (Git).
3. **Configure the CI/CD Pipeline**\
   Build the solution, generate the DACPAC, and deploy it.
4. **Validate Post-Deployment**\
   Run automated tests or manual queries to confirm success.

<Frame>
  ![The image is a flowchart illustrating the steps for implementing a database deployment, including setting up a database project, checking in changes to Azure DevOps, configuring the CI/CD pipeline, and executing the deployment.](https://kodekloud.com/kk-media/image/upload/v1752867640/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Implement-a-deployment-that-includes-database-tasks/database-deployment-flowchart-steps.jpg)
</Frame>

### Sample Azure Pipelines YAML

```yaml theme={null}
trigger:
- main

pool:
  vmImage: 'windows-latest'

variables:
  solution: '**/*.sln'
  buildConfiguration: 'Release'
  dacpacPath: '$(Build.ArtifactStagingDirectory)/db/MyDatabase.dacpac'

steps:
- task: NuGetToolInstaller@1
  inputs:
    versionSpec: '5.x'

- task: NuGetCommand@2
  inputs:
    restoreSolution: '$(solution)'

- task: VSBuild@1
  inputs:
    solution: '$(solution)'
    configuration: '$(buildConfiguration)'

- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: '$(Build.ArtifactStagingDirectory)'
    artifactName: 'db'

- task: SqlAzureDacpacDeployment@1
  inputs:
    azureSubscription: '$(AzureServiceConnection)'
    AuthenticationType: 'servicePrincipal'
    serverName: '$(SqlServerName).database.windows.net'
    databaseName: '$(DatabaseName)'
    deployType: 'DacpacTask'
    DeploymentAction: 'Publish'
    DacpacFile: '$(dacpacPath)'
    SqlUsername: '$(SqlUser)'
    SqlPassword: '$(SqlPassword)'
```

<Callout icon="lightbulb">
  Store sensitive values like `SqlPassword` and service connections in Azure Key Vault or secure pipeline variables.
</Callout>

## Best Practices for Reliable Deployments

* **Automate Everything**\
  Combine application and database steps in a single pipeline to prevent version drift.
* **Use Representative Environments**\
  Test changes in staging instances that mirror production.
* **Validate and Monitor**\
  Run integration tests post-deployment and monitor performance metrics.
* **Have a Rollback Plan**\
  Keep backups or leverage DACPAC drift detection to revert if needed.

<Callout icon="triangle-alert">
  Never apply untested schema changes directly to production. Always verify deployments in a safe environment first.
</Callout>

***

## Links and References

* [Azure DevOps][azure-devops]
* [SQL Server Data Tools (SSDT)][ssdt]
* [Azure Data Studio][ads]
* [Entity Framework Migrations][efm]

[azure-devops]: https://docs.microsoft.com/azure/devops

[ssdt]: https://docs.microsoft.com/sql/ssdt

[ads]: https://docs.microsoft.com/sql/azure-data-studio

[efm]: https://docs.microsoft.com/ef/core/managing-schemas/migrations

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/07c0911f-05cf-4ab9-a7cd-b6a2f1f44f5c/lesson/2ae2db0f-0494-4f5a-a669-ba307f2105c1" />
</CardGroup>
