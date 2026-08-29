# Bitnami Sealed Secrets

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Secret-Management-Sign-Verification/Bitnami-Sealed-Secrets/page

This guide explains managing Kubernetes secrets securely using Bitnami Sealed Secrets in a GitOps workflow with Flux.

In this guide, you’ll learn how to manage Kubernetes secrets securely using **Bitnami Sealed Secrets** in a GitOps workflow powered by [Flux](https://fluxcd.io/). By the end, you’ll have encrypted Secret manifests stored safely in Git and automatically decrypted in your cluster.

## 1. Declarative Secret Storage

According to [GitOps](https://www.gitops.tech/) principles, *all* Kubernetes resources—including secrets—should live as code in your Git repository.

### Creating a Standard Secret

```bash theme={null}
kubectl create secret generic mysql-password \
  --from-literal=password=s1Dhd@rt# \
  --dry-run=client -o yaml > mysql_k8s-secret.yaml
```

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: mysql-password
data:
  password: czFEZhAcnQj
```

<Callout icon="triangle-alert">
  Base64 encoding is *not* secure encryption. Never commit raw or Base64‐encoded secrets to Git.
</Callout>

## 2. Secret Management Solutions

Compare popular tools for encrypting Kubernetes secrets in GitOps repositories:

| Tool                                | Description                                   | Repository                                                                                                       |
| ----------------------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Bitnami Sealed Secrets              | Seal/unseal secrets with a controller and CLI | [https://github.com/bitnami-labs/sealed-secrets](https://github.com/bitnami-labs/sealed-secrets)                 |
| HashiCorp Vault                     | Centralized secrets vault with dynamic creds  | [https://www.vaultproject.io/](https://www.vaultproject.io/)                                                     |
| Mozilla SOPS                        | Encrypt YAML/JSON files                       | [https://github.com/mozilla/sops](https://github.com/mozilla/sops)                                               |
| GoDaddy Kubernetes External Secrets | Fetch secrets from external providers         | [https://github.com/godaddy/kubernetes-external-secrets](https://github.com/godaddy/kubernetes-external-secrets) |

In this article, we’ll focus on **Bitnami Sealed Secrets**.

## 3. What Are Bitnami Sealed Secrets?

Bitnami Sealed Secrets provides:

* A **Kubernetes controller** that decrypts sealed secrets inside the cluster.
* A **kubeseal CLI** to encrypt Kubernetes Secret manifests to SealedSecret manifests.
* A safe-to-commit SealedSecret format (even on public repos) that only your controller can decrypt.

## 4. Installing the Sealed Secrets Controller with Flux

Deploy the controller as a HelmRelease in Flux:

```bash theme={null}
