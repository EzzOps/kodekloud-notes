# Success! Revoked token (if it existed)
```

> **lightbulb** The token prefix (`s.` or `hvs.`) varies by Vault version.

## Emergency Scenario: Broken Authentication

Imagine Vault uses corporate LDAP for operator logins:

1. Operator logs in via LDAP
2. Vault validates credentials against the LDAP server
3. A network change or firewall misconfiguration breaks LDAP connectivity

![The image illustrates a broken authentication workflow involving a Vault operator, LDAP authentication, and corporate LDAP servers, highlighting issues with authentication and validation. It poses the question of what happens if there is no working authentication method to fix the problem.](https://kodekloud.com/kk-media/image/upload/v1752878485/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Regenerating-a-Root-Token/broken-authentication-workflow-vault-ldap.jpg)

Without a valid auth method or a root token, you cannot update the LDAP backend. In such emergencies, you can regenerate a root token by leveraging your unseal (recovery) keys—ensuring no single individual can generate it alone.

## Regenerating a Root Token

Root token regeneration follows the same quorum-based approach as Vault unsealing. You’ll:

1. Initialize the generation process.
2. Have each key holder submit their unseal key.
3. Decode the new root token with the one-time password (OTP).

![The image is an instructional guide on regenerating a root token using unseal/recovery keys, with three steps outlined: initializing root generation, each key holder running 'generate root' with their unseal key, and decoding the generated root token. It includes a Vault certification badge and a cartoon character at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878486/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Regenerating-a-Root-Token/regenerate-root-token-instructions-guide.jpg)

### Command Options

Below are the primary flags for `vault operator generate-root`:

![The image is a slide about Vault Initialization, showing command options and their descriptions for generating a root token. It includes a table with options like -generate-otp, -init, and -decode=\<string>.](https://kodekloud.com/kk-media/image/upload/v1752878487/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Regenerating-a-Root-Token/vault-initialization-command-options-table.jpg)

| Flag      | Description                                           |
| --------- | ----------------------------------------------------- |
| `-init`   | Start root generation; outputs a `nonce` and `OTP`.   |
| `-status` | View progress (`Progress X/Y`).                       |
| `-cancel` | Abort the generation operation.                       |
| `-otp`    | Supply the one-time password when decoding the token. |
| `-decode` | Provide the encoded token string for decoding.        |

### Step 1: Initialize Root Generation

Kick off the process to obtain a Nonce and OTP:

```bash theme={null}
vault operator generate-root -init
```

```text theme={null}
A One-Time-Password has been generated for you and is shown in the OTP field.
Keep this OTP secure; it’s required to decode the new root token.
Nonce        5b6e3831-2a45-4695-7757-5810074d36c8
Started      true
Progress     0/3
Complete     false
OTP          E87jF6ZeJo8NjWvytl7mvKLEr
OTP Length   26
```

* **Nonce**: Share with key holders.
* **OTP**: Confidential; do not expose.
* **Progress**: Tracks submissions (e.g., 0/3 keys submitted).

> **triangle-alert** Guard the OTP carefully. Anyone with the OTP and the final encoded token can reconstruct the root token.

### Step 2: Key Holders Submit Unseal Keys

Each key holder runs the command (no flags):

```bash theme={null}
vault operator generate-root
```

```text theme={null}
Root generation operation nonce: 5b6e3831-2a45-4695-7757-5810074d36c8
Unseal Key (hidden input):
Nonce       5b6e3831-2a45-4695-7757-5810074d36c8
Started     true
Progress    1/3
Complete    false
```

Repeat until the threshold is reached. After the final key:

```bash theme={null}
vault operator generate-root
```

```text theme={null}
Nonce          5b6e3831-2a45-4695-7757-5810074d36c8
Started        true
Progress       3/3
Complete       true
Encoded Token  G2NeKUZgXTsYYxILAC9ZFBguPw9ZBovFAs
```

### Step 3: Decode the Root Token

Use the OTP and the encoded token to reveal the new root token:

```bash theme={null}
vault operator generate-root \
  -otp="E87jF6ZeJo8NjWvytl7mvKLEr" \
  -decode="G2NeKUZgXTsYYxILAC9ZFBguPw9ZBovFAs"
