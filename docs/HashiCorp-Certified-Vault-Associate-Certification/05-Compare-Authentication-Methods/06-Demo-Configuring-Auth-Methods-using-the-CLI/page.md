# Demo Configuring Auth Methods using the CLI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Compare-Authentication-Methods/Demo-Configuring-Auth-Methods-using-the-CLI/page

This guide explains managing HashiCorp Vault authentication methods using the CLI, including enabling, listing, disabling, and tuning various backends.

In this guide, we’ll walk through how to manage HashiCorp Vault authentication methods (`auth` backends) using the Vault CLI. You’ll learn to enable, list, disable, tune, and interact with backends such as `userpass` and `approle` in a consistent, repeatable way.

## Viewing Available Auth Subcommands

Start by inspecting the top-level `vault auth` command:

```bash theme={null}
vault auth -h
```

To see commonly used subcommands:

| Command                     | Description                                      |
| --------------------------- | ------------------------------------------------ |
| `vault auth list`           | List all enabled auth methods                    |
| `vault auth enable [TYPE]`  | Enable a new auth backend                        |
| `vault auth disable [PATH]` | Disable an existing auth backend                 |
| `vault auth tune [OPTIONS]` | Update mount settings (e.g., TTLs, descriptions) |
| `vault auth help [BACKEND]` | Show detailed help for a specific auth backend   |

You can also run:

```bash theme={null}
vault auth help userpass
vault auth help approle
```

to get backend-specific guidance.

## Enabling and Listing Auth Methods

### 1. Enable `userpass` at the Default Path

```bash theme={null}
vault auth enable userpass
