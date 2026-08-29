# Demo Note About Backstage Database

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Backstage-Basics/Demo-Note-About-Backstage-Database/page

Explains Backstage development database behavior, transient in-memory or SQLite storage, and how to configure PostgreSQL for persistent catalog data across restarts.

A brief but important note about how Backstage stores catalog data during development.

By default, a development Backstage backend uses a local, non-production database. Depending on how your template is configured, this might be an in-memory store or a lightweight SQLite instance. That means when you add an application, component, or other catalog entity, the data may be transient — stored only in memory or a temporary local file — and will be lost when the backend process is restarted.

This transient behavior is intentional and convenient for iterating quickly: you can prototype without setting up a production-grade database. For staging or production environments (or when you want persistence across restarts during development), Backstage is typically configured to use PostgreSQL as the backing store.

Why persistence matters

* Prevents loss of added entities across backend restarts.
* Allows multiple developer or CI environments to share a consistent catalog.
* Required for production-grade Backstage deployments.

Quick comparison

| Storage Type   | Description                                                                               | Typical use case                                                            |
| -------------- | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| In-memory      | Volatile, fastest for tests. Data lost on restart.                                        | Short-lived demos and ephemeral tests                                       |
| SQLite (local) | Lightweight file-based store. May be used by some templates. Not intended for production. | Simple local development where persistence between restarts is not required |
| PostgreSQL     | Production-ready relational DB. Requires schema migrations.                               | Staging and production, or persistent local development                     |

Minimal PostgreSQL configuration

Add this to your `app-config.yaml` to point Backstage at a PostgreSQL instance:

```yaml theme={null}
backend:
  database:
    client: pg
    connection: postgres://backstage:backstage@localhost:5432/backstage
```

After configuring Postgres, you must run the backend database migrations to initialize the schema. Migration commands can vary by Backstage version and your project setup — see the Backstage documentation for the exact commands and steps for your repository.

Recommended steps to enable persistent storage

1. Start or provision a PostgreSQL instance (local Docker, managed service, etc.).
2. Update `app-config.yaml` with the Postgres connection string (see example above).
3. Run the backend database migrations (follow the Backstage docs).
4. Restart the Backstage backend. Entities added in the UI will now persist across restarts.

<Callout icon="lightbulb">
  If your components or services disappear after restarting the backend, you are almost certainly running with the default local/development database (in-memory or SQLite). For the rest of this course we keep the transient setup to simplify demos. When you need persistence, follow the Postgres configuration and migration steps in the [Backstage documentation](https://backstage.io/docs/).
</Callout>

From a teaching perspective, the transient dev database is useful because it gives a clean slate each session and avoids stale test data. If you'd like persistent state during development without provisioning a remote database, run a local PostgreSQL (for example via Docker) and point Backstage at it using the configuration above.

Further resources

* Backstage docs: [https://backstage.io/docs/](https://backstage.io/docs/)
* PostgreSQL: [https://www.postgresql.org/](https://www.postgresql.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/fcbbf923-69c3-4147-bd51-18db2bd18957/lesson/635dfd83-bc8b-439e-a272-31dfd777686d" />
</CardGroup>
