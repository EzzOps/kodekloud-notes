# -> (no keys found)
```

Import the administrator’s public key:

```bash theme={null}
gpg --import infrastructure/SOPS/dev-us-e1-k8s.pub
```

Validate the import and note the fingerprint (e.g., `CE284BB236654E42A`):

```bash theme={null}
gpg --list-public-keys
# gpg: key CE284BB236654E42: public key "dev.us.e1.k8s (k8s) <admin@bb.com>" imported
```

<Callout icon="lightbulb">
  You will use the PGP fingerprint with the `sops` CLI to encrypt your secret.
</Callout>

***

## 3. Install SOPS

Install the SOPS binary if it’s not already present:

```bash theme={null}
cd ~
wget https://github.com/mozilla/sops/releases/download/v3.7.3/sops-v3.7.3.linux.amd64
chmod +x sops-v3.7.3.linux.amd64
sudo mv sops-v3.7.3.linux.amd64 /usr/local/bin/sops
```

Confirm the installation:

```bash theme={null}
sops --version
# sops version 3.7.3
```

***

## 4. Encrypt the Secret with SOPS

Navigate to the directory containing your plaintext secret:

```bash theme={null}
cd bb-app-source/database
cat secret-mysql.yaml
```

Encrypt only the `data` and `stringData` sections in place:

```bash theme={null}
sops --encrypt \
  --encrypted-regex="^(data|stringData)$" \
  --pgp CE284BB236654E42A \
  --in-place secret-mysql.yaml
```

After encryption, `secret-mysql.yaml` will include an `sops:` block:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: secret-mysql
  namespace: database
stringData:
  password: ENC[AES256_GCM,data:...,iv:...]
sops:
  pgp:
    created_at: "2023-04-06T18:35:26Z"
    enc: |
      -----BEGIN PGP MESSAGE-----
      hQGMAxQRIka4bFJ8AQv/...
      -----END PGP MESSAGE-----
  mac: ENC[AES256_GCM,data:...]
  lastmodified: "2023-04-06T18:35:29Z"
```

### Encryption Backends Supported by SOPS

| Backend         | Description                                     |
| --------------- | ----------------------------------------------- |
| PGP             | Public-key encryption via GnuPG / GPG           |
| AWS KMS         | Key management using AWS Key Management Service |
| GCP KMS         | Google Cloud Key Management Service integration |
| Azure Key Vault | Microsoft Azure Key Vault integration           |
| HashiCorp Vault | Vault secret engine encryption                  |

***

## 5. Commit and Push

Add the encrypted secret to your Git repository and push:

```bash theme={null}
git add database/secret-mysql.yaml
git commit -m "chore: encrypt secret-mysql.yaml with SOPS"
git push origin infrastructure
```

***

## 6. Configure FluxCD Decryption

FluxCD needs the private key stored in a Kubernetes `Secret` (e.g., `sops-gpg`) and decryption enabled in the `Kustomization` manifest.

Edit `infrastructure/flux/kustomization-database.yaml`:

```yaml theme={null}
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: infra-database-mysql
  namespace: flux-system
spec:
  interval: 10s
  path: "./database"
  prune: true
  sourceRef:
    kind: GitRepository
    name: infra-source-git
  targetNamespace: database
  decryption:
    provider: sops
    secretRef:
      name: sops-gpg
```

Commit and push the FluxCD configuration:

```bash theme={null}
git add infrastructure/flux/kustomization-database.yaml
git commit -m "feat: enable SOPS decryption in Flux Kustomization"
git push origin infrastructure
```

