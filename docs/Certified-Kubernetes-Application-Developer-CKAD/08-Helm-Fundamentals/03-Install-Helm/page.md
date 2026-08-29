# Install Helm

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Helm-Fundamentals/Install-Helm/page

This article provides instructions for installing Helm on Linux systems, including prerequisites and methods using Snap and APT.

Before installing Helm, ensure you have a working Kubernetes cluster and a correctly configured kubectl utility on your local machine. A valid kubeconfig file containing the proper credentials for your target cluster is essential.

> **lightbulb** Verify that your Kubernetes setup is operational and that kubectl is set up before proceeding with the Helm installation.

Helm supports Linux, Windows, and macOS environments. This guide focuses on the installation process for Linux systems.

## Installing Helm on Linux

### Using Snap

If your Linux distribution supports Snap, you can install Helm using the Snap package manager. Snap's classic confinement allows Helm unrestricted access to locate your kubeconfig file (typically in your home directory). Execute the following command:

```bash theme={null}
sudo snap install helm --classic
```

### Installing Helm on APT-Based Distributions

For Debian, Ubuntu, or similar APT-based distributions, follow these steps:

```bash theme={null}
