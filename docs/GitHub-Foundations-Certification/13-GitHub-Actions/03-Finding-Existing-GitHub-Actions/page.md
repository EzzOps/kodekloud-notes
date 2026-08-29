# Trigger on pushes and pull requests targeting main
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  # Optionally allow manual runs from the UI
  workflow_dispatch:

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      # Step 1: Checkout the repository so the runner has access to files
      - name: Checkout Repository
        uses: actions/checkout@v4

      # Step 2: Simple validation: ensure index.html exists at repo root
      - name: Verify Core Files
        run: |
          if [ -f "index.html" ]; then
            echo "✔ index.html found. Ready for launch!"
          else
            echo "✖ index.html is missing! Game will not load."
            exit 1
          fi
```

> **lightbulb** Place this file under `.github/workflows/` and commit to the default branch (for example, `main`). Any push or pull request that targets `main` will trigger the workflow automatically.

When GitHub Pages is enabled for a repository, GitHub itself runs an internal workflow to build and deploy your site. That same Actions framework is what your custom workflows use — you can see build and deployment jobs, logs, and statuses in the Actions UI.

<Frame>
  <img alt="The image shows a GitHub Actions page displaying the status of a workflow run called &#x22;pages build and deployment,&#x22; which is successful." />
</Frame>

You can inspect workflow runs, job decomposition, and logs to troubleshoot or validate behavior. For example, the Pages workflow often runs multiple jobs (build, report status, deploy), which you can expand and view details for.

<Frame>
  <img alt="The image shows a GitHub Actions workflow summary for &#x22;pages build and deployment.&#x22; The workflow has successfully completed with three jobs: &#x22;build,&#x22; &#x22;report-build-status,&#x22; and &#x22;deploy.&#x22;" />
</Frame>

Once your workflow file is committed to `main`, the Actions tab will show runs for each push and PR targeting that branch. Click a run to view runner provisioning and logs for each step. Typical checkout-related log lines look like:

```bash theme={null}
/usr/bin/git config --global --add safe.directory /home/runner/work/block-buster/block-buster
/usr/bin/git config --local --unset-all extensions.worktreeConfig
/usr/bin/git log -1 --format=%H
22395540d73abadf9b9e13a991b29aa5988c
```

The shell step that verifies `index.html` will echo success or print an error and exit with a non-zero code to fail the job:

```bash theme={null}
if [ -f "index.html" ]; then
    echo "💻 index.html found. Ready for launch!"
else
    echo "❌ index.html is missing! Game will not load."
    exit 1
fi
# shell: /usr/bin/bash -e {0}
```

<Frame>
  <img alt="The image shows a GitHub Actions page displaying workflow runs for a repository named &#x22;block-buster&#x22; with workflows such as &#x22;Create code-check.yml&#x22; and &#x22;pages build and deployment&#x22;." />
</Frame>

## Quick reference

| Concept                | Description                                      | Example                        |
| ---------------------- | ------------------------------------------------ | ------------------------------ |
| Workflow file location | Where GitHub looks for your workflow definitions | `.github/workflows/<name>.yml` |
| Trigger on push        | Run when commits are pushed to branch(es)        | `on: push: branches: [ main ]` |
| Manual trigger         | Allow manual execution from the GitHub UI        | `on: workflow_dispatch`        |
| Checkout action        | Prepare runner with repository files             | `uses: actions/checkout@v4`    |
| Failing a job          | Exit with non-zero code to mark job as failed    | `exit 1` in a shell `run` step |

## Learn more

* [GitHub Actions — Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
* [actions/checkout](https://github.com/actions/checkout)
* [GitHub Pages documentation](https://docs.github.com/en/pages)

That's the basic flow: declare triggers, define jobs and steps, use actions (for checkout, caching, etc.), and run scripts or other action steps to validate, build, test, or deploy your code.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/e995be1d-2fac-4dc2-b467-fb8d1072632b/lesson/a6f134c1-36ee-46b9-bb45-0617829b8f69)


# Finding Existing GitHub Actions

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Actions/Finding-Existing-GitHub-Actions/page

Guide to finding and evaluating GitHub Actions in the Marketplace while assessing security, pinning versions, and following best practices to reduce supply chain risk

Where do we find existing GitHub Actions?

GitHub Actions are reusable automation components for workflows. They let you integrate tools and services into your CI/CD pipelines without reinventing common tasks. Actions can be authored by GitHub, partner organizations, or the community — enabling easy sharing and reuse across repositories.

The primary place to discover and evaluate actions is the GitHub Marketplace: [https://github.com/marketplace?type=actions](https://github.com/marketplace?type=actions). Marketplace listings show badges for GitHub-verified partners as well as community-created actions. Verified actions generally provide a higher level of trust, but community actions can also be useful when reviewed carefully.

<Frame>
  <img alt="The image showcases a list of GitHub-verified actions and third-party/community actions, each with descriptions and star ratings, from KodeKloud." />
</Frame>

Before adopting any third-party action, inspect its source code, documentation, and permissions to ensure it fits your security and maintenance standards.

> **lightbulb** When possible, prefer GitHub-verified actions. Always pin third-party actions to a specific tag or commit SHA to reduce supply-chain risk and avoid using moving references like `@main`.

Evaluation checklist

| What to check                 | Why it matters                            | How to verify                                                                        |
| ----------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------ |
| Repository health             | Determines maintenance and responsiveness | Look for recent commits, open/closed issues, PR activity, and number of contributors |
| Source code & README          | Confirms behavior and inputs/outputs      | Review the code, example usages, tests, and documented inputs/secrets                |
| Permissions & required scopes | Prevents over-privileged workflows        | Check the action README and your workflow’s `permissions` block (see docs)           |
| Release strategy              | Locks behavior to a known good version    | Prefer `uses: owner/repo@v1.2.3` or a commit SHA over branch names like `@main`      |
| License & ownership           | Ensures legal and support clarity         | Verify license file and maintainer information in the repo                           |
| Community signals             | Helps gauge trustworthiness               | Stars, forks, issues, and external references or blog posts help assess adoption     |

Example: pin an action to a commit SHA in your workflow

```yaml theme={null}
