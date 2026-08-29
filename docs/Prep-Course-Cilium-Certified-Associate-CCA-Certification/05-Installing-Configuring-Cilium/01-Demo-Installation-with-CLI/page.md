# Demo Installation with CLI

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Installing-Configuring-Cilium/Demo-Installation-with-CLI/page

Guide to install and verify Cilium on Kubernetes using the Cilium CLI, including creating a kind cluster, installing the CLI, deploying Cilium, checking status, and previewing manifests.

This guide walks through installing Cilium (a Kubernetes CNI powered by eBPF) on a cluster using the Cilium CLI. It covers creating a local example cluster with kind (optional), installing the cilium CLI, installing Cilium into the cluster, verifying the installation, and previewing the manifests that the CLI applies.

Target audience: Kubernetes users who want to replace or install a CNI with Cilium and those validating Cilium deployments in local or cloud clusters.

## Prerequisites

| Requirement                      | Purpose / Notes                                                                                               |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Kubernetes cluster without a CNI | The cluster must not already have a CNI installed (kubelet nodes will otherwise report NotReady).             |
| kubectl configured               | kubectl must point to the target cluster context.                                                             |
| (Optional) kind                  | Useful for local testing. The examples below show how to create a kind cluster with the default CNI disabled. |

> **lightbulb** You can use any Kubernetes distribution (kind, Minikube, EKS, GKE, etc.). The important requirement for this demonstration is that the cluster must not have a CNI installed — otherwise kubelet nodes will report NotReady until a CNI is present.

## 1 — Create a kind cluster (example)

If you want to follow along locally, create a kind cluster and disable the default CNI so we can install Cilium manually.

Save this example as `kind.config`:

```yaml theme={null}
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: tlv-cluster
networking:
  ipFamily: dual
  disableDefaultCNI: true
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```

Create the cluster:

```bash theme={null}
time kind create cluster --config kind.config
```

Switch kubectl context to the new cluster:

```bash theme={null}
kubectl config use-context kind-tlv-cluster
```

Verify node status. Nodes will typically show NotReady until a CNI is installed:

```bash theme={null}
kubectl get nodes
```

Example output:

```text theme={null}
NAME                         STATUS     ROLES           AGE   VERSION
tlv-cluster-control-plane    NotReady   control-plane   45s   v1.32.2
tlv-cluster-worker           NotReady   <none>          30s   v1.32.2
tlv-cluster-worker2          NotReady   <none>          30s   v1.32.2
```

## 2 — Install the Cilium CLI

Open the official Cilium Quick Installation page for the latest installation instructions:
[https://docs.cilium.io/en/stable/gettingstarted/quick-install/](https://docs.cilium.io/en/stable/gettingstarted/quick-install/)

<Frame>
  <img alt="A browser screenshot of the Cilium documentation page titled &#x22;Cilium Quick Installation,&#x22; showing installation instructions and a left-hand navigation menu. A green mouse cursor is visible pointing at the page text." />
</Frame>

On a Linux host you can download and install the cilium CLI with the following script. It detects CPU architecture, validates the tarball checksum, and installs the binary to `/usr/local/bin`:

```bash theme={null}
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then CLI_ARCH=arm64; fi

curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}
sha256sum --check cilium-linux-${CLI_ARCH}.tar.gz.sha256sum
sudo tar xzvf cilium-linux-${CLI_ARCH}.tar.gz -C /usr/local/bin
rm cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}
```

Confirm installation:

```bash theme={null}
cilium version
```

Example output:

```text theme={null}
cilium-cli: v0.18.2 compiled with go1.24.0 on linux/amd64
cilium image (default): v1.17.0
cilium image (stable): v1.17.2
cilium image (running): unknown. Unable to obtain cilium version. Reason: release: not found
```

Note: the "cilium image (running)" field is unknown until Cilium is installed and running in the cluster.

## 3 — Install Cilium with the CLI

By default, the CLI installs into the current kubectl context. Install with:

```bash theme={null}
cilium install
```

If you need custom settings, prepare a Helm values file (the CLI converts these into the Helm chart values) and pass it with `--values`.

Example `values.yaml` (enable IPv6):

```yaml theme={null}
