# Example for Linux AMD64 (adjust version and filename as needed)
wget https://github.com/argoproj/argo-rollouts/releases/download/v1.8.3/kubectl-argo-rollouts-linux-amd64

# make it executable
chmod +x kubectl-argo-rollouts-linux-amd64

# move it into your PATH and give the canonical name
sudo mv kubectl-argo-rollouts-linux-amd64 /usr/local/bin/kubectl-argo-rollouts
```

Verify the plugin is installed and check its version:

```bash theme={null}
kubectl argo rollouts version
```

Example output:

```bash theme={null}
kubectl-argo-rollouts: v1.8.3+49fa151
    BuildDate: 2025-06-04T22:15:54Z
    GitCommit: [AWS_SECRET_ACCESS_KEY]
    GitTreeState: clean
    GoVersion: go1.23.9
    Compiler: gc
    Platform: linux/amd64
```

<Callout icon="lightbulb">
  After installing the binary as /usr/local/bin/kubectl-argo-rollouts the plugin is available as the kubectl subcommand `kubectl argo rollouts`.
</Callout>

## Launch the Rollouts dashboard

Start the local dashboard proxy to serve the UI on [http://localhost:3100/rollouts](http://localhost:3100/rollouts) by default:

```bash theme={null}
kubectl argo rollouts dashboard -n argo-rollouts
```

* The command opens a local proxy and hosts the UI at [http://localhost:3100/rollouts](http://localhost:3100/rollouts).
* If you don’t pass `-n`, the plugin will target the `default` namespace or the context’s current namespace; use `-n <namespace>` to specify another one.
* If you prefer a different local port, check plugin help for available flags.

Open [http://localhost:3100/rollouts](http://localhost:3100/rollouts) in your browser. If you haven’t created any Rollout resources, the UI will indicate no Rollouts in the selected namespace.

## Next steps

* Create a Rollout manifest (canary or blue-green) and apply it to experiment with traffic shifting and automated analysis.
* Integrate metrics providers (Prometheus) and AnalysisTemplates for automated, metric-driven promotion or rollback.
* See the Argo Rollouts docs for examples and advanced configuration: [https://argoproj.github.io/argo-rollouts/](https://argoproj.github.io/argo-rollouts/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/8085d4fd-d85d-45dd-99a7-eba5ced8e438" />
</CardGroup>


# Demo Blue Green Deployment

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Rollouts/Demo-Blue-Green-Deployment/page

Demonstrates Argo Rollouts blue green deployment using active and preview services to atomically switch production traffic, enabling validation and manual promotion and rollback

Let's explore how Argo Rollouts implements a Blue-Green deployment pattern to switch production traffic between application versions atomically.

<Frame>
  <img alt="A presentation slide with a blue-green gradient background and a centered white title reading &#x22;Argo Rollouts - Blue-Green Deployment.&#x22; A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left corner." />
</Frame>

What makes Blue-Green different from Canary:

* Argo Rollouts still manages ReplicaSets for each version, but in Blue-Green the rollout controller swaps Service resources to redirect traffic from the old ReplicaSet (blue) to the new ReplicaSet (green).
* The Rollout spec references two Services (in the same namespace):
  * activeService (required): receives production traffic and points to the currently active ReplicaSet (the stable version).
  * previewService (optional): points to the new ReplicaSet so you can validate it without exposing it to production.

Key behaviors:

* When autoPromotionEnabled is false, promotion to active must be done manually (via CLI or UI).
* When promotion happens, the controller updates the activeService to point at the new ReplicaSet, switching production traffic atomically.

Table: Blue-Green rollout services

| Service role   | Purpose                                                           | Example name                |
| -------------- | ----------------------------------------------------------------- | --------------------------- |
| activeService  | Routes production traffic to the active ReplicaSet                | `highway-bluegreen-active`  |
| previewService | Optional: routes non-production/preview traffic to new ReplicaSet | `highway-bluegreen-preview` |

Minimal Rollout spec that demonstrates the blueGreen strategy and both services:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: rollout-bluegreen
spec:
  replicas: 2
  revisionHistoryLimit: 2
  selector:
    matchLabels:
      app: rollout-bluegreen
  template:
    metadata:
      labels:
        app: rollout-bluegreen
    spec:
      containers:
      - name: rollouts-demo
        image: argoproj/rollouts-demo:blue
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
  strategy:
    blueGreen:
      # activeService is mandatory; the rollout controller updates this service
      # to point to the ReplicaSet deemed "active" after promotion.
      activeService: rollout-bluegreen-active
      # previewService is optional; it is updated to point to the new ReplicaSet
      # while production (activeService) continues to serve the old ReplicaSet.
      previewService: rollout-bluegreen-preview
      # autoPromotionEnabled:false disables automated promotion. With this set to
      # false you must manually promote the new ReplicaSet (via CLI or UI).
      autoPromotionEnabled: false
```

Concrete example — highway animation application

* Namespace: `blue-green`
* 10 replicas of the application for each version (blue or green)
* Two Services referenced in the strategy: `highway-bluegreen-active` and `highway-bluegreen-preview`

Rollout manifest:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: highway-bluegreen
  namespace: blue-green
spec:
  replicas: 10
  revisionHistoryLimit: 2
  selector:
    matchLabels:
      app: highway-bluegreen
  template:
    metadata:
      labels:
        app: highway-bluegreen
    spec:
      containers:
      - name: highway-bluegreen
        image: siddharth67/highway-animation:blue
        ports:
        - containerPort: 3000
        env:
        - name: POD_COUNT
          value: "10"
  strategy:
    blueGreen:
      activeService: highway-bluegreen-active
      previewService: highway-bluegreen-preview
      autoPromotionEnabled: false
```

Service manifests (two services with identical selectors and ports; only the names differ):

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: highway-bluegreen-active
  namespace: blue-green
spec:
  selector:
    app: highway-bluegreen
  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000
  type: NodePort
---
apiVersion: v1
kind: Service
metadata:
  name: highway-bluegreen-preview
  namespace: blue-green
spec:
  selector:
    app: highway-bluegreen
  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000
  type: NodePort
```

<Callout icon="lightbulb">
  The preview service is optional. When present, it provides a non-production endpoint for the new ReplicaSet so you can validate the new version before switching production traffic to it.
</Callout>

Deployment steps

1. Create the namespace:

```bash theme={null}
kubectl create ns blue-green
```

2. Apply the manifests:

```bash theme={null}
kubectl apply -f .
