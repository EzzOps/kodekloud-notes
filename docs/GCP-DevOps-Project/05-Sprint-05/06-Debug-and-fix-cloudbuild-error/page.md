# gcp-devops-prod
```

> **triangle-alert** Switching the default namespace affects all subsequent `kubectl` commands in this session.

***

## Step 6. View Namespaced Workloads in GCP Console

1. In the GCP Console, go to **Kubernetes Engine** > **Workloads**.
2. Click **Show system workloads**, then open the **Filter** pane.
3. Select **gcp-devops-prod** under Namespace and apply.

You’ll see workloads scoped to your production namespace (none yet, until you deploy).

***

## Command Reference Table

| Step | Description                             | Command                                                                                                              |
| ---- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| 1    | Authenticate to GKE cluster             | `gcloud container clusters get-credentials gcp-devops-project --zone us-central1-c --project kodekloud-gcp-training` |
| 2    | List all namespaces                     | `kubectl get namespaces`                                                                                             |
| 3    | Create a new namespace                  | `kubectl create namespace gcp-devops-prod`                                                                           |
| 5    | Set new namespace as default (optional) | `kubectl config set-context --current --namespace=gcp-devops-prod`                                                   |

***

## Links and References

* [Kubernetes Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
* [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
* [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

That’s it! You’ve successfully created, verified, and configured a namespace in your GKE cluster. You can now deploy applications into `gcp-devops-prod`.

- [Watch Video](https://learn.kodekloud.com/user/courses/gcp-devops-project/module/c1a43d47-87cb-459f-a9bf-2000d6223395/lesson/5edc012d-3f98-4d8d-b1ff-0ad0ec770e72)


# Debug and fix cloudbuild error

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-05/Debug-and-fix-cloudbuild-error/page

This guide helps identify and fix a Cloud Build failure caused by an incorrect GKE cluster name in the configuration.

## Overview

We encountered a Cloud Build failure due to an incorrect GKE cluster name. In this guide, we will:

* Identify the root cause
* Correct the `cloudbuild.yaml` configuration
* Commit and merge the fix
* Monitor the updated build

## 1. Original `cloudbuild.yaml`

The pipeline failed because the cluster name in the `gke-deploy` step didn't match the actual cluster in the console:

```yaml theme={null}
steps:
  # build the container image
  - name: "gcr.io/cloud-builders/docker"
    args: ["build", "--tag", "gcr.io/$PROJECT_ID/gcpdevops", "."]
  # push container image
  - name: "gcr.io/cloud-builders/docker"
    args: ["push", "gcr.io/$PROJECT_ID/gcpdevops"]
  # deploy container image to GKE
  - name: "gcr.io/cloud-builders/gke-deploy"
    args:
      - run
      - --filename=gke.yaml
      - --image=gcr.io/$PROJECT_ID/gcpdevops
      - --location=us-central1-c
      - --cluster=gke-gcp-devops
      - --namespace=gcp-devops-prod
```

> **lightbulb** Always verify resource names in the [Google Cloud Console](https://console.cloud.google.com/). A mismatch will cause your build to fail.

## 2. Verify the Cluster Name

Navigate to the **Kubernetes clusters** section in the console. You'll see the actual name: **GCP DevOps Project**.

## 3. Updated `cloudbuild.yaml`

Replace the incorrect cluster reference (`gke-gcp-devops`) with the correct one (`gcp-devops-project`) and adjust the location flag:

```yaml theme={null}
steps:
  - id: "build the container image"
    name: "gcr.io/cloud-builders/docker"
    args: ["build", "-t", "gcr.io/$PROJECT_ID/gcpdevops", "."]
  - id: "push container image"
    name: "gcr.io/cloud-builders/docker"
    args: ["push", "gcr.io/$PROJECT_ID/gcpdevops"]
  - id: "deploy container image to GKE"
    name: "gcr.io/cloud-builders/gke-deploy"
    args:
      - "--filename=gke.yaml"
      - "--image=gcr.io/$PROJECT_ID/gcpdevops"
      - "--location=us-central1"
      - "--cluster=gcp-devops-project"
      - "--namespace=gcp-devops-prod"
```

## 4. Commit and Push the Fix

```bash theme={null}
git commit --amend --reset-author
