# Environment and Deployments

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Deployment-with-GitLab/Environment-and-Deployments/page

This guide explains how to configure and manage environments and deployments in GitLab CI/CD.

In this guide, you’ll learn how to configure and manage **environments** and **deployments** in GitLab CI/CD. Environments represent the target locations—such as development, staging, or production—where your code runs. Each pipeline deployment creates a record, providing a clear history of changes and showing what version is currently live.

<Callout icon="lightbulb">
  For full details, see the [Environments and Deployments reference in GitLab docs](https://docs.gitlab.com/ee/ci/environments/).
</Callout>

We’ll cover:

* Defining environments in `.gitlab-ci.yml`
* A sample pipeline with containerization, testing, and deployment
* Static vs. dynamic environments
* Creating environments in the GitLab UI
* Viewing, rolling back, and redeploying applications

***

## 1. Defining an Environment in `.gitlab-ci.yml`

You can declare environments directly in job definitions to track deployments and enable quick-access links.

### Simple Environment Declaration

```yaml theme={null}
deploy to production:
  stage: deploy
  script:
    - git push production HEAD:main
  environment: production
```

This tracks deployments under the `production` environment name.

### Expanded Environment Configuration

```yaml theme={null}
deploy to production:
  stage: deploy
  script:
    - git push production HEAD:main
  environment:
    name: production
    url: https://prod.example.com
```

* **name**: The identifier displayed in the GitLab UI.
* **url**: External link to the live application for rapid access.

***

## 2. Example Pipeline Configuration

Here’s a streamlined pipeline showcasing containerization, tests, and deployment to a Kubernetes namespace:

```yaml theme={null}
stages:
  - containerization
  - test
  - dev-deploy
