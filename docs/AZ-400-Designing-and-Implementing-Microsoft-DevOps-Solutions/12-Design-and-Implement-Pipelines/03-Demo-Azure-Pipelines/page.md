# Demo Azure Pipelines

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-Pipelines/Demo-Azure-Pipelines/page

This tutorial builds a CI/CD workflow for a Blazor WebAssembly app using Azure Pipelines and deploys it to Azure Static Web Apps.

In this tutorial, we’ll build a complete CI/CD workflow for a Blazor WebAssembly app using **Azure Pipelines** and deploy it to **Azure Static Web Apps**. By the end, code changes pushed to Git will automatically build, test, and publish your site.

## 1. Create an Azure DevOps Project

1. Sign in to [Azure DevOps](https://dev.azure.com/).
2. Click **New project**, name it **KodeKloudBlog**, and create.

<Frame>
  ![The image shows an Azure DevOps interface with a "Create new project" dialog open, where a user is entering details for a new project named "KodeKloudBlog."](../../../../images/kodekloud.com/kk-media/image/upload/v1752867801/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Azure-Pipelines/azure-devops-create-new-project-kodekloudblog.jpg)
</Frame>

## 2. Initialize the Repository

1. In your new project, go to **Repos** and create a Git repository.

2. Clone it locally:

   ```bash theme={null}
   git clone https://jeremymorgankodekloud@dev.azure.com/jeremymorgankodekloud/KodeKloudBlog/_git/KodeKloudBlog
   cd KodeKloudBlog
   ```

3. Copy your Blazor WebAssembly app into this folder.

4. Commit and push:

   ```bash theme={null}
   git add .
   git commit -m "Initial commit"
   git push -u origin master
   ```

<Frame>
  ![The image shows a screenshot of an Azure DevOps project dashboard named "KodeKloudBlog," featuring options for Boards, Repos, Pipelines, Test Plans, and Artifacts. It includes a welcome message and a section for project stats, which are currently unavailable.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867804/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Azure-Pipelines/azure-devops-kodekloudblog-dashboard-screenshot.jpg)
</Frame>

Now your code is versioned:

<Frame>
  ![The image shows an Azure DevOps interface for a repository, listing files and folders for the "KodeKloudBlog" project with last change timestamps and commit details.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867806/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Azure-Pipelines/azure-devops-kodekloudblog-repo-interface.jpg)
</Frame>

## 3. Create the Build Pipeline

### 3.1 Scaffold the Pipeline

1. Navigate to **Pipelines** > **Create Pipeline**.

<Frame>
  ![The image shows an Azure DevOps interface prompting the user to create their first pipeline, with a sidebar menu on the left and a "Create Pipeline" button in the center.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867807/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Azure-Pipelines/azure-devops-create-pipeline-interface.jpg)
</Frame>

2. Select **Azure Repos Git** as the source.

<Frame>
  ![The image shows an Azure DevOps interface for creating a new pipeline, asking "Where is your code?" with options like Azure Repos Git, Bitbucket Cloud, GitHub, and GitHub Enterprise Server.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867807/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Azure-Pipelines/azure-devops-new-pipeline-interface.jpg)
</Frame>

3. Choose the **ASP.NET Core** template and review the YAML:

   ```yaml theme={null}
   # azure-pipelines.yml
   trigger:
     branches:
       include:
         - master

   pool:
     vmImage: 'windows-latest'

   variables:
     solution: '**/*.sln'
     buildPlatform: 'Any CPU'
     buildConfiguration: 'Release'

   steps:
     - task: NuGetToolInstaller@1
       displayName: 'Install NuGet'

     - task: NuGetCommand@2
       inputs:
         restoreSolution: '$(solution)'

     - task: VSBuild@1
       inputs:
         solution: '$(solution)'
         msbuildArgs: '/p:DeployOnBuild=true /p:WebPublishMethod=Package /p:PackageAsSingleFile=true /p:SkipInvalidConfigurations=true'
         configuration: '$(buildConfiguration)'

     - task: VSTest@2
       inputs:
         platform: '$(buildPlatform)'
         configuration: '$(buildConfiguration)'
   ```

### 3.2 YAML Variables

| Variable           | Description                           |
| ------------------ | ------------------------------------- |
| solution           | Path to your `.sln` file (`**/*.sln`) |
| buildPlatform      | Target platform (`Any CPU`)           |
| buildConfiguration | Build mode (`Release`)                |

<Callout icon="lightbulb">
  Ensure your project has access to either Microsoft-hosted agents or self-hosted agents. Check **Project settings** > **Agent pools** to verify availability.
</Callout>

### 3.3 Run and Inspect

* Save and run the pipeline.
* If prompted to grant permissions for the agent pool, approve to continue.

<Frame>
  ![The image shows an Azure DevOps pipeline interface with a pop-up asking for permission to access a resource, specifically to permit the use of an agent pool for the pipeline.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867808/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Azure-Pipelines/azure-devops-pipeline-permission-popup.jpg)
</Frame>

* After completion, click the build to see each step’s logs:

<Frame>
  ![The image shows an Azure DevOps pipeline interface with a completed job run, displaying the steps and their statuses on the left and job details on the right.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867809/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Azure-Pipelines/azure-devops-pipeline-job-run-interface.jpg)
</Frame>

Review your agent pool:

<Frame>
  ![The image shows a web interface for Azure DevOps, specifically the "Agent pools" settings page, displaying two agents with their status, last run time, and version information.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867810/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Azure-Pipelines/azure-devops-agent-pools-settings.jpg)
</Frame>

## 4. Deploy to Azure Static Web Apps

1. In the [Azure portal](https://portal.azure.com/), search **Static Web Apps** > **Create**.
2. Configure subscription, resource group, and name (e.g., **KodeKloudBlog**).
3. Choose **Free** plan.
4. Under **Deployment Details**, select **Azure DevOps**, then your organization, project, repo, and branch.

<Frame>
  ![The image shows a Microsoft Azure portal page for creating a Static Web App, with fields for subscription, resource group, app details, hosting plan, and deployment details.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867811/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Azure-Pipelines/azure-portal-static-web-app-creation.jpg)
</Frame>

On **Advanced**, pick region and API settings if needed:

<Frame>
  ![The image shows a Microsoft Azure portal page for creating a Static Web App, specifically on the "Advanced" tab, where users can select the region for Azure Functions API and staging environments. There are options for distributed functions and a note about hosting plans.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867812/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Azure-Pipelines/azure-portal-static-web-app-advanced.jpg)
</Frame>

Review and **Create**:

<Frame>
  ![The image shows a Microsoft Azure portal page for creating a static web app, displaying details such as subscription, resource group, name, region, and repository information. There is a "Create" button at the bottom for finalizing the setup.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867813/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Azure-Pipelines/azure-portal-static-web-app-setup.jpg)
</Frame>

Once provisioned, you’ll see this confirmation:

<Frame>
  ![The image shows a Microsoft Azure congratulatory message for a new site, with recommended next steps including learning about Azure Static Web Apps, creating a static web app from VS Code, and installing the Static Web Apps CLI.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867815/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Azure-Pipelines/azure-congratulatory-message-static-web-apps.jpg)
</Frame>

Azure DevOps automatically creates a second pipeline for the Static Web App.

## 5. Adjust the Static Web App Pipeline

Edit the generated YAML to ensure the right VM image and paths:

```yaml theme={null}
