# Success! Data written to: database/rotate-root/prod-database
```

## Defining Roles

Roles define the SQL statements Vault runs to create and grant permissions to a dynamic user. Each role is tied to a configured database connection.

<Frame>
  ![The image illustrates a "Database Secrets Engine - Roles" concept, showing a central icon connected to three databases labeled "prod-sql-01," "oracle-db-22," and "mysql-dev-03," with a note to configure roles based on required permissions. A cartoon character is also present in the bottom right corner.](https://kodekloud.com/kk-media/image/upload/v1752878412/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Database-Secrets-Engine/database-secrets-engine-roles-diagram.jpg)
</Frame>

### Example: Dynamic Role

This example creates an `app-hcvop` role that grants read-only access:

```bash theme={null}
vault write database/roles/app-hcvop \
    db_name="prod-database" \
    creation_statements="CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}';
                         GRANT SELECT ON *.* TO '{{name}}'@'%';" \
    default_ttl="1h" \
    max_ttl="24h"
```

* `db_name`: references the database config (`prod-database`).
* `creation_statements`: templated SQL for creating and granting privileges.
* `default_ttl` / `max_ttl`: control lease duration and renewability.

<Frame>
  ![The image illustrates a diagram of a Database Secrets Engine, showing roles and their permissions required for accessing different databases. It includes a list of roles and arrows indicating access paths to various database servers.](https://kodekloud.com/kk-media/image/upload/v1752878413/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Database-Secrets-Engine/database-secrets-engine-roles-permissions-diagram.jpg)
</Frame>

### Static Roles

For applications that require a fixed username (e.g., `ecommerce_user`), use a **static role**. Vault will only rotate the password, preserving the username—ideal for legacy or COTS software.

## Password Policies

Vault auto-generates strong passwords by default (20 characters, mixed case, numbers, dash). You can attach a custom Vault policy to match your database’s requirements.

<Frame>
  ![The image outlines password policies for databases, specifying a default policy of 20 characters with at least one uppercase, one lowercase, one number, and one dash. It also notes that credentials from different plugins may vary based on the platform.](https://kodekloud.com/kk-media/image/upload/v1752878414/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Database-Secrets-Engine/password-policies-database-credentials-outline.jpg)
</Frame>

<Callout icon="triangle-alert">
  Ensure your password policy adheres to backend constraints such as maximum length and allowed characters.
</Callout>

## Generating Dynamic Credentials

Applications request credentials by reading from the role’s path. Vault creates the user, returns the credentials, and sets the lease TTL:

<Frame>
  ![The image illustrates the process of generating dynamic credentials using a database secrets engine, involving a Vault, a web application, and a database table. It shows the flow of requests and credentials between these components, with a focus on security and credential expiration.](https://kodekloud.com/kk-media/image/upload/v1752878416/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Database-Secrets-Engine/dynamic-credentials-database-secrets-engine.jpg)
</Frame>

```bash theme={null}
vault read database/creds/app-hcvop

Key              Value
---              -----
lease_id         database/creds/app-hcvop/abc123
lease_duration   1h
lease_renewable  true
username         V_VAULTUSE_APP_HCVOP_XYZ123
password         yRUSyd-vPYDg5NkU9kDg
```

Once the lease expires, Vault automatically revokes the database user.

## Vault Policy for Credential Generation

Grant your application’s Vault token permission to read from `database/creds/<role>`:

```hcl theme={null}
# Allow generating credentials for app-hcvop
path "database/creds/app-hcvop" {
  capabilities = ["read"]
}
```

Adjust policies per role to enforce least privilege.

***

With Vault’s Database Secrets Engine, you can automate the lifecycle of database credentials—improving security, simplifying audits, and eliminating long-lived static accounts.

## Links and References

* [Vault Database Secrets Engine](https://www.vaultproject.io/docs/secrets/databases)
* [HashiCorp Vault Documentation](https://www.vaultproject.io/docs/)
* [Custom Database Plugin](https://www.vaultproject.io/docs/secrets/plugins)
* [Vault Secrets Engines Overview](https://www.vaultproject.io/docs/secrets)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/0f2caef8-381e-4725-85dc-7512758c66f6" />
</CardGroup>


# Demo Database Secrets Engine

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Demo-Database-Secrets-Engine/page

This guide explains how to configure HashiCorp Vault’s Database Secrets Engine for managing dynamic PostgreSQL credentials in AWS RDS.

In this guide, you’ll learn how to enable and configure HashiCorp Vault’s Database Secrets Engine to manage dynamic credentials for a PostgreSQL database running in AWS RDS. We’ll cover:

1. Verifying enabled secrets engines
2. Enabling the Database Secrets Engine
3. Configuring the database connection
4. Creating a dynamic role
5. Rotating root credentials
6. Generating dynamic credentials
7. Revoking leases and cleanup

***

## Prerequisites

* A running Vault server (`vault status` returns OK)
* Network connectivity from Vault to your RDS instance (security group, firewall)
* AWS RDS PostgreSQL endpoint, admin username, and password

***

## 1. Verify Enabled Secrets Engines

Start by listing all secrets engines currently enabled:

```bash theme={null}
vault secrets list
```

Expected output:

```text theme={null}
Path         Type        Accessor           Description
----         ----        --------           -----------
aws/         aws         aws_9de29d31       n/a
cubbyhole/   cubbyhole   cubbyhole_772dff42 per-token private secret storage
identity/    identity    identity_8efc4dd9  identity store
sys/         system      system_5d807a2a    system endpoints used for control, policy and debugging
```

The `database/` engine should **not** appear yet.

***

## 2. Enable the Database Secrets Engine

Enable the database engine at its default mount path:

```bash theme={null}
vault secrets enable database
```

You should see:

```text theme={null}
Success! Enabled the database secrets engine at: database/
```

Verify it’s listed:

```bash theme={null}
vault secrets list
```

```text theme={null}
Path         Type        Accessor          Description
----         ----        --------          -----------
aws/         aws         aws_9de29d31      n/a
cubbyhole/   cubbyhole   cubbyhole_772dff42 per-token private secret storage
database/    database    database_123abc   n/a
identity/    identity    identity_8efc4dd9 identity store
sys/         system      system_5d807a2a   system endpoints used for control, policy and debugging
```

***

## 3. Configure the Database Connection

Create a Vault “database configuration” named `hcvop-db` that points to your AWS RDS PostgreSQL instance:

```bash theme={null}
vault write database/config/hcvop-db \
    plugin_name=postgresql-database-plugin \
    allowed_roles="hcvop-demo-role" \
    connection_url="postgresql://{{username}}:{{password}}@postgres01.cxojwmhweukf.us-east-1.rds.amazonaws.com:5432/" \
    username="postgres" \
    password="vaultdemo123"
