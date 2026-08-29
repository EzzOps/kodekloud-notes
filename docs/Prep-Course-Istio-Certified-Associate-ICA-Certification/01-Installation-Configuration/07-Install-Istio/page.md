# Example output:
/usr/sbin/helm
```

Add and update the Istio Helm repository:

```bash theme={null}
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update
```

Verify the repository was added:

```bash theme={null}
helm repo list
# Example output includes "istio"
```

What we will install

* istio/base — installs CustomResourceDefinitions (CRDs) and base resources.
* istio/istiod — the control plane (istiod replaces older Pilot/Galley components).
* istio/gateway — the ingress gateway (can be installed into istio-system or a separate namespace).

| Chart           | Purpose                                      | Notes                                              |
| --------------- | -------------------------------------------- | -------------------------------------------------- |
| `istio/base`    | Installs CRDs and cluster-level base objects | Must be installed before other Istio charts.       |
| `istio/istiod`  | Istio control plane (Pilot, etc.)            | You can customize resource requests and profile.   |
| `istio/gateway` | Ingress gateway deployment                   | Can be in `istio-system` or a dedicated namespace. |

Steps

1. Install the Istio base chart (creates `istio-system` and installs CRDs)

```bash theme={null}
helm install istio-base istio/base \
  --namespace istio-system \
  --create-namespace \
  --version 1.26.3 \
  --set profile=demo
```

Confirm the CRDs are present:

```bash theme={null}
kubectl get crd | grep 'istio.io'
# You should see many Istio CRDs listed with their creation timestamps.
```

<Frame>
  <img alt="The image shows a terminal window with commands related to installing Istio using Helm and checking custom resource definitions (CRDs) with kubectl. It confirms Istio's successful installation and lists several CRDs with their creation timestamps." />
</Frame>

<Callout icon="lightbulb">
  The base chart is required because it installs the Istio CustomResourceDefinitions (CRDs). Without these CRDs you cannot create many Istio resources.
</Callout>

<Callout icon="warning">
  Always install the `istio/base` chart before `istiod` or `gateway`. Installing the control plane without CRDs can cause resources to be invalid or fail to create.
</Callout>

2. Install the control plane (istiod)

For small clusters, reduce CPU request for the Pilot component to avoid scheduling pressure:

```bash theme={null}
helm install istiod istio/istiod \
  --namespace istio-system \
  --version 1.26.3 \
  --set profile=demo \
  --set pilot.resources.requests.cpu=250m
```

Check the istiod pod is running:

```bash theme={null}
kubectl get pods -n istio-system
# Example output:
# NAME                       READY   STATUS    RESTARTS   AGE
# istiod-7f65f9c48b-5wgpr    1/1     Running   0          11s
```

Sample helm install output (trimmed for clarity):

```bash theme={null}
# helm install istiod istio/istiod ...
NAME: istiod
LAST DEPLOYED: Tue Aug 26 22:26:57 2025
NAMESPACE: istio-system
STATUS: deployed
NOTES: "istiod" successfully installed!
```

3. Install the ingress gateway

You can install the gateway into `istio-system` or a separate namespace (e.g., `istio-ingress`). Here we install into `istio-system`:

```bash theme={null}
helm install istio-ingress istio/gateway \
  --namespace istio-system \
  --version 1.26.3
