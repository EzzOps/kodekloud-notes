# Peer removed successfully!
```

Always remove nodes via CLI to maintain quorum.

### 4. View Cluster Membership

```bash theme={null}
vault operator raft list-peers
# Node     Address            State     Voter
# vault-0  vault-0.hcvop:8201 leader    true
# vault-1  vault-1.hcvop:8201 follower  true
# vault-2  vault-2.hcvop:8201 follower  true
# vault-3  vault-3.hcvop:8201 follower  true
# vault-4  vault-4.hcvop:8201 follower  true
```

### 5. Raft Snapshots

<Frame>
  ![The image describes "Raft Snapshots," highlighting that integrated storage allows for manual or scheduled snapshot creation, which serves as a point-in-time backup including configuration data and KV store data. It also features a Vault certification badge.](https://kodekloud.com/kk-media/image/upload/v1752878471/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Implementing-Integrated-Storage/raft-snapshots-manual-scheduled-backup.jpg)
</Frame>

#### Manual Snapshot

```bash theme={null}
vault operator raft snapshot save daily.snap
# [INFO] storage.raft: snapshot complete up to: index=389
```

#### Restore from Snapshot

```bash theme={null}
vault operator raft snapshot restore daily.snap
# [INFO] storage.raft.fsm: snapshot installed
```

Automate these commands via cron or your preferred scheduler—even in open source.

***

Integrated Storage is now the default choice for Vault clusters, offering durability, high availability, and simplified operations without sacrificing performance. Use these guidelines to plan, configure, and manage your Vault Integrated Storage deployments effectively.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/cc08ce0d-3179-436b-9d9a-bcf1618a9646" />
</CardGroup>


# PKI Secrets Engine

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/PKI-Secrets-Engine/page

The PKI Secrets Engine in HashiCorp Vault automates the issuance and management of X.509 certificates for secure communications.

The PKI Secrets Engine in HashiCorp Vault dynamically issues and manages X.509 certificates for TLS and mutual TLS (mTLS) use cases. It automates private key generation, CSR submission, CA signing, and certificate retrieval—enforcing Vault’s authentication methods and ACL policies to authorize issuance.

## Key Benefits of Vault PKI

| Feature                                  | Benefit                                                         |
| ---------------------------------------- | --------------------------------------------------------------- |
| Automated Key & CSR Generation           | Eliminates manual certificate workflows                         |
| Short-lived Certificates                 | Reduces reliance on revocation lists; improves security posture |
| Unique Certificates per Workload         | Prevents sharing, wildcard, or self-signed usage                |
| Ephemeral TTLs                           | Ensures certificates expire quickly                             |
| Integration with Existing CA Hierarchies | Acts as an intermediate CA under an offline root                |

<Frame>
  ![The image is a slide about the PKI Secrets Engine, highlighting its benefits such as short TTLs for certificates, ease of allocation, and prevention of certificate sharing and MITM attacks. It also features a Vault certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878478/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-PKI-Secrets-Engine/pki-secrets-engine-benefits-slide.jpg)
</Frame>

Workloads can request certificates at runtime and discard them on shutdown, avoiding long-lived revocation lists.

## Vault as an Intermediate CA

Vault typically functions as an intermediate CA, integrating seamlessly with your offline root CA. The flow is:

1. Vault generates an intermediate CSR.
2. You sign it with the offline root CA.
3. You import the signed intermediate certificate into Vault.
4. Vault issues end-entity certificates on behalf of your root.

<Frame>
  ![The image is a slide about the PKI Secrets Engine, explaining the use of Vault as an intermediate CA, its integration with existing CA structures, and its capability to perform root and intermediate CA functions. It includes a Vault certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878479/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-PKI-Secrets-Engine/pki-secrets-engine-vault-ca-slide.jpg)
</Frame>

<Callout icon="triangle-alert">
  Never expose your root CA online. Keep the root CA offline and only use Vault’s intermediate for runtime operations.
</Callout>

## Certificate Management Architecture

A typical deployment architecture:

1. **Root CA** (offline, long-lived)
2. **Vault** running the PKI Secrets Engine (intermediate CA)
3. **Clients** (VMs, containers, applications) that authenticate to Vault and request certificates

<Frame>
  ![The image illustrates a common architecture for certificate management, showing a Root Certificate Authority, a Vault with a PKI Secrets Engine as an Intermediate CA, and a process for requesting and responding with certificates.](https://kodekloud.com/kk-media/image/upload/v1752878480/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-PKI-Secrets-Engine/certificate-management-architecture-diagram.jpg)
</Frame>

Clients receive their unique certificates and private keys securely at runtime.

***

## Enabling the PKI Secrets Engine

Enable Vault’s PKI engine at the default or a custom path:

```bash theme={null}
