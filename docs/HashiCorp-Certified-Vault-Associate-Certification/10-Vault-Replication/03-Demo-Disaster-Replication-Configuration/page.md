# Demo Disaster Replication Configuration

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Vault-Replication/Demo-Disaster-Replication-Configuration/page

This guide explains how to enable and configure performance replication in Vault Enterprise for active-active read scalability across multiple clusters.

In this guide, you’ll learn how to enable and configure **performance replication** in Vault Enterprise. Performance replication lets you distribute Vault policies, secrets engines, authentication methods, and audit configurations across multiple clusters for active-active read scalability, while routing write operations to a single primary.

<Frame>
  ![The image is an introduction to performance replication, explaining its features such as replicating configurations and servicing client read requests. It includes a diagram showing the relationship between a primary and secondary cluster, with Vault clients interacting with them.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878264/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Demo-Disaster-Replication-Configuration/performance-replication-introduction-diagram.jpg)
</Frame>

## Key Concepts

* **Active-Active Workloads**: Read operations (authentication, secret reads, dynamic secret generation) are served locally on each replica.
* **Centralized Writes**: All write requests (policy changes, configuration updates) are forwarded to the primary cluster.
* **Independent Authentication**: Tokens and leases created on a performance secondary are local and are *not* replicated from the primary. Clients must re-authenticate on each cluster.

## Performance vs. Disaster Recovery (DR) Replication

| Feature                | Performance Replication          | DR Replication                 |
| ---------------------- | -------------------------------- | ------------------------------ |
| Policies & Config      | ✓                                | ✗                              |
| Secrets Engines & Auth | ✓                                | ✗                              |
| Audit Configurations   | ✓                                | ✗                              |
| Tokens & Leases        | ✗                                | ✓                              |
| Use Case               | Active-active, low-latency reads | Failover and disaster recovery |
| Write Path             | Forwarded to primary             | Forwarded to primary           |

<Frame>
  ![The image is a diagram comparing performance and disaster recovery (DR) replication in a system with three clusters: Perf Secondary, Primary, and DR Secondary. It shows the flow of replicated data, including Vault Policies, Secrets Engines, Auth Methods, Audit Configurations, Tokens, and Leases.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878265/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Demo-Disaster-Replication-Configuration/performance-disaster-recovery-diagram.jpg)
</Frame>

## Example Architecture: Data Centers & Cloud Regions

### Multi–Data Center Deployment

A primary cluster in **Data Center A** replicates to performance secondaries in **Data Center B** and a **cloud region**. Local applications read and authenticate against their nearest replica, while writes go to the primary.

<Frame>
  ![The image illustrates a replication architecture with a primary cluster in Data Center A, connected to performance replication clusters in both Data Center B and a cloud region. It includes a certification badge and a cartoon character at the bottom.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878266/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Demo-Disaster-Replication-Configuration/replication-architecture-data-centers-cloud.jpg)
</Frame>

### Global Cloud Deployment

In a cloud setup, the primary (US-East2) replicates to secondaries in US-East and EU-West. Applications in each region authenticate to their local replica for reads; writes are sent back to the primary and propagated.

<Frame>
  ![The image illustrates application communication across three cloud regions (US-East, US-East2, and EU-West) with performance replication clusters and local apps interacting with local vault clusters.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878267/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Demo-Disaster-Replication-Configuration/application-communication-cloud-regions-diagram.jpg)
</Frame>

## How Performance Replication Works

1. **Active-Active Authentication**\
   Each performance replica handles logins locally. Tokens and leases exist only on the cluster where they were issued.

2. **Local Dynamic Secrets**\
   Replicas generate dynamic credentials (e.g., database passwords, AWS keys) without contacting the primary:

<Frame>
  ![The image is a slide about "Performance Replication," explaining an active/active solution for applications in multiple data centers, with details on authentication and failover processes. It includes a Vault certification badge.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878269/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Demo-Disaster-Replication-Configuration/performance-replication-active-active-slide.jpg)
</Frame>

<Frame>
  ![The image is a slide about "Performance Replication" in Vault, explaining how replicated clusters handle secrets and dynamic credentials locally, offloading some operations from the primary cluster. It also notes that write requests are forwarded to the primary cluster.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878270/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Demo-Disaster-Replication-Configuration/performance-replication-vault-clusters-slide.jpg)
</Frame>

3. **External Service Interactions**\
   Connections to AWS, databases, and other external services occur directly from each replica:

<Frame>
  ![The image illustrates a diagram of interaction with external services, showing a primary cluster and a performance replication cluster connecting to AWS and a database, with indications of needing database and AWS credentials.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878271/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Demo-Disaster-Replication-Configuration/external-services-interaction-diagram.jpg)
</Frame>

## Setup Process

Follow these four steps to configure performance replication:

<Frame>
  ![The image is a flowchart illustrating the setup process for a system, involving four steps: activating the primary, fetching a secondary token, activating the secondary, and replication. It includes brief descriptions for each step and features a Vault certification badge.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878273/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Demo-Disaster-Replication-Configuration/system-setup-flowchart-four-steps.jpg)
</Frame>

1. Enable performance replication on the primary.
2. Generate a secondary token.
3. Enable the secondary using the token.
4. Monitor the replication status.

### CLI Commands

```bash theme={null}
