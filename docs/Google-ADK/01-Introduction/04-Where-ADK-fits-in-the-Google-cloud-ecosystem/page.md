# Where ADK fits in the Google cloud ecosystem

Source: https://notes.kodekloud.com/docs/Google-ADK/Introduction/Where-ADK-fits-in-the-Google-cloud-ecosystem/page

Explains Google ADK as an open source, model‑agnostic framework for building production‑ready, multi-agent enterprise AI with GCP integrations, observability, and deployment tooling.

This article clarifies where the Google Agent Development Kit (ADK) sits inside the Google Cloud ecosystem and how it enables production-grade, enterprise AI agents. ADK is an open-source, model-agnostic framework (primarily Python and Java, with Go support) for building single- and multi-agent systems. It is designed for production usage with built-in evaluation, debugging, and observability tools and works with a variety of models such as Gemini, GPT, Claude, and Mistral.

<Frame>
  <img alt="A presentation slide titled &#x22;Google Agent Development Kit (ADK)&#x22; with a colorful agent logo and a &#x22;Production-ready&#x22; banner. Below are icons and labels for &#x22;Built-in evaluation&#x22; and &#x22;Debugging tools.&#x22;" />
</Frame>

> **lightbulb** ADK is vendor-agnostic: although it integrates deeply with Google Cloud, it also works equally well on other clouds such as Azure and AWS.

Core capabilities of ADK focus on enabling reliable, large-scale agent-based applications:

<Frame>
  <img alt="A presentation slide titled &#x22;Core Capabilities&#x22; showing four numbered, colored circular segments around gear icons. Each segment lists a capability: multi-agent orchestration; streaming support (real-time bidirectional audio/video); local CLI and web UI for development and debugging; and containerized deployment across environments." />
</Frame>

* Multi-agent orchestration: support for parallel, sequential, and hierarchical coordination patterns across agents.
* Streaming support: real-time bidirectional streaming for audio; video capabilities are available depending on integration and tooling choices.
* Local developer tools: CLI and web UI for iterative development, debugging, and evaluation workflows.
* Containerized deployment: build once and deploy across environments (Cloud Run, GKE, Compute Engine) with scaling and resilience in mind.

Table: Core capability to production benefit

| Core Capability           | Production Benefit                            | Example                                                   |
| ------------------------- | --------------------------------------------- | --------------------------------------------------------- |
| Multi-agent orchestration | Scale complex workflows and parallelize tasks | Research agents coordinating data retrieval and synthesis |
| Streaming support         | Low-latency, interactive experiences          | Voice assistants with real-time audio streaming           |
| Local developer tools     | Faster iteration and reproducible debugging   | CLI-driven testing and web UI trace visualization         |
| Containerized deployment  | Portable, scalable runtime across clouds      | Deploy to Cloud Run or GKE with CI/CD pipelines           |

Because ADK targets enterprise adoption, it emphasizes scale, observability, and production readiness from the start.

ADK integrates deeply with Google Cloud Platform (GCP) services and provides prebuilt connectors for common enterprise systems. Built by Google, ADK has native connectivity to Compute, Cloud Run, GKE, BigQuery, AlloyDB, Cloud Spanner, API management (Apigee), and more. On the enterprise side, ADK offers connectors and adapters for systems such as Salesforce, Workday, and SAP, enabling automation and cross-system workflows.

<Frame>
  <img alt="A presentation slide titled &#x22;Enterprise Connectivity&#x22; showing an &#x22;Application Integration&#x22; hub diagram linking clouds, user icons, chat and search symbols. The right side lists enterprise apps (Salesforce, Workday, SAP) and notes automation workflows built with application integration." />
</Frame>

Conceptually, ADK operates between the AI/model layer and the integration/deployment layers. It orchestrates model calls, manages tools, and exposes connectors so agents can act on enterprise data and services.

<Frame>
  <img alt="A dark-themed slide titled &#x22;How ADK Fits in&#x22; showing a three-step layered diagram. From bottom to top it lists the AI Layer (Vertex AI, Gemini API, LLM orchestration), the Agent Layer (ADK frameworks, multi-agent orchestration, tooling), and the Integration Layer (application integration, connectors, APIs)." />
</Frame>

Layer mapping

