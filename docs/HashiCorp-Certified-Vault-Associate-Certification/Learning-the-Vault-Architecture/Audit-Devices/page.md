# Audit Devices

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Learning-the-Vault-Architecture/Audit-Devices/page

This article explains Vaults audit devices, their configuration, types, best practices, and the importance of maintaining secure logging for compliance auditing.

Vault’s audit devices produce detailed JSON logs for every authenticated request and response. These logs can be forwarded to a SIEM or any log-aggregation tool for real-time alerting and compliance auditing. Sensitive data is hashed before logging, ensuring that secrets remain protected while still providing verifiable audit trails.

## Enabling a File-Based Audit Device

To start logging to a local file, run:

```bash theme={null}
vault audit enable file file_path=/var/log/vault_audit_log.log
```

<Callout icon="lightbulb">
  Ensure the operating-system user running Vault (commonly `vault`) has write permissions for `/var/log/vault_audit_log.log`. Without proper permissions, Vault will fail to enable the audit device.
</Callout>

## Audit Device Types

Vault currently offers three built-in audit backends:

| Audit Device Type | Description                                                                                                                                                                                                                                                 | Ideal Use Case                                               |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| file              | Appends JSON-formatted logs to a local file. Requires external agents (e.g., [Fluentd](https://www.fluentd.org/), AWS [CloudWatch Logs agent](https://docs.aws.amazon.[SECRET_REDACTED].html)) for shipping and log rotation. | On-premises deployments or standalone Vault servers.         |
| syslog            | Forwards logs to the local syslog daemon, which can relay to a centralized syslog server.                                                                                                                                                                   | Environments with existing syslog infrastructure.            |
| socket            | Streams logs over TCP, UDP, or Unix sockets. Avoid UDP for critical logs due to its inherent unreliability.                                                                                                                                                 | Remote log aggregation services or custom logging pipelines. |

<Frame>
  ![The image is a diagram titled "Audit Device" showing three types of logging methods: File, Syslog, and Socket, each with descriptions of their functions and characteristics.](https://kodekloud.com/kk-media/image/upload/v1752878208/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Audit-Devices/audit-device-logging-methods-diagram.jpg)
</Frame>

## Best Practices

<Callout icon="triangle-alert">
  Vault prioritizes security over availability: if it cannot write to any enabled audit device, it will refuse client requests and effectively go offline rather than risk losing audit data.
</Callout>

* Always enable at least one audit device to maintain a complete security trail.
* Deploy multiple audit backends to prevent a single point of failure.
* Regularly test your logging pipeline and verify that logs reach your SIEM or retention system.
* Monitor audit-device health and configure alerts for write failures.

<Frame>
  ![The image is a slide titled "Audit Device" explaining the importance of having more than one audit device enabled in Vault, emphasizing safety over availability, and noting that Vault requires writing to a log before completing requests. It includes a warning about the necessity of at least one audit device for logging.](https://kodekloud.com/kk-media/image/upload/v1752878212/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Audit-Devices/audit-device-importance-vault-logging.jpg)
</Frame>

## Further Reading

* [Vault Audit Logging](https://www.vaultproject.io/docs/audit)
* [Kubernetes Logging Best Practices](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
* [Security Information and Event Management (SIEM)](/docs/siem)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/f544757d-0901-47a3-a0e6-d9ab7822ef7a/lesson/4e2223ec-4d4e-4e90-bcb3-2d4568b12e22" />
</CardGroup>
