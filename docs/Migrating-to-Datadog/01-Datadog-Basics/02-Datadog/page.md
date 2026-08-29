# Datadog

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Datadog-Basics/Datadog/page

Overview of Datadog, a cloud-based observability and security platform that centralizes telemetry, integrates widely, and provides APM, logs, metrics, and security monitoring

In this lesson we cover what Datadog is and how it helps organizations meet monitoring, observability, and security objectives.

Datadog is a cloud-based observability and security platform that centralizes telemetry across an organization's entire stack. It collects and correlates metrics, traces, and logs, while providing first-class features for application performance monitoring (APM), real user monitoring (RUM), synthetic testing, infrastructure monitoring, network performance, and security monitoring. This unified approach delivers end-to-end visibility—from frontend applications and services through cloud platforms and on-premises infrastructure to databases—so teams can rapidly detect, investigate, and remediate issues.

Key benefits include:

* Unified telemetry: correlate frontend errors with backend traces and infrastructure metrics to reduce mean time to resolution (MTTR).
* Security + observability: enrich security events with contextual telemetry for faster investigation.
* Broad integrations: native and community integrations across cloud providers, container platforms, orchestration systems, databases, and third-party services.
* Advanced analytics: AI/ML-powered anomaly detection, automated root cause analysis, and forecasting.
* Open standards and modern tech: support for OpenTelemetry, eBPF, and deep Kubernetes integration.

<Frame>
  <img alt="The image shows Datadog highlighted as a leader in Gartner's Magic Quadrant for Application Performance Monitoring, with other companies positioned in different quadrants based on &#x22;Ability to Execute&#x22; and &#x22;Completeness of Vision.&#x22;" />
</Frame>

Datadog supports telemetry collection from many operating systems and dozens of programming languages (JavaScript, Java, Go, Python, Ruby, .NET, and more). It maintains hundreds of official integrations and community-supported plugins, enabling monitoring across nearly all common platforms and environments.

<Frame>
  <img alt="The image shows logos of various technology platforms and languages like Java, AWS, Azure, Docker, Kubernetes, Linux, and more, highlighting Datadog's integration capabilities. It mentions that Datadog supports more than 850 integrations." />
</Frame>

## Core Datadog capabilities

| Capability                          |                                                               What it does | Example use case                                                      |
| ----------------------------------- | -------------------------------------------------------------------------: | --------------------------------------------------------------------- |
| Metrics, traces, logs               | Centralize and correlate time-series metrics, distributed traces, and logs | Link a slow API trace to increased database latency                   |
| APM & RUM                           |                       Monitor service performance and real user experience | Identify a frontend regression causing higher error rates             |
| Synthetic monitoring                |                                             Automate uptime and API checks | Schedule a synthetic test for critical transaction workflows          |
| Infrastructure & network monitoring |                         Visualize host/container metrics and network flows | Detect noisy neighbors on a Kubernetes node                           |
| Security monitoring                 |                       Detect threats and misconfigurations using telemetry | Alert on suspicious inbound connections or anomalous process behavior |

## Getting started (high level)

* Install the Datadog Agent on hosts, VMs, or as a DaemonSet in Kubernetes to collect metrics, logs, and traces.
* Enable language-specific APM libraries (Java, Python, Node, etc.) to capture distributed traces.
* Configure integrations for cloud providers, databases, and third-party services to enrich telemetry.
* Create dashboards, monitors, and synthetic tests to observe SLAs and SLOs across systems.

<Callout icon="lightbulb">
  Start with the Datadog Agent and one APM integration for a quick win: install the Agent, enable tracing for one service, and create a dashboard that correlates traces with host metrics. See [Datadog documentation](https://docs.datadoghq.com/) for step-by-step guides.
</Callout>

## Why teams choose Datadog

* Fast time-to-value with out-of-the-box integrations and dashboards.
* Unified observability and security to reduce toolchain complexity.
* Scalable SaaS architecture for monitoring cloud-native and hybrid environments.
* Strong ecosystem and community support for OpenTelemetry, eBPF, and Kubernetes.

Resources and further reading:

* Datadog Documentation: [https://docs.datadoghq.com/](https://docs.datadoghq.com/)
* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* Kubernetes: [https://kubernetes.io/](https://kubernetes.io/)

That's it for this lesson. I hope you found the overview useful and that it helps you plan your observability and security strategy with Datadog.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/10421186-d141-4fde-9847-73ea4e4e675a/lesson/5bb5e499-7ec6-4dc5-a844-b5694c873fbb" />
</CardGroup>
