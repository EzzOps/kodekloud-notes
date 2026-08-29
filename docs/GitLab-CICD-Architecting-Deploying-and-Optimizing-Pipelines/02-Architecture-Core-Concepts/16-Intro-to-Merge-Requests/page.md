# Intro to Merge Requests

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Architecture-Core-Concepts/Intro-to-Merge-Requests/page

GitLab Merge Requests facilitate collaborative development by allowing teams to propose, review, and integrate code changes between branches.

GitLab Merge Requests (MRs) are the cornerstone of collaborative development in GitLab. They enable teams to propose, review, and integrate code changes from one branch into another. While MRs serve the same purpose as [GitHub Pull Requests](https://docs.github.com/en/pull-requests), they use different terminology and offer seamless integration with GitLab’s built-in CI/CD.

## What Is a Merge Request?

A Merge Request lets you:

* Propose changes from a **source branch** to a **target branch** (typically `main` or `master`).
* Collaborate through comments, inline code discussions, and approvals.
* Enforce quality gates by requiring passing CI/CD pipelines before merging.

> **lightbulb** Give your Merge Request a clear title and description. Assign reviewers early to accelerate feedback.

## GitLab vs. GitHub: Core Concepts

| Concept               | GitLab Merge Request                                                                      | GitHub Pull Request                                              |
| --------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Feature Name          | Merge Request                                                                             | Pull Request                                                     |
| Default Target Branch | `main` (configurable)                                                                     | `main` (or `master`)                                             |
| CI/CD Integration     | Built-in [GitLab CI/CD pipelines](https://docs.gitlab.com/ee/ci/)                         | External or [GitHub Actions](https://docs.github.com/en/actions) |
| Draft Mode            | [Work in Progress MR](https://docs.gitlab.com/ee/user/project/merge_requests/drafts.html) | Draft Pull Request                                               |

Despite these differences, both platforms follow a similar review workflow:

1. Create a feature branch
2. Commit your code
3. Submit for review
4. Discuss and revise
5. Merge into the main codebase

## Typical Merge Request Workflow

### 1. Create a Feature Branch

```bash theme={null}
git checkout -b feature-xyz
```

### 2. Develop and Commit Changes

```bash theme={null}
