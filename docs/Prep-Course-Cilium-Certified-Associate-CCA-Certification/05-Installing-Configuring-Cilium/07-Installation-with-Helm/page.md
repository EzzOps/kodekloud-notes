# Determine the stable CLI version
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)

# Default architecture; override for aarch64
CLI_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then
  CLI_ARCH=arm64
fi

# Download the tarball and checksum
curl -L --fail --remote-name-all "https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz"{,.sha256sum}

# Extract and install
tar xzf "cilium-linux-${CLI_ARCH}.tar.gz"
sudo mv cilium /usr/local/bin/
```

Verify the installation:

```bash theme={null}
cilium version
```

Notes:

* For macOS use the `darwin` tarball; for Windows use the appropriate zip.
* If you prefer package managers, check the Cilium docs for Homebrew, Chocolatey, or distribution packages.

## Install Cilium into the cluster

The Cilium CLI uses your current kubeconfig context to determine which cluster to install into. Ensure your kubeconfig points to the intended cluster before running the installer.

Warning: make sure you are targeting the correct cluster/context to avoid accidental changes to production clusters.

> **warning** Ensure your kubeconfig context is set to the intended cluster before running `cilium install`. Installing Cilium will create ClusterRoles, DaemonSets, Deployments, and other cluster-scoped resources.

Run the installer:

```bash theme={null}
cilium install
```

Wait for components to become healthy. Use --wait to block until readiness conditions are met:

```bash theme={null}
cilium status --wait
```

Example output (truncated):

```bash theme={null}
/'`\
/'--\__\
\__/--/
 \__/

Cilium:        OK
Operator:      OK
Hubble:        disabled
ClusterMesh:   disabled

DaemonSet            cilium               Desired: 2, Ready: 2/2, Available: 2/2
Deployment           cilium-operator      Desired: 2, Ready: 2/2, Available: 2/2
Containers:          cilium-operator      Running: 2
                     cilium               Running: 2
Image versions       cilium               quay.io/cilium/cilium:v1.9.5: 2
                     cilium-operator      quay.io/cilium/operator-generic:v1.9.5: 2
```

A successful deployment shows components (DaemonSet, Deployment, containers) with matching Desired/Ready/Available counts.

## Preview resources with a dry run

If you want to review the exact Kubernetes manifests that will be applied without changing the cluster, use a dry run. This is useful for auditing and validating Helm values before applying them.

```bash theme={null}
cilium install --dry-run
```

This prints the rendered YAML to stdout so you can inspect it, pipe to a file, or run `kubectl apply -f -` later when ready.

## Common CLI commands

| Command                    | Purpose                                         | Notes                             |
| -------------------------- | ----------------------------------------------- | --------------------------------- |
| `cilium install`           | Install Cilium using current kubeconfig context | Uses Helm under the hood          |
| `cilium install --dry-run` | Render manifests without applying               | Good for validation/auditing      |
| `cilium status --wait`     | Wait until Cilium components are ready          | Blocks until readiness conditions |
| `cilium uninstall`         | Remove Cilium resources from cluster            | Use with caution in production    |

## Configuring Cilium at install time

The Cilium CLI uses the Cilium Helm chart to render manifests. You can customize installation by supplying Helm values either inline via `--helm-set` or from a values file via `--values`.

Examples:

```bash theme={null}
# Pass individual Helm values from the CLI
cilium install \
  --helm-set ipv6.enabled=true \
  --helm-set routingMode=native \
  --helm-set autoDirectNodeRoutes=true

# Or use a YAML values file
cilium install --values values.yaml
```

For a complete list of configuration keys, review the Helm chart's `values.yaml` in the Cilium GitHub repository or the chart documentation.

> **lightbulb** The available configuration keys come from the Cilium Helm chart. Use --dry-run to preview the final rendered manifest or check the chart's values.yaml to see all options.

## Sample values.yaml

Below is an example `values.yaml` that enables IPv6 and configures dual-stack IPAM using a cluster pool. Adjust CIDRs and other options to match your network design and cluster requirements.

```yaml theme={null}
# Enable IPv6 support
ipv6:
  enabled: true

# Enable dual-stack mode (optional, if using both IPv4 and IPv6)
ipam:
  mode: "cluster-pool"
  operator:
    clusterPoolIPv6PodCIDRList:
      - "fd00::/104" # Adjust based on your network setup

# Use native routing mode (recommended for better performance)
routingMode: "native"

# eBPF/networking-related settings
bpf:
  masquerade: true
  tproxy: true
```

## Best practices and references

* Always validate rendered manifests using `cilium install --dry-run` before applying to production.
* Use the table above to quickly reference common cilium CLI commands.
* Consult the official documentation and Helm chart values:
  * Cilium Documentation: [https://cilium.io/docs/](https://cilium.io/docs/)
  * Cilium Helm chart / values: [https://github.com/cilium/cilium/tree/main/install/kubernetes/cilium](https://github.com/cilium/cilium/tree/main/install/kubernetes/cilium)
  * Cilium CLI releases: [https://github.com/cilium/cilium-cli/releases](https://github.com/cilium/cilium-cli/releases)

With these steps you can install and configure Cilium using the CLI, preview resources before applying changes, and supply Helm values either inline or via a values file.

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/2fded455-95ea-4183-8cce-f17de214691f/lesson/474fe5d0-25a0-4214-b89c-325d50c0e22e)


# Installation with Helm

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Installing-Configuring-Cilium/Installation-with-Helm/page

How to install and configure Cilium with Helm, manage CRDs, customize values, and verify deployment in Kubernetes.

In this lesson we cover how to install Cilium using Helm: adding the chart repository, customizing the installation with a values file, applying any required CRDs, and verifying the deployed resources.

<Frame>
  <img alt="A blue-green gradient slide with the title &#x22;Installing Cilium With Helm&#x22; centered. A small &#x22;© Copyright KodeKloud&#x22; notice appears in the bottom-left corner." />
</Frame>

## Quick workflow

1. Add the Cilium Helm repository to your local Helm configuration.
2. (Optional) Dump and edit the chart defaults into a values.yaml to customize behavior.
3. Ensure CRDs required by the chart are installed (some chart versions separate CRDs).
4. Install the Cilium chart into the target namespace (create it or use --create-namespace).
5. Inspect the rendered manifests and verify Kubernetes resources are running.

## Prerequisites

* Helm v3 installed and configured.
* kubectl configured for the target cluster.
* Sufficient cluster privileges (cluster-admin or equivalent) to create cluster-scoped resources and CRDs.

## Add the Cilium Helm repository and prepare values

Run these commands to add the official Cilium chart repo and fetch the default values for editing:

```bash theme={null}
