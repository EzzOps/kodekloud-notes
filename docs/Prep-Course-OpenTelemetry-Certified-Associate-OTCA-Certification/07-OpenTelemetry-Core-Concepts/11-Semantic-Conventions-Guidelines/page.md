# Semantic Conventions Guidelines

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Core-Concepts/Semantic-Conventions-Guidelines/page

Guidelines for using OpenTelemetry semantic conventions to name and reuse attributes for spans metrics and logs to ensure interoperability correlation and consistent analysis across systems

In this lesson we explain how to define consistent names and attributes in OpenTelemetry for spans, metrics, logs, and other telemetry signals. Using established semantic conventions ensures your telemetry is interoperable, easier to analyze, and simpler to correlate across systems.

> **lightbulb** Always prefer the established OpenTelemetry semantic conventions. Reusing standardized attribute names ensures interoperability and consistent analysis across traces, metrics, and logs.

## Why reuse matters

* Consistency: Standard attribute names allow tools and analysts to interpret telemetry without custom mappings.
* Correlation: Shared attributes make it straightforward to correlate traces, metrics, and logs across services.
* Compatibility: Instrumentation libraries, exporters, and backends expect common attribute names and semantics.

## Naming pattern

OpenTelemetry semantic attributes typically use a structured, dot-separated namespace to provide clear meaning. A common pattern is:

`[domain].[entity].[attribute]`

Note: Not every convention includes all three segments; some attributes use `domain.attribute` or other variations depending on the domain. Use the style appropriate to the specific semantic convention for that domain.

## Examples

Below are common OpenTelemetry semantic attributes, their meanings, and guidance on when to use them.

| Attribute                       | Meaning                                              | Usage / Notes                                                                                                                                                           |
| ------------------------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `http.method`                   | HTTP request method (e.g., GET, POST)                | Read as domain (`http`) and attribute (`method`). Use for HTTP spans and logs.                                                                                          |
| `db.name`                       | Name of the database or schema                       | Useful for database monitoring and correlating DB operations. Some DB-specific conventions exist (e.g., MongoDB may have additional keys like `db.mongodb.collection`). |
| `service.name`                  | Identifier for the service                           | Core resource attribute used to correlate traces, metrics, and logs for a service instance.                                                                             |
| `net.peer.ip` / `net.peer.port` | Network address components of the peer (IP and port) | Use `net.*` attributes instead of inventing a combined attribute for remote endpoints.                                                                                  |
| `exception.type`                | Classifies the exception type                        | Use alongside `exception.message` and `exception.stacktrace` for richer error context and grouping.                                                                     |
| `k8s.pod.uid`                   | Kubernetes Pod unique identifier (UID)               | `k8s` is used as the Kubernetes shorthand namespace. Use Kubernetes semantic keys where available.                                                                      |

## Best practices

* Reuse existing attributes: Before creating a new key, check the OpenTelemetry semantic conventions for an authoritative name.
* Prefer resource attributes for global information (e.g., `service.name`) and span attributes for operation-specific context.
* Use the structured namespace to keep attributes discoverable and consistent (e.g., `http.*`, `db.*`, `net.*`, `k8s.*`).
* When additional context is needed, prefer adding contextual values to existing conventions rather than inventing new keys.
* Document any organization-specific conventions in a central place and map them to OpenTelemetry keys for compatibility.

> **lightbulb** Tip: Instrumentation libraries and many backends provide mappings for common semantic conventions—reuse those mappings where possible to reduce engineering effort and improve interoperability.

## Where to find the conventions

Consult the official OpenTelemetry semantic conventions specification and related resources before defining new attributes:

* [OpenTelemetry Semantic Conventions specification](https://opentelemetry.io/specs/otel/semantic_conventions/)
* [OpenTelemetry Documentation](https://opentelemetry.io/)
* [OpenTelemetry Semantic Conventions repository](https://github.com/open-telemetry/opentelemetry-specification/tree/main/semantic_conventions)

These resources provide domain-specific guidance and the authoritative names to use across spans, metrics, and logs. When in doubt, prefer the standardized attribute names to maintain consistency across teams, tools, and platforms.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/da1c735f-c606-45b0-9bbf-04fe366fbd23/lesson/365b53ad-668f-476d-9449-2b7a3b1caf43)
