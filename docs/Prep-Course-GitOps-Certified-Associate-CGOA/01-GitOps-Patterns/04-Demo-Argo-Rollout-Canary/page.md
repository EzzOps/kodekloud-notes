# Demo Argo Rollout Canary

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Patterns/Demo-Argo-Rollout-Canary/page

Guide demonstrating Argo Rollouts canary deployments for gradual traffic shifting, including Rollout manifests, setWeight steps, pauses, promotion, inspection, and rollback commands.

In this lesson we demonstrate how to perform a gradual release using the canary deployment model provided by Argo Rollouts. Argo Rollouts extends Kubernetes Deployments with more control over update behavior — enabling canary, blue-green, and progressive delivery strategies. The canary strategy routes a percentage of traffic to a new revision and increases that percentage in controlled steps with optional pauses for validation.

<Frame>
  <img alt="The image shows a webpage titled &#x22;Canary Deployment Strategy&#x22; from Argo Rollouts, discussing a method for gradually releasing a new software version. It includes an overview and table of contents on the right." />
</Frame>

## Rollout manifest (canary strategy) — overview

A Rollout manifest (kind: `Rollout`) looks like a Deployment but gives you fine-grained control of updates. Instead of replacing all pods at once, the canary strategy lets you increment traffic using `setWeight` steps and `pause` actions (timed or indefinite).

Example Rollout (illustrative):

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: example-rollout
spec:
  replicas: 10
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.15.4
          ports:
            - containerPort: 80
  minReadySeconds: 30
  revisionHistoryLimit: 3
  strategy:
    canary:
      maxSurge: 25%
      maxUnavailable: 0
      steps:
        - setWeight: 10
          pause:
            duration: 1h
        - setWeight: 20
          pause: {} # pause indefinitely until manual promotion
```

Pause duration formats supported: seconds (`10s`), minutes (`10m`), hours (`1h`), or an empty object (`{}`) for an indefinite (manual) pause:

```yaml theme={null}
spec:
  strategy:
    canary:
      steps:
        - pause: { duration: 10s }  # 10 seconds
        - pause: { duration: 10m }  # 10 minutes
        - pause: { duration: 1h }   # 1 hour
        - pause: {}                 # pause indefinitely (manual promotion)
```

<Callout icon="warning">
  A `pause: {}` is an indefinite pause — the rollout will wait until you manually promote the next step (UI or `kubectl argo rollouts promote`). Plan for manual verification before continuing.
</Callout>

### Blue-green (reference snippet)

For comparison, here is a sample blue-green configuration (used for preview/promotion workflows):

```yaml theme={null}
revisions: 3
strategy:
  blueGreen:
    activeService: active-service
    previewService: preview-service
    previewReplicaCount: 1
    autoPromotionEnabled: false
    prePromotionAnalysis:
      templates:
        - templateName: success-rate
          args:
            - name: service-name
              value: guestbook-svc.default.svc.cluster.local
    postPromotionAnalysis:
      templates:
        - templateName: success-rate
          args:
            - name: service-name
              value: guestbook-svc.default.svc.cluster.local
```

## Applying the canary example from the repository

This repository contains a `patterns/canary/` folder with `rollout.yml` and `service.yml`. Below are the manifests used in the demo.

Initial `rollout.yml` (canary steps):

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: app-rollout
  namespace: canary
spec:
  replicas: 10
  selector:
    matchLabels:
      app: app-rollout
  template:
    metadata:
      labels:
        app: app-rollout
    spec:
      containers:
        - name: app
          image: siddharth67/app:v1
  strategy:
    canary:
      steps:
        - setWeight: 20
          pause: {}
        - setWeight: 40
          pause:
            duration: 1m
        - setWeight: 60
          pause:
            duration: 1m
        - setWeight: 80
          pause:
            duration: 1m
```

For demo speed we adjusted timed pauses to `10s` so the rollout completes faster:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: app-rollout
  namespace: canary
spec:
  replicas: 10
  selector:
    matchLabels:
      app: app-rollout
  template:
    metadata:
      labels:
        app: app-rollout
    spec:
      containers:
        - name: app
          image: siddharth67/app:v1
  strategy:
    canary:
      steps:
        - setWeight: 20
        - pause: {}
        - setWeight: 40
        - pause:
            duration: 10s
        - setWeight: 60
        - pause:
            duration: 10s
        - setWeight: 80
        - pause:
            duration: 10s
```

Commands to create the namespace and apply the manifests:

```bash theme={null}
