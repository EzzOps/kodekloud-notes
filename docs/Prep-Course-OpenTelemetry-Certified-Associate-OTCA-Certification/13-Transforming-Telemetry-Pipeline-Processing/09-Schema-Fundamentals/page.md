# Example (cross-language env vars per spec)
export OTEL_TRACES_SAMPLER=parentbased_traceidratio
export OTEL_TRACES_SAMPLER_ARG=0.10  # sample 10% of traces at the SDK (when parent decision allows)
```

> **lightbulb** Sampling at the SDK reduces network and backend load, but it discards data early. If you need sampling decisions based on full-trace results (errors, latency spikes, or aggregated attributes), consider sampling later in the pipeline (the Collector).

If the SDK does not sample, or if you need enrichment/normalization before deciding, the OpenTelemetry Collector is a powerful place to apply sampling. The Collector can receive telemetry from many SDKs, augment traces with transforms, and make more informed sampling decisions.

<Frame>
  <img alt="The image is a diagram illustrating a data flow process titled &#x22;From SDK to Collector – Why Sample Again, Where OTTL Helps,&#x22; featuring components such as Receiver, OTTL Transform, and Sampling Processor with Head and Tail Samplers." />
</Frame>

Transforms in the Collector (using OTTL) let you enrich telemetry so sampling policies can use attributes like error flags, tenant IDs, or latency labels. Example: set an error flag and copy a tenant attribute into spans before sampling.

```yaml theme={null}
processors:
  transform/normalize:
    error_mode: ignore
    traces:
      statements:
        - set(span.attributes["error.flag"], span.status.code == "STATUS_CODE_ERROR")
        - set(span.attributes["tenant"], resource.attributes["tenant"]) where
          resource.attributes["tenant"] != nil
```

After transforms, telemetry flows through processors that can include sampling processors before export.

Two fundamental Collector sampling approaches:

<Frame>
  <img alt="The image illustrates a process involving &#x22;Head vs Tail Sampling in the Collector,&#x22; featuring a &#x22;Processor (Sampling)&#x22; leading to &#x22;Head Sampling&#x22; and &#x22;Tail Sampling&#x22; options, with descriptions of each method." />
</Frame>

Table: Collector sampling comparison

| Approach      | How it works                                                                                                              | Pros                                                                                                  | Cons                                                                       |
| ------------- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Head sampling | Decide as spans arrive at the Collector (per-span or per-trace probabilistic policies based on partial info)              | Low memory & CPU, fast, scalable                                                                      | Cannot use full-trace outcomes (may miss important traces)                 |
| Tail sampling | Buffer and assemble a trace (or wait for a decision signal) and then evaluate the entire trace before keeping or dropping | Outcome-aware (keep traces with errors/latency/patterns), more accurate retention of important traces | Requires buffering, more memory and CPU, complexity in distributed systems |

> **warning** Tail sampling improves retention of high-value traces but increases memory and processing needs in the Collector. Plan capacity, timeouts, and resource limits carefully to avoid buffering overload.

When to choose which:

* Use SDK or Collector head sampling for lightweight, probabilistic reduction when you only need volume control.
* Use Collector tail sampling when you must make outcome-based decisions (for example, retain all traces that contain errors or unusually high latency).
* Combine approaches: use SDK sampling to reduce baseline volume and tail sampling in the Collector for application-level exceptions or multi-service error patterns.

References and further reading

* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* OTTL (OpenTelemetry Transformation Language) docs: [https://opentelemetry.io/docs/collector/processing/transform/](https://opentelemetry.io/docs/collector/processing/transform/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/85787c66-c021-47d9-bd3d-db54bc002465/lesson/5222f050-3143-492f-afd6-56c62ef81fba)


# Schema Fundamentals

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Transforming-Telemetry-Pipeline-Processing/Schema-Fundamentals/page

Explains OpenTelemetry telemetry schemas, schema_url usage, semantic versioning, and how schema-aware transforms in collectors and backends translate attributes to maintain compatibility.

A telemetry schema is a versioned changelog that documents semantic-convention changes (renames, additions, deprecations) for telemetry signals. Each schema file records what changed and is stored under a predictable path such as `/schema/version`. Backends, processors, and collectors use the `schema_url` embedded in telemetry to interpret and transform incoming data correctly over time.

Example schema file (YAML):

```yaml theme={null}
file_format: 1.1.0
schema_url: https://opentelemetry.io/schemas/1.1.0
versions:
  - version: 1.1.0
    changes:
      - rename_attributes:
          - from: http.status_code
            to: http.response.status_code
```

The `schema_url` within telemetry has two important parts:

* family name (groups the logical set of schema versions)
* semantic version (MAJOR.MINOR.PATCH)

If a schema host changes, the URL may redirect to a new location, allowing consumers to discover the rules for the referenced schema version.

<Frame>
  <img alt="The image illustrates the structure of schema URLs, showing how a base URL is combined with a family and version number. It also mentions the inclusion of redirects." />
</Frame>

Embedding `schema_url` makes telemetry self-describing. Example telemetry JSON:

```json theme={null}
{
  "schema_url": "https://opentelemetry.io/schemas/1.1.0",
  "resource": {
    "service.name": "payment.service"
  }
}
```

Typical schema files list changes in order and can target scopes: `all`, `spans`, `metrics`, etc. Example schema with scoped changes:

```yaml theme={null}
schema_url: https://opentelemetry.io/schemas/1.1.0
versions:
  - version: 1.1.0
    all:
      rename_attributes:
        - from: http.status_code
          to: http.response.status_code
    spans:
      add_attributes:
        - key: telemetry.source
          value: "payment-service"
    metrics:
      remove_attributes:
        - key: deprecated.metric.id
