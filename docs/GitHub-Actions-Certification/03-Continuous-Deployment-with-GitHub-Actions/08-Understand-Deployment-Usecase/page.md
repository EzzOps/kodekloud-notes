# Understand Deployment Usecase

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Deployment-with-GitHub-Actions/Understand-Deployment-Usecase/page

This article explores a full CI/CD pipeline including unit tests, Docker containerization, and Kubernetes deployments with manual approval for production.

In this lesson we explore a full CI/CD pipeline: from unit tests and coverage reports to Docker containerization and Kubernetes deployments. We’ll also add integration checks and enforce a manual approval gate before releasing to production.

## Pipeline Overview

| Stage               | Description                    | Commands                                                                   |
| ------------------- | ------------------------------ | -------------------------------------------------------------------------- |
| Unit Testing        | Validate application logic     | `npm install`<br />`npm test`                                              |
| Code Coverage       | Generate coverage metrics      | `npm install`<br />`npm run coverage`                                      |
| Docker Build & Push | Containerize and publish image | `docker build -t your-image:latest .`<br />`docker push your-image:latest` |

<Callout icon="lightbulb">
  Ensure your CI configuration archives test reports and coverage artifacts for visibility.
</Callout>

## 1. Completed CI Jobs

Here are the commands executed in separate CI stages:

```bash theme={null}
