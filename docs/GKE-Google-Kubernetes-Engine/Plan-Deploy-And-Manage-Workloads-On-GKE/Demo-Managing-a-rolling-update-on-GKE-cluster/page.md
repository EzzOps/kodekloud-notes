# Demo Managing a rolling update on GKE cluster

Source: https://notes.kodekloud.com/docs/GKE-Google-Kubernetes-Engine/Plan-Deploy-And-Manage-Workloads-On-GKE/Demo-Managing-a-rolling-update-on-GKE-cluster/page

This tutorial teaches how to manage rolling updates on a GKE cluster, ensuring zero downtime and safe rollbacks.

In this tutorial, you’ll learn how to perform and manage rolling updates on a Google Kubernetes Engine (GKE) cluster. These concepts apply equally to upstream Kubernetes, enabling you to update container images with zero downtime and perform safe rollbacks when needed.

## Prerequisites

* Google Cloud SDK with `gcloud` and `kubectl` installed
* A Google Cloud project with billing enabled
* [Enable the Kubernetes Engine API](https://console.cloud.google.com/apis/library/container.googleapis.com)

***

## 1. Configure and Create the Cluster

First, set your Compute Engine zone and create a single-node GKE cluster named `gke-deep-dive`.

```bash theme={null}
