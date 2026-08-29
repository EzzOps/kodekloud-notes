# azure-pipelines.yml
# Starter pipeline: build and deploy your code.
trigger:
  - main

pool:
  vmImage: ubuntu-latest

steps:
  - script: echo Hello, world!
    displayName: 'Run a one-line script'

  - script: |
      echo Add other tasks to build, test, and deploy your project.
      echo See https://aka.ms/yaml
    displayName: 'Run a multi-line script'
```

For more customization, see the [Azure Pipelines YAML schema](https://docs.microsoft.com/azure/devops/pipelines/yaml-schema).

***

## 4. Configure an Agent Pool

If you use self-hosted agents:

1. Go to **Project Settings** → **Agent pools** and note your pool name (e.g., `KodeKloudCustomer`).
2. Update the `pool` block in your YAML:

```yaml theme={null}
# azure-pipelines.yml
trigger:
  - main

pool:
  name: 'KodeKloudCustomer'

steps:
  - script: echo Hello, world!
    displayName: 'Run a one-line script'
    
  - script: |
      echo Add other tasks to build, test, and deploy your project.
      echo See https://aka.ms/yaml
    displayName: 'Run a multi-line script'
```

> **lightbulb** When targeting a self-hosted pool, remove the `vmImage` setting. Jobs run on your specified agents.

![The image shows a screenshot of the Azure DevOps interface, specifically the "Agent pools" section under "Project Settings," displaying details of an agent named "KodeKloudAgent1" which is online and idle.](https://kodekloud.com/kk-media/image/upload/v1752867386/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/azure-devops-agent-pools-kodekloudagent1.jpg)

Save and queue your pipeline. You should see a successful run:

![The image shows an Azure DevOps pipeline interface with a build summary for a project called "SimpleWebAPI." It displays details such as the trigger, repository, branch, and job status.](https://kodekloud.com/kk-media/image/upload/v1752867387/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/azure-devops-pipeline-simplewebapi-summary.jpg)

***

## 5. Set Up the GitHub Action

1. In your **SimpleWebAPI** GitHub repo, go to **Actions** → **Set up a workflow yourself**.
2. This creates a blank file at `.github/workflows/main.yml`. Replace its contents with:

```yaml theme={null}
# .github/workflows/trigger-azure-pipeline.yml
name: Trigger Azure Pipeline

on:
  push:
    branches:
      - main

jobs:
  trigger-pipeline:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Azure DevOps Pipeline
        uses: azure/pipelines@v1
        with:
          azure-devops-project-url: ${{ secrets.AZURE_DEVOPS_PROJECT_URL }}
          azure-pipeline-name: 'jeremykodekloud.SimpleWebAPI'
          azure-devops-token: ${{ secrets.AZURE_DEVOPS_TOKEN }}
```

![The image shows a GitHub Actions setup page for a repository, suggesting workflows for building and deploying applications, such as a .NET Desktop app.](https://kodekloud.com/kk-media/image/upload/v1752867388/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/github-actions-setup-workflows-dotnet.jpg)

![The image shows a GitHub interface where a user is editing a YAML file for a workflow in a repository. The right side displays a marketplace with featured actions like setting up Node.js and Java JDK environments.](https://kodekloud.com/kk-media/image/upload/v1752867389/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/github-yaml-workflow-editing-marketplace.jpg)

***

## 6. Configure Repository Secrets

In GitHub, go to **Settings** → **Secrets and variables** → **Actions** and add:

| Secret Name                 | Value Example                               |
| --------------------------- | ------------------------------------------- |
| AZURE\_DEVOPS\_PROJECT\_URL | `https://dev.azure.com/yourOrg/yourProject` |
| AZURE\_DEVOPS\_TOKEN        | *(your Azure DevOps PAT)*                   |

