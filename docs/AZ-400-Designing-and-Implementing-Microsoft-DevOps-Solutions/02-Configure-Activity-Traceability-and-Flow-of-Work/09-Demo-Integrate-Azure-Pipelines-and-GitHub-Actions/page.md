# azure-pipelines.yml (Starter)
trigger:
  - master

pool:
  vmImage: 'windows-latest'

steps:
  - script: echo Hello, world!
    displayName: 'Run a one-line script'
```

Replace the sample scripts with .NET build and test steps:

```yaml theme={null}
# azure-pipelines.yml (Build + Test)
trigger:
  - master

pool:
  vmImage: 'windows-latest'

steps:
  - task: UseDotNet@2
    inputs:
      packageType: 'sdk'
      version: '1.0.x'
      installationPath: '$(Agent.ToolsDirectory)/dotnet'

  - script: dotnet --version
    displayName: 'Check .NET Version'

  - script: dotnet restore
    displayName: 'Restore dependencies'

  - script: dotnet build --configuration Release --no-restore
    displayName: 'Build project'

  - script: dotnet test --no-build --verbosity normal
    displayName: 'Run tests'
```

Save and run the pipeline. After it succeeds, you’ll see a successful build run:

![The image shows an Azure DevOps pipeline interface with a successful job run for a project named "TestWeb." The pipeline was triggered by a user and completed in 16 seconds.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867373/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Generating-Release-Notes/azure-devops-pipeline-success-testweb.jpg)

***

## 3. Add the Generate Release Notes Task

Extend your YAML to generate and publish release notes in four steps:

```yaml theme={null}
# azure-pipelines.yml (Generate & Publish Release Notes)
trigger:
  - master

pool:
  vmImage: 'windows-latest'

steps:
  # Build and Test (from previous section)
  - task: UseDotNet@2
    inputs:
      packageType: 'sdk'
      version: '1.0.x'
      installationPath: '$(Agent.ToolsDirectory)/dotnet'
  - script: dotnet restore; dotnet build --configuration Release --no-restore; dotnet test --no-build
    displayName: 'Restore, Build, and Test'

  # 1. Generate release notes in repo root
  - task: XplatGenerateReleaseNotes@4
    inputs:
      outputFile: '$(Build.Repository.LocalPath)\releasenotes_$(Build.BuildId).md'
      templateLocation: 'Inline'
      inlineTemplate: |
        ## Build {{buildDetails.buildNumber}}
        **Branch:** {{buildDetails.sourceBranch}}
        **Author:** {{buildDetails.requestedFor.displayName}}
        **Commit:** {{buildDetails.sourceVersion}}
      dumpPayloadToConsole: false
      replaceFile: true

  # 2. Copy to wiki folder
  - task: CopyFiles@2
    displayName: 'Copy Release Notes to Wiki Folder'
    inputs:
      SourceFolder: '$(Build.Repository.LocalPath)'
      Contents: 'releasenotes_$(Build.BuildId).md'
      TargetFolder: '$(Build.Repository.LocalPath)/wiki'
      CleanTargetFolder: true
      OverWrite: true

  # 3. Clean up temporary file
  - script: del "$(Build.Repository.LocalPath)\releasenotes_$(Build.BuildId).md"
    displayName: 'Delete Temporary Release Notes File'

  # 4. Commit back to wiki (skip CI)
  - task: CmdLine@2
    displayName: 'Commit Release Notes to Wiki'
    inputs:
      script: |
        git checkout master
        git pull
        git config --global user.email "you@example.com"
        git config --global user.name "Your Name"
        git add wiki/releasenotes_$(Build.BuildId).md
        git commit -m "[skip ci] Update release notes for build $(Build.BuildId)"
        git push origin HEAD:master
