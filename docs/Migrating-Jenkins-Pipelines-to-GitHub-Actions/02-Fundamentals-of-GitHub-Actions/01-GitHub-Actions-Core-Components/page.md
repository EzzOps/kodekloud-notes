# GitHub Actions Core Components

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Fundamentals-of-GitHub-Actions/GitHub-Actions-Core-Components/page

Overview of GitHub Actions core components including workflows, jobs, steps, and reusable actions with examples and a quick reference for designing CI/CD automation

Explore the core components of GitHub Actions and how they fit together. This guide clarifies workflows, jobs, steps, and actions with a compact example and a quick reference table to help you design CI/CD automation in your repository.

## Core concepts

GitHub Actions consists of three primary building blocks:

* Workflows — define when and how automation runs.
* Jobs — independent units of work within a workflow that execute on a runner.
* Steps — sequential tasks inside a job that call actions or run commands.

### Workflow

A workflow is an automated process defined in a YAML file stored in your repository under `.github/workflows`. A repository may contain multiple workflows. Each workflow runs in response to one or more events (triggers) and can include an optional `name` that appears in the Actions tab.

> **lightbulb** Workflow definition files live in the `.github/workflows` directory of your repository.

### Jobs

Jobs are the units inside a workflow. A workflow can contain one or more jobs. Each job runs on a runner (GitHub-hosted or self-hosted). Specify the runner using the `runs-on` attribute (for example, `runs-on: ubuntu-latest`).

### Steps

Steps are the atomic operations within a job. Steps execute sequentially on the job's runner. A step can:

* Use an action via `uses:` (reusable component).
* Run shell commands with `run:`.

## Example workflow

This example illustrates a workflow with a job that runs unit tests on push events.

```yaml theme={null}
name: My Awesome App
on: push
jobs:
  unit-testing:
    name: Unit Testing
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Install NodeJS
        uses: actions/setup-node@v3
        with:
          node-version: 20

      - name: Install Dependencies
        run: npm install

      - name: Run Unit Tests
        run: npm test
```

Explanation of the example:

* `on: push` — triggers the workflow for `push` events.
* `unit-testing` — job identifier; `name: Unit Testing` is the display name.
* `runs-on: ubuntu-latest` — uses a GitHub-hosted Ubuntu runner.
* Steps (executed in order):
  * Checkout: `actions/checkout@v3` fetches the repository.
  * Install NodeJS: `actions/setup-node@v3` configures Node.js (`node-version: 20`).
  * Install Dependencies: runs `npm install`.
  * Run Unit Tests: runs `npm test`.

## Quick reference table

| Component | Purpose                                     | Example                                        |
| --------- | ------------------------------------------- | ---------------------------------------------- |
| Workflow  | Defines the automation and triggers         | `on: push`                                     |
| Job       | A group of steps that runs on a runner      | `runs-on: ubuntu-latest`                       |
| Step      | A single task in a job (runs sequentially)  | `run: npm test` or `uses: actions/checkout@v3` |
| Action    | Reusable automation component used by steps | `uses: actions/setup-node@v3`                  |

## Actions (reusable components)

Actions are modular, reusable components that simplify automation tasks. You can author your own actions or consume community and official ones from GitHub Marketplace.

Common use cases for actions:

* Building and pushing Docker images to registries.
* Provisioning or managing cloud resources (e.g., Azure AKS).
* Fetching secrets from HashiCorp Vault using [`hashicorp/vault-action`](https://github.com/hashicorp/vault-action).

Examples:

* Build and push Docker images: action that builds an image and pushes to Docker Hub or a container registry.
* Azure integrations: actions for creating and managing [Azure Kubernetes Service](https://learn.kodekloud.com/user/courses/azure-kubernetes-service) resources.
* Secrets management: `hashicorp/vault-action` for injecting secrets as environment variables.

<Frame>
  <img alt="A slide titled &#x22;GitHub Actions&#x22; showing three numbered workflow steps. The steps are: 1) Build and push Docker images, 2) Create AKS Cluster, and 3) Consume Vault Secrets, each with corresponding Docker/Azure/Vault icons." />
</Frame>

Triggers/events, runners, and advanced action patterns (composite actions, JavaScript and Docker actions, permissions) are covered in more detail elsewhere.

## Links and references

* [GitHub Actions documentation](https://docs.github.com/actions)
* [GitHub Marketplace - Actions](https://github.com/marketplace?type=actions)
* [hashicorp/vault-action](https://github.com/hashicorp/vault-action)
* [Azure Kubernetes Service (AKS) course](https://learn.kodekloud.com/user/courses/azure-kubernetes-service)

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/7d6172e9-5a43-4701-9feb-e4cfdb65b256/lesson/033a5dc3-36d5-431f-a660-d563c983761e)
