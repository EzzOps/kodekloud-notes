# global scope
from google.cloud import firestore
db = firestore.Client()

def hello_http(request):
    doc = db.collection('visits').document('counter')
    # use shared db client
    return 'ok'
```

Table: Performance tactics at a glance

| Tactic              | Why it helps              | Implementation tip                              |
| ------------------- | ------------------------- | ----------------------------------------------- |
| Reduce package size | Faster startup            | Remove unused packages, bundle/minify code      |
| Global clients      | Lower connection overhead | Create DB / HTTP clients outside handlers       |
| Lazy loading        | Avoid heavy startup cost  | Import heavy modules inside handler when needed |
| Right-size memory   | Balance latency and cost  | Benchmark with representative workloads         |

## Error handling and reliability

Assume failures are normal. Design to handle transient and permanent errors, and to fail in observable ways.

Best practices:

* Retries: Use exponential backoff with jitter to avoid thundering herds. Do not blindly retry non-idempotent operations.
* Dead letter queues (DLQs): Preserve messages that repeatedly fail via dead-letter topics/subscriptions for later inspection or reprocessing.
* Idempotency: Make operations idempotent where possible to prevent duplicate side effects during retries.
* Observability: Log errors, failed events, and context. Use structured logs, metrics, and traces for faster troubleshooting.

You can often configure event sources (for example, Pub/Sub) to route undeliverable messages to a dead-letter topic. Alternatively, publish failed events explicitly from your function to a DLQ for manual or automated reprocessing.

Implementation patterns and examples:

| Pattern           | Example                                                                           |
| ----------------- | --------------------------------------------------------------------------------- |
| Retry with jitter | Use exponential backoff + randomization to reduce synchronized retries            |
| DLQ handling      | Configure Pub/Sub dead-letter topic or publish failed events to a dedicated topic |
| Idempotency keys  | Include a deduplication ID (e.g., request ID) and persist processed IDs           |

Example pseudocode for exponential backoff with jitter:

```text theme={null}
wait = base * (2 ** attempt)
jitter = random_between(0, wait * 0.1)
sleep(wait + jitter)
```

## Security: least privilege and secret handling

Hardening your functions reduces exposure and prevents accidental data leaks.

Core security practices:

* Principle of least privilege: Grant service accounts only the permissions required for the function.
* Secrets management: Never commit secrets to source code. Use a managed secret service and grant functions minimal access to fetch secrets at runtime.
* Network controls: Use VPC connectors, private IPs, and firewall rules when accessing internal resources.
* Input validation and sanitization: Validate inputs to reduce attack surface and avoid injection attacks.

> **lightbulb** Store secrets in a managed secret service (for example, Secret Manager) and fetch them at runtime. Avoid embedding credentials in source code or storing API keys in plaintext environment variables—use secret-manager integrations where possible.

Quick question

Which practice improves Cloud Functions performance when connecting to a database?

* Option A: create a new connection on every request.
* Option B: use global variables for connection pooling.
* Option C: store credentials inside the function.

Correct answer: B. Using global variables for connection pooling enables connection reuse and reduces per-invocation setup time.

## Advanced tips for power users

* Use global variables for shared clients and connection pools to avoid repeated connection setup.
* When implementing retries, combine exponential backoff with jitter to avoid causing spikes that overload downstream services.
* Monitor functions with Cloud Monitoring and send logs to Cloud Logging. Use distributed tracing (Cloud Trace) to analyze end-to-end latency and hotspots.
* Benchmark different memory allocations—more memory can yield better performance for CPU-bound tasks, but increases cost. Measure tail latency, not just averages.

<Frame>
  <img alt="A slide titled &#x22;Pro Tips&#x22; with five colorful rounded boxes across the bottom. The boxes list tips like &#x22;Use global variables for connections,&#x22; &#x22;Implement exponential backoff,&#x22; &#x22;Monitor with Cloud Monitoring,&#x22; &#x22;Use Cloud Trace for debugging,&#x22; and &#x22;Set appropriate memory limits.&#x22;" />
</Frame>

> **warning** Be mindful of the cost/performance trade-off when increasing memory. Benchmark different settings because allocating more memory increases cost and may also change CPU allocation.

## Observability checklist

* Emit structured logs with sufficient context (request IDs, trace IDs).
* Create metrics for invocation count, error rate, latency, and cold-start frequency.
* Set alerts on error rate spikes, high latencies, or sudden cost increases.
* Correlate traces across services using Cloud Trace or OpenTelemetry.

## References and further reading

* [Cloud Functions documentation](https://cloud.google.com/functions/docs)
* [Cloud Monitoring](https://cloud.google.com/monitoring)
* [Secret Manager](https://cloud.google.com/secret-manager)
* [Pub/Sub dead-letter topics](https://cloud.google.com/pubsub/docs/dead-letter-topics)
* [Best practices for serverless applications](https://cloud.google.com/architecture/serverless-best-practices)

That covers the key best practices for Cloud Functions performance, reliability, and security.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/ff8693f0-36fe-4cca-9b05-f27ffa81ccb4/lesson/bfce5c03-9335-4bc9-9469-e370f6fe7d60)


# Cloud Functions Real World Integration Examples

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Orchestration-Options/Cloud-Functions-Real-World-Integration-Examples/page

Practical integration patterns using Google Cloud Functions to implement event-driven ETL, database streaming, IoT telemetry processing, and serverless APIs with operational guidance for production.

Welcome back. In this lesson we explore practical, production-ready integration patterns using Google Cloud Functions. These patterns show how serverless functions glue cloud services together to implement automated workflows, real-time pipelines, and lightweight APIs — all with minimal operational overhead.

We’ll walk through four common, real-world scenarios using an example Tesla service application. Different parts of that system react to events: a file upload from a support tool, a customer updating contact info, streaming telemetry from cars, or a mobile app requesting availability. Cloud Functions are an ideal fit for these event-driven automations.

What you’ll learn

* How functions respond to Cloud Storage uploads for ETL and analytics.
* How Firestore change events enable near-real-time analytics.
* How Pub/Sub + Functions validate and process IoT telemetry.
* How an HTTP-triggered function behind API Gateway supports serverless APIs.

Table of patterns and services

| Pattern                    | Primary trigger      | Typical downstream services                 | Example use                                               |
| -------------------------- | -------------------- | ------------------------------------------- | --------------------------------------------------------- |
| File upload processing     | `Cloud Storage`      | `Cloud Functions`, `BigQuery`, `Dataflow`   | Convert, enrich, and ingest diagnostic logs for analytics |
| Database change streaming  | `Firestore` triggers | `Cloud Functions`, `Pub/Sub`, `BigQuery`    | Keep analytics and downstream systems in sync on writes   |
| IoT / telemetry processing | `Pub/Sub` messages   | `Cloud Functions`, `Bigtable`, `Monitoring` | Validate, filter, and store time-series telemetry         |
| API Gateway pattern        | `HTTP` trigger       | `Cloud Functions`, `API Gateway`, `IAM`     | Build serverless APIs that aggregate multiple backends    |

We'll step through each pattern and show concise example code and architecture notes so you can adapt them to production.

***

## 1) File upload processing (Cloud Storage → Function → BigQuery)

Scenario
Support tools and automated agents upload car diagnostic logs to Cloud Storage. A Cloud Function triggers on object creation and implements validation, transformation (e.g., CSV → newline-delimited JSON), enrichment (attach metadata), and ingestion into BigQuery for analytics.

Why use Cloud Functions here

* Automatic, event-driven processing on file arrival.
* Fast, scalable, pay-per-execution model.
* Great for lightweight ETL or invoking a pipeline (e.g., Dataflow) for heavier loads.

Minimal Node.js example (GCS-triggered function)

```js theme={null}
// index.js
const {BigQuery} = require('@google-cloud/bigquery');
const BigQueryClient = new BigQuery();

