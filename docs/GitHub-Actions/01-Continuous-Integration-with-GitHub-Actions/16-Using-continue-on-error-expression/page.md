# Using continue on error expression

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Integration-with-GitHub-Actions/Using-continue-on-error-expression/page

This article explains how to use the `continue-on-error` feature in GitHub Actions to manage workflow failures.

GitHub Actions’ `continue-on-error` expression lets you prevent failures in a specific step or an entire job from aborting your workflow. You can use this setting to:

* Handle non-critical errors without stopping downstream steps.
* Upload logs and artifacts even when tests or checks fail.
* Experiment with unstable configurations in a matrix without blocking the run.

Below is an overview of how `continue-on-error` behaves at each level:

| Level | Scope                        | Typical Use Case                                          |
| ----- | ---------------------------- | --------------------------------------------------------- |
| Step  | A single step within a job   | Allow a flaky test or coverage threshold to fail “softly” |
| Job   | The entire job in a workflow | Let an experimental matrix configuration fail quietly     |

***

## Continue-on-error at the Step Level

When you set `continue-on-error: true` on a step, a non-zero exit code won’t fail the job. This is ideal for allowing post-test uploads or cleanup steps to run even if tests or coverage checks fail.

<Frame>
  ![The image shows a GitHub Docs page about GitHub Actions, specifically focusing on the "continue-on-error" feature in workflow syntax. It includes an example of preventing a specific failing matrix job from causing a workflow run to fail.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876520/notes-assets/images/GitHub-Actions-Using-continue-on-error-expression/github-actions-continue-on-error-example.jpg)
</Frame>

In this example, the **Code Coverage** job executes tests, enforces a coverage threshold, and then uploads the report regardless of success or failure.

```yaml theme={null}
