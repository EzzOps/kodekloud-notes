# Understanding DevOps Pipeline

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Integration-with-GitHub-Actions/Understanding-DevOps-Pipeline/page

This guide covers a complete DevOps pipeline including CI, CD, CDel, and post-build reporting using Jenkins and various deployment targets.

In this guide, we’ll walk through a complete DevOps pipeline—covering Continuous Integration (CI), Continuous Deployment (CD), Continuous Delivery (CDel), and Post-Build Reporting. We’ll orchestrate everything with [Jenkins][jenkins], deploying to three targets:

* **AWS EC2** (Docker container)
* **Kubernetes** via GitOps ([Argo CD][argocd])
* **AWS Lambda** (serverless)

<Frame>
  ![The image is a diagram illustrating a DevOps pipeline, detailing stages of continuous integration, deployment, and delivery, along with post-build processes.](https://kodekloud.com/kk-media/image/upload/v1752875978/notes-assets/images/GitHub-Actions-Certification-Understanding-DevOps-Pipeline/devops-pipeline-continuous-integration-diagram.jpg)
</Frame>

***

## Continuous Integration (CI)

We adopt a **feature-branch workflow**:

<Callout icon="lightbulb">
  Developers work in `feature/*` branches. Every push to a feature branch automatically triggers the Jenkins CI pipeline.
</Callout>

### CI Stages Overview

| Stage                    | Tool/Command                                                             | Purpose                                     |
| ------------------------ | ------------------------------------------------------------------------ | ------------------------------------------- |
| Install Dependencies     | `npm install`                                                            | Install Node.js packages                    |
| Dependency Vulnerability | `owasp-dependency-check`, `npm audit`                                    | Detect known security issues                |
| Unit Tests & Coverage    | `npm test`, `nyc --reporter=lcov npm test`                               | Validate functionality and measure coverage |
| Static Code Analysis     | `sonar-scanner`                                                          | Enforce quality gates via SonarCloud        |
| Containerization         | `docker build -t my-app:${BRANCH_NAME}-${BUILD_NUMBER} .`                | Package app into a Docker image             |
| Image Vulnerability Scan | `snyk test --docker my-app:${BRANCH_NAME}-${BUILD_NUMBER}`               | Scan container image for vulnerabilities    |
| Push to Registry         | `docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest` | Store image in AWS ECR                      |

***

### 1. Install Dependencies

```bash theme={null}
npm install
```

### 2. Dependency Vulnerability Scans

```bash theme={null}
owasp-dependency-check --project my-app
npm audit --audit-level=moderate
```

### 3. Unit Tests & Coverage

```bash theme={null}
npm test
