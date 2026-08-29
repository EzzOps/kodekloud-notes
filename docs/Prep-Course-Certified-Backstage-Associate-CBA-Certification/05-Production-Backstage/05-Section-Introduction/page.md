# Section Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Production-Backstage/Section-Introduction/page

Guide to deploying Backstage to production, covering PostgreSQL migration, OIDC authentication, Docker containerization, Kubernetes deployment, backups, upgrades, and operational best practices.

In this lesson we'll walk through deploying a production-grade Backstage instance. The goal is to move your app from a local developer environment (which typically uses an in-memory or SQLite database and minimal auth) into a resilient, secure, and maintainable production deployment.

What you'll learn and implement:

| Area                   | Why it matters                                                     | Typical target                                           |
| ---------------------- | ------------------------------------------------------------------ | -------------------------------------------------------- |
| Database               | Persistent, scalable storage for catalogs, identities, and plugins | Managed `Postgres` (e.g., AWS RDS, Cloud SQL)            |
| Authentication         | Secure access control so only authorized users can sign in         | OIDC / SSO via Okta, Google, Azure AD, GitHub, etc.      |
| Packaging              | Consistent runtime environment for deployment and upgrades         | Docker image + container orchestration (Kubernetes, ECS) |
| Maintenance & Upgrades | Safe upgrade paths and operational best practices                  | Version pinning, backups, health checks, monitoring      |

This lesson is practical and focused on concrete, production-ready changes:

* Replace the default development database (in-memory/SQLite) with a production-grade PostgreSQL database.
* Implement authentication (require users to sign in before using Backstage).
* Package Backstage into a Docker container and outline deployment options.
* Discuss upgrade strategies, backups, and routine maintenance tasks.

Prerequisites

* A working Backstage app used for local development.
* Basic familiarity with Docker and PostgreSQL (or access to a managed Postgres service).
* Access to an identity provider for configuring OIDC or SSO (e.g., Okta, Google Workspace, Azure AD).

> **lightbulb** This lesson is intended for readers who already have a Backstage app set up for local development. The default development database (in-memory or SQLite) is convenient for local testing but is not suitable for production—use a managed PostgreSQL instance or an equivalent production-grade database instead.

Links and references

* Backstage documentation: [https://backstage.io/docs](https://backstage.io/docs)
* PostgreSQL: [https://www.postgresql.org/](https://www.postgresql.org/)
* Docker: [https://www.docker.com/](https://www.docker.com/)
* Kubernetes: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* OIDC / OAuth resources: [https://oauth.net/](https://oauth.net/) and your identity provider docs

Next steps

Proceed to the database migration section to replace the development DB with PostgreSQL, then configure authentication and containerization. Each step includes configuration snippets, sample Dockerfiles, and recommended production settings.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/d82fc857-4b5c-42a7-ab46-3772f749a741/lesson/10148bbb-c4d2-42f6-82d2-c677c0e1b0ea)
