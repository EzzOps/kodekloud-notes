# 1. Add the Bitnami Sealed-Secrets Helm repository
flux create source helm sealed-secrets \
  --interval 1h \
  --url https://bitnami-labs.github.io/sealed-secrets

# 2. Create a HelmRelease for the controller
flux create helmrelease sealed-secrets-controller \
  --interval 1h \
  --release-name sealed-secrets-controller \
  --target-namespace kube-system \
  --source HelmRepository/sealed-secrets \
  --chart sealed-secrets \
  --chart-version ">=1.15.0-0" \
  --crds CreateReplace
```

Flux will pull the chart and install the Sealed Secrets controller into the `kube-system` namespace.

## 5. Encrypting a Secret with kubeseal

Follow these steps to seal your plain Secret:

1. **Generate the plain Secret manifest** (if not already done):

   ```bash theme={null}
   kubectl create secret generic mysql-password \
     --from-literal=password=s1Ddh@rt* \
     --dry-run=client -o yaml > mysql_k8s-secret.yaml
   ```

2. **Install the `kubeseal` client**:

   ```bash theme={null}
   wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/kubeseal-0.18.0-linux-amd64.tar.gz
   tar -zxvf kubeseal-0.18.0-linux-amd64.tar.gz
   mv kubeseal /usr/local/bin/
   ```

3. **Fetch the public certificate** from the controller:

   ```bash theme={null}
   kubeseal \
     --fetch-cert \
     --controller-name sealed-secrets-controller \
     --controller-namespace kube-system \
     > sealed-secrets.crt
   ```

4. **Seal the Secret**:

   ```bash theme={null}
   kubeseal \
     --cert sealed-secrets.crt \
     --scope cluster-wide \
     -o yaml < mysql_k8s-secret.yaml \
     > mysql-password_sealedsecret.yaml
   ```

> **lightbulb** The `--scope cluster-wide` flag allows decryption in any namespace. Omit or change the scope for namespace-restricted secrets.

## 6. Example Manifests

### 6.1 Original Kubernetes Secret

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: mysql-password
type: Opaque
data:
  password: czFEZhAcnQj
```

### 6.2 Resulting SealedSecret

```yaml theme={null}
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: mysql-password
  annotations:
    sealedsecrets.bitnami.com/cluster-wide: "true"
spec:
  encryptedData:
    password: AgBgdDPGdf3ngr7k3tA/Cg0B2UQd1wT390cVDs=
  template:
    metadata:
      name: mysql-password
      annotations:
        sealedsecrets.bitnami.com/cluster-wide: "true"
    data: {}
```

## 7. Applying the SealedSecret with Flux

1. Commit `mysql-password_sealedsecret.yaml` to your Git repo.
2. Flux syncs and applies the SealedSecret resource.
3. The Sealed Secrets controller in the cluster decrypts it and creates a standard Kubernetes Secret.
4. Your workloads can reference the decrypted Secret just like any other.

## 8. Summary

By integrating Bitnami Sealed Secrets with Flux, you get:

* **Encrypted Secret manifests** stored safely in Git.
* **Automated HelmRelease** deployment of the Sealed Secrets controller.
* **CLI-driven** encryption (`kubeseal`) and in-cluster decryption.
* A fully **GitOps-friendly** secret management workflow for Kubernetes.

***

## Links and References

