# What is GitHub Actions

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Fundamentals-of-GitHub-Actions/What-is-GitHub-Actions/page

Overview of GitHub Actions native CI/CD and repository automation integrated with GitHub, workflows in YAML, jobs and runners GitHub-hosted or self-hosted

If your organization already hosts code on GitHub, GitHub Actions is a native automation platform that enables you to run CI/CD pipelines and other repository automation directly alongside your code. Instead of introducing a separate CI/CD service, GitHub Actions integrates tightly with repository events, providing a unified experience for building, testing, and deploying applications.

Key benefits at a glance:

* Native integration with GitHub repositories and events.
* Author workflows using declarative YAML files stored in your repo.
* GitHub manages provisioning, scaling, and runner environments (unless you opt for self-hosted).
* Built-in support for multiple operating systems (Ubuntu, Windows, macOS).
* Rich visibility with logs, artifacts, and step-level outputs in the Actions tab.

What you can automate

* Continuous integration: run tests and static analysis on every push and pull request.
* Continuous delivery: publish packages or deploy merged changes to environments.
* Repository tasks: add labels, post comments, assign reviewers, or automate issue triage.
* Releases, package registry workflows, scheduled jobs, and more.

<Frame>
  <img alt="A diagram titled &#x22;GitHub Actions&#x22; showing automated repository actions branching into four categories: Pull Request, Issues, Release, and Registry Package. Each category displays purple icons for related events (e.g., Open, Closed, Merged, Labeled, Locked, Published, Created, Updated)." />
</Frame>

## Core concepts

Understanding these primary building blocks will help you design reliable workflows:

| Concept  | What it is                                                                          | Example                                           |
| -------- | ----------------------------------------------------------------------------------- | ------------------------------------------------- |
| Workflow | A YAML file stored in `.github/workflows` that defines when and how automation runs | `ci.yml` triggered on `push` and `pull_request`   |
| Job      | A collection of steps that run on a runner; jobs default to running in parallel     | `jobs: build:`                                    |
| Step     | A single task inside a job; steps run sequentially within a job                     | `- name: Run tests`                               |
| Runner   | The environment (VM or machine) that executes job steps                             | GitHub-hosted `ubuntu-latest` or a self-hosted VM |

## Example workflow

This minimal example demonstrates a matrix-based job that runs unit tests across multiple OSes:

```yaml theme={null}
name: My Awesome App
on: push
jobs:
  unit-testing:
    name: Unit Testing
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        cmd: [test]
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout
        run: echo Code Checkout
      - name: Install NodeJS - ${{ matrix.os }}
        run: echo Installing NodeJS
      - name: Run Tests
        run: echo npm run ${{ matrix.cmd }}
```

What this example demonstrates:

* The workflow triggers on a `push` event.
* There is a single job `unit-testing` that uses a matrix strategy.
* `runs-on: ${{ matrix.os }}` provisions one runner per OS in the matrix (three runners total).
* Each runner executes steps serially (checkout → install → run tests), while the runners run concurrently.

> **lightbulb** Workflows live in the `.github/workflows` directory of the repository. Each YAML file in that directory defines one workflow and its triggers.

## Runners and execution

A runner is the execution environment for jobs. GitHub Actions will provision runners based on `runs-on`. For the example above, GitHub creates three runners and runs the same job concurrently across them. You can monitor job logs, artifacts, and step outputs through the repository's Actions tab in the GitHub UI. These logs are invaluable for debugging and verifying CI/CD runs.

<Frame>
  <img alt="A presentation slide showing GitHub Actions workflows and runners. The left side displays the Actions UI with multiple &#x22;Unit Testing&#x22; jobs, and the right side has diagrams of GitHub-hosted runners (Windows, Ubuntu, macOS) performing steps like Clone Repo, Install NodeJS, and Run Tests." />
</Frame>

## Runner types — GitHub-hosted vs Self-hosted

Choose a runner type based on control, compliance, and cost:

| Runner type   | Pros                                                                    | Cons                                        | Typical use cases                                        |
| ------------- | ----------------------------------------------------------------------- | ------------------------------------------- | -------------------------------------------------------- |
| GitHub-hosted | Fresh VM for every job, maintained by GitHub, no machine management     | Limited persistence, usage quotas may apply | Standard CI builds, public projects, fast onboarding     |
| Self-hosted   | Full control, install custom or proprietary software, persistent caches | You manage security, maintenance, scaling   | Heavy builds, specialized hardware, private dependencies |

Practical differences:

* GitHub-hosted runners provide clean images with preinstalled common tools, but you cannot make system-level persistent changes across jobs.
* Self-hosted runners run on your infrastructure (on-prem or cloud) and allow customizations, privileged access, and long-lived caches. They require you to handle maintenance and scaling.

When to choose which:

* Use GitHub-hosted for general CI/CD workloads to reduce maintenance overhead.
* Use self-hosted for complex builds requiring GPUs, legacy tools, private network access, or when compliance requires on-prem execution.

<Frame>
  <img alt="An infographic slide titled &#x22;Runner Types&#x22; that compares GitHub-hosted runners (green panel) with self-hosted runners (orange panel), listing features and icons for each. Buttons labeled Workflow, Jobs, Steps, and Runners appear along the bottom." />
</Frame>

## Next steps & resources

To deepen your knowledge and start authoring workflows, check these resources:

* GitHub Actions documentation: [https://docs.github.com/actions](https://docs.github.com/actions)
* GitHub Actions workflow syntax: [https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
* CI/CD concepts and best practices: [https://docs.github.com/actions/learn-github-actions/introduction-to-github-actions](https://docs.github.com/actions/learn-github-actions/introduction-to-github-actions)

Summary

* GitHub Actions provides a flexible, integrated automation platform that supports CI/CD and many other repository automations.
* Workflows are defined in YAML files under `.github/workflows`.
* Jobs run on runners (GitHub-hosted or self-hosted), with steps executing sequentially inside jobs.
* Choose runner types based on control, security, and resource requirements.

That's all for now.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/7d6172e9-5a43-4701-9feb-e4cfdb65b256/lesson/f4a99186-571a-4774-a391-be03822efaf6)
