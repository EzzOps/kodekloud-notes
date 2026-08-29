# Push Based CICD Workflow

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/CICD-Workflow-for-AKS/Push-Based-CICD-Workflow/page

This guide explains converting an imperative AKS deployment to a declarative setup with YAML manifests and integrating it into a push-based CI/CD pipeline.

In this guide, you’ll learn how to convert an imperative AKS deployment into a declarative setup with YAML manifests and integrate it into a push-based CI/CD pipeline. We cover:

1. Exporting existing Kubernetes resources to YAML
2. Cleaning up and reapplying manifests
3. Deleting old imperative resources
4. Redeploying declaratively
5. Designing a push-based CI/CD workflow with Azure DevOps

***

## Preparing Your Environment

1. Log in to your Azure subscription (local machine or Cloud Shell).
2. Fetch and merge your AKS credentials into `kubeconfig`:

```bash theme={null}
az aks get-credentials \
  --name AKS1-KodeKloudApp \
  --resource-group MyResourceGroup
