# Introduction to the GitHub Actions Importer

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Introduction-to-the-GitHub-Actions-Importer/page

Explains the GitHub Actions Importer, a Dockerized GitHub CLI tool that automates migrating CI/CD pipelines from various platforms while analyzing, converting, auditing, and forecasting runtime and costs.

What is the GitHub Actions Importer?

The GitHub Actions Importer is a migration utility that simplifies moving CI/CD pipelines into GitHub Actions. It automates much of the conversion work so teams can consolidate builds, tests, and deployments inside the GitHub ecosystem while reducing manual effort and human error.

Supported source platforms

| Source platform                                                         | Typical use case                                |
| ----------------------------------------------------------------------- | ----------------------------------------------- |
| [Azure DevOps](https://azure.microsoft.com/services/devops/)            | Enterprise pipelines with Azure integrations    |
| [Bamboo](https://www.atlassian.com/software/bamboo)                     | Atlassian-hosted build plans and deployments    |
| [Bitbucket Pipelines](https://bitbucket.org/product/features/pipelines) | Bitbucket-native CI/CD workflows                |
| [CircleCI](https://circleci.com)                                        | Cloud-first pipelines with Docker-centric jobs  |
| [GitLab](https://gitlab.com)                                            | Full-featured pipelines and self-hosted runners |
| [Jenkins](https://www.jenkins.io)                                       | Highly customizable, plugin-driven builds       |
| [Travis CI](https://travis-ci.com)                                      | Legacy hosted CI pipelines                      |

Key features and how they help

* GitHub CLI extension: works as an extension to the [GitHub CLI](https://cli.github.com), enabling a scriptable, familiar command-line experience for creating and managing migrations.
* Docker-based execution: runs the migration tooling inside [Docker](https://www.docker.com) containers to ensure consistent, isolated, and secure execution across environments.
* Pipeline analysis and conversion: analyzes existing CI/CD configuration files to generate a migration plan and scaffold GitHub Actions workflows.
* Audit and forecasting: evaluates pipeline complexity and estimates future GitHub Actions runtime and concurrency so you can project capacity and cost before completing migration.

<Frame>
  <img alt="A presentation slide titled &#x22;Key Features and Functionality&#x22; showing four feature cards: CLI Extension, Docker-Based, Migration Support, and Audit & Forecast, each with a colorful icon and a short description. The cards highlight a command-line interface, containerized execution, CI/CD migration support, and complexity/usage evaluation." />
</Frame>

Audit and forecasting

The importer's audit tools estimate projected GitHub Actions runtime and concurrency consumption. Use these forecasts to plan runner capacity, concurrency limits, and cost implications before you finalize a migration strategy.

Conversion accuracy and next steps

The importer often converts approximately 80% of a typical pipeline automatically. Actual conversion rates depend on pipeline complexity, custom integrations, and platform-specific features (for example, proprietary plugins, in-house scripts, or specialized deployment targets). Any generated workflow should be reviewed, tested, and adjusted before being used in production.

> **lightbulb** Always inspect and test generated workflows. Automated conversions frequently require manual changes for `secrets` handling, environment setup, or custom steps. Refer to the GitHub Actions security and secrets docs when migrating sensitive data.

Links and references

* [GitHub Actions](https://github.com/features/actions) — official product page
* [GitHub CLI](https://cli.github.com) — command-line integration for the importer
* [Docker](https://www.docker.com) — runtime used for isolated migration tasks
* [GitHub Actions: Encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) — guidance for secrets management during migration

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/d81972b2-aae1-4631-8f2f-f94b48451e4e)
