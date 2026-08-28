# Semantic Conventions

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Core-Concepts/Semantic-Conventions/page

Explains OpenTelemetry semantic conventions for consistent telemetry attribute naming to improve correlation, simplify querying, and enable vendor neutral observability across traces, metrics, logs, and resources.

Hello telemetry explorers — welcome back.

In this lesson we'll cover semantic conventions: what they are, why they matter, and where to find the official OpenTelemetry definitions. By the end you should understand how consistent attribute naming improves correlation, query simplicity, and vendor-neutral observability.

Imagine two services sending telemetry to the same backend. Service A emits an attribute named `http.status_code` with value `200` and `user.id` with value `ID-01`. Another team emits the same concepts but with different keys: `status_code` (no `http.` prefix) and `userId` (camelCase).

<Frame>
  <img alt="The image is a diagram showing different services and applications (Service A, Service B, Application 1, Application 2) with their respective data keys and values, all connecting to an &#x22;Observability backend.&#x22;" />
</Frame>

If the backend stores these attributes as-is, it may recognize `http.status_code` as an HTTP status (because it follows a known convention), while `status_code` becomes a custom key and is treated differently. Likewise, `user.id` might be recognized, but `userId` or `userid` may be treated as arbitrary fields.

This fragmentation—different names for the same concept—makes it difficult to correlate traces, metrics, and logs, and complicates dashboarding, alerting, and automated analysis.

<Frame>
  <img alt="The image is a table titled &#x22;Fragmented Data, Broken Insights&#x22; with columns for Key, Data, Value, and Description, showing three entries related to HTTP status code, custom data, and user ID." />
</Frame>

When teams use inconsistent attribute names you end up writing multiple queries or creating mapping logic in the backend—both increase operational overhead and reduce effective observability.

<Frame>
  <img alt="The image presents a problem of fragmented data leading to broken insights caused by inconsistent naming and difficulty correlating traces, metrics, and logs. It highlights the issues of different teams naming the same concept differently and the challenge of correlating services." />
</Frame>

The result: dashboards that miss data, alert rules that are incomplete or duplicated, and brittle queries that break when naming varies.

<Frame>
  <img alt="The image illustrates the impact of fragmentation on observability, showing that it leads to reduced observability and increased operational overhead, using icons of data, magnifying glass, and upward graphs." />
</Frame>

What’s the solution? Semantic conventions.

Semantic conventions are a set of recommended attribute names and usage rules defined by the OpenTelemetry specification. They cover traces, metrics, logs, resources, and more. By adopting them, instrumentation across languages and libraries becomes consistent—enabling reliable correlation, simpler queries, and vendor-neutral interoperability.

Key benefits:

