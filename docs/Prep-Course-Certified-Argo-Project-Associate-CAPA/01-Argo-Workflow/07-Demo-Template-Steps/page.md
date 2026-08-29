# Demo Template Steps

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Demo-Template-Steps/page

Demonstrates Argo Workflows steps template using a Cosmic Moo example showing sequential step groups and parallel tasks calling a cow-says container

This example demonstrates the Argo Workflows "steps" template using a small workflow named "Cosmic Moo". The entrypoint template is `triple-moo`. The steps template models a list of lists: each outer list element (a step group) runs sequentially, and each item inside an inner list runs in parallel with the other items in that same group.

Key concepts:

* Outer list elements = sequential groups (one group runs after the previous completes).
* Inner list items = tasks that run in parallel within their group.

> **lightbulb** The steps template structure is a list of lists. Each top-level list element is a step group executed sequentially; items inside that group (an inner list) execute in parallel.

## Example workflow

In this workflow:

* The first step group contains a single step `first-moo` that runs first.
* After `first-moo` completes, the second step group runs two items in parallel: `parallel-moo-a` and `parallel-moo-b`.
* All steps call the `cow-says` template and pass a `message` parameter.

YAML:

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
      # First group (runs first)
      - - name: first-moo
          template: cow-says
          arguments:
            parameters:
              - name: message
                value: "Cosmic Ranch!"
      # Second group (runs after the first group completes). Items here run in parallel.
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

## How execution proceeds

1. Argo executes the first outer list element — the group containing `first-moo`.
2. Once `first-moo` succeeds, Argo proceeds to the next outer list element.
3. The next group contains `parallel-moo-a` and `parallel-moo-b`; those run concurrently.

Table: steps template summary

| Component                       | Behavior                                   | Example                                                 |
| ------------------------------- | ------------------------------------------ | ------------------------------------------------------- |
| Outer list element (step group) | Runs sequentially, one group after another | The first group runs before the second group            |
| Inner list items                | Run in parallel within the same group      | `parallel-moo-a` and `parallel-moo-b` run concurrently  |
| Template reference              | Defines the work each step performs        | `cow-says` template runs the `rancher/cowsay` container |

## Sample logs

When you inspect the logs for `first-moo`, you'll see the cowsay output such as:

```text theme={null}
< Cosmic Ranch! >
-----------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     |
```

Each parallel task (`parallel-moo-a` and `parallel-moo-b`) will produce its own cowsay output when they run.

## Previewing the execution graph

You can preview how the workflow will execute before submitting it using the Argo Workflows UI. Paste the YAML into the UI and choose the graph view to see the sequence and parallelism visually.

<Frame>
  <img alt="A screenshot of the Argo Workflows web UI showing a workflow graph with nodes labeled &#x22;cosmic-moo-nx4xq&#x22;, &#x22;first-moo&#x22;, and two parallel tasks (&#x22;parallel-moo-a&#x22; and &#x22;parallel-moo-b&#x22;). The right-hand panel displays the selected node's details, including pod name, host node, and a &#x22;Succeeded&#x22; phase." />
</Frame>

This rendered graph helps you visualize which steps run sequentially and which run in parallel.

## Links and references

* Argo Workflows: [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)
* Argo Workflows concepts: [https://argoproj.github.io/argo-workflows/workflows/what-is-workflow/](https://argoproj.github.io/argo-workflows/workflows/what-is-workflow/)
* Docker image used in example: [https://hub.docker.com/r/rancher/cowsay](https://hub.docker.com/r/rancher/cowsay)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/1ce86319-4f82-4bee-bbe5-d66122d3d739)
