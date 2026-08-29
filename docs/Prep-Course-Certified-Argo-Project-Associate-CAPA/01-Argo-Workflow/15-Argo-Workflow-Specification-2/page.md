# Argo Workflow Specification 2

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Argo-Workflow-Specification-2/page

Guide to Argo Workflows features and patterns covering conditional execution, background daemons, timeouts, exit handlers, retry strategies, and resource success/failure polling with practical YAML examples

This lesson expands on practical Argo Workflows fields: when, daemon, activeDeadlineSeconds, onExit, retryStrategy, and resource success/failure conditions. Each section includes a clear explanation, real-world YAML examples, and guidance for common patterns.

***

## When

The `when` expression controls conditional step execution. Evaluate parameters, previous step outputs, or workflow status to skip steps dynamically. If the expression resolves to false, the step is skipped—making `when` the primary built-in branching mechanism for simple if/then/else logic in Argo Workflows.

Example: run tests only in non-production environments.

```yaml theme={null}
spec:
  entrypoint: main
  arguments:
    parameters:
      - name: environment
        value: "production"
  templates:
    - name: main
      steps:
        - - name: build
            template: build-step
          - name: test
            template: test-step
            when: "{{workflow.parameters.environment}} != production" # Only run in non-prod
          - name: deploy
            template: deploy-step

    - name: build-step
      container:
        image: alpine
        command: [sh, -c]
        args: ["echo 'Building application...'"]

    - name: test-step
      container:
        image: alpine
        command: [sh, -c]
        args: ["echo 'Running tests...'"]

    - name: deploy-step
      container:
        image: alpine
        command: [sh, -c]
        args: ["echo 'Deploying to {{workflow.parameters.environment}}'"]
```

> **lightbulb** Use `when` for lightweight branching. For more complex logic, combine `when`
  with parameters and outputs from previous steps or use conditional templates.

***

## Daemon

A daemon template runs a container in the background (service mode). The workflow does not wait for a daemon step to exit. This is useful for temporary services (databases, mock APIs) that other steps need while they run.

Example: start Redis in the background and run tests that connect to it.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: daemon-workflow
  namespace: argo
spec:
  entrypoint: main
  templates:
    - name: main
      steps:
        - - name: start-database
            template: mock-database
          - name: run-tests
            template: test-step

    - name: mock-database
      daemon: true # Keeps this container running in the background
      container:
        image: redis:alpine
        command: ["redis-server"]
        readinessProbe:
          tcpSocket:
            port: 6379
          initialDelaySeconds: 5
          periodSeconds: 5

    - name: test-step
      container:
        image: alpine
        command: [sh, -c]
        args: ["echo 'Testing against database...'; sleep 3"]
```

Daemons are automatically terminated when the workflow finishes. This pattern is ideal when you need a short-lived service reachable by other steps during workflow execution.

***

## activeDeadlineSeconds (timeouts)

`activeDeadlineSeconds` sets a maximum runtime for a template or the entire workflow. When the limit is exceeded, Argo terminates the step or workflow and marks it failed—preventing hung workloads from consuming cluster resources.

Example: global workflow timeout with per-template overrides.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: timeout-workflow
  namespace: argo
spec:
  entrypoint: main
  activeDeadlineSeconds: 600 # Timeout after 600 seconds
  templates:
    - name: main
      steps:
        - - name: quick-task
            template: fast-step
          - name: slow-task
            template: slow-step

    - name: fast-step
      activeDeadlineSeconds: 100 # Timeout after 100 seconds
      container:
        image: alpine
        command: [sh, -c]
        args: ["echo 'Quick task'; sleep 2"]

    - name: slow-step
      activeDeadlineSeconds: 5 # This will timeout
      container:
        image: alpine
        command: [sh, -c]
        args: ["echo 'Starting slow task...'; sleep 30"]
```

Notes:

