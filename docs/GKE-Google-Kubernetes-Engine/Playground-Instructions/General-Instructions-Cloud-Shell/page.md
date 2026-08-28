# Stateless Deployment example
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels: { app: nginx }
  template:
    metadata: { labels: { app: nginx } }
    spec:
      containers:
      - name: nginx
        image: nginx:latest
```

### Batch Jobs

Batch workloads run to completion, ideal for data processing or scheduled tasks.

```yaml theme={null}
apiVersion: batch/v1
kind: Job
metadata:
  name: data-processor
spec:
  template:
    spec:
      containers:
      - name: processor
        image: gcr.io/my-project/data-processor:latest
      restartPolicy: OnFailure
```

<Callout icon="lightbulb">
  Use `CronJob` for recurring batch tasks, e.g., nightly backups or ETL pipelines.
</Callout>

### DaemonSets

DaemonSets ensure one pod per node (or per subset of nodes), perfect for logging agents and metrics collectors.

```yaml theme={null}
apiVersion: apps/v1
kind: DaemonSet
metadata: { name: fluentd-logger }
spec:
  selector: { matchLabels: { app: fluentd } }
  template:
    metadata: { labels: { app: fluentd } }
    spec:
      containers:
      - name: fluentd
        image: fluentd:v1.9
```

***

## Node Taints and Tolerations

Taints and tolerations let you control which pods can schedule onto which nodes, improving resource utilization and workload isolation.

<Frame>
  ![The image is a diagram illustrating "Effective Workload Management" in GKE using "Node Taints," highlighting their importance and benefits for workload distribution and resource optimization.](https://kodekloud.com/kk-media/image/upload/v1752875737/notes-assets/images/GKE-Google-Kubernetes-Engine-Section-Introduction/effective-workload-management-gke-node-taints.jpg)
</Frame>

* **Taint**: Applied to a node to repel pods
* **Toleration**: Added to pod specs to allow scheduling onto tainted nodes

```bash theme={null}
kubectl taint nodes node-1 key=value:NoSchedule
```

```yaml theme={null}
# Pod toleration example
apiVersion: v1
kind: Pod
metadata: { name: critical-app }
spec:
  tolerations:
  - key: "key"
    operator: "Equal"
    value: "value"
    effect: "NoSchedule"
  containers:
  - name: app
    image: gcr.io/my-project/critical-app:latest
```

<Callout icon="triangle-alert">
  A pod without a matching toleration won’t schedule on a tainted node. Double-check your keys and effects.
</Callout>

***

## Rolling Updates in GKE

Rolling updates ensure zero-downtime deployments by gradually replacing old pods with new versions.

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata: { name: web-app }
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 2
  template:
    metadata: { labels: { app: web-app } }
    spec:
      containers:
      - name: web
        image: gcr.io/my-project/web-app:v2.0
```

Key parameters:

* `maxUnavailable`: Pods that can be down during the update
* `maxSurge`: Additional pods to spin up above the desired replicas

***

## Further Reading

* [Google Kubernetes Engine Overview](https://cloud.google.com/kubernetes-engine/docs/concepts/overview)
* [Kubernetes Workloads](https://kubernetes.io/docs/concepts/workloads/)
* [Managing GKE Clusters](https://cloud.google.com/kubernetes-engine/docs/how-to)

For best practices on securing and optimizing your GKE workloads, visit the [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gke-google-kubernetes-engine/module/12020a5d-e2fd-46b5-82fb-35aa9cd57ad6/lesson/33469aad-a3a8-4d05-afb4-0058c399e725" />
</CardGroup>


# General Instructions Cloud Shell

Source: https://notes.kodekloud.com/docs/GKE-Google-Kubernetes-Engine/Playground-Instructions/General-Instructions-Cloud-Shell/page

This guide explains how to launch Google Cloud Shell, authenticate your session, and verify access without local setup.

Google Cloud Shell is a browser-based command-line environment that gives you instant access to a lightweight VM with the `gcloud` CLI preinstalled. This guide walks you through launching Cloud Shell, authenticating your session, and verifying access—all without any local setup.

## Launching Cloud Shell

1. Sign in to the [Google Cloud Console](https://console.cloud.google.com/) and select your desired project.
2. Click the **Activate Cloud Shell** button (terminal icon) in the top-right corner of the console.

<Callout icon="lightbulb">
  Provisioning the Cloud Shell VM can take a few seconds. You’ll see a spinner until the terminal is ready.
</Callout>

3. When initialization completes, a command prompt appears at the bottom of the console.

## Authenticating Your Session

Cloud Shell automatically uses your Google account credentials, but you can explicitly log in or refresh your tokens:

```bash theme={null}
gcloud auth login
```

This command opens an authorization URL in a separate tab. Follow the prompts to grant Cloud Shell the necessary permissions.

<Callout icon="triangle-alert">
  Cloud Shell sessions time out after 120 minutes of inactivity. Be sure to save any important work or scripts to your persistent home directory (`~/`) before you leave.
</Callout>

## Verifying Access

Run any `gcloud` command to confirm that authentication succeeded. For example, list all projects you can access:

```bash theme={null}
gcloud projects list
```

If you see a table of project IDs, names, and associated organizations, your Cloud Shell session is fully authenticated and ready for use.

## Links and References

* [Google Cloud Shell Overview](https://cloud.google.com/shell/docs/)
* [gcloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference)
* [Cloud Shell Quotas & Limits](https://cloud.google.com/shell/quotas)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gke-google-kubernetes-engine/module/f7a534a3-6dcf-42b8-96c8-648e59b02830/lesson/5588cc88-8eec-45cc-81b3-8628505180fd" />
</CardGroup>
