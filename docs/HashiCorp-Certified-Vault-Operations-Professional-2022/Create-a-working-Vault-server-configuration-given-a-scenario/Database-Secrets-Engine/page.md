# Database Secrets Engine

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/Database-Secrets-Engine/page

Vault’s Database Secrets Engine generates dynamic, time-bound credentials for databases, automatically revoking them upon lease expiration to enhance security and reduce risk.

Vault’s Database Secrets Engine generates dynamic, time-bound credentials for a variety of database backends. Each credential is leased, and Vault automatically revokes the user when the lease expires—eliminating stale accounts and reducing risk.

<Frame>
  ![The image is a slide titled "Intro to Database Secrets Engine," explaining how the engine generates dynamic credentials for databases, ties them to a lease, and revokes them upon expiration. It includes a certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878406/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Database-Secrets-Engine/intro-database-secrets-engine-slide.jpg)
</Frame>

## Supported Database Plugins

Vault ships with numerous database plugins out of the box. Below is a selection of popular platforms:

| Database Platform | Use Case                             |
| ----------------- | ------------------------------------ |
| Cassandra         | Distributed NoSQL storage            |
| Couchbase         | In-memory document store             |
| Elasticsearch     | Full-text search & analytics         |
| Microsoft SQL     | Enterprise RDBMS                     |
| Oracle            | High-performance transactional RDBMS |
| MySQL             | Widely-used open-source database     |
| PostgreSQL        | Advanced open-source relational DB   |
| MongoDB           | Flexible document database           |
| Snowflake         | Cloud-native data warehouse          |
| Redshift          | Petabyte-scale analytics             |

<Callout icon="lightbulb">
  If your database isn’t listed, implement a [custom database plugin](https://www.vaultproject.io/docs/secrets/plugins).
</Callout>

<Frame>
  ![The image lists various database plugins for a "Database Secrets Engine," including Cassandra, MongoDB, Oracle, and others. It also features a Vault certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878408/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Database-Secrets-Engine/database-secrets-engine-plugins-list.jpg)
</Frame>

## Configuration Workflow

Setting up the Database Secrets Engine consists of two main steps:

1. Configure Vault’s connection to your database (using a management account).
2. Define Vault roles that map to SQL statements granting the appropriate permissions.

<Frame>
  ![The image outlines two steps for configuring a database secrets engine: configuring Vault with database access and configuring roles based on required permissions. It includes a Vault certification badge and a cartoon character.](https://kodekloud.com/kk-media/image/upload/v1752878409/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Database-Secrets-Engine/database-secrets-engine-configuration-steps.jpg)
</Frame>

### 1. Enable the Engine and Configure a Connection

Enable the secrets engine:

```bash theme={null}
vault secrets enable database
```

Next, register a connection to your database. The following example creates a MySQL backend named `prod-database`:

```bash theme={null}
vault write database/config/prod-database \
    plugin_name=mysql-database-plugin \
    connection_url="{{username}}:{{password}}@tcp(prod.hcvop.com:3306)/" \
    allowed_roles="app-integration,app-hcvop" \
    username="vault-admin" \
    password="vneJ4908fkd3084Bmrk39fmslsl#e&349"
```

* `plugin_name`: selects the plugin (e.g., `mysql-database-plugin`, `mysql-rds-plugin`).
* `connection_url`: uses `{{username}}` and `{{password}}` placeholders.
* `allowed_roles`: limits which Vault roles can issue credentials.
* `username`/`password`: initial credentials Vault uses to manage users (these values are masked on read).

<Frame>
  ![The image illustrates a database secrets engine configuration, showing Vault interacting with multiple databases (prod-sql-01, mysql-dev-03, oracle-db-22) and highlighting the need for credentials.](https://kodekloud.com/kk-media/image/upload/v1752878410/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Database-Secrets-Engine/database-secrets-engine-vault-configuration.jpg)
</Frame>

### 2. Rotate Root Credentials

Regularly rotating root credentials reduces human exposure. Vault’s `rotate-root` endpoint generates new admin credentials and updates the database behind the scenes:

<Frame>
  ![The image is a slide about rotating root credentials, explaining the benefits of using the rotate-root endpoint for database configurations. It highlights compliance with internal policies and ensures only Vault and the database server know the credentials.](https://kodekloud.com/kk-media/image/upload/v1752878411/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Database-Secrets-Engine/rotate-root-credentials-database-configs.jpg)
</Frame>

```bash theme={null}
vault write -f database/rotate-root/prod-database
