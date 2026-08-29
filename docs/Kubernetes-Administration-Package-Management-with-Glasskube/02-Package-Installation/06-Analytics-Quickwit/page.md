# Analytics Quickwit

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Package-Installation/Analytics-Quickwit/page

Guide to installing and configuring Quickwit search and analytics as a namespaced Glasskube package, covering S3 storage setup, deployment steps, and verifying the web UI

Welcome back.

This lesson covers Quickwit — a high-performance, cloud-object-storage-optimized search and analytics engine — and shows how to install it as a namespaced package with Glasskube. We'll explain what Quickwit is, which values you must configure, how to prepare your cluster (namespace), and how to deploy and verify Quickwit using Glasskube.

Quickwit is designed for fast, scalable search and analytics over large datasets by leveraging an optimized file format and intelligent scheduling. It externalizes data to S3 or S3-compatible object stores for cost-effective, scalable storage.

<Frame>
  <img alt="The image shows a diagram of a single-node Kubernetes cluster with components divided into &#x22;Cluster Scoped&#x22; and &#x22;Namespace Scoped&#x22; categories, including database, observability, continuous deployment, and analytics tools." />
</Frame>

## Package overview

* Scope: Namespace-scoped package (Quickwit requires an existing namespace).
* Configuration: Several values must be supplied (see Required values).
* UI: Quickwit exposes a web-based UI (Glasskube provides an entry point to open it).
* Dependencies: None — Glasskube will not install additional packages for Quickwit.

<Frame>
  <img alt="The image describes features of a sub-second search and analytics engine on cloud storage, highlighting attributes like &#x22;Namespace scoped,&#x22; &#x22;Multiple value definitions,&#x22; &#x22;Has an entry point,&#x22; and &#x22;No dependencies.&#x22;" />
</Frame>

## Architecture and storage

Quickwit deploys a small set of components into the target namespace (indexer, searcher, janitor, control plane, metastore). A core design decision is that Quickwit externalizes object storage: indexes and metadata are stored in S3 or an S3-compatible object store. This approach enables high scalability and cost-efficient analytics at scale.

<Frame>
  <img alt="The image illustrates a single-node cluster structure for a Kubernetes setup, showcasing components like analytics, a database cluster, and connections to external object storage." />
</Frame>

## Required values (high level)

For most installations (including the demo) you will supply the following core values:

| Value               | Purpose                                                                  | Example                                    |
| ------------------- | ------------------------------------------------------------------------ | ------------------------------------------ |
| `defaultIndexUri`   | S3 URI used as the default index storage location                        | `s3://quickwit-indexes`                    |
| `metastoreUri`      | Metastore URI (can point to the same S3 bucket as the index)             | `s3://quickwit-indexes`                    |
| `s3AccessKeyId`     | S3 access key ID (or temporary/IAM-backed credentials)                   | `AKIA...`                                  |
| `s3SecretAccessKey` | S3 secret access key                                                     | `[AWS_SECRET_ACCESS_KEY]` |
| `s3Region`          | AWS region for the S3 bucket (or region for your S3-compatible provider) | `us-east-1`                                |

Optional values commonly used:

* `s3Endpoint` — set for non-AWS S3-compatible endpoints (e.g., MinIO, Ceph).
* `s3Flavor` — choose the S3 flavor if your provider requires special handling.
* Custom Quickwit domain or ingress settings for production-grade exposure.

Glasskube’s Configure button for namespaced packages lets you supply these values before installation and edit them later.

<Callout icon="lightbulb">
  You must create the target namespace in your cluster before installing a namespaced package like Quickwit. Glasskube does not auto-create the namespace for you.
</Callout>

<Callout icon="warning">
  Treat S3 credentials as secrets. Do not commit access keys to version control. In production, prefer IAM roles, temporary credentials, or Kubernetes secrets referenced by the package configuration.
</Callout>

## Quickwit quickstart (local / binary / Docker)

You can validate Quickwit locally before deploying to Kubernetes.

Install or check the binary:

```bash theme={null}
