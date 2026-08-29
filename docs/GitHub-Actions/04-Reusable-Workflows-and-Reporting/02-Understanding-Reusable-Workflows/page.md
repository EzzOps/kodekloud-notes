# Understanding Reusable Workflows

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Reusable-Workflows-and-Reporting/Understanding-Reusable-Workflows/page

This article explains how to create and use reusable workflows in GitHub Actions for efficient CI/CD pipeline management.

Creating modular, maintainable CI/CD pipelines is essential for growing codebases. GitHub Actions **reusable workflows** let you extract common jobs—such as deployments—into standalone workflows that multiple repositories or branches can call. This approach eliminates duplication, reduces errors, and enforces consistent deployment practices across projects.

![The image shows a visual representation of a CI/CD workflow with steps for unit testing, code coverage, dependency scanning, application building, and deployment to development and production environments.](https://kodekloud.com/kk-media/image/upload/v1752876737/notes-assets/images/GitHub-Actions-Understanding-Reusable-Workflows/ci-cd-workflow-unit-testing-deployment.jpg)

The diagram above depicts a typical CI/CD pipeline for a Node.js application:

1. **Unit Testing**
2. **Code Coverage**
3. **Dependency Scanning**
4. **Build**
5. **Deploy to Dev** (runs after build succeeds)
6. **Deploy to Prod** (waits for Dev deployment)

Each deployment job consists of five granular steps (e.g., environment setup, artifact upload, feature flag toggles, smoke tests, notifications).

## Why Use Reusable Workflows?

Imagine your organization maintains services in Java, Python, .NET, Go, and more. While build and test commands differ, deployment steps—like provisioning infrastructure, uploading artifacts, and running smoke tests—tend to be identical. Reusable workflows centralize these shared steps:

| Programming Language | Build Tool   | Test Tool    | Deployment Steps                         |
| -------------------- | ------------ | ------------ | ---------------------------------------- |
| Java                 | Maven/Gradle | JUnit/TestNG | Provision → Deploy → Smoke Test → Notify |
| Python               | pip/Poetry   | pytest       | Provision → Deploy → Smoke Test → Notify |
| .NET                 | dotnet build | xUnit        | Provision → Deploy → Smoke Test → Notify |
| Go                   | go build     | go test      | Provision → Deploy → Smoke Test → Notify |
| Node.js              | npm/ Yarn    | Jest/Mocha   | Provision → Deploy → Smoke Test → Notify |

By extracting deployment logic into its own workflow, you avoid copy-pasting nearly identical YAML across repositories. Instead, each app’s pipeline can **call** the reusable deployment workflow.

***

## 1. Extracting the Deployment Job

Let’s say you have a repository `xyz-org/nodejs-app-repo` with `.github/workflows/awesome-app.yml`:

```yaml theme={null}
