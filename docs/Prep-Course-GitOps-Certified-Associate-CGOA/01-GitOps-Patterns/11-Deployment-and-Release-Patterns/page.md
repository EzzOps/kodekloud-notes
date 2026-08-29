# List sealed-secrets pods in kube-system
kubectl -n kube-system get pods | grep -i sealed

# List related resources
kubectl -n kube-system get all | grep -i sealed

# List secrets (sealed-secrets publishes a TLS secret used by the controller)
kubectl -n kube-system get secret | grep -i sealed
```

Example output (names, timestamps and UIDs will vary):

```text theme={null}
pod/sealed-secrets-545f6845c-sx9bn       1/1     Running   0          34s
service/sealed-secrets                   ClusterIP   10.104.148.215   <none>        8080/TCP   35s
service/sealed-secrets-metrics           ClusterIP   10.97.142.113    <none>        8081/TCP   35s
deployment.apps/sealed-secrets           1/1     1            1          34s
replicaset.apps/sealed-secrets-545f6845c  1/1     34s

sealed-secrets-keykvrhb                   kubernetes.io/tls
```

## Install the kubeseal CLI

The `kubeseal` client encrypts Kubernetes Secret manifests using the controller's public key. The output is a SealedSecret resource that can be safely stored in Git and applied to the cluster; only the controller can decrypt it.

You can find releases on the Bitnami Labs Sealed Secrets GitHub repo: [bitnami-labs/sealed-secrets](https://github.com/bitnami-labs/sealed-secrets).

<Frame>
  <img alt="The image is a screenshot of a GitHub page for the project &#x22;Sealed Secrets&#x22; for Kubernetes, showing installation and usage documentation." />
</Frame>

<Frame>
  <img alt="The image shows a GitHub repository page for &#x22;bitnami-labs/sealed-secrets,&#x22; displaying a list of branches/tags and recent commits. The repository is described as a Kubernetes controller for encrypted secrets." />
</Frame>

Install a specific kubeseal version (replace `0.30.0` with the version you want):

```bash theme={null}
# Example: install a specific version
KUBESEAL_VERSION='0.30.0'
curl -L -o kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz \
  "https://github.com/bitnami-labs/sealed-secrets/releases/download/v${KUBESEAL_VERSION}/kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz"
tar -xvzf kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz kubeseal
sudo install -m 755 kubeseal /usr/local/bin/kubeseal
```

Or fetch and install the latest release automatically (requires `jq`):

```bash theme={null}
# Install latest kubeseal release (requires jq)
TAG=$(curl -s https://api.github.com/repos/bitnami-labs/sealed-secrets/releases/latest | jq -r .tag_name)
# Strip leading "v" from tag to get version (e.g., v0.30.0 -> 0.30.0)
VERSION=${TAG#v}
curl -L -o kubeseal-${VERSION}-linux-amd64.tar.gz \
  "https://github.com/bitnami-labs/sealed-secrets/releases/download/${TAG}/kubeseal-${VERSION}-linux-amd64.tar.gz"
tar -xvzf kubeseal-${VERSION}-linux-amd64.tar.gz kubeseal
sudo install -m 755 kubeseal /usr/local/bin/kubeseal
```

Verify the installed client:

```bash theme={null}
kubeseal --version
# Example output:
# kubeseal version: 0.30.0
```

<Callout icon="lightbulb">
  Ensure your `kubeconfig` points to the cluster where the sealed-secrets controller is installed before using `kubeseal`. The client fetches the controller's public key from the cluster to create SealedSecrets that only the controller can decrypt.
</Callout>

## What you now have

* Bitnami Sealed Secrets controller deployed in your cluster (via Helm or Argo CD)
* `kubeseal` CLI installed locally to generate SealedSecrets
* The foundation for a GitOps workflow: encrypt plain Secrets into SealedSecrets and commit them to Git; the sealed-secrets controller will decrypt and create Kubernetes Secrets in-cluster

## Quick links and references

* Artifact Hub sealed-secrets chart: [https://artifacthub.io/packages/helm/bitnami-labs/sealed-secrets](https://artifacthub.io/packages/helm/bitnami-labs/sealed-secrets)
* Sealed Secrets GitHub repo: [https://github.com/bitnami-labs/sealed-secrets](https://github.com/bitnami-labs/sealed-secrets)
* Argo CD documentation: [https://argo-cd.readthedocs.io/en/stable/](https://argo-cd.readthedocs.io/en/stable/)
* Helm documentation: [https://helm.sh/docs/](https://helm.sh/docs/)

If you'd like, I can add a sample workflow showing how to create a Secret locally, seal it with `kubeseal`, and commit the resultant SealedSecret to Git for automatic deployment.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/f1538ace-dc97-454d-b894-15bdd35bcb64/lesson/fe717104-74db-47b3-a737-c9b24b61f74e" />
</CardGroup>


# Deployment and Release Patterns

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Patterns/Deployment-and-Release-Patterns/page

Overview of Kubernetes deployment strategies including RollingUpdate Recreate blue green and canary patterns for safe application rollouts using GitOps traffic management and observability

In this lesson we'll cover common Kubernetes deployment and release patterns: RollingUpdate, Recreate, blue–green deployments, and canary releases. We begin with the two fundamental Deployment strategies supported by Kubernetes: `RollingUpdate` and `Recreate`. These strategies help you update application pods with predictable availability and resource usage during a rollout.

Imagine you're running a high-traffic web application with thousands of users. You must deploy a new version without causing downtime, but replacing all pods at once could overload the cluster or interrupt service. Kubernetes strategies manage pod replacement safely and predictably.

## RollingUpdate

A RollingUpdate replaces pods gradually—one or a few at a time—by creating new pods, verifying they are healthy, and then terminating old pods. This approach reduces service disruption and keeps the application available throughout the rollout.

Example Deployment (RollingUpdate):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      # Can be an absolute number or a percentage
      maxSurge: 1
      maxUnavailable: 0
  minReadySeconds: 10
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: my-app:1.0
```

Important parameters:

* `maxSurge`: number (or percentage) of extra pods that can be created above the desired `replicas` during the update.
* `maxUnavailable`: number (or percentage) of pods that can be unavailable during the update.
* `minReadySeconds`: time a pod must be in Ready state before it counts as available for the rollout decision.

Typical GitOps rollout (with ArgoCD) using RollingUpdate:

1. Developer updates the image tag in the Deployment manifest (e.g., `my-app:1.0` → `my-app:2.0`) and pushes the change to Git.
2. The GitOps operator detects the commit and applies the manifest to the cluster.
3. Kubernetes performs the rolling update: it creates new pods, waits for readiness, then removes old pods.
4. If the rollout fails or metrics regress, you can pause, investigate, and roll back.

Troubleshooting and common commands:

```bash theme={null}