```

Table: Schema scope mappings

| Scope     | Purpose                                        | Example change                                                               |
| --------- | ---------------------------------------------- | ---------------------------------------------------------------------------- |
| `all`     | Applies to every signal (spans, metrics, logs) | `rename_attributes: {from: http.status_code, to: http.response.status_code}` |
| `spans`   | Only affects span attributes                   | `add_attributes: [{key: telemetry.source, value: "payment-service"}]`        |
| `metrics` | Only affects metric attributes                 | `remove_attributes: [{key: deprecated.metric.id}]`                           |

Semantic versioning determines compatibility and consumer behavior. Follow [SemVer](https://semver.org) rules: patch releases are ignorable structural fixes, minor versions add backward-compatible rules, and major versions introduce potentially breaking changes. Tools should read schema files up to the minor version they support; newer minors or different majors may contain rules they don't understand.

<Frame>
  <img alt="The image outlines &#x22;SemVer Rules for Schemas,&#x22; describing three versioning types: MAJOR for incompatible changes, MINOR for backward-compatible additions, and PATCH for ignorable additions. It also specifies consumer behavior for version changes." />
</Frame>

> **lightbulb** Consumers can safely read schema files with the same major version and a minor version less than or equal to the minor they support. Patch differences are always safe.

Compatibility examples (quick reference):

| File version                     | Consumer version | Compatible? | Notes                                               |
| -------------------------------- | ---------------- | ----------: | --------------------------------------------------- |
| `1.1.0` vs `1.1.0`               | `1.1.0`          |         Yes | Exact match                                         |
| `1.0.1` vs `1.0.9`               | `1.0.x`          |         Yes | Patch-only differences are compatible               |
| file `1.1.x` vs consumer `1.3.x` | `1.x`            |         Yes | Newer consumer can read an older minor              |
| file `1.3.x` vs consumer `1.1.x` | `1.x`            |          No | File minor newer than consumer — consumer is behind |
| file `2.0.0` vs consumer `1.x.y` | major differs    |          No | Breaking changes possible                           |

Concrete example

* An SDK emits spans and metrics with `schema_url = https://opentelemetry.io/schemas/1.2.0`. Each span contains `deployment.environment = "prod"`.
* In schema `1.1.0` the same attribute was named `environment`.
* If the backend stores data using `1.1.0`, incoming `1.2.0` telemetry must be transformed before storage so the backend remains consistent.

<Frame>
  <img alt="The image is a diagram of a schema-aware observability system showing the flow of telemetry data from a source through a backend to storage, with schema transformation and translation rules applied. It includes a transformation of &#x22;deployment.environment&#x22; to &#x22;environment&#x22; in the storage phase." />
</Frame>

How translation preserves user experience

* SDK emits telemetry using the new schema (`1.2.0`) and queries or dashboards are written against `deployment.environment`.
* Storage uses `environment` with `schema_url = 'https://opentelemetry.io/schemas/1.1.0'`.
* A schema-aware query layer rewrites user-facing queries to match storage semantics.

Example user query (written against `1.2.0`):

```sql theme={null}
SELECT * FROM Spans WHERE deployment.environment = 'prod';
```

Translated storage query (rewritten to backend schema):

```sql theme={null}
SELECT * FROM Spans WHERE environment = 'prod' AND schema_url = 'https://opentelemetry.io/schemas/1.1.0';
```

Collector example (schema translation at the edge)

1. Developers configure their SDKs normally and emit spans/metrics under `1.2.0` (e.g., `deployment.environment = "prod"`).
2. Telemetry is sent to an OpenTelemetry Collector instead of directly to the backend.
3. The Collector runs a schema-transform processor configured with a target `schema_url` (for example, `https://opentelemetry.io/schemas/1.1.0`).
4. The processor consults both the incoming `1.2.0` rules and the target `1.1.0` rules to determine renames and rewrites.
5. The Collector outputs telemetry where attribute names and the `schema_url` match the target `1.1.0` format, then forwards it to the backend.

Because the Collector performs translation before storage, the backend receives consistent, target-schema-compliant payloads and does not need to perform per-item rewrites.

Summary

* Schema files are versioned declarations of semantic changes (renames, additions, deprecations).
* The telemetry `schema_url` makes data self-describing and enables correct interpretation across the pipeline.
* Follow semantic versioning: patches are safe, minors are backward-compatible additions, majors may break.
* Schema transforms (in the Collector or backend) map attributes between versions so storage and queries remain consistent across schema evolution.

Links and references

* [OpenTelemetry Collector documentation](https://opentelemetry.io/docs/collector/)
* [Semantic Versioning (SemVer)](https://semver.org)
* [OpenTelemetry Schemas (reference)](https://opentelemetry.io/schemas/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/85787c66-c021-47d9-bd3d-db54bc002465/lesson/fdd9d476-02e7-4e94-83d3-513278463bb7)
