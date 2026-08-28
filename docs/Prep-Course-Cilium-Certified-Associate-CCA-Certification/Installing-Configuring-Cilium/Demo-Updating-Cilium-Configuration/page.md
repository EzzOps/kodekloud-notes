# Example: extract and move helm binary (adjust filename for the version you downloaded)
tar -zxvf helm-v3.0.0-linux-amd64.tar.gz
mv linux-amd64/helm /usr/local/bin/helm
helm help
```

Add the Cilium Helm repository
Cilium publishes an official Helm chart. Add the repo and confirm it’s available to your Helm client:

```bash theme={null}
helm repo add cilium https://helm.cilium.io/
helm repo update
helm repo list
```

Expected output (example):

```text theme={null}
NAME    URL
cilium  https://helm.cilium.io/
```

Inspect chart default values
Before installing, download the chart's default values so you can review and override settings as required. This helps you understand tunables such as datapath mode, encryption, IPv6, Hubble, etc.

```bash theme={null}
helm show values cilium/cilium > values.yaml
```

The generated values.yaml contains many configuration options with inline comments. Example excerpts:

```yaml theme={null}
clustermeshApiserver:
  create: true
  name: clustermesh-apiserver
  automount: true
  annotations: {}
clustermeshcertgen:
  create: true
  name: clustermesh-apiserver-generate-certs

commonLabels: {}
upgradeCompatibility: null

debug:
  enabled: false
```

Enable IPv6 (optional)
If you want IPv6 support, edit values.yaml and enable the top-level IPv6 block for the Cilium agent. There are several IPv6-related settings across the file — ensure you edit the top-level agent configuration (not only example snippets).

```yaml theme={null}
ipv4:
  enabled: true
ipv6:
  enabled: true
```

Tip: Search values.yaml for the primary Cilium agent section (look for comments or headings around "Agent configuration") to make sure you modify the intended top-level options.

Install Cilium with Helm
Install the chart into the kube-system namespace, supplying your modified values.yaml. Optionally pin a chart version with --version.

```bash theme={null}
helm install cilium cilium/cilium --namespace kube-system -f values.yaml --version 1.17.2
```

Example install output:

```text theme={null}
NAME: cilium
LAST DEPLOYED: Tue Mar 25 21:26:25 2025
NAMESPACE: kube-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
You have successfully installed Cilium with Hubble.

Your release version is 1.17.2.

For any further help, visit https://docs.cilium.io/en/v1.17/gettinghelp
```

Verify the release
Confirm the Helm release exists in the kube-system namespace:

```bash theme={null}
helm list -n kube-system
```

View the rendered Kubernetes manifests that Helm applied
To inspect the fully rendered manifest for auditing or troubleshooting:

```bash theme={null}
helm get manifest cilium -n kube-system
```

Example snippet from the rendered manifest:

```yaml theme={null}
app.kubernetes.io/part-of: cilium
app.kubernetes.io/name: cilium-operator
spec:
  replicas: 2
  selector:
    matchLabels:
      io.cilium/app: operator
      name: cilium-operator
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 50%
    type: RollingUpdate
  template:
    metadata:
      annotations:
        prometheus.io/port: "9963"