```

```text theme={null}
Root token: hvs.gXtT3uq9teYf0ZnFQH6hOiw8
```

Authenticate and then revoke promptly:

```bash theme={null}
vault login hvs.gXtT3uq9teYf0ZnFQH6hOiw8
vault token revoke hvs.gXtT3uq9teYf0ZnFQH6hOiw8
# Success! Revoked token (if it existed)
```

## Best Practices

* Always revoke root tokens immediately after use.
* Limit the number of key holders and enforce MFA for key storage.
* Rotate recovery keys and OTP lifetimes regularly.

## References

* [HashiCorp Vault Operator Commands](https://www.vaultproject.io/docs/commands/operator)
* [Vault Authentication Methods](https://www.vaultproject.io/docs/auth)
* [Vault Init & Unseal](https://www.vaultproject.io/docs/concepts/core/seal)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/f5208dd1-969f-4f36-8709-41efd2a34db4)


# Rekey Vault and Rotate Encryption Keys

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Rekey-Vault-and-Rotate-Encryption-Keys/page

Learn to rekey Vault and rotate encryption keys for enhanced security and compliance in Vault administration tasks.

In this final lesson, you’ll learn how to rekey Vault (regenerate unseal or recovery key shares) and rotate the encryption key that secures data-at-rest. Both operations are essential Vault administration tasks that help maintain security, comply with policies, and ensure high availability.

## Rekey Vault

Rekeying creates a brand-new set of unseal or recovery key shares and lets you adjust how many shares exist and how many are required to reconstruct the master key. This operation is performed online—Vault continues to serve requests throughout.

![The image explains the concept of "Rekey" in a Vault system, highlighting its functions such as creating new recovery keys, specifying key numbers and thresholds, requiring a key threshold for rekeying, and providing a nonce value for key holders.](https://kodekloud.com/kk-media/image/upload/v1752878488/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Rekey-Vault-and-Rotate-Encryption-Keys/rekey-vault-system-functions-diagram.jpg)

By default, Vault initializes with 5 shares and a threshold of 3. Rekeying can, for example, increase this to 10 shares with a threshold of 7, or reduce it to 1 share with a threshold of 1—giving you full control over key distribution and recovery.

### Why Rekey Vault?

Rekeying is commonly required when:

* Lost or inaccessible key shares need replacement (e.g., lost PGP private key).
* Employees or key holders leave the organization.
* Your security policy mandates periodic rotation of master key shares.

![The image explains reasons for rekeying, such as lost keys, employee departures, and organizational security policies, using a diagram of key shards leading to a master key.](https://kodekloud.com/kk-media/image/upload/v1752878490/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Rekey-Vault-and-Rotate-Encryption-Keys/rekeying-reasons-diagram-key-shards.jpg)

### Rekey Command

Use the `vault operator rekey` command to start a rekey. You can include `-key-shares` and `-key-threshold` to change those values.

Initialize a rekey for recovery keys (auto-unseal defaults to unseal keys):

```bash theme={null}
vault operator rekey -init -target=recovery
```

Example output:

```bash theme={null}
WARNING! If you lose the keys after they are returned, there is no recovery...
Key                Value
---                -----
Nonce              6e2fb7b0-b9f6-12a8-d94c-a36a7b26c67c
Started            true
Rekey Progress     0/3
New Shares         5
New Threshold      3
```

Distribute the nonce to key holders. Each holder submits their key share with:

```bash theme={null}
vault operator rekey -target=recovery
```

Progress output:

```bash theme={null}
Rekey operation nonce: 6e2fb7b0-b9f6-12a8-d94c-a36a7b26c67c
Unseal Key (will be hidden):
Key                Value
---                -----
Nonce              6e2fb7b0-b9f6-12a8-d94c-a36a7b26c67c
Rekey Progress     1/3
```

Repeat until the threshold is met. On the final submission, Vault prints the new key shares:

```bash theme={null}
vault operator rekey -target=recovery
```

```bash theme={null}
Key 1: DwCpPnsbvUMqBtXJcAewCHgYr4b+5C56036mWDpX7d7r
Key 2: roNCdtdoK+Z7crwZvprYsrXm7ZkIzj7lwm6gq8LkP
Key 3: 5BYFqW/PT1TXtFmzXft10XwqIt6v/gQjWF8srMbx7Luo
Key 4: eD6gKkcdM5TmsnSSk5kOogI5KksdH2GzvguyBFungPS
Key 5: HtFsHfCvYsICEeTguouhqr4K9ehXAoJm8ktxdT0EJl

Vault rekeyed with 5 key shares and a key threshold of 3. Please securely distribute the key shares printed above. When Vault is re-sealed, restarted, or stopped, you must supply at least 3 of these keys to unseal it before it can start servicing requests.
```

> **lightbulb** In Vault Enterprise with replication enabled, always run the rekey on the primary cluster. Replicas will automatically receive the updated key shares.

### Production Impact

Rekey is non-disruptive. Vault continues handling API calls and UI requests throughout the process, ensuring zero downtime.

## Rekey vs. Key Rotation

These two operations are often confused. The diagram below clarifies their roles:

<Frame>
  <img alt="The image illustrates the difference between &#x22;Rekey&#x22; and &#x22;Key Rotation,&#x22; showing a process involving unseal/recovery keys leading to a master key, and an encryption key protected by a master key." />
</Frame>

| Operation    | Purpose                                                                                              |
| ------------ | ---------------------------------------------------------------------------------------------------- |
| Rekey        | Rotate unseal/recovery key shares and regenerate the master key.                                     |
| Key Rotation | Rotate the data-at-rest encryption key, retaining old keys for decryption without user intervention. |

## Rotate Encryption Key

Key rotation updates Vault’s internal encryption key used for data-at-rest. Vault transparently retains old key versions so existing data remains decryptable.

<Frame>
  <img alt="The image explains key rotation, highlighting that it involves changing the encryption key used for data protection without requiring user access, and allows old data to be decrypted with the previous key. It includes a visual of an encryption key and a &#x22;Rotate&#x22; button." />
</Frame>

Execute the following command:

```bash theme={null}
vault operator rotate
```

Sample output:

```bash theme={null}
Success! Rotated key

Key Term            2
Install Time        2022-12-25 15:47:00 UTC
Encryption Count    6
```

### Permissions Required

To rotate the encryption key, your policy must grant:

| Path           | Capabilities |
| -------------- | ------------ |
| sys/rotate     | update, sudo |
| sys/key-status | read         |

> **triangle-alert** Omitting `sys/key-status` read permission causes the CLI to report a permission error when displaying key status, even though the rotation itself succeeds.

***

## Links and References

* [Vault CLI Operator Commands](https://www.vaultproject.io/docs/commands/operator)
* [Vault Security Concepts](https://www.vaultproject.io/docs/concepts)
* [Vault Policies Overview](https://www.vaultproject.io/docs/concepts/policies)

Explore these resources for deeper insights into Vault key management. Good luck practicing these operations in your live environment!

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/a1a66678-68e7-47b1-87ef-ab353c67ac7d)
