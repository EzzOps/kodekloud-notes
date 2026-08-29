# Demo Audit Logs

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Monitor-a-Vault-Environment/Demo-Audit-Logs/page

Learn to configure and inspect Vault’s audit device, including listing, enabling, generating events, and viewing logs.

In this lesson, you’ll learn how to configure and inspect Vault’s audit device. We’ll cover:

* Listing existing audit devices
* Disabling and re-enabling audit devices
* Generating audit events
* Viewing and pretty-printing audit logs
* Cleaning up when finished

For more details, see the official [Vault Audit Device documentation](https://www.vaultproject.io/docs/audit).

***

## Table of Contents

1. [List Existing Audit Devices](#1-list-existing-audit-devices)
2. [Disable an Audit Device](#2-disable-an-audit-device)
3. [Enable the File Audit Device](#3-enable-the-file-audit-device)
4. [Generate Audit Events](#4-generate-audit-events)
5. [View and Pretty-Print Audit Logs](#5-view-and-pretty-print-audit-logs)
6. [Disable the File Audit Device](#6-disable-the-file-audit-device)

***

## 1. List Existing Audit Devices

To see which audit devices are currently enabled, run:

```bash theme={null}
vault audit list
```

Example output:

```text theme={null}
Path   Type   Description
----   ----   ----------
logs/  file   n/a
```

***

## 2. Disable an Audit Device

If you need a clean slate, disable any existing audit device first:

```bash theme={null}
vault audit disable logs
```

> Success! Disabled audit device (if it was enabled) at: logs/

Verify there are no active audit devices:

```bash theme={null}
vault audit list
```

Output:

```text theme={null}
No audit devices are enabled.
```

***

## 3. Enable the File Audit Device

Configure Vault to write audit logs to a local file:

<Callout icon="lightbulb">
  Be mindful of disk usage—audit files can grow quickly depending on the volume of requests.
</Callout>

```bash theme={null}
vault audit enable file file_path="/Users/bk/vault/vault_audit.log"
```

> Success! Enabled the file audit device at: file/

Confirm it’s active:

```bash theme={null}
vault audit list
```

Output:

```text theme={null}
Path   Type   Description
----   ----   ----------
file/  file   n/a
```

Ensure the log file appears in your working directory:

```bash theme={null}
ls
```

Sample result:

```text theme={null}
vault_audit.log  vault.hcl  data/
```

***

## 4. Generate Audit Events

Perform common Vault operations to create log entries:

1. List all enabled secrets engines:

   ```bash theme={null}
   vault secrets list
   ```

2. Write a KV secret:

   ```bash theme={null}
   vault kv put kv/hcvop certification="HashiCorp"
   ```

3. Delete the secret:

   ```bash theme={null}
   vault kv delete kv/hcvop
   ```

4. Clear the screen to prepare for log inspection:

   ```bash theme={null}
   clear
   ```

***

## 5. View and Pretty-Print Audit Logs

### Raw JSON Output

Audit logs are stored as newline-delimited JSON. To view raw entries:

```bash theme={null}
cat /Users/bk/vault/vault_audit.log
```

You’ll see entries like:

```json theme={null}
{"time":"2023-10-11T17:10:19.747Z","type":"response", …}
```

### Pretty-Print with jq

For easier reading, pipe through `jq`:

```bash theme={null}
cat /Users/bk/vault/vault_audit.log | jq
```

Example of a request/response entry:

```json theme={null}
{
  "time": "2023-10-11T17:10:19.747Z",
  "type": "response",
  "auth": { /* … */ },
  "request": {
    "id": "request_id",
    "operation": "operation_name",
    /* … */
  }
}
```

Example of a KV delete operation:

```json theme={null}
{
  "request": {
    "operation": "delete",
    "mount_type": "kv",
    /* … */
  },
  "path": "kv/data/hcvop",
  "response": { "mount_type": "kv" }
}
```

***

## 6. Disable the File Audit Device

When you’re done, remove the audit device to prevent further log growth:

<Callout icon="triangle-alert">
  Disabling the audit device stops new entries but does not delete existing logs. Archive or remove them manually if needed.
</Callout>

```bash theme={null}
vault audit disable file
```

> Success! Disabled audit device (if it was enabled) at: file/

Verify no devices remain:

```bash theme={null}
vault audit list
```

Output:

```text theme={null}
No audit devices are enabled.
```

***

## Summary of Commands

| Task                            | Command                                                 |
| ------------------------------- | ------------------------------------------------------- |
| List audit devices              | `vault audit list`                                      |
| Disable an audit device         | `vault audit disable <path>`                            |
| Enable file audit device        | `vault audit enable file file_path="…/vault_audit.log"` |
| Generate sample events          | `vault kv put` / `vault kv delete`                      |
| View raw logs                   | `cat vault_audit.log`                                   |
| Pretty-print logs               | `cat vault_audit.log \| jq`                             |
| Disable file audit device again | `vault audit disable file`                              |

***

## Links and References

* [Vault Audit Devices](https://www.vaultproject.io/docs/audit)
* [HashiCorp Vault CLI Commands](https://www.vaultproject.io/docs/commands)
* [jq Manual](https://stedolan.github.io/jq/manual/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/36cf9665-35d2-4dbc-9ddc-fc00ca80cbd4/lesson/236dc78c-af33-4815-90fc-c86b6ee99ba9" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/36cf9665-35d2-4dbc-9ddc-fc00ca80cbd4/lesson/db266764-4afa-4364-a1fd-eed8fb3a04fe" />
</CardGroup>
