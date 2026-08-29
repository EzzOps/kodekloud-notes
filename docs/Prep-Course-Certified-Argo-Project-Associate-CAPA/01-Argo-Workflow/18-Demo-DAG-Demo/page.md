# Demo DAG Demo

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Demo-DAG-Demo/page

Describes an Argo Workflow DAG example that demonstrates task dependencies, parallel execution, and join points using four tasks (A, B, C, D) and a shared echo container.

This lesson shows how to define an Argo Workflow as a Directed Acyclic Graph (DAG) by declaring task dependencies instead of listing steps sequentially. Using a DAG makes it natural to express parallelism, join points, and complex dependency relationships between tasks.

Overview

* Entrypoint: `main` — a DAG template that declares four tasks: A, B, C, and D.
* All tasks use the same container template `echo-message` (based on busybox) which echoes a parameter provided to the task.
* Dependencies:
  * A has no dependencies and runs first.
  * B and C both depend on A, so they run in parallel after A completes.
  * D depends on both B and C and runs only after both have finished.

> **lightbulb** If a task has no dependencies it becomes runnable immediately. Multiple tasks that become runnable at the same time will execute in parallel (subject to executor and cluster limits).

Task summary

| Task | Depends on | Purpose                        | Message parameter |
| ---- | ---------- | ------------------------------ | ----------------- |
| A    | (none)     | Starts the DAG                 | "Task A"          |
| B    | A          | Runs after A (parallel with C) | "Task B"          |
| C    | A          | Runs after A (parallel with B) | "Task C"          |
| D    | B, C       | Joins results of B and C       | "Task D"          |

Example workflow (Argo Workflow YAML)

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: dag-
  namespace: argo
spec:
  entrypoint: main
  templates:
  - name: main
    dag:
      tasks:
      - name: A
        template: echo-message
        arguments:
          parameters:
          - name: message
            value: "Task A"
      - name: B
        template: echo-message
        dependencies: [A] # B depends on A
        arguments:
          parameters:
          - name: message
            value: "Task B"
      - name: C
        template: echo-message
        dependencies: [A] # C also depends on A
        arguments:
          parameters:
          - name: message
            value: "Task C"
      - name: D
        template: echo-message
        dependencies: [B, C] # D depends on both B AND C
        arguments:
          parameters:
          - name: message
            value: "Task D"
  - name: echo-message
    inputs:
      parameters:
      - name: message
    container:
      image: busybox
      command: [sh, -c, "echo {{inputs.parameters.message}}"]
```

Execution order (step-by-step)

1. Task A runs first because it has no dependencies.
2. When A completes, both B and C become runnable and execute concurrently (subject to resource limits).
3. After both B and C finish, D becomes runnable and runs (it depends on B and C).
4. The workflow completes once D finishes.

Viewing status, logs, and common CLI commands

| Action                                 | Command                                            |
| -------------------------------------- | -------------------------------------------------- |
| Submit workflow (from file `dag.yaml`) | `argo submit -n argo dag.yaml`                     |
| Get workflow status                    | `argo get <workflow-name> -n argo`                 |
| Stream logs for the workflow           | `argo logs <workflow-name> -n argo`                |
| View logs for a specific step/pod      | `argo logs <workflow-name> -n argo -c <container>` |

Example task log output (each task echoes its message)

```console theme={null}
Task A
Task B
Task C
Task D
```

Container command executed for each task

```bash theme={null}
sh -c 'echo {{inputs.parameters.message}}'
```

Best practices & notes

* Use DAGs when you need parallelism or non-linear execution flows. For strict linear flows, a steps-based template may be simpler.
* Keep resource and concurrency limits in mind; "runnable" tasks may wait if cluster limits are reached.
* Prefer clear task names and parameter values so logs and UIs are easier to read.

Links and references

* [Argo Workflows - DAGs](https://argoproj.github.io/argo-workflows/workflows/dag/)
* [Argo Workflows documentation](https://argoproj.github.io/argo-workflows/)
* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

This simple DAG demonstrates how to control execution order by declaring dependencies between tasks rather than writing an explicit linear sequence—enabling parallel runs and join points with minimal YAML.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/d8e55b57-c411-49e6-9fa9-179b2f61b784)
