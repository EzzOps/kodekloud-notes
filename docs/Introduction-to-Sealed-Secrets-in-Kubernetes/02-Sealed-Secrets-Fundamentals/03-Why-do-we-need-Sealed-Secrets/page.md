# Why do we need Sealed Secrets

Source: https://notes.kodekloud.com/docs/Introduction-to-Sealed-Secrets-in-Kubernetes/Sealed-Secrets-Fundamentals/Why-do-we-need-Sealed-Secrets/page

This article explains the importance of Sealed Secrets in Kubernetes for securely managing sensitive information in GitOps workflows.

Before exploring how Sealed Secrets work, let’s examine the gap they fill in a GitOps-based Kubernetes workflow.

## The risk of plain Kubernetes Secrets in Git

In a GitOps pipeline, you typically declare your resources—including Secrets—as YAML manifests and commit them to your repository. Kubernetes offers two methods to create a Secret:

* **Imperative**:
  ```bash theme={null}
  kubectl create secret generic database --from-literal=DB_PASSWORD=password123
  ```
* **Declarative** (preferred in GitOps):
  ```yaml theme={null}
  apiVersion: v1
  kind: Secret
  metadata:
    name: database
    namespace: default
  data:
    DB_PASSWORD: cGFzc3dvcmQxMjM=
  ```

When you apply the declarative manifest, Kubernetes Base64-encodes your password (`password123` → `cGFzc3dvcmQxMjM=`).

> **lightbulb** Base64 encoding is **not** encryption. Anyone with read access to your cluster or Git repo can decode the value back to cleartext.

```bash theme={null}
echo cGFzc3dvcmQxMjM= | base64 --decode
