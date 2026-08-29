# Example output:
# Successfully packaged chart and saved it to: /path/to/demo-0.1.0.tgz
```

Using the example chart for this lesson (located at `manifests/helm/highway-chart`):

```bash theme={null}
cd manifests/helm/highway-chart
helm package .
# Successfully packaged chart and saved it to: /home/demos/manifests/helm/highway-chart/highway-chart-0.1.0.tgz
```

## 2) Authenticate to Docker Hub (OCI registry)

Log in to Docker Hub using Helm's registry login. Replace `siddharth67` with your Docker Hub username:

```bash theme={null}
helm registry login registry-1.docker.io -u siddharth67
# Password: <enter password or token>
# Login Succeeded
```

> **warning** Docker Hub may require a Personal Access Token instead of your account password depending on your account settings. If authentication fails, create a token in Docker Hub and use it as the password.

## 3) Push the packaged chart to Docker Hub (OCI)

When pushing a Helm chart as an OCI artifact, push it under your Docker Hub namespace. The destination format is `oci://registry-1.docker.io/<your-username>`.

Example:

```bash theme={null}
helm push highway-chart-0.1.0.tgz oci://registry-1.docker.io/siddharth67
# Pushed: registry-1.docker.io/siddharth67/highway-chart:0.1.0
# Digest: sha256:<digest-value>
```

Important: pushing to the `oci://registry-1.docker.io/docker` namespace will fail with `401 Unauthorized` unless `docker` is your namespace. Always use your own username or organization namespace.

## 4) Pull the chart from Docker Hub (OCI)

You can pull the chart tarball from the OCI registry with `helm pull`. Always include the chart name and version to avoid Helm attempting to list tags (which may require additional authentication):

```bash theme={null}
helm pull oci://registry-1.docker.io/siddharth67/highway-chart --version 0.1.0
# Pulled: registry-1.docker.io/siddharth67/highway-chart:0.1.0
# Digest: sha256:<digest-value>
```

## 5) Install the chart directly from the OCI registry

Helm can install charts directly from an OCI URL without first pulling a tarball. Example below creates a namespace and installs the chart using an explicit values file:

```bash theme={null}
kubectl create namespace oci-demo

helm install oci-demo-release oci://registry-1.docker.io/siddharth67/highway-chart \
  --version 0.1.0 \
  --values ../cgoa-demos/manifests/helm/highway-chart/values.yml \
  -n oci-demo
```

Example successful output:

```text theme={null}
Pulled: registry-1.docker.io/siddharth67/highway-chart:0.1.0
Digest: sha256:<digest-value>
NAME: oci-demo-release
LAST DEPLOYED: <timestamp>
NAMESPACE: oci-demo
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Verify the release resources:

```bash theme={null}
kubectl -n oci-demo get all
# Example output:
# NAME                                                READY   STATUS    RESTARTS   AGE
# pod/highway-animation-c5cccf6b-nrj15                1/1     Running   0          9s
# ...
```

## 6) Using OCI artifacts with GitOps tools

Many GitOps tools can use OCI registries as application sources for Helm charts.

* Argo CD supports OCI as an application source and can fetch Helm charts from OCI registries: [Argo CD GitOps course](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* Flux CD supports an `OCIRepository` source to track OCI artifacts: [Flux CD GitOps course](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd)

Example Argo CD Application (reference):

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-custom-image
  namespace: argocd
spec:
  project: default
  source:
    path: .
    repoURL: oci://registry-1.docker.io/some-user/my-custom-image
    targetRevision: 1.16.1
  destination:
    server: "https://kubernetes.default.svc"
    namespace: my-namespace
```

If the OCI registry is private, provide credentials to Argo CD via a Kubernetes Secret and configure Argo CD to use it. The same principle applies to Flux CD: create an `OCIRepository` and supply credentials when required.

Example Flux `OCIRepository`:

```yaml theme={null}
---
apiVersion: source.toolkit.fluxcd.io/v1
kind: OCIRepository
metadata:
  name: podinfo
  namespace: default
spec:
  interval: 5m0s
  url: oci://ghcr.io/stefanprodan/manifests/podinfo
  ref:
    tag: latest
```

## 7) Quick reference — common Helm OCI commands

| Task                | Command / Example                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------ |
| Package a chart     | `helm package ./path-to-chart`                                                             |
| Login to registry   | `helm registry login registry-1.docker.io -u <username>`                                   |
| Push chart to OCI   | `helm push chart-0.1.0.tgz oci://registry-1.docker.io/<username>`                          |
| Pull chart from OCI | `helm pull oci://registry-1.docker.io/<username>/chart --version 0.1.0`                    |
| Install from OCI    | `helm install release oci://registry-1.docker.io/<username>/chart --version 0.1.0 -n <ns>` |

## 8) Summary and best practices

* Use `helm package` to create chart tarballs and `helm push` to upload them as OCI artifacts.
* Authenticate with `helm registry login`. For Docker Hub, prefer a Personal Access Token if your account requires it.
* Always push to your own Docker Hub namespace (for example, `oci://registry-1.docker.io/<your-username>`).
* Install charts directly from OCI with `helm install` to avoid manual tarball handling.
* For GitOps automation, configure Argo CD or Flux to read from OCI registries and provide registry credentials via Kubernetes Secrets when registries are private.
* Automate credential rotation and secret management for production pipelines to reduce risk.

Resources and references:

* [OCI Specification](https://opencontainers.org)
* [Docker Hub](https://hub.docker.com)
* [Helm Documentation](https://helm.sh/docs/)
* [Argo CD Documentation](https://argo-cd.readthedocs.io/)
* [Flux CD Documentation](https://fluxcd.io/)

That's all — with these steps you can package Helm charts as OCI artifacts, publish them to registries like Docker Hub, and consume them manually or through GitOps workflows.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/24630e6a-9f49-42d1-abd0-75bafc02ce01/lesson/dbab5117-22bd-436f-9e0c-ff1e564f06fd)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/24630e6a-9f49-42d1-abd0-75bafc02ce01/lesson/b7657880-6ab2-4732-9b0e-d6055e5e6f00)


# Demo Raise Alert using AlertManager

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/Tooling/Demo-Raise-Alert-using-AlertManager/page

Guide to creating a Prometheus rule that alerts when Argo CD applications go OutOfSync, testing drift, viewing alerts in Alertmanager, and routing notifications (e.g. Slack).

In this lesson you'll learn how to raise an Alertmanager alert whenever an Argo CD application becomes OutOfSync. We assume Alertmanager and Prometheus are already installed and accessible (Alertmanager via NodePort in this environment). This guide covers:

* Creating a Prometheus rule for Argo CD application drift
* Where to add the rule (Prometheus Operator `PrometheusRule`)
* How to test by introducing drift in an Argo CD application
* Viewing the fired alert in Alertmanager and forwarding notifications (Slack example)

## Define the Prometheus alert rule

Create a `PrometheusRule` group that triggers when Argo CD reports an OutOfSync application. The PromQL expression uses the `argocd_app_info` metric exposed by Argo CD.

```yaml theme={null}
