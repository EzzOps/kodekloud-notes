# Scaling the Deployment using kubectl

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/Working-with-AKS/Scaling-the-Deployment-using-kubectl/page

This tutorial explains how to scale an Azure Kubernetes Service deployment and understand the pod limit enforced by Azure CNI.

In this tutorial, you’ll learn how to scale an Azure Kubernetes Service (AKS) deployment and understand the per-node pod limit enforced by Azure CNI. We’ll cover:

1. Inspecting your current Deployment and Service
2. Scaling the Deployment to 5 replicas
3. Hitting the 30-pod per-node limit
4. Examining Namespaces and system pods

***

## 1. Inspect the current Deployment and Service

Before scaling, verify your application’s replica count and external endpoint.

```bash theme={null}
