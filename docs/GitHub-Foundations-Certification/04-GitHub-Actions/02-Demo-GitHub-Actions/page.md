# Demo GitHub Actions

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Actions/Demo-GitHub-Actions/page

Overview of GitHub Actions workflows, triggers, and a sample validation job checking for a required file on push and pull request

GitHub Actions is GitHub’s built-in automation platform that runs workflows defined in your repository. Workflows are YAML files that describe when the automation should run (triggers) and what steps to execute (jobs and steps). Typical uses include testing, building, and deploying code whenever something changes in your repo.

Workflows are event-driven: GitHub fires events (pushes, pull requests, scheduled timers, manual triggers, and many others), and your workflows respond to those events.

<Frame>
  <img alt="This is a screenshot of a GitHub documentation page titled &#x22;Events that trigger workflows,&#x22; detailing how workflows can be configured to run on specific activities within GitHub. There is a menu on the right listing various event types." />
</Frame>

## Common triggers

* `push` — run when commits are pushed to branches or tags.
* `pull_request` — run when a pull request is opened, synchronized, or updated.
* `schedule` — run at regular intervals using cron syntax.
* `workflow_dispatch` — expose a manual run button in the Actions UI.
* Many repository events (assigned, labeled, opened, etc.) can also trigger workflows.

<Frame>
  <img alt="The image shows a GitHub documentation page describing events that trigger workflows, specifically detailing the &#x22;push&#x22; event including its payload and activity types. The sidebar displays a list of various event options." />
</Frame>

You can combine triggers so a single workflow runs on multiple events. For recurring runs, the `schedule` trigger uses cron syntax. For manual runs from the repository UI, enable `workflow_dispatch`:

```yaml theme={null}
on: workflow_dispatch
```

<Frame>
  <img alt="The image is a screenshot from GitHub Docs showing the &#x22;Events that trigger workflows&#x22; page, focusing on pull request event payload and activity types such as &#x22;assigned,&#x22; &#x22;unassigned,&#x22; &#x22;labeled,&#x22; etc." />
</Frame>

## Example: verify a required file on push and PR

This example creates a lightweight workflow that runs on pushes and pull requests targeting the `main` branch. It performs a simple check: confirm that `index.html` exists at the repository root. If the file is missing, the job fails.

Create a file at `.github/workflows/<name>.yml` with the following content:

```yaml theme={null}
name: Game Quality Check
