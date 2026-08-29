# Unit Tests
npm install
npm test
# Code Coverage
npm install
npm run coverage
# Docker Containerization
docker build -t your-image:latest .
docker run --rm your-image:latest
docker push your-image:latest
```

## 2. Kubernetes Deployment (Development)

Deploy to the development cluster using Kubernetes manifests:

1. Prepare manifests:
   * `deploy/deployment.yaml`
   * `deploy/ingress.yaml`
2. Apply them with `kubectl`:
   ```bash theme={null}
   kubectl apply -f deploy/deployment.yaml
   kubectl apply -f deploy/ingress.yaml
   ```
3. Verify the ingress and perform a quick integration test:
   ```bash theme={null}
   kubectl get ingress
   curl https://<dev-ingress-url>/live
   ```

> **lightbulb** Always verify that the ingress controller and TLS certificates are correctly configured in your dev environment.

## 3. Kubernetes Deployment (Production) with Manual Approval

Before pushing changes to production, insert a manual approval step in your CI/CD workflow. Upon approval, deploy using the same manifests against the production context:

> **triangle-alert** Production deployments are irreversible. Double-check your manifests, image tags, and environment-specific configurations before approving.

```bash theme={null}
# Apply production manifests
kubectl apply -f deploy/deployment.yaml --context=production
kubectl apply -f deploy/ingress.yaml --context=production

# Verify production ingress and run integration test
kubectl get ingress --context=production
curl https://<prod-ingress-url>/live
```

## References

* [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/reference/kubectl/)
* [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
* [npm Documentation](https://docs.npmjs.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions-certification/module/b6687abe-8094-4750-910b-5daa8bc710b1/lesson/bb45f143-6ae8-4663-8eca-7652f30e39c9)


# Understand Github Environments

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Deployment-with-GitHub-Actions/Understand-Github-Environments/page

This guide explains how GitHub Actions environments enhance security, organization, and control in software deployment workflows.

In modern software development, isolating stages like development, testing, and production is crucial. Each environment typically runs its own services (databases, APIs, vaults, etc.) secured by unique credentials or API keys.

In this guide, you’ll learn how GitHub Actions environments help you:

* Securely store environment-specific secrets and variables
* Organize and visualize deployment workflows
* Enforce protection rules to prevent unauthorized changes

## Key Benefits of Environments in GitHub Actions

* Store secrets and variables outside workflow files
* Apply deployment approvals, delays, and branch restrictions
* Track deployments with clear environment contexts

![The image shows two sections labeled "Repository secrets" and "Environment secrets," each containing entries for passwords like "DOCKER\_PASSWORD" and "DATABASE\_PASSWORD" associated with different environments such as production and development.](https://kodekloud.com/kk-media/image/upload/v1752875914/notes-assets/images/GitHub-Actions-Certification-Understand-Github-Environments/repository-environment-secrets-passwords.jpg)

## Repository vs. Environment Secrets

Use repository-level secrets for general workflows and environment-level secrets when you need stricter controls or approvals. Compare their properties below:

| Property      | Repository Secrets                                         | Environment Secrets                                            |
| ------------- | ---------------------------------------------------------- | -------------------------------------------------------------- |
| Scope         | Available to all workflows in the repository               | Only available to workflows referencing a specific environment |
| Visibility    | All repository collaborators                               | Restricted to designated users or teams                        |
| Accessibility | Accessible by every job in a workflow                      | Accessible only by jobs running in the targeted environment    |
| Precedence    | Lower priority—overridden if an environment secret matches | Higher priority—overrides repository-level secret              |

![The image is a comparison chart showing features, repository secrets, and environment secrets, with four numbered sections on the left and corresponding details on the right.](https://kodekloud.com/kk-media/image/upload/v1752875915/notes-assets/images/GitHub-Actions-Certification-Understand-Github-Environments/comparison-chart-features-secrets.jpg)

> **lightbulb** If a secret exists at both repository and environment levels, the environment secret takes precedence automatically.\
  Use this to ensure your production credentials always override any generic repository values.

## Deployment Protection Rules

Environments also let you enforce rules that control who can deploy and under what conditions:

* **Required reviewers**: Up to six people or teams; only one approval is needed.
* **Wait timer**: Introduce a delay before deployment starts.
* **Branch restrictions**: Limit deployments to specific branches (e.g., only `main` for production).

Configure these rules under **Settings > Environments** in your repository. Organization and enterprise accounts can set rules at higher scopes as well.

![The image shows a configuration screen for "Deployment Protection Rules" in a software environment, detailing settings for required reviewers and a wait timer.](https://kodekloud.com/kk-media/image/upload/v1752875916/notes-assets/images/GitHub-Actions-Certification-Understand-Github-Environments/deployment-protection-rules-configuration-screen.jpg)

### Required Reviewers

Assign trusted individuals or teams to approve deployments. Once an approval is granted, the workflow continues.

### Wait Timer

Set a delay to allow stakeholders to perform final checks before deployment.

### Deployment Branch Rules

Restrict which branches can trigger deployments to reduce risk and enforce release processes.

When a workflow references an environment:

1. GitHub validates all protection rules before starting any jobs.
2. Upon passing, jobs gain access to that environment’s secrets.

![The image shows a screenshot of "Deployment Protection Rules" with sections for restricting deployment branches and setting deployment protection rules, including reviewers and timers.](https://kodekloud.com/kk-media/image/upload/v1752875917/notes-assets/images/GitHub-Actions-Certification-Understand-Github-Environments/deployment-protection-rules-screenshot.jpg)

> **triangle-alert** Always scope production secrets narrowly and grant deployment approvals only to essential personnel.\
  Misconfigured rules can expose sensitive credentials or delay critical releases.

## Best Practices

* Start with minimal rules; expand as your project’s security needs grow.
* Rotate secrets regularly and audit environment access logs.
* Document environment policies in your repository’s README or a dedicated SECURITY guide.

## Links and References

* [GitHub Actions Documentation](https://docs.github.com/en/actions)
* [GitHub Environments Guide](https://docs.github.com/en/actions/deployment/targeting-different-environments)
* [Security Best Practices for GitHub](https://securitylab.github.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions-certification/module/b6687abe-8094-4750-910b-5daa8bc710b1/lesson/2645ba03-2dcb-49ed-a916-805f1f39af17)