* [Bitnami Sealed Secrets GitHub](https://github.com/bitnami-labs/sealed-secrets)
* [Flux CD Documentation](https://fluxcd.io/docs/)
* [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
* [GitOps Principles](https://www.gitops.tech/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/c8ad2608-2804-4413-9041-5e8dc9126d53/lesson/2a2558ff-c80f-4e96-978e-c899854f1f55)


# Cosign OCI Artifacts

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Secret-Management-Sign-Verification/Cosign-OCI-Artifacts/page

Learn to sign and verify OCI artifacts using Cosign and Flux in this comprehensive guide.

In this guide, you’ll learn how to sign and verify OCI artifacts using [SigStore](https://sigstore.dev)’s [Cosign](https://github.com/sigstore/cosign) alongside [Flux](https://fluxcd.io). By the end, you’ll be able to:

1. Package Kubernetes manifests into an OCI artifact
2. Sign the artifact with Cosign
3. Configure Flux to verify signatures on pull

> **lightbulb** * Flux v0.35+ installed and configured
  * `docker` and `kubectl` CLI tools available
  * Access to a container registry (e.g., GitHub Container Registry)

***

## 1. Package and Push Manifests as an OCI Artifact

Assume your repository has Nginx manifests structured like this:

```text theme={null}
nginx/
└── manifests/
    ├── deployment.yaml
    └── service.yaml
```

Authenticate with your registry and push:

```bash theme={null}
docker login ghcr.io \
  --username sid \
  --password <GitHub-Personal-Access-Token>

flux push artifact oci://ghcr.io/sid/nginx:7.7.0-1a2b3c4d \
  --path="./nginx/manifests" \
  --source="$(git config --get remote.origin.url)" \
  --revision="7.7.0-1a2b3c4d"
```

Expected output:

```text theme={null}
✔ pushing to ghcr.io/sid/nginx:7.7.0-1a2b3c4d
✔ artifact successfully pushed to ghcr.io/sid/nginx@sha256:235b486df438f015861f86dfa386d4fa
```

***

## 2. Install Cosign and Generate a Key Pair

Download the latest Cosign release and make it executable:

```bash theme={null}
wget https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64 \
  -O /usr/local/bin/cosign \
  && chmod +x /usr/local/bin/cosign
```

Generate your key pair:

```bash theme={null}
cosign generate-key-pair
```

You’ll be prompted to create a passphrase:

```text theme={null}
Enter password for private key: ********
Enter password for private key again: ********
Private key written to cosign.key
Public key written to cosign.pub
```

> **triangle-alert** Store your `cosign.key` in a secure vault. Loss or compromise of the private key may allow unauthorized signatures.

***

## 3. Sign the OCI Artifact

Use your private key to sign the pushed artifact:

```bash theme={null}
cosign sign \
  --key cosign.key \
  ghcr.io/sid/nginx:7.7.0-1a2b3c4d
```

Provide the passphrase when prompted. Cosign uploads the signature alongside the image.

***

## 4. Verify the Artifact Manually

Confirm the signature before deploying:

```bash theme={null}
cosign verify \
  --key cosign.pub \
  ghcr.io/sid/nginx:7.7.0-1a2b3c4d
```

You should see:

```text theme={null}
Verification for ghcr.io/sid/nginx:7.7.0-1a2b3c4d --
✔ Signature validated
✔ Certificate validated
```

***

## 5. Store the Public Key in Kubernetes

Flux verifies signatures by reading your public key from a Kubernetes Secret:

```bash theme={null}
kubectl -n flux-system create secret generic cosign-pub \
  --from-file=cosign.pub=cosign.pub
```

***

## 6. Configure Flux to Verify OCI Artifacts

Create an `OCIRepository` resource that enforces signature verification:

```yaml theme={null}
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: OCIRepository
metadata:
  name: demo-source-oci
  namespace: flux-system
spec:
  interval: 1m0s
  provider: generic
  url: oci://ghcr.io/sid/nginx
  ref:
    tag: 7.7.0-1a2b3c4d
  secretRef:
    name: ghcr-auth
  verify:
    provider: cosign
    secretRef:
      name: cosign-pub
```

When Flux pulls this artifact, it will:

* Fetch the OCI layer
* Verify the signature against the supplied public key
* Abort on failure or extract the tarball on success

***

## 7. Inspect the Verification Status

Check the status of your OCIRepository:

```bash theme={null}
kubectl -n flux-system get ocirepositories demo-source-oci -o yaml
```

Relevant status snippet:

```yaml theme={null}
status:
  conditions:
    - type: SourceVerified
      status: "True"
      reason: Succeeded
      message: verified signature of revision 7.7.0-1a2b3c4d
      lastTransitionTime: "2023-03-03T14:36:10Z"
```

If signature verification fails, Flux will not apply the artifact.

***

## CLI Commands at a Glance

| Command                                    | Description                           |
| ------------------------------------------ | ------------------------------------- |
| `flux push artifact ...`                   | Push manifests as an OCI artifact     |
| `cosign generate-key-pair`                 | Generate a private/public key pair    |
| `cosign sign --key cosign.key ...`         | Sign an OCI artifact                  |
| `cosign verify --key cosign.pub ...`       | Verify a signature on an OCI artifact |
| `kubectl create secret generic cosign-pub` | Store Cosign public key in Kubernetes |

***

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Flux GitHub Repository](https://github.com/fluxcd/flux)
* [SigStore Cosign](https://github.com/sigstore/cosign)
* [GitHub Container Registry](https://ghcr.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/c8ad2608-2804-4413-9041-5e8dc9126d53/lesson/86ab7d9b-31ac-45a0-8511-c0f5898e9744)
