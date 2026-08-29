# .github/workflows/ci.yml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run a pinned community action
        uses: user/action-name@4f2c3b1a9e8d6f7a0b1c2d3e4f5a6b7c8d9e0f1
        with:
          example-input: value
```

See the `actions/checkout` repository for implementation details: [https://github.com/actions/checkout](https://github.com/actions/checkout)

Additional practical tips

* Use Dependabot and other supply-chain tools to monitor action updates and vulnerabilities: [https://docs.github.com/en/code-security/supply-chain-security/keeping-your-dependencies-updated-automatically/about-dependabot](https://docs.github.com/en/code-security/supply-chain-security/keeping-your-dependencies-updated-automatically/about-dependabot)
* Limit repository secrets to only what workflows require; avoid exposing secrets to untrusted actions.
* If an action is useful but you need to audit or customize it, fork the repository and use your forked reference in workflows.
* Consider running untrusted actions inside isolated repositories or environments until audited.

> **warning** Be cautious with actions that request broad permissions or ask for sensitive inputs. Always pin to a release tag or a commit SHA, and prefer audited or verified actions for production workflows.

Links and references

* GitHub Marketplace (Actions): [https://github.com/marketplace?type=actions](https://github.com/marketplace?type=actions)
* GitHub Actions permissions docs: [https://docs.github.com/en/actions/learn-github-actions/workflow-syntax-for-github-actions#permissions](https://docs.github.com/en/actions/learn-github-actions/workflow-syntax-for-github-actions#permissions)
* Dependabot: [https://docs.github.com/en/code-security/supply-chain-security/keeping-your-dependencies-updated-automatically/about-dependabot](https://docs.github.com/en/code-security/supply-chain-security/keeping-your-dependencies-updated-automatically/about-dependabot)
* actions/checkout repository: [https://github.com/actions/checkout](https://github.com/actions/checkout)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/e995be1d-2fac-4dc2-b467-fb8d1072632b/lesson/7ee29ca9-2c10-4074-a275-f4297146c750)


# GitHub Actions Basics

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Actions/GitHub-Actions-Basics/page

Overview of GitHub Actions basics, explaining workflows, runners, CI/CD automation, caching, reusable actions, and a minimal workflow example for building and testing code

Let's briefly cover GitHub Actions and how it helps automate CI/CD directly from your repositories.

What is GitHub Actions?

GitHub Actions is a built-in automation platform in GitHub that enables you to define workflows which run on repository events. These workflows are commonly used to implement CI/CD pipelines that build, test, and deploy code — keeping automation next to the codebase for better visibility and collaboration.

Workflows can execute on multiple operating systems such as Ubuntu, Windows, and macOS:

<Frame>
  <img alt="The image shows icons representing Ubuntu, Windows, and MacOS as part of GitHub Actions, numbered one to three." />
</Frame>

Runners and environments

* GitHub-hosted runners: GitHub provisions and scales virtual machines for you, maintains the execution environment, and provides logs and workflow reporting.
* Self-hosted runners: You provide and manage the machines (physical or virtual) that run your jobs, which lets you control hardware, software, and networking.

GitHub Actions supports caching dependencies and build outputs through reusable actions (for example, `actions/cache`) which you can configure in workflows to speed up repeated runs and reduce network usage.

<Frame>
  <img alt="The image outlines two tasks managed by GitHub: executing tasks in virtual environments and caching necessary dependencies." />
</Frame>

Minimal workflow example

A typical workflow YAML defines triggers, jobs, and the steps each job runs. Here is a concise CI example that runs on pushes or pull requests to `main`, sets up Python, installs dependencies, and runs tests:

```yaml theme={null}
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest
```

Key concepts at a glance

| Concept  | What it is                                                  | Example                                                 |
| -------- | ----------------------------------------------------------- | ------------------------------------------------------- |
| Triggers | Events that start workflows                                 | `push`, `pull_request`, `schedule`                      |
| Runners  | Environment where jobs run                                  | `ubuntu-latest` (GitHub-hosted) or self-hosted machines |
| Jobs     | Isolated units of work; can run in parallel or sequentially | `build`, `test`, `deploy`                               |
| Steps    | Individual actions or shell commands inside a job           | `uses: actions/checkout@v3`, `run: pytest`              |
| Actions  | Reusable components from the Marketplace or your repo       | `actions/setup-python@v4`, `actions/cache`              |

> **lightbulb** Use the [GitHub Actions Marketplace](https://github.com/marketplace?type=actions) to find reusable actions for common tasks such as checking out code, setting up runtimes, caching dependencies, or deploying to cloud providers. Also consider `actions/cache` for dependency caching to speed up pipeline runs: [https://github.com/actions/cache](https://github.com/actions/cache).

Why adopt GitHub Actions?

* Integrated: Workflows live with your code, reducing context switching.
* Flexible: Support for multiple OSes and custom runners.
* Scalable: GitHub-hosted runners scale automatically; self-hosted lets you control resources.
* Extensible: Marketplace offers many prebuilt actions to streamline common steps and integrations.

Further reading and references

* GitHub Actions docs: [https://docs.github.com/actions](https://docs.github.com/actions)
* GitHub Actions Marketplace: [https://github.com/marketplace?type=actions](https://github.com/marketplace?type=actions)
* `actions/cache` action: [https://github.com/actions/cache](https://github.com/actions/cache)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/e995be1d-2fac-4dc2-b467-fb8d1072632b/lesson/f4946550-d87b-4e03-92a6-d1c4a6763e3d)
