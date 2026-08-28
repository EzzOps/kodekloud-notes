# 1. Create a token scoped to "web-app"
vault token create -policy="web-app" -format=json \
  | jq -r ".auth.client_token" > token.txt

# 2. Log in with the new token
vault login "$(cat token.txt)"

# 3. Verify read access (should succeed)
vault kv get secret/api/key/google

# 4. Verify write access is denied (should fail)
vault kv put secret/api/key/google key="ABCDE12345"

# 5. Verify AWS credentials issuance (should succeed)
vault read aws/creds/s3-readonly
```

<Callout icon="triangle-alert">
  Always test both allowed and denied operations. Overprovisioned policies can lead to security risks.
</Callout>

***

## Writing Administrative Policies

Vault operators need permissions to manage core system paths under `sys/`. Below is an example HCL policy granting common operator capabilities:

```hcl theme={null}
# Manage License
path "sys/license" {
  capabilities = ["read", "list", "create", "update", "delete"]
}

# Initialize Vault
path "sys/init" {
  capabilities = ["read", "create", "update"]
}

# Configure the UI
path "sys/config/ui" {
  capabilities = ["read", "list", "update", "delete", "sudo"]
}

# Rekey and Unseal Keys
path "sys/rekey/*" {
  capabilities = ["read", "list", "update", "delete"]
}

# Rotate the Master Key
path "sys/rotate" {
  capabilities = ["update", "sudo"]
}

