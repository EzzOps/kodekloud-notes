# Controls when the workflow will run
on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

# Allows you to run this workflow manually from the Actions tab
workflow_dispatch:

jobs:
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks executed as part of the job
    steps:
      # Checks out your repository under $GITHUB_WORKSPACE, so your job can access it
      - name: Checkout repository
        uses: actions/checkout@v4

      # Example: set up Node.js, install dependencies, run tests
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "18"

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test
```

## Mapping Jenkins concepts to GitHub Actions

The following table summarizes common Jenkins concepts and their GitHub Actions equivalents to help plan your migration.

| Jenkins concept                    | GitHub Actions equivalent                                     | Notes / Example                                                               |
| ---------------------------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Jenkinsfile (Groovy)               | Workflow YAML (`.github/workflows/*.yml`)                     | Convert Declarative stages to jobs/steps.                                     |
| Agent (`agent any` / Docker agent) | `runs-on` and container support (`container:`)                | Use `container:` for running steps inside a container.                        |
| Credentials / Secret Text          | GitHub Secrets (`Settings → Secrets and variables → Actions`) | Access via `secrets.MY_SECRET` in workflows.                                  |
| Plugins (e.g., Slack, Artifactory) | Marketplace Actions or API calls                              | Many integrations exist; otherwise call vendor APIs.                          |
| Multi-branch jobs                  | `on: pull_request` / branch filters in `on:`                  | Branch filters and PR triggers are built-in.                                  |
| Post-build actions                 | Separate jobs triggered by `needs:` or `if:` conditions       | Use `needs:` to control job order and `if:` expressions for conditional runs. |

## Example: Jenkins -> GitHub Actions direct conversion

Given the Jenkins Declarative pipeline above, the equivalent GitHub Actions workflow looks like:

```yaml theme={null}
# GitHub Actions equivalent
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Build
        run: make build

      - name: Test
        run: make test
```

This straightforward mapping covers many simple pipelines. For pipelines with parallel stages, credentials, or specialized plugins, you’ll expand jobs, use `needs` for dependencies, and reference `secrets` or marketplace actions.

## Tools and automation to accelerate migration

There are community and vendor tools that can assist in converting Jenkins pipelines or exporting job definitions, but results vary depending on pipeline complexity.

Key utilities and approaches:

* Use the GitHub Marketplace to find Actions that replace Jenkins plugins.
* Employ the `gh` CLI to create workflows, manage secrets, and interact with repos programmatically.
* For large fleets, write scripts to translate common patterns (e.g., shell steps) into YAML templates you can reuse.

Install or update the GitHub CLI (`gh`) using one of these package managers:

```bash theme={null}
# Homebrew (macOS / Linux)
brew install gh
brew upgrade gh

# MacPorts (macOS)
sudo port selfupdate
sudo port install gh

# Conda
conda install -c conda-forge gh
conda update -c conda-forge gh
```

Useful `gh` commands:

* `gh auth login` — authenticate to GitHub.
* `gh secret set` — add repository secrets.
* `gh repo clone` / `gh workflow` — manage workflows and repos from scripts.

## Migration checklist

* [ ] Inventory all Jenkins jobs, pipelines, and plugins.
* [ ] Identify secrets and set them in GitHub Actions secrets.
* [ ] Map artifact stores and update publishing steps (e.g., to S3, Artifactory).
* [ ] Convert build and test steps to Actions jobs/steps.
* [ ] Replace or reimplement plugin functionality with Marketplace Actions or API calls.
* [ ] Create tests and smoke checks in GitHub Actions before decommissioning Jenkins.

## Links and references

* [GitHub Actions documentation](https://docs.github.com/en/actions)
* [GitHub Marketplace](https://github.com/marketplace)
* [GitHub CLI (`gh`)](https://cli.github.com/)
* [Jenkins documentation](https://www.jenkins.io/doc/)

At the end of this course you’ll be able to confidently migrate Jenkins pipelines to GitHub Actions, reduce operational overhead, and modernize CI/CD workflows.

If you're ready to get started, [enroll now](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions) and join the learning community at KodeKloud.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/4b72039d-b086-4331-9b30-0ce7dbd431be/lesson/86ac6605-2eb6-462e-9363-dc708af6be75" />
</CardGroup>


# Demo Convert Jenkins Job to GitHub Actions Workflow

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Manual-Migration-From-Jenkins-to-GitHub-Actions/Demo-Convert-Jenkins-Job-to-GitHub-Actions-Workflow/page

Migrating a Jenkins freestyle job to a manually triggered GitHub Actions workflow that reproduces shell steps and installs required packages.

In this lesson we'll migrate a simple Jenkins freestyle job into a GitHub Actions workflow. The goal is to replicate the Jenkins job behavior (a sequence of shell steps run on a single node) by creating a single-job workflow that can be manually triggered from the Actions UI.

Below are the original Jenkins job and its build steps, followed by a concise GitHub Actions workflow that reproduces the same execution flow on `ubuntu-latest`.

<Frame>
  <img alt="A dark-themed Jenkins dashboard screenshot showing a list of CI pipeline jobs (ci-pipeline-poll-scm, Generate ASCII Artwork, scripted-pipeline, solar-system-ci-pipeline) with columns for last success, failure, and duration. The left sidebar shows navigation items like New Item, Build History, Manage Jenkins and a Build Queue panel." />
</Frame>

This migration focuses on the "Generate ASCII Artwork" freestyle job. Open its configuration to inspect the build steps and options.

<Frame>
  <img alt="A screenshot of the Jenkins web UI showing the &#x22;Configure&#x22; page for a job (Generate ASCII Artwork) with the General settings panel, description field, and several option checkboxes. The sidebar lists other sections (Source Code Management, Triggers, Environment, Build Steps) and Save/Apply buttons are visible at the bottom." />
</Frame>

Key characteristics of this Jenkins job:

* No source control is configured (it was run manually in Jenkins).
* No automated triggers (built manually).
* No environment variables defined.
* Several shell build steps that run sequentially on one build node.

<Frame>
  <img alt="A dark-themed Jenkins &#x22;Configure&#x22; settings screen showing the Triggers and Environment sections with multiple checkboxes (e.g., Poll SCM, Build periodically). The left sidebar lists job configuration tabs like General, Source Code Management, Triggers, and Build Steps." />
</Frame>

Below is the core shell script the Jenkins job ran. It:

* Calls the adviceslip API to fetch a piece of advice.
* Validates the advice contains more than five words.
* Installs `cowsay` and prints the advice as ASCII art.

```bash theme={null}
