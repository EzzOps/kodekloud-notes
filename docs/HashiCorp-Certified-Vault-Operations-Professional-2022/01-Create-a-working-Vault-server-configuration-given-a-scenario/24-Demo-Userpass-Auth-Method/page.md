# latest_version: 2
```

## Encrypt Data

1. Base64-encode your plaintext:
   ```bash theme={null}
   BASE64=$(base64 <<< "Getting Started with HashiCorp Vault")
   echo $BASE64
   ```
2. Encrypt the encoded string:
   ```bash theme={null}
   vault write transit/encrypt/training plaintext=$BASE64
   ```

Sample response:

```text theme={null}
Key         Value
---         -----
ciphertext  vault:v2:…  
key_version 2  
```

Store the `ciphertext` for later use.

## Rewrap Data After Rotation

After rotating to version 3:

```bash theme={null}
vault write -f transit/keys/training/rotate
```

Rewrap the version 2 ciphertext to version 3:

```bash theme={null}
vault write transit/rewrap/training \
  ciphertext="vault:v2:…"
```

Response:

```text theme={null}
Key         Value
---         -----
ciphertext  vault:v3:…  
key_version 3  
```

## Decrypt Ciphertexts

Decrypt version 2:

```bash theme={null}
vault write transit/decrypt/training ciphertext="vault:v2:…"
```

Decrypt version 3:

```bash theme={null}
vault write transit/decrypt/training ciphertext="vault:v3:…"
```

Both return the same Base64 plaintext.

## Enforce Minimum Decryption Version

To block decryption of older ciphertext, set `min_decryption_version=3`:

```bash theme={null}
vault write transit/keys/training/config min_decryption_version=3
```

Verify:

```bash theme={null}
vault read transit/keys/training
# min_decryption_version: 3
```

Attempting to decrypt version 2 now fails:

```bash theme={null}
vault write transit/decrypt/training ciphertext="vault:v2:…"
```

<Callout icon="triangle-alert">
  Any ciphertext with a version lower than the `min_decryption_version` will be rejected.
</Callout>

Decryption of version 3 still succeeds:

```bash theme={null}
vault write transit/decrypt/training ciphertext="vault:v3:…"
```

## Conclusion

In this lesson, you have:

* Enabled and configured the Transit Secrets Engine
* Created, rotated, and inspected encryption keys
* Encrypted, decrypted, and rewrapped data
* Enforced minimum decryption version policies

For more information, visit the [Vault Transit Secrets Engine documentation](https://www.vaultproject.io/docs/secrets/transit).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/73cc37b9-4677-4263-ab67-988cec966042" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/dc0cb54c-c853-4bdf-819c-83a0a0094bab" />
</CardGroup>


# Demo Userpass Auth Method

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Demo-Userpass-Auth-Method/page

This tutorial covers enabling and managing the userpass auth method in Vault, including user creation and authentication.

In this tutorial, you’ll learn how to enable and manage the `userpass` auth method in Vault. We’ll cover:

* Enabling and inspecting auth backends
* Configuring and listing policies
* Creating, reading, and updating users
* Authenticating with the `userpass` method

## Table of Contents

1. [Enable the userpass Auth Method](#enable-the-userpass-auth-method)
2. [Inspect Auth Backends](#inspect-auth-backends)
3. [Manage Policies](#manage-policies)
4. [Create and Configure Users](#create-and-configure-users)
5. [Authenticate with userpass](#authenticate-with-userpass)

***

## 1. Enable the userpass Auth Method

First, see which auth methods are currently enabled:

```bash theme={null}
vault auth list
```

Example output:

| Path   | Type  | Accessor              | Description             |
| ------ | ----- | --------------------- | ----------------------- |
| token/ | token | auth\_token\_9e81d3bb | token based credentials |

Enable `userpass` at the default path:

```bash theme={null}
vault auth enable userpass
```

Success message:

```text theme={null}
Success! Enabled userpass auth method at: userpass/
```

:::note Custom Path
You can also enable `userpass` under a custom mount point, for example `local`:

```bash theme={null}
vault auth enable -path=local userpass
```

:::

After enabling, verify both default and custom mounts:

```bash theme={null}
vault auth list
```

| Path      | Type     | Accessor                | Description             |
| --------- | -------- | ----------------------- | ----------------------- |
| local/    | userpass | auth\_userpass\_abcd123 | n/a                     |
| userpass/ | userpass | auth\_userpass\_efgh456 | n/a                     |
| token/    | token    | auth\_token\_9e81d3bb   | token based credentials |

If you only need the default mount, disable the custom one:

```bash theme={null}
vault auth disable local
```

Now you should see:

```bash theme={null}
vault auth list
```

| Path      | Type     | Accessor                | Description             |
| --------- | -------- | ----------------------- | ----------------------- |
| token/    | token    | auth\_token\_9e81d3bb   | token based credentials |
| userpass/ | userpass | auth\_userpass\_efgh456 | n/a                     |

***

## 2. Inspect Auth Backends

Vault supports multiple auth methods. To view all enabled backends:

```bash theme={null}
vault auth list
```

| Mount Point | Auth Method | Description                |
| ----------- | ----------- | -------------------------- |
| token/      | token       | Token-based authentication |
| userpass/   | userpass    | Username & password        |

For more details, see the [Vault Authentication Methods](https://www.vaultproject.io/docs/auth) reference.

***

## 3. Manage Policies

Before creating users, check existing policies:

```bash theme={null}
vault policy list
```

Example output:

* default
* kv-policy
* root

We’ll use `kv-policy` in this demo to grant Key/Value access.

***

## 4. Create and Configure Users

### 4.1 Create Users

Add a new user named `automation` with `kv-policy`:

```bash theme={null}
vault write auth/userpass/users/automation \
    password=Password1 \
    policies=kv-policy
