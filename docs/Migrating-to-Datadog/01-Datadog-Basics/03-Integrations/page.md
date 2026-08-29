# Integrations

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Datadog-Basics/Integrations/page

Overview of Datadog integrations catalog, data collected, marketplace, and best practices for safe rollout.

In this lesson we explore Datadog’s integrations catalog and how it supports an enterprise observability strategy. A robust observability platform must collect metrics, traces, and logs across the technologies your teams rely on—everything from Redis, SQL databases, and Windows/Ubuntu servers to Java applications—so you can monitor system health, performance, and user-facing behavior.

Below we cover where to find Datadog integrations (documentation and console), what they typically collect, marketplace extensions, and recommended best practices for safe rollout.

Here we are in the [Datadog documentation](https://docs.datadoghq.com/).

<Frame>
  <img alt="The image shows a webpage from Datadog's documentation section, specifically focused on integrations, featuring categories like AI/ML, AWS, and Kubernetes." />
</Frame>

Browsing the catalog

* The Datadog Integrations documentation lists every officially supported integration. You can filter and search by category (for example, AI/ML, cloud providers, orchestration, observability tools).
* Example: filtering on Google Cloud surfaces integrations such as CheckWAF, GigaOm, Google Cloud APIs, and BigQuery—each entry includes setup steps, configuration options, and the data types collected.

Where to enable integrations in the Datadog platform

* From the Datadog console go to Integrations → Integrations to view a platform-side catalog that mirrors the documentation.
* The console also surfaces suggested or autodetected integrations based on telemetry observed from your environment.

<Frame>
  <img alt="The image shows a Datadog integrations dashboard with autodetected and installed integrations like Nginx, SSH, and Docker. It includes various navigation tabs and categories for different services." />
</Frame>

What you’ll find per integration

* Suggested integrations discovered by Datadog based on detected technologies.
* Autodetected and installed integrations (for example, Nginx, SSH, Docker).
* Detailed configuration guides that explain:
  * What the integration collects: metrics, logs, and/or traces.
  * Required Datadog Agent versions and any integration package versions.
  * Authentication and permission requirements (API keys, service accounts, IAM roles).

Integration capabilities at a glance

| Capability           | What to expect                                                        | Examples                                                                    |
| -------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Data types collected | Metrics, traces, logs, and custom events depending on the integration | `nginx`: metrics + logs; `postgres`: metrics + traces (if APM enabled)      |
| Installation surface | Agent-based, API-key-based, or cloud-provider native integration      | Agent on VMs/containers; GCP/AWS integrations via IAM or service accounts   |
| Configuration scope  | Per-host, per-service, or account-level settings                      | Host agent config, Datadog-AWS/GCP integration, or marketplace app settings |
| Requirements         | Agent version, permissions, environment variables, network access     | Agent >= X.Y.Z, API key with write scope, IAM role with read access         |

Full catalog and Marketplace

* The documentation lists the full catalog—everything from 1Password and Active Directory to major cloud providers and managed services.

<Frame>
  <img alt="The image shows a dashboard from Datadog featuring various software integration options like Akamai, Alibaba Cloud, and Amazon Web Services, among others." />
</Frame>

* Datadog’s Marketplace extends functionality with vendor and community-contributed apps. Marketplace items can provide specialized dashboards, CI/CD integrations, or tooling that is not part of core integrations.

<Frame>
  <img alt="The image shows a section of the Datadog marketplace interface displaying various app integrations and tools from different providers, each shown with a card format." />
</Frame>

Best practices for enabling integrations

* Verify Agent and integration package versions against the integration’s documentation before deploying.
* Confirm permissions and credentials (API keys, service accounts, IAM roles) are scoped correctly and follow the principle of least privilege.
* Test in staging with a minimal configuration to validate telemetry collection and avoid noise in production.
* Use the Marketplace for specialized use-cases or vendor-provided integrations that extend core Datadog capabilities.
* Monitor initial data volumes and set appropriate retention/ingestion limits to control cost.

Quick rollout checklist

| Step | Action                                                                  |
| ---- | ----------------------------------------------------------------------- |
| 1    | Review integration docs for version and credential requirements         |
| 2    | Create or scope service accounts / API keys with least privilege        |
| 3    | Deploy to staging with a minimal config and confirm metrics/logs/traces |
| 4    | Validate dashboards and alerts using the collected telemetry            |
| 5    | Roll out to production and monitor ingestion, alerts, and costs         |

> **warning** Misconfigured credentials or excessive permissions can cause missing data or security exposure. Always use scoped service accounts and test in a non-production environment first.

> **lightbulb** Before enabling integrations in production, confirm your Datadog Agent version and the permissions needed (API keys, service accounts, or IAM roles). This prevents partial data collection and permission-related failures.

Links and references

* Datadog Integrations documentation: [https://docs.datadoghq.com/integrations/](https://docs.datadoghq.com/integrations/)
* Datadog Marketplace: [https://www.datadoghq.com/marketplace/](https://www.datadoghq.com/marketplace/)
* Datadog Agent docs: [https://docs.datadoghq.com/agent/](https://docs.datadoghq.com/agent/)
* Redis: [https://redis.io/](https://redis.io/)
* Ubuntu Server: [https://ubuntu.com/server](https://ubuntu.com/server)
* OpenJDK: [https://openjdk.org/](https://openjdk.org/)
* Google Cloud: [https://cloud.google.com/](https://cloud.google.com/)
* CircleCI: [https://circleci.com/](https://circleci.com/)
* Ansible: [https://www.ansible.com/](https://www.ansible.com/)

That covers the essentials of Datadog integrations—where to find them, what they collect, marketplace options, and safe rollout practices. This concludes the lesson. I hope you found it useful; see you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/10421186-d141-4fde-9847-73ea4e4e675a/lesson/1b92b0b0-78a7-4b7e-9e7a-785dde12db8d)
