# Default path: "approle"
vault auth enable approle

# Custom path: "hcvop"
vault auth enable -path=hcvop approle
```

### 2. Create a Role

```bash theme={null}
vault write auth/approle/role/hcvop \
  token_policies=web-app \
  token_ttl=1h \
  token_max_ttl=24h \
  secret_id_ttl=24h \
  token_bound_cidrs="10.1.16.0/16" \
  token_type=batch
```

### 3. View Role Configuration

```bash theme={null}
vault read auth/approle/role/hcvop
```

Sample output:

```text theme={null}
Key                    Value
---                    -----
token_policies         [web-app]
token_ttl              1h
token_max_ttl          24h
secret_id_ttl          24h
token_bound_cidrs      [10.1.16.0/16]
token_type             batch
```

### 4. Retrieve the Role ID

```bash theme={null}
vault read auth/approle/role/hcvop/role-id
```

```text theme={null}
Key     Value
---     -----
role_id 22549d0d-147a-d6e2-fa2e-9cedd3b20977
```

### 5. Generate a Secret ID

> **triangle-alert** `secret_id` is sensitive. Store or wrap it securely and avoid long-lived exposure.

```bash theme={null}
vault write -f auth/approle/role/hcvop/secret-id
```

```text theme={null}
Key                Value
---                -----
secret_id          0514b3b1-e1ce-2741-0b57-ef836c29c7d3
secret_id_accessor da025e1f-7247-1888-218c-37382d31e98e
secret_id_ttl      24h
```

### 6. Authenticate with AppRole (CLI)

```bash theme={null}
vault write auth/approle/login \
  role_id=22549d0d-147a-d6e2-fa2e-9cedd3b20977 \
  secret_id=0514b3b1-e1ce-2741-0b57-ef836c29c7d3
```

Sample response:

```text theme={null}
Key                   Value
---                   -----
token                 hvs.CAESIGjTXNY...
token_accessor        KmRLXSRBozhXo...
token_duration        24h
token_renewable       true
token_policies        ["default" "web-app"]
token_meta_role_name  hcvop
```

### 7. Authenticate with AppRole (HTTP API)

```bash theme={null}
curl --request POST \
     --data '{"role_id":"22549d0d-147a-d6e2-fa2e-9cedd3b20977","secret_id":"0514b3b1-e1ce-2741-0b57-ef836c29c7d3"}' \
     https://vault.example.com:8200/v1/auth/approle/login | jq .
```

Sample JSON:

```json theme={null}
{
  "auth": {
    "client_token": "hvs.CAESIIJoCqiCpci...",
    "policies": ["default","web-app"],
    "metadata": {"role_name":"hcvop"},
    "lease_duration": 2764800,
    "renewable": true,
    "token_type": "service"
  }
}
```

Extract only the token:

```bash theme={null}
curl --request POST \
     --data '{"role_id":"...","secret_id":"..."}' \
     https://vault.example.com:8200/v1/auth/approle/login \
  | jq -r '.auth.client_token'
