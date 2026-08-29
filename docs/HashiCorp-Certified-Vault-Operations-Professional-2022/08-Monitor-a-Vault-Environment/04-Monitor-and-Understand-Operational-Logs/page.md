# Enable the default file audit device
vault audit enable file file_path="/var/log/vault_audit.log"
# Enable file audit on a custom mount point "logs/"
vault audit enable -path=logs file \
  file_path="/var/log/audit.log"
# Output: Success! Enabled the file audit device at: logs/
```

For **syslog** or **socket**, replace `file` with `syslog` or `socket` and add the required flags.\
Run `vault audit enable -help` for full parameter details.

## Listing and Disabling Audit Devices

Quickly view or remove audit devices:

```bash theme={null}
# List all enabled audit devices
vault audit list
# Example output:
# Path    Type    Description
# ----    ----    -----------
# file/   file    n/a
# Disable the syslog audit device
vault audit disable syslog/
# Output: Success! Disabled audit device at: syslog/
```

## Inspecting a Sample Audit Entry

Pipe JSON logs through `jq` for readability:

```bash theme={null}
cat /var/log/vault_audit.log | jq
```

```json theme={null}
{
  "time": "2022-12-25T21:20:12.40607Z",
  "type": "response",
  "auth": {
    "client_token": "hmac-sha256:c134d4c72a6cd891102c654b0b897f3b747a3366e88b6b2fc25247bd977ec949",
    "display_name":"root",
    "policies":    ["root"],
    "token_type":  "service",
    "issue_time":  "2022-12-25T11:07:35-04:00"
  },
  "request": {
    "id":        "96801004-f2a5-a994-bc7a-0b15e3739db9",
    "operation": "update",
    "path":      "secret/data/myapp"
  },
  "response": {
    "status": "success"
  }
}
```

Notice how tokens and sensitive fields are hashed rather than exposed in plain text.

## Permissions for Audit Device Management

To grant a policy permission to create, read, and manage an audit device, include the `sudo` capability:

```hcl theme={null}
# Policy to manage the file audit device
path "sys/audit/file" {
  capabilities = [
    "create",
    "read",
    "update",
    "delete",
    "list",
    "sudo"
  ]
}
```

Without `sudo`, roles cannot enable, disable, or reconfigure audit devices.

## Links and References

* [Vault Audit Devices](https://www.vaultproject.io/docs/audit)
* [Vault CLI Documentation](https://www.vaultproject.io/docs/commands/audit)
* [JSON Query with jq](https://stedolan.github.io/jq/)

***

This concludes our overview of Vault audit devices and log management. In the next hands-on lab, you’ll enable devices, generate log entries, and configure a log collector for centralized monitoring.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/36cf9665-35d2-4dbc-9ddc-fc00ca80cbd4/lesson/bc202187-a5f5-43d7-a625-b7e904688541)


# Monitor and Understand Operational Logs

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Monitor-a-Vault-Environment/Monitor-and-Understand-Operational-Logs/page

This guide explains how to work with HashiCorp Vault’s operational logs for troubleshooting and adjusting verbosity.

In this guide, you’ll learn how to work with HashiCorp Vault’s operational logs—where they’re written, how to adjust verbosity, and how to retrieve them for effective troubleshooting.

## Vault Server Logs

Vault emits logs at startup and continuously during operation. These logs capture:

* Listener and port configurations
* Storage backend details
* Vault version and module information
* Active log level settings

They’re critical for diagnosing syntax errors, configuration mistakes, or runtime failures.

![The image is a slide titled "Vault Server Logs," explaining how Vault logs configuration information during startup and continues logging for troubleshooting, with configurable log levels like err, warn, info, debug, and trace.](https://kodekloud.com/kk-media/image/upload/v1752878579/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Monitor-and-Understand-Operational-Logs/vault-server-logs-configuration-troubleshooting.jpg)

> **lightbulb** If your HCL file has a syntax error (for example, a missing comma or bracket), Vault’s startup logs will identify the exact line number and issue.

## Vault Log Levels

Vault supports five log levels, from least to most verbose. Choose the level that best matches your troubleshooting needs:

| Level | Description                            | Use Case               |
| ----- | -------------------------------------- | ---------------------- |
| error | Only critical failures                 | Production emergency   |
| warn  | Warnings and errors                    | Pre-production staging |
| info  | General operational messages (default) | Routine monitoring     |
| debug | Detailed internal operations           | In-depth debugging     |
| trace | Full trace of Vault internals          | Deep diagnostics       |

![The image illustrates "Vault Log Levels" with a gradient arrow indicating log detail from "ERROR" to "TRACE," and a star marking the default setting. It also features a certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878579/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Monitor-and-Understand-Operational-Logs/vault-log-levels-gradient-arrow-diagram.jpg)

## Configuring the Log Level

After updating any log settings, restart the Vault server for changes to take effect. You can set the log level via:

### 1. CLI Flag

```bash theme={null}
vault server -config=/opt/vault/vault.hcl --log-level=debug
```

### 2. Environment Variable

```bash theme={null}
export VAULT_LOG_LEVEL=trace
vault server -config=/opt/vault/vault.hcl
```

### 3. Configuration File

Add this to your HCL:

```hcl theme={null}
log_level = "warn"
```

Then restart Vault.

> **triangle-alert** An invalid `log_level` value in your HCL will prevent Vault from starting. Always verify the syntax.

## Viewing Vault Logs

### Using systemd (journalctl)

On Linux systems with systemd, Vault logs go to journald. View them with:

```bash theme={null}
journalctl -b --no-pager -u vault
```

Navigate with Page Up/Page Down, `Shift+G` to jump to the end, and `Ctrl+C` to exit.

### Using Docker

If Vault runs inside Docker:

```bash theme={null}
docker logs vault0
```

Sample output:

```text theme={null}
Couldn't start vault with IPC_LOCK. Disabling IPC_LOCK...
==> Vault server configuration:
Api Address: http://0.0.0.0:8200
Cluster Address: https://0.0.0.0:8201
Log Level: info
...
```

### Using Portainer

In exam or lab environments, Vault containers may be managed via Portainer. Use its UI to:

* Start/stop containers
* View real-time logs
* Inspect environment settings

## Links and References

* [HashiCorp Vault Documentation](https://www.vaultproject.io/docs/)
* [Docker Documentation](https://docs.docker.com/)
* [systemd journalctl Manual](https://www.freedesktop.org/software/systemd/man/journalctl.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/36cf9665-35d2-4dbc-9ddc-fc00ca80cbd4/lesson/0a0fa240-1bd2-4b34-b181-97678db1134c)
