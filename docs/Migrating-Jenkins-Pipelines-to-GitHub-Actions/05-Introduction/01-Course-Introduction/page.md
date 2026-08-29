# Using a tag (recommended for controlled versioning)
- name: Checkout
  uses: actions/checkout@v3.6.0
```

```yaml theme={null}
# Using a branch (tracks the latest on that branch)
- name: Checkout
  uses: actions/checkout@main
```

```yaml theme={null}
# Using a commit SHA (most stable / immutable)
- name: Checkout
  uses: actions/checkout@[AWS_SECRET_ACCESS_KEY]
```

SHAs are immutable, making them the most dependable choice for reproducible workflows. Many teams adopt a practical compromise: pin to a stable major tag (for example `@v3`) or a specific release tag (for example `@v3.6.0`) and then periodically update to a new tag or SHA after validating the action in a test environment.

## Best practices

* Pin actions to a tag or SHA to avoid unexpected changes in CI.
* Prefer actions from verified authors or well-known maintainers.
* Review action source code (or vendor internal copies) for how secrets and repository data are handled.
* Use least-privilege permissions for workflow tokens and secrets; avoid granting excessive access to third-party actions.

## Links and references

* [GitHub Marketplace — Actions](https://github.com/marketplace/actions)
* [GitHub Actions documentation](https://docs.github.com/actions)

Additional security considerations for actions and workflows will be covered later in this course.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/7d6172e9-5a43-4701-9feb-e4cfdb65b256/lesson/0a458dc3-9238-429c-bf5b-ff7cff304726" />
</CardGroup>


# Course Introduction

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Introduction/Course-Introduction/page

Guide to migrating CI/CD pipelines from Jenkins to GitHub Actions with practical patterns, examples, secrets handling, tooling, and hands-on labs to modernize workflows

In this lesson you will learn how to migrate CI/CD workflows from Jenkins to GitHub Actions. This course is built to help teams move from legacy Jenkins pipelines to modern, GitHub-native workflows with minimal friction.

What you'll gain:

* Practical, hands-on labs to experiment and learn by doing.
* Clear migration patterns and real-world examples to convert Jenkins jobs into GitHub Actions workflows.
* Strategies for handling secrets, artifacts, plugins, and environment variables during migration.

Welcome to the [Jenkins to GitHub Actions migration course](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions). I'm Siddharth, and I’ll walk you through migrating pipelines, mapping constructs, and automating repetitive steps.

<Frame>
  <img alt="A presentation slide titled &#x22;Pipeline Definition&#x22; comparing Jenkins and GitHub Actions with colored bars and icons. It lists three comparison points (Groovy/Jenkinsfile vs YAML, pipeline storage/versioning, and plugins vs built‑in integrations) and shows a presenter in a small video thumbnail at the bottom-right." />
</Frame>

We’ll cover the pros and cons of each platform, key differences you need to be aware of, and common migration pitfalls to avoid.

## Why migrate from Jenkins to GitHub Actions

* Native integration with GitHub repositories, pull requests, and the Actions Marketplace.
* Workflows defined in YAML stored in the repository for visibility and versioning.
* Reduced operational overhead — no need to manage Jenkins masters or plugin compatibility.
* Flexible runners: use GitHub-hosted runners or self-hosted runners for custom workloads.

## Course structure (what we'll cover)

1. Jenkins fundamentals and what to migrate
2. GitHub Actions basics and YAML workflow patterns
3. Mapping Jenkins pipeline constructs to Actions jobs/steps
4. Handling secrets, artifacts, and environment variables
5. Tools and automation to accelerate migration
6. Labs: migrate a simple pipeline, then a complex pipeline with plugins and conditional logic

<Callout icon="lightbulb">
  Before you begin, ensure you have:

  * Access to the source Jenkins pipelines (Jenkinsfile or job configuration).
  * A GitHub repository where you can store workflows (`.github/workflows/`).
  * Permissions to create Actions and add secrets in the target repository.
</Callout>

## Deep dive: Jenkins — what to look for

When assessing Jenkins pipelines, inventory:

* Pipeline type: Declarative or Scripted (Groovy).
* Steps that call shell commands, invoke Docker, or use specific plugins.
* How secrets and credentials are stored (Jenkins credentials store).
* Artifact storage locations (Nexus, Artifactory, S3).
* Custom plugins that may not have direct GitHub Action equivalents.

Example Jenkins pipeline (Declarative):

```groovy theme={null}
// Jenkins (Declarative Pipeline)
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'make build'
      }
    }
    stage('Test') {
      steps {
        sh 'make test'
      }
    }
  }
}
```

Quick job run result example:

```text theme={null}
Results - <1s
> Job completed at Tue May 20 12:59:51 UTC 2025 — Print Message
```

<Callout icon="warning">
  Important: Jenkins plugins may implement complex behavior (credential masking, custom credential types, or specialized SCM integrations). When a plugin lacks an Actions equivalent, plan for manual translation or replacement with a community GitHub Action or a small custom action.
</Callout>

## GitHub Actions fundamentals

GitHub Actions uses YAML workflows stored in `.github/workflows/`. Workflows are composed of jobs, each running on a runner (`runs-on`) and containing steps. Steps can use actions from the Marketplace or run arbitrary shell commands.

Minimal, complete CI workflow example:

```yaml theme={null}
name: CI
