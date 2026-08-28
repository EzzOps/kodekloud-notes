# Enable AWS Secrets Engine at default path
vault secrets enable aws

# Disable the AWS Secrets Engine
vault secrets disable aws

# List all enabled Secrets Engines
vault secrets list

# Move a Secrets Engine to a new mount path
vault secrets move new-path/ old-path/

# Tune PKI engine default lease TTL to 72 hours
vault secrets tune -default-lease-ttl=72h pki/

# Enable KV v2 at custom path with description
vault secrets enable \
  --path="cloud-kv" \
  --description="My Secrets Engine" \
  kv-v2

# View detailed mount information
vault secrets list --detailed
```

### Sample Output

```text theme={null}
Path             Type          Accessor                Description
----             ----          ---------               -----------
aws/             aws           aws_dafa7adc            n/a
azure/           aws           aws_1a214ff6            n/a
vault-ops-pro/   kv            kv_28b1ceaa             Earn Your HCVOP Certification
cloud-team-kv/   kv            kv_fa270a3f             n/a
cubbyhole/       cubbyhole     cubbyhole_88c8e2e3      per-token private secret storage
dev-team-kv/     kv            kv_55c319c4             n/a
identity/        identity      identity_e60e93cb       identity store
kv-v2/           kv            kv_eea3206c             n/a
sys/             system        system_66b0d8ee         system endpoints used for control
transit/         transit       transit_7b8038ca        n/a
```

<Callout icon="triangle-alert">
  Ensure your Vault token has the `root` policy or appropriate `sys/mount` and `sys/cap` capabilities to enable and configure Secrets Engines.
</Callout>

## Enabling Engines via UI

1. Open the Vault UI and navigate to the **Secrets** tab.
2. Click **Enable New Secrets Engine**.
3. Select an engine type, configure the mount path and options, then click **Save**.
4. For engines not fully supported in the UI, switch to the CLI or API for advanced settings.

<Frame>
  ![The image is a screenshot of a user interface for enabling secrets engines, showing a list of already enabled engines and an option to add more. It includes annotations and a cartoon character in the bottom right corner.](https://kodekloud.com/kk-media/image/upload/v1752878448/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Enable-and-Configure-Secrets-Engines/secrets-engines-ui-screenshot-annotations.jpg)
</Frame>

## Next Steps

Now that you’ve learned how to enable and manage Vault Secrets Engines, the next sections will dive deeper into configuring each engine:

1. Key/Value (KV) Secrets Engine
2. Database Secrets Engine
3. Public Key Infrastructure (PKI)
4. Transit Secrets Engine
5. Identity and Cubbyhole Engines

Stay tuned to master dynamic secrets, encryption, and certificate automation in HashiCorp Vault.

## Links and References

* [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
* [Vault CLI Commands](https://www.vaultproject.io/docs/commands/secrets)
* [HashiCorp Learn: Vault Secrets Engines](https://learn.hashicorp.com/collections/vault/secrets)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/0aa8745e-4c7d-4213-9c38-b099d71c6c8e" />
</CardGroup>


# Identity Secrets Engine

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Identity-Secrets-Engine/page

Vault’s Identity Secrets Engine manages identities and policies, tracks clients, maps authentication methods, and enables scalable policy assignment using groups.

Vault’s Identity Secrets Engine is the core component for managing identities and policies in Vault. It tracks all clients (entities), maps authentication methods to those entities via aliases, and enables scalable policy assignment using groups.

## Overview

<Callout icon="lightbulb">
  The Identity Secrets Engine is mounted by default in Vault (path: `identity/`). It cannot be disabled or moved.
</Callout>

Key characteristics:

* Represents every Vault client as an **entity**, each with:
  * A unique entity ID.
  * Zero or more **aliases** linking auth methods.
* Operators can manage entities, aliases, and groups via the **UI**, **CLI**, or **API**.
* On first login, Vault auto-creates an entity and alias if none exist.

| Feature       | Description                                            |
| ------------- | ------------------------------------------------------ |
| Entities      | Unique identities for users or systems                 |
| Aliases       | Links between auth methods and entities                |
| Groups        | Collections of entities for policy management at scale |
| Default Mount | Always enabled at `identity/`                          |

## Entities and Aliases

An **entity** represents one person or system. An **alias** maps a particular authentication method to that entity. You can pre-create entities and add aliases later or let Vault handle it automatically.

When a new user logs in via **userpass**, Vault:

1. Creates an entity (e.g., `b81de864-...`).
2. Attaches an alias combining the auth method (`userpass`) and username (`JSmith`).
3. Associates policies and optional metadata.

Example CLI commands:

```bash theme={null}
vault write identity/entity name="Julie Smith" metadata=department=finance policies="management"
vault write identity/entity-alias name="JSmith" canonical_id="E48C..." mount_accessor="$(vault auth list -format=json | jq -r '.userpass_accessor')"
```

<Frame>
  ![The image illustrates a Vault entity setup, showing a user with an alias, entity ID, and associated policy. It includes a character labeled as a finance specialist and a certification badge.](https://kodekloud.com/kk-media/image/upload/v1752878449/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Identity-Secrets-Engine/vault-entity-setup-user-policy.jpg)
</Frame>

## Multiple Authentication Methods

Without consolidation, multiple auth methods create separate entities:

* `userpass/JSmith` → entity `B81D…` (policy: `accounting`)
* `ldap/jsmith@example.com` → entity `E93D…` (policy: `finance`)
* `github/jsmith22` → entity `F45A…` (policy: `accounts-payable`)

This fragmentation can complicate policy management and reporting.

<Frame>
  ![The image illustrates a "Vault Entities" diagram featuring a character named Julie Smith, a finance specialist, with authentication options and entity details for accounting and finance departments. It also includes a certification badge labeled "Vault Certified Operations Professional."](https://kodekloud.com/kk-media/image/upload/v1752878450/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Identity-Secrets-Engine/vault-entities-julie-smith-diagram.jpg)
</Frame>

### Consolidating into a Single Entity

To unify access, create one **Julie Smith** entity and attach all auth method aliases:

1. Create the entity and assign shared policy (`management`):
   ```bash theme={null}
   vault write identity/entity name="Julie Smith" policies="management"
   ```
2. Add aliases for each auth method:
   ```bash theme={null}
   vault write identity/entity-alias name="JSmith" canonical_id="E48C..." mount_accessor="userpass_accessor"
   vault write identity/entity-alias name="jsmith@example.com" canonical_id="E48C..." mount_accessor="ldap_accessor"
   vault write identity/entity-alias name="jsmith22" canonical_id="E48C..." mount_accessor="github_accessor"
   ```
3. On login via any method, tokens inherit:
   * Alias-level policy (e.g., `accounting`)
   * Entity-level policy (`management`)

<Frame>
  ![The image illustrates the concept of Vault Entities, showing how a user named Julie Smith is authenticated via LDAP to receive a Vault token, which inherits capabilities from multiple policies. It includes a diagram of the authentication process and lists aliases with associated policies.](https://kodekloud.com/kk-media/image/upload/v1752878452/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Identity-Secrets-Engine/vault-entities-authentication-diagram.jpg)
</Frame>

## Vault Groups

Groups enable policy management for many entities simultaneously:

* A **group** can contain entities and subgroups.
* Assign policies at the group level; all members inherit them.
* Similar to directory-based groups (LDAP/AD).

Example: A **Finance Team** group with the `finance` policy includes:

* Maria (entity-level `accounts-payable`)
* John  (entity-level `management`)

On login, tokens merge policies from:

1. Alias
2. Entity
3. Group

<Frame>
  ![The image illustrates a "Vault Groups" structure, showing members with their entity IDs, policies, and aliases, and explaining how tokens inherit capabilities from aliases, entities, and groups.](https://kodekloud.com/kk-media/image/upload/v1752878453/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Identity-Secrets-Engine/vault-groups-structure-illustration.jpg)
</Frame>

## Internal vs. External Groups

Vault supports two group types:

| Group Type     | Creation             | Membership Source      | Use Case                                              |
| -------------- | -------------------- | ---------------------- | ----------------------------------------------------- |
| Internal Group | Manually in Vault    | Vault managed          | Propagate permissions across namespaces               |
| External Group | Auto-mapped from IdP | LDAP, OIDC, Okta, etc. | Mirror external identity provider groups and policies |

<Frame>
  ![The image compares internal and external Vault groups, explaining that internal groups are manually created to propagate identical permissions, while external groups are inferred and created based on group associations from authentication methods.](https://kodekloud.com/kk-media/image/upload/v1752878455/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Identity-Secrets-Engine/vault-groups-internal-external-comparison.jpg)
</Frame>

### Internal Groups and Namespaces

Use internal groups at the root namespace to grant child namespaces access without reconfiguring auth everywhere:

* At root: create an internal group `team-finance` with policy `finance`.
* In child namespace (`finance`): reference the root group as a subgroup.
* Users authenticated at root automatically gain child namespace permissions.

<Frame>
  ![The image is an informational slide about internal groups in Vault, explaining their use in managing permissions and propagating them through namespaces. It includes a diagram showing the relationship between a root namespace and a child namespace.](https://kodekloud.com/kk-media/image/upload/v1752878456/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Identity-Secrets-Engine/vault-internal-groups-permissions-diagram.jpg)
</Frame>

### External Groups

External groups sync with your identity provider’s groups:

* Create a Vault external group (e.g., `team-finance`).
* Map an alias to the provider’s group name or UUID.
* Assign policies in Vault; manage membership in your IdP.

On login, Vault reflects current IdP memberships and applies policies.

<Frame>
  ![The image explains how external groups are used to set permissions based on group membership from an external identity provider, with a diagram showing integration between Active Directory and HashiCorp Vault.](https://kodekloud.com/kk-media/image/upload/v1752878458/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Identity-Secrets-Engine/external-groups-permissions-active-directory-vault.jpg)
</Frame>

## Summary

* **Entities** unify clients under a unique identifier.
* **Aliases** link auth methods to entities for granular policies.
* **Groups** (internal/external) scale policy management across teams and namespaces.
* Use the Vault **CLI** and **UI** to configure entities, aliases, and groups.

## Links and References

* [Vault Identity Secrets Engine](https://www.vaultproject.io/docs/secrets/identity)
* [Managing Identities and Access](https://www.vaultproject.io/guides/identity)
* [HashiCorp Vault CLI](https://www.vaultproject.io/docs/commands)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/48dbcef3-9a97-4549-8cfb-90a89176bc65" />
</CardGroup>
