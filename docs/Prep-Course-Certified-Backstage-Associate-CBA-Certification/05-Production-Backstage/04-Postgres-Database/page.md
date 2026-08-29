# Set Python interpreter for `node-gyp` to use
ENV PYTHON=/usr/bin/python3
# Install isolate-vm dependencies, these are needed by the @backstage/plugin-scaffolder-backend.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 g++ build-essential && \
    rm -rf /var/lib/apt/lists/*
# Install sqlite3 dependencies. You can skip this if you don't use sqlite3 in the image,
# in which case you should also move better-sqlite3 to "devDependencies" in package.json.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*
# From here on we use the least-privileged `node` user to run the backend.
USER node
# This should create the app dir as `node`.
# If it is instead created as `root` then the `tar` command below will fail: 'can't create directory `packages/`: Permission denied'.
# If this occurs, then ensure BuildKit is enabled ('DOCKER_BUILDKIT=1') so the app dir is correctly created as `node`.
WORKDIR /app
# Copy files needed by Yarn
COPY --chown=node:node .yarn ./.yarn
COPY --chown=node:node .yarnrc.yml ./
COPY --chown=node:node backstage.json ./
# This switches many Node.js dependencies to production
ENV NODE_ENV=production
# This disables node snapshot for Node 20 to work with the Scaffolder.
ENV NODE_OPTIONS="--no-node-snapshot"
# Copy repo skeleton first, to avoid unnecessary docker cache invalidation.
# The skeleton contains the package.json of each package in the monorepo,
# and along with yarn.lock and the root package.json, that's enough to run yarn install.
COPY --chown=node:node yarn.lock package.json packages/backend/dist/skeleton.tar.gz ./
RUN tar xzf skeleton.tar.gz && rm skeleton.tar.gz
RUN --mount=type=cache,target=/home/node/.cache/yarn,sharing=locked,uid=1000,gid=1000 \
    yarn workspaces focus --all --production && rm -rf "$(yarn cache clean)"
# This will include the examples, if you don't need these simply remove this line
COPY --chown=node:node examples ./examples
# Then copy the rest of the backend bundle, along with any other files we might want.
COPY --chown=node:node packages/backend/dist/bundle.tar.gz app-config*.yaml ./
RUN tar xzf bundle.tar.gz && rm bundle.tar.gz
CMD ["node", "packages/backend", "--config", "app-config.yaml", "--config", "app-config.production.yaml"]
```

## Prepare the repository (local or CI)

Before running a Docker build, produce the backend artifacts the Dockerfile expects. Run these steps locally or replicate them in your CI pipeline.

1. Install dependencies

* Use Yarn v3+ (Backstage uses Yarn Berry). Install in immutable mode so the lockfile is enforced:

```bash theme={null}
yarn install --immutable
```

2. Generate TypeScript types

* Compile or type-check to ensure any generated types are available:

```bash theme={null}
yarn tsc
```

3. Build the backend bundle

* Produce the `bundle.tar.gz` and `skeleton.tar.gz` artifacts under `packages/backend/dist`.

Option A — build the whole monorepo (recommended):

```bash theme={null}
yarn build
```

Option B — build only the backend package:

```bash theme={null}
# Use your workspace name if different, e.g.:
yarn workspace @backstage/backend build
```

After these steps confirm:

* `packages/backend/dist/bundle.tar.gz`
* `packages/backend/dist/skeleton.tar.gz`

exist in your repo root (or in the CI build context).

## Important: Docker BuildKit

<Callout icon="warning">
  Make sure Docker BuildKit is enabled when building this Dockerfile (see [https://docs.docker.com/develop/develop-images/build\_enhancements/](https://docs.docker.com/develop/develop-images/build_enhancements/)). BuildKit is required for the `--mount=type=cache` and certain ownership behaviors used in the Dockerfile. You can enable it by setting `DOCKER_BUILDKIT=1` in your build environment.
</Callout>

BuildKit is required for mount caching and for correct ownership handling that the Dockerfile relies on. In CI, enable BuildKit or use a builder (kaniko/buildah) that supports these Dockerfile features.

## Build the Docker image

From the repository root (so the `packages/backend/dist` artifacts are in context), run:

```bash theme={null}
DOCKER_BUILDKIT=1 docker build -f packages/backend/Dockerfile -t backstage:latest .
```

Notes:

* `-f packages/backend/Dockerfile` specifies the Dockerfile path.
* The final `.` is the build context (typically the repo root).
* `DOCKER_BUILDKIT=1` enables BuildKit features.

## Run the container locally

By default the Backstage backend listens on port 7000. Run the container and map the port:

```bash theme={null}
docker run --rm -p 7000:7000 backstage:latest
```

If you override or provide additional configuration files at runtime, either include them in the image during build or mount them at runtime. The generated CMD expects `app-config.yaml` and `app-config.production.yaml` to be present in the container.

## Quick reference table

| Task                 | Command / Path                                                                        | Notes                                                     |
| -------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Dockerfile location  | `packages/backend/Dockerfile`                                                         | The generated Dockerfile used to build the backend image. |
| Install dependencies | `yarn install --immutable`                                                            | Requires Yarn v3 (Berry).                                 |
| Generate types       | `yarn tsc`                                                                            | Ensures TypeScript artifacts are available.               |
| Build monorepo       | `yarn build`                                                                          | Produces `packages/backend/dist/bundle.tar.gz`.           |
| Build image          | `DOCKER_BUILDKIT=1 docker build -f packages/backend/Dockerfile -t backstage:latest .` | Build context must include `packages/backend/dist`.       |
| Run container        | `docker run --rm -p 7000:7000 backstage:latest`                                       | Adjust ports/config if necessary.                         |

## CI/CD considerations

* Reproduce the local preparation steps in your CI pipeline: install dependencies, run `yarn tsc`, and create the `dist` artifacts.
* Ensure the CI runner enables Docker BuildKit or uses an alternative builder that supports the Dockerfile mount features.
* Push the built image to your container registry and deploy through your preferred orchestrator (Kubernetes, AWS ECS, etc.).
* For multi-stage or automated pipelines, make sure the build context (or artifacts archive) includes `packages/backend/dist` so the Dockerfile COPY steps succeed.

## Links and references

* Backstage documentation: [https://backstage.io/docs](https://backstage.io/docs)
* Docker BuildKit: [https://docs.docker.com/develop/develop-images/build\_enhancements/](https://docs.docker.com/develop/develop-images/build_enhancements/)
* Yarn v3 (Berry): [https://yarnpkg.com/getting-started](https://yarnpkg.com/getting-started)
* Kubernetes: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* Amazon ECS: [https://aws.amazon.com/ecs/](https://aws.amazon.com/ecs/)

This sequence packages your Backstage backend into a production-ready Docker image, following recommended practices for reproducible builds and CI/CD.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/d82fc857-4b5c-42a7-ab46-3772f749a741/lesson/24aeb58f-e979-44e3-802d-917e6b7531a8" />
</CardGroup>


# Postgres Database

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Production-Backstage/Postgres-Database/page

Guide to configuring Backstage to use a persistent PostgreSQL database, updating app-config, running migrations, and following production best practices for credentials, backups, and secure connections

In this lesson we cover how to configure Backstage to use a persistent PostgreSQL database instead of the default ephemeral stores used in many local or development setups.

By default Backstage often runs with an in-memory database (or a local SQLite file in some templates). That means any entities or state you create while Backstage runs are temporary — they are lost when the process stops or restarts. For production and long-lived environments, use a persistent database such as Postgres to retain entities, settings, and application state across restarts.

<Frame>
  <img alt="A slide titled &#x22;Managing Data in Backstage&#x22; comparing two environments: a Development Environment using an in-memory database (stacked server icon) and a Production Environment using a Postgres database (elephant logo). The slide notes the in-memory DB is temporary and lost on restart, while Postgres provides persistent storage." />
</Frame>

Overview — steps to configure Backstage with Postgres:

1. Provision a Postgres instance (local container, Docker Compose, or a managed cloud database).
2. Update Backstage's `app-config.yaml` to point to the Postgres instance.
3. Initialize the database schema by running Backstage database migrations.
4. Start Backstage with the environment variables or configuration in place so it can connect to Postgres.

Configuration example

Add a `backend.database` section under your backend configuration in `app-config.yaml`. This tells Backstage to use the `pg` client (node-postgres) and to read connection details from environment variables:

```yaml theme={null}
backend:
  database:
    client: pg
    connection:
      host: ${POSTGRES_HOST}
      port: ${POSTGRES_PORT}
      user: ${POSTGRES_USER}
      password: ${POSTGRES_PASSWORD}
      database: ${POSTGRES_DB}
```

Common connection options explained:

| Field      | Purpose                                     | Example                                 |
| ---------- | ------------------------------------------- | --------------------------------------- |
| `host`     | Hostname or IP of the Postgres server       | `db.example.internal`                   |
| `port`     | TCP port used by Postgres (default: `5432`) | `5432`                                  |
| `user`     | Username Backstage will use to connect      | `backstage_user`                        |
| `password` | Password for the user                       | (set via environment or secret manager) |
| `database` | The database name on the Postgres server    | `backstage`                             |

You can supply a single connection string instead of individual fields:

```yaml theme={null}
backend:
  database:
    client: pg
    connection: postgres://user:password@host:5432/database
```

Or use an environment variable for the connection string:

```yaml theme={null}
backend:
  database:
    client: pg
    connection: ${DATABASE_URL}
```

<Callout icon="lightbulb">
  After configuring the connection, run Backstage's database migrations to create required tables and schemas. The exact migration command depends on your repository (check package.json scripts or README). Run migrations before starting Backstage in production to avoid runtime schema errors.
</Callout>

Best practices and operational notes

* Use strong credentials and store them in a secrets manager or environment variables — do not commit credentials to source control.
* Restrict network access to the database (VPCs, security groups, or private networks).
* Enable SSL/TLS for connections when using remote or managed Postgres services.
* Regularly back up your Postgres data and test restore procedures.
* For production, prefer a managed or highly available Postgres offering (for example, AWS RDS, Google Cloud SQL, or a clustered deployment).

<Callout icon="warning">
  Do not run production Backstage against an ephemeral or in-memory database. Data loss can occur on process restarts. Also ensure your migration strategy is part of your deployment pipeline to avoid schema drift.
</Callout>

Quick reference — example environment variable names

| Env var             | Purpose                                                          |
| ------------------- | ---------------------------------------------------------------- |
| `POSTGRES_HOST`     | Postgres hostname                                                |
| `POSTGRES_PORT`     | Postgres port (usually `5432`)                                   |
| `POSTGRES_USER`     | Username for Backstage DB connection                             |
| `POSTGRES_PASSWORD` | Password for the user                                            |
| `POSTGRES_DB`       | Database name Backstage will use                                 |
| `DATABASE_URL`      | Full connection string, e.g. `postgres://user:pass@host:5432/db` |

Links and references

* [PostgreSQL](https://www.postgresql.org/)
* [Backstage](https://backstage.io/)
* [node-postgres (pg)](https://node-postgres.com/)
* [AWS RDS for PostgreSQL](https://aws.amazon.com/rds/postgresql/)
* [Google Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres)

With the database configured and migrations applied, Backstage will persist entities and other state to Postgres instead of using an ephemeral in-memory store.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/d82fc857-4b5c-42a7-ab46-3772f749a741/lesson/cdb1de6b-4cdd-4d3d-b3cb-6786ac4117a6" />
</CardGroup>
