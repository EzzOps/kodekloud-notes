# Project Status Meeting 1

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Integration-with-GitLab/Project-Status-Meeting-1/page

This article outlines a plan to build a GitHub Actions CI/CD pipeline for a Node.js application, covering preparatory tasks and workflow design.

In this lesson, we’ll outline a nine-task plan to build a robust GitHub Actions workflow for our Node.js application. We’ll cover the first four preparatory steps, then get ready to implement jobs for unit testing, code coverage, and container scanning.

***

## Tasks Overview

| Task # | Task Name                             | Goal                                                 |
| ------ | ------------------------------------- | ---------------------------------------------------- |
| 1      | Review Node.js Application Structure  | Understand key files, folders, and scripts           |
| 2      | Gather DevOps Requirements            | Define CI/CD objectives: testing, coverage, scanning |
| 3      | Define High-Level Workflow Design     | Outline workflow jobs, steps, and dependencies       |
| 4      | Prepare Repository for GitHub Actions | Create workflow folders and placeholder files        |

***

## 1. Reviewing the Node.js Application Structure

### Overview

Examine `package.json`, `src/`, `tests/`, and configuration files to map dependencies and scripts.

### Rationale

A clear project structure ensures CI/CD steps run against the correct files and directories.

### Steps

1. Open `package.json` to list dependencies and custom scripts.
2. Inspect `src/` for source code and `tests/` for existing test cases.
3. Verify `.gitignore` and any config files (`.eslintrc`, `.prettierrc`) align with best practices.

<Callout icon="lightbulb">
  Consistent project layout reduces CI configuration errors and simplifies maintenance.
</Callout>

***

## 2. Gathering DevOps Requirements

### Overview

Identify the essential DevOps checks our GitHub Actions pipeline must perform.

### Rationale

Aligning with DevOps goals helps automate quality gates and security checks.

### Key Requirements

* Run `npm test` on pull requests and main branch pushes
* Generate code coverage reports via `jest --coverage`
* Scan Docker images for vulnerabilities using a security scanner

***

## 3. Defining the Workflow’s High-Level Design

### Overview

Draft a YAML outline for the GitHub Actions workflow with three main jobs: test, coverage, and scan.

### Rationale

A modular, high-level design makes it easier to extend and debug the CI/CD pipeline.

### Workflow Outline

```yaml theme={null}
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ '*' ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Dependencies
        run: npm ci
      - name: Run Unit Tests
        run: npm test

  coverage:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v2
      - name: Generate Coverage Report
        run: npm run coverage

  scan:
    runs-on: ubuntu-latest
    needs: coverage
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker Image
        run: docker build . -t my-node-app:latest
      - name: Scan Container for Vulnerabilities
        uses: aquasecurity/trivy-action@v0.2.0
        with:
          image-ref: my-node-app:latest
```

***

## 4. Preparing the Repository for GitHub Actions

### Overview

Set up repository directories and placeholder workflow files before writing actual job steps.

### Rationale

Creating the `.github/workflows` structure in advance makes iteration faster and cleaner.

### Steps

1. Create `.github/workflows/` at the repo root.
2. Add `ci.yml` containing the outline from Section 3.
3. Commit and push these changes, then open a pull request targeting `main`.

<Callout icon="triangle-alert">
  Never commit secrets (e.g., `DOCKER_HUB_TOKEN`) to source files. Store them securely in GitHub repository settings under **Secrets and variables**.
</Callout>

***

## Next Steps

Once these four tasks are complete, we will implement:

* Unit Testing Job with parallel matrix strategy
* Code Coverage Report with badge publishing
* Container Security Scanning with vulnerability alerts

***

## References

* [GitHub Actions Documentation](https://docs.github.com/actions)
* [Jest Code Coverage](https://jestjs.io/docs/configuration#coveragedirectory-string)
* [Trivy Docker Scanner](https://github.com/aquasecurity/trivy)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/3a1c2306-8091-4dfe-b40f-e2ca53918553/lesson/d4eeaac7-c732-4546-9e6d-8f89b76b2e34" />
</CardGroup>
