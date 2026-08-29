# Check initialization and seal state
vault status
```

Example output:

```plaintext theme={null}
Key                     Value
---                     -----
Recovery Seal Type      awskms
Initialized             false
Sealed                  true
Version                 1.10.0+ent
Storage Type            raft
HA Enabled              true
```

> **lightbulb** Vault is uninitialized and sealed. The `Recovery Seal Type` shows AWS KMS for auto-unseal.

## 2. Initialize Vault

Generate the recovery key shares and the initial root token:

```bash theme={null}
vault operator init
```

Sample output:

```plaintext theme={null}
Recovery Key 1: Sr90rdG3SEEz8pEmUd1HJhWmoDzMLiHwBay4EpD82Duy
Recovery Key 2: Mjk+TZO/p4sm36KTaZFXNuPuCMjdn6Y/Qvm65DLX2e8
Recovery Key 3: 6WltKoVAf8J4yTHVfMt/Ky9txhJL5P3XIlf9W6Baz93
Recovery Key 4: aDy61n4SezTFZFVtfkD6jiUTse16BG4BH4Cx1GRUPjm
Recovery Key 5: +xb/S9Sb4S2poactdbwzjl9zGpH7qB25YmyIOAJ2Yjx
Initial Root Token: hvs.jtEqNjivmy2aw9d30RRpt71
Success! Vault is initialized.
```

> **triangle-alert** Securely distribute and store your recovery keys and initial root token. Anyone holding 3 of 5 keys can generate a new root token.

## 3. Authenticate with the Initial Root Token

Log in using the root token you just received:

```bash theme={null}
vault login hvs.jtEqNjivmy2aw9d30RRpt71
```

You should see:

```plaintext theme={null}
Success! You are now authenticated.
token                 hvs.jtEqNjivmy2aw9d30RRpt71
token_policies        ["root"]
```

## 4. Revoke the Root Token

Revoking the root token simulates loss of access:

```bash theme={null}
vault token revoke hvs.jtEqNjivmy2aw9d30RRpt71
```

After revocation, any Vault API call will return a `403 permission denied`:

```bash theme={null}
vault policy list
# → Error listing policies: permission denied
```

Now no valid authentication mechanism remains.

## 5. Begin Root Token Generation

Initialize the root-token recovery process:

```bash theme={null}
vault operator generate-root -init
```

Output includes:

```plaintext theme={null}
Nonce         babe8c7d-8a2d-f604-0d27-3667f70e93bb
Progress      0/3
OTP           LlfdKVI8pV5pQZQExfi10s5LIRvws
OTP Length    28
```

> **lightbulb** Save the **Nonce** and **One-Time Password (OTP)**. You will need them to decode the final token.

## 6. Submit Recovery Keys

Enter recovery keys one at a time until you reach the threshold (3/3):

```bash theme={null}
vault operator generate-root
# Enter Unseal Key when prompted
```

Repeat for each key:

| Attempt | Command                      | Progress |
| ------- | ---------------------------- | -------- |
| 1       | vault operator generate-root | 1/3      |
| 2       | vault operator generate-root | 2/3      |
| 3       | vault operator generate-root | 3/3      |

After the third key, you’ll receive an **Encoded Token**:

```plaintext theme={null}
Encoded Token: JBoVSgEbPDI6QQNZJmQeKSYhP3MgVnUKPzIH0Q
```

## 7. Decode the New Root Token

Use the `Encoded Token` and `OTP` to retrieve the actual root token:

```bash theme={null}
vault operator generate-root \
  -decode="JBoVSgEbPDI6QQNZJmQeKSYhP3MgVnUKPzIH0Q" \
  -otp="LlfdKVI8pV5pQZQExfi10s5LIRvws"
```

Result:

```plaintext theme={null}
hvs.jMupJyUlV5DxCYB0c9CMdPj
```

## 8. Authenticate with the New Root Token

Log in with your newly generated root token:

```bash theme={null}
vault login hvs.jMupJyUlV5DxCYB0c9CMdPj
```

Expected output:

```plaintext theme={null}
Success! You are now authenticated.
token                 hvs.jMupJyUlV5DxCYB0c9CMdPj
token_policies        ["root"]
```

## 9. Verify Restored Access

Confirm Vault is functional again:

```bash theme={null}
vault policy list
vault secrets enable aws
# → Enables the AWS secrets engine
```

### Example HCL Policy

```hcl theme={null}
path "sys/tools/hash" {
  capabilities = ["update"]
}

