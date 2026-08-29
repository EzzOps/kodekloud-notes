# GitHub Packages

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Integration-with-GitHub-Actions/GitHub-Packages/page

GitHub Packages is a package hosting service that integrates with GitHub, supporting multiple ecosystems and streamlining workflows for package management.

Imagine your organization has multiple teams working on projects in Node.js, Ruby, .NET, Java—and running Docker containers. Each team uses GitHub Actions to build, package, and publish artifacts to external registries like [npm Registry](https://www.npmjs.com/), [RubyGems](https://rubygems.org/), [Maven](https://maven.apache.org/), [Docker Hub](https://hub.docker.com/), and [NuGet](https://www.nuget.org/). Managing credentials for all these services can quickly become a headache.

![The image illustrates GitHub Packages, showing various programming languages and tools like JavaScript, Ruby, and Docker, linked to their respective package registries or repositories such as npm, RubyGems, and Docker.](https://kodekloud.com/kk-media/image/upload/v1752875946/notes-assets/images/GitHub-Actions-Certification-GitHub-Packages/github-packages-programming-languages-tools.jpg)

By consolidating your packages into a single registry—GitHub Packages—you streamline authentication, governance, and version control. Publish and consume packages alongside your code without juggling multiple credentials.

## What Is GitHub Packages?

GitHub Packages is a native package hosting service that lives alongside your repositories. It supports multiple ecosystems, provides fine-grained access control, and integrates directly with GitHub Actions to automate your CI/CD pipelines.

![The image is a presentation slide about GitHub Packages, featuring icons and text highlighting seamless integration with package managers and secure code sharing.](https://kodekloud.com/kk-media/image/upload/v1752875946/notes-assets/images/GitHub-Actions-Certification-GitHub-Packages/github-packages-integration-presentation-slide.jpg)

## Supported Ecosystems

GitHub Packages works with all major package managers and container registries:

| Ecosystem     | Registry URL                                    | Example Manager Action          |
| ------------- | ----------------------------------------------- | ------------------------------- |
| JavaScript    | `https://npm.pkg.github.com/`                   | actions/setup-node\@v3          |
| Ruby          | `https://rubygems.pkg.github.com/`              | ruby/setup-ruby\@v1             |
| Java (Maven)  | `https://maven.pkg.github.com/OWNER/REPO`       | actions/setup-java\@v3          |
| Java (Gradle) | same as Maven                                   | gradle config in `build.gradle` |
| Docker        | `ghcr.io`                                       | docker/login-action\@v2         |
| .NET (NuGet)  | `https://nuget.pkg.github.com/OWNER/index.json` | actions/setup-dotnet\@v2        |

![The image illustrates GitHub Packages, showing different programming languages and tools like JavaScript, Ruby, and Docker, and their corresponding package managers such as npm registry and RubyGems.](https://kodekloud.com/kk-media/image/upload/v1752875948/notes-assets/images/GitHub-Actions-Certification-GitHub-Packages/github-packages-programming-languages-tools-2.jpg)

## Why Use GitHub Packages?

* **Centralized management**\
  Keep code, CI/CD workflows, and packages in one place for consistent versioning.
* **Secure distribution**\
  Leverage private packages or granular access controls tied to your GitHub org.
* **Streamlined workflows**\
  Publish & consume packages in the same Actions workflow—no external credentials needed.

![The image highlights three benefits of using GitHub Packages: centralized management, secure distribution, and simplified workflow, each represented by an icon.](https://kodekloud.com/kk-media/image/upload/v1752875949/notes-assets/images/GitHub-Actions-Certification-GitHub-Packages/github-packages-benefits-icons.jpg)

## Integration with GitHub Actions

GitHub Actions automates build, test, and publish steps to your GitHub Packages registry. Each package manager exposes a unique endpoint:

![The image illustrates GitHub Actions with GitHub Packages, showing package registry endpoints for npm, maven, nuget, and rubygems, alongside a container registry endpoint for ghcr.io.](https://kodekloud.com/kk-media/image/upload/v1752875950/notes-assets/images/GitHub-Actions-Certification-GitHub-Packages/github-actions-packages-registry-diagram.jpg)

### Example Workflows

#### Publish an npm Package

```yaml theme={null}
