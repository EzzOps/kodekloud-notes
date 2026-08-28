# wrapping_token: hvs.CAESI…XYZ
# Wait >5 seconds
vault unwrap hvs.CAESI…XYZ
# Error: wrapping token is not valid or does not exist
```

Or with 5-minute TTL:

```bash theme={null}
vault kv get -wrap-ttl=5m secret/training
# wrapping_token: hvs.CAESI…ABC
vault unwrap hvs.CAESI…ABC  # succeeds
vault unwrap hvs.CAESI…ABC  # fails immediately
```

## 7. UI Demonstration

In the Vault UI, a privileged user can:

1. Navigate to **Secrets → KV**
2. Select **training** and choose **Wrap**
3. Copy the wrapping token and share via secure channels

An unprivileged user then goes to **Tools → Unwrap Secret**, pastes the token, and retrieves the secret.

<Frame>
  ![The image shows a web interface for HashiCorp Vault, displaying a secret with a key-value pair under the "training" section. A notification at the bottom indicates a secret was successfully wrapped.](https://kodekloud.com/kk-media/image/upload/v1752878420/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Demo-Cubbyhole-Secrets-Engine/hashicorp-vault-web-interface-secret-training.jpg)
</Frame>

***

## Summary

* Stored token-specific data in **Cubbyhole**
* Verified strict isolation between tokens
* Secured KV secrets and demonstrated access denial
* Generated, inspected, and unwrapped **response-wrapping** tokens
* Showed one-time-use and TTL behaviors via CLI & UI

By following this guide, you can securely share secrets without exposing them directly over the network.

***

## References

* [Vault Overview][vault-overview]
* [Cubbyhole Secrets Engine][cubbyhole-docs]
* [Response Wrapping Guide][wrapping-docs]

[vault-overview]: https://www.vaultproject.io/docs/what-is-vault

[cubbyhole-docs]: https://www.vaultproject.io/docs/secrets/cubbyhole

[wrapping-docs]: https://www.vaultproject.io/docs/concepts/response-wrapping

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/4b3224f2-2952-45d2-95f8-dc95b46714a0" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/9e8d0533-11b3-4299-81b1-0eece13c20e6" />
</CardGroup>


# Demo Identity Secrets Engine

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Demo-Identity-Secrets-Engine/page

Learn to use HashiCorp Vaults Identity Secrets Engine for user creation, policy management, and entity handling.

In this guide, you’ll learn how to leverage the HashiCorp Vault Identity Secrets Engine to:

* Create a user with the **userpass** auth method
* Define entities and entity aliases
* Observe how combined policies affect access
* (Optionally) Manage entities via the Vault UI

Before you begin, make sure a Vault server is running and you have a root token.

<Callout icon="lightbulb">
  * Vault ≥ 1.0 installed and unsealed
  * Root token for policy/entity management
  * `vault` CLI available in your `$PATH`
</Callout>

***

## 1. Review Existing Policies

List current policies to confirm what’s available:

```bash theme={null}
vault policy list
```

Expected output:

```plaintext theme={null}
default
engineering
kv-policy
manager
root
```

We will use **kv-policy** and **manager** in this demo.

### Policy Permissions Overview

| Policy    | Path                    | Capabilities |
| --------- | ----------------------- | ------------ |
| kv-policy | kv/data/automation      | read         |
| manager   | kv/data/operations/\*\* | read         |

***

## 2. Create a Userpass User

Define a new user `bryan` with the `kv-policy` attached:

```bash theme={null}
vault write auth/userpass/users/bryan \
    password=bryan \
    policies=kv-policy
```

You should see:

```plaintext theme={null}
Success! Data written to: auth/userpass/users/bryan
```

Verify the policy:

```bash theme={null}
vault policy read kv-policy
```

```hcl theme={null}
path "kv/data/automation" {
  capabilities = ["read"]
}
```

And inspect the `manager` policy:

```bash theme={null}
vault policy read manager
```

```hcl theme={null}
path "kv/data/operations/**" {
  capabilities = ["read"]
}
```

***

## 3. Authenticate as `bryan` and Test Access

Log in with the new user:

```bash theme={null}
vault login -method=userpass username=bryan
Password (will be hidden):
```

Successful login shows:

```plaintext theme={null}
token_policies       ["default" "kv-policy"]
```

### Test Allowed Access

```bash theme={null}
vault kv get kv/automation
```

```plaintext theme={null}
=== Secret Path ===
kv/data/automation

 ======= Metadata =======
 Key     Value
 version 1

 ======= Data =======
 Key           Value
 certification hcvop