```

Check Cilium runtime status
Verify pods, daemonsets, and deployments in kube-system to ensure agents and operator are running:

```bash theme={null}
kubectl -n kube-system get pods -l k8s-app=cilium
kubectl -n kube-system get daemonsets,deployments -l k8s-app=cilium
```

If you have the Cilium CLI installed, it provides a concise view of component health:

```bash theme={null}
cilium status
```

Typical status output shows agent and operator availability, Hubble status, Envoy proxy counts, and any health issues.

<Callout icon="lightbulb">
  If you are deploying to a managed Kubernetes service (EKS, GKE, AKS), consult the Cilium documentation for platform-specific prerequisites and recommended settings (for example, node taints/labels, node groups, or specific annotations). These are documented in the Cilium installation guide: [https://docs.cilium.io/en/v1.17/](https://docs.cilium.io/en/v1.17/)
</Callout>

Quick reference — common verification commands

| Command                                           | Purpose                                                      |
| ------------------------------------------------- | ------------------------------------------------------------ |
| kubectl -n kube-system get pods -l k8s-app=cilium | List Cilium pods and their status                            |
| kubectl -n kube-system get daemonsets,deployments | Check daemonsets & deployments in kube-system                |
| helm list -n kube-system                          | Confirm Helm release presence and status                     |
| helm get manifest cilium -n kube-system           | View rendered manifest applied by Helm                       |
| cilium status                                     | High-level Cilium component health (if cilium CLI installed) |

Wrapping up
Summary of the Helm-based installation flow:

1. Ensure Helm is installed and kubectl is configured for your cluster.
2. Add and update the Cilium Helm repository.
3. Inspect the chart defaults and adjust values.yaml for your needs (IPv6, datapath, Hubble, etc.).
4. Install the chart into your target namespace with Helm.
5. Verify the Helm release and inspect manifests; confirm runtime status with kubectl and cilium CLI.

For production deployments or cloud-managed clusters, follow the platform-specific guidance in the Cilium docs: [https://docs.cilium.io/en/v1.17/](https://docs.cilium.io/en/v1.17/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/2fded455-95ea-4183-8cce-f17de214691f/lesson/e9ff683d-d77f-4eaa-bd54-489ee9f27d2f" />
</CardGroup>


# Demo Updating Cilium Configuration

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Installing-Configuring-Cilium/Demo-Updating-Cilium-Configuration/page

Updating Cilium configuration on Kubernetes clusters using Helm or ConfigMap edits, restarting components, and verifying changes.

This guide shows two ways to change an existing Cilium configuration on a Kubernetes cluster:

* Update via Helm (recommended when Cilium was installed with Helm).
* Edit the Cilium ConfigMap directly (useful for quick runtime changes or when Helm was not used).

These instructions assume you have kubectl and, if using Helm, the Helm CLI configured for the cluster.

<Frame>
  <img alt="A presentation slide titled &#x22;Updating Cilium Configuration&#x22; with a large turquoise curved shape on the right containing the word &#x22;Demo.&#x22; The bottom-left shows a small &#x22;© Copyright KodeKloud&#x22; attribution." />
</Frame>

## 1 — Verify cluster and Cilium installation

Confirm cluster nodes:

```bash theme={null}
kubectl get nodes
```

Confirm Cilium pods (all namespaces):

```bash theme={null}
kubectl get pods -A
```

Example (abbreviated) output:

```text theme={null}
NAMESPACE     NAME                                             READY   STATUS    RESTARTS   AGE
kube-system   cilium-hpfns                                     1/1     Running   0          2m
kube-system   cilium-operator-59944f4b8f-kw9p9                 1/1     Running   0          2m
kube-system   cilium-qn9dg                                     1/1     Running   0          2m
kube-system   coredns-668d6bf9bc-gpc8z                         1/1     Running   0          3m
...
```

If Cilium was installed with Helm, prefer updating configuration via Helm so your changes are tracked by the release.

## Quick comparison: Helm vs ConfigMap editing

| Resource Type                | Use Case                                                     | Recommended when                                                                       |
| ---------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| Helm values + helm upgrade   | Persistent, repeatable configuration changes tracked by Helm | Cilium installed with Helm; you want changes preserved across upgrades                 |
| Edit cilium-config ConfigMap | Immediate runtime tweaks or when Helm was not used           | Quick tests or clusters without Helm-managed Cilium (note: may be overwritten by Helm) |

## 2 — Update configuration via Helm (recommended)

1. Export or open the `values.yaml` you used for the Helm release and change the values you want.\
   Example: enable debug logging by changing:

```yaml theme={null}
debug:
  # -- Enable debug logging
  enabled: false
```

to:

```yaml theme={null}
debug:
  # -- Enable debug logging
  enabled: true
```

2. Confirm the Helm release and namespace (Cilium commonly lives in `kube-system`):

```bash theme={null}
helm list -n kube-system
```

3. Apply the updated values with `helm upgrade`. The `-n` (namespace) flag must match the existing release:

```bash theme={null}
helm upgrade cilium cilium/cilium -n kube-system -f values.yaml
```

A successful upgrade will generate and apply new Kubernetes manifests. Example summary:

```text theme={null}
STATUS: deployed
REVISION: 2
NOTES:
You have successfully upgraded Cilium.
```

## 3 — Update configuration by editing the ConfigMap directly

Cilium stores many runtime options in the `cilium-config` ConfigMap in the `kube-system` namespace. Use this method for quick runtime changes or when Cilium was not installed with Helm.

Inspect whether a specific flag (e.g., `debug`) is set:

```bash theme={null}
kubectl describe configmap cilium-config -n kube-system | grep -i debug -A 3
```

Example output:

```text theme={null}
debug:
true
```

Edit the ConfigMap:

```bash theme={null}
kubectl edit configmap cilium-config -n kube-system
```

Make required changes in the `data:` section. Example — disable IPv6:
Before:

```yaml theme={null}
enable-ipv6: "true"
k8s-require-ipv6-pod-cidr: "true"
```

After:

```yaml theme={null}
enable-ipv6: "false"