| Layer             | Examples                                  | Role                                                       |
| ----------------- | ----------------------------------------- | ---------------------------------------------------------- |
| AI layer          | Vertex AI, Gemini API, third-party LLMs   | Provide model inference and LLM orchestration              |
| Agent layer       | ADK frameworks, multi-agent orchestration | Coordinate model calls, tools, and cross-agent workflows   |
| Integration layer | Connectors, APIs, application integration | Connect agents to enterprise systems (CRM, ERP, databases) |

For deployment and operations, ADK uses the standard GCP stack: BigQuery and Cloud Storage for data, Cloud Run/GKE/Compute Engine for hosting, and Cloud Monitoring/Logging and security tooling for observability and governance. These integrations make it straightforward to embed agents in enterprise pipelines and monitoring setups.

<Frame>
  <img alt="A slide titled &#x22;Complete Deployment Stack&#x22; with three numbered panels. The panels list Storage (BigQuery, Cloud Storage, Databases), Deployment (Cloud Run, GKE, Compute Engine), and Operations (Cloud Monitoring, Logging, Security)." />
</Frame>

Deployment stack (concise)

| Resource Type                         | Typical Use                                                   |
| ------------------------------------- | ------------------------------------------------------------- |
| BigQuery / Cloud Storage              | Data warehousing and object storage for agent inputs and logs |
| Cloud Run / GKE / Compute Engine      | Runtime environments for agent services                       |
| Cloud Monitoring / Logging / Security | Observability, tracing, and governance for production agents  |

Why ADK matters

<Frame>
  <img alt="A presentation slide titled &#x22;Why ADK Matters&#x22; that lists four numbered benefits: a unified framework for enterprise AI agent development, leveraging GCP services without data duplication, seamless connection to existing enterprise applications, and production-ready deployment from day one. Each point is shown with a colorful circular icon on a dark background and a small KodeKloud copyright." />
</Frame>

* Unified framework: a consistent development model for agent-based applications across teams.
* Efficient use of cloud services: connect to GCP services without unnecessary data duplication where possible.
* Enterprise connectivity: prebuilt connectors and APIs to integrate with existing applications and workflows.
* Production-ready: built-in testing, evaluation, and deployment patterns informed by Google's internal agent experience.

The ADK development lifecycle

* Local development and iterative debugging using the ADK CLI and web UI.
* Built-in evaluation and testing to validate agent behavior, performance, and safety constraints.
* Packaging and containerized deployment to Cloud Run, GKE, or other compute targets using ADK tooling and CI/CD best practices.
* Observability and governance with Cloud Monitoring, Logging, and security integrations.

Typical enterprise use cases

<Frame>
  <img alt="A presentation slide titled &#x22;Enterprise Use Cases&#x22; on a dark background. It lists four items: multi-agent research and analysis systems; enterprise process automation across systems; customer service and support agents; and data analysis and business intelligence agents." />
</Frame>

* Multi-agent research and analysis systems that coordinate data retrieval, enrichment, and synthesis.
* Enterprise process automation connecting disparate systems and workflows (e.g., HR, finance, CRM).
* Customer service and support agents delivering reliable, explainable interactions.
* Data analysis and business intelligence agents that query enterprise datasets and synthesize insights.

ADK represents a practical, enterprise-ready approach to agent-based AI: open source, production-grade, and integrated with enterprise systems.

<Frame>
  <img alt="A presentation slide titled &#x22;ADK: The Future of Enterprise AI&#x22; showing three colored circular icons labeled &#x22;Open Source,&#x22; &#x22;Production-Ready,&#x22; and &#x22;Enterprise-Integrated,&#x22; with a link to google.github.io/adk-docs. The slide has a dark background and a small KodeKloud copyright note." />
</Frame>

Resources and further reading

* ADK documentation: [https://google.github.io/adk-docs](https://google.github.io/adk-docs)
* Vertex AI: [https://cloud.google.com/vertex-ai](https://cloud.google.com/vertex-ai)
* BigQuery: [https://cloud.google.com/bigquery](https://cloud.google.com/bigquery)
* Cloud Run: [https://cloud.google.com/run](https://cloud.google.com/run)
* GKE: [https://cloud.google.com/kubernetes-engine](https://cloud.google.com/kubernetes-engine)

In this lesson we will explore ADK features, show how to set up agent projects, and demonstrate workflows for building, evaluating, and deploying production-ready agents.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-adk/module/f42f0830-1e38-449f-8a50-9bf698eb02ab/lesson/b7d9d702-923c-42b1-bb34-c3fee409afd4)
