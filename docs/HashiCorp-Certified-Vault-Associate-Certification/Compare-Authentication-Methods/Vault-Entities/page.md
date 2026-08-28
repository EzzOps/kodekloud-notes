# Vault Entities

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Compare-Authentication-Methods/Vault-Entities/page

This guide explains how Vault consolidates identities and policies for users and machines across multiple authentication methods.

Vault’s Identity Secrets Engine (enabled by default) provides a unified way to map users and machines—across various auth methods—to logical entities. In this guide, you’ll learn how Vault auto-creates entities and aliases, understand the challenges of multiple auth methods, and see how to consolidate them into a single, manageable entity.

## 1. Entities and Aliases

<Callout icon="lightbulb">
  An **entity** represents a user or machine in Vault with a unique ID, metadata, and attached policies. An **alias** links that entity to a specific auth method (e.g., auth mount accessor + username).
</Callout>

* **Entity**
  * Unique identifier (ID)
  * Optional metadata (e.g., email, department)
  * Attached policies defining capabilities

* **Alias**
  * Maps one auth method and credential identifier to an entity
  * An entity can have zero or more aliases

When a user first logs in via any supported auth method (UserPass, LDAP, OIDC, AppRole, AWS, GitHub, etc.), Vault automatically:

1. Creates a new entity.
2. Creates an alias for that auth path and user identifier.
3. Applies policies attached to both the alias and the entity.

## 2. Single Auth Method Example

Julia Smith logs in with the UserPass method as `jsmith`:

1. Vault creates an entity for Julia (`ent-userpass-xxxx`).
2. Vault attaches an alias combining the UserPass accessor and `jsmith`.
3. Any policies assigned to that alias or entity govern her token’s permissions.

## 3. Multiple Auth Methods: The Challenge

If Julia also logs in via LDAP (`jsmith@example.com`) and GitHub (`JSmith22`), Vault will create separate entities and aliases for each method:

| Auth Method | Entity ID         | Attached Policy   |
| ----------- | ----------------- | ----------------- |
| UserPass    | ent-userpass-1234 | accounting        |
| LDAP        | ent-ldap-5678     | finance           |
| GitHub      | ent-github-9012   | accounts\_payable |

<Callout icon="triangle-alert">
  Each login issues a token scoped only to that specific entity’s policies. To switch permissions, users must log out and authenticate with a different method.
</Callout>

## 4. Consolidating into a Single Entity

You can streamline user access by creating one master entity (e.g., “Julia Smith”) and assigning all auth-method aliases to it. Attach a shared policy (e.g., `management`) at the entity level so any login inherits both alias and entity policies.

<Frame>
  ![The image illustrates the concept of Vault Entities, showing how a user named Julie Smith is associated with multiple policies through different aliases, and how authentication with LDAP credentials results in a Vault token that inherits capabilities from these policies.](https://kodekloud.com/kk-media/image/upload/v1752878038/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Vault-Entities/vault-entities-julie-smith-policies.jpg)
</Frame>

## 5. Login Workflow with a Consolidated Entity

1. User logs in via LDAP (`jsmith@example.com`).
2. Vault validates credentials against the LDAP server.
3. Vault resolves the LDAP alias to the master “Julia Smith” entity.
4. Vault issues a token that includes:
   * Policies on the LDAP alias (e.g., `finance`)
   * Policies on the entity (e.g., `management`)

## 6. Creating the Entity and Aliases

Use the Vault CLI to set up the consolidated entity and its aliases:

```shell theme={null}
