# Create the argocd namespace and apply the cluster-scoped manifest
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Or install via Helm (defaults to non-HA):

```bash theme={null}
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm install my-argo-cd argo/argo-cd --version 4.8.0
```

Notes about Helm:

* To enable HA with the Helm chart, override the relevant values (replica counts, resource requests/limits, and storage) either via a values file or `--set` flags.
* For chart-specific configuration and HA options, see the chart documentation: [https://github.com/argoproj/argo-helm](https://github.com/argoproj/argo-helm)

Install the argocd CLI
After Argo CD is installed, install the argocd CLI to interact with the Argo CD API server.

Linux amd64 example:

```bash theme={null}
# Download the argocd client binary
curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
chmod +x /usr/local/bin/argocd

# Verify installation
argocd version
```

If you are on a different OS or architecture, download the appropriate release binary from the Argo CD releases page and place it in a directory on your PATH:

* Argo CD Releases: [https://github.com/argoproj/argo-cd/releases](https://github.com/argoproj/argo-cd/releases)

Useful links and references

* Official Argo CD documentation: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Argo CD GitHub repository (manifests): [https://github.com/argoproj/argo-cd](https://github.com/argoproj/argo-cd)
* Argo Helm charts: [https://github.com/argoproj/argo-helm](https://github.com/argoproj/argo-helm)

Quick decision guide

* Labs / POCs: use non-HA manifests (install.yaml or namespace-install.yaml).
* Production: use HA manifests or configure HA via Helm; make sure to provision multiple replicas, persistent storage, and appropriate RBAC/permissions.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/a98a2a50-e1ce-474f-860a-86ef35a41e2d" />
</CardGroup>


# Multi Cluster Application Deployment

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Multi-Cluster-Application-Deployment/page

Guide for registering external Kubernetes clusters with Argo CD to enable GitOps multi-cluster application deployments, RBAC setup, and credential storage.

Learn how Argo CD can manage applications across multiple Kubernetes clusters — not just the cluster where Argo CD itself runs. This guide shows the recommended sequence: prepare your kubeconfig, register the external cluster with Argo CD, and verify that the cluster is available as a deployment destination.

Argo CD supports multi-cluster deployments by storing external cluster credentials in its own namespace and using a dedicated service account on each external cluster to apply manifests.

<Frame>
  <img alt="A slide titled &#x22;Multi-Cluster Deployment&#x22; showing a controller pulling manifests from a GitHub repository and deploying them to dev and prod Kubernetes clusters. The diagram uses icons for GitHub, a squid-like operator inside a dashed box, and Kubernetes cluster symbols with arrows labeled &#x22;deploy.&#x22;" />
</Frame>

## Overview — steps to add an external cluster

1. Add the external cluster details (server, certificates, user credentials, context) to your local kubeconfig.
2. Use the argocd CLI to register that kubeconfig context with Argo CD (`argocd cluster add`).
3. Confirm Argo CD created the required ServiceAccount, ClusterRole, and ClusterRoleBinding on the target cluster.
4. Verify the cluster appears in Argo CD’s cluster list and inspect the stored secret if needed.

<Callout icon="lightbulb">
  Before running the commands below, ensure you have access to the target cluster API endpoint and appropriate client certificates or tokens. You can also use cloud provider IAM auth (e.g., EKS, GKE) depending on your environment.
</Callout>

## Example commands

Add the cluster server, user credentials, and context into kubeconfig:

```bash theme={null}
$ kubectl config set-cluster prod --server=https://1.2.3.4 --certificate-authority=prod.crt
Cluster "prod" set.

$ kubectl config set-credentials admin --client-certificate=admin.crt --client-key=admin.key
User "admin" set.

$ kubectl config set-context admin-prod --cluster=prod --user=admin --namespace=prod-app
Context "admin-prod" set.
```

Register the context with Argo CD (this will create a service account and RBAC bindings on the external cluster):

```bash theme={null}
$ argocd cluster add admin-prod

WARNING: This will create a service account `argocd-manager` on the cluster referenced by context `admin-prod` with full cluster level admin privileges. Do you want to continue [y/N]? y

INFO[0011] ServiceAccount "argocd-manager" created in namespace "kube-system"
INFO[0011] ClusterRole "argocd-manager-role" created
INFO[0011] ClusterRoleBinding "argocd-manager-role-binding" created
Cluster 'https://1.2.3.4' added
```

Check the clusters that Argo CD knows about:

```bash theme={null}
$ argocd cluster list

SERVER                         NAME         VERSION   STATUS      MESSAGE   PROJECT
https://1.2.3.4               admin-prod   1.21      Successful
https://kubernetes.default.svc in-cluster   1.20      Successful
```

Argo CD stores the cluster credentials as Kubernetes Secrets in the argocd namespace. You can inspect a secret like this:

```Expected Output: theme={null}
bash
$ kubectl describe secret cluster-1.2.3.4-1827028835 -n argocd

....Data
config: 3017 bytes    # user token/cert
name: 54 bytes        # context name
server: 21 bytes      # server url
```

<Callout icon="warning">
  When you run `argocd cluster add`, Argo CD will create an `argocd-manager` ServiceAccount with cluster-admin level permissions by default. Limit access and scope where possible — for production, prefer restricting RBAC to the minimum required privileges.
</Callout>

## Quick reference — commands and purpose

| Command                                    | Purpose                                      | Notes                                                                     |
| ------------------------------------------ | -------------------------------------------- | ------------------------------------------------------------------------- |
| `kubectl config set-cluster`               | Add cluster endpoint & CA to kubeconfig      | Provide the API server URL and CA cert                                    |
| `kubectl config set-credentials`           | Add user credentials (cert/key or token)     | Use client certs or bearer token                                          |
| `kubectl config set-context`               | Create a kubeconfig context for the cluster  | Include namespace if you want a default namespace                         |
| `argocd cluster add <context>`             | Register the kubeconfig context with Argo CD | Creates ServiceAccount, ClusterRole, ClusterRoleBinding on target cluster |
| `argocd cluster list`                      | List clusters registered in Argo CD          | Shows status and server URL                                               |
| `kubectl describe secret <name> -n argocd` | Inspect stored cluster credentials           | Secrets store the kubeconfig/config data                                  |

## Verification and troubleshooting

* Use `argocd cluster list` to confirm the cluster status shows Successful.
* If a cluster shows errors, check the target cluster’s kube-apiserver reachability, certificate validity, and whether the created ServiceAccount/RBAC objects exist in the target cluster’s `kube-system` namespace.
* Inspect Argo CD logs for errors: `kubectl -n argocd logs deploy/argocd-server` or check the repo-server and application-controller logs for sync problems.

## Links and references

* [Argo CD documentation — multi-cluster setup](https://argo-cd.readthedocs.io/en/stable/)
* [Kubernetes kubeconfig documentation](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
* [kubectl config command reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#config)
* [Kubernetes ServiceAccount concept](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)
* [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

This workflow lets Argo CD act as a single control plane for application deployment across multiple Kubernetes clusters, enabling consistent GitOps-driven rollouts to dev, staging, and production clusters.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/e7ab6911-8176-42a9-ac35-3a90cea16f0e" />
</CardGroup>
