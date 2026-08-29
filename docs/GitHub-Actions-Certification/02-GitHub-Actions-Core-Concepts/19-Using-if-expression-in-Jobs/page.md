# Enable runner diagnostic logging
ACTIONS_RUNNER_DEBUG = true

# Enable step debug logging
ACTIONS_STEP_DEBUG  = true
```

> If both secret and variable exist for the same key, the secret value overrides the variable.

***

## Demo: Creating and Observing a Debug Workflow

This demo shows a simple workflow that fails intentionally, illustrating how step debug logging provides extra detail.

### 1. Create a New Repository

1. In GitHub, create a **public** repo named `debug-workflow-demo` with a `README.md`.
2. Clone the repository locally or open it in VS Code.

### 2. Add the Workflow File

Create file `.github/workflows/debug.yaml` with the following content:

```yaml theme={null}
name: Debugging Demo

on:
  workflow_dispatch:

env:
  USER_1: "foo-user"
  USER_2: "bar-user"

jobs:
  debug_job:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set USERNAME from USER_1
        run: |
          echo "USERNAME=$USER_1" >> $GITHUB_ENV

      - name: Print USERNAME and Fail
        run: |
          echo "Printing USERNAME from previous step"
          echo "Username: $USERNAME"
          exit 1

      - name: Print USER_2
        run: |
          echo "Printing USER_2: $USER_2"
```

Commit and push:

```bash theme={null}
git add .github/workflows/debug.yaml
git commit -m "Add debug workflow"
git push
```

### 3. Run Without Debug Logging

1. In the repo, go to **Actions → Debugging Demo**.
2. Click **Run workflow**.

The third step fails and the fourth step is skipped:

![The image shows a GitHub Actions interface with a failed debug job, displaying the setup and steps of the workflow.](https://kodekloud.com/kk-media/image/upload/v1752876133/notes-assets/images/GitHub-Actions-Certification-Enable-step-debug-logging-in-a-workflow/github-actions-failed-job-workflow.jpg)

*Default logs* only display commands and outputs, without showing condition evaluations or skipped steps details.

***

## Enabling Step Debug Logging in the UI

1. On the failed run’s page, click **Re-run jobs ▶︎ Re-run with debug logging**.
2. The job reruns and prepends each log line with `##[debug]`:

