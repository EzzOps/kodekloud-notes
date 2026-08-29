# Using Helm Charts

Source: https://notes.kodekloud.com/docs/Lens-Kubernetes-IDE/Lens-Introduction/Using-Helm-Charts/page

This guide explains how to use Helm charts in Lens for deploying applications to Kubernetes.

Deploying applications to Kubernetes is seamless with Helm charts and Lens. In this guide, you’ll learn how to add Helm repositories, browse and install charts, customize values, inspect deployed resources, and connect to your application—all within Lens.

## Prerequisites

> **lightbulb** * Lens installed and connected to your Kubernetes cluster
  * [Helm][helm-docs] CLI installed and configured
  * Access to the internet (for public Helm repositories)

***

## 1. Add Helm Repositories in Lens

1. Open Lens and select **Clusters → *your-cluster***.
2. Go to **Lens → Preferences → Kubernetes → Helm**.
3. Click **Add** to include community and custom repositories (e.g., Aerokube, Armory, Bitnami).

![The image shows a software interface for managing Helm charts, with a dropdown menu listing various repositories and an option to add a custom Helm repository.](https://kodekloud.com/kk-media/image/upload/v1752881202/notes-assets/images/Lens-Kubernetes-IDE-Using-Helm-Charts/helm-charts-management-interface.jpg)

***

## 2. Browse and Search Charts

1. Press **Esc** to close Preferences.
2. Navigate to **Apps → Charts** in the sidebar.
3. Filter by repository or search for **cassandra**.

![The image shows a software interface listing various Helm charts, including their names, descriptions, versions, app versions, and repositories. The interface appears to be part of a Kubernetes management tool.](https://kodekloud.com/kk-media/image/upload/v1752881203/notes-assets/images/Lens-Kubernetes-IDE-Using-Helm-Charts/helm-charts-kubernetes-interface.jpg)

Click **Details** on the Cassandra chart to view installation steps and default values.

***

## 3. Install the Cassandra Chart

You can install directly in Lens or via the CLI:

```bash theme={null}
