# or explicitly
kubectl apply -f rollout.yml -n blue-green
kubectl apply -f service.yml -n blue-green
```

Verify resources:

```bash theme={null}
kubectl -n blue-green get all
```

Expected sample output (consolidated):

* 10 pods for the current ReplicaSet
* Two services with NodePort mappings
* A ReplicaSet that reflects the current revision

```text theme={null}
NAME                                        READY   STATUS    RESTARTS   AGE
pod/highway-bluegreen-674c49d44d-2xp7m     1/1     Running   0          2m
...
pod/highway-bluegreen-674c49d44d-zf58b     1/1     Running   0          2m

NAME                                 TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
service/highway-bluegreen-active     NodePort   10.110.42.78     <none>        3000:30920/TCP      2m
service/highway-bluegreen-preview    NodePort   10.110.199.112   <none>        3000:31981/TCP      2m

NAME                                     DESIRED   CURRENT   READY   AGE
replicaset.apps/highway-bluegreen-674c49d44d   10        10        10      2m
```

Note: Because both services initially use the same selector, both will route to the same pods (blue). Production traffic is served through the activeService.

Introducing a new version (green)

1. Update the Rollout manifest image to the green tag, for example:

```yaml theme={null}
# change this in the Rollout template spec
image: siddharth67/highway-animation:green
```

2. Apply the updated rollout manifest:

```bash theme={null}
kubectl apply -f rollout.yml -n blue-green
```

Behavior:

* With autoPromotionEnabled: false, Argo Rollouts creates a new ReplicaSet for the green version and updates the previewService to select the new ReplicaSet.
* Both ReplicaSets run in parallel (10 blue + 10 green), so you’ll see \~20 pods while both versions are active.
* activeService continues to serve the blue pods (production). previewService points to the green pods for validation.

Verify pods:

```bash theme={null}
kubectl -n blue-green get pods
```

Promote the new version to production

* Use the Argo Rollouts UI, or the kubectl plugin:

```bash theme={null}
kubectl argo rollouts promote highway-bluegreen -n blue-green
```

After promotion, the rollout controller updates the activeService to point at the green ReplicaSet. Production traffic is now routed to the green pods.

Rollback

* If the green version has issues, you can rollback to a previous revision using the Argo Rollouts UI or CLI. The controller keeps revision history (controlled by revisionHistoryLimit), which enables safe rollbacks.

<Callout icon="warning">
  If autoPromotionEnabled is false, the new ReplicaSet will not receive production traffic until you manually promote it. Make sure to validate the previewService before promotion, and coordinate promotion with your release process.
</Callout>

Observability

* The Argo Rollouts UI displays the strategy (blue-green), revisions, and which revision is active, preview, or stable.
* Unlike Canary releases, Blue-Green does not show incremental traffic weights; traffic is switched atomically by updating the activeService.

Quick reference: common commands

| Task               | Command                                                    |
| ------------------ | ---------------------------------------------------------- |
| Create namespace   | `kubectl create ns blue-green`                             |
| Apply manifests    | `kubectl apply -f rollout.yml -n blue-green`               |
| List resources     | `kubectl -n blue-green get all`                            |
| Promote rollout    | `kubectl argo rollouts promote <rollout-name> -n <ns>`     |
| Get rollout status | `kubectl argo rollouts get rollout <rollout-name> -n <ns>` |

Summary

* Blue-Green with Argo Rollouts uses two services (active and optional preview) to switch traffic atomically between ReplicaSets.
* Use previewService to validate new versions without impacting production.
* Set autoPromotionEnabled to false to require manual promotion for safer releases.
* Use the Argo Rollouts UI or kubectl plugin for promotion, observation, and rollback.

Links and References

* Argo Rollouts documentation: [https://argoproj.github.io/argo-rollouts/](https://argoproj.github.io/argo-rollouts/)
* Kubernetes Services: [https://kubernetes.io/docs/concepts/services-networking/service/](https://kubernetes.io/docs/concepts/services-networking/service/)
* kubectl-argo-rollouts plugin: [https://argoproj.github.io/argo-rollouts/installation/](https://argoproj.github.io/argo-rollouts/installation/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/95bb8080-9700-470c-b838-f6a7d444a528" />
</CardGroup>


# Demo Canary Deployment

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Rollouts/Demo-Canary-Deployment/page

Guide showing how to perform gradual canary releases with Argo Rollouts, including examples, commands, manifests, traffic weighting, pauses, promotion, and verification steps.

In this guide you'll learn how to perform a gradual release with Argo Rollouts using the Canary deployment strategy. Canary releases route a small percentage of production traffic to a new application revision, then incrementally increase that percentage while you monitor behaviour and optionally run automated checks.

Argo Rollouts supports multiple strategies — Canary, Blue/Green, and Progressive Delivery. This article focuses on Canary, with concise examples, commands, and tips to run a canary rollout locally or in a cluster.

## High-level overview: what a Rollout looks like

* A Rollout is similar to a Kubernetes Deployment manifest but uses the `Rollout` kind and extra strategy fields.
* Strategy steps let you incrementally shift traffic (weights) and pause at steps either for a duration or indefinitely for manual promotion.
* A Rollout will create ReplicaSets and Pods — you will not see a Deployment object for that app.

|   Resource | Purpose                                                         | Example use                                               |
| ---------: | --------------------------------------------------------------- | --------------------------------------------------------- |
|    Rollout | Declarative progressive delivery resource                       | `kind: Rollout` with `strategy.canary`                    |
| ReplicaSet | Managed by Rollout per revision                                 | Created for each revision                                 |
|    Service | Routes traffic between revisions when using weight-based canary | `Service` referenced by the Rollout traffic routing logic |

Useful links:

* [Argo Rollouts documentation](https://argoproj.github.io/argo-rollouts/)
* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

## Canary rollout — simple example

A basic Canary Rollout that controls traffic by weight and pauses between steps:

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
    canary: # Use the Canary strategy
      maxSurge: "25%"
      maxUnavailable: 0
      steps:
        - setWeight: 10
        - pause:
            duration: "1h"   # pause for 1 hour
        - setWeight: 20
        - pause: {}         # pause indefinitely until manually promoted
```

