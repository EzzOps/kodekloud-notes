# NAME      TYPE    DATA   AGE
# sops-gpg  Opaque  1      30s
```

FluxCD will mount this secret to decrypt any SOPS-encrypted manifests in Git.

## 6. Clean Up Local GPG Material

Once the keys are exported and stored:

```bash theme={null}
rm sops-gpg.key

# Remove both public and secret keys from your local keyring:
gpg --delete-secret-and-public-keys 65DD426C08931CDEB33F4DCCE248B2366542A
```

Confirm deletion:

```bash theme={null}
gpg --list-secret-keys 65DD426C08931CDEB33F4DCCE248B2366542A
gpg --list-public-keys 65DD426C08931CDEB33F4DCCE248B2366542A
# gpg: error reading key: No public key
```

## 7. Summary

You have successfully:

1. Generated a 3072-bit OpenPGP key pair without passphrase or expiry.
2. Exported and committed the public key for developer usage.
3. Created a Kubernetes secret containing the private key for FluxCD.
4. Cleared all local key material to maintain security.

You’re now ready to encrypt secrets with `sops-gpg.pub` in your GitOps repository—Flux will automatically decrypt them in-cluster.

## Links and References

* [OpenPGP Official Site](https://www.openpgp.org/)
* [Mozilla SOPS GitHub](https://github.com/mozilla/sops)
* [FluxCD Documentation](https://fluxcd.io/docs/)
* [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/c8ad2608-2804-4413-9041-5e8dc9126d53/lesson/1f64b743-b032-46e6-af75-c00467869125)


# DEMO Mozilla SOPS Developer

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Secret-Management-Sign-Verification/DEMO-Mozilla-SOPS-Developer/page

Learn to encrypt and manage Kubernetes secrets in Git using Mozilla SOPS with a PGP key and automate decryption with FluxCD.

Learn how to encrypt and manage your Kubernetes secrets in Git using [Mozilla SOPS](https://github.com/mozilla/sops) with a PGP key, then let FluxCD decrypt them automatically on apply.

## Prerequisites

* A Git repository with your application code checked out.
* Administrator-generated PGP keypair (public key committed in `infrastructure/SOPS/`).
* FluxCD installed in your cluster.
* `gpg`, `git`, `wget`, and `kubectl` available on your machine.

***

## Table of Contents

1. [Prepare the Repository](#prepare-the-repository)
2. [Import the Public PGP Key](#import-the-public-pgp-key)
3. [Install SOPS](#install-sops)
4. [Encrypt the Secret with SOPS](#encrypt-the-secret-with-sops)
5. [Commit and Push](#commit-and-push)
6. [Configure FluxCD Decryption](#configure-fluxcd-decryption)
7. [Verify Decrypted Secret in Cluster](#verify-decrypted-secret-in-cluster)

***

## 1. Prepare the Repository

Switch to your infrastructure branch and restore the plaintext secret for re-encryption.

```bash theme={null}
cd bb-app-source/
git checkout infrastructure
```

> **triangle-alert** Always back up existing sealed or encrypted secrets before modifying them.

| Action                            | Command                                                                      |
| --------------------------------- | ---------------------------------------------------------------------------- |
| Backup old Bitnami Sealed Secret  | `mv database/secret-mysql-sealed.yaml database/secret-mysql-sealed.yaml.bak` |
| Restore plaintext secret manifest | `mv database/secret-mysql-backup.yaml database/secret-mysql.yaml`            |

Verify the plaintext `Secret` at `database/secret-mysql.yaml`:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: secret-mysql
  namespace: database
stringData:
  password: mysql-password-0123456789
```

***

## 2. Import the Public PGP Key

On a fresh developer machine, confirm you have no existing public keys:

```bash theme={null}
gpg --list-public-keys
