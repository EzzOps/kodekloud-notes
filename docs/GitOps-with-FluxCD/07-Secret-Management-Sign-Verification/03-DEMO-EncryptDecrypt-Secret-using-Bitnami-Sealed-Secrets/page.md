# Enter your GHCR token when prompted
```

> **lightbulb** Ensure your token has at least `read:packages` and `write:packages` scopes to push and pull images.

***

## 3. Push the OCI Artifact with Flux

Package your manifests folder and push it as an OCI artifact:

```bash theme={null}
flux push artifact \
  oci://ghcr.io/sidd-harth-2/bb-app:7.10.0-$(git rev-parse --short HEAD) \
  --path="./manifests" \
  --source="$(git config --get remote.origin.url)" \
  --revision="7.10.0/$(git rev-parse --short HEAD)"
```

Expected output:

```plaintext theme={null}
pushing artifact to ghcr.io/sidd-harth-2/bb-app:7.10.0-d6c285f
artifact successfully pushed to ghcr.io/sidd-harth-2/bb-app:7.10.0-d6c285f@sha256:eda014...
```

Verify the new package under **Packages → bb-app** on GitHub.

***

## 4. Sign the Artifact with Cosign

1. Pull the image by tag:

   ```bash theme={null}
   docker pull ghcr.io/sidd-harth-2/bb-app:7.10.0-d6c285f
   ```

2. Sign by digest:

   ```bash theme={null}
   cosign sign \
     --key ../cosign/cosign.key \
     ghcr.io/sidd-harth-2/bb-app@sha256:eda014...
   ```

Approve uploading to the transparency log when prompted. A `.sig` blob is now attached to your OCI package.

***

## 5. Verify the Signature Locally

Use your public key to confirm the artifact’s integrity:

```bash theme={null}
cosign verify \
  --key ../cosign/cosign.pub \
  ghcr.io/sidd-harth-2/bb-app@sha256:eda014...
```

You should see:

```plaintext theme={null}
Verification for ghcr.io/sidd-harth-2/bb-app@sha256:eda014...
  - The cosign claims were validated
  - Evidence of claims in the transparency log was verified offline
  - The signatures were verified against the specified public key