path "identity/oidc/provider/+authorize" {
  capabilities = ["read", "update"]
}
```

***

Regenerating the root token with recovery keys ensures you can restore full access even if the original token is lost or revoked. For more details, see the [Vault CLI Generate-Root Documentation](https://www.vaultproject.io/docs/commands/operator/generate-root).

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/f15c55a1-02f2-423f-83b3-c490a745aabb)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/1ad448b4-a6f6-4003-9e2f-487e6c3bb3e4)


# Demo Rekey Vault and Rotate Encryption Keys

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Demo-Rekey-Vault-and-Rotate-Encryption-Keys/page

This hands-on guide teaches rekeying a Vault cluster and rotating encryption keys using AWS KMS for enhanced security.

In this hands-on guide, you will learn how to rekey a Vault cluster and rotate its encryption keys using AWS KMS for auto-unseal. Rekeying lets you replace old recovery keys (for example when an employee leaves), while key rotation refreshes the master encryption key to maintain security.

## Prerequisites

* Vault Enterprise v1.10.0+ configured with AWS KMS auto-unseal
* `vault` CLI installed (>= v1.10.0)
* AWS IAM permissions for KMS
* Network access to Vault server

## 1. Check Initial Vault Status

Verify that Vault is sealed and using AWS KMS for auto-unseal:

```bash theme={null}
vault status
```

Expected output:

```text theme={null}
Key                        Value
---                        -----
Recovery Seal Type         awskms
Initialized                false
Sealed                     true
Total Recovery Shares      0
Threshold                  0
Unseal Progress            0/0
Unseal Nonce               n/a
Version                    1.10.0+ent
Storage Type               raft
HA Enabled                 true
```

## 2. Initialize the Vault Cluster

Initialize Vault to set up Shamir sealing and generate recovery keys and a root token:

```bash theme={null}
vault operator init > init.txt
```

Vault logs will display the security barrier setup and Raft storage configuration. Review the generated tokens:

```bash theme={null}
cat init.txt
```

Sample output:

```text theme={null}
Recovery Key 1: yILFH1+RnXAWfkwDjPZGfpj2PtChxLHmcCzdBV2dBzhd
Recovery Key 2: XpdyFUPwzNviwcFttS2+fb5/7tiJCaKxgLdZcWr5JPL
Recovery Key 3: 7bNyeKbRz+kkKo3vtlPpcIXGObJcCFaEQL+IUJ5J9BXA
Recovery Key 4: qaFHQJwdMfIDaTcJwltHFDC+/hPjy91StnbZSOCWUKin
Recovery Key 5: FHjem7Hsw0TPkEyvdOvsh8Pp2JymJr6Aa74sajj40/yr

Initial Root Token: hvs.Wxqk6kDX3fAko3LoCCfczQ3D
Success! Vault is initialized.
Recovery key initialized with 5 key shares and a key threshold of 3.
```

Check status again—Vault should now be unsealed with Shamir recovery:

```bash theme={null}
vault status
```

```text theme={null}
Recovery Seal Type         shamir
Initialized                true
Sealed                     false
Total Recovery Shares      5
Threshold                  3
Version                    1.10.0+ent
Storage Type               raft
HA Enabled                 true
...
```

## 3. Rekey the Vault Cluster

Rekeying replaces existing recovery keys with a new set. This is crucial if a key is compromised or when rotating personnel access.

> **triangle-alert** Losing all recovery keys renders your data unrecoverable. Always store keys securely and offsite.

### 3.1 Initiate Rekey

```bash theme={null}
vault operator rekey -init -target=recovery
```

Output:

```text theme={null}
WARNING! If you lose the keys after they are returned, there is no recovery.
Nonce                      9e107605-d80a-c795-e7a2-589c2266b552
Started                    true
Rekey Progress             0/3
New Shares                 5
New Threshold              3
Verification Required      false
```

### 3.2 Submit Existing Recovery Keys

Submit any 3 of the existing 5 recovery keys (order does not matter). Each submission advances the progress:

```bash theme={null}
vault operator rekey -target=recovery
