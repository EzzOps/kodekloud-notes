# 1. Add the database host
consul kv put apps/eCommerce/database_host customer_db

# 2. Add the database name
consul kv put apps/eCommerce/database billing

# 3. Add the connection string
consul kv put apps/eCommerce/connection_string 'Server=myServerAddress;Database=myDataBase;Uid=myUsername;Pwd=myPassword;'
```

Each command will return a confirmation similar to:

```text theme={null}
Success! Data written to: apps/eCommerce/database_host
```

***

## 3. Deleting an Entry

If you need to remove a key, use `consul kv delete`. For example, to delete the connection string:

```bash theme={null}
consul kv delete apps/eCommerce/connection_string
```

Successful deletion yields:

```text theme={null}
Success! Deleted key: apps/eCommerce/connection_string
```

***

## 4. Adding Data for the Search Service

Next, create configuration entries for a hypothetical search service:

```bash theme={null}
# Store the current version
consul kv put apps/search/version 4

# Store the service URL
consul kv put apps/search/url search.service.consul
```

Refresh the UI to verify new keys under **apps → search**.

> **lightbulb** If you don’t see the new entries right away, click the **Refresh** button in the UI or clear your browser cache.

***

## 5. Querying Data in the CLI

Retrieve a value directly from the CLI:

```bash theme={null}
consul kv get apps/search/url
```

Output:

```text theme={null}
search.service.consul
```

***

## 6. Querying Data via the HTTP API

Consul’s HTTP API returns values in Base64. First, inspect the raw JSON:

```bash theme={null}
curl -s http://127.0.0.1:8500/v1/kv/apps/search/url | jq
```

Sample response:

```json theme={null}
[
  {
    "LockIndex": 0,
    "Key": "apps/search/url",
    "Flags": 0,
    "Value": "c2VhcmNoLnNlcnZpY2UuY29uc3Vs",
    "Namespace": "default",
    "CreateIndex": 2359,
    "ModifyIndex": 2359
  }
]
```

To decode in one step:

```bash theme={null}
curl -s http://127.0.0.1:8500/v1/kv/apps/search/url \
  | jq -r '.[0].Value' \
  | base64 --decode
```

Output:

```text theme={null}
search.service.consul
```

> **lightbulb** Any application using Consul’s K/V HTTP API must Base64-decode the `Value` field before use.

***

## 7. Operation Summary

| Operation     | CLI Command                   | API Endpoint                       |
| ------------- | ----------------------------- | ---------------------------------- |
| Add Key       | `consul kv put <key> <value>` | POST `/v1/kv/:key`                 |
| Delete Key    | `consul kv delete <key>`      | DELETE `/v1/kv/:key`               |
| Get Key (CLI) | `consul kv get <key>`         | —                                  |
| Get Key (API) | —                             | GET `/v1/kv/:key` (Base64-encoded) |

***

## 8. Further Reading

* [Consul K/V Store Overview](https://www.consul.io/docs/agent/kv)
* [Consul HTTP API Reference](https://www.consul.io/api-docs/kv)
* [Installing Consul](https://www.consul.io/docs/install)

You’ve now mastered adding, deleting, and retrieving key/value pairs in Consul using the UI, CLI, and HTTP API. Happy configuring!

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/70a7eb0f-aec7-41aa-b417-398c341698b6/lesson/8daa6274-68ef-4e26-8a1b-41643814b399)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/70a7eb0f-aec7-41aa-b417-398c341698b6/lesson/0859eaa2-247a-4a8f-ba16-f748e256a817)


# Interacting with Consul KV

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Access-the-Consul-KeyValue-KV/Interacting-with-Consul-KV/page

This article explains how to interact with Consuls key/value store using HTTP API, command-line interface, and web UI.

Consul’s key/value (KV) store lets you centrally manage configuration data, feature flags, and more. You can interact with the KV store in three ways:

| Interface    | Description                               | Ideal For                      |
| ------------ | ----------------------------------------- | ------------------------------ |
| HTTP API     | Perform CRUD operations over HTTP         | Applications, automation, SDKs |
| Command-Line | `consul kv` subcommands for KV management | Administrators, scripts        |
| Web UI       | Browser-based view and edit               | Exploratory or ad hoc changes  |

Below, we’ll explore each interface in detail.

***

## 1. Consul KV HTTP API

The HTTP API exposes a `/v1/kv` endpoint. Use standard HTTP verbs (`PUT`, `GET`, `DELETE`) to manage keys.

### 1.1 Writing a Key (`PUT`)

```bash theme={null}
curl --request PUT \
     --data 'enabled' \
     https://consul.example.com:8500/v1/kv/data/app4
