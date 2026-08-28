# Demo Configure cluster autoscaling

Source: https://notes.kodekloud.com/docs/GKE-Google-Kubernetes-Engine/GKE-Deployment-and-Administration/Demo-Configure-cluster-autoscaling/page

Learn to enable and manage autoscaling for Google Kubernetes Engine clusters and node pools using the gcloud CLI.

In this guide, you’ll learn how to enable and manage **autoscaling** for your Google Kubernetes Engine (GKE) clusters and node pools using the `gcloud` CLI. We’ll cover cluster creation with autoscaling, verifying configurations, and updating existing pools.

## Overview

Autoscaling in GKE lets your cluster grow or shrink node capacity automatically based on workload. Configuring autoscaling properly helps you optimize cost and performance.

## Prerequisites

* A Google Cloud project with billing enabled
* [Cloud SDK (gcloud)](https://cloud.google.com/sdk/docs/install) installed and authenticated
* IAM permissions: `Kubernetes Engine Admin`, `Compute Admin`

| Resource        | Purpose                                    | Reference                                                                                                                                                  |
| --------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| gcloud CLI      | Manage GKE clusters                        | [https://cloud.google.com/sdk](https://cloud.google.com/sdk)                                                                                               |
| GKE Autoscaling | Automatic scaling of node pools            | [https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-autoscaler](https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-autoscaler) |
| IAM Roles       | Permissions to create and modify resources | [https://cloud.google.com/iam/docs/understanding-roles](https://cloud.google.com/iam/docs/understanding-roles)                                             |

## 1. Set the Default Compute Zone

Configure a default zone so you don’t need to specify `--zone` every time:

```bash theme={null}
gcloud config set compute/zone us-west1-a
```

<Callout icon="lightbulb">
  You can override this with `--zone` or set a default region:

  ```bash theme={null}
  gcloud config set compute/region us-west1
  ```
</Callout>

## 2. Create a Cluster with Autoscaling

Use the following command to create `gke-deep-dive-auto` with autoscaling enabled (1–2 nodes):

```bash theme={null}
gcloud container clusters create gke-deep-dive-auto \
  --enable-autoscaling \
  --num-nodes=1 \
  --min-nodes=1 \
  --max-nodes=2 \
  --disk-type=pd-standard \
  --disk-size=10
```

| Flag                             | Description                   |
| -------------------------------- | ----------------------------- |
| `--enable-autoscaling`           | Enables cluster autoscaling   |
| `--num-nodes=1`                  | Initial node count            |
| `--min-nodes=1`, `--max-nodes=2` | Defines the autoscaling range |
| `--disk-type=pd-standard`        | Boot disk type                |
| `--disk-size=10`                 | Boot disk size in GB          |

<Callout icon="triangle-alert">
  Cluster creation can take several minutes. Monitor progress in the Cloud Console or via:

  ```bash theme={null}
  gcloud container operations list
  ```
</Callout>

## 3. Verify Cluster Autoscaling

Once ready, describe just the autoscaling block:

```bash theme={null}
gcloud container clusters describe gke-deep-dive-auto \
  --format="yaml(nodePools[].autoscaling)"
```

Expected output:

```yaml theme={null}
- autoscaling:
    enabled: true
    minNodeCount: 1
    maxNodeCount: 2
```

To view the full node pool details:

```bash theme={null}
gcloud container clusters describe gke-deep-dive-auto \
  --format="yaml(nodePools[0])"
```

## 4. Compare with a Cluster Without Autoscaling

If you omit `--enable-autoscaling` when creating a cluster, the `autoscaling` section is not present:

```bash theme={null}
gcloud container clusters describe gke-deep-dive \
  --format="yaml(nodePools[0])"
```

No `autoscaling:` block will appear in the output.

## 5. Add a New Node Pool with Autoscaling

You can attach a new node pool to an existing cluster and enable autoscaling:

```bash theme={null}
gcloud container node-pools create gke-deep-dive-node-pool \
  --cluster=gke-deep-dive \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=2 \
  --disk-type=pd-standard \
  --disk-size=10
```

Verify both pools:

```bash theme={null}
gcloud container clusters describe gke-deep-dive \
  --format="yaml(nodePools)"
```

Look for:

```yaml theme={null}
- name: gke-deep-dive-node-pool
  autoscaling:
    enabled: true
    minNodeCount: 1
    maxNodeCount: 2
```

## 6. Enable Autoscaling on an Existing Node Pool

To update an existing node pool (e.g., `default-pool`) and enable autoscaling:

```bash theme={null}
gcloud container clusters update gke-deep-dive \
  --enable-autoscaling \
  --node-pool=default-pool \
  --min-nodes=1 \
  --max-nodes=2
```

Re-run the description to confirm:

```bash theme={null}
gcloud container clusters describe gke-deep-dive \
  --format="yaml(nodePools)"
```

Both pools should now include:

```yaml theme={null}
autoscaling:
  enabled: true
  minNodeCount: 1
  maxNodeCount: 2
```

Congratulations! You’ve successfully configured cluster-level and node-pool–level autoscaling in GKE.

## Links and References

* [GKE Cluster Autoscaler Overview](https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-autoscaler)
* [gcloud container clusters create](https://cloud.google.com[AWS_SECRET_ACCESS_KEY]/create)
* [Google Kubernetes Engine Documentation](https://cloud.google.com/kubernetes-engine/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gke-google-kubernetes-engine/module/897349c1-bf57-4c08-82fb-0aa0ce0e0f6b/lesson/dbda1f08-6b26-4ee2-8ee0-2f4cbfd59eb2" />
</CardGroup>
