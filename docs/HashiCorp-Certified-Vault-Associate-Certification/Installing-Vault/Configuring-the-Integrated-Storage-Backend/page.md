# Configuring the Integrated Storage Backend

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Installing-Vault/Configuring-the-Integrated-Storage-Backend/page

Integrate Vault storage using Raft protocol for high availability without external dependencies, simplifying operations and ensuring data replication across nodes.

Integrate Vault storage using the built-in Raft consensus protocol for a high-availability cluster without external dependencies like Consul. This approach simplifies operations, reduces network hops, and ensures every node holds a complete data replica.

## Why Choose Integrated Storage (Raft)

<Frame>
  ![Deploying the Integrated Storage Backend](https://kodekloud.com/kk-media/image/upload/v1752878150/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Configuring-the-Integrated-Storage-Backend/deploying-integrated-storage-backend-vault.jpg)
</Frame>

* **Raft Protocol**: Leader election and data replication ported from Consul directly into Vault.
* **High Availability**: A 3–5 node cluster tolerates up to two node failures, since each node holds a full data copy.
* **Simplified Operations**: No separate Consul cluster to provision, monitor, or troubleshoot.
* **Built-in Snapshots**: Automated data retention snapshots; Enterprise users can leverage the Vault 1.6+ snapshot agent.
* **Official Support**: HashiCorp fully supports both Integrated Storage (Raft) and Consul backends in Enterprise.

## Deployment Topology

This diagram shows five Vault nodes (A–E) forming a Raft cluster communicating over TCP port 8201:

<Frame>
  ![Network Diagram: Vault Integrated Storage Cluster](https://kodekloud.com/kk-media/image/upload/v1752878151/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Configuring-the-Integrated-Storage-Backend/network-diagram-vault-nodes-storage.jpg)
</Frame>

| Component  | Description                            |
| ---------- | -------------------------------------- |
| Nodes A–E  | Vault servers forming the Raft cluster |
| Port 8201  | Inter-node Raft communication          |
| Local Disk | Persists replicated Vault data         |

## Vault Configuration Example

Below is a sample HCL file for a Vault node with integrated storage. Make sure each `node_id` is unique across the cluster:

```hcl theme={null}
storage "raft" {
  path    = "/opt/vault/data"
  node_id = "node-a-us-east-1.example.com"
  retry_join {
    auto_join = "provider=aws region=us-east-1 tag_key=vault tag_value=us-east-1"
  }
}

listener "tcp" {
  address                  = "0.0.0.0:8200"
  cluster_address          = "0.0.0.0:8201"
  tls_disable              = false
  tls_cert_file            = "/etc/vault.d/client.pem"
  tls_key_file             = "/etc/vault.d/cert.key"
  tls_disable_client_certs = true
}

seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "12345678-abcd-1234-abcd-123456789101"
  endpoint   = "example.kms.us-east-1.vpce.amazonaws.com"
}
