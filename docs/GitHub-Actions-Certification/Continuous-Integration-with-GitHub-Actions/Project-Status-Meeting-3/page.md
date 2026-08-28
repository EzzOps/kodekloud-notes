# Shared steps pointing at production DB
- name: Install Dependencies
  run: npm install

- name: Unit Testing
  id: nodejs-unit-testing-step
  run: npm test

- name: Archive Test Result
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: Mocha-Test-Result
    path: test.results.xml

code-coverage:
  name: Code Coverage
  runs-on: ubuntu-latest
  steps:
    - name: Checkout Repository
      uses: actions/checkout@v4

    - name: Setup NodeJS Version - 18
      uses: actions/setup-node@v3
      with:
        node-version: 18

    - name: Cache NPM dependencies
      uses: actions/cache@v3
      with:
        path: node_modules
        key: ${{ runner.os }}-node-modules-{{ hashFiles('package-lock.json') }}

    - name: Install Dependencies
      run: npm install
```

<Frame>
  ![The image shows a GitHub Actions workflow summary for a project, displaying successful completion of unit testing, code coverage, and containerization jobs. The workflow is named "solar-system.yml" and includes details like job durations and annotations.](https://kodekloud.com/kk-media/image/upload/v1752875955/notes-assets/images/GitHub-Actions-Certification-Project-Status-Meeting-2/github-actions-workflow-summary-solar-system.jpg)
</Frame>

***

## 2. Root Cause

The workflow’s global `env` block defines production credentials, causing both testing jobs to connect to the live database:

```yaml theme={null}
name: Solar System Workflow

