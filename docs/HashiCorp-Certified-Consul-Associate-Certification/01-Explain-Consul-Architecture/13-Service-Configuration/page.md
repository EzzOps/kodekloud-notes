# Service Configuration

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Explain-Consul-Architecture/Service-Configuration/page

This article explores using Consuls distributed Key/Value store for dynamic service configuration, ensuring redundancy and high availability for application settings.

In this lesson, we’ll explore how to leverage Consul’s distributed Key/Value (K/V) store for dynamic service configuration. Consul automatically replicates all K/V data across every server in the cluster, delivering redundancy and high availability for your application settings.

## Consul K/V Store: At a Glance

| Feature                  | Description                                                                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| Distributed & Replicated | Every write is propagated to all Consul servers, ensuring consistency across the cluster.                                            |
| Flexible Storage         | Store any configuration data—strings, JSON blobs, or serialized objects (≤512 KB per key).                                           |
| Versioning & Atomic Ops  | Supports atomic Compare-and-Set (CAS) operations and optimistic locking.                                                             |
| Not a Full Data Store    | Designed for configuration and service discovery, not high-throughput persistence like [DynamoDB](https://aws.amazon.com/dynamodb/). |

<Callout icon="triangle-alert">
  Always enable ACLs to restrict access to your K/V data. Without proper ACLs, unauthorized users could browse or delete critical entries.
</Callout>

## Accessing the K/V Store

You can interact with Consul’s K/V store in several ways:

| Method   | Usage Example                                        |
| -------- | ---------------------------------------------------- |
| CLI      | `consul kv put key value`                            |
| HTTP API | `curl --request PUT http://localhost:8500/v1/kv/key` |
| Web UI   | Navigate to **Key/Value** in the Consul dashboard    |

## Key/Value Hierarchies & Limits

* **Flat Namespace**: Keys are simple strings; forward slashes (`/`) only emulate folders (e.g., `app/config/db/connection_string`).
* **Size Limit**: Each value ▶ 512 KB.
* **Any Object Type**: Store text, JSON, or serialized binaries, up to the size cap.

## Example: Managing Application Parameters

Suppose you have a “training” application deployed by a CI/CD pipeline (Jenkins, CircleCI, GitLab CI, etc.). You need to supply:

* Database connection string
* Application version
* Database name
* Database table name

First, store these in Consul:

```bash theme={null}
