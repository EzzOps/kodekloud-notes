# Timeout for Jobs and Steps

Source: https://notes.kodekloud.com/docs/GitHub-Actions/GitHub-Actions-Core-Concepts/Timeout-for-Jobs-and-Steps/page

Learn to use the timeout-minutes option in GitHub Actions to prevent jobs or steps from running indefinitely and control your CI/CD pipelines.

In this guide, you’ll learn how to use the `timeout-minutes` option in GitHub Actions to prevent jobs or steps from running indefinitely. By setting timeouts, you safeguard your CI/CD pipelines from unexpected delays and control your billable minutes.

## Why Enforce Timeouts?

* **Prevent runaway workflows** that consume unnecessary resources
* **Control billing** by limiting how long jobs or steps can execute
* **Fail fast** when something goes wrong (e.g., infinite loops or stalled processes)

<Callout icon="lightbulb">
  By default, GitHub Actions will cancel any workflow that runs longer than **360 minutes** (6 hours). Configuring `timeout-minutes` at a finer granularity helps you catch issues earlier.
</Callout>

***

## The Problem: Unbounded Workflow Runs

Imagine you accidentally set a `sleep` duration too high:

```yaml theme={null}
