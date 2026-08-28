# Demo UserPass Auth Method

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Compare-Authentication-Methods/Demo-UserPass-Auth-Method/page

This tutorial explains how to enable and use the userpass authentication method in HashiCorp Vault for username/password scenarios.

In this tutorial, you’ll learn how to enable and use the **userpass** authentication method in HashiCorp Vault. This approach is ideal for simple username/password scenarios.

## Prerequisites

* Vault CLI installed and configured
* Vault server unsealed and reachable
* A Vault token with `root` or `sudo` privileges

For more details on installing Vault, see the [Vault Installation Guide](https://www.vaultproject.io/docs/install).

***

## 1. Verify Existing Auth Methods

Before enabling new methods, check which authentication backends are active:

```shell theme={null}
vault auth list
```

Example output:

| Path   | Type  | Description                     |
| ------ | ----- | ------------------------------- |
| token/ | token | default token-based credentials |

<Callout icon="lightbulb">
  The `token` method is enabled by default and provides basic token authentication.
</Callout>

***

## 2. Enable the Userpass Auth Method

Activate the `userpass` backend at its default path:

```shell theme={null}
vault auth enable userpass
```

Expected response:

```text theme={null}
Success! Enabled userpass auth method at: userpass/
```

***

## 3. Create Userpass Users

Add individual users under `auth/userpass/users`. Each user can be assigned one or more policies.

| Username | Password | Policies |
| -------- | -------- | -------- |
| frank    | vault    | bryan    |
| jamie    | cloud    | bryan    |

### 3.1 Create User “frank”

```shell theme={null}
vault write auth/userpass/users/frank \
    password=vault \
    policies=bryan
```

### 3.2 Create User “jamie”

```shell theme={null}
vault write auth/userpass/users/jamie \
    password=cloud \
    policies=bryan
```

<Callout icon="triangle-alert">
  Storing plaintext passwords in scripts can be insecure. Consider using environment variables or a secure secrets store.
</Callout>

***

## 4. List and Inspect User Configurations

### 4.1 List All Users

```shell theme={null}
vault list auth/userpass/users
```

Example output:

```text theme={null}
Keys
----
frank
jamie
```

### 4.2 Read a User’s Settings

Inspect configuration for user `jamie`:

```shell theme={null}
vault read auth/userpass/users/jamie
```

Key settings include token TTLs, policies, and CIDR restrictions.

***

## 5. Authenticate with Userpass

After creating users, log in using the `userpass` method. Each login issues a distinct Vault token.

### 5.1 Login as “jamie”

```shell theme={null}
vault login -method=userpass username=jamie
```

Enter password when prompted:

```text theme={null}
Password (will be hidden): cloud
Success! You are now authenticated.
```

### 5.2 Login as “frank”

```shell theme={null}
vault login -method=userpass username=frank
```

Enter password:

```text theme={null}
Password (will be hidden): vault
Success! You are now authenticated.
```

Each session returns token details:

| Field                 | Description                           |
| --------------------- | ------------------------------------- |
| `token`               | Your Vault token                      |
| `token_policies`      | Applied policies (`bryan`, `default`) |
| `token_duration`      | Token TTL                             |
| `token_meta_username` | Username metadata                     |

***

## References

* [Vault Userpass Auth Method](https://www.vaultproject.io/docs/auth/userpass)
* [Vault Authentication Overview](https://www.vaultproject.io/docs/auth)
* [Vault CLI Commands](https://www.vaultproject.io/docs/commands)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/eebfb593-8885-43b0-a9ba-9f88af87092e/lesson/92fadff8-1b0e-42ce-b2f2-80a2d8d05e1c" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/eebfb593-8885-43b0-a9ba-9f88af87092e/lesson/f62930b5-58f2-4c69-aad0-f9710e962cd2" />
</CardGroup>