## Blue/Green (excerpt)

For comparison, here is an excerpt showing Blue/Green-related fields supported by Rollouts:

```yaml theme={null}
revisionHistoryLimit: 3

strategy:
  blueGreen:
    # Required: service that Rollout modifies as the active service
    activeService: active-service

    # Optional pre-promotion analysis
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

    previewService: preview-service
    previewReplicaCount: 1
    autoPromotionEnabled: false
    # When autoPromotionEnabled is false, Rollout remains paused until manually resumed.
```

## Walkthrough: applying a Canary rollout

1. Repository layout (example)

* patterns/canary contains `rollout.yml` and `service.yml`.

2. Example canary Rollout manifest for an application (app-rollout)

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
        - pause: {}               # pause indefinitely (manual promotion required)
        - setWeight: 40
        - pause:
            duration: "1m"
        - setWeight: 60
        - pause:
            duration: "1m"
        - setWeight: 80
        - pause:
            duration: "1m"
```

3. Shorter demo pauses (use seconds)
   If you prefer fast demos, shorten pauses to seconds:

```yaml theme={null}
strategy:
  canary:
    steps:
      - setWeight: 20
      - pause: {}
      - setWeight: 40
      - pause:
          duration: "10s"
      - setWeight: 60
      - pause:
          duration: "10s"
      - setWeight: 80
      - pause:
          duration: "10s"
```

Pause duration examples (note valid formats — include a suffix):

```yaml theme={null}
strategy:
  canary:
    steps:
      - pause: { duration: "10" }   # invalid — missing a unit; use "10s", "10m", or "10h"
      - pause: { duration: "10s" }  # 10 seconds
      - pause: { duration: "10m" }  # 10 minutes
      - pause: { duration: "10h" }  # 10 hours
      - pause: {}                   # pause indefinitely (manual promotion)
```

4. Create namespace, apply manifests, and verify

Run these commands from the patterns/canary directory (where `rollout.yml` and `service.yml` are located):

```bash theme={null}
