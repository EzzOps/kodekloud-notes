# Basics of CICD

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Migration-Overview/Basics-of-CICD/page

Explains Continuous Integration and Continuous Deployment workflows, branching, pipelines, best practices, and CD options to automate building, testing, and deploying code.

In this lesson we cover the essentials of Continuous Integration (CI) and Continuous Deployment/Delivery (CD), and how they integrate into a typical Git-based development workflow.

Git repositories—hosted on platforms such as [Gitea](https://gitea.io/), [GitHub](https://github.com/), [GitLab](https://gitlab.com/), or [Bitbucket](https://bitbucket.org/)—act as the single source of truth for your codebase. Although examples below reference Gitea, the CI/CD concepts, patterns, and pipeline stages apply to any Git hosting provider and CI system.

## Typical branching model and pull requests

A common branching workflow looks like this:

* The production-ready line of development lives on the `main` (historically `master`) branch. Code on `main` is what gets deployed to production.
* New work happens on feature branches such as `feature/A` or `feature/B`. Feature branches isolate changes until they are ready.
* When a feature is ready, a developer pushes commits to the feature branch and opens a pull request (PR) to merge into `main`.
* Reviewers inspect the PR and CI pipelines typically run automatically to validate the changes before merge.

Using this model encourages small, frequent merges and minimizes long-lived diverging branches.

## Why CI is necessary

Without Continuous Integration, teams commonly face:

* Delayed testing: Tests run late, often after multiple changes are merged, making root-cause analysis harder.
* Inefficient deployments: Manual steps across environments (dev, staging, prod) increase the chance of configuration drift and human error.
* Lower quality assurance: Heavy reliance on manual verification causes bottlenecks and inconsistent coverage.

CI automates build, test, and validation steps for every change, catching integration issues early and improving release confidence.

## A typical CI flow (feature branch → PR → merge)

A typical CI workflow for a single feature might look like:

1. Developer 1 creates `feature/A`, implements changes, and pushes commits.
2. A pull request is opened to merge `feature/A` into `main`.
3. A CI pipeline is triggered for the PR. Common stages:
   * Unit tests
   * Dependency and license scanning
   * Build artifact creation
   * Static analysis and vulnerability scanning
   * Optional: container image build and push to a registry
4. CI systems often run tests against a simulated merge commit (feature branch merged into `main`) to catch integration issues early.
5. If tests fail, the developer updates `feature/A` and pushes new commits. The CI pipeline re-runs until it passes.
6. Once CI succeeds, reviewers approve the PR and it is merged into `main`.
7. A `main` pipeline runs after merge. This pipeline may:
   * Produce canonical release artifacts
   * Run additional integration or end-to-end tests
   * Prepare deployment packages for CD

Running CI both for PRs and for `main` serves complementary purposes: PR pipelines validate proposed changes in isolation (or via merge simulation), while `main` pipelines validate the actual post-merge state and produce the artifacts used for deployment.

## Parallel work and integration

* Multiple developers can work in parallel on different feature branches (`feature/A`, `feature/B`).
* Each feature branch triggers its own PR pipeline.
* After both branches are merged, `main` now contains changes from both features. The `main` CI pipeline ensures the combined changes build and pass tests together.

This frequent integration and automated verification is the core of Continuous Integration: enabling parallel work while reducing integration risk.

> **lightbulb** Continuous Integration is primarily about frequent automated builds and tests that validate integrations early and often, reducing the chance that defects reach production.

## CD: Continuous Deployment vs Continuous Delivery

CD refers to the pipeline that takes validated CI artifacts through environments and into production. There are two common variants:

| CD Mode               | Description                                                                                       | Typical use case                                                                  |
| --------------------- | ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Continuous Deployment | Successful CI on `main` automatically deploys artifacts to production with no human intervention. | High-release-frequency teams with strong automated testing and observability.     |
| Continuous Delivery   | CI produces deployable artifacts, but a manual approval (a gate) is required before production.   | Teams needing compliance checks, coordinated releases, or extra human validation. |

A practical CD workflow that balances safety and speed often follows these steps:

1. After a successful PR CI run, optionally deploy the feature branch or the merge result to a staging/dev environment.
2. Run integration, smoke, or end-to-end tests in that environment.
3. If tests pass, merge the PR. The `main` CI verifies the merged state and triggers the CD pipeline.
4. The CD pipeline deploys to staging and either:
   * Automatically promotes to production (Continuous Deployment), or
   * Waits for manual approval before promoting to production (Continuous Delivery).

The manual approval step is valuable when compliance, coordination of large changes, or an additional human sanity check is required.

## Recommended CI pipeline stages (example)

* checkout code
* install dependencies / cache dependencies
* run unit tests (fast feedback)
* run linting / static analysis
* run integration/e2e tests (can be staged)
* build and tag artifacts (e.g., Docker images)
* push artifacts to registry / store release artifacts
* run vulnerability scans and policy checks
* deploy to staging (optional) and run smoke tests

Breaking stages into fast and slow categories helps provide rapid feedback to developers while keeping longer-running tests as gate checks.

## Best practices and tips

* Keep PRs small and focused—smaller changes reduce review time and make CI faster.
* Run fast feedback (unit tests, linters) first, then long-running tests (integration, e2e).
* Use branch protections to require passing CI and at least one review before merging `main`.
* Make pipeline logs and failure messages clear to speed up debugging.
* Automate rollbacks and canary deployments in production to reduce blast radius.
* Cache dependencies and split workloads to optimize CI runtime and cost.

## Summary

* CI automates building and testing on feature branches and PRs to detect integration issues early.
* CI runs both on PRs (to validate proposed changes) and on `main` after merge (to validate the canonical state and produce artifacts).
* CD moves validated artifacts through environments (staging → production). It can be fully automated (Continuous Deployment) or require a manual approval before production (Continuous Delivery).
* Together, CI and CD help teams deliver higher-quality software faster and with less operational risk.

Apply these patterns and adapt pipeline stages, approval gates, and environments to your team’s risk tolerance and release cadence.

## Links and references

* [Gitea](https://gitea.io/)
* [GitHub](https://github.com/)
* [GitLab](https://gitlab.com/)
* [Bitbucket](https://bitbucket.org/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/c8922198-0dcd-4910-9545-21e08f8a847c/lesson/11ac32ad-d4aa-441d-aefb-d703263ef226)
