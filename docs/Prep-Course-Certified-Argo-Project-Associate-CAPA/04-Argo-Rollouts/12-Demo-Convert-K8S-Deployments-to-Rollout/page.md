# Demo Convert K8S Deployments to Rollout

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Rollouts/Demo-Convert-K8S-Deployments-to-Rollout/page

Guide to converting a Kubernetes Deployment into an Argo Rollout using workloadRef, enabling blue green or canary strategies and controlling original Deployment scale down behavior

In this lesson we'll convert an existing Kubernetes Deployment into an Argo Rollout so the Argo Rollouts controller can manage lifecycle and rollout strategy (for example, blue/green or canary). This approach lets you adopt an existing Deployment without rewriting the pod template by using workloadRef.

<Frame>
  <img alt="A blue-gradient presentation slide with the centered title &#x22;K8S Deployment to Rollout.&#x22; Small copyright text &#x22;Copyright KodeKloud&#x22; appears in the lower-left corner." />
</Frame>

Overview

* Replace the Deployment kind with an argoproj.io/v1alpha1 Rollout so Argo Rollouts manages the resource.
* Use spec.workloadRef to point the Rollout to an existing Deployment (no pod-template rewrite needed).
* Configure spec.workloadRef.scaleDown to control what happens to the original Deployment after the Rollout succeeds.
* Choose a rollout strategy; this example uses blueGreen and requires activeService (previewService is optional).

Key parts explained

| Field                      | Purpose                                                                                  | Example / Notes                                                      |
| -------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| apiVersion / kind          | Instructs Kubernetes to treat this as an Argo Rollout managed resource                   | `argoproj.io/v1alpha1 / Rollout`                                     |
| spec.replicas              | Number of desired replicas for the Rollout                                               | Same concept as Deployment                                           |
| spec.workloadRef           | Adopts an existing Deployment so the Rollout uses the same pod template                  | `apiVersion: apps/v1`, `kind: Deployment`, `name: <deployment-name>` |
| spec.workloadRef.scaleDown | Policy to control scaling behavior of the original Deployment after successful rollout   | `onSuccess`, `never`, `progressive` (see table below)                |
| spec.strategy.blueGreen    | Blue/green rollout configuration; `activeService` is required, `previewService` optional | Provides traffic promotion and internal preview testing              |

scaleDown option summary

| Option      | Behavior                                                                               |
| ----------- | -------------------------------------------------------------------------------------- |
| onSuccess   | Controller scales the original Deployment to zero after the Rollout becomes healthy.   |
| never       | Controller does not scale down the original Deployment. Use when you want both to run. |
| progressive | Controller gradually scales down the original Deployment alongside the Rollout.        |

Example Rollout manifest

* This manifest adopts an existing Deployment named `highway-animation-1` and performs a blue/green rollout using `activeService` and `previewService`.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: highway-animation-rollout
  namespace: beta
spec:
  replicas: 4
  workloadRef:
    apiVersion: apps/v1
    kind: Deployment
    name: highway-animation-1
    scaleDown: onSuccess
  strategy:
    blueGreen:
      activeService: highway-bluegreen-active
      previewService: highway-bluegreen-preview
```

What happens when you apply this

* The Rollout resource takes control of the specified Deployment (it "adopts" it).
* The Rollout controller will create new ReplicaSets/Pods for the rollout while the original Deployment pods remain until scaleDown policy executes.
* With `scaleDown: onSuccess`, when the Rollout becomes healthy the controller scales the original Deployment to zero, leaving the Rollout-managed pods servicing traffic.

Apply the Rollout and observe the cluster

1. Initial state (plain Deployment running four replicas):

```bash theme={null}
