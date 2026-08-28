# Conclusion

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-[AWS_SECRET_ACCESS_KEY]

Summary of a Prometheus course covering architecture, metric types, PromQL, deployment, alerting, best practices, and practical next steps for instrumenting services and configuring monitoring

Thank you for completing this course on Prometheus.

This final section summarizes the core concepts, practical workflows, and recommended next steps so you can confidently apply Prometheus for monitoring infrastructure and applications.

## Course summary

Prometheus provides a robust, open-source monitoring solution focused on time-series metrics. Throughout the lessons you learned how to design, deploy, and query Prometheus to get actionable observability from services and infrastructure.

| Topic                   | What you learned                                                        | Why it matters                                                     |
| ----------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Prometheus architecture | Components such as the Prometheus server, exporters, and Alertmanager   | Helps you plan deployment and scale monitoring reliably            |
| Metric types            | Counter, Gauge, Histogram, Summary                                      | Choose appropriate types for accurate measurements and aggregation |
| Provisioning & scraping | How to deploy a Prometheus server and configure scrape targets          | Enables collection of metrics from services and exporters          |
| PromQL                  | Writing queries to retrieve and aggregate metrics                       | Lets you build dashboards, alerts, and diagnostics                 |
| Core features           | Alerting, federation, service discovery, and storage/retention concerns | Essential for real-world, production-grade monitoring              |

## Practical next steps

Apply what you learned with hands-on exercises that reinforce concepts and expose real-world trade-offs:

1. Instrument a small service (HTTP server, microservice, or CLI) using a Prometheus client library.
2. Deploy a Prometheus instance and add your service as a scrape target.
3. Create basic PromQL queries and visualize them in Grafana or the Prometheus UI.
4. Add alerting rules and integrate Alertmanager for notification routing.
5. Iterate on label design and monitor cardinality and storage costs.

Example PromQL queries to try:

```promql theme={null}
