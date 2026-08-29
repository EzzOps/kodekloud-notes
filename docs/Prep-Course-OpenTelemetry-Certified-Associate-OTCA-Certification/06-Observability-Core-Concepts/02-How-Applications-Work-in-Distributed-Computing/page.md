# How Applications Work in Distributed Computing

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Observability-Core-Concepts/How-Applications-Work-in-Distributed-Computing/page

How modern distributed microservice applications work and why observability with OpenTelemetry is essential for diagnosing and troubleshooting failures.

The role of distributed computing is central to understanding OpenTelemetry and observability. This article explains how modern applications are built, how they behave in distributed systems, and why observability matters when troubleshooting them.

Where do you see modern applications? Examples include online shopping sites, internet banking portals, utility bill payment systems, streaming services such as Netflix and YouTube, insurance and travel portals, and government sites for tasks like booking a driving test or applying for a license.

<Frame>
  <img alt="The image is an infographic titled &#x22;Where We See Modern Applications,&#x22; featuring icons for online shopping, internet banking, utilities portals, Netflix, YouTube, insurance portals, travel agencies, and government portals." />
</Frame>

All of these are examples of user-facing applications that rely on many backend systems working together. Under the hood, they rarely run as a single monolithic process.

Most modern applications are built as a collection of microservices plus supporting systems (databases, caches, message brokers). These components may be implemented in different programming languages and run on different platforms, but together they deliver one cohesive user experience.

<Frame>
  <img alt="The image shows a diagram illustrating how microservices power apps, featuring a shopping cart interface and a code snippet representation." />
</Frame>

Consider the typical flow when a user clicks “Place Order” on an e-commerce site:

* The front end calls the checkout service (it might be hosted on an [EC2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2) instance).
* The checkout service retrieves cart details from a cache such as [Redis](https://redis.io/).
* It then queries the product catalog from a catalog service running in [Kubernetes](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial).
* The checkout service calls a pricing or currency service, which may receive updates through a messaging system like [Kafka](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka).
* It invokes the payment service—this could be deployed in [Kubernetes](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial) or provided by a third‑party gateway.
* Finally, the order is passed to shipping/fulfillment (possibly another service on [EC2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)).

This sequence of service calls across platforms is a distributed system: many independent components coordinate to satisfy a single user request.

In distributed systems, there are multiple touchpoints and dependencies. Each component (service, database, cache, or message broker) must operate correctly for the request to succeed. When one component fails or degrades, the user experience suffers.

<Frame>
  <img alt="The image depicts an e-commerce shopping cart interface with a series of backend services and technologies, illustrating a failure in the checkout process within a microservices architecture." />
</Frame>

Degradation can present in many ways: a site may not load, pages can return 500 Internal Server Error responses, transactions might fail, or interactions may be slow and time out. Any of these issues indicates a malfunction somewhere in the distributed topology.

So how do you diagnose and find the root cause?

<Frame>
  <img alt="The image features a question about diagnosing and fixing the root cause of a &#x22;500 Internal Server Error,&#x22; accompanied by a large question mark." />
</Frame>

> **lightbulb** Observability provides the telemetry—logs, metrics, and distributed traces—that you need to locate failures, understand why they happened, and resolve the root cause. By collecting and correlating telemetry across services and infrastructure, you can trace a user request end-to-end and identify the problematic component or dependency.

Key telemetry types and their purposes:

| Telemetry Type     |                                              What it shows | Common use                                              |
| ------------------ | ---------------------------------------------------------: | ------------------------------------------------------- |
| Metrics            | Time-series numeric data (latency, error rate, throughput) | Monitor trends, set alerts, and detect anomalies        |
| Logs               |                  Timestamped event records and text output | Inspect detailed events, stack traces, and errors       |
| Distributed traces |        End-to-end request flow with timing across services | Visualize service call graph, find slow or failing hops |

How observability helps in practice:

* Correlate traces with logs and metrics to narrow down the failing service.
* Use distributed tracing to follow a specific user request across services.
* Inspect service logs and metrics for the identified component to determine cause (e.g., timeout, exception, resource exhaustion).
* Implement alerts on key metrics (error rate, latency) to detect regressions early.

Further reading and references:

* [OpenTelemetry](https://opentelemetry.io/) — vendor-neutral observability framework
* [Kubernetes Documentation](https://kubernetes.io/docs/) — orchestration for microservices
* [Redis](https://redis.io/) — in-memory cache
* [Apache Kafka](https://kafka.apache.org/) — event streaming platform

By instrumenting each component and using tools like OpenTelemetry, you gain visibility across the entire distributed system—making it possible to detect issues quickly, reduce mean time to resolution (MTTR), and improve user experience.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/79b34fea-6f94-4854-a31e-9ac0fbc10eca/lesson/925e5a28-0f42-4e0f-95bd-7df9aeaba8c5)
