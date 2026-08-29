# Schemas Why Schemas Matter

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Transforming-Telemetry-Pipeline-Processing/Schemas-Why-Schemas-Matter/page

Explains OpenTelemetry schemas and how schema_url provides a versioned contract enabling producers and consumers to evolve independently without breaking dashboards alerts or downstream tools.

This lesson explains OpenTelemetry (OTel) schemas, why they matter, and how `schema_url` provides a versioned contract that helps producers and consumers evolve independently without breaking dashboards, alerts, or downstream tools.

Producers are the application SDKs that generate telemetry (traces, metrics, logs) and send it downstream. Telemetry items include attributes such as `http.status_code` and `service.name` defined by OTel semantic conventions. When telemetry is emitted without a schema reference (`schema_url`), it’s common — but it leaves no explicit, machine-readable way to indicate how many attributes exist, when an attribute name changes, or how attributes map across versions.

Over time attribute names and meanings can evolve. For example, `http.status_code` might be renamed to `http.response.status_code` to clarify that the value refers specifically to the response. Producers can include a `schema_url` so the data becomes self-describing and version-aware.

Here is a typical span payload that includes the newer attribute name and a schema reference at the resource level:

```json theme={null}
{
  "name": "GET",
  "context": {
    "trace_id": "0x3cf644517d2321004cad06b5e5a99c9",
    "span_id": "0xec7c96bee62b1f12",
    "trace_state": "[]"
  },
  "kind": "SpanKind.CLIENT",
  "parent_id": null,
  "start_time": "2025-10-11T04:03:17.505814Z",
  "end_time": "2025-10-11T04:03:20.917103Z",
  "status": {
    "status_code": "UNSET"
  },
  "attributes": {
    "http.method": "GET",
    "http.url": "http://httpbin.org/delay/2",
    "http.response.status_code": 200
  },
  "events": [],
  "links": [],
  "resource": {
    "attributes": {
      "telemetry.sdk.language": "python",
      "telemetry.sdk.name": "opentelemetry",
      "telemetry.sdk.version": "1.37.0",
      "service.name": "payment.service"
    },
    "schema_url": "https://opentelemetry.io/schema/1.1.0"
  }
}
```

<Frame>
  <img alt="The image illustrates schema evolution, showing the transition of http.status_code to http.response.status_code and the addition of a schema_url from an empty string to &#x22;https://opentelemetry.io/schema/1.1.0&#x22;." />
</Frame>

Originally telemetry had no schema defined. Later it referenced `https://opentelemetry.io/schemas/1.1.0`. Both the attribute name and the schema reference evolved, making the data self-describing and version-aware.

Producers and consumers evolve at different speeds: attribute names change, new attributes are added, and old ones are renamed. Without a declared contract, dashboards and alerts can break when they expect an attribute name that no longer exists. Schemas provide that contract — they declare names and meanings so producers can evolve independently while consumers continue to read and interpret the data.

<Frame>
  <img alt="The image illustrates &#x22;Schemas as Contracts Between Producers and Consumers,&#x22; showing a schema file as a contract detailing names, meaning, and structure. Producers and consumers rely on this schema to facilitate communication and compatibility." />
</Frame>

The schema file acts as a bridge from the data producers emit to the systems that visualize or query it downstream. Consider this example payload emitted by a producer:

```json theme={null}
{
  "service.name": "payment-service",
  "http.response.status_code": 200
}
```

If a dashboard or alert still queries `http.status_code`, it will not find that attribute and the visualization may appear broken (greyed out). To avoid a wholesale coordinated change across many producers and consumers, introduce a schema file that declares how names changed. For example, a `1.1.0` schema might express this rename:

```yaml theme={null}
file_format: 1.1.0
schema_url: https://opentelemetry.io/schemas/1.1.0
versions:
  - version: 1.1.0
    changes:
      - rename_attributes:
          from: http.status_code
          to: http.response.status_code
```

With such a schema, consumers or intermediaries can automatically translate between versions: map incoming attributes to the names dashboards expect, or update dashboards to understand new names. With both producers and consumers referencing the same schema, the dashboard works again without changing every producer.

> **lightbulb** Schemas decouple producers and consumers by providing a versioned contract for attribute names and meanings. This enables safe, incremental evolution of telemetry without breaking downstream systems.

> **warning** If you do not adopt schemas or a mapping strategy, dashboards, alerts, and queries that rely on specific attribute names are at risk of breaking when those names change. Consider adding `schema_url` to your producers and validating schema-aware mappings in pipelines.

Key benefits of using OTel schemas

| Benefit                 | What it solves                                                        | Example                                                          |
| ----------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Versioned contract      | Prevents breaking changes when attributes are renamed or restructured | Map `http.response.status_code` to `http.status_code` via schema |
| Automatic translation   | Enables pipelines to transform attributes for legacy consumers        | Pipeline maps new attribute names to old queries                 |
| Clear evolution history | Documents when and why changes occurred                               | `versions` section in schema YAML records renames and additions  |
| Better interoperability | Helps multiple teams and tools read telemetry consistently            | SDKs, observability tools, and dashboards align on semantics     |

How to adopt schemas (practical steps)

1. Add `schema_url` to your producers (SDKs or instrumentation).
2. Publish or reference a schema file that records renames, additions, and breaking changes.
3. Update pipelines (collectors, processors) to consult the schema and perform attribute mapping where necessary.
4. Gradually update dashboards and consumers to use the newer attribute names; rely on schema mappings during the transition.

References and further reading

* OpenTelemetry Schemas: [https://opentelemetry.io/docs/reference/specification/schemas/](https://opentelemetry.io/docs/reference/specification/schemas/)
* OpenTelemetry Semantic Conventions: [https://opentelemetry.io/docs/reference/specs/semantic\_conventions/](https://opentelemetry.io/docs/reference/specs/semantic_conventions/)
* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)

Now that you understand why schemas matter, design producers and pipelines to include schema references so consumers can remain compatible as the telemetry data model evolves.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/85787c66-c021-47d9-bd3d-db54bc002465/lesson/8efc0cff-8139-475c-9600-8970cb10b39e)
