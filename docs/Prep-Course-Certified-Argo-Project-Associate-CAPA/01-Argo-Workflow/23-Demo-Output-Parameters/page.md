# Demo Output Parameters

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Demo-Output-Parameters/page

Explains Argo Workflows output parameters with a producer step capturing stdout as outputs.result and passing it to a consumer step as an input parameter, with example YAML and tips

Output parameters let one step expose a value that later steps can consume as arguments. This is useful for passing a script's stdout, results from a task, or any computed string into conditional logic, loops, or downstream templates.

In this concise example we'll walk through a simple workflow that generates a message in one step (the producer) and consumes that message in a subsequent step (the consumer).

## Workflow YAML (example)

The entrypoint `main` contains two sequential steps: `generate` (runs the `producer` template) and `consume` (runs the `consumer` template). The `producer` template uses a `script` that writes to stdout; Argo Workflows captures that stdout as the step result. The `consume` step receives that result via an argument.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: simple-output-example-
spec:
  entrypoint: main
  templates:
  - name: main
    steps:
      # The 'generate' step runs first
      - name: generate
        template: producer
      # The 'consume' step runs after 'generate' completes
      - name: consume
        template: consumer
        arguments:
          parameters:
          - name: message
            value: "{{steps.generate.outputs.result}}"

  - name: producer
    script:
      image: busybox:1.28
      command: ["sh", "-c"]
      source: |
        echo "hello from the producer step"

  - name: consumer
    inputs:
      parameters:
      - name: message
    container:
      image: busybox:1.28
      command: ["sh", "-c"]
      args: ["echo Received: '{{inputs.parameters.message}}'"]
```

## How it works (key points)

* The `producer` step runs first and prints a message to stdout.
* Argo captures the `script` template's stdout automatically and exposes it as `outputs.result` for the step.
* The `consume` step uses an argument with `value: "{{steps.generate.outputs.result}}"` to receive the message.
* Inside the `consumer` template, you access the passed parameter as `{{inputs.parameters.message}}`.

| Expression                        | What it returns                                                    | Example                             |
| --------------------------------- | ------------------------------------------------------------------ | ----------------------------------- |
| `{{steps.<step>.outputs.result}}` | The stdout result captured from a previous step (script templates) | `{{steps.generate.outputs.result}}` |
| `{{inputs.parameters.<name>}}`    | The value of an input parameter inside the template                | `{{inputs.parameters.message}}`     |

> **lightbulb** When a template uses `script`, Argo Workflows automatically captures the script's stdout as `outputs.result`. For container templates, echo or write to a defined output path and map it explicitly to expose outputs, or wrap the container output so it becomes available as `outputs.result`.

> **warning** Output parameters are only available after the producing step has completed. If a downstream step references an output from a still-running or failed step, it will not receive a valid value.

## What you will see in the UI

In the Argo Workflows UI you can inspect the workflow graph and the Inputs/Outputs pane for a node. The following screenshot shows the vertical graph and the `Inputs/Outputs` pane listing the `message` parameter with the value produced by the `generate` step.

<Frame>
  <img alt="A screenshot of an Argo Workflows UI showing a vertical workflow graph with three completed nodes (simple-output-example-..., generate, consume) on the left and toolbar buttons like RESUBMIT, DELETE, LOGS across the top. The right pane shows Inputs/Outputs with a parameter &#x22;message&#x22; set to &#x22;hello from the producer step&#x22; and an output Exit code of 0." />
</Frame>

## Inspecting logs

You can verify the flow by viewing logs from each step:

* `generate` step (producer) stdout:

```text theme={null}
hello from the producer step
```

* `consume` step (consumer) stdout:

```text theme={null}
Received: hello from the producer step
```

This confirms that the `producer` script output was captured as `steps.generate.outputs.result` and passed into the `consumer` step as the `message` parameter.

## When to use output parameters

* When you need to pass small text values (IDs, messages, JSON snippets) produced by one step into another.
* For larger binary blobs or files, consider using artifacts instead of output parameters.

## Links and references

* Official docs: [Argo Workflows — Parameters and Results](https://argoproj.github.io/argo-workflows/)
* Getting started: [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/f38290b2-a9f7-4f39-b2ea-0e505e03079e)
