# Continuous Deployment ArgoCD

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Package-Installation/Continuous-Deployment-ArgoCD/page

Guide to installing and accessing ArgoCD with Glasskube for GitOps continuous deployment, including initial admin password retrieval, dashboard access, and security recommendations.

With cluster monitoring in place, the next step is continuous deployment. In this guide we install ArgoCD using Glasskube and verify access to its web UI. ArgoCD provides GitOps-driven continuous delivery: it continuously monitors Git repositories containing Kubernetes manifests or Helm charts and reconciles the cluster to match the desired state stored in Git.

<Frame>
  <img alt="The image is a diagram depicting a single-node Kubernetes cluster with continuous deployment using Argo CD, showing applications A and B within different namespaces." />
</Frame>

## Why ArgoCD?

ArgoCD is a cluster-scoped GitOps controller that acts as the continuous-deployment engine for Kubernetes. It is designed to:

* Continuously compare cluster state to Git and apply changes automatically.
* Provide a web UI for visualizing and managing applications.
* Support declarative application definitions (manifests, Helm, Kustomize, etc.).

Package characteristics for this installation are summarized below.

| Characteristic | Details                              |
| -------------- | ------------------------------------ |
| Scope          | Cluster-scoped package               |
| Values         | No custom value definitions required |
| Entry point    | Web UI (ArgoCD dashboard)            |
| Dependencies   | None                                 |

<Frame>
  <img alt="The image describes a tool for deploying GitOps definitions, highlighting four features: cluster scoped, no value definition, has an entry point, and no dependencies." />
</Frame>

## Install ArgoCD using Glasskube CLI

Use the Glasskube CLI to install ArgoCD into your cluster. The example below demonstrates a typical interactive installation session.

```bash theme={null}
