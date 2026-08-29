# Managing Policies using the CLI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Create-Vault-Policies/Managing-Policies-using-the-CLI/page

This article explains how to manage Vault policies using the CLI, including listing, reading, writing, deleting, and formatting policies.

Vault policies define fine-grained authorization rules for accessing secrets and operations. Using Vault’s `policy` namespace in the CLI, you can list, read, create/update, delete, and format policy files.

| Subcommand | Description                                |
| ---------- | ------------------------------------------ |
| `list`     | List all existing policies                 |
| `read`     | Display the HCL contents of a policy       |
| `write`    | Create or update a policy from an HCL file |
| `delete`   | Remove a policy from Vault                 |
| `fmt`      | Canonicalize an HCL policy file’s format   |

For detailed syntax, see the [Vault CLI Policy Commands](https://www.vaultproject.io/docs/commands/policy).

## 1. Listing Policies

To view all policies currently loaded into Vault:

```bash theme={null}
vault policy list
```

Sample output:

```text theme={null}
admin-policy
default
root
```

<Callout icon="lightbulb">
  Vault always provides a `default` and `root` policy. Custom policies appear alongside these.
</Callout>

## 2. Writing (Creating or Updating) a Policy

Create a new policy or update an existing one by specifying the policy name and the path to your HCL file:

```bash theme={null}
vault policy write admin-policy /tmp/admin.hcl
```

Expected output:

```text theme={null}
Success! Uploaded policy: admin-policy
```

Steps breakdown:

1. `vault` – invokes the Vault CLI
2. `policy` – selects the policy management namespace
3. `write` – subcommand for creation or update
4. `admin-policy` – policy name
5. `/tmp/admin.hcl` – HCL file path

<Callout icon="lightbulb">
  Ensure the HCL file path is correct and accessible. Relative or absolute paths both work.
</Callout>

## 3. Reading a Policy

To inspect the rules defined in a policy:

```bash theme={null}
vault policy read admin-policy
```

This outputs the HCL block that defines all allowed paths and capabilities for `admin-policy`.

## 4. Deleting a Policy

Remove a policy when it’s no longer needed:

```bash theme={null}
vault policy delete admin-policy
```

Expected output:

```text theme={null}
Success! Deleted policy: admin-policy
```

<Callout icon="triangle-alert">
  Deleting a policy is irreversible. Make sure it’s no longer in use by any Vault tokens or roles.
</Callout>

## 5. Formatting a Policy File

If your HCL file has inconsistent whitespace or indentation, `fmt` will rewrite it in a canonical form:

```bash theme={null}
vault policy fmt /tmp/admin.hcl
```

This command overwrites `/tmp/admin.hcl` with a properly formatted version.

## Example: Creating a `webapp` Policy

Given an HCL file `/tmp/webapp.hcl`, create a new policy named `webapp`:

```bash theme={null}
vault policy write webapp /tmp/webapp.hcl
```

You should see:

```text theme={null}
Success! Uploaded policy: webapp
```

Now, running `vault policy list` will include `webapp`:

```bash theme={null}
vault policy list