![The image shows a GitHub repository settings page where a new secret is being added under "Actions secrets." The secret is named "AZURE\_DEVOPS\_PROJECT\_URL" with a URL provided in the secret field.](https://kodekloud.com/kk-media/image/upload/v1752867390/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/github-repo-settings-actions-secret.jpg)

![The image shows a GitHub repository settings page for managing "Actions secrets and variables," with options to add new repository secrets.](https://kodekloud.com/kk-media/image/upload/v1752867391/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/github-repo-settings-actions-secrets.jpg)

![The image shows a GitHub repository settings page, specifically the "Secrets and variables" section, with two repository secrets listed: "AZURE\_DEVOPS\_PROJECT\_URL" and "AZURE\_DEVOPS\_TOKEN".](https://kodekloud.com/kk-media/image/upload/v1752867392/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/github-repo-settings-secrets-variables.jpg)

Commit your workflow to `main`. The GitHub Action triggers immediately, and you should see a corresponding run in Azure Pipelines.

![The image shows an Azure DevOps pipeline run summary for a project named "SimpleWebAPI," indicating a successful job execution. The pipeline was triggered by a user and completed in 14 seconds.](https://kodekloud.com/kk-media/image/upload/v1752867393/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/azure-devops-simplewebapi-pipeline-summary.jpg)

![The image shows a GitHub Actions workflow summary with a successful build job and annotations indicating warnings about deprecated Node.js versions and commands.](https://kodekloud.com/kk-media/image/upload/v1752867393/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/github-actions-workflow-success-warnings.jpg)

![The image shows an Azure DevOps pipeline interface with a list of recent pipeline runs for a project named "SimpleWebAPI," all of which have successfully completed.](https://kodekloud.com/kk-media/image/upload/v1752867394/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Integrate-Azure-Pipelines-and-GitHub-Actions/azure-devops-pipeline-simplewebapi-successful.jpg)

***

## 7. Verify Continuous Integration

Every push to `main` now triggers:

```bash theme={null}
# Pull latest changes
git pull

# Make edits and commit
git add .
git commit -m "Fix typo in README"
git push
```

Watch the GitHub Action and Azure Pipeline execute in tandem—your CI process is fully automated!

***

## References

* [Azure DevOps Docs: Pipelines YAML](https://docs.microsoft.com/azure/devops/pipelines/yaml-schema)
* [GitHub Actions: Secrets](https://docs.github.com/actions/security-guides/encrypted-secrets)
* [Azure Pipelines GitHub Action](https://github.com/azure/pipelines)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/503e97d4-be52-440b-8a4e-8610d1eca6ed/lesson/bdbadfc9-4cdc-403e-89ea-8313e6ec094a)


# Demo Repository Integration with Azure Boards

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Configure-Activity-Traceability-and-Flow-of-Work/Demo-Repository-Integration-with-Azure-Boards/page

Learn to link commits and pull requests to Azure Boards work items for better tracking and visibility.

Learn how to link commits and pull requests directly to Azure Boards work items for seamless tracking and enhanced visibility.

## Prerequisites

* An existing Azure DevOps project with Azure Boards enabled
* A Git repository named **Customer Portal** in the same project
* Git CLI and an IDE (e.g., Visual Studio Code)

***

## Step 1: Identify the Work Item

Navigate to **Azure Boards** and locate the work item you need to address. For this demo, our target is:

* Work Item ID: **69**
* Title: *“Add a sentence to the README file.”*

![The image shows a screenshot of a work items list from Azure DevOps, displaying tasks with details such as ID, title, assigned person, state, and area path. The tasks are unassigned and marked as "To Do" under the "Customer Portal" area.](https://kodekloud.com/kk-media/image/upload/v1752867396/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Repository-Integration-with-Azure-Boards/azure-devops-work-items-to-do-list.jpg)

Make note of this ID—you’ll need it when linking your commit or pull request.

***

## Step 2: Apply the Code Change

1. Open the **Customer Portal** repo in your editor.
2. Edit `README.md` to add the required sentence.
3. Stage your change:

   ```bash theme={null}
   git add README.md
   ```

***

## Step 3: Commit with a Work Item Reference

When committing changes, include one of these keywords followed by the work item ID (`#69`):

* fixes
* resolves
* closes

```bash theme={null}
git commit -m "Add README sentence (fixes #69)"
git push origin main
```

> **lightbulb** You can also use the `AB#<ID>` format in commit messages or PR descriptions to link work items.\
  Example: `git commit -m "Update docs AB#69"`.

> **triangle-alert** Ensure your repository is connected to Azure Boards and that you have the correct permissions. Missing the `#` or using an unsupported keyword will prevent the link from forming.

***

## Step 4: Verify the Link in Azure Boards

Return to the work item in Azure Boards (ID 69). In the **Development** section, you should see the linked commit and any associated pull requests.

![The image shows an Azure DevOps interface displaying a repository named "Customer Portal" with files like azure-pipelines.yml and README.md. The README file contains sections for introduction, getting started, build and test, and contribute.](https://kodekloud.com/kk-media/image/upload/v1752867398/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Demo-Repository-Integration-with-Azure-Boards/azure-devops-customer-portal-repo.jpg)

***

## Quick Reference: Commit Keyword Table

| Keyword  | Effect                                  | Example        |
| -------- | --------------------------------------- | -------------- |
| fixes    | Closes work item when the commit merges | `fixes #69`    |
| resolves | Same as `fixes`                         | `resolves #69` |
| closes   | Alternative close keyword               | `closes #69`   |
| AB#      | Direct link without auto-close behavior | `AB#69`        |

***

## Best Practices

* Always reference work item IDs in both commit messages and pull request descriptions for clear traceability.
* Write concise, descriptive commit messages that reflect the scope of the change.
* Regularly review the **Development** section in Azure Boards to confirm that links are up to date.
* Encourage your team to follow this process to maintain project transparency.

***

## Links and References

* [Azure Boards Documentation](https://learn.microsoft.com/azure/devops/boards/)
* [Linking Work Items to Code](https://learn.microsoft.com/azure/devops/boards/add-work-items-to-code)
* [Git Commit Best Practices](https://www.atlassian.com/git/tutorials/saving-changes)
* [Azure DevOps Git Integration](https://learn.microsoft.com/azure/devops/repos/git/)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/503e97d4-be52-440b-8a4e-8610d1eca6ed/lesson/8757794f-e70a-41a4-bccb-a400ff4d3b2f)
