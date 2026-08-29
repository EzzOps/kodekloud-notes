# Demo Vault Agent

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Vault-Agent/Demo-Vault-Agent/page

Learn to use HashiCorp Vault Agent for automatic AppRole authentication and rendering configuration files with secrets from Vault.

Learn how to leverage HashiCorp Vault Agent to automatically authenticate via AppRole and render configuration files with secrets fetched from Vault.

## Prerequisites

| Requirement       | Description                                          |
| ----------------- | ---------------------------------------------------- |
| Vault Server      | Running, unsealed, and accessible (default `:8200`). |
| Vault CLI & Agent | Installed on your local machine.                     |
| AppRole Policy    | A policy (e.g., `cloud-policy`) defined in Vault.    |

***

## 1. Enable the AppRole Auth Method

Enable AppRole so Vault Agent can authenticate:

```bash theme={null}
vault auth enable approle
```

Expected output:

```text theme={null}
Success! Enabled approle auth method at: approle/
```

> **lightbulb** AppRole is a machine-friendly auth method designed for non-interactive workflows.\
  Learn more: [AppRole Auth Method](https://www.vaultproject.io/docs/auth/approle)

***

## 2. Create an AppRole for the Agent

Define a role with the appropriate policy:

```bash theme={null}
vault write auth/approle/role/agent \
  token_policies="cloud-policy"
```

Verify the role settings:

```bash theme={null}
vault read auth/approle/role/agent
```

Sample output:

| Key              | Value           |
| ---------------- | --------------- |
| bind\_secret\_id | true            |
| token\_policies  | \[cloud-policy] |

***

## 3. Retrieve Role ID and Secret ID

Fetch the `role_id`:

```bash theme={null}
vault read -format=json auth/approle/role/agent/role-id
```

Generate a one-time `secret_id`:

```bash theme={null}
vault write -f auth/approle/role/agent/secret-id
```

Example JSON response:

```json theme={null}
{
  "data": {
    "role_id": "3ae4b467-c469-6a38-adbe-83e1ab5f1dd0",
    "secret_id": "6b74a5ef-d4f5-0690-67f1-c457c1060ac7"
  }
}
```

***

## 4. Store Role ID & Secret ID in Files

Create two files in your working directory:

**role.txt**

```text theme={null}
3ae4b467-c469-6a38-adbe-83e1ab5f1dd0
```

**secret.txt**

```text theme={null}
6b74a5ef-d4f5-0690-67f1-c457c1060ac7
```

> **triangle-alert** Ensure these files have restrictive permissions (e.g., `chmod 600`) to prevent unauthorized access.

***

## 5. Configure Vault Agent (`agent.hcl`)

Define auto-auth and token sink settings:

```hcl theme={null}
auto_auth {
  method "approle" {
    mount_path = "approle"
    config = {
      role_id_file_path    = "/path/to/role.txt"
      secret_id_file_path  = "/path/to/secret.txt"
    }
  }

  sink "file" {
    config = {
      path = "/path/to/sink.txt"
    }
  }
}

vault {
  address = "http://127.0.0.1:8200"
}
```

> **lightbulb** * `mount_path` defaults to `"approle"`.
  * Adjust `address` if your Vault server listens on a different host or port.

***

## 6. Start Vault Agent

Run the agent with your configuration:

```bash theme={null}
vault agent -config=agent.hcl
```

You should see logs indicating successful authentication and token writing:

```text theme={null}
[INFO] sink.file: file sink configured: path=/path/to/sink.txt
[INFO] auth.handler: authentication successful, sending token to sinks
[INFO] auth.handler: renewed auth token
```

Verify the token:

```bash theme={null}
cat /path/to/sink.txt