exports.processDiagnosticLog = async (event, context) => {
  const file = event;
  console.log(`Processing file: ${file.name}`);

  // 1) Download and parse the file (omitted)
  // 2) Validate/transform records
  // 3) Enrich with metadata (timestamp, vehicleId from filename, etc.)
  // 4) Insert into BigQuery
  const rows = [{ vehicleId: 'VIN123', ts: Date.now(), metric: 42 }];
  await BigQueryClient
    .dataset('tesla_logs')
    .table('diagnostics')
    .insert(rows);
  console.log('Inserted rows into BigQuery');
};
```

Operational notes

* Use content-based deduplication or object metadata to ensure idempotency.
* For large files, trigger a Dataflow job via Cloud Functions rather than processing inline.
* Monitor function retries and error logs; consider a dead-letter bucket.

<Frame>
  <img alt="A presentation slide titled &#x22;Real-World Integration Examples&#x22; listing four patterns: File Upload Processing, Database Change Streaming, IoT Data Processing, and API Gateway Pattern. Below is a simple diagram showing data flowing from GCS to BigQuery." />
</Frame>

***

## 2) Database change streaming (Firestore → Function → Analytics Pipeline)

Scenario
A customer updates contact info or a service-request status in the mobile app. Firestore triggers on document create/update/delete and a Cloud Function reacts to sanitize/enrich the change and push the record into an analytics store such as BigQuery.

Why this pattern

* Keeps analytics and downstream systems up-to-date without polling.
* Enables event-driven enrichment and fan-out (e.g., publish to Pub/Sub, call external APIs).

Sample Firestore-triggered function (Node.js)

```js theme={null}
// index.js
exports.onCustomerUpdate = async (change, context) => {
  const before = change.before.exists ? change.before.data() : null;
  const after = change.after.exists ? change.after.data() : null;
  console.log('Document changed:', context.params.documentId);

  // Example: normalize phone number, validate fields, enrich with region
  const enriched = { ...after, normalizedPhone: normalize(after.phone) };

  // Forward to analytics pipeline: e.g., BigQuery or Pub/Sub
  // await publishToPubSub('customer-updates', enriched);
};
```

Operational notes

* Design idempotent writes (use stable document IDs or dedup keys).
* Consider partial updates and schema evolution — use versioned schemas or schema-checking libraries.
* Use IAM to limit which services can trigger or read data.

<Frame>
  <img alt="A presentation slide titled &#x22;Real-World Integration Examples&#x22; showing four example patterns (File Upload Processing, Database Change Streaming, IoT Data Processing, API Gateway Pattern) and a pipeline diagram inside a shaded box: Firestore → Function → Analytics Pipeline → BigQuery." />
</Frame>

Quick quiz
Which GCP service can directly trigger a function when a document is created or updated?
Answer: Firestore triggers.

***

## 3) IoT / Telemetry processing (Pub/Sub → Function → Time-series DB)

Scenario
Cars stream telemetry messages (sensor readings, battery metrics, GPS) to Pub/Sub. Cloud Functions subscribe to those topics, validate incoming messages (timestamps, schema), run anomaly detection or filtering, and store the cleaned data in a time-series store (Cloud Bigtable or a managed time-series solution) for monitoring and predictive maintenance.

Why this pattern

* Pub/Sub handles high-throughput ingestion and backpressure.
* Functions provide lightweight, scalable compute for validation and enrichment.
* Enables near-real-time alerts on anomalies (e.g., sudden temp spikes).

Sample Pub/Sub-triggered function (Node.js)

```js theme={null}
// index.js
exports.processTelemetry = async (message, context) => {
  const payload = JSON.parse(Buffer.from(message.data, 'base64').toString());
  // 1) Basic timestamp sanity checks
  if (!isValidTimestamp(payload.ts)) throw new Error('Bad timestamp');

  // 2) Schema validation / transformation
  // 3) Anomaly detection (simple threshold example)
  if (payload.batteryTemp > 80) {
    // alerting, write to alerting topic or monitoring
  }

  // 4) Write to time-series DB (Bigtable example) or Cloud Storage
};
```

Operational notes

* Use message attributes and ordering keys when sequence matters.
* Configure retry/backoff policies and dead-letter topics for poison messages.
* Choose storage based on query patterns: Bigtable for high-volume point reads, BigQuery for analytics.

<Frame>
  <img alt="A presentation slide titled &#x22;Real-World Integration Examples&#x22; showing options like File Upload Processing, Database Change Streaming, a highlighted IoT Data Processing, and API Gateway Pattern. Below is a simple pipeline diagram: Pub/Sub → Function → Data Validation → Time-Series DB." />
</Frame>

***

## 4) API Gateway pattern (API Gateway → HTTP Function → Multiple Backends)

Scenario
A mobile app asks, “Show me the nearest Tesla service station with availability tomorrow.” The request routes through API Gateway to an HTTP-triggered Cloud Function, which aggregates availability, location, and user preference services, applies authorization and rate limiting, and returns the combined response.

Why this pattern

* Serverless APIs with integrated authentication, monitoring, and routing via API Gateway.
* Functions allow flexible orchestration across multiple backends without managing servers.
* Good for low-latency, lightweight orchestration logic.

Minimal HTTP function (Node.js / Express-style)

```js theme={null}
// index.js
exports.getNearestService = async (req, res) => {
  const { lat, lon, date } = req.query;
  // 1) Authenticate request (use IAM or API key checks)
  // 2) Query location service and availability backend in parallel
  const [locations, availability] = await Promise.all([
    fetchLocationService(lat, lon),
    fetchAvailabilityService(date)
  ]);

  // 3) Compose response and return
  res.json({ nearby: composeResponse(locations, availability) });
};
```

Operational notes

* Use API Gateway for routing, security (API keys, JWT), and quota enforcement.
* Implement caching for expensive backend calls where freshness allows.
* Monitor latency and cold-starts; consider keeping critical functions warm or using newer runtimes with lower cold-start times.

<Frame>
  <img alt="A presentation slide titled &#x22;Real-World Integration Examples&#x22; listing File Upload Processing, Database Change Streaming, IoT Data Processing, and API Gateway Pattern. Below is a grey flow diagram showing HTTP → Function → Business Logic → Multiple Backends." />
</Frame>

***

## Summary: Key considerations for production-ready Cloud Functions

* Idempotency: Design functions so repeated invocations don’t cause duplicates.
* Retry semantics: Understand automatic retries (e.g., Pub/Sub vs. HTTP) and use dead-letter topics/buckets if needed.
* Authentication & Authorization: Use IAM, API Gateway, and service accounts to limit access.
* Schema validation: Validate inputs early (JSON Schema, Protobuf) to avoid downstream failures.
* Observability: Export structured logs, set up traces, and instrument metrics and alerts.
* Cost & performance: Choose between inline processing, batching, or delegating to Dataflow/BigQuery for heavy workloads.

> **lightbulb** When designing these integrations, consider idempotency, retry semantics, authentication/authorization, schema validation, and monitoring so your workflows stay reliable and maintainable.

This covers common, real-world integration patterns using Cloud Functions. Each example can be extended with more robust error handling, observability, and security controls for production. See the linked Google Cloud docs for reference implementations and deeper configuration options.

That's it for this lesson — see you in the next one.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/ff8693f0-36fe-4cca-9b05-f27ffa81ccb4/lesson/b60bb2a0-78b7-4d9a-9f88-43a4c94bae86)
