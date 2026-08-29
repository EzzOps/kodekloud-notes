# Sprint 02 review

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-02/Sprint-02-review/page

This article reviews Sprint 02, focusing on setting up a GKE cluster and understanding Kubernetes fundamentals.

Welcome back! In this lesson, we recap Sprint 02, where we focused on:

| Objective              | Description                                                            |
| ---------------------- | ---------------------------------------------------------------------- |
| Create a GCP account   | Sign up for Google Cloud Platform and configure billing.               |
| Learn GKE fundamentals | Understand Kubernetes architecture and Google Kubernetes Engine (GKE). |
| Set up a GKE cluster   | Deploy and initialize a Kubernetes cluster on GCP.                     |

***

## What We Achieved

1. **GCP Account Setup**
   * Registered for a [Google Cloud Platform](https://cloud.google.com) account.
   * Enabled billing and configured IAM permissions.

2. **GKE Fundamentals**
   * Explored key concepts: nodes, pods, control plane, and networking.
   * Reviewed GKE-specific features like auto-scaling and regional clusters.

3. **Cluster Provisioning**
   * Created a GKE cluster using the `gcloud` CLI.
   * Retrieved credentials and verified the cluster’s health.

<Callout icon="triangle-alert">
  Make sure your IAM user has the **Kubernetes Engine Admin** role before creating a cluster. Insufficient permissions will cause `gcloud container clusters create` to fail.
</Callout>

***

## Essential gcloud & kubectl Commands

```bash theme={null}
