# Demo Retry

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Demo-Retry/page

Demonstrates adding retry strategies with exponential backoff to Argo Workflows using a flaky task

This demo demonstrates how to add a retry strategy to Argo Workflows using a flaky task that sometimes fails and sometimes succeeds. The example shows an entrypoint `main` with a single step that runs the `unstable-step` template. The container script generates a pseudo-random number (based on epoch seconds) and only succeeds when that number is zero (roughly a 33% chance on any attempt).

## Workflow (no retries)

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
    container:
      image: alpine
      command: ["sh", "-c"]
      args:
      - |
        echo "Attempt {{retries}}"
        RANDOM_NUM=$(( $(date +%s) % 3 ))
        if [ $RANDOM_NUM -eq 0 ]; then
          echo "Success!"
          exit 0
        else
          echo "Failed, will retry..."
          exit 1
        fi
```

Explanation of the container script:

* RANDOM\_NUM is computed from the current epoch seconds modulo 3, producing 0, 1, or 2.
* If RANDOM\_NUM == 0 the script prints "Success!" and exits 0.
* Otherwise the script prints "Failed, will retry..." and exits 1.
* Because of this logic, each attempt has about a 33% chance to succeed.

By default, a failed step will not be retried automatically. To give the step more chances, add a `retryStrategy` to the template.

## Workflow with retryStrategy (exponential backoff)

Below is the same workflow with a retry strategy that limits retries and uses exponential backoff:

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
      limit: 3              # Retry up to 3 times
      retryPolicy: "Always" # Options: Always, OnFailure, OnError, OnTransientError
      backoff:
        duration: "5s"      # Initial wait before the first retry
        factor: 2           # Multiply wait by this factor for each subsequent retry
        maxDuration: "1m"   # Cap the wait time at this duration
    container:
      image: alpine
      command: ["sh", "-c"]
      args:
      - |
        echo "Attempt {{retries}}"
        RANDOM_NUM=$(( $(date +%s) % 3 ))
        if [ $RANDOM_NUM -eq 0 ]; then
          echo "Success!"
          exit 0
        else
          echo "Failed, will retry..."
          exit 1
        fi
```

## retryStrategy fields — quick reference

| Field               | Purpose                                                          | Example / Notes                                      |
| ------------------- | ---------------------------------------------------------------- | ---------------------------------------------------- |
| limit               | Maximum number of retries (does not include the initial attempt) | `3`                                                  |
| retryPolicy         | When to retry                                                    | `Always`, `OnFailure`, `OnError`, `OnTransientError` |
| backoff.duration    | Initial wait time before the first retry                         | `"5s"`                                               |
| backoff.factor      | Multiplier applied to the wait each retry (exponential backoff)  | `2`                                                  |
| backoff.maxDuration | Maximum cap on the backoff wait                                  | `"1m"`                                               |

Details on retryPolicy options:

* Always: retry on any non-zero exit (failures or errors).
* OnFailure: retry only when the step exits with a failure code.
* OnError: retry on internal engine errors.
* OnTransientError: retry only for transient errors (for example, temporary network/TLS issues).

> **lightbulb** Argo template variables such as  can be used in the container command/args to show which attempt is running.

## Example log flow with retries

* First attempt (Attempt 0) fails → workflow waits according to backoff → second attempt (Attempt 1) runs.
* If Attempt 1 succeeds you will see:

```text theme={null}
Attempt 1
Success!
```

If subsequent attempts also fail, you will see additional "Attempt N" lines and the container's output for each run until the retry limit is reached or the task succeeds.

## When to use retries

Use retries for steps that are prone to transient or intermittent failures, such as:

* Intermittent network issues when calling external APIs.
* Temporary TLS or certificate handshake failures.
* Short-lived service outages in dependent systems.

Retries with exponential backoff prevent immediately failing workflows and reduce pressure on external services by spacing retry attempts.

## References

* Argo Workflows — RetryStrategy: [https://argoproj.github.io/argo-workflows/workflows/retries/](https://argoproj.github.io/argo-workflows/workflows/retries/)
* Argo Workflows Documentation: [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/61233f32-f908-4466-9cb1-f02671eb1fbc)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/5c948821-5400-4cb2-8f05-dd37f3d723f2)
