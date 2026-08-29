# s.xxxxxxxxxxxxxxxxxxxxxxxx
```

***

### 6.1 Preserve the Secret ID File (Optional)

By default, Vault Agent deletes `secret.txt`. To retain it, add `remove_secret_id_file = false`:

```hcl theme={null}
auto_auth {
  method "approle" {
    mount_path = "approle"
    config = {
      role_id_file_path      = "/path/to/role.txt"
      secret_id_file_path    = "/path/to/secret.txt"
      remove_secret_id_file  = false
    }
  }
  sink "file" {
    config = {
      path = "/path/to/sink.txt"
    }
  }
}
```

Restart Vault Agent. The `secret.txt` file will persist.

***

## 7. Templating with Vault Agent

Vault Agent can render templates populated with secrets. Follow these steps:

### 7.1 Prepare the Template (`web.tmpl`)

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

### 7.2 Seed the KV Store

Populate Vault’s KV engine:

```bash theme={null}
vault kv put kv/apps/webapp \
  username="administrator" \
  password="kfi3ksoi2msij2s"
```

### 7.3 Update `agent.hcl` with a Template Block

Add a `template` stanza to render `web.tmpl` to `output.yaml`:

```hcl theme={null}
template {
  source      = "/path/to/web.tmpl"
  destination = "/path/to/output.yaml"
}
```

Full `agent.hcl` snippet:

```hcl theme={null}
template {
  source      = "/path/to/web.tmpl"
  destination = "/path/to/output.yaml"
}

vault {
  address = "http://127.0.0.1:8200"
}
```

### 7.4 Restart Vault Agent & Verify

```bash theme={null}
vault agent -config=agent.hcl
```

Check the rendered file:

```bash theme={null}
cat /path/to/output.yaml
```

Expected content:

```yaml theme={null}
production:
  adapter: postgresql
  encoding: unicode
  database: orders
  username: "administrator"
  password: "kfi3ksoi2msij2s"
```

***

## Conclusion

You’ve now automated the following with Vault Agent:

1. AppRole-based auto-authentication.
2. Securely stored & managed `role_id` and `secret_id`.
3. Token persistency with customizable sinks.
4. Dynamic templating to inject secrets into configuration files.

***

## Links and References

* [Vault Agent Overview](https://www.vaultproject.io/docs/agent)
* [AppRole Auth Method](https://www.vaultproject.io/docs/auth/approle)
* [Vault CLI Documentation](https://www.vaultproject.io/docs/commands)
* [Template Syntax](https://www.vaultproject.io/docs/agent/templates)
* [KV Secrets Engine](https://www.vaultproject.io/docs/secrets/kv)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/25b89318-77a0-4f52-a4d7-2df3696e3362/lesson/72c31d12-bcc9-4d96-b28b-2057ea11b144)


# Intro to the Vault Agent

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Vault-Agent/Intro-to-the-Vault-Agent/page

Vault Agent is a client-side daemon that manages Vault interactions for applications without native integration, enabling secure secret retrieval and token management.

Vault Agent is a client-side daemon that runs alongside your application to handle all Vault interactions on its behalf. It’s especially valuable for legacy or third-party applications without native Vault integration. By deploying Vault Agent, you avoid modifying your application code, while still benefiting from dynamic secret retrieval, secure token management, and template rendering.

## Why Use Vault Agent?

* Securely inject secrets into applications that cannot reach Vault directly
* Automate authentication, token renewal, and secret caching
* Render configuration files at startup using Vault data

> **lightbulb** Vault Agent supports multiple authentication methods (like [AppRole][] and [Kubernetes][]) and can wrap responses to protect tokens in transit.

## Vault Agent Features at a Glance

| Feature                            | Description                                                                         |
| ---------------------------------- | ----------------------------------------------------------------------------------- |
| Automatic Authentication & Renewal | Authenticates to Vault (e.g., AppRole, Kubernetes) and renews tokens automatically. |
| Secure Token Storage & Delivery    | Stores tokens in a configured sink (file, memory) and optionally wraps them.        |
| Local Secret Caching               | Caches fetched secrets to minimize Vault API calls and reduce latency.              |
| Templating                         | Renders configuration files by pulling secrets from Vault into templates.           |

***

## 1. Automatic Authentication and Renewal

Vault Agent can authenticate using various methods. Below is an example `auto_auth` block for the AppRole method:

```hcl theme={null}