For details, see [FluxCD Kustomization Documentation](https://fluxcd.io[AWS_SECRET_ACCESS_KEY]/).

***

## 7. Verify Decrypted Secret in Cluster

Trigger reconciliation and inspect the applied secret:

```bash theme={null}
flux reconcile source git flux-system
flux reconcile kustomization infra-database-mysql

kubectl -n database get secret secret-mysql -o json \
  | jq -r .data.password | base64 -d
# => mysql-password-0123456789
```

You should see the original plaintext password, confirming that FluxCD decrypted the secret before applying it.

***

## Links and References

* [Mozilla SOPS Releases](https://github.com/mozilla/sops/releases)
* [GnuPG (GPG) Documentation](https://gnupg.org/documentation/)
* [FluxCD Kustomization Docs](https://fluxcd.io[AWS_SECRET_ACCESS_KEY]/)
* [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/c8ad2608-2804-4413-9041-5e8dc9126d53/lesson/6f504936-daab-4ee3-8063-793bc83a9329" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/c8ad2608-2804-4413-9041-5e8dc9126d53/lesson/9ae09784-a5ae-481c-a4f1-cf7d338e2713" />
</CardGroup>


# DEMO Setup Bitnami Sealed

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Secret-Management-Sign-Verification/DEMO-Setup-Bitnami-Sealed/page

This guide explains deploying Bitnami Sealed Secrets with Flux CD and sealing Kubernetes Secrets for secure Git storage.

In this guide, you’ll deploy the Bitnami Sealed Secrets controller using Flux CD and learn how to seal Kubernetes Secrets for safe Git storage. Follow the steps below to get started.

## Prerequisites

* A running Kubernetes cluster and configured `kubectl` context
* Flux v2 installed ([Flux CLI Install](https://fluxcd.io/docs/installation/))
* A Git repository (e.g., `bb-app-source-git`) with an `infrastructure` branch

***

## 1. Switch to the `infrastructure` branch

<Callout icon="lightbulb">
  Always ensure your working directory is clean before switching branches.
</Callout>

```bash theme={null}
cd bb-app-source-git
git checkout infrastructure
```

Expected output:

```text theme={null}
Switched to branch 'infrastructure'
Your branch is up to date with 'origin/infrastructure'.
```

***

## 2. Define the Helm repository

Create a `HelmRepository` manifest under the `bitnami-sealed-secrets` directory to let Flux pull the Sealed Secrets charts.

```yaml theme={null}
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: HelmRepository
metadata:
  name: sealed-secrets
  namespace: flux-system
spec:
  interval: 24h
  url: https://bitnami-labs.github.io/sealed-secrets
```

Commit and push:

```bash theme={null}
git add bitnami-sealed-secrets/helmrepository.yaml
git commit -m "Add Bitnami Sealed Secrets HelmRepository"
git push
```

***

## 3. Create a Flux Kustomization

In your Flux cluster repo (for example, `block-buster/flux-clusters/dev-cluster`), scaffold a Kustomization that points to the Sealed Secrets path.

```bash theme={null}
cd ~/block-buster/flux-clusters/dev-cluster
flux create kustomization sealed-secrets \
  --source GitRepository/infra-source-git \
  --path "./bitnami-sealed-secrets" \
  --prune=true \
  --interval=1h \
  --export > sealed-secrets-kustomization.yaml
```

Commit and reconcile:

```bash theme={null}
git add sealed-secrets-kustomization.yaml
git commit -m "Add Sealed Secrets Kustomization"
git push

flux reconcile source git infra-source-git
flux reconcile kustomization sealed-secrets
```

***

## 4. Verify the Sealed Secrets controller

The controller is deployed in the `kube-system` namespace. Run:

```bash theme={null}
kubectl -n kube-system get all
```

You should see:

| Resource                                  | READY | STATUS  | AGE |
| ----------------------------------------- | ----- | ------- | --- |
| pod/sealed-secrets-controller-xxxxx       | 1/1   | Running | 30s |
| service/sealed-secrets-controller         | —     | —       | 30s |
| deployment.apps/sealed-secrets-controller | 1/1   | Running | 30s |
| replicaset.apps/sealed-secrets-controller | 1     | 1       | 30s |

A TLS Secret (`kubernetes.io/tls`) containing the controller’s key pair is also created in `kube-system`.

***

## 5. Install the `kubeseal` CLI

Download and install the latest `kubeseal` binary:

```bash theme={null}
VERSION="v0.19.5"
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/${VERSION}/kubeseal-${VERSION}-linux-amd64.tar.gz
tar -xzf kubeseal-${VERSION}-linux-amd64.tar.gz
sudo mv kubeseal /usr/local/bin/
```

Validate installation:

```bash theme={null}
kubeseal --version
```

Expected:

```text theme={null}
kubeseal version: 0.19.5
```

***

## 6. Fetch the Sealed Secrets public certificate

You need the controller’s public key to seal secrets locally:

```bash theme={null}
kubeseal \
  --fetch-cert \
  --controller-name sealed-secrets-controller \
  --controller-namespace kube-system \
  > sealed-secrets.pub
```

This outputs `sealed-secrets.pub`, which you will use to encrypt your Kubernetes Secrets.

***

## 7. Seal and commit Kubernetes Secrets

1. Create a plain Secret manifest (`secret.yaml`).

2. Run:

   ```bash theme={null}
   kubeseal \
     --cert sealed-secrets.pub \
     < secret.yaml \
     > sealed-secret.yaml
   ```

3. Review, commit, and push `sealed-secret.yaml` to your Git repo. Flux will apply it automatically.

***

## Links and References

* [Sealed Secrets Repository](https://github.com/bitnami-labs/sealed-secrets)
* [Flux CD Documentation](https://fluxcd.io/docs/)
* [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/c8ad2608-2804-4413-9041-5e8dc9126d53/lesson/254cf972-bcf8-421d-81ec-9434f6d441fc" />
</CardGroup>
