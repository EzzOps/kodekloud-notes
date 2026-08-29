# Demo Manifest Repository and Configure ArgoCD

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Kubernetes-and-GitOps/Demo-Manifest-Repository-and-Configure-ArgoCD/page

This guide covers cloning a Kubernetes manifest repository, creating encrypted MongoDB credentials, and deploying an application using Argo CD in a GitOps workflow.

In this guide, you’ll learn how to:

1. Clone and migrate a Kubernetes manifest repository.
2. Create and encrypt MongoDB credentials with Bitnami Sealed Secrets.
3. Deploy a Solar System application using Argo CD in a secure GitOps workflow.

***

## 1. Clone the Manifest Repository

Start by cloning the repository that holds your Kubernetes manifests:

```bash theme={null}
git clone https://github.com/username/manifest-repo.git
cd manifest-repo
ls kubernetes
