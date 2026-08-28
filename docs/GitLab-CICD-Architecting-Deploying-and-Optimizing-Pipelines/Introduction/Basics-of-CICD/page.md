# .gitlab-ci.yml
unit-testing:
  tags:
    - ubuntu-latest
  script:
    - echo "Running unit tests on Ubuntu"
```

## 2. Default Containers for SAST Runners

GitLab’s SAST runners come pre-configured with a Ruby 3.1 image. This is ideal for Ruby projects but can lead to errors if used for other languages:

```yaml theme={null}
# .gitlab-ci.yml
workflow:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

sast-unit-test:
  tags:
    - sast-linux-small-amd64
  script:
    - ruby --version
    - bundle install
    - bundle exec rspec
```

## 3. Installing Custom Runtimes

When you need a language runtime not in the default image—such as Node.js 20—you can install it during `before_script`. This adds pipeline time and may increase CI minutes usage.

<Callout icon="lightbulb">
  Installing additional packages in `before_script` can slow down your pipelines. Consider using a custom image (see next section) for faster, repeatable builds.
</Callout>

```yaml theme={null}
# .gitlab-ci.yml
workflow:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

node-test:
  tags:
    - sast-linux-small-amd64
  before_script:
    - apt-get update && apt-get install -y curl gnupg
    - curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    - apt-get install -y nodejs
  script:
    - npm install
    - npm test
```

## 4. Using Dedicated Docker Images

Specifying an image lets GitLab pull a pre-built container with your desired tools. This ensures consistency and speeds up jobs by eliminating runtime installation steps.

```yaml theme={null}
# .gitlab-ci.yml
workflow:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

node-test:
  tags:
    - linux
  image: node:20-alpine3.17
  script:
    - npm install
    - npm test
```

Docker Container - node:20-alpine3.17

1. Checkout Code – 2s
2. Install Dependencies – 3m
3. Run Tests – 5m

### Comparison: Before vs. After Using an Image

| Configuration         | Installation Steps                 | Pipeline Duration | Maintenance Overhead |
| --------------------- | ---------------------------------- | ----------------- | -------------------- |
| Custom Runtime in Job | Update OS, add repos, install Node | High              | High                 |
| Docker Image          | Pull pre-built container           | Low               | Low                  |

## 5. Avoid Hitting Production Dependencies

<Callout icon="triangle-alert">
  Running tests against your production database can degrade performance and expose sensitive data. Always use a separate test database or service container for CI tasks.
</Callout>

## 6. Using Service Containers

Service containers run alongside your job’s main container in the same network. Use them for databases, caches, or any supporting service:

```yaml theme={null}
# .gitlab-ci.yml
workflow:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

integration-test:
  tags:
    - linux
  image: node:20-alpine3.17
  services:
    - name: siddarth67/mongo-db:non-prod
      alias: mongo
  variables:
    MONGO_URI: "mongodb://mongo:27017/db"
  script:
    - npm install
    - npm test
```

When this job runs, GitLab launches two containers on a shared bridge network:

1. **mongo** (alias): MongoDB service with test data
2. **Job container**: Checks out code, installs dependencies, and runs tests against `mongodb://mongo:27017/db`

## Summary

By combining runner tags, Docker images, and service containers, you can build CI/CD pipelines that are:

* Isolated and reproducible
* Fast and cost-effective
* Configurable per-project requirements

## Links and References

