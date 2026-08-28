# Enable IPv6 support
ipv6:
  enabled: true
```

Install with the custom values:

```bash theme={null}
cilium install --values values.yaml
```

The CLI auto-detects cluster type and existing components (for example, whether kube-proxy is installed). If kube-proxy is already present, the default behavior is to run Cilium alongside kube-proxy. To replace kube-proxy with Cilium's eBPF-based proxy, enable the appropriate Helm value or use CLI options to enable kube-proxy replacement.

A sample installer log (abridged):

```text theme={null}
Auto-detected Kubernetes kind: kind
Using Cilium version 1.17.0
Auto-detected cluster name: kind-tlv-cluster
Auto-detected kube-proxy has been installed
```

## 4 — Verify Cilium status

After install, verify the Cilium control plane, pods, and related components:

```bash theme={null}
cilium status
```

Example output (abridged and formatted):

```text theme={null}
Cilium:              OK
Operator:            OK
Envoy DaemonSet:     OK
Hubble Relay:        disabled
ClusterMesh:         disabled

DaemonSet           cilium            Desired: 3, Ready: 3/3, Available: 3/3
DaemonSet           cilium-envoy      Desired: 3, Ready: 3/3, Available: 3/3
Deployment          cilium-operator   Desired: 1, Ready: 1/1, Available: 1/1

Containers:
  cilium            Running: 3
  cilium-envoy      Running: 3
  cilium-operator   Running: 1

Cluster Pods: 3/3 managed by Cilium
Helm chart version: 1.17.0
Image versions:
  cilium          quay.io/cilium/cilium:v1.17.0@sha256:...
  cilium-envoy    quay.io/cilium/cilium-envoy:v1.31.5@sha256:...
  cilium-operator quay.io/cilium/operator-generic:v1.17.0@sha256:...
```

This output confirms the Cilium DaemonSet and operator are running and ready across the nodes.

<Callout icon="lightbulb">
  If you want Cilium to replace kube-proxy functionality with the eBPF-based proxy, enable the appropriate Helm values (or use the CLI options) to enable kube-proxy replacement. That is a configuration choice — by default the installer runs alongside kube-proxy when it detects kube-proxy is installed.
</Callout>

## 5 — Preview the manifests (dry run)

To inspect the raw Kubernetes manifests that the CLI will apply, run a dry run and capture the output:

```bash theme={null}
cilium install --dry-run > cilium-dry-run.yaml
```

Open `cilium-dry-run.yaml` to review the generated resources (DaemonSets, Deployments, ConfigMaps, RBAC, etc.). Example excerpt (operator pod spec):

```yaml theme={null}
restartPolicy: Always
priorityClassName: system-cluster-critical
serviceAccountName: "cilium-operator"
automountServiceAccountToken: true
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchLabels:
          io.cilium/app: operator
      topologyKey: kubernetes.io/hostname
nodeSelector:
  kubernetes.io/os: linux
tolerations:
  - operator: Exists
volumes:
  - name: cilium-config-path
    configMap:
      name: cilium-config
```

Reviewing manifests is recommended for audits, compliance, or to tailor Cilium to production environments.

## Resources and next steps

* Cilium Quick Start / Installation: [https://docs.cilium.io/en/stable/gettingstarted/quick-install/](https://docs.cilium.io/en/stable/gettingstarted/quick-install/)
* Cilium CLI repo: [https://github.com/cilium/cilium-cli](https://github.com/cilium/cilium-cli)
* kind project (local Kubernetes): [https://kind.sigs.k8s.io/](https://kind.sigs.k8s.io/)
* Kubernetes docs: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

Suggested next steps:

* Review Helm values to enable production features (Hubble observability, ClusterMesh, etc.).
* If replacing kube-proxy, test kube-proxy replacement settings in a staging cluster first.
* Validate networking and policy behavior with sample workloads and network policies.

Table — Common cilium CLI commands

| Command                              | Purpose                                      |
| ------------------------------------ | -------------------------------------------- |
| cilium install                       | Install Cilium into current kubectl context  |
| cilium install --values values.yaml  | Install with custom Helm values              |
| cilium status                        | Show Cilium and component status             |
| cilium install --dry-run > file.yaml | Preview generated manifests without applying |

You now have Cilium installed using the CLI. Adjust Helm values and CLI options based on your environment and production requirements.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/2fded455-95ea-4183-8cce-f17de214691f/lesson/36065cfe-d592-40bf-8ece-f54bc4ca88fc" />
</CardGroup>


# Demo Installation with Helm

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Installing-Configuring-Cilium/Demo-Installation-with-Helm/page

Guide to installing and verifying Cilium on Kubernetes using Helm, customizing values including IPv6, and checking runtime status and manifests

In this lesson we demonstrate how to install Cilium onto a Kubernetes cluster using Helm. The guide covers adding the Cilium Helm repository, inspecting and customizing chart values, enabling optional IPv6 support, installing the chart into the cluster, and verifying the installation and runtime status.

<Frame>
  <img alt="A presentation slide reading &#x22;Install Celium Helm&#x22; on the left with a large turquoise curved shape on the right containing the word &#x22;Demo.&#x22; Small &#x22;© Copyright KodeKloud&#x22; text appears in the bottom-left." />
</Frame>

Prerequisites

* A Kubernetes cluster with sufficient privileges to install cluster-wide addons (RBAC/ClusterRole/ClusterRoleBinding privileges).
* Helm installed locally (Helm v3+ recommended).
* kubectl configured to target your cluster context.

| Requirement        | Purpose                                           | Example / Link                                                                     |
| ------------------ | ------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Kubernetes cluster | Target platform for Cilium                        | [Kubernetes docs](https://kubernetes.io/)                                          |
| Helm (v3+)         | Package manager used to install the Cilium chart  | [https://helm.sh](https://helm.sh)                                                 |
| kubectl            | Inspect cluster resources and verify installation | [https://kubernetes.io/docs/tasks/tools/](https://kubernetes.io/docs/tasks/tools/) |

If you need to install Helm locally, follow the official instructions at [https://helm.sh](https://helm.sh). A common manual installation sequence:

```bash theme={null}