* Workflow-level `activeDeadlineSeconds` applies to the whole run.
* Template-level settings override the workflow-level timeout for that template.
* Use conservative timeouts to avoid prematurely killing long-running valid work.

***

## onExit (exit handler)

`onExit` sets an exit handler that always runs at the end of a workflow—whether it succeeded, failed, or was terminated. Use it for cleanup, alerts, or final audit logging. Inside the exit handler you can inspect variables like `{{workflow.status}}` to determine the final state.

Example: always run a cleanup template that reports the workflow status.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: exit-handler-workflow
  namespace: argo
spec:
  entrypoint: main
  onExit: cleanup # Always run this template at the end

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

`onExit` runs even when the workflow is terminated externally, making it a reliable place to free resources or post a final summary.

***

## retryStrategy

`retryStrategy` enables automatic retries for failing steps. Configure retry limit, retry policy, and backoff settings (initial duration, multiplier, and max backoff). This is essential for handling transient failures (network flakiness, intermittent external service errors).

Example: retry up to 3 times with exponential backoff.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: retry-workflow
  namespace: argo
spec:
  entrypoint: main
  templates:
    - name: main
      steps:
        - - name: flaky-task
            template: unstable-step

    - name: unstable-step
      retryStrategy:
        limit: 3 # Retry up to 3 times
        retryPolicy: "Always" # Options: Always, OnFailure, OnError, OnTransientError
        backoff:
          duration: "5s" # Start with 5 second wait
          factor: 2 # Double the wait each retry
          maxDuration: "1m" # Cap at 1 minute wait
      container:
        image: alpine
        command: [sh, -c]
        args:
          - |
            echo "Attempt {{retries}}"
            RANDOM_NUM=$((RANDOM % 3))
            if [ $RANDOM_NUM -eq 0 ]; then
              echo "Success!"
              exit 0
            else
              echo "Failed, will retry..."
              exit 1
            fi
```

Sample CLI output demonstrating retries:

```bash theme={null}
$ argo -n argo get retry-workflow-5lhgj

STEP
✔ retry-workflow-5lhgj
├✔ flaky-task
└✖ flaky-task(0)
  ✔ flaky-task(1)
```

With the configured backoff, retries occur at \~5s, \~10s, \~20s (factor applied), capped at 1 minute.

> **lightbulb** Use `retryStrategy` for transient failures. Tune `retryPolicy` and backoff to
  match the expected failure profile of your tasks.

***

## Resource template: successCondition and failureCondition

Resource templates allow Argo to create Kubernetes resources and then poll their live status. Use `successCondition` and `failureCondition` to evaluate the resource's status object so the workflow reflects the actual readiness of the resource (not just the API apply success).

* successCondition: expression evaluated against the live resource that marks the step successful when true (e.g., `status.succeeded == 1` for a Job).
* failureCondition: expression evaluated against the live resource that marks the step failed when true (e.g., `status.failed > 3`).

This polling behavior integrates Kubernetes controller state into the workflow's control flow.

Flow example (Job with backoff/failure tracking)

* Argo creates a Job with `backoffLimit: 4` and `failureCondition: status.failed > 3`.
* Argo polls the Job status repeatedly and evaluates success/failure expressions.
* If `status.succeeded == 1` becomes true first → step succeeds.
* If `status.failed > 3` becomes true first → step fails.

ASCII flow:

Initial Setup
Argo creates Job with backoffLimit: 4 and failureCondition: status.failed > 3
Job Status: `{ succeeded: 0, failed: 0 }`

Attempt 1 - Pod Fails
K8s Job Controller:
Creates Pod #1 -> Pod exits with code 1 -> Pod fails

Updates Job: status.failed = 1

Job Status: (succeeded: 0, failed: 1)

Argo Polls Job:
Checks: 1 > 3 ❌ FALSE

Continue waiting...

Attempt 2 - Pod Fails
K8s Job Controller:
Creates Pod #2 -> Pod exits with code 1 -> Pod fails

Updates Job: status.failed = 2

Job Status: (succeeded: 0, failed: 2)

Argo Polls Job:
Checks: 2 > 3 ❌ FALSE

Continue waiting...

Attempt 3 - Pod Fails
K8s Job Controller:
Creates Pod #3 -> Pod exits with code 1 -> Pod fails

Updates Job: status.failed = 3

Job Status: (succeeded: 0, failed: 3)

Argo Polls Job:
Checks: 3 > 3 ❌ FALSE

Continue waiting...

Attempt 4 - Failure Condition Triggered!
K8s Job Controller:
Creates Pod #4 -> Pod exits with code 1 -> Pod fails

Updates Job: status.failed = 4

Job Status: (succeeded: 0, failed: 4)

Argo Polls Job:
Checks: 4 > 3 ✅ TRUE

Failure Condition Met!

Result: Argo marks the resource step as FAILED
Workflow stops or proceeds to onExit handler

Example resource template that waits for a Job to succeed:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: resource-workflow
  namespace: argo
spec:
  entrypoint: main
  serviceAccountName: argo # workflow needs permission to create resources

  templates:
    - name: main
      steps:
        - - name: create-job
            template: job-template

    - name: job-template
      resource:
        action: create
        successCondition: status.succeeded == 1 # Wait until job succeeds
        failureCondition: status.failed > 3 # Fail if job fails > 3 times
        manifest: |
          apiVersion: batch/v1
          kind: Job
          metadata:
            generateName: processing-job-
            namespace: argo
          spec:
            backoffLimit: 4
            template:
              spec:
                containers:
                  - name: processor
                    image: alpine
                    command: [sh, -c]
                    args: ["echo 'Processing data...'; sleep 5"]
                restartPolicy: Never
```