```

Run the updated pipeline and inspect the release-notes generation logs:

![The image shows an Azure DevOps pipeline interface with a list of jobs and their statuses on the left, and detailed log output of a task called "XplatGenerateReleaseNotes" on the right.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867374/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Generating-Release-Notes/azure-devops-pipeline-jobs-logs.jpg)

***

## 4. Edit and View in Visual Studio Code

For easier editing, clone the repo locally and open **azure-pipelines.yml** in VS Code. You’ll find all tasks, including the release-notes steps, in one file.

![The image shows a Visual Studio Code interface with a file explorer on the left, highlighting the "azure-pipelines.yml" file, and the file's content displayed on the right.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867375/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Generating-Release-Notes/visual-studio-code-file-explorer-azure-pipelines.jpg)

***

## 5. Review Logs and Verify the Wiki

After another run, confirm the copy step output:

![The image shows an Azure DevOps pipeline interface with a list of jobs and their statuses on the left, and detailed log output for a specific job, "XplatGenerateReleaseNotes," on the right.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867376/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Generating-Release-Notes/azure-devops-pipeline-jobs-logs-2.jpg)

Cleaning target folder: C:\agent\_work\7\s\wiki
Copying C:\agent\_work\7\releasenotes\_1216.md to C:\agent\_work\7\s\wiki\releasenotes\_1216.md

Finally, navigate to your Azure DevOps Wiki—each build now publishes a new `releasenotes_<BuildId>.md` page:

![The image shows a README file in an Azure DevOps Wiki, detailing a .NET Web API application called TestWeb, with sections on description, installation, usage, contributing, and licensing.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867369/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Generating-Release-Notes/azure-devops-wiki-readme-testweb.jpg)

> **lightbulb** This template shows build number, branch, author, and commit. Extend the Handlebars template to include work items, pull requests, changelogs, or custom fields from Azure Boards.

***

With this setup, every commit to `master` triggers a pipeline that generates and publishes release notes to your Azure DevOps Wiki—fully automated, CI-safe, and effortless to maintain.

## Links and References

* [Generate Release Notes Extension (MarketPlace)](https://marketplace.visualstudio.com/items?itemName=richardfennellBM.BM-VSTS-GenerateReleaseNotes)
* [Azure Pipelines YAML Reference](https://docs.microsoft.com/azure/devops/pipelines/yaml-schema)
* [Azure DevOps Wiki Documentation](https://docs.microsoft.com/azure/devops/project/wiki/wiki-overview)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/503e97d4-be52-440b-8a4e-8610d1eca6ed/lesson/f3d0bf76-5e14-43d4-a4d0-abc85e00b331)


# Demo Integrate Azure Pipelines and GitHub Actions

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Configure-Activity-Traceability-and-Flow-of-Work/Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/page

This guide explains how to trigger an Azure Pipeline from a GitHub Action upon code pushes to the main branch.

In this guide, you’ll learn how to trigger an Azure Pipeline automatically from a GitHub Action whenever you push code to the `main` branch. By the end, you’ll have a seamless CI flow between GitHub and Azure DevOps.

***

## 1. Connect GitHub to Azure DevOps

1. In your Azure DevOps project (e.g., **SimpleWebAPI**), navigate to **Project Settings** → **GitHub Connections**.
2. Click **Connect Your GitHub Account** and authorize Azure DevOps to access your repos.
3. Select the **SimpleWebAPI** repository and hit **Save**, then approve the installation in GitHub.

![The image shows an Azure DevOps project dashboard for "SimpleWebAPI," displaying project details, statistics, and navigation options on the left sidebar.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867377/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/azure-devops-simplewebapi-dashboard.jpg)

![The image shows a webpage for connecting GitHub with Azure Boards, featuring a sidebar with project settings and an illustration of a person watering a plant.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867379/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/github-azure-boards-connection-webpage.jpg)

![The image shows a GitHub permissions page for installing Azure Boards, with options to select repositories and permissions for accessing metadata, code, and external domains. There are buttons for approving or rejecting the installation.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867380/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/github-permissions-azure-boards-installation.jpg)

***

## 2. Generate a Personal Access Token (PAT)

You’ll need a PAT with permissions to queue builds. In Azure DevOps:

1. Click your user icon → **Personal Access Tokens** → **New Token**.
2. Give it a name, expiration date, and select scopes:
   * **Build (read & execute)**
   * **Token administration (read & manage)**
3. Create the token and copy it immediately.

> **triangle-alert** You will **only** see the PAT value once. Store it securely in your password manager.

![The image shows a screenshot of the Azure DevOps user settings page, specifically the "Personal Access Tokens" section, listing various tokens with their status and expiration dates.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867381/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/azure-devops-personal-access-tokens-screenshot.jpg)

***

## 3. Create an Azure Pipeline

1. In **SimpleWebAPI**, select **Pipelines** → **Create Pipeline**.
2. Choose **GitHub** and pick **SimpleWebAPI**. Approve the Azure Pipelines app if prompted.
3. Opt for **Starter Pipeline** to get a minimal YAML template.

![The image shows an Azure DevOps dashboard with a list of projects, including "SimpleWebAPI," "Customer Portal," "Test Project," and "jeremy." The interface includes options for creating a new project and filtering existing ones.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867382/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/azure-devops-dashboard-projects-list.jpg)

![The image shows an Azure DevOps interface for creating a new pipeline, asking "Where is your code?" with options for Azure Repos Git, Bitbucket Cloud, GitHub, and GitHub Enterprise Server. The left sidebar includes navigation options like Overview, Boards, Repos, and Pipelines.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867383/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/azure-devops-new-pipeline-interface.jpg)

![The image shows an Azure DevOps interface for creating a new pipeline, with a section to select a repository. The left sidebar includes options like Overview, Boards, Repos, and Pipelines.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867384/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/azure-devops-new-pipeline-interface-2.jpg)

![The image shows an Azure DevOps interface for configuring a new pipeline, with options for different project types like ASP.NET, .NET Core, and Xamarin.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867385/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/azure-devops-new-pipeline-configuration.jpg)

```yaml theme={null}
