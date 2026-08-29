# Exploring Observability

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Observability-Basics/Exploring-Observability/page

Explains observability importance for modern distributed cloud systems, describing telemetry types, placement in architectures, and benefits for business and engineering teams.

This lesson explains how system architectures have evolved, why observability is essential for modern distributed systems, and where to place telemetry to gain actionable insights for both business and engineering teams.

## How system architectures have changed

Over time we moved from single, bundled applications to highly distributed systems. Monoliths—where frontend, backend, integration layers, and databases were packaged together—gave way to services that run across many hosts, regions, and platforms. This architectural shift accelerated with widespread public cloud adoption.

<Frame>
  <img alt="The image illustrates four distributed service icons arranged in a grid, with a header that states &#x22;System architectures have evolved significantly over the years.&#x22;" />
</Frame>

## Where systems run today

Hosting models also evolved: from on-premises data centers to public and private clouds, and now to hybrid and multi-cloud deployments that span multiple providers and regions. This diversification adds operational complexity and increases the need for consistent visibility across environments.

<Frame>
  <img alt="The image illustrates the evolution of system hosting environments, moving from On-Premise to Cloud, and finally to Multi-Cloud with logos of major providers like Google Cloud, Azure, and AWS." />
</Frame>

## From in-house monoliths to cloud-native platforms

Historically, in-house monoliths ran on application servers and platform stacks such as Microsoft IIS or Linux-based application hosts and connected to local databases. Today’s distributed systems run across regions and cloud providers and often use orchestration and managed platforms like Kubernetes, Azure App Service, and Google Cloud Run.

<Frame>
  <img alt="The image depicts a diagram titled &#x22;In-House Monoliths,&#x22; showing multiple stacks, each consisting of three blocks leading to separate databases." />
</Frame>

## Why observability matters

Distributed architectures and multi-cloud deployments make root-cause analysis and performance tuning more challenging. Observability provides the telemetry and context teams need to understand system behavior, reduce mean time to detection (MTTD), and shorten mean time to resolution (MTTR).

* For business teams: observability turns raw telemetry into actionable business insights and user behavior data, helping prioritize product and operational decisions.
* For engineering teams: it accelerates detection of performance regressions, pinpoints optimization opportunities, and improves incident response.

<Frame>
  <img alt="The image illustrates the value of monitoring for business teams, highlighting benefits like translating business information from data and making data-driven decisions." />
</Frame>

> **lightbulb** Observability is the practice of deriving meaningful insight about system state and behavior from telemetry data—metrics, traces, and logs—so teams can diagnose issues, predict problems, and optimize performance.

## Core telemetry types and what they reveal

Use a combination of telemetry to get a complete view of system health and performance:

| Telemetry    | What it measures                    | Typical example                              | Primary use                            |
| ------------ | ----------------------------------- | -------------------------------------------- | -------------------------------------- |
| Metrics      | Numeric measurements over time      | 250 ms average request latency               | Trend analysis, alerting, SLA tracking |
| Traces       | Distributed request flow and timing | Trace showing a slow DB call across services | Root-cause analysis for slow requests  |
| Logs         | Discrete events and error details   | "Error: failed to connect to database"       | Forensic diagnosis and context         |
| Error counts | Aggregate failure rates             | 130 HTTP 500 errors in the past hour         | Detecting spikes in failures, alerting |

Combining these signals lets teams quickly triangulate the source of problems—e.g., a latency spike in metrics, traces that identify a slow downstream service, and logs that show the exception.

## Placing observability in your architecture

Observability should be integrated end-to-end: from the user device through API gateways and integration layers, into microservices or serverless functions, and down to data stores and infrastructure. Instrument the cloud platform, orchestrator, and underlying infrastructure to avoid blind spots.

<Frame>
  <img alt="The image illustrates an end-to-end architecture with integrated observability, showing a user accessing a system through a laptop, which connects to an API Gateway that manages multiple microservices and a database within a cloud platform. It highlights observability points throughout the architecture." />
</Frame>

## Quick reference: benefits by team

| Team       | Observable outcomes                                                   |
| ---------- | --------------------------------------------------------------------- |
| Business   | Data-driven decisions, user behavior insights, product health metrics |
| Technology | Faster incident response, performance tuning, capacity planning       |

## Further reading and references

* [New Relic: What is observability?](https://newrelic.com/what-is/observability) — definition and context for observability practice.
* [Kubernetes documentation](https://kubernetes.io/docs/) — platform guidance for orchestrated deployments.

That concludes this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/9d4795bc-91eb-4262-ae9c-f7153c17438e/lesson/68048065-c079-4b5a-9d69-00a8a53fb918)
