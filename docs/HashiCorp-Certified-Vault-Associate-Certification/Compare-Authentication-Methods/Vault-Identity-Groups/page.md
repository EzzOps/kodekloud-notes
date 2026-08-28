# 1. Create the master entity with the 'management' policy
vault write identity/entity name="Julia Smith" policies="management"

# Capture the generated entity ID
ENTITY_ID=$(vault read -field=id identity/entity/name/Julia-Smith)

# UserPass alias
USERPASS_ACCESSOR=$(vault auth list -format=json | jq -r '.["userpass/"].accessor')
vault write identity/entity-alias \
    name="jsmith" \
    canonical_id="$ENTITY_ID" \
    mount_accessor="$USERPASS_ACCESSOR"

# LDAP alias
LDAP_ACCESSOR=$(vault auth list -format=json | jq -r '.["ldap/"].accessor')
vault write identity/entity-alias \
    name="jsmith@example.com" \
    canonical_id="$ENTITY_ID" \
    mount_accessor="$LDAP_ACCESSOR"

# GitHub alias
GITHUB_ACCESSOR=$(vault auth list -format=json | jq -r '.["github/"].accessor')
vault write identity/entity-alias \
    name="JSmith22" \
    canonical_id="$ENTITY_ID" \
    mount_accessor="$GITHUB_ACCESSOR"
```

After this configuration, any login—UserPass, LDAP, or GitHub—will automatically combine the alias’s policies with the shared `management` policy on the entity.

## Links and References

* [Vault Identity Concepts](https://www.vaultproject.io/docs/concepts/identity)
* [Vault CLI Authentication](https://www.vaultproject.io/docs/commands/auth)
* [Configuring LDAP Auth](https://www.vaultproject.io/docs/auth/ldap)
* [GitHub Auth Method](https://www.vaultproject.io/docs/auth/github)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/eebfb593-8885-43b0-a9ba-9f88af87092e/lesson/7c8e8011-a214-4479-be89-c5eed4009dd3" />
</CardGroup>


# Vault Identity Groups

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Compare-Authentication-Methods/Vault-Identity-Groups/page

This guide explains managing identity groups in HashiCorp Vault, detailing internal and external group types for permission management.

In this guide, you’ll learn how to manage identity groups in HashiCorp Vault. Groups simplify permission management by aggregating entities and nesting subgroups. Vault supports two group types—**internal** and **external**—each tailored for different authentication and authorization workflows.

## Group Basics

A Vault group collects multiple entities and can nest other groups. When you assign policies to a group, all its members inherit those policies upon login. A token’s effective policies are the union of:

1. The entity’s auth method alias
2. The entity’s own policies
3. Any policies from groups (and nested groups) the entity belongs to

| Step | Policy Source     | Example Policy |
| ---- | ----------------- | -------------- |
| 1    | Auth method alias | `superuser`    |
| 2    | Entity            | `management`   |
| 3    | Group membership  | `finance`      |

Consider this scenario:

* **Entities and Aliases**
  * Mariah (`e1`):
    * Entity policy: `accounts-payable`
    * Alias (userpass) policy: `base-user`
  * John Lee (`e2`):
    * Entity policy: `management`
    * Alias (userpass) policy: `superuser`

* **Group**
  * **Finance Team**: policy `finance`, members `e1` and `e2`

When John logs in as `john.lee`, his token combines `superuser`, `management`, and `finance`.

<Frame>
  ![The image illustrates a "Vault Groups" structure, showing members with their entity IDs, policies, and aliases, highlighting how a token inherits capabilities from these elements.](https://kodekloud.com/kk-media/image/upload/v1752878039/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Vault-Identity-Groups/vault-groups-structure-token-capabilities.jpg)
</Frame>

<Callout icon="lightbulb">
  You can nest groups indefinitely. Policies from parent groups cascade to all nested subgroups and members.
</Callout>

## Types of Vault Groups

Vault provides two primary group types:

| Group Type     | Creation Method                                | Typical Use Case                                                                      |
| -------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------- |
| Internal Group | UI, CLI (`vault write`), API                   | Manually defined for consistent permission sets across entities                       |
| External Group | Automatically by auth method or manual mapping | Reflects groups from LDAP, OIDC, Okta, etc., without Vault-side membership management |

<Frame>
  ![The image explains the difference between "Internal Group" and "External Group" in Vault, highlighting their creation methods and purposes. Internal Groups are created manually to propagate identical permissions, while External Groups are inferred and created based on group associations from authentication methods.](https://kodekloud.com/kk-media/image/upload/v1752878040/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Vault-Identity-Groups/internal-external-groups-vault-diagram.jpg)
</Frame>

### Internal Groups and Cross-Segment Configuration

Internal groups are ideal when you centralize authentication but distribute access across Vault namespaces or segments:

1. Enable an auth method (e.g., OIDC) at the root namespace.
2. Map external group `Team-Finance` from your identity provider.
3. Create an internal group (e.g., `finance-internal`) and add `Team-Finance` as a member.
4. Attach segment-specific policies (like `finance-read`, `finance-write`) to the internal group.

<Frame>
  ![The image is a presentation slide about Vault Groups, explaining how internal groups manage permissions and propagate them through Vault Namespaces. It includes a diagram showing the relationship between a root namespace and a child namespace.](https://kodekloud.com/kk-media/image/upload/v1752878042/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Vault-Identity-Groups/vault-groups-permissions-diagram.jpg)
</Frame>

<Callout icon="triangle-alert">
  Ensure that policy names are unique across namespaces to avoid unintended access overlaps when using internal groups with Vault Enterprise namespaces.
</Callout>

### External Groups

External groups let Vault grant permissions based on existing groups in your identity provider. Supported methods include LDAP, Active Directory, Okta, and any OIDC-compliant system. To use:

1. Create an external group in Vault matching the name in your IdP (e.g., `Team-Finance`).
2. Attach Vault policies (for example, `finance-policy`) to that external group.
3. When users authenticate, they are automatically associated with the external group and receive the mapped policies.

<Frame>
  ![The image explains how external groups are used in Vault to set permissions based on group membership from identity providers like LDAP, Okta, or OIDC. It includes a diagram showing the connection between Active Directory and HashiCorp Vault.](https://kodekloud.com/kk-media/image/upload/v1752878043/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Vault-Identity-Groups/vault-external-groups-permissions-diagram.jpg)
</Frame>

## Next Steps

* Practice creating **internal** and **external** groups in the [Vault UI](https://www.vaultproject.io/docs/ui).
* Observe policy inheritance across entities and namespaces.
* Explore advanced topics: [Vault Namespaces](https://www.vaultproject.io/docs/enterprise/namespaces), [Policies](https://www.vaultproject.io/docs/concepts/policies), and [Auth Methods](https://www.vaultproject.io/docs/auth).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/eebfb593-8885-43b0-a9ba-9f88af87092e/lesson/bb25de14-21b1-4aec-8876-5ae099dfbf7d" />
</CardGroup>
