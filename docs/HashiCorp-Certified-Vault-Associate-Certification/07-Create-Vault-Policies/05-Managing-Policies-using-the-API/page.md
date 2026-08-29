# Output:
# default
# root
```

Read the contents of the `default` policy:

```bash theme={null}
vault policy read default
# Allow tokens to look up their own properties
path "auth/token/lookup-self" {
  capabilities = ["read"]
}

# Allow tokens to renew themselves
path "auth/token/renew-self" {
  capabilities = ["update"]
}

# Allow tokens to revoke themselves
path "auth/token/revoke-self" {
  capabilities = ["update"]
}

# Allow tokens to view their own capabilities
path "sys/capabilities-self" {
  capabilities = ["update"]
}
```

Attempting to read the `root` policy returns an error:

```bash theme={null}
vault policy read root
# Error reading policy: No policy named 'root'
```

Under the hood, the `root` policy behaves as if it contains:

```hcl theme={null}
path "*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}
```

* [Vault Policies Overview](https://www.vaultproject.io/docs/concepts/policies)
* [HCL Configuration Language](https://www.vaultproject.io/docs/configuration/hcl)
* [Vault Authentication Methods](https://www.vaultproject.io/docs/auth)
* [Vault CLI Guide](https://www.vaultproject.io/docs/commands)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/83a61f63-3f1f-436c-8aa3-e972b099eeec/lesson/0691a24b-ed2f-46b4-b147-372fac3ce38c)


# Managing Policies using the API

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Create-Vault-Policies/Managing-Policies-using-the-API/page

This article explains how to manage Vault policies using the HTTP API, including creating and updating policies with example commands.

Vault’s HTTP API provides a straightforward way to create, update, and manage policies. By sending a `PUT` request to the `/v1/sys/policy/<name>` endpoint along with a JSON payload, you can define or overwrite policy rules.

## Create or Update a Policy

Use the following `curl` command to create or update a policy named `webapp`:

```bash theme={null}
curl \
  --header "X-Vault-Token: s.bCEo8HFNIIR8wRGAzwXwkqUk" \
  --request PUT \
  --data @payload.json \
  http://127.0.0.1:8200/v1/sys/policy/webapp
```

| Option                        | Description                                                       | Example                                     |
| ----------------------------- | ----------------------------------------------------------------- | ------------------------------------------- |
| `--header "X-Vault-Token: …"` | Vault token for authentication                                    | `X-Vault-Token: s.bCEo8HFNIIR8wRGAzwXwkqUk` |
| `--request PUT`               | HTTP method for creating or updating a policy                     | `PUT`                                       |
| `--data @payload.json`        | Path to the JSON file with the policy definition                  | `@payload.json`                             |
| API endpoint                  | Target URL for policy management; replace `webapp` with your name | `/v1/sys/policy/webapp`                     |

> **triangle-alert** Using `PUT` on an existing policy will overwrite it. Always review the policy rules before applying.

### payload.json Example

Below is a sample `payload.json` defining a policy with read, write, list, and delete permissions on `kv/apps/webapp`:

```json theme={null}
{
  "policy": "
    path \"kv/apps/webapp\" {
      capabilities = [\"create\", \"update\", \"read\", \"delete\", \"list\"]
    }
  "
}
```

* **`policy`**: Contains the HCL-like policy string.
* **`path "kv/apps/webapp"`**: Specifies the secrets path this policy governs.
* **`capabilities`**: Lists allowed operations on that path.

> **lightbulb** Ensure `payload.json` is located in your current directory or provide an absolute path.\
  For advanced policy syntax, see the [Vault Policy Documentation](https://www.vaultproject.io/docs/concepts/policies).

## Next Steps & References

* Learn more about Vault’s policy engine and HCL syntax:\
  [Vault Policy Language](https://www.vaultproject.io/docs/concepts/policies)
* Explore other system endpoints in the API:\
  [Vault HTTP API Reference](https://www.vaultproject.io/api-docs)
* Secure Vault tokens and follow [best practices](/docs/security/best-practices).

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/83a61f63-3f1f-436c-8aa3-e972b099eeec/lesson/725b59ca-113b-4b81-8696-428b32d41eab)
