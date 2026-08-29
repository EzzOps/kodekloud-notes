# Example: Publish a NuGet package in Azure Pipelines
steps:
  - task: NuGetCommand@2
    inputs:
      command: 'push'
      packagesToPush: '**/*.nupkg'
      publishVstsFeed: 'your-feed-name'
```

<Callout icon="lightbulb">
  Use upstream sources to cache npm, Maven, or PyPI packages—reducing build times and improving reliability.
</Callout>

***

## GitHub Packages

GitHub Packages is GitHub’s integrated registry, working with **GitHub Actions** and repository permissions.

* **Authentication**: Uses your GitHub account credentials
* **Supported Formats**: npm, NuGet, Maven, RubyGems, Docker, and more
* **Access Control**: Repository-level permissions and fine-grained scopes

```yaml theme={null}
# Example: Publish npm package with GitHub Actions
name: Publish npm Package
on:
  push:
    tags:
      - 'v*.*.*'
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

***

## NuGet

NuGet is the de facto package manager for the .NET ecosystem, providing:

* Distribution of libraries and CLI tools
* Integration with **Visual Studio** and the `.NET CLI`
* Automatic dependency resolution and semantic versioning

```bash theme={null}
# Install a package
dotnet add package Newtonsoft.Json --version 13.0.1

# Restore dependencies
dotnet restore
```

***

## npm

npm is the largest registry for JavaScript and Node.js packages, featuring:

* Over a million modules and growing
* Simple commands: `npm install`, `npm update`
* Scripts, semantic versioning, and built-in security audits

<Frame>
  ![The image is an informational graphic about npm, highlighting it as the largest software registry and part of the JavaScript ecosystem. It features two sections: "What is npm?" and "Key Features."](../../../../images/kodekloud.com/kk-media/image/upload/v1752867905/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Discovering-Package-Management-Tools/npm-software-registry-infographic.jpg)
</Frame>

```bash theme={null}
# Install dependencies
npm install

# Run a project script
npm run build

# Audit for vulnerabilities
npm audit fix
```

<Callout icon="triangle-alert">
  Regularly run `npm audit` and review advisories. Use lockfiles (`package-lock.json`) to ensure reproducible builds.
</Callout>

***

## Further Reading

