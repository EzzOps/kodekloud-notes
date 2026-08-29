# 1. Login and capture JWT
curl -s -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# 2. Attempt logout (if no endpoint exists)
curl -i -X POST http://localhost:3000/api/auth/logout \
  -H "Authorization: Bearer eyJ..."
# 3. Verify token remains valid until expiry
curl -i -X GET http://localhost:3000/api/protected \
  -H "Authorization: Bearer eyJ..."
# If valid, protected route responds 200 OK — indicates no server-side invalidation
```

***

## Prioritization & remediation roadmap

Top fixes to reduce risk fast:

| Priority | Action                                                                                 | Duration  |
| -------- | -------------------------------------------------------------------------------------- | --------- |
| P0       | Replace weak/hard-coded JWT secrets with a strong random secret and enforce min length | Immediate |
| P0       | Implement token blacklisting (Redis) for revocation                                    | Immediate |
| P1       | Add refresh token pattern with HttpOnly secure cookies                                 | Week 1    |
| P1       | Add logout that revokes access and refresh tokens                                      | Week 1    |
| P2       | Add CSRF protection if cookies are used                                                | Week 2    |
| P2       | Move any session state to Redis or a DB-backed store (no memory store in prod)         | Week 2–4  |

Suggested timeline:

* Immediate: JWT secret rotation and token blacklisting.
* Week 1: Refresh tokens + secure cookie patterns and logout.
* Week 2: CSRF controls and session store adoption.
* Month 1: Session monitoring, adaptive timeouts, and device tracking.

***

## Compliance impact

The audit mapped findings to common frameworks:

* OWASP Top 10: A07:2021 (Identification and Authentication Failures) — applicable due to lack of revocation and long-lived tokens.
* PCI DSS / SOC 2 / NIST: Insufficient session invalidation and access management controls may impact compliance posture.

***

## Closing notes

* JWT-only architectures reduce some cookie risks but require operational controls: revocation, refresh, and secure storage.
* If you introduce cookies later, ensure Secure, HttpOnly, and SameSite flags and add CSRF protection.
* Break audits into focused checks (sessions, cookies, CSRF, storage) to produce actionable, prioritized findings and reduce missed items.

Upcoming topics will cover file handling and business logic audits.

## Links and references

* [OWASP Top 10 — Authentication Failures](https://owasp.org/Top10/)
* [Express Session Documentation](https://www.npmjs.com/package/express-session)
* [csurf middleware](https://www.npmjs.com/package/csurf)
* [jsonwebtoken](https://www.npmjs.com/package/jsonwebtoken)
* [node-redis client](https://www.npmjs.com/package/redis)

- [Watch Video](https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/eaf75a67-f28f-4217-a3f9-92d411403129/lesson/de194ae1-791f-4364-9686-c6938882ec80)


# Demo Database Security Audit

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Security-Auditing-with-Claude-Code/Demo-Database-Security-Audit/page

A database security audit of an Express login demo identifying vulnerabilities and recommending prioritized fixes for TLS, secrets, queries, permissions, logging, and tenant isolation.

This lesson walks through a database security audit for an Express login demo application. The objective is to inspect every database interaction, surface security gaps, and produce prioritized remediation steps so the app can be safely promoted to production.

Initial CLI session used to launch the auditing tool:

```bash theme={null}
jeremy@MACSTUDIO Express-login-demo % claude

* Welcome to Claude Code!

/help for help, /status for your current setup

cwd: /Users/jeremy/Repos/Claude Code Course/Express-login-demo

> Try "how does <filepath> work?"

? for shortcuts