# Seal the Vault
path "sys/seal" {
  capabilities = ["sudo"]
}
```

### Key Points

* **Capabilities**
  * `read`, `list`, `create`, `update`, `delete`: Standard operations.
  * `sudo`: Grants access to root-protected endpoints (use sparingly).

* **Least Privilege**\
  Only include the paths and capabilities that each operator role truly requires.

***

## Links and References

* [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
* [Vault CLI Reference](https://www.vaultproject.io/docs/commands)
* [Vault Policy Management](https://www.vaultproject.io/docs/concepts/policies)
* [Terraform Vault Provider Registry](https://registry.terraform.io/providers/hashicorp/vault/latest)
* [jq Manual](https://stedolan.github.io/jq/manual/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/83a61f63-3f1f-436c-8aa3-e972b099eeec/lesson/8e53f231-10d5-472a-a37f-99b72974b689" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/83a61f63-3f1f-436c-8aa3-e972b099eeec/lesson/77addfcc-3dee-4a61-a241-bdf03488c60b" />
</CardGroup>


# Configuring the Consul Storage Backend

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Installing-Vault/Configuring-the-Consul-Storage-Backend/page

This guide explains how to configure HashiCorp Vault to use Consul as its storage backend for reliable data management.

In this guide, you’ll learn how to set up HashiCorp Vault to use Consul as its storage backend. Consul delivers a durable, highly available key–value store that scales independently, ensuring Vault’s data is stored reliably across clusters.

## Why Choose Consul for Vault Storage

Consul offers robust features that enhance Vault’s resilience and scalability:

| Feature              | Benefit                      | Details                                                           |
| -------------------- | ---------------------------- | ----------------------------------------------------------------- |
| Durable KV Storage   | High availability            | Replicates data across 3–5 voting members for automatic failover. |
| Independent Scaling  | Flexible capacity management | Scale Consul CPU and memory separately from Vault instances.      |
| Built-in Integration | Service discovery & health   | Vault registers itself in Consul for health checks and topology.  |
| Automated Snapshots  | Simplified backups           | Create snapshots for backup and upgrades with minimal downtime.   |
| Enterprise Support   | Official HashiCorp support   | Fully supported as a Vault backend in enterprise environments.    |

<Callout icon="lightbulb">
  Running a dedicated Consul cluster adds maintenance overhead—setup, ACLs, upgrades, and monitoring. However, with proper automation, it operates with minimal intervention.
</Callout>

## Cluster Topology

* One Vault cluster ↔ One Consul cluster (no cross–data-center mixing)
* Odd number of nodes (3 or 5) ensures reliable leader election
* Leader nodes accept commits and replicate logs to followers

## Dedicated Consul Cluster for Vault

To prevent resource contention and maintain performance, host Vault storage on a dedicated Consul cluster. Do not co-locate service discovery or mesh workloads on the same cluster.

## AWS Deployment Example

<Frame>
  ![The image illustrates the deployment of the Consul storage backend across three availability zones within a VPC, each containing a private subnet. It highlights a special installation of Consul using redundancy zones.](https://kodekloud.com/kk-media/image/upload/v1752878148/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Configuring-the-Consul-Storage-Backend/consul-storage-backend-deployment-vpc.jpg)
</Frame>

Distribute Vault and Consul nodes across multiple Availability Zones (AZs) in a VPC:

* **Vault servers** deployed in each AZ for redundancy
* **Consul servers** in each AZ, using enterprise Redundancy Zones

Even if an entire AZ becomes unavailable, both Consul and Vault remain operational.

## Vault Nodes & Local Consul Agents

Vault servers run a local Consul agent in client mode. Each agent joins the cluster and handles all API requests, so Vault always points to localhost:

<Frame>
  ![The image illustrates the deployment of a Consul storage backend with three Vault nodes, each communicating with a local Consul agent, connected to a Consul cluster.](https://kodekloud.com/kk-media/image/upload/v1752878149/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Configuring-the-Consul-Storage-Backend/consul-storage-backend-vault-nodes-deployment.jpg)
</Frame>

This model removes the need to update Vault’s configuration when the Consul cluster membership changes.

## Vault Configuration Example

Below is a sample HCL configuration for Vault using Consul as the storage backend:

```hcl theme={null}
storage "consul" {
  address = "127.0.0.1:8500"        # Consul API endpoint
  path    = "vault/"               # KV prefix for Vault data
  token   = "1a2b3c4d-1234-abdc-1234-1a2b3c4d5e6a"  # ACL token
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

api_addr     = "https://vault-us-east-1.example.com:8200"
cluster_addr = "https://node-a-us-east-1.example.com:8201"
cluster_name = "vault-prod-us-east-1"
ui           = true
log_level    = "INFO"
```

<Callout icon="triangle-alert">
  Ensure the Consul ACL token has permissions scoped only to the `vault/` path. Rotate tokens periodically to maintain security.
</Callout>

## Consul Server Configuration Example

Place the following JSON in `/etc/consul.d/server.json` on each Consul server node:

```json theme={null}
{
  "log_level": "INFO",
  "server": true,
  "ui": true,
  "data_dir": "/opt/consul/data",
  "bootstrap_expect": 5,
  "encrypt": "xxxxxxxxxxxxxx",
  "retry_join": [
    "provider=aws tag_key=Environment-Name tag_value=consul-cluster region=us-east-1"
  ],
  "leave_on_terminate": true,
  "enable_syslog": true,
  "bind_addr": "10.11.11.11",
  "advertise_addr": "10.11.11.11",
  "client_addr": "0.0.0.0",
  "datacenter": "us-east-1",
  "acl": {
    "enabled": true,
    "default_policy": "deny",
    "down_policy": "extend-cache",
    "tokens": {
      "agent": "xxxxxxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  },
  "key_file": "/etc/consul.d/cert.key",
  "cert_file": "/etc/consul.d/client.pem",
  "ca_file": "/etc/consul.d/chain.pem",
  "verify_incoming": true,
  "verify_outgoing": true,
  "verify_server_hostname": true
}
```

Customize addresses, data directories, and ACL tokens to fit your environment.

## Further Reading

* [Vault Storage Backends](https://www.vaultproject.io/docs/configuration/storage)
* [Consul Storage Backend](https://www.vaultproject.io/docs/configuration/storage/consul)
* [HashiCorp Consul GitHub Course](https://github.com/btkrausen/HashiCorp)

Use available coupons to get started with Consul and Vault today!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/a5a3d715-00ac-4573-aa63-061912aafce2/lesson/e7e944a2-5b70-407b-80c2-e505d93e3725" />
</CardGroup>
