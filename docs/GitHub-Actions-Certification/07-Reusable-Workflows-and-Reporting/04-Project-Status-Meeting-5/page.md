# .github/workflows/nodejs-ci.yml
name: Node.js CI/CD

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '14'

      - run: npm install
      - run: npm test

      - name: Build and push image
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKER_HUB }}/app-node:latest

      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@v1
        with:
          manifests: k8s/deployment.yml
```

## Expansion to Java and Python Applications

Dasher Technologies will now extend this CI/CD pattern to its Java and Python services. Because all three microservices share the same Kubernetes deployment model, we’ll extract common steps into a single reusable workflow.

| Service   | Language | CI/CD Workflow File |
| --------- | -------- | ------------------- |
| Service A | Node.js  | `nodejs-ci.yml`     |
| Service B | Java     | `java-ci.yml`       |
| Service C | Python   | `python-ci.yml`     |

<Callout icon="lightbulb">
  Extracting shared deployment steps into a reusable workflow ensures consistency, reduces duplication, and makes future updates easier.
</Callout>

## Designing the Reusable Deployment Workflow

We’ll create a reusable workflow at `.github/workflows/deploy.yml` containing the standardized Kubernetes deployment logic:

```yaml theme={null}
# .github/workflows/deploy.yml
name: Reusable Kubernetes Deployment

on:
  workflow_call:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up kubectl
        uses: azure/setup-kubectl@v1

      - name: Authenticate to Kubernetes
        run: |
          kubectl config set-context ${{ secrets.K8S_CONTEXT }}

      - name: Apply manifests and rollout
        run: |
          kubectl apply -f k8s/deployment.yml
          kubectl rollout status deployment/${{ github.job }}
```

Each service-specific workflow will call this reusable deployment:

```yaml theme={null}
# .github/workflows/nodejs-ci.yml (excerpt)
...
jobs:
  build:
    # build steps here

  deploy:
    uses: ./.github/workflows/deploy.yml
    with:
      # pass any required inputs or secrets
```

## Action Items

* Finalize and review `deploy.yml` template
* Update Java and Python workflows to invoke the reusable deployment
* Run end-to-end tests for all three services
* Document the new CI/CD pattern for the engineering team

## Links and References

* [GitHub Actions Documentation](https://docs.github.com/actions)
* [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
* [Docker Hub](https://hub.docker.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/da8706ee-24ab-41a1-916d-da8232ca028e/lesson/064e58a9-1e11-442e-9773-c046755ad261" />
</CardGroup>


# Project Status Meeting 5

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Reusable-Workflows-and-Reporting/Project-Status-Meeting-5/page

Alice and her team implement a long-term storage solution for CI artifacts by syncing reports to Amazon S3, addressing GitHub Actions’ retention limits.

In this lesson, Alice and her team address GitHub Actions’ artifact retention limits by implementing a long-term storage solution. By adding a dedicated workflow that collects test and coverage reports and syncs them to an Amazon S3 bucket, they ensure indefinite access to CI artifacts.

***

## Background

Our existing CI pipeline uses two primary jobs:

| Job Name      | Artifact Name   | Description                           |
| ------------- | --------------- | ------------------------------------- |
| unit-test     | test-reports    | Runs unit tests and exports JUnit XML |
| code-coverage | coverage-report | Generates coverage data (`lcov`)      |

<Callout icon="lightbulb">
  Artifacts are retained for up to 90 days and can be no larger than 5 GB each. Syncing reports to S3 immediately after CI avoids expiration and size caps.
</Callout>

***

## Solution Overview

1. Extend (or create) a workflow that triggers when the primary CI run completes.
2. Download the `test-reports` and `coverage-report` artifacts.
3. Use an S3 sync action to upload all reports to your S3 bucket.

***

## Workflow Configuration

Add a new file at `.github/workflows/report-storage.yml`:

```yaml theme={null}
name: Store Reports to S3

on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]

jobs:
  upload-reports:
    name: Upload Test & Coverage Reports
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Download Test Reports
        uses: actions/download-artifact@v3
        with:
          name: test-reports
          path: reports/tests

      - name: Download Coverage Reports
        uses: actions/download-artifact@v3
        with:
          name: coverage-report
          path: reports/coverage

      - name: Sync Reports to S3
        uses: jakejarvis/s3-sync-action@v0.5.1
        with:
          args: --acl private --delete
        env:
          AWS_S3_BUCKET: ${{ secrets.S3_BUCKET }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: us-east-1
          SOURCE_DIR: reports/
```

<Callout icon="triangle-alert">
  Make sure you’ve defined the following secrets under **Settings > Secrets and variables > Actions**:

  * `S3_BUCKET`
  * `AWS_ACCESS_KEY_ID`
  * `AWS_SECRET_ACCESS_KEY`
</Callout>

<Callout icon="lightbulb">
  The `workflow_run` trigger ensures the upload job only runs after the `CI` workflow has completed successfully.
</Callout>

***

## Next Steps

1. Commit and push `report-storage.yml` to your repository.
2. Confirm that `unit-test` and `code-coverage` jobs publish artifacts named `test-reports` and `coverage-report`.
3. Trigger your CI workflow and verify the `reports/` directory appears in your S3 bucket.

With this setup, Alice’s team will maintain reliable, long-term access to both test results and coverage metrics.

***

## Links and References

* [GitHub Actions: workflow\_run event](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_run)
* [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/)
* [jakejarvis/s3-sync-action](https://github.com/jakejarvis/s3-sync-action)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/da8706ee-24ab-41a1-916d-da8232ca028e/lesson/6a92e896-2260-4b90-a75a-775538d7db06" />
</CardGroup>
