# Read anything under application1
path "secret/apps/application1/*" {
  capabilities = ["read"]
}

# Matches kv/platform/db-2, kv/platform/db-3/production, etc.
path "kv/platform/db-*" {
  capabilities = ["read"]
}
```

To include the parent path itself:

```hcl theme={null}
path "secret/apps/application1" {
  capabilities = ["read"]
}
```

### Plus (`+`) Wildcards

```hcl theme={null}
# Matches secret/dev/db, secret/prod/db, etc.
path "secret/+/db" {
  capabilities = ["read"]
}

# Matches kv/data/apps/dev/webapp or kv/data/apps/qa/webapp
path "kv/data/apps/+webapp" {
  capabilities = ["read"]
}
```

Combine both for advanced matching:

```hcl theme={null}
path "secret/apps/+/*team-*" {
  capabilities = ["create", "read"]
}
```

<Callout icon="triangle-alert">
  Wildcards can inadvertently grant broader access. Always test your patterns to ensure they match only the intended paths.
</Callout>

***

## ACL Templates (Variable Interpolation)

Use Vault templates to inject dynamic values:

```hcl theme={null}
path "secret/data/{{identity.entity.id}}/*" {
  capabilities = ["create", "read", "update", "delete"]
}

path "secret/metadata/{{identity.entity.id}}/*" {
  capabilities = ["list"]
}
```

Vault replaces `{{identity.entity.id}}` at runtime, generating per-user policies automatically. Other templates include `identity.entity.name`, group IDs, and more.

***

## Assigning and Testing Policies

1. Create a policy (e.g., `web-app`) via the Vault CLI or API.

2. Issue a token bound to that policy:

   ```bash theme={null}
   vault token create -policy="web-app"
   ```

   Example output:

   Key                     Value

   ***

   token                   [VAULT_TOKEN]
   token\_accessor          18r88muoe3x1xEqVqXdlTMwJ
   token\_duration          8h
   token\_renewable         true
   token\_policies          \["default" "web-app"]
   identity\_policies       \[]

3. Test with the new token:

   ```bash theme={null}
   vault login <token>

   # Should succeed (read)
   vault read secret/apikey/Google

   # Should fail (no create/update)
   vault write secret/apikey/Google key="ABCDE12345"

   # Should succeed (AWS read-only creds)
   vault read aws/creds/s3-readonly
   ```

***

## Example: Administrative Policy

Operators require access to system (`sys/`) endpoints. Sample admin policy:

```hcl theme={null}
# License management
path "sys/license" {
  capabilities = ["read", "list", "create", "update", "delete"]
}

# Initialize Vault
path "sys/init" {
  capabilities = ["read", "create", "update"]
}

# UI settings
path "sys/config/ui" {
  capabilities = ["read", "list", "update", "delete", "sudo"]
}

# Rekey operations
path "sys/rekey/*" {
  capabilities = ["read", "list", "create", "update", "delete"]
}

# Rotate the master key
path "sys/rotate" {
  capabilities = ["update", "sudo"]
}

# Seal/unseal Vault
path "sys/seal" {
  capabilities = ["sudo"]
}
```

For more examples, see the official HashiCorp [Vault documentation][vault-docs] and community [Vault guides][vault-guides].

[vault-docs]: https://www.vaultproject.io/docs/

[vault-guides]: https://github.com/hashicorp/vault-guides

***

Mastering Vault policies—capabilities, wildcards, and templates—is essential for robust RBAC. Practice in a dev environment to solidify your understanding.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/968cf007-376b-48c8-83f9-17521b5dd575/lesson/8b8d6d11-227a-463c-8942-8d935f3ea30d" />
</CardGroup>


# Demo Vault Agent

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Configure-Vault-Agent/Demo-Vault-Agent/page

This tutorial explains configuring HashiCorp Vault Agent for automatic AppRole login and dynamic template rendering to inject secrets into a configuration file.

In this tutorial, you’ll learn how to configure HashiCorp Vault Agent for automatic AppRole login and dynamic template rendering. By the end, you’ll have a Vault Agent setup that fetches a token via AppRole and injects secrets into a configuration file.

## Prerequisites

* A local Vault server running, unsealed, and accessible at `http://127.0.0.1:7200`.
* Vault CLI (`vault`) installed and authenticated as an operator.
* Basic knowledge of Vault’s AppRole auth method and KV secrets engine.

<Callout icon="lightbulb">
  Ensure your Vault server is unsealed and you have the `root` or equivalent token in `VAULT_TOKEN` before proceeding.
</Callout>

***

## 1. Enable and Configure AppRole

1. **Enable the AppRole auth method**
   ```bash theme={null}
   vault auth enable approle
   ```
