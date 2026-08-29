# Understanding Deployment Pipeline

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Deployment-with-GitLab/Understanding-Deployment-Pipeline/page

This guide explains how to extend a CI/CD pipeline to include Kubernetes deployments, integration tests, and manual approval steps.

In modern DevOps workflows, a well-structured CI/CD pipeline automates building, testing, and deploying your application. In this guide, we'll extend our existing pipeline—unit testing, code coverage, and Docker containerization—to include deployments to Kubernetes (development and production), integration tests, and a manual approval step.

## Pipeline Stages Overview

| Stage                                              | Description                                                         |
| -------------------------------------------------- | ------------------------------------------------------------------- |
| 1. Unit Testing                                    | Install dependencies, execute unit tests, and publish test reports. |
| 2. Code Coverage                                   | Generate and upload coverage metrics.                               |
| 3. Docker Containerization                         | Build a Docker image, validate locally, and push to a registry.     |
| 4. Kubernetes Deployment (Dev) + Integration Tests | Deploy manifests to dev cluster, verify via Ingress, and run tests. |
| 5. Manual Approval                                 | Pause the pipeline for stakeholder review before production.        |
| 6. Kubernetes Deployment (Prod) + Smoke Tests      | Deploy to prod cluster and perform smoke tests.                     |

***

## 1. Unit Testing

First, install project dependencies and run your unit tests to catch regressions early.

```bash theme={null}
npm install
npm test
