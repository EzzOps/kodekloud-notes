# Unsealing with Transit Auto Unseal

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Learning-the-Vault-Architecture/Unsealing-with-Transit-Auto-Unseal/page

This article explains how Vaults Transit Auto Unseal method enables automatic unsealing of clusters while protecting the master key through a dedicated Transit Secrets Engine.

Vault’s Transit Auto Unseal method offloads unseal operations to a dedicated Transit Secrets Engine running in a separate Vault cluster. This approach protects the master key and enables automatic unsealing of dependent clusters on startup.

## Architecture Overview

One Vault cluster (the “unsealer”) runs the Transit Secrets Engine and holds the encryption key for unsealing. Other clusters delegate their unseal operations to this central cluster:

<Frame>
  ![The image illustrates the process of unsealing with Transit Auto Unseal, showing a flow from a Vault Cluster to a Master Key, then to an Encryption Key, and finally to Vault Data. It includes icons representing each component and a character illustration in the corner.](https://kodekloud.com/kk-media/image/upload/v1752878225/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Unsealing-with-Transit-Auto-Unseal/unsealing-transit-auto-unseal-diagram.jpg)
</Frame>

Each dependent cluster connects to the Transit cluster using the configured key. You can chain dependencies (green unseals from orange, red from green, etc.), but the core pattern remains: one cluster auto-unseals from another.

<Frame>
  ![The image illustrates the concept of "Unsealing with Transit Auto Unseal," showing a central "Vault Cluster (Running Transit)" connected to multiple "Other Vault Clusters In the Organization" with arrows indicating interaction.](https://kodekloud.com/kk-media/image/upload/v1752878226/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Unsealing-with-Transit-Auto-Unseal/unsealing-transit-auto-unseal-diagram-2.jpg)
</Frame>

## Key Features

<Frame>
  ![The image is a slide titled "Unsealing with Transit Auto Unseal," listing features such as using a different Vault cluster's Transit Secret Engine, key rotation support, and availability in open source and Enterprise. It also mentions the need for a highly-available core Vault cluster.](https://kodekloud.com/kk-media/image/upload/v1752878227/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Unsealing-with-Transit-Auto-Unseal/unsealing-transit-auto-unseal-features.jpg)
</Frame>

| Feature                        | Description                                                                                  |
| ------------------------------ | -------------------------------------------------------------------------------------------- |
| Dedicated Transit Engine       | Uses a separate Vault cluster’s Transit Secrets Engine for master key protection.            |
| Key Rotation Support           | Rotate the unseal key regularly to meet compliance and security requirements.                |
| Open Source & Enterprise Ready | Available in Vault OSS and Enterprise editions without additional plugins.                   |
| High Availability Requirement  | The Transit cluster must be HA with a resilient backend; downtime halts auto-unseal actions. |

<Callout icon="triangle-alert">
  If the central Transit cluster becomes unavailable, all dependent Vault clusters will fail to unseal. Ensure your Transit cluster is highly available and monitored.
</Callout>

## Configuration

To enable Transit Auto Unseal, add a `seal` stanza to your Vault configuration file:

```hcl theme={null}
seal "transit" {
  address            = "https://vault.example.com:8200"
  token              = "s.Qf1s5zigZ4OX6akYjQXJC1jY"
  disable_renewal    = "false"

  # Key configuration
  key_name           = "transit_key_name"
  mount_path         = "transit/"
  namespace          = "ns1/"

  # TLS Configuration
  tls_ca_cert        = "/etc/vault/ca_cert.pem"
  tls_client_cert    = "/etc/vault/client_cert.pem"
  tls_client_key     = "/etc/vault/client_key.pem"
  tls_server_name    = "vault"
  tls_skip_verify    = "false"
}
```

* `address` and `token` point to the central Vault cluster running Transit.
* `key_name`, `mount_path`, and `namespace` identify which key to use.
* TLS settings ensure secure communication between clusters.

## Links and References

* [Vault Transit Secrets Engine][transit-docs]
* [Vault Unsealing Concepts][unseal-docs]
* [Vault Configuration][config-docs]

[transit-docs]: https://www.vaultproject.io/docs/secrets/transit

[unseal-docs]: https://www.vaultproject.io/docs/concepts/seal

[config-docs]: https://www.vaultproject.io/docs/configuration

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/f544757d-0901-47a3-a0e6-d9ab7822ef7a/lesson/73e8e0a7-f46b-4147-a94e-2138992a629f" />
</CardGroup>
