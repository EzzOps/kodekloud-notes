# task.tekton.dev/hello-task created
```

Start the Task and stream logs with `tkn`:

```bash theme={null}
tkn task start hello-task -n ci-pipelines --showlog
```

Example output:

```plaintext theme={null}
TaskRun started: hello-task-run-qxq4n
Waiting for logs to be available...
[say-hello] Hello from KodeKloud!
```

This TaskRun is an instantiation of the Task we defined.

## Make the Task reusable with a parameter

Replace the hard-coded message with a `message` parameter so the Task can be reused:

```yaml theme={null}
apiVersion: tekton.dev/v1
kind: Task
metadata:
  name: hello-task
  namespace: ci-pipelines
spec:
  params:
    - name: message
      type: string
      default: "Hello from KodeKloud!"
  steps:
    - name: say-hello
      image: alpine:3.18
      script: |
        echo "$(params.message)"
```

Apply the updated Task:

```bash theme={null}
kubectl apply -f hello-task.yaml
# task.tekton.dev/hello-task configured
```

Start the Task without passing a parameter — it will use the default:

```bash theme={null}
tkn task start hello-task -n ci-pipelines --showlog
```

Output:

```plaintext theme={null}
TaskRun started: hello-task-run-qx4h
Waiting for logs to be available...
[say-hello] Hello from KodeKloud!
```

Pass a custom message using `-p`:

```bash theme={null}
tkn task start hello-task -n ci-pipelines -p message="Hello from Nourhan!" --showlog
```

Output:

```plaintext theme={null}
TaskRun started: hello-task-run-rzjzf
Waiting for logs to be available...
[say-hello] Hello from Nourhan!
```

Note: the `-p` parameter format is `-p name="value"`.

## Create a multi-step build Task

A realistic CI Task runs multiple sequential steps (clone → build → test). Define a `build-task` that accepts an `app-name` parameter and runs three steps that print indicative messages:

`build-task.yaml`:

```yaml theme={null}
apiVersion: tekton.dev/v1
kind: Task
metadata:
  name: build-task
  namespace: ci-pipelines
spec:
  params:
    - name: app-name
      type: string
  steps:
    - name: clone
      image: alpine:3.18
      script: |
        echo "Cloning repo for $(params.app-name)"
    - name: build
      image: alpine:3.18
      script: |
        echo "Building $(params.app-name)"
    - name: test
      image: python:3.11-alpine
      script: |
        echo "Running tests for $(params.app-name)"
```

Apply the Task:

```bash theme={null}
kubectl apply -f build-task.yaml
# task.tekton.dev/build-task created
```

Start the TaskRun and pass `app-name`:

```bash theme={null}
tkn task start build-task -n ci-pipelines -p app-name="web-server" --showlog
```

Output (steps run sequentially):

```plaintext theme={null}
TaskRun started: build-task-run-sk277
Waiting for logs to be available...
[clone] Cloning repo for web-server
[build] Building web-server
[test] Running tests for web-server
```

Each step runs in sequence; choose images tailored to the step (e.g., a git image for clone, build tool images for compilation, test runners for tests).

## Create a deploy Task

Create a Task that deploys a named app to an environment. It accepts `app-name` and `environment` (default `staging`).

`deploy-task.yaml`:

```yaml theme={null}
apiVersion: tekton.dev/v1
kind: Task
metadata:
  name: deploy-task
  namespace: ci-pipelines
spec:
  params:
    - name: app-name
      type: string
    - name: environment
      type: string
      default: staging
  steps:
    - name: deploy
      image: alpine:3.18
      script: |
        echo "Deploying $(params.app-name) to $(params.environment)"
```

Apply it:

```bash theme={null}
kubectl apply -f deploy-task.yaml
# task.tekton.dev/deploy-task created
```

## Wire Tasks into a Pipeline

Create a Pipeline that runs `build-task` first, then `deploy-task`. The Pipeline accepts `app-name` and `target-env`, and passes them into the Tasks.

`pipeline.yaml`:

```yaml theme={null}
apiVersion: tekton.dev/v1
kind: Pipeline
metadata:
  name: ci-pipeline
  namespace: ci-pipelines
