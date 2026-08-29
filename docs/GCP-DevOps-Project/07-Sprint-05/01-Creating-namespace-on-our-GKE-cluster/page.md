# Creating namespace on our GKE cluster

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-05/Creating-namespace-on-our-GKE-cluster/page

This guide explains how to create and manage a Kubernetes namespace on a Google Kubernetes Engine cluster.

In this guide, you’ll learn how to create and manage a dedicated Kubernetes namespace on a Google Kubernetes Engine (GKE) cluster. Namespaces provide logical separation for applications, improving resource management, security, and clarity.

## Why Use Kubernetes Namespaces?

A single GKE cluster can host multiple environments or teams. Namespaces help you:

* Enforce resource quotas and limits per team or environment
* Simplify Role-Based Access Control (RBAC)
* Keep workloads organized and isolated

<Callout icon="lightbulb">
  Namespaces are a native Kubernetes feature. Learn more in the [Kubernetes Namespaces documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/).
</Callout>

## Prerequisites

* A Google Cloud project (e.g., `kodekloud-gcp-training`)
* A GKE cluster named `gcp-devops-project` in zone `us-central1-c`
* Access to **Cloud Shell**, or local installation of [`gcloud`](https://cloud.google.com/sdk/docs) and [`kubectl`](https://kubernetes.io/docs/tasks/tools/)

***

## Step 1. Connect to Your GKE Cluster

1. Open **Cloud Shell** in the GCP Console:\
   **Kubernetes Engine** > **Clusters** > **Connect** > **Run in Cloud Shell**.
2. Authorize Cloud Shell by pressing **Enter** when prompted.
3. Fetch cluster credentials:

   ```bash theme={null}
   gcloud container clusters get-credentials gcp-devops-project \
     --zone us-central1-c \
     --project kodekloud-gcp-training
   ```

Your local `kubeconfig` is now configured to interact with the `gcp-devops-project` cluster.

***

## Step 2. List Existing Namespaces

Run:

```bash theme={null}
kubectl get namespaces
```

Example output:

```txt theme={null}
NAME              STATUS   AGE
default           Active   15m
kube-node-lease   Active   15m
kube-public       Active   15m
kube-system       Active   15m
```

***

## Step 3. Create a New Namespace

Create the `gcp-devops-prod` namespace for production workloads:

```bash theme={null}
kubectl create namespace gcp-devops-prod
```

***

## Step 4. Verify Your New Namespace

List namespaces again:

```bash theme={null}
kubectl get namespaces
```

You should see:

```txt theme={null}
NAME                  STATUS   AGE
default               Active   2m
gcp-devops-prod       Active   5s
kube-node-lease       Active   15m
kube-public           Active   15m
kube-system           Active   15m
```

***

## Step 5. (Optional) Set the New Namespace as Default

To avoid specifying `-n gcp-devops-prod` on every command, update your context:

```bash theme={null}
kubectl config set-context --current --namespace=gcp-devops-prod
```

Confirm your active namespace:

```bash theme={null}
kubectl config view --minify --output "jsonpath={..namespace}"
