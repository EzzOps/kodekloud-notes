# Introduction

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Observability-Basics/Introduction/page

Hands-on course guiding teams through migrating observability to Datadog using OpenTelemetry, covering planning, execution, dashboards, integrations, and post-migration validation.

Welcome — and thanks for joining. If you've ever wondered how leading global companies implement observability at scale, this course will show you their patterns and best practices.

Migrating to Datadog is a hands-on, demonstration-driven guide that walks you through building a modern observability platform. I'm Pedro, and in this lesson I'll guide you step-by-step through the migration process, explaining not only how to perform each task but why it matters.

As systems scale and architectures become more distributed, observability moves from optional to mission-critical. Datadog is a proven SaaS observability platform used by organizations such as Airbnb, Samsung, 21st Century Fox, and Whole Foods to monitor applications and infrastructure in real time.

> **lightbulb** This course emphasizes demonstrations and real-world examples so you learn both the practical steps and the rationale behind migrating to Datadog.

We start with observability fundamentals: what observability truly means, its four core pillars (metrics, logs, traces, and profiles), and how modern toolchains collect and correlate telemetry to give you actionable insights.

<Frame>
  <img alt="The image shows a person speaking in front of a list titled &#x22;Migrating to Datadog Curriculum,&#x22; which includes topics like Observability Basics and Datadog Basics. The person is wearing a KodKloud T-shirt and appears to be in an office setting." />
</Frame>

OpenTelemetry is an important part of modern observability stacks, with broad community adoption and growing enterprise support. We'll cover how OpenTelemetry fits into a Datadog migration and how to leverage it for consistent telemetry collection.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;Migrating to Datadog,&#x22; highlighting OpenTelemetry's huge community and enterprise support, with a small circular inset of a person in the bottom right corner." />
</Frame>

Next, the course shifts to Datadog basics. You'll get a clear walkthrough of Datadog's SaaS architecture, the agent ecosystem, common integrations, and serverless support — all shown live so you can see how pieces fit together.

<Frame>
  <img alt="The image is a slide from a presentation about Datadog integrations, showcasing various technology logos and stating there are over 850 integrations. A person is visible in the bottom right corner." />
</Frame>

In the pre-migration module, we evaluate your current telemetry setup, discuss migration drivers, and compare migration strategies (phased vs. Big Bang). You’ll learn how to plan rollbacks, orchestrate the migration, and avoid common pitfalls during cutover.

The migration module focuses on hands-on tasks:

* Migrating dashboards and visualizations
* Configuring and validating integrations
* Implementing distributed tracing and cross-platform correlation
* Addressing security and performance considerations
* Communicating changes across teams and stakeholders

Post-migration, we’ll show how to validate outcomes, decommission legacy monitoring components safely, and improve alerting and incident response. You’ll also discover advanced Datadog features such as Watchdog and communications integrations with Slack and Microsoft Teams.

This course is ideal for DevOps engineers, SREs, platform teams, and architects modernizing observability or migrating from tools like Prometheus, Grafana, Dynatrace, or the Elastic Stack.

At KodeKloud, our community supports collaboration and continuous learning — ask questions, share experiences, and connect with peers as you progress through the migration.

<Frame>
  <img alt="The image shows a digital interface for the KodeKloud community with various categories and a world map indicating user locations. There is also an inset of a person speaking at the bottom right corner." />
</Frame>

Migrate with clarity, build with confidence, and get the most from Datadog.

## Course Roadmap

| Module                        | Focus                                          | Key outcomes                                                                           |
| ----------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------------- |
| Observability Basics          | Concepts, pillars, OpenTelemetry               | Understand metrics, logs, traces, profiles, and telemetry collection                   |
| Datadog Fundamentals          | Architecture, agents, integrations, serverless | Learn how Datadog collects and stores telemetry and how to connect systems             |
| Pre-Migration Planning        | Assessment, strategy, risk management          | Choose a migration approach and prepare rollback and orchestration plans               |
| Migration Execution           | Dashboards, integrations, tracing              | Migrate dashboards, enable integrations, and implement distributed monitoring          |
| Post-Migration & Optimization | Validation, decommission, alerts               | Validate the migration, retire legacy systems, and tune alerting and incident response |

## Links and References

* [OpenTelemetry](https://opentelemetry.io)
* [Datadog Documentation](https://docs.datadoghq.com/)
* [Prometheus](https://prometheus.io)
* [Grafana](https://grafana.com)
* [Dynatrace](https://www.dynatrace.com)
* [Elastic Stack](https://www.elastic.co/elastic-stack)
* [Slack](https://slack.com)
* [Microsoft Teams](https://www.microsoft.com/microsoft-teams)

If you’re ready to begin, proceed to the Observability Basics module to build a solid foundation before starting your Datadog migration.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/9d4795bc-91eb-4262-ae9c-f7153c17438e/lesson/04fbedc8-cdb0-445a-9e58-fa9dd510ba88)