> **warning** Resource templates require the workflow's ServiceAccount to have permissions
  to create and read the resource types used in your manifest. Ensure RBAC is
  configured (create, get, list, watch) for those resources.

Best practices:

* Tailor expressions to each resource kind (Job, Deployment, StatefulSet, etc.). Reference the resource's `.status` schema when writing conditions.
* Prefer conditions that reflect actual readiness (e.g., `status.availableReplicas == spec.replicas` for Deployments).
* Use `failureCondition` to fail fast if the resource enters an unrecoverable state.

***

Quick reference table

| Field                               | Purpose                                           | Typical use-case                                                   |
| ----------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------ |
| when                                | Conditional execution of a step                   | Skip steps based on `{{workflow.parameters}}` or previous outputs  |
| daemon                              | Run container as background service               | Start DB or mock API for parallel consumers                        |
| activeDeadlineSeconds               | Timeout for template or workflow                  | Prevent hung tasks from consuming resources                        |
| onExit                              | Exit handler that always runs                     | Cleanup, notifications, final logging                              |
| retryStrategy                       | Automatic retries with backoff                    | Handle transient failures (network, flaky services)                |
| successCondition / failureCondition | Poll and evaluate live Kubernetes resource status | Wait for Jobs/Deployments to reach desired state before continuing |

***

## Summary

* when: conditional step execution using parameters, outputs, or status.
* daemon: run background services that other steps can use; they are terminated when the workflow ends.
* activeDeadlineSeconds: enforce timeouts at workflow or template level to avoid resource leaks.
* onExit: reliable cleanup/notification handler executed at workflow completion.
* retryStrategy: configure retries and exponential backoff for transient errors.
* resource successCondition / failureCondition: poll and evaluate live Kubernetes resource status so workflow steps reflect the resource's actual state.

Links and references

* Argo Workflows docs: [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)
* Kubernetes Jobs: [https://kubernetes.io/docs/concepts/workloads/controllers/job/](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
* Kubernetes Deployments: [https://kubernetes.io/docs/concepts/workloads/controllers/deployment/](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/96d16716-0a03-433b-aaf8-d860ba04c30c)
