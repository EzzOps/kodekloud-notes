# Template Invocators Types Steps

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Template-Invocators-Types-Steps/page

Describes Argo Workflows Steps templates demonstrating sequential step-groups and parallel steps using a cowsay example with reusable templates and parameter passing

Explore the Steps template invoker type in Argo Workflows. Steps templates let you compose multi-step workflows that run tasks both sequentially and in parallel. This example workflow, named "Cosmic Move", shows how a Steps template orchestrates reusable templates (here, `cow-says`) into a sequence of step groups with parallel execution inside groups.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: cosmic-moo-
spec:
  entrypoint: triple-moo
  templates:
  - name: triple-moo
    steps:
    - - name: first-moo
        template: cow-says
        arguments:
          parameters:
          - name: message
            value: "Cosmic Ranch!"
    - - name: parallel-moo-a
        template: cow-says
        arguments:
          parameters:
          - name: message
            value: "Galaxy Moo!"
      - name: parallel-moo-b
        template: cow-says
        arguments:
          parameters:
          - name: message
            value: "Milky Whey!"
  - name: cow-says
    inputs:
      parameters:
      - name: message
    container:
      image: rancher/cowsay
      command: ["cowsay"]
      args: ["{{inputs.parameters.message}}"]
```

How this workflow is wired:

* The workflow entrypoint is `triple-moo`.
* `triple-moo` uses a `steps` block to orchestrate calls to the reusable `cow-says` template.
* `cow-says` is a simple container task that runs `cowsay` with the supplied `message` parameter.

Understanding the `steps` structure

* `steps` is a list of step-groups (a list of lists).
  * Each top-level list item (each top-level `-`) is a step-group that executes in sequence.
  * Within a step-group, each inner `-` is an individual step that runs in parallel with the other inner steps in that group.

<Callout icon="lightbulb">
  Think of `steps` as a sequence of step-groups: each top-level dash creates a group that runs one after another; steps inside the same group (inner dashes) run concurrently.
</Callout>

Execution semantics (summary):

* Top-level elements (step-groups) run one after another (sequential).
* Inner list elements inside a group run at the same time (parallel).
* The workflow advances to the next group only after every step in the current group finishes.

Example: what happens in the "Cosmic Move" workflow

* First step-group:
  * `first-moo` runs by itself. The workflow waits until it completes.
* Second step-group:
  * `parallel-moo-a` and `parallel-moo-b` run concurrently. The workflow proceeds only after both finish.

When you inspect a running workflow with argo, the execution tree shows the sequence and parallel steps. Example output:

```console theme={null}
$ argo -n argo get cosmic-moo-k2kxq

STEP                    TEMPLATE       PODNAME
✓ cosmic-moo-k2kxq      triple-moo
├─✓ first-moo            cow-says       cosmic-moo-k2kxq-cow-says-2575730875
├─✓ parallel-moo-a       cow-says       cosmic-moo-k2kxq-cow-says-1190566453
└─✓ parallel-moo-b       cow-says       cosmic-moo-k2kxq-cow-says-1140233596
```

Quick reference table

| Concept                        | Behavior                                   | Example                                |
| ------------------------------ | ------------------------------------------ | -------------------------------------- |
| Step-group (top-level item)    | Runs sequentially relative to other groups | First group contains `first-moo`       |
| Steps in a group (inner items) | Run in parallel with each other            | `parallel-moo-a` and `parallel-moo-b`  |
| Entry point                    | Template name used to start the workflow   | `entrypoint: triple-moo`               |
| Reusable template              | Called by steps with parameters            | `cow-says` accepts `message` parameter |

Best practices

* Use Steps templates when you need explicit ordering and occasional parallelism between tasks.
* Keep reusable work in separate templates and pass parameters for customization.
* Use clear step names to make the execution tree easy to read when inspecting runs with `argo get`.

Links and references

* [Argo Workflows Documentation](https://argoproj.github.io/argo-workflows/)
* [Argo Workflows: Steps Templates](https://argoproj.github.io/argo-workflows/workflow-concepts/#steps)
* [rancher/cowsay on Docker Hub](https://hub.docker.com/r/rancher/cowsay)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/06207e06-90ea-4393-afdb-a33701d29999" />
</CardGroup>