```

Verify both the gateway and istiod are running:

```bash theme={null}
kubectl get pods -n istio-system
# Example output:
# NAME                                  READY   STATUS    RESTARTS   AGE
# istio-ingress-6cc846956d-b57jn        1/1     Running   0          5s
# istiod-7f65f9c48b-5wgpr               1/1     Running   0          64s
```

Optional diagnostics: run istioctl analyze to catch common issues (if istioctl is installed).

```bash theme={null}
istioctl analyze
# If not installed you may see:
# -bash: istioctl: command not found
```

4. Enable automatic sidecar injection

Label the namespace where you want Istio to automatically inject the Envoy sidecar. This example enables injection in the `default` namespace.

Check existing labels:

```bash theme={null}
kubectl get ns default --show-labels
# Before labeling:
# NAME      STATUS   AGE    LABELS
# default   Active   5m     kubernetes.io/metadata.name=default
```

Label the namespace:

```bash theme={null}
kubectl label ns default istio-injection=enabled --overwrite
# namespace/default labeled
```

Confirm the label:

```bash theme={null}
kubectl get ns default --show-labels
# After labeling:
# NAME      STATUS   AGE    LABELS
# default   Active   5m     istio-injection=enabled,kubernetes.io/metadata.name=default
```

5. Deploy a sample workload (Redis) to validate sidecar injection

Create a simple Redis pod in the labeled namespace:

```bash theme={null}
kubectl run redis --image=redis --restart=Never
kubectl get pods
# You should see the redis pod in a Running state.
```

Describe the redis pod and confirm both containers are present (application + Istio sidecar):

```bash theme={null}
kubectl describe pod redis
# Look near the top for two containers: "redis" and "istio-proxy" (with its version).
```

<Frame>
  <img alt="The image shows a terminal window displaying Kubernetes container details, including information about two containers: one running Redis and another running an Istio proxy." />
</Frame>

6. Inspect and customize Helm chart values

To review default chart values before customizing or upgrading, extract them to files:

```bash theme={null}
helm show values istio/istiod > istiod.yaml
helm show values istio/gateway > gateway.yaml
ls -lh istiod.yaml gateway.yaml
# Example files created: istiod.yaml (large), gateway.yaml
```

Edit `istiod.yaml` or `gateway.yaml` to change settings such as image tags, resources, or gateway configuration. Example snippet from a values file:

```yaml theme={null}
# Tolerations for the waypoint proxy.
tolerations: []

base:
  enableIstioConfigCRDs: true

gateways:
  securityContext: {}
  seccompProfile: {}

pdb:
  minAvailable: 1
  maxUnavailable: 1
  unhealthyPodEvictionPolicy: ""
```

Apply your custom values when upgrading the release:

```bash theme={null}
helm upgrade istiod istio/istiod -n istio-system -f istiod.yaml
```

This updates the existing release using your modified configuration.

References

* Istio Helm charts: [https://istio.io/latest/docs/setup/install/helm/](https://istio.io/latest/docs/setup/install/helm/)
* Helm documentation: [https://helm.sh/docs/](https://helm.sh/docs/)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* istioctl analyze: [https://istio.io/latest/docs/ops/diagnostic-tools/istioctl-analyze/](https://istio.io/latest/docs/ops/diagnostic-tools/istioctl-analyze/)

Summary
You have now installed Istio via Helm (base, istiod, and gateway), verified CRDs, enabled automatic sidecar injection for a namespace, deployed a sample workload to verify injection, and exported chart values for customization. Adjust values and resource requests as needed for production environments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/65ee174b-536e-4657-9b6f-85c90c7612da/lesson/6573340b-df72-4556-ad3e-57932412cc44" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/65ee174b-536e-4657-9b6f-85c90c7612da/lesson/51813dbf-e627-448d-8a3e-c0cece77f868" />
</CardGroup>


# Install Istio

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Installation-Configuration/Install-Istio/page

Guide to installing and validating Istio on Kubernetes using istioctl or Helm, configuring sidecar injection, and deploying the Bookinfo sample for verification.

This guide walks through installing Istio on a Kubernetes cluster using two common methods: istioctl (recommended for simplicity) and Helm (recommended for modular, production-style installs). It also covers sidecar injection, validating the install, and deploying the Bookinfo sample application for verification. The examples use Istio 1.26.3 (the version referenced for the [ICA exam](https://learn.kodekloud.com/user/courses/istio-certified-associate)).

Prerequisites

* A functioning Kubernetes cluster (managed: EKS/GKE/AKS or local: kind/Minikube).
* A valid `kubeconfig` context pointing to the cluster.
* `kubectl` installed and configured to talk to your cluster.
* `istioctl` downloaded for the Istio version you plan to install (example below uses `1.26.3`).

<Callout icon="lightbulb">
  Install the `istioctl` client that matches the major/minor version you intend to run in-cluster. Minor version mismatches can work in some cases, but matching versions reduces surprises during labs or exams.
</Callout>

## Install or verify tooling

Install `istioctl` (example: 1.26.3)
On Linux/macOS you can download the official release with the Istio download script:

```bash theme={null}
