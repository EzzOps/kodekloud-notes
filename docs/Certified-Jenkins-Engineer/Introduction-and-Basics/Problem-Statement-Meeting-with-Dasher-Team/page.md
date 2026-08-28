# Problem Statement Meeting with Dasher Team

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Introduction-and-Basics/Problem-Statement-Meeting-with-Dasher-Team/page

This article examines DevOps prerequisites for Dasher Technology and demonstrates how GitHub Actions can streamline their CI/CD workflow.

This article examines the DevOps prerequisites of Dasher Technology and demonstrates how GitHub Actions can streamline their CI/CD workflow.

Dasher Technology offers a platform that integrates data, applications, and devices across on-premises environments. Their R\&D team is exploring cloud migration and containerization, starting with a Node.js project before extending to Java and Python applications. To spearhead this, they formed a DevOps team led by Alice, whose mission is to design and implement a best-practice CI/CD pipeline on a multi-cloud infrastructure using Docker and Kubernetes.

## Current State and Challenges

Alice’s assessment uncovered several critical gaps in the existing Node.js project:

* No version control system in place
* Developers work in isolation with manual code integration
* Slow, error-prone testing and infrequent merges
* Manual deployments across development, staging, and production

<Callout icon="triangle-alert">
  Without version control and automation, release risk is high and collaboration suffers.
</Callout>

<Frame>
  ![The image outlines the DevOps requirements for the Task Dash Team, highlighting processes like code integration, collaboration, manual testing, and deployment, alongside automated tasks such as unit testing, code coverage, building, pushing, deploying, and automated IT.](https://kodekloud.com/kk-media/image/upload/v1752870588/notes-assets/images/Certified-Jenkins-Engineer-Problem-Statement-Meeting-with-Dasher-Team/devops-requirements-task-dash-team.jpg)
</Frame>

## Defining the CI/CD Pipeline

To address these challenges, Alice defined a CI/CD pipeline with these stages:

1. Adopt GitHub for version control and team collaboration
2. Automate unit tests and measure code coverage
3. Build and push Docker images
4. Deploy the application to Kubernetes
5. Run automated integration tests

## Evaluating CI/CD Tools

The market offers many CI/CD solutions:

| Tool      | Pros                                           | Cons                                     |
| --------- | ---------------------------------------------- | ---------------------------------------- |
| Jenkins   | Extensible, self-hosted, large plugin library  | Manual maintenance, steep learning curve |
| Travis CI | Easy cloud setup, GitHub integration           | Limited concurrency in open-source tier  |
| CircleCI  | Fast workflows, SSH debugging                  | Usage-based pricing                      |
| Spinnaker | Kubernetes-centric, advanced deployment models | Complex configuration                    |
| Bamboo    | Tight Jira integration                         | License costs                            |

These tools require provisioning servers, installing dependencies, and ongoing management. As projects multiply (Java, Python, AWS, Azure), manual overhead grows:

<Frame>
  ![The image lists traditional CI/CD tools and their challenges, featuring logos for Java, Maven, Python, Azure, AWS CLI, Trivy, and Kubesec.](https://kodekloud.com/kk-media/image/upload/v1752870589/notes-assets/images/Certified-Jenkins-Engineer-Problem-Statement-Meeting-with-Dasher-Team/ci-cd-tools-challenges-logos.jpg)
</Frame>

## Jenkins Setup: Manual Steps

If choosing Jenkins, the initial setup includes:

| Step | Description                                           |
| ---- | ----------------------------------------------------- |
| 1    | Provision VM with CPU, memory, and disk               |
| 2    | Install Java JDK                                      |
| 3    | Configure firewall rules                              |
| 4    | Install Jenkins and required plugins                  |
| 5    | Install Node.js, npm (multiple versions)              |
| 6    | Install Docker for image builds                       |
| 7    | Install `kubectl`, Helm, and other Kubernetes clients |
| 8    | Add CLIs for integration testing and reporting        |

<Callout icon="lightbulb">
  As the ecosystem expands, you may also need Maven, Python, AWS CLI, Trivy, KubeSec, and other DevSecOps tools.
</Callout>

## Why GitHub Actions?

Alice needed a solution that:

* Requires minimal setup and no separate infrastructure
* Lets the team focus on pipeline development, not server management
* Scales automatically across multiple languages and clouds

After evaluation, GitHub Actions emerged as the best fit. In the next sections, we will:

* Initialize the GitHub repository for Node.js
* Configure workflows for testing and code coverage
* Build and publish Docker images
* Deploy to Kubernetes using `kubectl` and Helm
* Automate end-to-end integration tests

## Links and References

* [GitHub Actions Documentation](https://docs.github.com/actions)
* [Docker Hub](https://hub.docker.com/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Trivy: Container Image Security Scanner](https://github.com/aquasecurity/trivy)
* [Helm Charts](https://helm.sh/docs/topics/charts/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/2e8ea9bb-e5bb-428e-85d9-89f2eb816adb/lesson/dca7fdee-6afa-4fbb-a76e-8029aa525025" />
</CardGroup>
