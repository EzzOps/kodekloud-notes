# Install dependencies
npm install

# Run unit tests
npm test

# (Optional) Archive or download test reports
```

> **lightbulb** Store your test reports (e.g., JUnit XML) as artifacts for later analysis or reporting.

***

## 2. Code Coverage

Run two parallel jobs:

* **Test Report**: Fails on test errors.
* **Coverage Analysis**: Runs coverage but ignores errors to avoid blocking downstream stages.

```bash theme={null}
# Job A: Test Report
npm install
npm test
# Job B: Coverage Analysis (errors ignored)
npm install
npm run coverage
# Archive coverage-report artifact
```

> **lightbulb** Ignoring coverage errors ensures that a slight dip in metrics doesn’t halt deployments.

***

## 3. Containerization

Build and push a Docker image tagged with the commit SHA. Optionally, smoke-test the container before pushing.

```bash theme={null}
# Build image
docker build -t myregistry/xyz-app:${CI_COMMIT_SHA} .

# Optional smoke test
docker run --rm myregistry/xyz-app:${CI_COMMIT_SHA} npm test

# Push to registry
docker push myregistry/xyz-app:${CI_COMMIT_SHA}
```

***

## 4. Deploy to Development

Apply Kubernetes manifests to the **development** cluster and retrieve the ingress hostname.

```bash theme={null}
# Apply manifests to dev context
kubectl apply -f k8s/ --context dev

# Fetch Dev ingress URL
INGRESS_URL=$(kubectl get ingress xyz-app-ingress \
  --context dev \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

echo "Dev URL: https://${INGRESS_URL}"
```

> **lightbulb** Ensure your kubeconfig is configured with the `dev` context. See [Kubernetes docs](/docs/concepts/configuration/organize-cluster-access-kubeconfig/).

***

## 5. Integration Testing

Validate the development deployment by hitting the health endpoint.

```bash theme={null}
curl --fail https://${INGRESS_URL}/live
```

***

## 6. Manual Approval

A developer or reviewer must approve the pipeline before production rollout. If declined, the pipeline stops here.

> **triangle-alert** Do not skip this step. Manual gates help prevent unintended production changes.

***

## 7. Deploy to Production

Once approved, deploy the same manifests to the **production** cluster.

```bash theme={null}
kubectl apply -f k8s/ --context prod

INGRESS_URL=$(kubectl get ingress xyz-app-ingress \
  --context prod \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

echo "Prod URL: https://${INGRESS_URL}"
```

***

## 8. Post-Deployment Integration Testing

Confirm that the production service is live and healthy.

```bash theme={null}
curl --fail https://${INGRESS_URL}/live
```

***

## Commands Summary

```bash theme={null}
# 1. Unit Testing
npm install
npm test

# 2. Code Coverage (parallel jobs)
npm install && npm test          # Test Report
npm install && npm run coverage  # Coverage Analysis (ignored errors)

# 3. Containerization
docker build -t myregistry/xyz-app:${CI_COMMIT_SHA} .
docker run --rm myregistry/xyz-app:${CI_COMMIT_SHA} npm test
docker push myregistry/xyz-app:${CI_COMMIT_SHA}

# 4. Deploy to Dev
kubectl apply -f k8s/ --context dev
INGRESS_URL=$(kubectl get ingress xyz-app-ingress \
  --context dev \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl --fail https://${INGRESS_URL}/live

# 6. Deploy to Prod
kubectl apply -f k8s/ --context prod
INGRESS_URL=$(kubectl get ingress xyz-app-ingress \
  --context prod \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl --fail https://${INGRESS_URL}/live
```

***

## Links and References

* [GitLab CI/CD pipelines][GitLab CI/CD pipelines]
* [Node.js][Node.js]
* [npm][npm]
* [Docker][Docker]
* [Kubernetes][Kubernetes]

[GitLab CI/CD pipelines]: https://docs.gitlab.com/ee/ci/

[Node.js]: https://nodejs.org/

[npm]: https://docs.npmjs.com/

[Docker]: https://www.docker.com/

[Kubernetes]: https://kubernetes.io/

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/3a1c2306-8091-4dfe-b40f-e2ca53918553/lesson/5ac9bf82-a437-4cd4-b49a-62e131b893ec)


# What are Services

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Integration-with-GitLab/What-are-Services/page

This guide covers GitLab CI/CD pipeline configurations using runners, Docker images, and service containers for efficient job execution.

![The image is a blue gradient background with the text "GitLab CI/CD – Image and Service" and a copyright notice for KodeKloud.](https://kodekloud.com/kk-media/image/upload/v1752877293/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-What-are-Services/gitlab-ci-cd-image-service.jpg)

GitLab CI/CD pipelines run jobs on self-managed or GitLab-hosted runners. Each job executes in an environment defined by tags, Docker images, and optional service containers. This guide covers:

* Choosing runners with tags
* Default containers for SAST
* Installing custom runtimes
* Using dedicated Docker images
* Spinning up service containers

## 1. Choosing a Runner with Tags

Tags assign jobs to specific runners. For example, `ubuntu-latest` provides a full Ubuntu environment with pre-installed tools:

```yaml theme={null}
