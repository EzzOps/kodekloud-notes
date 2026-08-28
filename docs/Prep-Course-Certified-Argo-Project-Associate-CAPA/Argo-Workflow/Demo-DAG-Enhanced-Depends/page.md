# Demo DAG Enhanced Depends

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Demo-DAG-Enhanced-Depends/page

Explains Argo Workflows DAG depends expressions enabling conditional task execution using status selectors and boolean operators with examples and best practices.

Earlier we covered the `dependencies` field inside a DAG task template. This lesson shows the enhanced `depends` expression, which adds conditional logic based on other tasks' results so you can run tasks only when specific conditions are met.

The `depends` expression uses the syntax:

* taskName.Result — where Result is a status selector (e.g., `Succeeded`, `Failed`, `Skipped`, `Error`, `Daemoned`)
* Or aggregate selectors like `AnySucceeded` and `AllFailed`

You can combine expressions with Boolean operators:

* OR: `||`
* AND: `&&`
* NOT: `!`

Basic examples:

* Run `task-2` only if `task-1` succeeded:

```yaml theme={null}
depends: "task-1.Succeeded"
```

* A more complex expression:

```yaml theme={null}
depends: "(task-A.Succeeded || task-A.Skipped) && !task-B.Failed"
```

Status selectors and their meanings:

| Selector     | Meaning                                                    |
| ------------ | ---------------------------------------------------------- |
| Succeeded    | Task completed successfully (exit code 0)                  |
| Failed       | Task completed with non-zero exit code                     |
| Skipped      | Task was skipped/omitted (e.g., depends condition not met) |
| Error        | Task errored (system error)                                |
| Daemoned     | Task entered a daemon state (long-running)                 |
| AnySucceeded | At least one task in a group succeeded                     |
| AllFailed    | All tasks in a group failed                                |

Example: a complete Argo Workflow demonstrating `depends` in a DAG with four tasks. Tasks A and B run in parallel; C runs if either A or B succeeds; D runs only if both A and B succeed.

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
        template: succeeds
      - name: B
        template: fails
      - name: C-runs-if-either-succeeds
        template: echo-message
        arguments:
          parameters:
          - name: message
            value: "C: ran because A or B succeeded"
        depends: "A.Succeeded || B.Succeeded"
      - name: D-runs-if-both-succeed
        template: echo-message
        arguments:
          parameters:
          - name: message
            value: "D: ran because both A and B succeeded"
        depends: "A.Succeeded && B.Succeeded"

  - name: succeeds
    container:
      image: busybox
      command: ["sh", "-c", "echo 'I succeeded.'"]

  - name: fails
    container:
      image: busybox
      command: ["sh", "-c", "echo 'I failed.'; exit 1"]

  - name: echo-message
    inputs:
      parameters:
      - name: message
    container:
      image: busybox
      command: ["sh", "-c", "echo {{inputs.parameters.message}}"]
```

How this workflow behaves:

* The `succeeds` template echoes "I succeeded." and exits with code 0, so tasks using it report `Succeeded`.
* The `fails` template echoes "I failed." and exits non-zero, so tasks using it report `Failed`.
* The `echo-message` template prints the provided `message` parameter.

DAG behavior:

* Tasks A and B have no dependencies and start in parallel.
* Task C uses `depends: "A.Succeeded || B.Succeeded"` — it runs if either A or B succeeds.
* Task D uses `depends: "A.Succeeded && B.Succeeded"` — it runs only if both A and B succeed.

If B fails and A succeeds:

* C runs because at least one of A or B succeeded.
* D is skipped because both did not succeed. The UI shows D as Skipped/Omitted with the message "depends condition not met."

<Frame>
  <img alt="A screenshot of the Argo Workflows web UI showing a DAG with nodes A, B, C and D and status icons for each. The right-hand panel displays details for node D, marked Skipped/Omitted with the message &#x22;depends condition not met.&#x22;" />
</Frame>

Additional valid `depends` expressions (patterns you can reuse):

```yaml theme={null}
depends: "task || task-2.Failed"
depends: "(task.Succeeded || task.Skipped || task.Daemoned) || task-2.Failed"
depends: "(task-2.Succeeded || task-2.Skipped) && !task-3.Failed"
depends: "task-1.AnySucceeded || task-2.AllFailed"
```

| Common Pitfalls                                      | Recommendation                                                                                                        |   |                    |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | - | ------------------ |
| Forgetting YAML quoting for the `depends` expression | Always wrap the expression in quotes to avoid YAML parsing issues with \`                                             |   | `, `&&`, and `!\`. |
| Mixing `dependencies` and `depends` on the same task | Use one or the other. Convert `dependencies: [A, B, C]` to `depends: "A && B && C"` if you need the `depends` syntax. |   |                    |

<Callout icon="lightbulb">
  Use quotes around the `depends` expression so YAML treats operators (`||`, `&&`, `!`) correctly. `depends` supports boolean operators and selectors like `Succeeded`, `Failed`, `Skipped`, `Daemoned`, `AnySucceeded`, `AllFailed`.
</Callout>

<Callout icon="warning">
  Do not use both `dependencies` and `depends` on the same task. To convert `dependencies: [A, B, C]` into `depends`, use: `depends: "A && B && C"`.
</Callout>

Links and references:

* [Argo Workflows documentation](https://argoproj.github.io/argo-workflows/)
* For more DAG patterns and examples, consult the Argo docs and community examples.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/4ea238df-f582-426e-9069-8b0691a59eb7" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/9d88de1f-c669-4157-8d28-de88c3873d91" />
</CardGroup>
