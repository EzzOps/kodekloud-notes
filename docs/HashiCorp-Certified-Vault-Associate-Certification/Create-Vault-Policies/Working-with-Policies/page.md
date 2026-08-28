# Working with Policies

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Create-Vault-Policies/Working-with-Policies/page

This guide covers creating, testing, and writing policies for tokens in HashiCorp Vault to ensure secure access control.

In this guide, you’ll learn how to create and test tokens scoped to specific policies and write administrative policies for Vault operators. Leveraging policy-based access control (PBAC) in HashiCorp Vault ensures fine-grained security, minimal access, and clear audit trails.

## Table of Contents

1. [Creating a Token with a Policy](#creating-a-token-with-a-policy)
2. [Inspecting an Existing Token](#inspecting-an-existing-token)
3. [Testing Token Capabilities](#testing-token-capabilities)
4. [Writing Administrative Policies](#writing-administrative-policies)
5. [Links and References](#links-and-references)

***

## Creating a Token with a Policy

To issue a new Vault token and bind it to one or more policies, run:

```bash theme={null}
vault token create -policy="web-app"
```

Example output:

```text theme={null}
Key                    Value
---                    -----
token                  s.7uBlZwXSxOg31uGXIUetEdXD
token_accessor         18r88muoe3x1xEqVqXdlTMwJ
token_duration         768h
token_renewable        true
token_policies         ["default" "web-app"]
identity_policies      []
```

### Token Attributes

| Field              | Description                                           |
| ------------------ | ----------------------------------------------------- |
| token              | The actual authentication token                       |
| token\_accessor    | Short-lived handle for revocation or lookup           |
| token\_duration    | Time-to-live (TTL) for the token                      |
| token\_renewable   | Indicates if the token can be renewed                 |
| token\_policies    | List of attached policies (always includes `default`) |
| identity\_policies | Attached identity group policies (if any)             |

<Callout icon="lightbulb">
  Every token in Vault inherits the `default` policy. Always design your custom policies to grant only the permissions required for your application.
</Callout>

***

## Inspecting an Existing Token

To review the details and policies of an existing Vault token, use:

```bash theme={null}
vault token lookup <token>
```

This command displays all token attributes, including the list of policies attached.

***

## Testing Token Capabilities

Before deploying a token in production, validate that it grants exactly the permissions you need. Suppose your `web-app` policy (`web-app.hcl`) should:

1. Read a secret at `secret/data/api/key/google`.
2. Generate AWS credentials from `aws/creds/s3-readonly`.

After writing and loading your policy:

```bash theme={null}
vault policy write web-app web-app.hcl
```

Test the policy with these steps:

```bash theme={null}
