# KeyValue Secrets Engine

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/KeyValue-Secrets-Engine/page

This guide explores the Key/Value Secrets Engine in Vault, focusing on storing static secrets and managing them effectively.

In this guide, we’ll explore the Key/Value (KV) Secrets Engine in Vault, focusing on what Operations Professionals need to know. The KV Secrets Engine is ideal for storing **static secrets**—such as service-account passwords or API keys—that are generated outside Vault. While Vault also offers powerful dynamic credentials, static secrets remain ubiquitous in many environments.

Vault supports two flavors of the KV Secrets Engine:

* **Version 1**: A simple, non-versioned store.
* **Version 2**: A fully versioned store, tracking metadata (creation time, version number, deletion status, etc.).

Secrets can be accessed via the UI, CLI, or API. Access control is enforced by Vault policies that grant specific capabilities (`create`, `read`, `update`, `delete`) on defined paths. All data at rest is encrypted using AES-256. You can mount multiple KV engines at unique paths to isolate workloads.

<Frame>
  ![The image is a slide about the Key/Value Secrets Engine, explaining how it can be enabled at different paths, stores secrets as key-value pairs, and requires specific capabilities for writing and updating secrets.](https://kodekloud.com/kk-media/image/upload/v1752878473/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-KeyValue-Secrets-Engine/key-value-secrets-engine-slide.jpg)
</Frame>

***

## How to Store Secrets as Key/Value Pairs

To write secrets, choose a mount path and supply your key/value pairs. For example, after enabling the KV engine at `secret/`:

```bash theme={null}
vault write secret/applications/web01 \
  user=dbadmin \
  password=P@ssw0rd \
  api=b93md83mdmapw
```

* **create** capability is required when writing to a new path.
* **update** capability is required for overwriting an existing secret.

<Callout icon="lightbulb">
  Ensure your Vault policies explicitly grant `create` and `update` permissions on the exact path (e.g., `secret/applications/web01`) or via wildcards (e.g., `secret/applications/*`).
</Callout>

***

## Organizing a KV Engine Hierarchy

Suppose you mount a KV engine at `apps/`. You can structure environments like this:

* `apps/AWS/prod` – Production credentials
* `apps/AWS/dev`  – Development certificates

Example writes:

```bash theme={null}
vault write apps/AWS/prod \
  user=dbadmin \
  password=P@ssw0rd \
  api=b93md83mdmapw

vault write apps/AWS/dev \
  cert='---BEGIN CERTI...' \
  key='---BEGIN PRIVA...'
```

You can also manage KV engines via the CLI.

***

## Enabling and Listing KV Version 1

```bash theme={null}
