# Managing Dependencies

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Managing-Complexity-Risk-and-Toil/Managing-Dependencies/page

How to identify, classify, and mitigate service dependencies using resilience patterns like circuit breakers, fallbacks, and bulkheads to reduce blast radius and improve system reliability.

Welcome back. Now that we've explored why simplicity matters, this lesson focuses on managing dependencies — everything your system relies on: third‑party libraries, external APIs, internal services, and infrastructure components. Left unmanaged, dependencies increase complexity and the risk of outages, regressions, and operational toil.

Think about shipping a feature only to discover a transitive library introduced a breaking change deep in your stack. You aren’t just running your own code: every dependency expands your risk surface. Common failure modes include:

* Availability coupling — if a dependency is down, your service might be down too.
* Latency coupling — slow dependencies can determine your response time.
* Cascading failures — one failure can trigger a domino effect across components.
* Capacity coupling — a dependency under pressure can overwhelm your system (or vice versa).

<Frame>
  <img alt="A slide titled &#x22;The Dependency Challenge&#x22; that lists four dependency risks—Availability coupling, Latency coupling, Cascading failures, and Capacity coupling—each shown with a colored icon. Each risk has a one-line explanation about how dependencies affect availability, speed, failure spread, and capacity." />
</Frame>

Well-managed dependencies reduce these risks. Common resilience patterns include circuit breakers, fallbacks and graceful degradation, bulkheads, and other isolation strategies. These patterns help contain failures, preserve core functionality, and make recovery predictable. We’ll expand on each pattern and show how to apply them to a sample system.

<Frame>
  <img alt="A presentation slide titled &#x22;The Dependency Challenge&#x22; showing four colorful cards labeled Circuit Breakers, Fallbacks, Bulkheads, and Graceful Degradation with short descriptions. Each card summarizes a resilience strategy for managing dependencies (prevent cascade failures, maintain functionality during outages, isolate failures, and preserve core business value)." />
</Frame>

Dependency types

Use the following classification to reason about impact, operational requirements, and mitigation costs.

| Dependency type         | What it is                                                | Reliability/ops concerns                                |
| ----------------------- | --------------------------------------------------------- | ------------------------------------------------------- |
| Direct dependencies     | Your component calls another component directly           | Immediate availability and latency coupling             |
| Indirect dependencies   | Dependency via a chain of calls                           | Harder to observe and reason about; transitive failures |
| Runtime dependencies    | Services required when the app runs (APIs, DBs, caches)   | Live availability, connection pooling, timeouts         |
| Build‑time dependencies | Libraries, frameworks, CI/CD tooling used to build/deploy | Supply-chain, reproducibility, and build-time failures  |

<Frame>
  <img alt="A presentation slide titled &#x22;The Dependency Challenge&#x22; that lists four dependency types. They are Direct (Component A calls Component B), Indirect (A relies on B through an intermediary), Runtime (external services, databases, caches), and Build‑Time (libraries, frameworks, tools)." />
</Frame>

Blast radius and prioritization

Blast radius measures how many services, users, or business capabilities are affected when a dependency fails. Estimating blast radius helps prioritize resilience work. Consider:

* Dependent services — how many services rely on this dependency?
* Criticality of dependent paths — are core user journeys impacted?
* Traffic volume — how much user activity traverses the dependency?
* Recovery time — how quickly can the system be restored?

Use these factors to decide which dependencies deserve investment (e.g., highly critical + high traffic = top priority).

<Frame>
  <img alt="A presentation slide titled &#x22;Blast Radius Analysis&#x22; showing a table of factors. Four colored rows list characteristics (Dependent Services, Criticality, Traffic Volume, Recovery Time) each paired with a short description about impact or restoration." />
</Frame>

Applying this to the KodeKloud Record Store

