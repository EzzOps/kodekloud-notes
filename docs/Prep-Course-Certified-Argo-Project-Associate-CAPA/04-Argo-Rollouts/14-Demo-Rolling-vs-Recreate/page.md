# rollout-initial.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: highway-bluegreen
  namespace: argo-analysis-lab
spec:
  replicas: 5
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
          value: "5"
  strategy:
    blueGreen:
      activeService: highway-bluegreen-active
      previewService: highway-bluegreen-preview
      autoPromotionEnabled: false
---
apiVersion: v1
kind: Service
metadata:
  name: highway-bluegreen-active
  namespace: argo-analysis-lab
spec:
  type: NodePort
  selector:
    app: highway-bluegreen
  ports:
    - port: 80
      targetPort: 3000
      nodePort: 32079
---
apiVersion: v1
kind: Service
metadata:
  name: highway-bluegreen-preview
  namespace: argo-analysis-lab
spec:
  type: NodePort
  selector:
    app: highway-bluegreen
  ports:
    - port: 80
      targetPort: 3000
      nodePort: 31058
```

Create the namespace and apply the manifest:

```bash theme={null}
# create namespace
kubectl create namespace argo-analysis-lab

# apply the rollout and services
kubectl -n argo-analysis-lab apply -f rollout-initial.yaml
```

Expected output after applying:

```text theme={null}
rollout.argoproj.io/highway-bluegreen created
service/highway-bluegreen-active created
service/highway-bluegreen-preview created
```

Verify pods and services in the namespace:

```bash theme={null}
kubectl -n argo-analysis-lab get pods,svc
```

Example output (NodePort mappings shown):

```text theme={null}
NAME                                            READY   STATUS    RESTARTS   AGE
pod/highway-bluegreen-xxxxx                     1/1     Running   0          30s
pod/highway-bluegreen-xxxxx                     1/1     Running   0          30s
pod/highway-bluegreen-xxxxx                     1/1     Running   0          30s
pod/highway-bluegreen-xxxxx                     1/1     Running   0          30s
pod/highway-bluegreen-xxxxx                     1/1     Running   0          30s

NAME                                    TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)            AGE
service/highway-bluegreen-active        NodePort   10.110.85.145   <none>        80:32079/TCP       30s
service/highway-bluegreen-preview       NodePort   10.108.197.140  <none>        80:31058/TCP       30s
```

Open the Argo Rollouts UI and switch to the `argo-analysis-lab` namespace to confirm the Rollout and blue/green details.

<Frame>
  <img alt="A screenshot of the Argo Rollouts web UI for the &#x22;highway-bluegreen&#x22; rollout showing a BlueGreen strategy, container image &#x22;siddharth67/highway-animation:blue&#x22;, and a Revision 1 marked stable and active with green checkmarks. The top-right shows the namespace &#x22;argo-analysis-lab&#x22; and control buttons like Restart, Retry, Abort, and Promote." />
</Frame>

Access the app via the active service NodePort on any cluster node:
http\://\<node-ip>:32079

The application exposes a `/health` endpoint that returns a simple JSON payload:

```json theme={null}
{
  "status": "OK",
  "message": "Highway Animation Server is running"
}
```

<Callout icon="lightbulb">
  This `/health` endpoint is a good target for an Argo Rollouts [AnalysisTemplate](https://argoproj.github.io/argo-rollouts/features/analysis/). An AnalysisRun can query the endpoint and assert that `"status" == "OK"` before promoting the preview to active.
</Callout>

<Callout icon="warning">
  The Rollout is configured with `autoPromotionEnabled: false`. Promotion must be performed manually via the Argo Rollouts UI/CLI or gated using an AnalysisRun. Also be cautious exposing NodePorts in production clusters — prefer Ingress or LoadBalancer for controlled external access.
</Callout>

Resources at a glance:

| Resource Type     | Purpose                                                                                    |
| ----------------- | ------------------------------------------------------------------------------------------ |
| Rollout           | Manages blue/green deployment of `highway-bluegreen` with 5 replicas and manual promotion. |
| Service (active)  | NodePort service routed to the active replica set (port 32079).                            |
| Service (preview) | NodePort service routed to the preview replica set (port 31058).                           |

Links and references:

* Argo Rollouts blue/green traffic management: [https://argoproj.github.io/argo-rollouts/features/traffic-management/#blue-green](https://argoproj.github.io/argo-rollouts/features/traffic-management/#blue-green)
* Argo Rollouts analysis feature (AnalysisTemplate & AnalysisRun): [https://argoproj.github.io/argo-rollouts/features/analysis/](https://argoproj.github.io/argo-rollouts/features/analysis/)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

That's the health-check setup for this Rollout. You can now author an AnalysisTemplate that probes `/health`, run an AnalysisRun during promotion, and use its result to gate the transition from preview to active.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/4589c468-b93e-431d-93da-b6f5f6d7eef8" />
</CardGroup>


# Demo Rolling vs Recreate

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Rollouts/Demo-Rolling-vs-Recreate/page

Demonstrates Kubernetes Deployment RollingUpdate versus Recreate strategies by upgrading a sample app to show how rolling updates preserve availability while Recreate causes downtime

In this hands-on demo you'll see the practical difference between the RollingUpdate and Recreate deployment strategies in Kubernetes. We'll deploy a small HTTP app that returns its version (v1 or v2) and observe behavior during an upgrade. This shows how each strategy affects availability and rollout behavior.

What you'll learn:

* How to deploy a simple Deployment and Service
* How RollingUpdate preserves availability during updates
* How Recreate causes downtime by terminating all pods before creating new ones

Deployment manifest (patterns/release/deployment.yaml)

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: app-demo
spec:
  replicas: 5
  selector:
    matchLabels:
      app: app-demo
  template:
    metadata:
      labels:
        app: app-demo
    spec:
      containers:
      - name: app
        image: siddharth67/app:v1
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 3311
```

Note: The manifest above omits a `strategy` section. Kubernetes defaults to the RollingUpdate strategy when `strategy` is not specified.

<Callout icon="lightbulb">
  If you require zero-downtime updates, RollingUpdate is the default and preferred choice. The Recreate strategy will terminate all existing pods before creating new ones, which causes an interruption in service.
</Callout>

## 1) Clone the repo and apply resources

Run the commands below to prepare the demo namespace and apply the manifests:

```bash theme={null}
