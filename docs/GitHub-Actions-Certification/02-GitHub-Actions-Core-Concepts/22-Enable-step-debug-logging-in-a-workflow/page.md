# Enable step debug logging in a workflow

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/GitHub-Actions-Core-Concepts/Enable-step-debug-logging-in-a-workflow/page

This guide explains how to enable step debug logging in GitHub Actions workflows for better issue diagnosis.

Debug logging in GitHub Actions exposes low-level details about workflow execution, making it easier to diagnose issues in jobs and steps. This guide covers:

* What debug logging is and when to use it
* How to enable it via secrets or variables
* A demo workflow showing debug logging in action
* Managing debug settings by default at the repository level

***

## What Is Debug Logging?

By default, GitHub Actions logs include only high-level execution output. When you need deeper insights—such as condition evaluations, environment variable settings, and runner internals—you can turn on debug logging.

![The image shows a GitHub documentation page about enabling debug logging in GitHub Actions, with navigation links on the left and content explaining how to set up debug logging.](https://kodekloud.com/kk-media/image/upload/v1752876131/notes-assets/images/GitHub-Actions-Certification-Enable-step-debug-logging-in-a-workflow/github-actions-debug-logging-docs.jpg)

### Types of Debug Logging

Use one or both of the following:

| Debug Type                | Purpose                                          | Secret/Variable Name   |
| ------------------------- | ------------------------------------------------ | ---------------------- |
| Runner Diagnostic Logging | Captures the runner’s internal execution details | `ACTIONS_RUNNER_DEBUG` |
| Step Debug Logging        | Increases verbosity around each step’s execution | `ACTIONS_STEP_DEBUG`   |

![The image shows a GitHub documentation page about enabling runner and step debug logging in GitHub Actions. It includes instructions and a navigation menu on the left.](https://kodekloud.com/kk-media/image/upload/v1752876132/notes-assets/images/GitHub-Actions-Certification-Enable-step-debug-logging-in-a-workflow/github-actions-runner-debug-logging.jpg)

> **lightbulb** If you set both a secret and a variable with the same name, **the secret wins**.\
  Ensure you configure the correct value in your repository settings.

***

## Enabling Debug Logging via Secrets or Variables

To activate debug logging for a run, add one or both keys as **repository secrets** or **repository variables**:

```bash theme={null}