* Enable correlation across telemetry signals (traces, metrics, logs).
* Simplify querying and analysis.
* Ensure consistent instrumentation across teams and vendors.
* Improve interoperability with backends like [Prometheus](https://prometheus.io/), [Jaeger](https://www.jaegertracing.io/), and commercial observability platforms.

<Frame>
  <img alt="The image illustrates the value of semantic conventions in four points: enabling correlation across telemetry signals, simplifying querying and analysis, ensuring consistent instrumentation, and improving interoperability with certain backends." />
</Frame>

Why do semantic conventions matter? They eliminate naming inconsistencies so dashboards, alerts, and automation are reliable and resilient across teams and tools.

<Frame>
  <img alt="The image explains the importance of semantic conventions, highlighting their role in solving inconsistency problems, powering correlation and automation, and enabling vendor-neutral observability." />
</Frame>

Because different teams or vendors might otherwise name the same attribute in different ways, having a common foundation is essential. That is why semantic conventions are a core part of the OpenTelemetry specification.

Where semantic conventions apply

* Resource attributes: describe the entity producing telemetry (hosts, containers, cloud provider, service name).
* Operation/span attributes: HTTP requests/responses, RPCs, database calls, messaging operations.
* Event fields: metadata attached to span events (exceptions, retries, state changes).
* Logs: standardized log fields such as `log.message`.
* Metrics: recommended metric names and units.
* General attributes: cross-cutting identifiers like trace IDs and span IDs.

<Frame>
  <img alt="The image is a diagram titled &#x22;Semantic Conventions Landscape,&#x22; depicting different attributes and fields related to operations and resources, including Resource Attributes, Operation/Span Attributes, Event Fields, Logs, Metrics, and General Attributes. Each section briefly describes its purpose." />
</Frame>

Table: Where to apply semantic conventions

| Category                    | What it describes                                     | Example attribute(s)                  |
| --------------------------- | ----------------------------------------------------- | ------------------------------------- |
| Resource attributes         | Entity producing telemetry (service, host, container) | `service.name`, `host.id`             |
| Operation / Span attributes | Details of operations (HTTP, RPC, DB, messaging)      | `http.method`, `db.system`            |
| Event fields                | Additional event-level metadata inside spans          | `exception.type`, `exception.message` |
| Logs                        | Standardized log fields for structured logging        | `log.message`, `log.severity`         |
| Metrics                     | Recommended metric names and units                    | `process.cpu.utilization`             |
| General / Cross-cutting     | Identifiers and correlation fields                    | `trace_id`, `span_id`                 |

Common domain examples (canonical attribute names)

* HTTP: `http.method`, `http.status_code`
* RPC: `rpc.system`, `rpc.method`
* Messaging: `messaging.system`, `messaging.operation`
* Database: `db.system`, `db.statement`
* Exceptions/events: `exception.type`, `exception.message`
* Operating system: `os.type`, `os.version`
* Cloud: `cloud.provider`, `cloud.region`

Note on user identity: OpenTelemetry prefers `enduser.*` attributes (for example `enduser.id`) rather than ad-hoc names like `userId`.

<Frame>
  <img alt="The image is a table showing examples of domains and their corresponding attributes, covering areas such as HTTP, RPC, Messaging, Database, Exceptions, and OS." />
</Frame>

Where to find the official list

* OpenTelemetry semantic conventions docs: [https://opentelemetry.io/docs/reference/specification/semantic\_conventions/](https://opentelemetry.io/docs/reference/specification/semantic_conventions/)
* GitHub repository (semantic\_conventions folder): [https://github.com/open-telemetry/opentelemetry-specification/tree/main/semantic\_conventions](https://github.com/open-telemetry/opentelemetry-specification/tree/main/semantic_conventions)

The documentation covers many domains (HTTP, databases, messaging, cloud providers, CI/CD, GraphQL, and more) and specifies attribute names, types, and semantics.

<Frame>
  <img alt="The image shows a webpage from the OpenTelemetry documentation detailing the semantic conventions version 1.37.0, including a list of areas where these conventions are defined, such as CICD, Cloud Providers, and GraphQL." />
</Frame>

If you use official instrumentation libraries or auto-instrumentation, many of these attributes are applied for you. You do not need to memorize every attribute, but become familiar with common conventions and consult the docs when adding custom attributes or manual instrumentation.

<Callout icon="lightbulb">
  You don’t need to memorize every semantic attribute. Use the official OpenTelemetry instrumentation libraries and consult the semantic conventions documentation when defining custom attributes or manual instrumentation.
</Callout>

Summary — key takeaways

* OpenTelemetry uses semantic conventions to address inconsistent telemetry naming across teams and vendors.
* Semantic conventions standardize attributes across signals (traces, metrics, logs) and domains (HTTP, RPC, messaging, DB, exceptions, cloud, etc.).
* Following these conventions makes correlation reliable, queries simpler, and observability vendor-neutral and easier to maintain.

<Frame>
  <img alt="The image outlines key takeaways from Semantic Conventions, highlighting OpenTelemetry's role in standardizing telemetry across various domains and categories to ensure consistency. It emphasizes standardized attributes for traces, metrics, and logs." />
</Frame>

Further reading and references

* OpenTelemetry specification — semantic conventions: [https://opentelemetry.io/docs/reference/specification/semantic\_conventions/](https://opentelemetry.io/docs/reference/specification/semantic_conventions/)
* OpenTelemetry instrumentation: [https://opentelemetry.io/docs/instrumentation/](https://opentelemetry.io/docs/instrumentation/)
* OpenTelemetry GitHub — semantic\_conventions folder: [https://github.com/open-telemetry/opentelemetry-specification/tree/main/semantic\_conventions](https://github.com/open-telemetry/opentelemetry-specification/tree/main/semantic_conventions)

That’s it for this section.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/da1c735f-c606-45b0-9bbf-04fe366fbd23/lesson/55ac3503-fecf-40db-bb78-185a6354ad7a" />
</CardGroup>