* [Azure Artifacts Documentation](https://docs.microsoft.com/azure/devops/artifacts/)
* [GitHub Packages](https://docs.github.com/packages)
* [NuGet Docs](https://docs.microsoft.com/nuget/)
* [npm Documentation](https://docs.npmjs.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/54c26a08-243e-448b-bba5-3fbefddf9145/lesson/48289a08-237e-4523-9209-3d192dc759c8" />
</CardGroup>


# Exploring Azure Artifacts

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-a-Package-Management-Strategy/Exploring-Azure-Artifacts/page

This article explores Azure Artifacts, focusing on package management within Azure DevOps for efficient CI/CD pipelines.

In this lesson, we dive into **Azure Artifacts**, a core component of Azure DevOps that enables enterprise-scale package management. Mastering Azure Artifacts is essential for the [AZ-400 exam](https://learn.microsoft.com/en-us/certifications/exams/az-400) and for streamlining your CI/CD pipelines with reliable, repeatable package deployments.

<Frame>
  ![The image is a slide titled "Introduction" with three bullet points: "Exploring Azure Artifacts," "Importance of package management in software development," and "Overview of Azure Artifacts as an extension of Azure DevOps."](../../../../images/kodekloud.com/kk-media/image/upload/v1752867907/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-Azure-Artifacts/introduction-azure-artifacts-package-management.jpg)
</Frame>

## Why Choose Azure Artifacts?

Azure Artifacts augments your DevOps workflow with:

| Benefit                        | Description                                                      |
| ------------------------------ | ---------------------------------------------------------------- |
| Tight Azure DevOps Integration | Automate package restore and publishing in Pipelines and Boards. |
| Multi-format Support           | Host and manage NuGet, npm, Maven, Python, and more.             |
| Fine-grained Access Control    | Assign permissions at feed and individual package levels.        |

<Callout icon="lightbulb">
  Azure Artifacts scales from small teams to large enterprises, offering performance and security.
</Callout>

## Package Management Workflow

Follow these three core steps to onboard packages:

1. **Set up a feed**
2. **Push your packages**
3. **Consume packages**

<Frame>
  ![The image outlines a three-step process for creating and sharing packages: setting up a feed, pushing packages to the feed, and consuming packages from the feed.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867908/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-Azure-Artifacts/three-step-package-creation-sharing-process.jpg)
</Frame>

***

## 1. Creating a Feed

In Azure DevOps:

1. Navigate to **Artifacts**.
2. Click **Create Feed**.

<Frame>
  ![The image shows a screenshot of the Azure DevOps interface, specifically the "Create new feed" configuration window, where users can set permissions and visibility for package feeds.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867909/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-Azure-Artifacts/azure-devops-create-new-feed-screenshot.jpg)
</Frame>

Configure these settings:

| Setting          | Options                                          | Description                                                          |
| ---------------- | ------------------------------------------------ | -------------------------------------------------------------------- |
| Visibility       | Private, Organization, Public                    | Controls who can view and install your packages.                     |
| Upstream Sources | NuGet.org, npmjs.com, Maven Central, other feeds | Automatically proxy or cache packages from external registries.      |
| Scope            | Entire organization or specific projects         | Limits feed access to select projects or makes it organization-wide. |

<Callout icon="triangle-alert">
  Public feeds expose your packages to the internet. Ensure no sensitive artifacts are published inadvertently.
</Callout>

***

## 2. Consuming a Feed

After feed creation, select **Connect to Feed** for authentication snippets, or **Search Stream Sources** to browse upstream packages:

<Frame>
  ![The image shows a screenshot of an Azure DevOps interface with options to connect to a feed or search upstream sources, under the title "Consuming the Feed."](../../../../images/kodekloud.com/kk-media/image/upload/v1752867910/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-Azure-Artifacts/azure-devops-consuming-feed-screenshot.jpg)
</Frame>

* **Connect to Feed**: Copy configuration for `NuGet.config`, `.npmrc`, `settings.xml`, or `pip.conf`.
* **Search Stream Sources**: Filter by package name, version, license, or dependencies.

***

## 3. CI/CD Integration

Use Azure Pipelines to restore, version, and publish packages automatically:

<Frame>
  ![The image illustrates integrating with CI/CD pipelines, highlighting automated package versioning, restoring packages during builds, and continuous integration with Azure Pipelines, alongside a screenshot of Azure DevOps.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867911/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-Azure-Artifacts/ci-cd-pipelines-azure-devops-integration.jpg)
</Frame>

### Pipeline Steps

```yaml theme={null}
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - '**/*.csproj'

steps:
- task: NuGetToolInstaller@1

- task: NuGetCommand@2
  inputs:
    command: 'restore'
    restoreSolution: '**/*.sln'
    feedsToUse: 'select'
    vstsFeed: '<YOUR_FEED_ID>'

- task: DotNetCoreCLI@2
  inputs:
    command: 'publish'
    projects: '**/*.csproj'
    arguments: '--configuration Release --output $(Build.ArtifactStagingDirectory)'

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)'
    ArtifactName: 'drop'
    publishLocation: 'Container'

- task: AzureWebApp@1
  inputs:
    azureSubscription: '<Your Azure Subscription>'
    appType: 'webApp'
    appName: '<Your App Name>'
    package: '$(Build.ArtifactStagingDirectory)/**/*.zip'
```

Automate version bumps using tools like [Dependabot](https://dependabot.com/) or GitHub’s native versioning bot.

***

## Best Practices

<Frame>
  ![The image outlines three best practices for using Azure Artifacts: using semantic versioning, organizing packages with scopes and views, and implementing retention policies for artifact management.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867912/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-Azure-Artifacts/azure-artifacts-best-practices-diagram.jpg)
</Frame>

* Adopt [semantic versioning](https://semver.org/) to signal breaking changes, features, and fixes.
* Leverage **scopes and views** to partition packages by team, environment, or lifecycle.
* Implement automated **retention policies** to purge stale artifacts and optimize storage costs.

***

## Links and References

* [Azure Artifacts Documentation](https://learn.microsoft.com/azure/devops/artifacts/)
* [Azure Pipelines Documentation](https://learn.microsoft.com/azure/devops/pipelines/)
* [Semantic Versioning Guide](https://semver.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/54c26a08-243e-448b-bba5-3fbefddf9145/lesson/91d566d8-52db-453a-946d-5dd211a505aa" />
</CardGroup>
