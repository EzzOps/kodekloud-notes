# The GitHub Flow

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Git-and-GitHub-Basics/The-GitHub-Flow/page

Comparison of GitHub Flow and GitFlow branching models, explaining differences, uses, sequences, and guidance for choosing workflows based on release cadence and team needs

This article compares GitHub Flow and GitFlow — two popular Git branching models — and explains when to use each. It preserves the original step-by-step sequences and practical tips so you can pick the right workflow for your team and release cadence.

## Overview

* GitHub Flow is a lightweight, branch-based workflow optimized for continuous delivery and frequent deployments.
* GitFlow is a more structured, release-focused model suited to teams with scheduled releases or multiple supported versions.

Both workflows use branches to isolate work, but they differ in branch types, merge strategies, and release processes.

## GitHub Flow (lightweight, continuous delivery)

GitHub Flow emphasizes simplicity and speed. It's ideal for teams that deploy often and want fast feedback loops.

Core principles:

* Short-lived feature branches created from `main`
* Frequent commits and small pull requests
* Pull requests as the central place for code review, CI checks, and discussion
* Merge to `main` only after approval and passing checks
* Delete feature branches after merging to keep the repo tidy

Typical sequence:

1. Create a new branch from `main` to isolate your work:

```bash theme={null}
git checkout -b feature-branch-name
git commit -m "Description of change"
```

2. Commit frequently on the feature branch as you implement and test changes.

3. Open a pull request to propose the change. Use the PR for code review, CI validation, and discussion. Team members can suggest or push refinements to the same feature branch.

4. Once the PR is approved and all automated checks pass, merge the PR into `main`.

5. Delete the feature branch after merging to keep the repository clean.

This simple cycle — branch, commit, open PR, review, merge, delete — supports fast, repetitive deployments and continuous delivery.

<Callout icon="lightbulb">
  Use continuous integration (CI) to run automated tests on pull requests. If you deploy from `main`, ensure pipeline gates (tests and reviews) are enforced before merging to avoid shipping regressions.
</Callout>

## GitFlow (structured, release-oriented)

GitFlow provides explicit branch types and rules to support release management, hotfixes, and multiple concurrent versions.

Key branches:

* `master` (or `main`): production-ready code
* `develop`: integration branch for ongoing development
* `feature/*`: feature development branches, branched from `develop`
* `release/*`: preparation branches for upcoming releases
* `hotfix/*`: urgent fixes branched from `master`

How GitFlow typically operates:

* Developers create `feature/*` branches from `develop` to implement new functionality.
* When preparing a release, create a `release/*` branch from `develop`. Perform final testing, minor fixes, and version bumping on this branch while new features continue on `develop`.
* Only bug fixes and release-related adjustments go into a `release/*` branch; new major features wait for the next cycle.
* When the release is ready, merge the `release/*` branch into `master` and tag the release. Then merge the `release/*` branch back into `develop` to preserve fixes.
* For critical production issues, create a `hotfix/*` branch from `master`. Apply the fix, then merge it into both `master` (and tag) and `develop`.

## Comparing GitHub Flow vs GitFlow

| Aspect          |                                         GitHub Flow | GitFlow                                                                        |
| --------------- | --------------------------------------------------: | ------------------------------------------------------------------------------ |
| Primary goal    |               Continuous delivery, fast deployments | Structured release management, versioning                                      |
| Main branches   |               `main` + short-lived feature branches | `master`/`main`, `develop`, `feature/*`, `release/*`, `hotfix/*`               |
| Best for        | Teams deploying frequently (trunk-based-style flow) | Teams with scheduled releases or multiple supported versions                   |
| Merge policy    |            PR → merge to `main` after approval & CI | Merges between `feature`, `develop`, `release`, and `master` per release rules |
| Release process |           Typically deploy from `main` continuously | Explicit `release/*` branches with tagging and back-merging                    |
| Complexity      |                                                 Low | Higher — more branch management required                                       |

## When to choose which

Choose GitHub Flow if:

* You practice continuous deployment or delivery.
* You prefer fast, incremental changes and smaller pull requests.
* Your team benefits from less branching overhead and more frequent releases.

Choose GitFlow if:

* Your project requires formal release preparation with versioning.
* You must maintain multiple production versions concurrently (e.g., long-term support).
* You need explicit isolation for release stabilization and QA before production.

<Callout icon="warning">
  If your team prioritizes fast, small releases and continuous deployment pipelines, GitHub Flow is typically the better fit. Choose GitFlow when you need explicit, structured release isolation or must support multiple concurrent production versions.
</Callout>

## Quick tips and best practices

* Keep pull requests small and focused to speed up reviews and reduce merge conflicts.
* Automate quality gates (lint, tests, security scans) in CI for every PR.
* Use feature flags when you need larger or risky changes deployed incrementally.
* Establish a clear branching policy and document merge and release steps for your team.

## Links and references

* [GitHub Flow - GitHub Docs](https://docs.github.com/en/get-started/quickstart/github-flow)
* [A successful Git branching model (GitFlow) — Vincent Driessen](https://nvie.com/posts/a-successful-git-branching-model/)
* [Git basics - Branching and merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
* [Continuous Integration (CI) concepts](https://en.wikipedia.org/wiki/Continuous_integration)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/283f1e98-efc7-4003-9946-920de806da32/lesson/909b7bf0-8232-405f-a559-234ce9f71cd8" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/283f1e98-efc7-4003-9946-920de806da32/lesson/6cb30de2-182e-4a08-aafe-9b0d40cb7295" />
</CardGroup>
