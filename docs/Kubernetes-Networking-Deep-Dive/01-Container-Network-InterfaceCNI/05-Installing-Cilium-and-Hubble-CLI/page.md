# Check the health of your Cilium cluster
cilium status

# Run a connectivity test between pods
cilium connectivity test

# Enable Hubble for network observability
cilium hubble enable

# Install Cilium into your Kubernetes cluster
cilium install
```

> **lightbulb** The Cilium CLI v0.14+ supports both direct CLI installs and Helm-style deployments, giving you full flexibility.

## 2. Installation Methods: CLI vs. Helm

Cilium can be installed in two interchangeable ways:

| Installation Method | Command Example                                     | Benefits                             |
| ------------------- | --------------------------------------------------- | ------------------------------------ |
| Cilium CLI          | `cilium install`                                    | All-in-one tool; built-in validation |
| Helm Chart          | `helm install cilium cilium/cilium --version 1.x.y` | Familiar Helm workflow; chart config |

![The image shows logos for "Cilium" and "Helm" under the title "Installation Options and Components," with a note about the benefits for Helm users who also use the Cilium CLI.](https://kodekloud.com/kk-media/image/upload/v1752880260/notes-assets/images/Kubernetes-Networking-Deep-Dive-Installing-Cilium-Overview/cilium-helm-installation-options-components.jpg)

In this demo, we’ll walk through both methods side by side.

## 3. Observability with Hubble

[Hubble][hubble-docs] provides real-time visibility into network flows, service dependencies, and security policies. You can enable it:

* **During** Cilium installation:
  ```bash theme={null}
  cilium install --enable-hubble
  ```
* **After** Cilium is up and running:
  ```bash theme={null}
  cilium hubble enable
  ```

> **triangle-alert** You must install Cilium before enabling Hubble, as Hubble relies on core Cilium components.

To interact with Hubble:

```bash theme={null}
# Install Hubble CLI
curl -L --remote-name https://github.com/cilium/hubble-cli/releases/latest/download/hubble-linux-amd64.tar.gz
tar xzvf hubble-linux-amd64.tar.gz
sudo mv hubble /usr/local/bin/

# Check Hubble status
hubble status

# Stream live network events
hubble observe
```

***

* [Cilium Documentation][cilium-docs]
* [Cilium CLI Reference][cilium-cli]
* [Hubble Observability][hubble-docs]
* [Helm Charts – Cilium][cilium-helm]

[cilium-docs]: https://docs.cilium.io/

[cilium-cli]: https://docs.cilium.io/cilium-cli/

[hubble-docs]: https://docs.cilium.io/gettingstarted/hubble/

[cilium-helm]: https://docs.cilium.io/gettingstarted/k8s-install-default/

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-networking/module/5eea49e6-caea-4e84-88a0-268ea6f263af/lesson/a8f11d12-c943-4891-b899-e28bb4a94c03)


# Installing Cilium and Hubble CLI

Source: https://notes.kodekloud.com/docs/Kubernetes-Networking-Deep-Dive/Container-Network-InterfaceCNI/Installing-Cilium-and-Hubble-CLI/page

This guide explains how to install the Cilium and Hubble command-line tools on a Linux system.

Before you deploy Cilium in your Kubernetes cluster, you’ll need to install two command-line tools locally: the Cilium CLI and the Hubble CLI. This guide walks you through downloading, verifying, and installing both CLIs on Linux.

## Install Cilium CLI

Follow these steps to fetch the latest stable Cilium CLI release, verify its integrity, and install it to `/usr/local/bin`.

### 1. Download and verify the Cilium CLI

> **lightbulb** Make sure you have `curl`, `sha256sum`, and `tar` installed. You’ll also need `sudo` privileges to copy the binary into `/usr/local/bin`.

```bash theme={null}
