# Send a simple metric
statsd.increment("my_lambda.invocations")
```

Best practices:

* Store `DD_API_KEY` and other secrets in a secrets manager or encrypted store.
* Use platform-native mechanisms to inject secrets into environment variables (e.g., AWS Secrets Manager, AWS KMS, Azure Key Vault, GCP Secret Manager).

## Instrumentation Checklist (Quick Start)

| Step | Action                                                                                                                                                   |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Choose the appropriate Datadog runtime library and any required extension/layer for your platform and runtime.                                           |
| 2    | Add the library/layer to your function/package and follow the runtime-specific instrumentation guide.                                                    |
| 3    | Configure the Datadog site and credentials via environment variables or your provider's secret mechanism.                                                |
| 4    | Enable and configure the provider logging integration (e.g., CloudWatch Logs subscription) or use the Datadog extension where available to forward logs. |
| 5    | Verify that metrics, traces, logs, and profiles appear in the Datadog UI and dashboards.                                                                 |

## Validation and Troubleshooting

* Confirm environment variables are present in deployed functions and not printed in logs.
* Check the Datadog UI for incoming metrics and traces; use logs to debug missing instrumentation.
* Validate CloudWatch Logs subscriptions or extension logs for any forwarding errors.
* Use sampling and rate limits to avoid excessive ingestion costs.

## Links and References

* Datadog Serverless: [https://docs.datadoghq.com/serverless/](https://docs.datadoghq.com/serverless/)
* Datadog CloudWatch integration: [https://docs.datadoghq.com/integrations/amazon\_cloudwatch/](https://docs.datadoghq.com/integrations/amazon_cloudwatch/)
* AWS KMS: [https://aws.amazon.com/kms/](https://aws.amazon.com/kms/)
* AWS Secrets Manager: [https://aws.amazon.com/secrets-manager/](https://aws.amazon.com/secrets-manager/)
* HashiCorp Vault: [https://www.vaultproject.io/](https://www.vaultproject.io/)

That's it for this lesson — you should now understand how Datadog Serverless Connectors collect telemetry from serverless platforms, the common configuration patterns, and the recommended security practices for handling credentials.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/10421186-d141-4fde-9847-73ea4e4e675a/lesson/bd90e090-1f87-4c74-af2c-8b846e2bdf7c)


# Understanding the Architecture

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Datadog-Basics/Understanding-the-Architecture/page

Overview of Datadog architecture, components, data collection and delivery models, observability features, integrations, agents, data flow, and enterprise networking and site considerations for deployment

In this lesson we examine Datadog’s architecture and the platform components that make the observability solution work end-to-end.

Although Datadog is presented as a single Software-as-a-Service (SaaS) console, the platform is composed of several integrated parts: local collectors (Agents), cloud and system Integrations, and APIs that enable custom logic, ingestion, and checks. These components work together to collect, process, store, and surface telemetry (metrics, logs, traces, and profiles).

<Frame>
  <img alt="The image illustrates the architecture of Datadog, featuring the Datadog Console (SaaS) and its installed components: Agent, APIs, and Integrations." />
</Frame>

## Delivery models: SaaS vs Self-hosted

When evaluating observability platforms you’ll encounter two common delivery models:

| Delivery model        |                                    Typical use case | Notes                                                                                                                                                  |
| --------------------- | --------------------------------------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SaaS                  |                    Fast onboarding, managed backend | Datadog is primarily a SaaS offering — the console and backend are hosted by Datadog. Agents and integrations run in your environment to collect data. |
| Self-hosted (on-prem) | Strict regulatory/compliance or network constraints | You host the control plane and storage (e.g., self-hosted Grafana). Greater operational overhead but more control.                                     |

Choose based on technical, compliance, and operational requirements: latency, data residency, control of infrastructure, and security posture are common decision drivers.

## Core components and responsibilities

* Datadog Console (SaaS): Central UI, dashboards, alerting, and control plane.
* Agents: Lightweight collectors that gather metrics, logs, traces, and continuous profiles from hosts, containers, and serverless runtimes.
* Integrations & APIs: Cloud, database, and third-party system connectors; public APIs for custom ingestion, checks, and automation.
* Clients: Engineers and responders use browsers and mobile apps to view dashboards, receive alerts, and manage incidents.

Table — Core components at a glance:

| Component      | Role                                  | Examples                                    |
| -------------- | ------------------------------------- | ------------------------------------------- |
| Console (SaaS) | UI and control plane                  | Dashboards, monitors, Incident Management   |
| Agent          | Local telemetry collection            | Host agent, Containerized Agent, APM tracer |
| Integrations   | Connector to services and platforms   | AWS, Azure, Kubernetes, Databases           |
| APIs           | Programmatic ingestion and automation | Custom metrics API, Events API, Checks      |

Datadog supports telemetry from containerized applications, serverless functions (AWS Lambda, Azure Functions), cloud platforms, on‑prem infrastructure, and frontend applications. Each source typically has a tailored collection method or a dedicated integration.

<Frame>
  <img alt="The image illustrates Datadog's architecture, showing data sources like frontend and cloud providers feeding metrics, logs, traces, and profiles into Datadog, which is accessed by clients on mobile and laptop and used by engineers." />
</Frame>

## Platform capabilities and observability features

Datadog ingests and correlates multiple telemetry types to provide holistic observability:

* Metrics, logs, traces, and continuous profiling (correlated across dimensions).
* UX monitoring: Real User Monitoring (RUM) for frontend performance and behavior.
* CI/CD monitoring: pipeline and workflow observability.
* LLM observability: monitoring of large language model usage and behavior.
* Security tooling: SIEM, SOAR, code analysis, runtime security.
* Cost monitoring: cloud cost insights and allocation.
* Dashboards, alerting, incidents, metrics analytics, and notebooks.

Use these capabilities to connect incidents with root causes — trace to metric to log — for faster resolution.

## How data reaches Datadog

Data collection typically begins with Agents and platform integrations:

* Agents: Installed where telemetry originates (hosts, containers, or as binaries). For Kubernetes, deploy an Agent inside the cluster to collect node, pod, and service telemetry.
* Serverless and cloud-native integrations: Some integrations collect telemetry without a persistent agent by using platform APIs or function-level instrumentation (e.g., [Datadog’s Lambda Forwarder for AWS Lambda logs](https://docs.datadoghq.com/integrations/amazon_lambda/)).
* Ingestion pipelines: Datadog supports pre-ingestion processing, enrichment, and parsing rules so telemetry is normalized before storage and analysis.

Example: installing the Datadog Agent into a Kubernetes cluster (Helm):

```bash theme={null}
helm repo add datadog https://helm.datadoghq.com
helm repo update
helm install datadog-agent datadog/datadog \
  --set datadog.apiKey=<YOUR_API_KEY> \
  --set datadog.site='datadoghq.com'
