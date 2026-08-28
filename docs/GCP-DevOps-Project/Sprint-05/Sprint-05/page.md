# Sprint 05

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-05/Sprint-05/page

This article outlines the steps to deploy Docker images to a Google Kubernetes Engine cluster using a CI/CD pipeline.

In Sprint 0.5, we’ll extend our CI/CD pipeline to push Docker images into a Google Kubernetes Engine (GKE) cluster. By breaking this large goal into focused milestones, we improve visibility, estimation accuracy, and enable parallel work.

<Callout icon="lightbulb">
  Breaking down tasks helps with:

  * Tracking incremental progress
  * Clarifying deliverables
  * Providing more accurate time estimates
  * Allowing multiple team members to work concurrently
</Callout>

## Milestone Breakdown

| Step                         | Goal                                   | Example Command                   |
| ---------------------------- | -------------------------------------- | --------------------------------- |
| 1. Create Namespace          | Isolate resources in the cluster       | `kubectl create namespace my-app` |
| 2. Write Deployment Manifest | Define your Kubernetes Deployment      | See `deployment.yaml` below       |
| 3. Update Cloud Build        | Apply manifests in your build pipeline | See `cloudbuild.yaml` snippet     |
| 4. Validate Deployment       | Ensure pods and services are running   | `kubectl get all -n my-app`       |

<Frame>
  ![The image lists four steps for a deployment process: creating a namespace in a GKE cluster, creating a deployment file, updating Cloud Build code, and validating the deployment.](https://kodekloud.com/kk-media/image/upload/v1752875500/notes-assets/images/GCP-DevOps-Project-Sprint-05/gke-deployment-process-steps.jpg)
</Frame>

***

## 1. Create a GKE Namespace

Define an isolated namespace before any resources are applied:

```yaml theme={null}