2. **Create an AppRole named `agent`** with the policy `cloud-policy`:
   ```bash theme={null}
   vault write auth/approle/role/agent token_policies="cloud-policy"
   ```
3. **Verify the role**
   ```bash theme={null}
   vault read auth/approle/role/agent
   ```
   Expected output:
   ```text theme={null}
   Key              Value
   ---              -----
   token_policies   ["cloud-policy"]
   ```

***

## 2. Retrieve Role ID & Secret ID

1. **Fetch the Role ID**
   ```bash theme={null}
   vault read auth/approle/role/agent/role-id
   ```
2. **Generate a Secret ID**
   ```bash theme={null}
   vault write -f auth/approle/role/agent/secret-id
   ```
3. **Store credentials** in files for the agent to consume:
   ```bash theme={null}
   echo "<ROLE_ID>"   > role.txt
   echo "<SECRET_ID>" > secret.txt
   ```

<Callout icon="triangle-alert">
  Keep `secret.txt` secure! Anyone with access can authenticate as the AppRole.
</Callout>

***

## 3. Create Vault Agent Configuration

Save the following as `agent.hcl`. It tells the agent how to authenticate and where to write its token.

```hcl theme={null}
vault {
  address = "http://127.0.0.1:7200"
}

auto_auth {
  method "approle" {
    config = {
      role_id_file_path                   = "./role.txt"
      secret_id_file_path                 = "./secret.txt"
      remove_secret_id_file_after_reading = true
    }
  }
  sink "file" {
    config = {
      path = "./sink.txt"
    }
  }
}
```

If you prefer to keep the Secret ID after login, set `remove_secret_id_file_after_reading = false`.

***

## 4. Run the Vault Agent

Start the agent with your configuration:

```bash theme={null}
vault agent -config=agent.hcl
```

You should see logs like:

```text theme={null}
2022-06-28T13:28:44.821-0400 [INFO] sink.file: creating file sink
2022-06-28T13:28:44.843-0400 [INFO] auth.handler: authentication successful, sending token to sinks
```

Verify the token is written:

```bash theme={null}
cat sink.txt
```

***

## 5. Enable Templating

Stop the agent (Ctrl+C) and append a `template` block to `agent.hcl`:

```hcl theme={null}
template {
  source      = "./web.tmpl"
  destination = "./output.yaml"
}
```

Now your full `agent.hcl` looks like:

```hcl theme={null}
vault {
  address = "http://127.0.0.1:7200"
}

auto_auth {
  method "approle" {
    config = {
      role_id_file_path                   = "./role.txt"
      secret_id_file_path                 = "./secret.txt"
      remove_secret_id_file_after_reading = false
    }
  }
  sink "file" {
    config = {
      path = "./sink.txt"
    }
  }
}

template {
  source      = "./web.tmpl"
  destination = "./output.yaml"
}
```

### Template File: `web.tmpl`

```yaml theme={null}
production:
  adapter: postgresql
  encoding: unicode
  database: orders
  {{ with secret "kv/apps/webapp" }}
  username: "{{ .Data.data.username }}"
  password: "{{ .Data.data.password }}"
  {{ end }}
```

***

## 6. Populate the KV Store

Store sample credentials under `kv/apps/webapp`:

```bash theme={null}
vault kv put kv/apps/webapp username=administrator password=kfi3ksoi2msij2s
```

***

## 7. Restart the Agent and Verify Rendering

Start the agent again:

```bash theme={null}
vault agent -config=agent.hcl
```

You should see template rendering logs:

```text theme={null}
2022-06-28T13:14:15.854-0400 [INFO] (runner) rendered "./web.tmpl" => "./output.yaml"
```

Inspect the generated file:

```yaml theme={null}
production:
  adapter: postgresql
  encoding: unicode
  database: orders
  username: "administrator"
  password: "kfi3ksoi2msij2s"
```

***

## Configuration Blocks Overview

| Block      | Purpose                                      |
| ---------- | -------------------------------------------- |
| vault      | Vault server address                         |
| auto\_auth | AppRole login method and token sink          |
| sink       | File sink for writing the Vault token        |
| template   | Source and destination for rendering secrets |

***

## Conclusion

You’ve successfully:

* Enabled the AppRole auth method in Vault
* Retrieved Role ID and Secret ID for machine identity
* Configured Vault Agent for auto-authentication and token storage
* Rendered secrets into a dynamic configuration file using templating

For more details, visit the [Vault Agent Documentation](https://www.vaultproject.io/docs/agent).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/0e6639de-d61c-402b-a161-8f7fc39daf07/lesson/de64e058-744c-4a60-a44a-3cd3fe85b6d2" />
</CardGroup>
