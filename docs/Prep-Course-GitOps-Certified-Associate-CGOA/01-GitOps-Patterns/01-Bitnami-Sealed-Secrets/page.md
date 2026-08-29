# Bitnami Sealed Secrets

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Patterns/Bitnami-Sealed-Secrets/page

Explains using Bitnami Sealed Secrets and kubeseal to encrypt Kubernetes Secrets for safe GitOps storage and automated cluster decryption via a controller holding a private key.

In this lesson we examine how Bitnami Sealed Secrets enables secure, GitOps-friendly management of Kubernetes Secrets.

Kubernetes Secrets can be created with `kubectl` or a YAML manifest. A core GitOps principle is that every resource—including Secrets—should be stored declaratively in Git. That raises a key question: how do you keep sensitive (often Base64-encoded) data safe in a Git repository (public or private)?

There are multiple approaches (HashiCorp Vault, SOPS, Bitnami Sealed Secrets, etc.). This article focuses on Bitnami Sealed Secrets and explains how to create, store, and deploy encrypted Secret manifests that only the target cluster can decrypt.

## Overview

* The Bitnami Sealed Secrets controller is a Kubernetes controller installed into your cluster.
* The `kubeseal` client transforms a standard Kubernetes Secret manifest into a SealedSecret object that is safe to commit to Git because the secret data is encrypted.
* The controller running in the target cluster holds the private key and decrypts SealedSecret objects back into native Kubernetes Secrets.
* Only the controller (or anyone with access to its private key) can decrypt a SealedSecret. Even the author who created the SealedSecret cannot recover plaintext without the controller’s private key.
* You can install the controller with Helm, Kustomize, or via GitOps tools such as ArgoCD. The examples below show both Helm/GitOps options.

## How sealing and unsealing works

* On the client side you use the `kubeseal` utility to convert a native Secret YAML into a SealedSecret YAML.
* `kubeseal` uses asymmetric cryptography: the Sealed Secrets controller in the cluster holds the private key and `kubeseal` uses the controller’s public certificate to encrypt the Secret so that only the controller can decrypt it.
* By default `kubeseal` fetches the controller’s public certificate automatically over the Kubernetes API. You can also provide the certificate locally with `--cert` (useful when the cluster API is not reachable or for reproducible encryption).

## Quick reference: common commands

| Step                                     | Command / Example                                                                                                                                                                                              | Purpose                                                                           |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Create a local Secret manifest (dry-run) | `kubectl create secret generic mysql-password --from-literal=password='s1DdH@rtf' --dry-run=client -o yaml > mysql-password_k8s-secret.yaml`                                                                   | Export a standard Secret to YAML without applying it to the cluster.              |
| Create ArgoCD app (example)              | `argocd app create sealed-secrets \  --repo https://bitnami-labs.github.io/sealed-secrets \  --helm-chart sealed-secrets \  --revision 2.2.0 \  --dest-namespace kube-system \  --dest-server https://1.2.3.4` | Example: use ArgoCD to install the Sealed Secrets Helm chart into a cluster.      |
| Install kubeseal client                  | `wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/kubeseal-0.18.0-linux-amd64 -O kubeseal && \  sudo install -m 755 kubeseal /usr/local/bin/kubeseal`                             | Download and install the `kubeseal` binary locally.                               |
| Create SealedSecret YAML                 | `kubeseal -o yaml --scope cluster-wide --cert sealedSecret.crt < mysql-password_k8s-secret.yaml > mysql-password_sealed-secret.yaml`                                                                           | Encrypt the Secret YAML to produce a SealedSecret suitable for committing to Git. |

## Example workflow and commands (detailed)

1. Create a Kubernetes Secret manifest locally (dry-run) and export it to YAML:

```bash theme={null}
kubectl create secret generic mysql-password --from-literal=password='s1DdH@rtf' --dry-run=client -o yaml > mysql-password_k8s-secret.yaml
```

2. (Optional) Create an ArgoCD application to deploy the Sealed Secrets Helm chart into your cluster (example):

```bash theme={null}
argocd app create sealed-secrets \
  --repo https://bitnami-labs.github.io/sealed-secrets \
  --helm-chart sealed-secrets \
  --revision 2.2.0 \
  --dest-namespace kube-system \
  --dest-server https://1.2.3.4
