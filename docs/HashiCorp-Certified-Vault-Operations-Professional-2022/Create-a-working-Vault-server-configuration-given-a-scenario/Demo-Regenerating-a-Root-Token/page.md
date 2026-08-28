# Demo Regenerating a Root Token

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Demo-Regenerating-a-Root-Token/page

This tutorial explains how to recover access to a Vault cluster by regenerating a root token using recovery keys.

In this tutorial, you’ll learn how to recover access to your Vault cluster by regenerating a root token using the recovery keys. We’ll cover status verification, initialization, revocation, root token generation, and final validation.

## Table of Contents

1. [Check Vault Status](#check-vault-status)
2. [Initialize Vault](#initialize-vault)
3. [Authenticate with the Initial Root Token](#authenticate-with-the-initial-root-token)
4. [Revoke the Root Token](#revoke-the-root-token)
5. [Begin Root Token Generation](#begin-root-token-generation)
6. [Submit Recovery Keys](#submit-recovery-keys)
7. [Decode the New Root Token](#decode-the-new-root-token)
8. [Authenticate with the New Root Token](#authenticate-with-the-new-root-token)
9. [Verify Restored Access](#verify-restored-access)

***

## 1. Check Vault Status

Start with a fresh, uninitialized Vault server configured with AWS KMS auto-unseal:

```bash theme={null}