```

### Test Denied Access

```bash theme={null}
vault kv get kv/operations/admin
```

```plaintext theme={null}
Error reading kv/data/operations/admin: 403 Permission denied
```

<Callout icon="triangle-alert">
  You should see a **403 Permission denied** error because `kv-policy` does not cover `operations/**`.
</Callout>

***

## 4. Obtain the Userpass Mount Accessor

Re-authenticate as root and list auth methods to retrieve the `mount_accessor`:

```bash theme={null}
vault auth list
```

```plaintext theme={null}
Path       Type       Accessor
----       ----       --------
token      token      auth_token_9e81d3bb
userpass/  userpass   auth_userpass_0479382c
```

Note the `auth_userpass_0479382c` value for the next step.

***

## 5. Create an Entity and Entity Alias

1. **Create an entity** named “Bryan Krausen” with the `manager` policy:

   ```bash theme={null}
   vault write identity/entity \
       name="Bryan Krausen" \
       policies=manager
   ```

   ```plaintext theme={null}
   Key   Value
   ---   -----
   id    7a0f656b-8c8e-d6fd-83da-1d5650d85c38
   name  Bryan Krausen
   ```

2. **Link the user to that entity** via an alias:

   ```bash theme={null}
   vault write identity/entity-alias \
       name="bryan" \
       canonical_id="7a0f656b-8c8e-d6fd-83da-1d5650d85c38" \
       mount_accessor="auth_userpass_0479382c"
   ```

   ```plaintext theme={null}
   Key            Value
   ---            -----
   canonical_id   7a0f656b-8c8e-d6fd-83da-1d5650d85c38
   id             7a2a8c47-d65b-44a5-c0b5-8a45a9ddb588
   ```

***

## 6. Verify Combined Policies

Log back in as `bryan`:

```bash theme={null}
vault login -method=userpass username=bryan
Password (will be hidden):
```

Now your token includes three policies:

```plaintext theme={null}
policies            ["default" "kv-policy" "manager"]
identity_policies   ["manager"]
```

### Test Enhanced Access

* **Automation secret** (via `kv-policy`):

  ```bash theme={null}
  vault kv get kv/automation
  ```

* **Operations secret** (via `manager` policy):

  ```bash theme={null}
  vault kv get kv/operations/admin
  ```

  ```plaintext theme={null}
  === Secret Path ===
  kv/data/operations/admin

  ===== Data =====
  Key    Value
  ---    -----
  creds  lj3ofdj2posl2
  ```

You can repeat this process to add additional aliases (e.g., [GitHub](https://www.vaultproject.io/docs/auth/github), [OIDC](https://www.vaultproject.io/docs/auth/oidc)) to grant the same `manager` policy across auth methods.

***

## 7. Using the Vault UI

1. In the Vault UI, navigate to **Access → Entities**.
2. Create or delete entities, view details, and manage aliases.

<Frame>
  ![The image shows a user interface for managing entities in a system, displaying details such as name, ID, and timestamps for creation and last update. It appears to be part of a software application related to access management.](https://kodekloud.com/kk-media/image/upload/v1752878422/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Demo-Identity-Secrets-Engine/access-management-entity-ui-details.jpg)
</Frame>

3. To add an alias, choose **Create Entity Alias**:

<Frame>
  ![The image shows a web interface for creating an entity alias in HashiCorp Vault, with fields for "Name" and "Auth Backend" and options to create or cancel.](https://kodekloud.com/kk-media/image/upload/v1752878423/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Demo-Identity-Secrets-Engine/hashicorp-vault-entity-alias-interface.jpg)
</Frame>

4. Inspect token settings and policies:

<Frame>
  ![The image shows a user interface for managing access in HashiCorp Vault, displaying token settings and policies for a user named "bryan." The sidebar includes options like Auth Methods, Entities, and Groups.](https://kodekloud.com/kk-media/image/upload/v1752878424/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Demo-Identity-Secrets-Engine/hashicorp-vault-user-interface-bryan.jpg)
</Frame>

5. View or merge entities as needed:

<Frame>
  ![The image shows a web interface for managing entities in HashiCorp Vault, displaying a list of entities with their aliases and options to merge or create new entities.](https://kodekloud.com/kk-media/image/upload/v1752878425/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Demo-Identity-Secrets-Engine/hashicorp-vault-entity-management-interface.jpg)
</Frame>

***

## Links and References

* [Vault Identity Secrets Engine](https://www.vaultproject.io/docs/secrets/identity)
* [Userpass Auth Method](https://www.vaultproject.io/docs/auth/userpass)
* [Vault CLI Commands](https://www.vaultproject.io/docs/commands)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/f695566f-8dbe-454e-8c59-ccb5a035daf5" />
</CardGroup>
