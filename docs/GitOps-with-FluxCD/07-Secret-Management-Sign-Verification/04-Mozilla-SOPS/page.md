# Mozilla SOPS

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Secret-Management-Sign-Verification/Mozilla-SOPS/page

Learn to use Mozilla SOPS with PGP to securely encrypt and manage Kubernetes secrets in Git repositories.

In this guide, you’ll learn how to use Mozilla SOPS with PGP (GPG) to securely encrypt and manage Kubernetes secrets in Git repositories.

## Overview

SOPS (Secrets OPerationS) lets you encrypt structured files—YAML, JSON, and ENV—so they can be safely stored in public Git repos. It integrates with multiple key management systems:

| Provider        | URI Scheme          |
| --------------- | ------------------- |
| Google KMS      | `gcp-kms://…`       |
| AWS KMS         | `awskms://…`        |
| Azure Key Vault | `azurekeyvault://…` |
| HashiCorp Vault | `vault://…`         |
| PGP/GPG         | `pgp:KEYID`         |

> **lightbulb** For full SOPS documentation, see the Mozilla SOPS [GitHub repository](https://github.com/mozilla/sops).

## What Is PGP/GPG?

* **PGP**: Pretty Good Privacy
* **GPG**: GNU Privacy Guard (OpenPGP implementation)

Both provide strong encryption and decryption for secure data handling.

## Step 1: Generate a GPG Key

Create a 3072-bit RSA key without passphrase or expiration:

```bash theme={null}
gpg --batch --full-generate-key <<EOF
%no-protection
Key-Type: RSA
Key-Length: 3072
Subkey-Type: RSA
Subkey-Length: 3072
Expire-Date: 0
Name-Comment: k8s
Name-Real: prod.us-e1.k8s
Name-Email: admin@bb.com
EOF
```

Verify the fingerprint:

```text theme={null}
gpg: key CDF0BCF69E51F marked as ultimately trusted
```

List and export your keys:

```bash theme={null}
