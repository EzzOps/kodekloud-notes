# .github/workflows/deploy.yml
on: workflow_dispatch

env:
  CONTAINER_REGISTRY: docker.io
  IMAGE_NAME: github-actions-nginx

jobs:
  docker:
    # ...
  deploy:
    needs: docker
    concurrency:
      group: production-deployment
      cancel-in-progress: false
    runs-on: ubuntu-latest
    steps:
      - name: Docker Run
        run: |
          echo docker run -d -p 8080:80 \
            $CONTAINER_REGISTRY/${{ vars.DOCKER_USERNAME }}/${{ IMAGE_NAME }}:latest
          sleep 6000s   # ❌ Intended 600s but used 6000s
```

If this runs unchecked, the job hangs for nearly 1 hour and 40 minutes, burning through your minutes until the default 6-hour limit is reached.

***

## Adding a Timeout

You can apply `timeout-minutes` at **two** levels:

| Scope      | Applies To               | Syntax Location   | Use Case                               |
| ---------- | ------------------------ | ----------------- | -------------------------------------- |
| Step-Level | A single `run` or action | Within a `steps:` | Limit a long-running command or action |
| Job-Level  | All steps in a job       | Within the `job:` | Enforce a total time budget per job    |

### Step-Level Timeout

Limit just the problematic step to, for example, **1 minute**:

```yaml theme={null}
jobs:
  deploy:
    needs: docker
    runs-on: ubuntu-latest
    steps:
      - name: Docker Run
        timeout-minutes: 1
        run: |
          echo docker run -d -p 8080:80 \
            $CONTAINER_REGISTRY/${{ vars.DOCKER_USERNAME }}/${{ IMAGE_NAME }}:latest
          sleep 6000s
```

If the `Docker Run` step exceeds 1 minute, it is automatically canceled and the job fails.

### Job-Level Timeout

Apply a timeout for the **entire** job — all steps must finish before the deadline:

```yaml theme={null}
jobs:
  deploy:
    needs: docker
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Setup Environment
        run: echo "Setting up environment"
      - name: Docker Run
        run: |
          echo docker run -d -p 8080:80 \
            $CONTAINER_REGISTRY/${{ vars.DOCKER_USERNAME }}/${{ IMAGE_NAME }}:latest
          sleep 6000s
```

Here, if any step in `deploy` takes longer than 5 minutes in total, the workflow stops.

<Callout icon="triangle-alert">
  Setting overly aggressive timeouts may cause legitimate tasks to fail. Choose values that balance reliability and cost control.
</Callout>

***

## Demo and Logs

After committing your changes, trigger the workflow manually. You’ll see:

```bash theme={null}
docker run -d -p 8080:80 \
  $CONTAINER_REGISTRY/siddharth67/$IMAGE_NAME:latest
# -> docker run -d -p 8080:80 \
#    docker.io/siddharth67/github-actions-nginx:latest
Error: The action has timed out.
```

In the GitHub Actions UI, an annotation appears:

> **The action has timed out.**

Logs show the step ran for roughly 1 minute and then terminated at the `timeout-minutes` threshold.

***

## Best Practices

* Use **step-level** timeouts for known long-running commands.
* Apply **job-level** timeouts to guard entire workflows.
* Monitor execution times and adjust `timeout-minutes` as your builds evolve.

***

## Links and References

* [GitHub Actions: Workflow syntax for GitHub Actions – timeout-minutes](https://docs.github.com/actions/reference/workflow-syntax-for-github-actions#jobsjob_idtimeout-minutes)
* [GitHub Actions Concepts](https://docs.github.com/actions/learn-github-actions/introduction-to-github-actions)
* [Managing billing and usage for GitHub Actions](https://docs.github.com/billing/managing-billing-for-github-actions)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/0ac6c98f-7100-471e-b9aa-037f25cb58d7/lesson/a739686f-48c9-4148-b406-b206dd04a950" />
</CardGroup>


# Triggering a workflow

Source: https://notes.kodekloud.com/docs/GitHub-Actions/GitHub-Actions-Core-Concepts/Triggering-a-workflow/page

This guide covers common triggers for GitHub Actions workflows, including configuration and combining multiple triggers.

GitHub Actions can respond to many events—from code pushes and pull requests to scheduled cron jobs and manual dispatch. In this guide, we’ll cover the most common triggers, show you how to configure them, and demonstrate how to combine multiple triggers in a single workflow.

For a complete list of events, see the [official documentation][events-doc].

<Frame>
  ![The image shows a GitHub documentation page about events that trigger workflows, detailing how to configure workflows based on specific activities or events. The sidebar lists various related topics and options.](https://kodekloud.com/kk-media/image/upload/v1752876646/notes-assets/images/GitHub-Actions-Triggering-a-workflow/github-workflows-events-documentation-sidebar.jpg)
</Frame>

## Common Repository Events

You can launch workflows in response to repository activity. Below is a quick reference:

| Event         | Description                               | YAML snippet      |
| ------------- | ----------------------------------------- | ----------------- |
| push          | Run on commits pushed to branches or tags | `on: push`        |
| pull\_request | Trigger on PR open, edit, close, etc.     | see example below |
| issues        | Fire when issues are opened or modified   | `on: issues`      |
| release       | Trigger on draft, published, or edited    | `on: release`     |
| fork          | Run when someone forks the repository     | `on: fork`        |

### 1. Push

The simplest trigger is `push`. It fires whenever you push commits:

```yaml theme={null}
on: push
```

<Frame>
  ![The image shows a GitHub documentation page about events that trigger workflows, specifically focusing on the "push" event. It includes notes and examples related to webhook payloads and workflow triggers.](https://kodekloud.com/kk-media/image/upload/v1752876647/notes-assets/images/GitHub-Actions-Triggering-a-workflow/github-workflows-push-event-documentation.jpg)
</Frame>

### 2. Pull Request

Trigger workflows when pull requests change state—opened, edited, assigned, or closed:

```yaml theme={null}
on:
  pull_request:
    types: [opened, edited, closed, assigned]
