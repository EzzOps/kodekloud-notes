# Add the Cilium Helm repository
helm repo add cilium https://helm.cilium.io

# Update local repo cache
helm repo update

# (Optional) Dump chart default values so you can edit them
helm show values cilium/cilium > values.yaml
```

* Edit values.yaml to customize things like operator settings, IPAM mode, enabling Hubble, kube-proxy replacement, node init settings, or image overrides.
* If you want the chart defaults, skip creating or editing values.yaml and install directly.

## CRDs: important note

> **warning** Some Cilium chart versions separate CRDs from the main chart. If the chart requires CRDs to be installed separately, apply the CRD manifests or install the cilium-crds chart before installing the main cilium chart. Helm's automatic CRD handling can vary by chart version.

If the chart provides a cilium-crds chart or CRD manifests, install/apply them first. Example (if provided by the chart):

```bash theme={null}
# Example: install CRDs separately if the chart exposes them
helm install cilium-crds cilium/cilium-crds --namespace kube-system --create-namespace
# or apply CRD manifests provided by the chart repository
kubectl apply -f https://raw.githubusercontent.com/cilium/cilium/<version>/install/kubernetes/00-crds.yaml
```

## Install the Cilium chart

Install Cilium into the kube-system namespace (or your preferred namespace). Create the namespace first or use --create-namespace:

```bash theme={null}
# Install Cilium in the kube-system namespace, using any customizations from values.yaml
helm install cilium cilium/cilium --namespace kube-system -f values.yaml
# OR (create namespace automatically)
helm install cilium cilium/cilium --namespace kube-system --create-namespace -f values.yaml
```

You can omit `-f values.yaml` to use the chart defaults.

## Inspect the generated manifests and verify resources

To review what Helm rendered and applied:

```bash theme={null}
# Show the final manifest rendered by Helm for the release "cilium"
helm get manifest cilium -n kube-system
```

To examine live Kubernetes resources created by the chart:

```bash theme={null}
# List Cilium pods and related resources (label may vary by chart version)
kubectl get pods,ds,svc -n kube-system -l k8s-app=cilium

# If that label does not match your installation, list all resources in the namespace
kubectl get all -n kube-system

# Check CRDs created for Cilium
kubectl get crds | grep cilium
```

## Common commands reference

| Task                      | Command / Example                                                          |               |
| ------------------------- | -------------------------------------------------------------------------- | ------------- |
| Add Cilium Helm repo      | `helm repo add cilium https://helm.cilium.io`                              |               |
| Show chart default values | `helm show values cilium/cilium > values.yaml`                             |               |
| Install Cilium            | `helm install cilium cilium/cilium --namespace kube-system -f values.yaml` |               |
| Get rendered manifest     | `helm get manifest cilium -n kube-system`                                  |               |
| List Cilium workloads     | `kubectl get pods,ds,svc -n kube-system -l k8s-app=cilium`                 |               |
| Verify CRDs               | \`kubectl get crds                                                         | grep cilium\` |

## Links and references

* [Cilium Helm repository](https://helm.cilium.io)
* [Cilium documentation](https://docs.cilium.io/)
* [Helm documentation](https://helm.sh/docs/)
* [Kubernetes documentation](https://kubernetes.io/docs/)

You can skip creating a values.yaml to use all chart defaults, or generate and edit the values.yaml to apply non-default configuration changes before installing.

> **lightbulb** Ensure you have appropriate cluster permissions (cluster-admin or equivalent) when installing Cilium, since it creates cluster-wide resources and CRDs.

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/2fded455-95ea-4183-8cce-f17de214691f/lesson/6c872543-3227-4186-90ea-63667adc9995)


# Note About Cilium CLI

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Installing-Configuring-Cilium/Note-About-Cilium-CLI/page

Explains difference between the local Cilium CLI used for installation and cluster management and the in‑pod cilium/cilium-dbg tools used for in-cluster diagnostics and debugging

So before we proceed, a quick clarification about the Cilium command-line tools — this often causes confusion later when working with clusters.

<Frame>
  <img alt="A teal-to-blue gradient slide with a subtle diamond pattern and centered white text reading &#x22;A Note About Cilium CLI.&#x22; A small copyright notice for KodeKloud appears in the bottom-left." />
</Frame>

There are two separate command-line tools that share the name "cilium," but they serve different purposes and run in different environments:

* A local Cilium CLI binary you install on your workstation. It is used for installing Cilium on a cluster and for higher-level management and checks (for example, `cilium install` and `cilium status`).
* One or more Cilium binaries that run inside Cilium agent pod(s) in the cluster. These in-pod tools — commonly `cilium` and `cilium-dbg` — are focused on in-cluster diagnostics and advanced debugging.

> **lightbulb** These are distinct tools even though they share the same command name. Use the local CLI for installation and cluster-level checks; use the in-pod binaries for deep debugging and diagnostics inside the cluster.

Comparison at a glance:

| Tool                           | Primary scope                                    | Typical location                       | Common examples                             |
| ------------------------------ | ------------------------------------------------ | -------------------------------------- | ------------------------------------------- |
| Local Cilium CLI               | Install, upgrade, and basic cluster-level checks | Your workstation / CI runner           | `cilium install`, `cilium status`           |
| In-pod `cilium` / `cilium-dbg` | Deep diagnostics, runtime troubleshooting        | Inside Cilium agent pods (kube-system) | `cilium status` (in-pod), `cilium-dbg help` |

Examples of common commands

Local machine (installer / management CLI)

```bash theme={null}