In INPUT_VALIDATION_SECURITY_REPORT.md
```

We follow a structured checklist covering parameterized queries, secret management, permissions, encryption, PII controls, timeouts/pools, and audit/logging.

<Frame>
  <img alt="A dark-themed Visual Studio Code window with a file explorer on the left and a central terminal/editor pane showing a database security checklist (parameterized queries, connection string security, user permissions, encryption, PII handling, timeouts, connection pool settings, etc.). The project file tree and a highlighted security report file are visible in the sidebar." />
</Frame>

## High-level audit focus areas

* Parameterized queries / safe ORM usage to prevent SQL/NoSQL injection
* Connection string protection, TLS/SSL, and secret management
* Database user permissions (principle of least privilege)
* Encryption at rest and TLS in transit
* PII handling, retention, and logging hygiene
* Query timeouts, connection-pool limits, and transaction discipline
* Audit logging for sensitive operations and schema changes
* NoSQL injection hardening and row/tenant isolation for multi-tenant apps

Principle of least privilege: give each DB account only the privileges it needs — separate read-only, migration, and admin accounts; avoid SUPERUSER-level credentials unless explicitly required.

We verify that critical fields are minimized, encrypted or tokenized where needed, and that PII is redacted from logs.

Example checklist items (condensed):

* Verify parameterized queries or ORM APIs are used instead of concatenating user input.
* Ensure connection strings and credentials are stored in a secrets manager and rotated.
* Confirm DB connections use TLS/SSL (validate server certificate).
* Validate query timeouts and pool limits are configured at driver and server levels.
* Confirm audit logging for schema and privilege changes, failed logins, and sensitive table access.
* Enforce row-level security (or server-side tenant scoping) for multi-tenant data isolation.

<Frame>
  <img alt="A Visual Studio Code window with the explorer on the left and a text file open in the main pane. The file shows a numbered security checklist covering items like audit logging, NoSQL injection hardening, row/tenant isolation, TLS, secret management, and schema controls." />
</Frame>

## Row / tenant isolation

* Enforce server-side row-level security (e.g., Postgres RLS: [https://www.postgresql.org/docs/current/ddl-rowsecurity.html](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)) or strict ownership/tenant filters in queries.
* Never rely on client-side filtering for multi-tenant isolation — always scope queries server-side.

## NoSQL sanitization (Mongoose example)

For MongoDB/Mongoose, avoid passing raw user input directly into query filters:

```javascript theme={null}
// For Mongoose, enable sanitizeFilter to avoid passing raw user input into query filters
const mongoose = require('mongoose');
mongoose.set('sanitizeFilter', true);
```

See Mongoose migration docs for sanitizeFilter: [https://mongoosejs.com/docs/migration.html#sanitizeFilter](https://mongoosejs.com/docs/migration.html#sanitizeFilter)

## TLS / secret management and schema controls to check

* DB connections must use TLS/SSL (for Postgres: use `sslmode=require` or `verify-full`; see Postgres libpq SSL mode docs: [https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE)).
* Store credentials in a secrets manager (e.g., AWS Secrets Manager: [https://aws.amazon.com/secrets-manager/](https://aws.amazon.com/secrets-manager/), HashiCorp Vault: [https://www.vaultproject.io/](https://www.vaultproject.io/)) and rotate them periodically.
* Do not commit plaintext passwords in `.env`. Keep a `.env.example` for local development only. (See the dotenv package: [https://www.npmjs.com/package/dotenv](https://www.npmjs.com/package/dotenv))
* Enforce foreign keys, unique constraints, and NOT NULL where appropriate.
* Avoid `SELECT *` — always fetch only the required fields.

### Example: enabling SSL/TLS in node-postgres Pool (illustrative)

```javascript theme={null}
// javascript
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT || 5432),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  // Connection pool limits and timeouts
  max: Number(process.env.DB_POOL_MAX || 20),
  idleTimeoutMillis: Number(process.env.DB_IDLE_TIMEOUT || 30000),
  connectionTimeoutMillis: Number(process.env.DB_CONN_TIMEOUT || 5000),
  // TLS options (for production)
  ssl: {
    rejectUnauthorized: true, // ensure server certificate is validated
    // ca: process.env.DB_SSL_CA, // if using a custom CA
  },
});
```

See node-postgres pooling docs: [https://node-postgres.com/features/pooling](https://node-postgres.com/features/pooling)

<Frame>
  <img alt="A dark-themed Visual Studio Code window showing a project explorer on the left and an editor/terminal pane with a security-audit checklist for an Express app in the center. The text highlights critical flags (e.g., direct string concatenation) and lists a structured findings/report template." />
</Frame>

## Critical flags to watch for

* Direct string concatenation with user input in SQL or NoSQL queries — extremely high severity.
* Passing user JSON directly into NoSQL query filters without sanitization (see OWASP NoSQL Injection: [https://owasp.org/www-community/attacks/NoSQL\_Injection](https://owasp.org/www-community/attacks/NoSQL_Injection)).
* Hard-coded credentials or placeholder secrets committed to the repository (e.g., `JWT_SECRET=your_jwt_secret_key_here`, `DB_PASSWORD=your_db_password`).

## Useful audit commands (examples)

* Search for environment files and secrets:

```bash theme={null}