![The image shows a GitHub repository settings page focused on "Actions secrets and variables," with an option to re-run the job with debug logging enabled.](https://kodekloud.com/kk-media/image/upload/v1752876134/notes-assets/images/GitHub-Actions-Certification-Enable-step-debug-logging-in-a-workflow/github-actions-failed-job-debug.jpg)

![The image shows a debug log from a GitHub Actions workflow, detailing the setup and execution of a job with various steps and actions.](https://kodekloud.com/kk-media/image/upload/v1752876135/notes-assets/images/GitHub-Actions-Certification-Enable-step-debug-logging-in-a-workflow/github-actions-workflow-debug-log.jpg)

Sample condition evaluation output:

```text theme={null}
##[debug]Evaluating condition for step: 'Checkout Repository'
##[debug]Evaluating: success()
##[debug]=> true
##[debug]Result: true
##[debug]Starting: Checkout Repository
```

And insight into skipped steps:

```text theme={null}
##[debug]Evaluating condition for step: 'Print USER_2'
##[debug]=> false
##[debug]Skipping step 'Print USER_2'
```

***

## Downloading Runner Diagnostic Logs

After rerunning with debug, you can **Download log archive** from the run’s summary. The ZIP includes:

* All job logs with `##[debug]` entries
* A `runner-diagnostic-logs` folder containing runner internals

***

## Enabling Debug Logging by Default

To apply debug settings to every workflow run:

1. Navigate to **Settings → Secrets and variables → Actions → Variables**.
2. Click **New repository variable** and add:

   * `ACTIONS_RUNNER_DEBUG = true`
   * `ACTIONS_STEP_DEBUG  = true`

![The image shows a GitHub interface where a user is adding a new action variable named "ACTIONS\_STEP\_DEBUG" in the settings section of a repository.](https://kodekloud.com/kk-media/image/upload/v1752876136/notes-assets/images/GitHub-Actions-Certification-Enable-step-debug-logging-in-a-workflow/github-add-action-variable-settings.jpg)

![The image shows a GitHub repository settings page focused on "Actions secrets and variables," with sections for environment and repository variables. Two repository variables, "ACTIONS\_RUNNER\_DEBUG" and "ACTIONS\_STEP\_DEBUG," are set to true.](https://kodekloud.com/kk-media/image/upload/v1752876138/notes-assets/images/GitHub-Actions-Certification-Enable-step-debug-logging-in-a-workflow/github-repo-settings-actions-secrets-2.jpg)

### Precedence: Variables vs. Secrets

If a key exists as both a variable and a secret, **the secret value takes precedence**:

| Setting Type  | ACTIONS\_RUNNER\_DEBUG | Resulting Behavior          |
| ------------- | ---------------------- | --------------------------- |
| Repo Variable | true                   | Logging enabled by variable |
| Repo Secret   | false                  | Logging disabled by secret  |

![The image shows a GitHub repository settings page focused on "Actions secrets and variables," with options to manage environment and repository secrets.](https://kodekloud.com/kk-media/image/upload/v1752876139/notes-assets/images/GitHub-Actions-Certification-Enable-step-debug-logging-in-a-workflow/github-repo-settings-actions-secrets.jpg)

> **triangle-alert** Always verify the final debug log behavior when mixing variables and secrets. Secrets override variables, which may disable diagnostic logging if set to `false`.

***

By following these steps, you can enable and customize both step-level and runner-level debug logging in GitHub Actions, giving you full visibility into your workflow executions.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions-certification/module/54711be0-66e6-461b-b935-f77d78a5e000/lesson/8b981037-16ef-44dd-9db7-c37988726b6d)


# Using if expression in Jobs

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/GitHub-Actions-Core-Concepts/Using-if-expression-in-Jobs/page

This guide explains using context variables and `if` expressions in GitHub Actions workflows for conditional job execution.

In this guide, you’ll discover how to harness context variables and `if` expressions in GitHub Actions workflows to run jobs conditionally. This is essential for optimizing CI/CD pipelines, reducing unnecessary steps, and ensuring deployments only occur on the desired branch.

## What Are Context Variables?

When a workflow runs, GitHub makes a set of context variables available in JSON format. You can reference these contexts with expressions like `${{ github.ref }}` or `${{ env.VAR_NAME }}`.

```json theme={null}
{
  "token": "****",
  "job": "dump_contexts_to_log",
  "ref": "refs/heads/main",
  "sha": "ab3c0b9ccd2c8b0154e48e279bad3cf8c646",
  "repository": "sidd-harth-7/actions-1",
  "repository_owner_id": 147399322,
  "repository_owner": "sidd-harth-7",
  "repositoryUrl": "git://github.com/sidd-harth-7/actions-1.git",
  "run_id": 6492400732,
  "run_number": 1,
  "event_name": "push"
}
```

For a deep dive into expressions and context variables, see the [GitHub Actions Expressions docs][expressions-docs].

![The image shows a GitHub Docs page about "Expressions" in GitHub Actions, explaining how to evaluate expressions in workflows and actions. It includes navigation links and a section on using expressions with the if keyword.](https://kodekloud.com/kk-media/image/upload/v1752876174/notes-assets/images/GitHub-Actions-Certification-Using-if-expression-in-Jobs/github-actions-expressions-docs-page.jpg)

## Common Contexts in Workflows

| Context   | Description                                   | Example                          |
| --------- | --------------------------------------------- | -------------------------------- |
| `github`  | Information about the workflow run and event  | `${{ github.ref }}`              |
| `env`     | Environment variables defined in the workflow | `${{ env.CONTAINER_REGISTRY }}`  |
| `secrets` | Encrypted secrets stored in your repository   | `${{ secrets.DOCKER_PASSWORD }}` |
| `vars`    | Repository-level variables                    | `${{ vars.DOCKER_USERNAME }}`    |

## Sample Workflow: Build and Conditional Deploy

Below is a workflow that builds a Docker image on every push but only deploys when the push targets the `main` branch.

```yaml theme={null}
name: Deploy on Main

on:
  push:
    branches: [ main ]

env:
  CONTAINER_REGISTRY: docker.io
  IMAGE_NAME: github-actions-nginx

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker Image
        run: |
          docker build -t ${{ env.CONTAINER_REGISTRY }}/${{ vars.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:latest .
      - name: Log In to Registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login ${{ env.CONTAINER_REGISTRY }} --username ${{ vars.DOCKER_USERNAME }} --password-stdin
      - name: Push Image
        run: |
          docker push ${{ env.CONTAINER_REGISTRY }}/${{ vars.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:latest

  deploy:
    if: github.ref == 'refs/heads/main'
    needs: docker
    concurrency:
      group: production-deployment
      cancel-in-progress: false
    runs-on: ubuntu-latest
    steps:
      - name: Run Container
        timeout-minutes: 10
        run: |
          docker run -d -p 8080:80 ${{ env.CONTAINER_REGISTRY }}/${{ vars.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:latest
          sleep 600
```

> **lightbulb** The `deploy` job is guarded by the `if` expression. It only runs when `github.ref` equals `refs/heads/main`.

## Observing Workflow Runs

1. Push to a feature branch:

![The image shows a GitHub Actions interface with a list of workflow runs titled "Exploring Variables and Secrets." It displays details such as event triggers, status, branch, and execution time.](https://kodekloud.com/kk-media/image/upload/v1752876174/notes-assets/images/GitHub-Actions-Certification-Using-if-expression-in-Jobs/github-actions-exploring-variables-secrets.jpg)

2. Notice that the `docker` job succeeded but the `deploy` job is skipped:

![The image shows a GitHub Actions workflow summary with a successful run, displaying jobs for "docker" and "deploy" in a sequence.](https://kodekloud.com/kk-media/image/upload/v1752876175/notes-assets/images/GitHub-Actions-Certification-Using-if-expression-in-Jobs/github-actions-workflow-success-docker-deploy.jpg)

> **triangle-alert** If your `if` condition is malformed or compares the wrong context, the job will silently skip. Always verify your branch references.

3. Open a pull request from your feature branch into `main`:

![The image shows a GitHub interface where a user is creating a pull request to merge changes from a "feature/testing" branch into the "main" branch. The interface indicates that the branches can be automatically merged.](https://kodekloud.com/kk-media/image/upload/v1752876176/notes-assets/images/GitHub-Actions-Certification-Using-if-expression-in-Jobs/github-pull-request-feature-main-merge.jpg)

4. Ensure all status checks pass before merging:

![The image shows a GitHub pull request page with details about commits, checks, and merge status. It indicates that all checks have passed and the branch has no conflicts with the base branch.](https://kodekloud.com/kk-media/image/upload/v1752876177/notes-assets/images/GitHub-Actions-Certification-Using-if-expression-in-Jobs/github-pull-request-commits-checks-status.jpg)

5. After merging into `main`, observe the full workflow including `deploy`:

![The image shows a GitHub Actions interface with a list of workflow runs for a project titled "Exploring Variables and Secrets." It displays the status, branch, and timing of each workflow run.](https://kodekloud.com/kk-media/image/upload/v1752876179/notes-assets/images/GitHub-Actions-Certification-Using-if-expression-in-Jobs/github-actions-workflow-runs-exploring-variables.jpg)

![The image shows a GitHub Actions interface with a workflow in progress, displaying jobs for "docker" and "deploy" in a sequence.](https://kodekloud.com/kk-media/image/upload/v1752876180/notes-assets/images/GitHub-Actions-Certification-Using-if-expression-in-Jobs/github-actions-workflow-docker-deploy.jpg)

This end-to-end example illustrates how to use `if` expressions and contexts to drive conditional job execution in your CI/CD pipelines.

## Links and References

* [GitHub Actions Expressions][expressions-docs]
* [Contexts and Expression Syntax](https://docs.github.com/en/actions/learn-github-actions/contexts)
* [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

[expressions-docs]: https://docs.github.com/en/actions/learn-github-actions/expressions

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions-certification/module/54711be0-66e6-461b-b935-f77d78a5e000/lesson/082a4fa9-78b2-41a4-95e6-af74d0e44126)