```

***

That concludes the AppRole auth method guide. For human-centric authentication, explore the [Userpass auth method](https://www.vaultproject.io/docs/auth/userpass).

## Links and References

* [Vault AppRole Documentation](https://www.vaultproject.io/docs/auth/approle)
* [HashiCorp Vault Concepts](https://www.vaultproject.io/docs/concepts)
* [jq Manual](https://stedolan.github.io/jq/)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/8dc0af78-c47f-4f35-83c0-f5eafa95f7f6)


# Auto Unsealing Vault

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Auto-Unsealing-Vault/page

This guide covers Vaults auto-unseal feature, its mechanisms, configuration, migration strategies, and design considerations for simplifying the unsealing process.

Vault’s auto-unseal feature streamlines the unsealing process by replacing manual Shamir key entry with cloud-based key management services (KMS). This guide covers how auto-unseal works, supported mechanisms, configuration examples, migration strategies, and design considerations.

## What Is Auto-Unseal?

By default, Vault uses Shamir’s Secret Sharing to protect its master key. Administrators must supply a threshold of unseal key shares (e.g., 3 out of 5) each time Vault starts. Auto-unseal simplifies this by delegating master key encryption and decryption to a trusted cloud KMS. When Vault launches, it contacts the configured KMS to decrypt the master key, avoiding manual key entry.

![The image explains "Auto Unseal," highlighting the use of a trusted cloud-based key instead of shared keys to protect the master key, with a diagram showing an encryption key and encrypted data.](https://kodekloud.com/kk-media/image/upload/v1752878384/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Auto-Unsealing-Vault/auto-unseal-cloud-key-diagram.jpg)

Vault’s data encryption key encrypts all backend data (Raft, Consul, S3, etc.). Under auto-unseal, the master key protecting the data key is encrypted by the cloud KMS instead of Shamir shards.

![The image explains "Auto Unseal," showing a process where a cloud-based key protects a master key, which then secures an encryption key for encrypted data in a storage backend.](https://kodekloud.com/kk-media/image/upload/v1752878385/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Auto-Unsealing-Vault/auto-unseal-cloud-key-encryption-process.jpg)

## Supported Auto-Unseal Mechanisms

Vault natively integrates with multiple cloud KMS providers and on-prem HSMs:

![The image lists supported auto unseal mechanisms for Vault, including AWS KMS, Azure Key Vault, GCP Cloud KMS, AliCloud KMS, OCI KMS, and HSM (Enterprise Only), with a note about using the Transit Secrets Engine from another Vault cluster.](https://kodekloud.com/kk-media/image/upload/v1752878386/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Auto-Unsealing-Vault/vault-auto-unseal-mechanisms-list.jpg)

| Mechanism Type  | Provider        | Notes                                 |
| --------------- | --------------- | ------------------------------------- |
| AWS KMS         | AWS             | Regional or multi-Region keys†        |
| Azure Key Vault | Microsoft Azure | Managed identities supported          |
| GCP Cloud KMS   | Google Cloud    | Global or regional key rings          |
| AliCloud KMS    | Alibaba Cloud   | China region availability             |
| OCI KMS         | Oracle Cloud    | Enterprise tenancy support            |
| HSM             | On-premises     | PKCS#11, FIPS 140-2 (Enterprise Only) |
| Transit         | Vault cluster   | Use Transit Secrets Engine endpoint   |

† Regional key outage can affect unseal. See *Design Considerations*.

## How Auto-Unseal Works

1. You create a key (or HSM object) in your cloud KMS.
2. Configure Vault’s `seal` stanza with the KMS details.
3. On initialization, Vault encrypts its master key with the KMS key and stores the ciphertext under `core/master`.
4. At each startup, Vault automatically requests a decrypt operation from the KMS to recover the master key.

![The image explains how auto unseal works in Vault, highlighting that the master key is encrypted with a cloud-based key and stored on the backend, and it contrasts this with the Shamir method. It includes a Vault certification badge.](https://kodekloud.com/kk-media/image/upload/v1752878387/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Auto-Unsealing-Vault/auto-unseal-vault-explanation-diagram.jpg)

## Design Considerations

![The image outlines design considerations for Vault, including key rotation support, regional limitations of cloud-based KMS services, and health check features for auto-unseal operations. It also mentions periodic health checks and logging warnings if issues are detected.](https://kodekloud.com/kk-media/image/upload/v1752878389/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Auto-Unsealing-Vault/vault-design-considerations-key-rotation.jpg)

* **Key Rotation**

> **lightbulb** Vault supports automatic rotation of cloud-managed keys (e.g., AWS KMS annual rotation). Ensure Vault’s service account has decrypt permissions on new key versions.

* **Regional Outages**

> **triangle-alert** Some KMS providers are regional. A full-region outage can prevent Vault from unsealing. Consider multi-region keys or Transit auto-unseal for high availability.

* **Health Checks**\
  Vault pings the KMS every 10 minutes; on failure, it logs warnings and retries every minute. A loss of access only impacts restarts, not normal operations.

For on-premises or multi-region failover, you can import the same external key into multiple regions or use a Transit Secrets Engine in another Vault cluster.

## Enabling Auto-Unseal

Add a `seal` block to your Vault HCL configuration:

```hcl theme={null}
listener "tcp" {
  address         = "0.0.0.0:8200"
  cluster_address = "0.0.0.0:8201"
  tls_disable     = 0
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

Authentication methods:

* AWS: IAM instance role (preferred) or environment variables (\[AWS\_ACCESS\_KEY\_ID], \[AWS\_SECRET\_ACCESS\_KEY]).
* Azure: Managed identity or `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`.
* GCP: Service account JSON (`GOOGLE_APPLICATION_CREDENTIALS`) or instance default credentials.

### Example: Azure Key Vault

```hcl theme={null}
seal "azurekeyvault" {
  vault_name    = "vault-hashicorp"
  key_name      = "hashicorp-vault-key"
  tenant_id     = "8427464-8963-6422-example"
  client_id     = "03dc33fc-16d9-example"
  client_secret = "DKEMCI8…."
}
```

### Example: GCP Cloud KMS

```hcl theme={null}
seal "gcpckms" {
  project     = "vault-project"
  region      = "global"
  key_ring    = "hashicorp-vault-keyring"
  crypto_key  = "hashicorp-vault-key"
  credentials = "/usr/gcp.json"
}
```

### Auto-Unsealing with Transit

Use a highly available Vault cluster running the Transit Secrets Engine:

![The image illustrates the process of auto unsealing with a transit secrets engine in a Vault cluster, showing how an encryption key is used to unseal multiple clusters.](https://kodekloud.com/kk-media/image/upload/v1752878390/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Auto-Unsealing-Vault/auto-unsealing-transit-secrets-vault.jpg)

```hcl theme={null}
seal "transit" {
  address         = "https://vault.example.com:8200"
  token           = "s.Qf1s5zigZ40X6akYexample"
  key_name        = "auto-unseal-key"
  mount_path      = "/transit"
  tls_ca_cert     = "/etc/vault/ca.pem"
  tls_client_cert = "/etc/vault/client.pem"
  tls_client_key  = "/etc/vault/key.pem"
}
```

## Other Options

Vault Enterprise also provides:

* HSM integration via PKCS#11 (FIPS 140-2)
* AliCloud KMS
* Oracle Cloud Infrastructure KMS

![The image is a slide discussing options not covered, specifically HSM, AliCloud, and Oracle Cloud, with details on HSM integration and compliance. It includes a Vault certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878391/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Auto-Unsealing-Vault/hsm-alicloud-oracle-cloud-options-slide.jpg)

## Seal Migration

You can migrate between seal methods (e.g., Shamir ↔ AWS KMS) with minimal downtime. Vault must be restarted on each node.

![The image illustrates a migration process from a Vault Cluster using Shamir Keys to one with Auto Unseal, highlighting differences in unsealing methods and security features. It includes icons for AWS, Google Cloud, Azure, and HSM, indicating integration with these services.](https://kodekloud.com/kk-media/image/upload/v1752878392/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Auto-Unsealing-Vault/vault-migration-shamir-auto-unseal-diagram.jpg)

### Example: Shamir → AWS KMS

1. Add the AWS KMS `seal` stanza.
2. Restart Vault on a node:
   ```bash theme={null}
   systemctl restart vault.service
   ```
3. Monitor logs for migration mode:
   ```text theme={null}
   2022-12-25T10:47:09.295-0400 [WARN] core: entering seal migration mode; Vault will not automatically unseal even if using an autoseal: from_barrier_type=shamir to_barrier_type=awskms
   ```
4. Unseal with migration:
   ```bash theme={null}
   vault operator unseal -migrate
   ```
5. Verify status:
   ```text theme={null}
   Recovery Seal Type         shamir
   Sealed                     false
   Seal Migration in Progress true
   ```
6. Repeat on each node (Standby nodes → Leader).

![The image outlines the steps for "Shamir to Auto Unseal Migration" with a sequence of operations involving standby and leader nodes. It includes a diagram of nodes and a certification badge in the top right corner.](https://kodekloud.com/kk-media/image/upload/v1752878394/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Auto-Unsealing-Vault/shamir-auto-unseal-migration-diagram.jpg)

### Example: Auto-Unseal → Shamir Keys

1. Add `disabled = true` to the active seal stanza.
2. Restart Vault and run:
   ```bash theme={null}
   vault operator unseal -migrate
   ```
3. Apply across all nodes.

![The image illustrates the migration process from an auto unseal Vault cluster to a Shamir keys Vault cluster, highlighting features and differences between the two methods.](https://kodekloud.com/kk-media/image/upload/v1752878395/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Auto-Unsealing-Vault/vault-migration-auto-unseal-shamir-keys.jpg)

### Example: Rotating Auto-Unseal Keys

Rotate from one KMS key to another:

```hcl theme={null}
seal "awskms" {
  disabled   = true
  region     = "us-east-1"
  kms_key_id = "12345678-abcd-1234-abcd-123456789101"
}

seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "98765432-dcba-4321-dcba-10987654321"
}
```

1. Restart Vault and run `vault operator unseal -migrate` with recovery keys.
2. Repeat on each node.

![The image is a slide about "Seal Migration," explaining that migrating from one seal type to another requires downtime for Vault and is not frequently performed. It includes examples of migrations like Shamir to AWS KMS and GCP Cloud KMS to Azure Key Vault.](https://kodekloud.com/kk-media/image/upload/v1752878396/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Auto-Unsealing-Vault/seal-migration-downtime-examples.jpg)

***

## Links and References

* [Vault Auto-Unseal Documentation](https://www.vaultproject.io/docs/secrets/auto-unseal)
* [AWS KMS Overview](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)
* [Azure Key Vault Documentation](https://docs.microsoft.com/azure/key-vault/)
* [GCP Cloud KMS Documentation](https://cloud.google.com/kms/docs)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/7d277204-752e-4e8d-819a-d716205ef97c)