```

| Parameter         | Description                                                                              | Example                                                      |
| ----------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| plugin\_name      | The database plugin to use                                                               | postgresql-database-plugin                                   |
| allowed\_roles    | Roles permitted to generate credentials via this connection                              | hcvop-demo-role                                              |
| connection\_url   | Template URL with placeholders for the admin credentials                                 | `postgresql://{{username}}:{{password}}@your-rds-host:5432/` |
| username/password | Admin credentials Vault will use to manage the database (rotations, user creation, etc.) | postgres / vaultdemo123                                      |

Success message:

```text theme={null}
Success! Data written to: database/config/hcvop-db
```

To inspect the saved configuration:

```bash theme={null}
vault read database/config/hcvop-db
```

```text theme={null}
Key                       Value
---                       -----
allowed_roles             [hcvop-demo-role]
connection_url            postgresql://{{username}}:{{password}}@postgres01.cxojwmhweukf.us-east-1.rds.amazonaws.com:5432/
plugin_name               postgresql-database-plugin
password_policy           n/a
root_credentials_rotate_statements []
```

<Callout icon="lightbulb">
  Vault does **not** show the stored `username` and `password` for security reasons.
</Callout>

***

## 4. Create a Dynamic Role

A Vault “role” defines how dynamic users are created and what permissions they have:

```bash theme={null}
vault write database/roles/hcvop-demo-role \
    db_name="hcvop-db" \
    default_ttl="4h" \
    max_ttl="24h" \
    creation_statements="
      CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';
      GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";
    "
```

* **db\_name**: Must match the configuration name (`hcvop-db`).
* **default\_ttl/max\_ttl**: Time-to-live for generated credentials.
* **creation\_statements**: SQL executed to create a new user with permissions.

Verify the role:

```bash theme={null}
vault read database/roles/hcvop-demo-role
```

```text theme={null}
Key                   Value
---                   -----
creation_statements   [CREATE ROLE "{{name}}" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO "{{name}}";]
db_name               hcvop-db
default_ttl           4h
max_ttl               24h
```

***

## 5. Rotate the Root Credentials

Regularly rotating your admin credentials reduces risk:

```bash theme={null}
vault write -f database/rotate-root/hcvop-db
```

```text theme={null}
Success! Data written to: database/rotate-root/hcvop-db
```

<Callout icon="triangle-alert">
  After rotation, the old admin credentials become invalid immediately. Update any systems relying on these credentials.
</Callout>

***

## 6. Generate Dynamic Credentials

Applications can now request short-lived credentials:

```bash theme={null}
vault read database/creds/hcvop-demo-role
```

```text theme={null}
Key             Value
---             -----
lease_id        database/creds/hcvop-demo-role/sTmzKcBPw1uGOygvuPpc4i3i
lease_duration  4h
lease_renewable true
username        v-root-hcvop-de-Mop0jmV6qCkFhmuT6ftu-1652122668
password        wzpc9Br-CTAuvZw-aS50
```

These credentials automatically expire after the TTL unless renewed.

***

## 7. Revoke Leases and Cleanup

### Revoke a Single Lease

```bash theme={null}
vault lease revoke database/creds/hcvop-demo-role/sTmzKcBPw1uGOygvuPpc4i3i
```

### Revoke All Leases for a Role

```bash theme={null}
vault lease revoke -prefix database/creds/hcvop-demo-role
```

Vault will run the appropriate SQL to drop the dynamic users in your database.

***

## References

* [Vault Database Secrets Engine](https://www.vaultproject.io/docs/secrets/databases)
* [AWS RDS for PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)
* [HashiCorp Vault CLI](https://www.vaultproject.io/docs/commands)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/91b40042-d98d-48e8-be99-8b4c8d78e92b" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/b59936f2-3ed0-4ec2-b1fd-971dcce5c2ca/lesson/974a425b-c165-4ef1-b492-9c8935d70a39" />
</CardGroup>
