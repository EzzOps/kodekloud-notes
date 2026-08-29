# Vault Configuration File

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Learning-the-Vault-Architecture/Vault-Configuration-File/page

This guide explains how to configure HashiCorp Vault for reliable operation using a configuration file in HCL or JSON format.

In this guide, you’ll learn how to configure HashiCorp Vault for reliable, long-term operation—whether you’re running a single-node server or a multi-node cluster. Vault servers load their settings from a configuration file written in HCL or JSON. This file defines:

* **Storage backend** (Consul, S3, DynamoDB, Integrated Storage)
* **Listener settings** (API and cluster addresses, ports, TLS)
* **Seal mechanism** (AWS KMS, Azure KMS, Transit)
* **Cluster parameters** (cluster name, UI, API address, log level)
* **Optional stanzas** (telemetry, audit devices, etc.)

## Running Vault with a Config File

To start Vault using your configuration file:

```bash theme={null}
vault server -config /etc/vault.d/vault.hcl
```

<Callout icon="lightbulb">
  In production environments, manage Vault with a service manager like **systemd** or **Windows Service Manager** to ensure automatic startup and proper log handling.
</Callout>

## Key Configuration Components

| Component     | Description                                      | Example                                              |
| ------------- | ------------------------------------------------ | ---------------------------------------------------- |
| Storage       | Persistent data backend                          | `storage "consul" { ... }`                           |
| Listener      | Network interface, ports, and TLS settings       | `listener "tcp" { address = "0.0.0.0:8200" }`        |
| Seal          | Auto-unseal mechanism configuration              | `seal "awskms" { region = "us-east-1" }`             |
| Telemetry     | Metrics collection and export                    | `telemetry { prometheus_retention_time = "24h" }`    |
| Audit devices | Write-ahead logs of Vault requests and responses | `audit "file" { path = "/var/log/vault_audit.log" }` |

## Configuration Structure

A Vault configuration file comprises multiple named stanzas and top-level parameters. Here’s the skeleton in HCL:

```hcl theme={null}
listener "tcp" {
  <param1> = <value1>
  <param2> = <value2>
}

seal "awskms" {
  <param1> = <value1>
  <param2> = <value2>
}
