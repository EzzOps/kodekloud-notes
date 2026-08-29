# Demo Template Suspend

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Demo-Template-Suspend/page

Explains Argo Workflows Suspend template for pausing workflow nodes for manual approvals or timed delays, with examples, usage patterns, and resume methods.

This lesson explains the Suspend template in Argo Workflows. The Suspend template pauses a workflow node either until a user or external process resumes it, or until a specified duration elapses. Common use cases include manual approvals, gating deployments, and short timed delays between steps.

Key references:

* [Argo Workflows overview](https://argoproj.github.io/argo-workflows/)
* [Argo CLI reference](https://argoproj.github.io/argo-workflows/cli/)
* [Argo Server API](https://argoproj.github.io/argo-workflows/argo-server/)
* [Argo UI](https://argoproj.github.io/argo-workflows/argo-ui/)

## Example workflow

Below is a compact example showing a typical pattern: run a "develop" step, wait for manual approval, pause for a short duration, then run a "test" step.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: suspend-
spec:
  entrypoint: suspend
  templates:
  - name: suspend
    steps:
    - - name: develop
        template: cowsay
      - name: approval
        template: approval
      - name: delay
        template: delay
      - name: test
        template: cowsay

  - name: approval
    suspend: {}

  - name: delay
    suspend:
      duration: "10s"

  - name: cowsay
    container:
      image: rancher/cowsay
      command: [cowsay]
      args: ["I will be executed for both develop and test steps"]
```

## What each part does

* spec.entrypoint: `suspend` — the workflow begins at the `suspend` template.
* templates\[0] (name: suspend): defines a steps-style workflow with four steps. In the example above these steps are defined in the same step group (inner list), which means they will be started concurrently. To make them run sequentially, see the note below.
* `develop` — executes the `cowsay` template.
* `approval` — runs the `approval` template; this is a Suspend template.
* `delay` — runs the `delay` template, a Suspend template that uses a duration to pause the node.
* `test` — executes the `cowsay` template again.
* approval / suspend:  — empty braces signal an indefinite suspend; the node is suspended until explicitly resumed.
* delay / suspend.duration: "10s" — suspends the delay node for 10 seconds; after that the node completes and the workflow continues.
* cowsay container — a small container used for both `develop` and `test`; it produces the same logs when each step runs.

## Sequential vs. concurrent steps

If you want the steps to run strictly in sequence (develop → approval → delay → test), structure the `steps` so each step group is a separate top-level list item, for example:

```yaml theme={null}
steps:
- - name: develop
    template: cowsay
- - name: approval
    template: approval
- - name: delay
    template: delay
- - name: test
    template: cowsay
```

When steps are defined in the same inner list, they start concurrently. In that concurrent case, a Suspend node suspends only that specific node — other concurrently running steps continue. Use separate step groups to enforce a linear approval-plus-delay flow.

> **lightbulb** The suspend duration must be a valid time string (for example "10s", "1m", "30s"). Avoid ambiguous formats like plain integers ("10") — include a time suffix.

## Typical execution flow (sequential example)

1. The `develop` step runs the `cowsay` template and completes.
2. The `approval` step runs the `approval` Suspend template. With `suspend: {}`, the workflow enters a suspended state and waits for manual resume.
3. After the workflow is resumed (UI/CLI/API), the `delay` step starts and suspends itself for `10s` using `suspend.duration`.
4. Once the 10-second pause finishes, the `test` step runs the `cowsay` template.

## Resume a suspended workflow

You can resume a suspended workflow using the UI, CLI, or API:

* UI: Click the Resume button in the Argo UI for the suspended workflow and confirm.
* CLI: Use the Argo CLI:

```bash theme={null}
argo resume <workflow-name>
```

* API: Call the Argo Server API or use automation that interacts with Argo to resume workflows.

## Templates and use cases

| Template name | Type                    | Typical use case                                                        |
| ------------- | ----------------------- | ----------------------------------------------------------------------- |
| `approval`    | Suspend (no duration)   | Manual approval or external gating (indefinite pause until resume)      |
| `delay`       | Suspend (with duration) | Short timed wait between steps (e.g., retries, cooldowns)               |
| `cowsay`      | Container               | Simple example container template for running commands / producing logs |

## Notes on logs and the graph view

* Both `develop` and `test` use the same `cowsay` template, so their logs will be identical when they run.
* Use the Argo UI graph view to visualize the workflow execution, suspended nodes, and node timing. Toggle between graph and DAG views to better understand execution order and concurrency.

## Example cowsay output

```text theme={null}
/ I will be executed for both develop and \
\ test steps
------------------------------
\   ^__^
 \(oo)\_______
 (__) \       )\/\
      ||----w |
      ||     ||
```

Further reading:

* [Argo Workflows documentation](https://argoproj.github.io/argo-workflows/)
* [Argo CLI docs](https://argoproj.github.io/argo-workflows/cli/)
* [Argo Server API docs](https://argoproj.github.io/argo-workflows/argo-server/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/26774ca3-63d3-40be-b7e0-aef5d8340bc3)