Key runtime dependencies for the KodeKloud Records Store include the API service, [PostgreSQL](https://www.postgresql.org/) database, [RabbitMQ](https://www.rabbitmq.com/) for messaging, [Celery](https://docs.celeryq.dev/) workers for background tasks, and observability components like [Prometheus](https://prometheus.io/) and [Jaeger](https://www.jaegertracing.io/). Mapping these dependencies reveals which components are most critical and the potential blast radius.

<Frame>
  <img alt="A system dependency diagram for the KodeKloud Records Store showing the web UI and microservices and how they connect to messaging, database, and observability components. It includes Web API (port 8000), RabbitMQ (5672), PostgreSQL (9432), Celery workers, and an observability stack with Grafana (5000), Loki (3100) and Alertmanager (9093)." />
</Frame>

<Callout icon="lightbulb">
  The diagram shows example ports for the demo environment. Common defaults are: PostgreSQL 5432, Grafana 3000, RabbitMQ 5672, and Loki 3100. Always verify and use the ports configured for your environment.
</Callout>

High‑level component map (conceptual)

```text theme={null}
KodeKloud Records Store
├── API Service (FastAPI)
│   ├── Routes/Endpoints
│   │   ├── /products - Product management
│   │   ├── /orders - Order management
│   │   ├── /checkout - Order processing
│   │   ├── /health - Health checks
│   │   ├── /trace-test - Diagnostic tracing
│   │   ├── /slow-operation - Latency simulation
│   │   └── /error-test - Error generation
│   ├── Database Connection
│   │   └── PostgreSQL Database
│   │       ├── Products Table
│   │       └── Orders Table
│   ├── Background Processing
│   │   ├── Celery Worker
│   │   │   ├── Process Order Task
│   │   │   └── Send Order Confirmation Task
│   │   └── RabbitMQ Message Queue
│   ├── Observability Stack
│   │   ├── Metrics Collection
│   │   │   ├── Prometheus
│   │   │   └── Pushgateway (for batch metrics)
│   │   ├── Logs Management
│   │   │   ├── Fluent Bit (collection)
│   │   │   └── Loki (storage)
│   │   ├── Tracing
│   │   │   └── Jaeger
│   │   ├── Monitoring
│   │   │   ├── Grafana (dashboards)
│   │   │   ├── Alertmanager (alerts)
│   │   │   └── Blackbox Exporter (synthetic testing)
│   │   └── Telemetry Instrumentation
│   │       ├── FastAPI Instrumentation
│   │       ├── SQLAlchemy Instrumentation
│   │       └── Celery Instrumentation
└── Infrastructure
    └── Docker Compose Environment
```

Classifying dependencies

Not all dependencies need the same level of investment. Classify them to focus mitigation efforts on what matters most:

<Frame>
  <img alt="A presentation slide titled &#x22;Dependency Classification&#x22; that explains classifying dependencies by criticality. It shows four labeled boxes—Critical, Important, Non-Critical, and External—each with a short description of that dependency type." />
</Frame>

Example classification for KodeKloud Record Store

|                                   Dependency | Classification                 | Typical mitigations                                               |
| -------------------------------------------: | ------------------------------ | ----------------------------------------------------------------- |
|    [PostgreSQL](https://www.postgresql.org/) | Critical                       | Connection pooling, timeouts, read replicas, backups              |
|                        API service (FastAPI) | Critical                       | Autoscaling, load balancing, liveness/readiness probes            |
|        [RabbitMQ](https://www.rabbitmq.com/) | Important                      | Replicated brokers, local queueing fallback, synchronous fallback |
|  [Celery](https://docs.celeryq.dev/) workers | Important                      | Task timeouts, dead-letter queues, isolated worker pools          |
| Monitoring stack (Prometheus, Grafana, Loki) | Non‑critical for core function | Local buffering, reduced sampling, rate limiting                  |
|                          Email notifications | Non‑critical                   | Queue for later delivery, retry logic, batched/manual fallback    |

Dependency management strategies

Circuit breakers

Circuit breakers stop repeated calls to a failing dependency and allow your system to fail fast rather than hanging while waiting. They generally have three states:

* Closed — calls proceed normally.
* Open — calls are blocked because failures exceeded a threshold.
* Half‑open — a limited number of test calls are allowed to see if the dependency recovered.

Use mature libraries when possible: [Resilience4j](https://resilience4j.readme.io/) for Java, [PyBreaker](https://pypi.org/project/pybreaker/) for Python.

Example pseudocode (illustrative):

```python theme={null}