```

***

## 6. Configure Flux to Pull and Verify

1. Change to your Flux cluster repo:

   ```bash theme={null}
   cd ~/block-buster/flux-clusters/dev-cluster
   ```

2. Create an `OCIRepository` source for GHCR:

   ```bash theme={null}
   flux create source oci 10-demo-source-oci-bb-app \
     --url oci://ghcr.io/sidd-harth-2/bb-app \
     --tag 7.10.0-d6c285f \
     --secret-ref ghcr-auth \
     --provider generic \
     --export > 10-demo-source-oci-bb-app.yaml
   ```

3. Edit **10-demo-source-oci-bb-app.yaml** to include Cosign verification:

   ```yaml theme={null}
   apiVersion: source.toolkit.fluxcd.io/v1beta2
   kind: OCIRepository
   metadata:
     name: 10-demo-source-oci-bb-app
     namespace: flux-system
   spec:
     interval: 1m0s
     provider: generic
     url: oci://ghcr.io/sidd-harth-2/bb-app
     ref:
       tag: 7.10.0-d6c285f
     secretRef:
       name: ghcr-auth
     verify:
       provider: cosign
       secretRef:
         name: cosign-pub
   ```

4. Apply the source:

   ```bash theme={null}
   kubectl apply -f 10-demo-source-oci-bb-app.yaml
   ```

5. Ensure secrets exist:

   ```bash theme={null}
   kubectl -n flux-system get secret ghcr-auth cosign-pub
   ```

6. Create and apply a `Kustomization` to deploy the manifests:

   ```bash theme={null}
   flux create kustomization 10-demo-kustomize-oci-bb-app \
     --source=OCIRepository/10-demo-source-oci-bb-app \
     --target-namespace=10-demo \
     --path="./" \
     --prune=false \
     --interval=10s \
     --export > 10-demo-kustomize-oci-bb-app.yaml

   kubectl apply -f 10-demo-kustomize-oci-bb-app.yaml
   ```

***

## 7. Confirm Verification and Deployment

1. Reconcile and check the OCI source status:

   ```bash theme={null}
   flux reconcile source oci -n flux-system 10-demo-source-oci-bb-app
   flux get sources oci -n flux-system
   ```

   You should see `READY True`.

2. Inspect the `SourceVerified` condition:

   ```bash theme={null}
   kubectl -n flux-system get ocirepository 10-demo-source-oci-bb-app -o yaml
   ```

3. Verify deployment in the `10-demo` namespace:

   ```bash theme={null}
   kubectl -n 10-demo get all
   ```

4. Access the application on its NodePort (e.g., `localhost:30010`). You should see version **7.10.0** of Block Buster:

![The image shows a "Block Buster" game interface with colorful blocks, a paddle, and a ball, set against a starry background. Game details like pod name, IP, and version are displayed at the top.](https://kodekloud.com/kk-media/image/upload/v1752877687/notes-assets/images/GitOps-with-FluxCD-DEMO-Cosign-OCI-Artifacts/block-buster-game-interface-stars.jpg)

***

## Links and References

* [Cosign by Sigstore](https://github.com/sigstore/cosign)
* [Flux CD Documentation](https://fluxcd.io/docs/)
* [GitHub Container Registry](https://ghcr.io/)
* [OCI Artifacts Spec](https://github.com/opencontainers/artifacts)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/c8ad2608-2804-4413-9041-5e8dc9126d53/lesson/3db54ec2-a57f-479e-9fcd-f4ca0717bcce)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/c8ad2608-2804-4413-9041-5e8dc9126d53/lesson/909af89e-e23d-4fdb-ab12-99e20cf7d386)


# DEMO EncryptDecrypt Secret using Bitnami Sealed Secrets

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Secret-Management-Sign-Verification/DEMO-EncryptDecrypt-Secret-using-Bitnami-Sealed-Secrets/page

This guide explains how to secure Kubernetes Secrets using Bitnami Sealed Secrets with FluxCD and Kustomize for declarative management.

In this guide, we’ll cover how to secure Kubernetes Secrets by encrypting them with [Bitnami Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) and manage them declaratively using FluxCD and Kustomize.

## Table of Contents

| Step                        | Description                                | Reference Command                   |
| --------------------------- | ------------------------------------------ | ----------------------------------- |
| 1. Background               | Plaintext Secret in Git                    | –                                   |
| 2. Automatic Reconciliation | FluxCD constantly applies Git manifests    | `kubectl -n database get po,secret` |
| 3. Suspend Reconciliation   | Pause FluxCD Kustomization                 | `flux suspend kustomization …`      |
| 4. Trigger Pod Failure      | Restart Pod to observe missing Secret      | `kubectl rollout restart …`         |
| 5. Encrypt with kubeseal    | Generate a `SealedSecret`                  | `kubeseal --cert …`                 |
| 6. Replace Plaintext        | Commit encrypted manifest to Git           | `git add sealed-secret-mysql.yaml`  |
| 7. Resume Reconciliation    | Apply updated Git source and resume FluxCD | `flux resume kustomization …`       |
| 8. Verify Decryption        | Confirm the decrypted Secret in cluster    | `kubectl get secret …`              |

***

## 1. Background: Plaintext Secret in Git

We have a FluxCD `Kustomization` that applies manifests from a Git repository:

```yaml theme={null}
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: infra-database-kustomize-git-mysql
  namespace: flux-system
spec:
  interval: 10s
  path: ./database
  prune: true
  sourceRef:
    kind: GitRepository
    name: infra-source-git
  targetNamespace: database
```

Under `./database/secret-mysql.yaml`, the MySQL password is stored in plaintext:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: secret-mysql
  namespace: database
stringData:
  password: mysql-password-0123456789
```

> **triangle-alert** Storing passwords or tokens in plaintext within Git exposes them to unauthorized access. Always encrypt sensitive data before committing.

FluxCD’s Kustomize controller reconciles this Secret every 10 seconds, ensuring it’s present in the cluster.

***

## 2. Demonstrate Automatic Reconciliation

Verify the Secret and Pod exist:

```bash theme={null}
kubectl -n database get pods,secret
```

Delete the Secret to see automatic re-creation:

```bash theme={null}
kubectl -n database delete secret secret-mysql
