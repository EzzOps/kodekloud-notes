# Tailoring Your Configuration

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-Structuring-your-Platform/Tailoring-Your-Configuration/page

Guidance to configure Datadog Agent to reduce costs, control metric cardinality, filter and mask logs, and enforce explicit, auditable collection rules.

This guide explains how to tailor your Datadog Agent configuration before deploying it. It focuses on Agent-level optimizations for collection, shipment, filtering, masking, and cost control. Platform-specific deployment details (Kubernetes, Docker, cloud providers) are out of scope, but these Agent-centric best practices apply across environments.

Objectives:

* Reduce unnecessary ingestion and storage costs.
* Prevent sensitive data from being sent to Datadog.
* Keep metric cardinality in check.
* Make collection rules explicit and auditable.

## High-level goals

* Reduce log volume and exclude or mask sensitive data before ingestion.
* Limit metric collection and manage cardinality to control costs.
* Configure an appropriate Agent log level so the Agent does not create excess logs.
* Make collection, filters, and tags explicit so you collect only what you need.

> **lightbulb** Start with conservative collection rules. Enable additional sources, higher verbosity, or broader scraping only when you need them for troubleshooting. Incrementally expand data collection after validating cost and usefulness.

## Agent-level settings

Set basic Agent options in `datadog.yaml` so behavior is explicit and predictable.

Example (`datadog.yaml`):

```yaml theme={null}
