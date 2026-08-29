# Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Dashboarding-Visualization/Introduction/page

Overview of Prometheus visualization options, comparing built-in tools like the expression browser and console templates with third-party Grafana for creating dashboards, queries, and shared monitoring views.

In this section we'll explore Prometheus's dashboarding and visualization options. Visualization is the process of representing Prometheus metrics as graphs, tables, and dashboards so humans can more easily spot trends, anomalies, and correlations. Raw metric values are useful, but plotting them reveals patterns that are otherwise hard to detect.

Prometheus provides several ways to visualize metrics:

* Built-in tools for quick inspection and lightweight dashboards.
* Third-party products optimized for rich, reusable dashboards.

One built-in option is the expression browser, which you can use to run ad-hoc PromQL queries and inspect metrics immediately.

<Frame>
  <img alt="The image is a slide titled &#x22;visualization,&#x22; describing ways to visualize Prometheus metric data using built-in tools like the Expression browser and Console Templates, and third-party tools like Grafana." />
</Frame>

The expression browser is great for quick queries and debugging. Another built-in feature is console templates, which let you create small, predefined HTML-like pages that render specific graphs and metric tables.

For sophisticated, production-grade dashboards, third-party tools like Grafana are the standard choice. Grafana is purpose-built for visualization, supports Prometheus as a data source, and offers rich panels, templating, alerts, and sharing capabilities so teams can have a single dashboard that summarizes key signals.

<Callout icon="lightbulb">
  Use the expression browser for exploratory PromQL queries and quick checks. Use console templates for simple, static metric pages. Use Grafana for interactive, shareable dashboards and long-term team visibility.
</Callout>

## Visualization Tools at a Glance

| Tool               | Type        | Best for                                            | Quick tip                                                           |
| ------------------ | ----------- | --------------------------------------------------- | ------------------------------------------------------------------- |
| Expression Browser | Built-in    | Ad-hoc PromQL queries and metric inspection         | Accessible via the Prometheus UI for immediate query results        |
| Console Templates  | Built-in    | Simple, predefined pages for specific graphs/tables | Useful for embedding fixed views or a small set of dashboards       |
| Grafana            | Third-party | Rich, interactive dashboards, templating, alerting  | Use Prometheus as a datasource and create reusable dashboard panels |

## When to use each option

* Expression Browser: troubleshooting, validating queries, and exploring metric names and labels.
* Console Templates: embedding a small set of curated views without an external dependency.
* Grafana: centralized dashboards for on-call teams, executive summaries, and long-lived visualizations.

## Links and references

* [Prometheus Documentation — Querying Prometheus](https://prometheus.io/docs/prometheus/latest/querying/basics/)
* [Grafana](https://grafana.com)
* [Prometheus Console Templates](https://prometheus.io/docs/visualization/console_templates/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/d8fe7717-c2f8-4cfc-b3a7-c88d20fd5659/lesson/06603318-db3a-4c26-a094-ad654cdd3bdb" />
</CardGroup>
