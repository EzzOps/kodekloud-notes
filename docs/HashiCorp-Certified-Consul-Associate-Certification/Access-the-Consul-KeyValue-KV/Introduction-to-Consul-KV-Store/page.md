# => true
```

A response of `true` means the write succeeded. If the path (`data/app4`) doesn’t exist, Consul creates it automatically.

### 1.2 Reading a Key (`GET`)

```bash theme={null}
curl https://consul.example.com:8500/v1/kv/data/app4 | jq
```

```json theme={null}
[
  {
    "LockIndex": 0,
    "Key": "data/app4",
    "Flags": 0,
    "Value": "J2VuYWJsZWQn",
    "CreateIndex": 69,
    "ModifyIndex": 87
  }
]
```

The `Value` field is Base64-encoded. Decode it:

```bash theme={null}
echo "J2VuYWJsZWQn" | base64 --decode
# => 'enabled'
```

<Callout icon="lightbulb">
  Base64 encoding is not encryption. Data at rest in Consul is unencrypted by default; the API simply returns values encoded in Base64.
</Callout>

For full API reference, see the [Consul KV HTTP API documentation](https://www.consul.io/api-docs/kv).

***

## 2. Consul Command-Line Interface

The `consul kv` set of commands provides a quick way to interact with the KV store from your terminal.

```bash theme={null}
# Write or update a key
consul kv put app1/config/apikey 4fe20s12a02$23
# Read back the value
consul kv get app1/config/apikey
# Delete the key
consul kv delete app1/config/apikey
# Output: Success! Data deleted at key: app1/config/apikey
```

| Subcommand | Action                       |
| ---------- | ---------------------------- |
| `put`      | Create or update a key       |
| `get`      | Retrieve the plaintext value |
| `delete`   | Remove a key and its data    |

Consult the [Consul CLI documentation](https://www.consul.io/docs/commands/kv) for additional flags and examples.

***

## 3. Consul Web UI

The Consul UI provides a visual way to browse and modify KV entries.

1. Log in to your Consul cluster.
2. Click on the **Key/Value** tab in the top navigation.
3. Drill down through key prefixes to locate your entry.
4. Click on a key to view or edit its value in JSON, YAML, or HCL format.

<Frame>
  ![The image is a screenshot of a user interface for accessing a key/value store, highlighting the key name, key value, and options to view data in different formats. It includes labeled annotations and a cartoon character in the bottom right corner.](https://kodekloud.com/kk-media/image/upload/v1752877775/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Interacting-with-Consul-KV/key-value-store-ui-screenshot.jpg)
</Frame>

***

## 4. Limiting Access with ACLs

By default, Consul’s KV store is open to all clients. To enforce security:

1. Enable ACLs in your Consul configuration.
2. Bootstrap an ACL management token.
3. Create policies that grant read/write permissions on specific key prefixes.
4. Distribute tokens to users or applications.

<Callout icon="triangle-alert">
  Once ACLs are enabled, all API, CLI, and UI requests require a valid token. Plan your migration and token distribution carefully.
</Callout>

For a deep dive, see the [Consul ACL guide](https://www.consul.io/docs/security/acl).

***

## Links and References

* [Consul Key/Value HTTP API](https://www.consul.io/api-docs/kv)
* [Consul CLI Commands: `kv`](https://www.consul.io/docs/commands/kv)
* [Consul Web UI Overview](https://www.consul.io/docs/ui)
* [Consul ACL Security](https://www.consul.io/docs/security/acl)
* [HashiCorp Consul Documentation](https://www.consul.io/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/70a7eb0f-aec7-41aa-b417-398c341698b6/lesson/ca2bd73a-7f10-4da4-8839-a2e82b26b618" />
</CardGroup>


# Introduction to Consul KV Store

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Access-the-Consul-KeyValue-KV/Introduction-to-Consul-KV-Store/page

The Consul Key/Value Store is a centralized repository for storing configuration parameters, metadata, and arbitrary data objects with high availability and fault tolerance.

The Consul Key/Value (KV) Store is a centralized repository for storing configuration parameters, metadata, and arbitrary data objects. Built into Consul, it’s always enabled and ready for use, although leveraging it remains optional. Data is replicated across all server nodes—voters, non-voters, and read replicas—ensuring high availability and fault tolerance.

<Frame>
  ![The image is an informational slide about a centralized Key/Value store, explaining its features and use cases, particularly in storing configuration parameters and metadata. It highlights its distributed architecture, installation with Consul, and accessibility by server and client agents.](https://kodekloud.com/kk-media/image/upload/v1752877777/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Introduction-to-Consul-KV-Store/centralized-key-value-store-features.jpg)
</Frame>

## Distributed Architecture and High Availability

* Replicates data across all Consul server nodes (voting, non-voting, read replicas)
* Maintains redundancy even if one or more nodes fail
* Accessible by server and client agents, as well as external clients with a valid ACL token (when ACLs are enabled)

<Callout icon="lightbulb">
  Consul KV Store is designed strictly for key/value operations, not as a full database or file system.
</Callout>

## What the Consul KV Store Is Not

<Frame>
  ![The image explains what a Key/Value store is not, highlighting that it is not a full-featured database, not encrypted, lacks a directory structure, and is stored in a single datacenter without replication.](https://kodekloud.com/kk-media/image/upload/v1752877778/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Introduction-to-Consul-KV-Store/key-value-store-not-full-database.jpg)
</Frame>

| Limitation                    | Explanation                                                            |
| ----------------------------- | ---------------------------------------------------------------------- |
| Not a full database           | Lacks complex queries and advanced features (e.g., DynamoDB)           |
| Not encrypted by default      | Stored in plaintext—use Vault for sensitive data                       |
| No directory hierarchy        | Forward slashes (`/`) in keys are part of the name, not actual folders |
| Single-datacenter replication | Replicates only within one datacenter, not across regions              |

<Callout icon="triangle-alert">
  Consul KV Store data is *not* encrypted by default. For secrets and sensitive information, use [HashiCorp Vault](https://www.vaultproject.io).
</Callout>

## Object Size Limitation

Each key/value object is limited to **512 KB**.

<Frame>
  ![The image provides additional information about Consul K/V, highlighting an object size limitation of 512KB and backup and recovery options using the consul snapshot save command and Consul snapshot agent for Enterprise.](https://kodekloud.com/kk-media/image/upload/v1752877779/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Introduction-to-Consul-KV-Store/consul-kv-size-limit-backup-recovery.jpg)
</Frame>

## Backup and Recovery

Consul supports snapshot-based backup and restore for KV data:

```bash theme={null}
