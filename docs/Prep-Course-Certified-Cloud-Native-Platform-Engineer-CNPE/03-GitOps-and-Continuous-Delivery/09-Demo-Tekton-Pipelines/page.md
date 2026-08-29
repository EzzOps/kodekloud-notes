# edit rollout.yaml: containers[0].image = argoproj/rollouts-demo:yellow
controlplane ➜ kubectl apply -f rollout.yaml
rollout.argoproj.io/rollout-demo configured
```

After applying the updated image the Rollout creates a new revision and will advance to the first step (setWeight: 25). One pod (25%) runs the new `yellow` image while the others remain on `blue`:

```bash theme={null}
controlplane ➜ kubectl argo rollouts get rollout rollout-demo -n canary-demo
Name:               rollout-demo
Namespace:          canary-demo
Status:             Degraded/Healthy (depends on checks)
Strategy:           Canary
Step:               1/4
SetWeight:          25
ActualWeight:       25
Images:             argoproj/rollouts-demo:yellow (canary), argoproj/rollouts-demo:blue (stable)

Replicas:
  Desired: 4
  Current: 4
  Ready:   4
  Available: 4
```

You can also inspect pods directly to confirm which revision is running:

```bash theme={null}
controlplane ➜ kubectl get pods -n canary-demo
NAME                                      READY STATUS    AGE
rollout-demo-544bf7c68b-6jh2n             1/1   Running   5m
rollout-demo-544bf7c68b-6lzjz             1/1   Running   5m
rollout-demo-544bf7c68b-7l7dr             1/1   Running   5m
rollout-demo-544bf7c68b-bpbwd             1/1   Running   42s

controlplane ➜ kubectl describe pod -n canary-demo rollout-demo-544bf7c68b-bpbwd | grep -i image
    Image:          argoproj/rollouts-demo:yellow
```

The Argo Rollouts UI also visualizes canary progress and revision distribution. Example UI view:

<Frame>
  <img alt="This is the interface of Argo Rollouts, showing a rollout demo with canary strategy, including steps for weight adjustment and revision details. The rollout status is detailed with sections for steps, summary, containers, and revisions." />
</Frame>

***

## Promote to additional steps (CLI or UI)

Use CLI promote to move through the next pause or next weight:

```bash theme={null}
controlplane ➜ kubectl argo rollouts promote rollout-demo -n canary-demo
rollout 'rollout-demo' promoted
```

Each promote advances to the next step you defined (50% → 75% → 100%). When the Rollout reaches 100% and checks look good, the new revision becomes the stable revision.

You may also use the UI's "Promote Full" option to advance all remaining steps at once.

***

## Rollback

If the canary revision shows regressions, you can roll back from the Argo Rollouts dashboard to the previous stable revision. The UI provides an immediate way to revert so traffic returns to the stable revision.

<Frame>
  <img alt="The image shows a dashboard from the Argo Rollouts system, displaying a canary deployment strategy with various steps, including weight settings and pauses, and information on deployment revisions." />
</Frame>

***

## Manage existing workloads with workloadRef

If you already have an existing `Deployment`, you can let a `Rollout` reference that Deployment via `workloadRef`. This allows adding progressive delivery to an existing workload without replacing the resource.

Create a Deployment (example uses `replicas: 0` initially):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-app
  namespace: canary-demo
spec:
  replicas: 0
  selector:
    matchLabels:
      app: demo-app
  template:
    metadata:
      labels:
        app: demo-app
    spec:
      containers:
        - name: demo-app
          image: argoproj/rollouts-demo:blue
          ports:
            - containerPort: 8080
```

Apply the Deployment:

```bash theme={null}
controlplane ➜ kubectl apply -f deployment.yaml
deployment.apps/demo-app created
```

Create a Rollout that references the existing Deployment via `workloadRef`, and define a canary strategy:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: demo-app-rollout
  namespace: canary-demo
spec:
  replicas: 4
  workloadRef:
    apiVersion: apps/v1
    kind: Deployment
    name: demo-app
  strategy:
    canary:
      steps:
        - setWeight: 10
        - pause: {}
        - setWeight: 50
        - pause: {}
        - setWeight: 100
