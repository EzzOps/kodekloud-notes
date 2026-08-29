# Discovering Package Management Tools

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-a-Package-Management-Strategy/Discovering-Package-Management-Tools/page

This article explores package management tools in Azure DevOps and GitHub, highlighting their importance in software development and CI/CD pipelines.

Design and Implementation of a Package Management Strategy

## Introduction

In this lesson, we explore package management in **Azure DevOps** and **GitHub**—critical components of modern software development and CI/CD pipelines. We’ll start by defining package management, then highlight why it matters. Finally, we’ll dive into four main tools:

* Azure Artifacts
* GitHub Packages
* NuGet
* npm

![The image is an introduction slide for "Package Management in Azure DevOps and GitHub," highlighting three sections: definition of package management, its importance in software development and CI/CD, and an overview of tools like Azure Artifacts and GitHub Packages.](https://kodekloud.com/kk-media/image/upload/v1752867904/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Discovering-Package-Management-Tools/package-management-azure-devops-github.jpg)

## Key Package Management Tools at a Glance

| Tool            | Platform     | Supported Packages                         | Highlights                                      |
| --------------- | ------------ | ------------------------------------------ | ----------------------------------------------- |
| Azure Artifacts | Azure DevOps | NuGet, npm, Maven, Python, universal feeds | Upstream sources, seamless CI/CD integration    |
| GitHub Packages | GitHub       | npm, NuGet, Maven, RubyGems, Docker images | Native auth, GitHub Actions workflows           |
| NuGet           | .NET         | .NET libraries and tools                   | Visual Studio & `dotnet` CLI integration        |
| npm             | Node.js      | JavaScript modules                         | Vast registry, script support, dependency audit |

> **lightbulb** Consistent versioning, faster builds, and secure dependency control are essential for scalable CI/CD. A unified registry reduces “works on my machine” issues and simplifies audits.

***

## Azure Artifacts

Azure Artifacts is a universal package management solution built into Azure DevOps. It allows teams to:

* Store and version packages in one central location
* Proxy public registries using **upstream sources**
* Integrate directly with Azure Pipelines for seamless CI/CD

```yaml theme={null}
