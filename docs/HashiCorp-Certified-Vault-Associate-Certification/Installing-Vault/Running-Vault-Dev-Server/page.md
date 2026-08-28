# 1. Download the Vault ZIP archive
curl -O https://releases.hashicorp.com/vault/1.12.3/vault_1.12.3_linux_amd64.zip

# 2. Unzip the archive
unzip vault_1.12.3_linux_amd64.zip

# 3. Move the binary to a system PATH location
sudo mv vault /usr/local/bin/
```

After installation, verify with:

```bash theme={null}
vault --version
```

## Next Steps

1. Create a Vault configuration file (`vault.hcl`)
2. Start the Vault server: `vault server -config=vault.hcl`
3. Initialize: `vault operator init`
4. Unseal: `vault operator unseal`

## Links and References

* [Vault Documentation](https://www.vaultproject.io/docs)
* [HashiCorp Releases](https://releases.hashicorp.com/vault/)
* [Helm Charts](https://github.com/hashicorp/vault-helm)
* [APT Package Repository](https://apt.releases.hashicorp.com)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/a5a3d715-00ac-4573-aa63-061912aafce2/lesson/0ab4cf0a-9e52-4d9e-b338-736d4ace8138" />
</CardGroup>


# Running Vault Dev Server

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Installing-Vault/Running-Vault-Dev-Server/page

This article explains how to run HashiCorp Vault in Dev Server mode for experimentation and development purposes.

Now that you’ve installed HashiCorp Vault on your machine, you can start Vault in Dev Server mode. This mode launches Vault fully initialized, unsealed, and authenticated as the root user—without requiring any configuration files. Dev Server runs entirely in memory, with no TLS encryption, making it ideal for quick experimentation and development but **not** for production.

<Callout icon="triangle-alert">
  Vault Dev Server skips all security controls.

  * Data is lost when the process stops.
  * All traffic is unencrypted.\
    Never use Dev Server in a production or sensitive environment.
</Callout>

## Dev Server Features

| Feature                                   | Description                                                     |
| ----------------------------------------- | --------------------------------------------------------------- |
| Auto-initialized & unsealed               | Vault comes up ready to use without manual setup                |
| Built-in UI                               | Accessible at [http://127.0.0.1:8200](http://127.0.0.1:8200)    |
| Provides a root token                     | Displayed in the startup logs                                   |
| In-memory storage                         | Non-persistent; all data is lost when Vault stops               |
| No TLS                                    | All API calls and UI traffic are in clear text                  |
| Default KV v2 Secrets Engine at `secret/` | Pre-mounted for immediate key/value operations                  |
| Single authentication method              | Root token only; no additional auth backends enabled by default |

<Frame>
  ![The image is a slide titled "Running Vault Dev Server," listing features and warnings about using the Vault Dev Server mode, emphasizing not to use it in production.](https://kodekloud.com/kk-media/image/upload/v1752878169/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Running-Vault-Dev-Server/running-vault-dev-server-features-warnings.jpg)
</Frame>

## When to Use Dev Server

Vault Dev Server is perfect for:

* Proof-of-concepts (POCs) for secret management
* Testing new Vault features or upgrades
* Developing CI/CD integrations (e.g., with [Jenkins](https://www.jenkins.io/))
* Exploring unfamiliar secrets engines

<Frame>
  ![The image is a slide titled "Where Would I Use Dev Server?" listing four uses: Proof of Concepts, New Development Integrations, Testing New Features of Vault, and Experimenting with Features. It includes a graphic of a triangle labeled "Dev Server Mode" and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878170/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Running-Vault-Dev-Server/dev-server-uses-proof-concepts-testing.jpg)
</Frame>

Never run Dev Server mode in a production environment.

## Launching the Dev Server

Assuming the `vault` binary is on your PATH, open a terminal (or PowerShell on Windows) and execute:

```bash theme={null}
vault server -dev
```

You should see output like the following:

```bash theme={null}
==> Vault server configuration:
    Api Address: http://127.0.0.1:8200
    Listener 1: tcp (addr: "127.0.0.1:8200", cluster addr: "127.0.0.1:8201")
    Storage:
      Type: inmem
    Version: Vault v1.7.0
    Version Sha: 4221b8c84b1a074b8e2c554499f92b39bf
==> Vault server started! Log data will stream in below:
2021-04-11T08:04:07.699-0800 [INFO]  core: security barrier initialized
...
Root Token: s.XXXXXXXXXXXXXXXX
```

<Callout icon="lightbulb">
  Before running additional commands, point your shell to the Dev Server:

  ```bash theme={null}
  export VAULT_ADDR='http://127.0.0.1:8200'
  # Windows PowerShell:
  # $Env:VAULT_ADDR = "http://127.0.0.1:8200"
  ```
</Callout>

### Verify Vault Status

Confirm that Vault is unsealed and running:

```bash theme={null}
vault status
```

Expected output:

```bash theme={null}
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Version         1.7.0
Storage Type    inmem
HA Enabled      false
```

You’re now connected to your Dev Server and ready to start issuing Vault commands.

## Next Steps

1. **Authenticate**\
   Use the root token from the startup log:
   ```bash theme={null}
   vault login s.XXXXXXXXXXXXXXXX
   ```
2. **Mount & Test Secrets Engines**\
   For example, enable a new KV engine at `kv-data/`:
   ```bash theme={null}
   vault secrets enable -path=kv-data kv-v2
   ```
3. **Cleanup**\
   When you’re done, terminate the Vault process. All in-memory data will be discarded.

## Links and References

* [Vault Dev Server Documentation](https://www.vaultproject.io/docs/commands/server/dev)
* [HashiCorp Vault Overview](https://www.vaultproject.io/docs/concepts/overview)
* [GitHub Repository: hashicorp/vault](https://github.com/hashicorp/vault)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/a5a3d715-00ac-4573-aa63-061912aafce2/lesson/1d9f7b1a-9a85-4ff9-90b0-649285632e07" />
</CardGroup>