```

<Frame>
  ![The image shows a GitHub Docs page about GitHub Actions, specifically detailing events that trigger workflows related to pull requests. It includes a list of activity types and webhook event payloads.](https://kodekloud.com/kk-media/image/upload/v1752876649/notes-assets/images/GitHub-Actions-Triggering-a-workflow/github-actions-pull-requests-workflows.jpg)
</Frame>

<Callout icon="lightbulb">
  You can filter by branches or tags under each event to narrow down when the workflow runs. See [GitHub Actions filters][filtering] for details.
</Callout>

## Scheduled Workflows

Use `schedule` with cron syntax to run jobs at regular intervals.

```yaml theme={null}
on:
  schedule:
    # Quote strings because '*' has special meaning in YAML
    - cron: '30 5 * * 1-5'
    - cron: '0 0 * * 0'
```

<Callout icon="triangle-alert">
  Running jobs too frequently can exhaust your GitHub Actions minutes. Always double-check your cron schedules.
</Callout>

If you need to test or build complex expressions, [Crontab Guru][crontab] is a fantastic visual tool:

<Frame>
  ![The image shows a webpage from "crontab guru," a tool for creating and understanding cron schedule expressions. It displays a cron expression set to run every minute.](https://kodekloud.com/kk-media/image/upload/v1752876650/notes-assets/images/GitHub-Actions-Triggering-a-workflow/crontab-guru-every-minute-schedule.jpg)
</Frame>

## Manual Triggers with workflow\_dispatch

Add `workflow_dispatch` to let users kick off a workflow by pushing a button. You can even define input parameters:

<Frame>
  ![The image shows a GitHub documentation page about "workflow\_dispatch" in GitHub Actions, detailing how to manually trigger workflows and configure inputs.](https://kodekloud.com/kk-media/image/upload/v1752876651/notes-assets/images/GitHub-Actions-Triggering-a-workflow/github-actions-workflow-dispatch-documentation.jpg)
</Frame>

```yaml theme={null}
on:
  workflow_dispatch:
    inputs:
      logLevel:
        description: 'Log level'
        required: true
        default: 'warning'
        type: choice
        options:
          - info
          - warning
          - debug
      tags:
        description: 'Include test scenario tags'
        required: false
        type: boolean
      environment:
        description: 'Target environment'
        required: true
```

Use these inputs in your job steps:

```yaml theme={null}
jobs:
  display-inputs:
    runs-on: ubuntu-latest
    steps:
      - name: Show inputs
        run: |
          echo "Log level: ${{ inputs.logLevel }}"
          echo "Tags: ${{ inputs.tags }}"
          echo "Environment: ${{ inputs.environment }}"
```

## Combining Schedule and Manual Dispatch

You can merge multiple triggers into one workflow. Here’s an example that builds, logs in, and pushes a Docker image on both a schedule and via manual dispatch.

```yaml theme={null}
name: CI/CD Docker Pipeline

on:
  schedule:
    - cron: '*/1 * * * *'
  workflow_dispatch:

env:
  CONTAINER_REGISTRY: docker.io
  IMAGE_NAME: github-actions-nginx

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
      - name: Build image
        run: |
          docker build -t ${{ env.CONTAINER_REGISTRY }}/${{ vars.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:latest .
      - name: Authenticate
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login \
            --username ${{ vars.DOCKER_USERNAME }} --password-stdin
      - name: Push image
        run: |
          docker push ${{ env.CONTAINER_REGISTRY }}/${{ vars.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}:latest
```

Once you push this file, the Actions tab will display scheduled runs alongside a **Run workflow** button for manual execution:

<Frame>
  ![The image shows a GitHub Actions interface with a list of workflow runs related to "Exploring Variables and Secrets." It displays the status, branch, and actor for each workflow run.](https://kodekloud.com/kk-media/image/upload/v1752876652/notes-assets/images/GitHub-Actions-Triggering-a-workflow/github-actions-workflow-runs-variables-secrets.jpg)
</Frame>

Each entry shows its trigger type—push, schedule, or manual—so you can tailor your CI/CD process to any scenario.

***

## Links and References

* [Events that trigger workflows][events-doc]
* [Workflow filtering][filtering]
* [Crontab Guru][crontab]
* [GitHub Actions Documentation](https://docs.github.com/en/actions)

[events-doc]: https://docs.github.com/en/actions/reference/events-that-trigger-workflows

[filtering]: https://docs.github.com/en/actions/learn-github-actions/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet

[crontab]: https://crontab.guru/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/0ac6c98f-7100-471e-b9aa-037f25cb58d7/lesson/45a1352b-6272-4969-bd76-7eda7103a80a" />
</CardGroup>
