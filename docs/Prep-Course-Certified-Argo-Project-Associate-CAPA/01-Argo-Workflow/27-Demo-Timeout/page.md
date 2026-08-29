# Demo Timeout

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Demo-Timeout/page

Explains using activeDeadlineSeconds in Argo Workflows to set workflow and template pod timeouts, their interactions, effects, examples, and best practices

In this lesson you'll learn how to use timeouts to limit how long a template or an entire Argo Workflow can run. Argo supports the activeDeadlineSeconds field at two scopes:

* workflow\.spec.activeDeadlineSeconds — enforces a maximum runtime for the entire workflow (measured from creation). When exceeded, the Argo controller terminates the workflow.
* template-level activeDeadlineSeconds — enforces a maximum runtime for the pod that runs that template. When exceeded, Kubernetes terminates the pod.

You can use either level independently or both together. The effective behavior is a combination: a template can be terminated early by its own activeDeadlineSeconds, and the entire workflow can be terminated by the workflow-level activeDeadlineSeconds.

> **lightbulb** activeDeadlineSeconds is measured in seconds. Template-level timeouts normally translate to the pod's activeDeadlineSeconds and cause Kubernetes to terminate the pod when exceeded. The workflow-level timeout is enforced by the Argo controller and will terminate the whole workflow if it runs longer than the specified value.

## How activeDeadlineSeconds works (quick overview)

* Workflow-level timeout:
  * Enforced by the Argo controller.
  * Kills the workflow once total runtime since creation exceeds the value.
* Template-level timeout:
  * Enforced by Kubernetes for the pod running the template (via pod activeDeadlineSeconds).
  * When a pod is terminated by Kubernetes for exceeding its deadline, that step/template is marked failed.
* Combined behavior:
  * The earliest-exceeded deadline takes effect for a given pod/task.
  * If any step fails (including due to timeout) the workflow will be marked failed unless you use retries, continueOn, or exit handlers.

## Example Workflow YAML

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: timeout-workflow
  namespace: argo
spec:
  entrypoint: main
  # Workflow-level timeout: 60 seconds (1 minute)
  activeDeadlineSeconds: 60

  templates:
  - name: main
    steps:
      - - name: quick-task
          template: fast-step
        - name: slow-task
          template: slow-step

  - name: fast-step
    # Template-level timeout: 100 seconds (longer than workflow-level)
    activeDeadlineSeconds: 100
    container:
      image: alpine
      command: ["sh", "-c"]
      args: ["echo 'Quick task'; sleep 2"]

  - name: slow-step
    # Template-level timeout: 5 seconds (shorter than the task duration)
    activeDeadlineSeconds: 5
    container:
      image: alpine
      command: ["sh", "-c"]
      args: ["echo 'Starting slow task...'; sleep 30"]
```

## Explanation of the example

1. The workflow spec sets a total timeout of 60 seconds.
2. The `main` template runs two sequential steps: `quick-task` (uses `fast-step`) and `slow-task` (uses `slow-step`).
3. `fast-step` sets activeDeadlineSeconds to 100 seconds, which is longer than the workflow-level 60s. Because `fast-step` itself only sleeps 2 seconds, it completes successfully before any timeout is reached.
4. `slow-step` sets activeDeadlineSeconds to 5 seconds but runs `sleep 30`. Kubernetes will terminate the pod for `slow-step` after \~5 seconds with an event like: "Pod was active on the node longer than the specified deadline." That step will be marked failed.
5. When a child step fails (for example due to pod termination for timeout), the workflow will typically be marked failed unless you configure retries, continueOn, or exit handlers to alter that behavior.

## Quick reference table

| Resource               | Purpose                                                           | Example                                |
| ---------------------- | ----------------------------------------------------------------- | -------------------------------------- |
| Workflow-level timeout | Bound the entire workflow runtime (enforced by Argo controller)   | `spec.activeDeadlineSeconds: 60`       |
| Template-level timeout | Bound an individual template/pod runtime (enforced by Kubernetes) | `templates[].activeDeadlineSeconds: 5` |

> **warning** Important: activeDeadlineSeconds is an integer number of seconds. Template-level timeouts usually translate to the pod's activeDeadlineSeconds and will be enforced by Kubernetes; the workflow-level timeout is enforced by the Argo controller. Ensure you pick values that reflect the longest acceptable runtime for each scope and test how retries or continueOn affect behavior.

## Best practices

* Use workflow-level activeDeadlineSeconds to prevent runaway workflows and control resource consumption.
* Use template-level activeDeadlineSeconds for steps that you know can hang or take unpredictably long.
* Combine both levels to provide both per-step protection and an overall safety net.
* When using template-level timeouts, add logs or artifacts early in the template so failures due to timeouts are diagnosable.
* If a specific task is prone to transient failures, consider retries with backoff rather than only relying on deadlines.

## Links and references

* [Argo Workflows - Timeouts and Retries](https://argoproj.github.io/argo-workflows/fields/#activedeadlineseconds)
* [Kubernetes - Pod activeDeadlineSeconds](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-disruption-and-deletion)
* [Argo Workflows Documentation](https://argoproj.github.io/argo-workflows/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/de9d8db6-8441-41fb-a873-3c8024ab6d6c)
