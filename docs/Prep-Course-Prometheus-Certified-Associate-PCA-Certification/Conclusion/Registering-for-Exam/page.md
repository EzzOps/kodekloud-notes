# Rate of HTTP requests per second across all instances
sum by (job) (rate(http_requests_total[5m]))

# 95th percentile request duration for a particular service
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))
```

## Best practices & considerations

* Design labels carefully: prefer stable, low-cardinality labels such as `job`, `service`, and `region`. Avoid high-cardinality labels like unique request IDs.
* Keep retention and storage trade-offs in mind: longer retention increases cost and storage requirements.
* Use exporters for third-party systems (node\_exporter, kube-state-metrics, Blackbox exporter) rather than custom scraping where possible.
* Protect your Prometheus server: secure access to the UI, consider remote write to long-term storage, and set resource limits for scaling.

<Callout icon="lightbulb">
  We'd love your feedback. Please share topics you'd like us to cover next so we can continue creating helpful, high-quality content.
</Callout>

## Further reading & references

* [Prometheus Documentation](https://prometheus.io/docs/)
* [PromQL Guide](https://prometheus.[SECRET_REDACTED]/)
* [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)
* [Grafana](https://grafana.com/)
* [Prometheus Exporters](https://prometheus.io/docs/instrumenting/exporters/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/803356a8-be12-48c5-b49b-4a44e66ba3a3/lesson/af00a389-409b-404b-9e18-87b0c8dce7c6" />
</CardGroup>


# Registering for Exam

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Conclusion/Registering-for-Exam/page

Instructions for registering, scheduling, and preparing for the Prometheus Certified Associate exam on the Linux Foundation Training site

To register for the Prometheus Certified Associate (PCA) exam, open the Linux Foundation Training site and go to the My Training portal:

* [https://training.linuxfoundation.org](https://training.linuxfoundation.org)

<Frame>
  <img alt="The image shows a webpage from The Linux Foundation advertising the &#x22;2022 - 10th Open Source Jobs Report.&#x22; It features a person wearing glasses with code reflected in them and text highlighting critical skills, hiring trends, and education." />
</Frame>

Sign in using your preferred method (email, Google, GitHub, etc.). If you do not yet have an account, select Create an Account and follow the on-screen registration steps.

<Frame>
  <img alt="The image shows a login page for The Linux Foundation's Training & Certification, with options to sign in using email or social media accounts." />
</Frame>

After signing in you will arrive at your training dashboard. Use the search box to look for "PCA" or "Prometheus Certified Associate." Click the exam/course result to view detailed information, including pricing, available date/time options, and any bundled materials.

<Frame>
  <img alt="The image shows a website portal interface with a welcome message and options to connect GitHub and LinkedIn. Various course options are displayed below." />
</Frame>

Steps to complete registration and scheduling

1. On the PCA exam/course page, confirm the exam price and click Enroll Now.
2. Proceed to checkout and enter your payment information.
3. After payment, follow the final registration steps. Typical items include:
   * Providing identification details.
   * Choosing an exam date and time (or scheduling with the proctoring provider).
   * Confirming contact information and any required policies/agreements.
4. Complete these steps and confirm your appointment. You should receive a confirmation email with scheduling and exam access details.

Quick checklist: what you will need before the exam

| Item                          | Why it matters                                       | Notes                                                        |
| ----------------------------- | ---------------------------------------------------- | ------------------------------------------------------------ |
| Government-issued photo ID    | Required for identity verification during proctoring | Check the confirmation email for exact accepted IDs          |
| Stable internet connection    | Required for online, proctored delivery              | Prefer wired connections and close unnecessary apps          |
| Compatible computer & browser | Proctoring may require specific OS/browser versions  | See exam instructions for system requirements                |
| Payment method                | To complete enrollment                               | Card or other supported payment options on the checkout page |
| Scheduling preferences        | To reserve a convenient slot                         | Time zone and proctor availability affect options            |

<Callout icon="lightbulb">
  Before your test date, make sure you have the required form(s) of ID ready (usually a government-issued photo ID). Check the confirmation email or the exam page for the exact ID requirements and any proctoring instructions.
</Callout>

Additional resources and links

* Linux Foundation Training: [https://training.linuxfoundation.org](https://training.linuxfoundation.org)
* Prometheus project documentation: [https://prometheus.io/docs/](https://prometheus.io/docs/)
* General exam preparation tips: review the PCA exam objectives on the exam page after enrolling.

Once you've completed registration and received confirmation, you are set to take the PCA exam on your scheduled date. Good luck!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/803356a8-be12-48c5-b49b-4a44e66ba3a3/lesson/1213f02c-9690-4cae-a941-d3ebc75fe2b7" />
</CardGroup>