* [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
* [Docker Hub: node](https://hub.docker.com/_/node)
* [NodeSource Node.js Binaries](https://github.com/nodesource/distributions)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/3a1c2306-8091-4dfe-b40f-e2ca53918553/lesson/18021019-745f-4240-b254-428200696166" />
</CardGroup>


# Basics of CICD

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Introduction/Basics-of-CICD/page

This article explains the key concepts of Continuous Integration and Continuous Delivery/Deployment, emphasizing their importance in modern software engineering.

In this lesson, we’ll cover the key concepts of Continuous Integration (CI) and Continuous Delivery/Deployment (CD), explore a typical Git-based workflow, and highlight why CI/CD is vital for modern software engineering.

***

## 1. A Typical Git Workflow

All source code is maintained in a Git repository, usually hosted on platforms like GitLab, GitHub, or Bitbucket. Collaboration features—such as Merge Requests (MRs), pipelines, and permission controls—streamline team workflows.

1. Developers branch off the protected **main** branch to create isolated **feature branches**.
2. They commit and push changes to their feature branch.
3. An MR is opened to merge the feature into **main**, triggering code review.
4. After approvals, changes merge into **main** and deploy to the target environment.

<Callout icon="lightbulb">
  Enable branch protection on **main** to require MRs and automated checks before merging.
</Callout>

Without CI/CD automation, manual testing and deployments introduce risks:

| Risk                  | Impact                                       |
| --------------------- | -------------------------------------------- |
| No guaranteed testing | Bugs slip into production                    |
| Manual errors         | Misconfigurations, inconsistent environments |
| Slow feedback loops   | Delayed fixes and longer release cycles      |

<Frame>
  ![The image is a diagram explaining the CI/CD process, showing the flow from feature branch creation to deployment and production, including steps like commit, pull request, review, and approval.](https://kodekloud.com/kk-media/image/upload/v1752877294/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Basics-of-CICD/ci-cd-process-diagram-flow.jpg)
</Frame>

***

## 2. Challenges of Manual Integration

When multiple developers merge without CI pipelines, teams often face:

| Challenge           | Description                                                            |
| ------------------- | ---------------------------------------------------------------------- |
| Delayed Testing     | QA happens post-merge, making bug isolation and fixes more difficult.  |
| Inefficient Deploys | Manual steps across dev, staging, and production increase error rates. |
| QA Bottlenecks      | Manual quality checks slow down releases and risk missing regressions. |

<Frame>
  ![The image illustrates a workflow for continuous integration, highlighting the process from feature branches to production, and emphasizes the challenges of delayed testing, inefficient deployment, and quality assurance without CI.](https://kodekloud.com/kk-media/image/upload/v1752877295/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Basics-of-CICD/ci-workflow-feature-branches-production.jpg)
</Frame>

***

## 3. Introducing Continuous Integration

Continuous Integration ensures that every code change is automatically tested and validated before merging into **main**.

1. Developer 1 branches off **main** to work on **feature-A**.
2. Opening an MR triggers the CI pipeline, which performs:
   * Unit tests
   * Dependency and license scans
   * Artifact builds
   * Static code analysis and vulnerability scanning
3. If any stage fails, the MR remains open for fixes; pushing new commits retriggers CI.
4. On passing all checks, the MR is approved and merged into **main**.
5. A post-merge pipeline runs integration tests against the updated **main** branch.

Meanwhile, Developer 2 works on **feature-B** in parallel. Once feature-B’s MR passes CI and merges, the post-merge pipeline verifies that A and B integrate without conflict, keeping **main** stable and healthy.

<Callout icon="lightbulb">
  Fast feedback from CI pipelines helps catch issues early and reduces merge conflicts.
</Callout>

<Frame>
  ![The image illustrates a continuous integration workflow, showing steps from feature branching and committing to production, including unit testing, dependency scanning, building artifacts, and code scanning.](https://kodekloud.com/kk-media/image/upload/v1752877296/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Basics-of-CICD/continuous-integration-workflow-diagram.jpg)
</Frame>

***

## 4. From Integration to Delivery and Deployment

Once CI validates code quality, CD automates the path to production:

| Process               | Deployment Target              | Human Gate Required | Typical Use Case            |
| --------------------- | ------------------------------ | ------------------- | --------------------------- |
| Continuous Delivery   | Non-production (e.g., staging) | Yes                 | Manual approval before prod |
| Continuous Deployment | Production                     | No                  | Fully automated releases    |

1. **Continuous Delivery**
   * Deploys to staging or QA environments.
   * Executes integration, performance, and end-to-end tests.
   * Awaits manual approval for production.

2. **Continuous Deployment**
   * Automatically deploys to production after successful CI.
   * Ideal for teams with mature test suites and low risk tolerance.

<Callout icon="triangle-alert">
  Skipping manual approvals in CD demands comprehensive automated tests to prevent production incidents.
</Callout>

<Frame>
  ![The image illustrates a continuous deployment/delivery pipeline, showing the process from feature branch creation to production deployment, including stages like commit, pull request, review, CI/CD, and testing. It includes elements like unit testing, dependency scanning, and code scanning, with paths for both continuous deployment and delivery.](https://kodekloud.com/kk-media/image/upload/v1752877298/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Basics-of-CICD/continuous-deployment-pipeline-diagram.jpg)
</Frame>

***

## Summary

* **Continuous Integration (CI)** automates testing and validation for every code change.
* **Continuous Delivery (CD)** adds automated deployments to staging with a human gate.
* **Continuous Deployment** fully automates production releases.

Together, CI/CD accelerates release cycles, ensures higher software quality, and minimizes operational risks.

***

## Links and References

* [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
* [Continuous Integration on Wikipedia](https://en.wikipedia.org/wiki/Continuous_integration)
* [DevOps Practices](https://en.wikipedia.org/wiki/DevOps)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/75db752f-09a3-4df6-a1ac-3a1fa506eb65/lesson/1cd42fab-5c47-448e-a4f5-a64e5b46cdda" />
</CardGroup>