```

After collection, telemetry is sent to the Datadog backend where it’s processed, stored, and surfaced in the Console and mobile clients.

<Frame>
  <img alt="The image illustrates Datadog's data workflow, showing how data from a cloud platform, database, and application are processed by an agent before being sent to Datadog." />
</Frame>

## Enterprise network considerations

Access and authentication:

* Datadog is accessed over the public internet with standard browsers and the mobile app.
* Integrate with your Identity Provider (IdP) for SSO and centralized access control to enforce corporate policies.

Egress, proxies, and firewall considerations:

* Many organizations require outbound traffic to be routed through proxies or firewalls. Configure Datadog Agents and integrations to work through your proxy.
* Verify required allowlists (hostnames, IPs) and TLS interception rules so agents can reach Datadog endpoints.

## Sites, regions, and data residency

Datadog operates multiple sites/regions. Your site selection affects latency and compliance (data residency). Important points:

* Site selection is persistent for an organization; data cannot be moved later.
* Evaluate regulatory and business requirements (e.g., GDPR, data residency) before choosing a site.

<Frame>
  <img alt="The image is a table showing different Datadog site options, including site URLs, parameters, and their respective locations." />
</Frame>

> **lightbulb** Carefully evaluate data residency and compliance requirements before choosing your Datadog site. The selection is persistent for your organization and cannot be changed later.

## Summary

Datadog is a SaaS console backed by a distributed collection layer (Agents and Integrations) and public APIs. Understanding where and how telemetry is collected, the difference between agent-based and platform-native integrations, and the implications of networking and site selection will help you design an observability deployment that meets performance, security, and compliance goals.

Further reading and references:

* Datadog documentation: [https://docs.datadoghq.com/](https://docs.datadoghq.com/)
* Kubernetes Basics: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* Datadog AWS Lambda integration: [https://docs.datadoghq.com/integrations/amazon\_lambda/](https://docs.datadoghq.com/integrations/amazon_lambda/)

That's it for this lesson. I hope you found it useful.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/10421186-d141-4fde-9847-73ea4e4e675a/lesson/d3ecb6bb-e7e4-4314-9e7b-a92e13c90319)
