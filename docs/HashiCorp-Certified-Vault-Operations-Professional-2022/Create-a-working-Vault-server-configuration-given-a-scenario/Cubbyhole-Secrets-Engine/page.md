# Cubbyhole Secrets Engine

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Cubbyhole-Secrets-Engine/page

Vault’s Cubbyhole Secrets Engine provides isolated storage for secrets, ensuring each token has a private compartment that is destroyed upon expiration or revocation.

Vault’s **Cubbyhole Secrets Engine** offers isolated, per-token storage for secrets. Just like kindergarten cubbies, each token gets its own private compartment: when the token is revoked or expires, its cubbyhole and all its contents are destroyed. No other token—even the root token—can access another token’s cubbyhole.

<Callout icon="lightbulb">
  The Cubbyhole engine is automatically enabled at the `cubbyhole/` path. It cannot be disabled, relocated, or instantiated multiple times.
</Callout>

<Frame>
  ![The image is an introduction slide about the Cubbyhole Secrets Engine, explaining its default settings, token linkage, and restrictions on disabling or moving it.](https://kodekloud.com/kk-media/image/upload/v1752878397/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Cubbyhole-Secrets-Engine/cubbyhole-secrets-engine-introduction-slide.jpg)
</Frame>

Imagine each basket below represents a token’s private cubbyhole. When the token’s TTL ends or it’s revoked, its basket—and everything inside—vanishes.

<Frame>
  ![The image illustrates the concept of service tokens having individual cubbyholes, with each token stored separately and inaccessible to others, and notes that cubbyholes expire with the tokens.](https://kodekloud.com/kk-media/image/upload/v1752878399/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Cubbyhole-Secrets-Engine/service-tokens-cubbyholes-expiration-illustration.jpg)
</Frame>

## Viewing and Using Cubbyhole

You don’t need to enable Cubbyhole—it’s always available. Verify it with:

```bash theme={null}
vault secrets list
```

Example output:

```text theme={null}
Path          Type       Accessor                  Description
----          ----       ---------                 -----------
cloud/        kv         kv_dd590f0e
cubbyhole/    cubbyhole  cubbyhole_9c6c2ca2       per-token private secret storage
identity/     identity   identity_e55fbf01        n/a
kv/           kv         kv_ed482380              n/a
kvv2/         kv         kv_0559442e              n/a
```

### CLI: Write and Read

Use KV v1–style commands:

```bash theme={null}