```

Success message:

```text theme={null}
Success! Data written to: auth/userpass/users/automation
```

Verify the list of `userpass` users:

```bash theme={null}
vault list auth/userpass/users
```

| Keys       |
| ---------- |
| automation |

Add a second user `bryan`:

```bash theme={null}
vault write auth/userpass/users/bryan \
    password=Secret123 \
    policies=kv-policy
```

Confirm both users:

```bash theme={null}
vault list auth/userpass/users
```

| Keys       |
| ---------- |
| automation |
| bryan      |

### 4.2 Read and Update User Configuration

#### Read Current Settings

Inspect the `automation` user:

```bash theme={null}
vault read auth/userpass/users/automation
```

| Key                        | Value        |
| -------------------------- | ------------ |
| policies                   | \[kv-policy] |
| token\_ttl                 | 0s           |
| token\_max\_ttl            | 0s           |
| token\_no\_default\_policy | false        |

By default, TTLs are `0s`, inheriting the system defaults.

#### Update Token TTL

Set a 24-hour token TTL for `automation`:

```bash theme={null}
vault write auth/userpass/users/automation token_ttl=24h
```

Verify the update:

```bash theme={null}
vault read auth/userpass/users/automation
```

| Key        | Value        |
| ---------- | ------------ |
| token\_ttl | 24h          |
| policies   | \[kv-policy] |

:::note Token Time-To-Live (TTL)
Defining `token_ttl` limits how long a login token remains valid. Adjust according to your security requirements.
:::

***

## 5. Authenticate with userpass

Now that your user is configured, log in with:

```bash theme={null}
vault login -method=userpass username=automation
```

Enter the password when prompted. Example response:

```text theme={null}
Success! You are now authenticated.

Key                    Value
---                    -----
token                  hvs.CAE...5sNTd
token_accessor         62meW...3mjErMQwlQ
token_duration         24h
token_renewable        true
token_policies         ["default" "kv-policy"]
token_meta_username    automation
```

You now have a token scoped to `kv-policy` with a 24-hour TTL. To reuse the token directly:

```bash theme={null}
vault login hvs.CAE...5sNTd
```

Success message:

```text theme={null}
Success! Token renewed successfully.
```

:::warning Security Reminder
Always store your Vault tokens securely. Avoid checking plaintext tokens into version control or logs.
:::

***

## Conclusion

You’ve successfully:

* Enabled and inspected the `userpass` auth method
* Listed and managed Vault policies
* Created users and customized their token TTL
* Authenticated via `userpass` for secure, password-based access

For more on Vault auth methods and best practices, visit the [HashiCorp Vault Documentation](https://www.vaultproject.io/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/0962b0e6-b90b-4f19-91d6-b876d7a9f8cb" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/2019f26f-c69d-43e5-bce8-5a4d70ef4040" />
</CardGroup>
