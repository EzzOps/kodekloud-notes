# Demo Progressive Delivery with Argo Rollouts

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/GitOps-and-Continuous-Delivery/Demo-Progressive-Delivery-with-Argo-Rollouts/page

Guide to Argo Rollouts for Kubernetes, demonstrating canary progressive delivery, image updates, promotion, rollback, and attaching rollouts to existing Deployments via workloadRef

Deploying new versions to production can be risky: push a bad image and all pods may be replaced at once, causing user-facing errors. Progressive delivery gives you control over how a new version is introduced — shift a small percentage of traffic first, observe health and metrics, then gradually increase exposure. If anything looks wrong, abort and traffic returns to the stable revision.

Argo Rollouts implements progressive delivery for Kubernetes as a drop-in replacement for Deployments. This walkthrough shows how to:

* Verify Argo Rollouts is running
* Create a Rollout (canary strategy with weights and pauses)
* Perform a canary release by updating the image and promoting
* Attach a Rollout to an existing Deployment using `workloadRef`

***

## Verify Argo Rollouts is running

Confirm the Argo Rollouts controller and dashboard are up:

```bash theme={null}
controlplane ➜ kubectl get pods -n argo-rollouts
NAME                                           READY   STATUS    RESTARTS   AGE
argo-rollouts-5f64f8d68-1xr9s                  1/1     Running   0          10m
argo-rollouts-dashboard-755bbc64c-59rhx        1/1     Running   0          10m
```

***

## Create a Rollout — basic structure

A `Rollout` resource closely resembles a `Deployment`. The main difference is the `strategy` section, which defines canary or blue/green progressive delivery behavior.

Here is a minimal Rollout that behaves like a regular Deployment:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: rollout-demo
  namespace: canary-demo
spec:
  replicas: 4
  selector:
    matchLabels:
      app: rollout-demo
  template:
    metadata:
      labels:
        app: rollout-demo
    spec:
      containers:
        - name: demo
          image: argoproj/rollouts-demo:blue
          ports:
            - containerPort: 8080
```

To enable canary-style progressive delivery, add a `strategy.canary.steps` sequence. The example below progresses 25% → pause → 50% → pause → 75% → pause → 100%:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: rollout-demo
  namespace: canary-demo
spec:
  replicas: 4
  selector:
    matchLabels:
      app: rollout-demo
  template:
    metadata:
      labels:
        app: rollout-demo
    spec:
      containers:
        - name: demo
          image: argoproj/rollouts-demo:blue
          ports:
            - containerPort: 8080
  strategy:
    canary:
      steps:
        - setWeight: 25
        - pause: {}
        - setWeight: 50
        - pause: {}
        - setWeight: 75
        - pause: {}
        - setWeight: 100
```

Apply the Rollout:

```bash theme={null}
controlplane ➜ kubectl apply -f rollout.yaml
rollout.argoproj.io/rollout-demo created
```

Inspect the rollout using the Argo Rollouts kubectl plugin:

```bash theme={null}
controlplane ➜ kubectl argo rollouts get rollout rollout-demo -n canary-demo
Name:               rollout-demo
Namespace:          canary-demo
Status:             Healthy
Strategy:           Canary
Step:               1/4
SetWeight:          0
ActualWeight:       0
Images:             argoproj/rollouts-demo:blue (stable)

Replicas:
  Desired: 4
  Current: 4
  Ready:   4
  Available: 4
```

***

## Promote and update the image (canary release)

Promoting a rollout advances it to the next defined step. Running `promote` with no image change will not progress a revision (there is no new revision to advance):

```bash theme={null}
controlplane ➜ kubectl argo rollouts promote rollout-demo -n canary-demo
rollout 'rollout-demo' promoted
```

To create a canary release, update the container image (for example, `blue` → `yellow`) in `rollout.yaml`, then apply the change:

```bash theme={null}
