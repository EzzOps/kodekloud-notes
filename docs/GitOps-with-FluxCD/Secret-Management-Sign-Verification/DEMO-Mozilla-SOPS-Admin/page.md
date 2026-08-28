# Download the Cosign binary
wget "https://github.[AWS_SECRET_ACCESS_KEY].0.0/cosign-linux-amd64"

# Move into your PATH and make executable
sudo mv cosign-linux-amd64 /usr/local/bin/cosign
sudo chmod +x /usr/local/bin/cosign
```

### 2. RPM Package

```bash theme={null}
wget "https://github.[AWS_SECRET_ACCESS_KEY].0.0/cosign-2.0.0.x86_64.rpm"
sudo rpm -Uvh cosign-2.0.0.x86_64.rpm
```

### 3. DEB Package

```bash theme={null}
wget "https://github.[AWS_SECRET_ACCESS_KEY].0.0/cosign_2.0.0_amd64.deb"
sudo dpkg -i cosign_2.0.0_amd64.deb
```

## Verify Installation

After installation, check your Cosign version:

```bash theme={null}
root@host:~# cosign version
cosign: A tool for Container Signing, Verification and Storage in an OCI registry.
GitVersion:    v2.0.0
GitCommit:     [AWS_SECRET_ACCESS_KEY]
BuildDate:     2023-02-23T19:26:35Z
GoVersion:     go1.20.1
Compiler:      gc
Platform:      linux/amd64
```

<Callout icon="lightbulb">
  Ensure you install v2.0.0 or later for full compatibility with Flux CD’s image verification features.
</Callout>

## Generate a Cosign Key Pair

Create an asymmetric key pair to sign your OCI artifacts:

```bash theme={null}
root@host:~# cosign generate-key-pair
Enter password for private key:
Enter password for private key again:
Private key written to cosign.key
Public key written to cosign.pub
```

Verify the files:

```bash theme={null}
root@host:~# ls cosign.*
cosign.key  cosign.pub
```

<Callout icon="triangle-alert">
  Keep your private key (`cosign.key`) secure and never commit it to version control. Remember your password—it’s required for signing and verification.
</Callout>

## Configure Flux CD with the Public Key

To enable [Flux CD](https://fluxcd.io) to verify image signatures, store the public key as a Kubernetes Secret in the `flux-system` namespace:

```bash theme={null}
root@host:~# kubectl -n flux-system create secret generic cosign-pub \
  --from-file=cosign.pub=cosign.pub
secret/cosign-pub created
```

Flux will automatically fetch this key and validate any signed OCI artifacts during reconciliation.

## Next Steps

1. Build and push an OCI artifact (e.g., container image).
2. Sign the image using Cosign.
3. Observe Flux CD verifying the signature in your cluster.

## References

* [Sigstore Cosign Documentation](https://github.com/sigstore/cosign)
* [Flux CD Official Site](https://fluxcd.io)
* [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
* [OCI Artifacts Specification](https://github.com/opencontainers/artifacts)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/c8ad2608-2804-4413-9041-5e8dc9126d53/lesson/4ec5c36f-d64b-4e15-bcbb-a4c113d84f49" />
</CardGroup>


# DEMO Mozilla SOPS Admin

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Secret-Management-Sign-Verification/DEMO-Mozilla-SOPS-Admin/page

This guide explains generating an OpenPGP key pair for use with Mozilla SOPS and FluxCD, including key management and secure cleanup.

In this guide, you’ll learn how to generate an OpenPGP key pair using `gpg`, export the keys for use with [Mozilla SOPS](https://github.com/mozilla/sops) and [FluxCD](https://fluxcd.io/), and then securely clean up local key material. This workflow enables encrypted secrets in GitOps pipelines, ensuring that only Flux can decrypt them in-cluster.

## 1. Install & Review GPG

First, confirm that `gpg` is installed:

```bash theme={null}
gpg --version
```

Then inspect common OpenPGP options:

| Option               | Description                     | Example                                  |
| -------------------- | ------------------------------- | ---------------------------------------- |
| `-o, --output`       | Write output to a specific file | `gpg -o file.txt --decrypt secret.gpg`   |
| `-s, --sign`         | Create a signature              | `gpg -s document.txt`                    |
| `-e, --encrypt`      | Encrypt for specified recipient | `gpg -e -r alice document.txt`           |
| `--list-keys`        | List public keys                | `gpg --list-keys alice`                  |
| `--list-secret-keys` | List secret keys                | `gpg --list-secret-keys`                 |
| `--armor`            | ASCII-armored output            | `gpg --armor --export alice@example.com` |

<Callout icon="lightbulb">
  You can run `gpg --help` for a full list of options. Use `--openpgp` to enforce strict OpenPGP behavior.
</Callout>

## 2. Generate a GPG Key Pair

Create a 3072-bit RSA primary key and subkey with no passphrase or expiration. Replace the real name, email, and comment as needed:

```bash theme={null}
gpg --batch --full-generate-key \
  --passphrase '' \
  --key-length 3072 \
  --subkey-length 3072 \
  --exp-date 0 \
  --name-real "dev.us-e1.k8s" \
  --name-email "admin@bb.com" \
  --comment "k8s"
```

When complete, note the **Key Fingerprint** in the output (e.g., `65DD426C08931CDEB33F4DCCE248B2366542A`). You’ll use this in subsequent commands.

## 3. List and Verify Your Keys

View all public keys:

```bash theme={null}
gpg --list-public-keys
```

Sample output:

```text theme={null}
pub   rsa3072 2023-04-06 [SCEA]
      65DD426C08931CDEB33F4DCCE248B2366542A
uid           [ultimate] dev.us-e1.k8s <admin@bb.com>
sub   rsa3072 2023-04-06 [SEA]
```

To filter by fingerprint:

```bash theme={null}
gpg --list-public-keys 65DD426C08931CDEB33F4DCCE248B2366542A
```

And list secret keys:

```bash theme={null}
gpg --list-secret-keys
```

## 4. Export Keys for SOPS & Flux

### 4.1 Export the Private Key

```bash theme={null}
gpg --export-secret-keys --armor 65DD426C08931CDEB33F4DCCE248B2366542A \
  > sops-gpg.key
```

<Callout icon="triangle-alert">
  Keep `sops-gpg.key` confidential. This private key will be stored in-cluster as a Kubernetes secret. Never commit it to Git.
</Callout>

### 4.2 Export the Public Key

Prepare a directory in your Git repository for the public key:

```bash theme={null}
mkdir -p bb-app-source/sops
cd bb-app-source/sops
gpg --export --armor 65DD426C08931CDEB33F4DCCE248B2366542A \
  > sops-gpg.pub
```

Commit `sops-gpg.pub` so that developers can encrypt secrets:

```bash theme={null}
git add sops-gpg.pub
git commit -m "Add SOPS public key for Flux decryption"
```

## 5. Create a Kubernetes Secret for Flux

Import the private key into the `flux-system` namespace:

```bash theme={null}
kubectl -n flux-system create secret generic sops-gpg \
  --from-file=sops.asc=sops-gpg.key
```

Verify the secret:

```bash theme={null}
kubectl -n flux-system get secret sops-gpg