spec:
  params:
    - name: app-name
      type: string
    - name: target-env
      type: string
      default: staging
  tasks:
    - name: build
      taskRef:
        name: build-task
      params:
        - name: app-name
          value: $(params.app-name)
    - name: deploy
      runAfter:
        - build
      taskRef:
        name: deploy-task
      params:
        - name: app-name
          value: $(params.app-name)
        - name: environment
          value: $(params.target-env)
```

Apply the Pipeline:

```bash theme={null}
kubectl apply -f pipeline.yaml
# pipeline.tekton.dev/ci-pipeline created
```

Start a PipelineRun and stream logs:

```bash theme={null}
tkn pipeline start ci-pipeline \
  -n ci-pipelines \
  -p app-name="webserver" \
  -p target-env="prod" \
  --showlog
```

Expected output:

```plaintext theme={null}
PipelineRun started: ci-pipeline-run-vjx7b
Waiting for logs to be available...
[build : clone] Cloning repo for webserver
[build : build] Building webserver
[build : test] Running tests for webserver
[deploy : deploy] Deploying webserver to prod
```

<Frame>
  <img alt="The image displays the Tekton Dashboard with a list of tasks, showing task names, namespaces, and creation times. It includes options for filtering and managing tasks in a CI pipeline context." />
</Frame>

The PipelineRun executed the `build` Task (three sequential steps) followed by the `deploy` Task. You can inspect TaskRun logs and statuses from the CLI or Dashboard.

<Frame>
  <img alt="The image shows a Tekton Dashboard with a successful pipeline run named &#x22;ci-pipeline-run-ds8l4-build,&#x22; displaying logs with tasks labeled &#x22;clone,&#x22; &#x22;build,&#x22; and &#x22;test.&#x22;" />
</Frame>

## Tekton Dashboard

Tekton provides a [Dashboard](https://tekton.dev/docs/dashboard/) UI for visualizing pipelines and runs. From the Dashboard you can:

* View Pipelines, PipelineRuns, Tasks, and TaskRuns.
* Inspect logs, parameters, statuses, and related Pods.
* Instantiate TaskRuns and PipelineRuns (subject to cluster RBAC).

The Dashboard complements CLI workflows and is useful for debugging and auditing CI/CD runs.

## Next steps and extensions

Once you master Tasks and Pipelines:

* Replace demo `echo` scripts with real clone/build/test/deploy steps.
* Add Workspaces to share files/artifacts between steps.
* Integrate image registries, results, conditions, or custom cluster resources.
* Secure access via RBAC and configure Tekton Triggers for event-driven runs.

## Links and References

* [Tekton Pipelines documentation](https://tekton.dev/docs/)
* [Tekton CLI (`tkn`)](https://tekton.dev/docs/cli/)
* [Tekton Dashboard](https://tekton.dev/docs/dashboard/)
* [kubectl reference](https://kubernetes.io/docs/reference/kubectl/overview/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/dff5382b-dbe7-4cac-bd2b-d5a47028945e/lesson/231fc569-3421-4ad0-9aa7-8c5fff348d7e)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/dff5382b-dbe7-4cac-bd2b-d5a47028945e/lesson/f963fc71-6121-47e8-89a4-681bf8bc36a8)


# GitOps Explained Desired State Drift and Reconciliation

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/GitOps-and-Continuous-Delivery/GitOps-Explained-Desired-State-Drift-and-Reconciliation/page

Explains GitOps principles, the declarative desired state model, reconciliation loop, drift detection and self healing, and the four pillars enabling secure auditable continuous delivery.

Welcome to the GitOps and Continuous Delivery lesson.

Scenario: It's 2 a.m. and your pager goes off — production is down. You SSH into the cluster to investigate, but something changed and you have no record of what, when, or who. You're flying blind. This is the world before GitOps.

In this lesson you'll learn:

* The problems GitOps solves,
* The four pillars of GitOps,
* How the reconciliation loop functions, and
* How drift detection and self-healing work.

<Frame>
  <img alt="The image lists four learning objectives related to GitOps, including understanding its problems, defining its pillars, explaining the reconciliation loop, and understanding drift detection and self-healing strategies." />
</Frame>

Why incidents like this occur

Many Kubernetes environments grant developers direct `kubectl` access to production. That enables ad-hoc, imperative changes from developers' laptops. Those changes are applied directly, often without a centralized audit trail or version history.

Example (imperative action):

```bash theme={null}
