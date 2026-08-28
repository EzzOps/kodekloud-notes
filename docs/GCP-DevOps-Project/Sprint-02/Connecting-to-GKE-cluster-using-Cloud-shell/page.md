# Connecting to GKE cluster using Cloud shell

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-02/Connecting-to-GKE-cluster-using-Cloud-shell/page

This article provides a guide to connect to a GKE cluster using Cloud Shell, authenticate, verify connectivity, and explore workloads.

Welcome to this step-by-step guide on establishing a secure connection to your Google Kubernetes Engine (GKE) cluster via Google Cloud Shell. You’ll learn how to authenticate your session, verify connectivity with `kubectl`, and explore workloads directly in the Google Cloud Console.

## 1. Retrieve Cluster Credentials

1. Open the [GKE Clusters](https://console.cloud.google.com/kubernetes/list) page in the Google Cloud Console.
2. Click your cluster name.
3. Select **Connect**, then choose **Run in Cloud Shell**.

Cloud Shell will launch at the bottom of your browser with the following command pre-filled:

```bash theme={null}
gcloud container clusters get-credentials gcp-devops-project \
  --region us-central1 \
  --project flowing-castle-374710
```

Press **Enter**, then **Authorize** when prompted. This updates your local kubeconfig so that `kubectl` can interact with your GKE cluster.

<Callout icon="lightbulb">
  You need to run this `gcloud container clusters get-credentials` command each time you start a new Cloud Shell session, as kubeconfig configurations aren’t persisted across sessions.
</Callout>

## 2. Verify Connection with kubectl

After retrieving credentials, confirm your connection and inspect system components:

| kubectl Command                   | Description                                    |
| --------------------------------- | ---------------------------------------------- |
| `kubectl get namespaces`          | List all namespaces in the cluster             |
| `kubectl get pods -n kube-system` | List all pods in the **kube-system** namespace |

Run:

```bash theme={null}
