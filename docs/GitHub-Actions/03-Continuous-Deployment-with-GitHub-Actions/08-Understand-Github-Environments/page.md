# Example: Build and run locally
npm install
npm test
npm run coverage
docker build -t my-app:latest .
docker run -p 3000:3000 my-app:latest
docker push my-app:latest
```

## Deploying to Kubernetes

To deploy the Docker image, prepare these Kubernetes manifests:

* **Deployment**: Defines Pods and ReplicaSets in `k8s/deployment.yaml`
* **Service**: Exposes Pods internally via `k8s/service.yaml`
* **Ingress**: Routes external HTTP traffic using `k8s/ingress.yaml`

Apply them in sequence:

```bash theme={null}
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## Integration Testing on Dev

Once the resources are live, validate the deployment:

```bash theme={null}
curl http://dev.my-app.example.com/health
```

A `200 OK` response confirms that the application is operating correctly in the development cluster.

> **lightbulb** Ensure your Kubernetes context is set to the development cluster:

  ```bash theme={null}
  kubectl config use-context dev-cluster
  ```

## Manual Approval Gate

Before proceeding to production, implement a manual approval step in your CI/CD workflow. This prevents unintentional releases.

> **triangle-alert** An administrator must review the integration test results and approve the release.\
  Skipping this step can lead to unverified changes reaching production.

## Production Deployment

After approval, deploy to the production cluster using the same manifests:

1. Switch to the production context:
   ```bash theme={null}
   kubectl config use-context prod-cluster
   ```
2. Apply the manifests:
   ```bash theme={null}
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   kubectl apply -f k8s/ingress.yaml
   ```
3. Run production integration tests:
   ```bash theme={null}
   curl http://my-app.example.com/health
   ```

Optionally, configure post-deployment alerts or monitoring checks to ensure reliability.

## Next Steps

In the next lesson, we’ll cover Kubernetes fundamentals in depth and build automated workflow files for our CI/CD pipeline.

## Links and References

* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)
* [CI/CD Best Practices](https://www.redhat.com/en/topics/devops/what-is-ci-cd)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions/module/92928734-1d5a-462d-9414-2d3865f5ef79/lesson/fa0d124d-feb8-48a0-b10e-0cf45d876932)


# Understand Github Environments

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Deployment-with-GitHub-Actions/Understand-Github-Environments/page

This article explains GitHub Environments, focusing on organizing, protecting, and visualizing deployments in GitHub Actions.

In this lesson, we’ll dive into GitHub Environments and explore how they help you organize, protect, and visualize deployments in GitHub Actions. You’ll learn how to store secrets, enforce protection rules, and reference environments in your workflows.

## What Are Environments?

Environments provide isolated stages in your CI/CD pipeline—such as **development**, **staging**, and **production**—so that different teams can work concurrently without stepping on each other’s toes. Each environment typically uses its own services (databases, vaults, APIs) secured by environment-specific credentials (usernames/passwords or API keys).

When you run workflows in GitHub Actions, environments let you:

* Store and manage sensitive credentials securely
* Pause workflows for manual approvals or delays
* Restrict deployments by branch or user permissions

## Secrets and Variables in GitHub Actions

GitHub Actions supports two levels of secret storage:

1. **Repository secrets**
2. **Environment secrets**

By keeping sensitive information—like API keys or database passwords—out of your workflow files, you centralize secret management and reduce the risk of accidental disclosure.

![The image shows two sections labeled "Repository secrets" and "Environment secrets," each containing entries for passwords like "DOCKER\_PASSWORD" and "DATABASE\_PASSWORD" associated with different environments.](https://kodekloud.com/kk-media/image/upload/v1752876462/notes-assets/images/GitHub-Actions-Understand-Github-Environments/repository-secrets-environment-secrets-passwords.jpg)

> **lightbulb** Environment secrets override repository secrets when they share the same name. Plan your naming conventions and access levels accordingly.

### Repository vs. Environment Secrets

| Feature       | Repository Secrets                    | Environment Secrets                                    |
| ------------- | ------------------------------------- | ------------------------------------------------------ |
| Scope         | Single repository                     | Specific to an environment; reusable across repos      |
| Visibility    | All repository collaborators          | Restricted to users with environment access            |
| Accessibility | Available to all jobs in a workflow   | Only available to jobs that reference that environment |
| Precedence    | Lower if an environment secret exists | Overrides repository secrets when names collide        |

![The image is a comparison chart between "Repository Secrets" and "Environment Secrets," highlighting features and their corresponding levels of access and visibility. It includes icons and numbered labels for each feature.](https://kodekloud.com/kk-media/image/upload/v1752876463/notes-assets/images/GitHub-Actions-Understand-Github-Environments/repository-secrets-vs-environment-secrets-chart.jpg)

## Referencing an Environment in Your Workflow

Here’s a sample job that targets a **production** environment:

```yaml theme={null}
jobs:
  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      - name: Deploy
        run: ./scripts/deploy.sh
```

This job will pause if any **deployment protection rules** are configured for the `production` environment.

## Deployment Protection Rules

Environments in GitHub Actions let you enforce rules before workflows proceed. You can require approvals, add delays, and restrict deployments to certain branches or users. To configure these:

1. Go to **Settings** in your repository (or organization/enterprise).
2. Select **Environments**, then choose or create an environment.
3. Under **Deployment protection rules**, add your constraints.

![The image shows a configuration screen for "Deployment Protection Rules" in a software environment, detailing options for required reviewers and a wait timer. It includes fields to add reviewers and set a wait time before deployment.](https://kodekloud.com/kk-media/image/upload/v1752876464/notes-assets/images/GitHub-Actions-Understand-Github-Environments/deployment-protection-rules-configuration.jpg)

### Common Rule Types

| Rule Type           | Description                                                                         |
| ------------------- | ----------------------------------------------------------------------------------- |
| Required reviewers  | Specify up to six people or teams. One approval unlocks the deployment.             |
| Wait timer          | Introduce a mandatory delay before jobs start.                                      |
| Branch restrictions | Only allow deployments to run from designated branches (e.g., `main` or `release`). |

When a workflow references an environment with protection rules, it will:

1. Pause until all **required reviewers** have approved.
2. Enforce any **wait timer** before continuing.
3. Check that the workflow branch meets **branch restrictions**.

![The image shows a diagram of "Deployment Protection Rules" with sections for restricting deployment branches and setting deployment protection rules, including events and environments.](https://kodekloud.com/kk-media/image/upload/v1752876465/notes-assets/images/GitHub-Actions-Understand-Github-Environments/deployment-protection-rules-diagram.jpg)

> **triangle-alert** Over-privileged environments or weak approval policies can expose production data. Review access controls regularly and follow the principle of least privilege.

***

By structuring your CI/CD pipeline with GitHub Environments, you gain fine-grained control over deployments while keeping secrets centralized and secure. Start with basic rules and expand them as your project requirements grow.

## Links and References

* [GitHub Actions Environments](https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment)
* [Managing secrets in GitHub](https://docs.github.com/actions/security-guides/encrypted-secrets)
* [GitHub Actions documentation](https://docs.github.com/actions)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions/module/92928734-1d5a-462d-9414-2d3865f5ef79/lesson/02ef7603-94d0-4be3-97f1-86ae2c14ac83)
