# Section Overview Configure Vault Agent

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Configure-Vault-Agent/Section-Overview-Configure-Vault-Agent/page

This article explains how to configure the HashiCorp Vault Agent for authentication, token renewal, and dynamic template rendering.

The HashiCorp Vault Agent is a lightweight client-side daemon that automates authentication, token renewal, and configuration templating. By offloading these responsibilities from your application, you eliminate hardcoded credentials and simplify secret management workflows.

In this section, we'll explore two primary topics:

1. Authenticate and synchronize tokens
2. Render dynamic templates

These built-in features of the Vault Agent—auto-auth, token synchronization, and templating—work together to streamline Vault integration.

> **lightbulb** * Vault Server v1.2+ installed and accessible
  * Supported auto-auth method configured (e.g., Kubernetes, AWS, AppRole)
  * `vault` CLI and Vault Agent binary available in your PATH

## Vault Agent Features at a Glance

| Feature               | Description                                                                 | Benefit                                        |
| --------------------- | --------------------------------------------------------------------------- | ---------------------------------------------- |
| Auto-Authentication   | Automatically authenticates using methods like Kubernetes, AWS, or AppRole. | Removes manual login steps on startup.         |
| Token Synchronization | Periodically renews the Vault token before it expires.                      | Ensures uninterrupted secret access.           |
| Templating            | Renders templates into configuration files or environment variables.        | Injects dynamic secrets into your application. |

> Ready to get started? Let’s dive into secure auto-auth and token synchronization.

## 1. Authenticate and Synchronize Tokens

Vault Agent’s auto-auth feature handles the initial login. Once authenticated, token synchronization keeps your session alive by renewing the token automatically.

* Auto-auth:
  * Supported methods: [Kubernetes](https://www.vaultproject.io/docs/auth/kubernetes), [AWS](https://www.vaultproject.io/docs/auth/aws), [AppRole](https://www.vaultproject.io/docs/auth/approle)
  * Configuration file snippet:
    ```hcl theme={null}
    auto_auth {
      method "approle" {
        mount_path = "auth/approle"
        config = {
          role_id_file_path = "/path/to/role_id"
          secret_id_file_path = "/path/to/secret_id"
        }
      }
      sink "file" {
        config = { path = "/tmp/vault-token" }
      }
    }
    ```

* Token synchronization:
  ```hcl theme={null}
  cache {
    use_auto_auth_token = true
  }
  listener "tcp" {
    address     = "127.0.0.1:8200"
    tls_disable = true
  }
  vault {
    address = "https://vault.example.com:8200"
  }
  ```

> **triangle-alert** Ensure the Vault Agent configuration file (`agent.hcl`) has proper file permissions to prevent unauthorized users from reading sensitive settings.

## 2. Render Dynamic Templates

The Vault Agent template engine uses [HCL](https://www.vaultproject.io/docs/configuration/hcl) or Go templates to inject secrets directly into files or environment variables:

```hcl theme={null}
template {
  source      = "/etc/vault-agent/templates/config.ctmpl"
  destination = "/etc/myapp/config.json"
  command     = "systemctl restart myapp"
}
```

Example `config.ctmpl`:

```hcl theme={null}
{
  "db_username": "{{ with secret "database/creds/app" }}{{ .Data.username }}{{ end }}",
  "db_password": "{{ with secret "database/creds/app" }}{{ .Data.password }}{{ end }}"
}
```

## References

* [Vault Agent Auto-Auth Documentation](https://www.vaultproject.io/docs/agent/autoauth)
* [Vault Agent Template Engine](https://www.vaultproject.io/docs/agent/templates)
* [Vault Configuration HCL](https://www.vaultproject.io/docs/configuration)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/0e6639de-d61c-402b-a161-8f7fc39daf07/lesson/544519ff-f54f-48fd-9133-3db87169cf12)
