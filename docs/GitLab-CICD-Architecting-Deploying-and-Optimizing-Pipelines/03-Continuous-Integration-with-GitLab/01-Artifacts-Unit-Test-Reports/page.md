# Download and publish test reports for CI dashboards
```

<Callout icon="lightbulb">
  Ensure your test reports (e.g., JUnit XML) are stored in a known directory so your CI tool can archive them.
</Callout>

***

## 2. Code Coverage

Measure code coverage to identify untested parts of the codebase.

```bash theme={null}
npm install
npm run coverage
# Upload coverage report (e.g., Istanbul/nyc) to your coverage service
```

***

## 3. Docker Containerization

Package the application into a Docker image, verify it locally, then push to your registry (Docker Hub, AWS ECR, etc.).

```bash theme={null}
docker build -t your-app:latest .
docker run --rm your-app:latest
docker push your-app:latest
```

***

## 4. Deploy to Kubernetes (Dev) + Integration Tests

Apply your Kubernetes manifests to the development namespace, then validate functionality through the Dev Ingress.

```bash theme={null}
# Deploy to dev namespace
kubectl apply -f k8s/deployment.yaml   --namespace=dev
kubectl apply -f k8s/service.yaml      --namespace=dev
kubectl apply -f k8s/ingress.yaml      --namespace=dev

# Verify Ingress endpoint
kubectl get ingress --namespace=dev
curl https://dev.your-domain.com/healthz
```

<Callout icon="lightbulb">
  Use environment-specific `ConfigMap` or `Secret` manifests to configure your dev environment. Keep secrets encrypted (e.g., [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)).
</Callout>

***

## 5. Manual Approval

Introduce a manual gate to ensure that a team lead or QA engineer reviews the dev deployment results before promoting to production.

<Callout icon="triangle-alert">
  Skipping this approval can lead to unverified changes hitting production. Always review test logs and integration results.
</Callout>

***

## 6. Deploy to Kubernetes (Prod) + Smoke Tests

Upon approval, deploy the identical manifests to your production namespace and execute a quick smoke test.

```bash theme={null}
# Deploy to prod namespace
kubectl apply -f k8s/deployment.yaml   --namespace=prod
kubectl apply -f k8s/service.yaml      --namespace=prod
kubectl apply -f k8s/ingress.yaml      --namespace=prod

# Verify Ingress and run smoke test
kubectl get ingress --namespace=prod
curl https://prod.your-domain.com/healthz
```

***

## Next Steps

Before writing your CI/CD workflow (e.g., GitHub Actions, GitLab CI, Jenkins Pipeline), ensure all Kubernetes best practices are in place:

* Namespace isolation for dev and prod
* Resource requests and limits
* Liveness and readiness probes
* Secure handling of secrets

***

## Links and References

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Official Documentation](https://docs.docker.com/)
* [npm CLI Commands](https://docs.npmjs.com/cli/v7/)
* [Sealed Secrets by Bitnami](https://github.com/bitnami-labs/sealed-secrets/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/df17ec22-8cda-4af7-af44-10f9f061d4a8/lesson/4069c393-95e0-4518-bea7-e7db1b2d2710" />
</CardGroup>


# Artifacts Unit Test Reports

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Integration-with-GitLab/Artifacts-Unit-Test-Reports/page

This guide explains how to collect and visualize JUnit-style test results in GitLab CI/CD using Mocha and Node.js.

In this guide, you’ll learn how to collect JUnit-style XML results from a Node.js project using Mocha, upload them as artifacts in GitLab CI/CD, and visualize test reports in merge requests and pipelines. We’ll cover:

1. Basic `artifacts` configuration
2. Customizing retention and upload settings
3. Enabling `artifacts:reports` for JUnit
4. Available report types
5. Viewing failures in a merge request
6. Analyzing test summaries in the pipeline

***

## Prerequisites

* A GitLab project with CI/CD enabled
* A Node.js test suite configured with [mocha-junit-reporter](https://www.npmjs.com/package/mocha-junit-reporter)

<Callout icon="lightbulb">
  Install the JUnit reporter locally:

  ```bash theme={null}
  npm install --save-dev mocha-junit-reporter
  ```

  Ensure your `package.json` test script invokes the reporter.
</Callout>

***

## 1. Basic CI/CD Job to Run Tests and Upload Artifacts

Start with a simple CI job that runs tests and uploads **all** generated files upon success:

```yaml theme={null}
stages:
  - test

variables:
  MONGO_URI: 'mongodb+srv://supercluster.d83jj.mongodb.net/superData'
  MONGO_USERNAME: superuser
  MONGO_PASSWORD: $M_DB_PASSWORD

unit_testing:
  stage: test
  image: node:17-alpine3.14
  before_script:
    - npm install
  script:
    - npm test
  artifacts:
    when: on_success
    expire_in: 30 days
```

This configuration uploads every file created during the job and retains them for 30 days.

***

## 2. Always Upload & Customize Artifact Retention

To ensure test results are available even on failure, adjust the `artifacts` block:

```yaml theme={null}
unit_testing:
  stage: test
  image: node:17-alpine3.14
  before_script:
    - npm install
  script:
    - npm test
  artifacts:
    when: always
    expire_in: 3 days
    name: "Mocha-Test-Result"
    paths:
      - test-results.xml
```

* **when: always** – captures artifacts on success or failure
* **expire\_in: 3 days** – limits storage time to 3 days
* **name** – assigns a meaningful archive name
* **paths** – points to the JUnit XML file

### Generating the JUnit XML

Make sure your test command includes the JUnit reporter:

```bash theme={null}
npm test