on:
  workflow_dispatch:
  push:
    branches:
      - main
      - feature/*

env:
  MONGO_URI: mongodb+srv://supercluster.d83ji.mongodb.net/superData
  MONGO_USERNAME: ${{ vars.MONGO_USERNAME }}
  MONGO_PASSWORD: ${{ secrets.MONGO_PASSWORD }}

jobs:
  unit-testing:
    name: Unit Testing
    strategy:
      matrix:
        nodejs_version: [18, 20]
        operating_system: [ubuntu-latest]
        exclude:
          - nodejs_version: 18
            operating_system: macos-latest
    runs-on: ${{ matrix.operating_system }}
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        run: nvm install ${{ matrix.nodejs_version }}
```

<Callout icon="triangle-alert">
  Never run tests against your production database. Doing so risks data corruption and performance degradation.
</Callout>

***

## 3. Refactoring Strategy

To prevent production downtime, Alice proposed spinning up a dedicated MongoDB service container inside the CI job. This gives each job its own ephemeral database instance, fully isolated from production.

### 3.1 Define a MongoDB Service in GitHub Actions

Add a `services` section under each job to start a MongoDB Docker container:

```yaml theme={null}
jobs:
  unit-testing:
    runs-on: ubuntu-latest
    services:
      mongodb:
        image: mongo:6.0
        ports:
          - 27017:27017
        env:
          MONGO_INITDB_DATABASE: testdb
    steps:
      - uses: actions/checkout@v4
      - name: Wait for MongoDB to start
        run: |
          for i in {1..10}; do
            nc -z localhost 27017 && break
            echo "Waiting for MongoDB…"
            sleep 5
          done
      - name: Install Dependencies
        run: npm install
      - name: Run Unit Tests
        env:
          MONGO_URI: mongodb://localhost:27017/testdb
        run: npm test
```

| Field    | Description                                        |
| -------- | -------------------------------------------------- |
| services | Defines Docker containers to run alongside the job |
| image    | Docker image for the service (e.g., `mongo:6.0`)   |
| ports    | Host-to-container port mappings                    |
| env      | Initialization variables for the container         |

<Callout icon="lightbulb">
  Using an isolated service container ensures your CI jobs are reproducible and safe. You can apply the same pattern for integration tests, Redis, PostgreSQL, and more.
</Callout>

***

## 4. Project Tasks Overview

<Frame>
  ![The image is a project status meeting table listing tasks, their priorities, assigned person (Alice), status, and comments/issues. Some tasks are completed, some are in progress, and others have not started.](https://kodekloud.com/kk-media/image/upload/v1752875956/notes-assets/images/GitHub-Actions-Certification-Project-Status-Meeting-2/project-status-meeting-tasks-table.jpg)
</Frame>

***

## 5. Next Steps

1. Update all testing and coverage jobs to use in-job MongoDB services.
2. Remove production credentials from the global `env` scope.
3. Validate workflow changes on a feature branch before merging to `main`.

Thank you for joining this meeting. Let’s keep our production environment healthy by isolating CI dependencies!

***

## References

* [GitHub Actions: Service containers](https://docs.github.com/en/actions/using-jobs/using-a-service-container)
* [MongoDB Docker Hub](https://hub.docker.com/_/mongo)
* [GitHub Actions Cache](https://docs.github.com/en/actions/advanced-guides/caching-dependencies-to-speed-up-workflows)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/56d72a06-285c-4516-9880-073fb56f579b/lesson/36c349a1-6556-44f0-9d89-3f76f204c271" />
</CardGroup>


# Project Status Meeting 3

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Integration-with-GitHub-Actions/Project-Status-Meeting-3/page

This update covers workflow refactoring, deployment prerequisites, and a primer on Kubernetes fundamentals.

Welcome to the third Project Status Meeting. This update covers our recent workflow refactoring, deployment prerequisites, and a primer on Kubernetes fundamentals.

## Workflow Refactoring: Jobs vs. Service Containers

By decoupling workloads into dedicated **job** and **service** containers, we have achieved:

* **Isolated processing:** Batch tasks no longer compete with live services.
* **Reduced database load:** Production database performance improved significantly.
* **Enhanced reliability:** Scheduled jobs now complete without conflicts.

<Callout icon="lightbulb">
  Using separate containers for one-off jobs helps maintain consistent performance for core microservices.
</Callout>

## Deployment Requirements

Before advancing to the staging and production phases, ensure the following components are in place:

| Requirement         | Description                                     | Example Command                                  |
| ------------------- | ----------------------------------------------- | ------------------------------------------------ |
| Container Registry  | Centralized storage for versioned Docker images | `docker push registry.example.com/myapp:1.0.0`   |
| CI/CD Pipeline      | Automated build, test, and deployment workflows | GitHub Actions, GitLab CI, or Jenkins            |
| Configuration Files | Kubernetes manifests or Helm charts             | `deployment.yaml`, `service.yaml`, `values.yaml` |
| Cluster Access      | kubeconfig and RBAC roles configured            | `kubectl config use-context staging-cluster`     |

<Callout icon="triangle-alert">
  Verify your `kubeconfig` context before running `kubectl apply` to avoid unintended cluster changes.
</Callout>

## Kubernetes Fundamentals

Understanding these core Kubernetes resources will streamline our deployment process:

| Resource Type | Purpose                                 | Example CLI                                    |
| ------------- | --------------------------------------- | ---------------------------------------------- |
| Pod           | Smallest deployable unit                | `kubectl run nginx --image=nginx`              |
| Deployment    | Declarative updates and scaling of pods | `kubectl create deployment web --image=myapp`  |
| Service       | Exposes pods internally or externally   | `kubectl expose deployment web --port=80`      |
| Job           | Runs batch or one-time tasks            | `kubectl create job migrate-db --image=alpine` |

For a deeper dive, refer to [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/).

## Next Steps

Alice’s team will finalize manifest files, conduct staging tests, and prepare for the production rollout. In our next meeting, we’ll review deployment logs, performance metrics, and plan the final cutover.

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/56d72a06-285c-4516-9880-073fb56f579b/lesson/7dd4399d-0808-4c9d-a58e-2a1b3bc38812" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/56d72a06-285c-4516-9880-073fb56f579b/lesson/f2741588-b88e-4fad-a988-194069c75b9f" />
</CardGroup>
