# Demo Exit Handler

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Demo-Exit-Handler/page

Shows an Argo Workflows onExit exit handler example that always runs for cleanup and notifications, demonstrating behavior with an intentionally failing task and conditional actions based on workflow status

In this lesson we demonstrate an Argo Workflows exit handler using a compact example. Exit handlers run once at the end of a workflow regardless of success or failure and are ideal for cleanup, notifications, or posting results to external systems. This behavior is analogous to Jenkins pipelines' `post { always { ... } }` block.

Below is a minimal workflow that shows an `onExit` handler named `cleanup`. The primary work deliberately fails (exit code 1) so you can verify the exit handler still executes.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: exit-handler-workflow
  namespace: argo
spec:
  entrypoint: main
  onExit: cleanup # Always runs this template at the end
  templates:
  - name: main
    steps:
    - - name: work
        template: do-work
  - name: do-work
    container:
      image: alpine
      command: [sh, -c]
      args: ["echo 'Doing work...'; exit 1"] # This fails intentionally
  - name: cleanup
    container:
      image: alpine
      command: [sh, -c]
      args:
      - |
        echo "Workflow status: {{workflow.status}}"
        echo "Cleaning up resources..."
        if [ "{{workflow.status}}" = "Failed" ]; then
          echo "Sending failure notification"
        fi
```

> **lightbulb** Use `onExit` to centralize cleanup and notification logic. Inspect `{{workflow.status}}` to run conditional actions (for example, send alerts on Failure or perform extra validation on Succeeded).

## What each template does

| Template            | Purpose                           | Example behavior                                                      |
| ------------------- | --------------------------------- | --------------------------------------------------------------------- |
| entrypoint (`main`) | Starting point of the workflow    | Executes the `do-work` step                                           |
| `do-work`           | Primary task/container            | Prints a message and intentionally exits 1 to simulate failure        |
| `cleanup`           | Exit handler invoked via `onExit` | Prints workflow status and conditionally sends a failure notification |

Explanation:

* `entrypoint: main` — workflow starts at the `main` template.
* `onExit: cleanup` — ensures the `cleanup` template runs when the workflow finishes, irrespective of success or failure.
* `do-work` — the container task that demonstrates a failing step.
* `cleanup` — exit handler that reads `{{workflow.status}}` and conditionally performs actions.

## Viewing results

Even when a step fails, the exit handler still runs. In the Argo UI you can see the failed `work` step and the exit-handler node (typically displayed in green to indicate it completed). The screenshot below shows the failed `work` step and the exit-handler node along with pod details.

<Frame>
  <img alt="A screenshot of the Argo Workflows web UI showing a vertical workflow graph with a red failed &#x22;work&#x22; step and a green exit-handler node. The right-hand summary panel lists pod details including a &#x22;Failed&#x22; phase and an error message with an exit code." />
</Frame>

Sample `cleanup` logs printed after the workflow fails:

```text theme={null}
Workflow status: Failed
Cleaning up resources...
Sending failure notification
```

You can replace the `echo` commands with real integrations: Slack notifications, posting status to a webhook, cleaning up cloud resources, or triggering recovery workflows. When designing critical cleanup actions, make them idempotent so repeated runs are safe.

> **warning** Although `onExit` executes in normal success and failure scenarios, extreme outages (for example: controller crashes, severe cluster failures, or lost persistence) may prevent the exit handler from running. For critical cleanup, combine `onExit` with idempotent design or external watchdog processes.

## Practical tips

* Test exit handlers by forcing failures (exit codes) or injecting errors to ensure notifications and cleanups behave as expected.
* Use `{{workflow.status}}`, `{{workflow.name}}`, and other workflow variables to include contextual details in alerts.
* Keep exit handlers small and focused; offload heavy or long-running recovery tasks to separate workflows or jobs to avoid unexpected interactions.

## References

* Argo Workflows docs: [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)
* Jenkins pipeline `post` directive: [https://www.jenkins.io/doc/book/pipeline/syntax/#post](https://www.jenkins.io/doc/book/pipeline/syntax/#post)
* Example Slack incoming webhook: [https://api.slack.com/messaging/webhooks](https://api.slack.com/messaging/webhooks)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/e2ced3ee-781d-4448-8a60-7bb557fc0505)