```

Apply the Rollout:

```bash theme={null}
controlplane ➜ kubectl apply -f workloadref-rollout.yaml
rollout.argoproj.io/demo-app-rollout created
```

The Rollout will reconcile and manage the referenced Deployment, scaling it to the number of replicas configured by the Rollout (for example, from `replicas: 0` up to 4) and shifting traffic according to canary steps:

```bash theme={null}
controlplane ➜ kubectl get pods -n canary-demo
NAME                                     READY   STATUS    AGE
demo-app-677bb5c8-6cxs5                  1/1     Running   53s
demo-app-677bb5c8-c4xg4                  1/1     Running   53s
demo-app-677bb5c8-rbxg4                  1/1     Running   53s
demo-app-677bb5c8-sbkm4                  1/1     Running   53s
```

<Frame>
  <img alt="The image shows the Argo Rollouts user interface displaying a demo application rollout in progress using a canary strategy, with weight settings and revisions detailed." />
</Frame>

***

> **lightbulb** A common YAML mistake is using `step` (singular) instead of the required `steps` (plural) under `spec.strategy.canary`. If you see an error like `unknown field "spec.strategy.canary.step"`, verify you have `steps:` and that each step entry is properly indented.

***

## Quick reference

| Action                       | Command / Note                                            |
| ---------------------------- | --------------------------------------------------------- |
| Check Argo Rollouts pods     | `kubectl get pods -n argo-rollouts`                       |
| Inspect a rollout            | `kubectl argo rollouts get rollout <name> -n <namespace>` |
| Promote canary to next step  | `kubectl argo rollouts promote <name> -n <namespace>`     |
| Attach Rollout to Deployment | use `spec.workloadRef` in the Rollout manifest            |
| UI promote / rollback        | Available in Argo Rollouts dashboard                      |

***

## Next steps & references

Practice the walkthrough: verify Argo Rollouts is installed, create a canary Rollout, update images to trigger revisions, promote step-by-step, and roll back if needed. Add observability and automated analysis (metrics, alerts) to make promotion decisions safer.

* Argo Rollouts documentation: [https://argoproj.github.io/argo-rollouts/](https://argoproj.github.io/argo-rollouts/)
* Argo Rollouts GitHub: [https://github.com/argoproj/argo-rollouts](https://github.com/argoproj/argo-rollouts)

Now you have a compact, hands-on guide: verify Argo Rollouts, create and apply a canary Rollout, perform controlled image updates and promotions, roll back when necessary, and attach Rollouts to pre-existing Deployments with `workloadRef`.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/dff5382b-dbe7-4cac-bd2b-d5a47028945e/lesson/a0077fb2-6b11-4efb-a3e6-a2eb38e6b16e)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/dff5382b-dbe7-4cac-bd2b-d5a47028945e/lesson/52cac868-334e-4f7b-8cf5-be4a61331d73)


# Demo Tekton Pipelines

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/GitOps-and-Continuous-Delivery/Demo-Tekton-Pipelines/page

A hands on demo of Tekton Pipelines showing how to create reusable Tasks, Pipelines, and run builds and deployments in Kubernetes using tkn and the Tekton Dashboard

[Tekton](https://tekton.dev/docs/) is a Kubernetes-native CI/CD system. Rather than running an external CI server, Tekton runs as custom resources inside your cluster: controllers, Pipelines, Tasks, TaskRuns, and PipelineRuns all live in Kubernetes.

Key concepts at a glance:

|              Resource | Purpose                                                                  | Example / Notes                        |
| --------------------: | ------------------------------------------------------------------------ | -------------------------------------- |
|                  Task | A unit of work composed of one or more steps (containers or scripts).    | Use for build/test/deploy steps.       |
|              Pipeline | A sequence that wires Tasks together and passes parameters between them. | Orchestrates Tasks and their ordering. |
| TaskRun / PipelineRun | Concrete executions (instances) of a Task or Pipeline.                   | `tkn` shows logs and status for runs.  |

In this guide you'll:

* Verify Tekton is running in your cluster.
* Create a minimal Task and run it.
* Make the Task reusable with parameters.
* Build a multi-step Task (clone → build → test).
* Add a deploy Task and wire everything into a Pipeline.
* Run the Pipeline and view logs.

> **lightbulb** You need `kubectl` access to the cluster and the `tkn` CLI installed/configured to follow the examples that use `tkn` commands and `--showlog`. See the Tekton docs and Kubernetes docs linked in the References section below.

> **warning** Examples assume resources are created in the `ci-pipelines` namespace. Create it beforehand if it doesn't exist: `kubectl create namespace ci-pipelines`. Ensure your user has the necessary RBAC permissions to create Tekton resources and view logs.

## Verify Tekton Pipelines is running

Check the Tekton pods in the `tekton-pipelines` namespace:

```bash theme={null}
kubectl get pods -n tekton-pipelines
```

Example output:

```plaintext theme={null}
NAME                                         READY   STATUS    RESTARTS   AGE
tekton-dashboard-7c54d984dd-rj9gv            1/1     Running   0          31m
tekton-events-controller-5cbc777ccd-hd47v    1/1     Running   0          31m
tekton-pipelines-controller-5f567589-1g9v    1/1     Running   0          31m
tekton-pipelines-webhook-75cd84877-mfknj     1/1     Running   0          31m
```

If the controllers and webhook are up and Running, you're ready to create Tasks.

## Create a minimal Task

Create `hello-task.yaml` with a single step that prints a message:

```yaml theme={null}
apiVersion: tekton.dev/v1
kind: Task
metadata:
  name: hello-task
  namespace: ci-pipelines
spec:
  steps:
    - name: say-hello
      image: alpine:3.18
      script: |
        echo "Hello from KodeKloud!"
```

Apply the Task:

```bash theme={null}
kubectl apply -f hello-task.yaml
