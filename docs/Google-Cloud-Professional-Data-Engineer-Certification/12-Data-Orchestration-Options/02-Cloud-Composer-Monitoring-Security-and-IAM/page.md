# Cloud Composer Monitoring Security and IAM

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Orchestration-Options/Cloud-Composer-Monitoring-Security-and-IAM/page

Guide to Cloud Composer monitoring, security, IAM roles, service accounts, network controls, and cost optimization for running and maintaining production Airflow environments on Google Cloud

Hello and welcome back.

This lesson explains how Cloud Composer supports monitoring, security, and IAM for running production Airflow environments. It builds on orchestration patterns and DAG triggering methods in Cloud Composer and focuses on what to do after your environment is deployed: keeping it healthy, secure, and cost-efficient.

We cover three areas:

* Monitoring your Airflow environment
* Security and IAM controls
* Cost optimization strategies

***

## Monitoring

Observability is essential when workflows run on schedules—from every minute to once per day. Use multiple layers of visibility so teams can detect, triage, and resolve issues quickly.

### Key monitoring surfaces

* Airflow UI — First stop for runtime triage: view task status, durations, DAG runs, retries, and per-task logs. Useful for identifying long-running tasks, failures, and retry patterns. Note: access to the Airflow web UI may depend on your environment’s network configuration (public, private, or IAP-protected).
* Cloud Logging — Composer forwards Airflow and worker logs to [Cloud Logging](https://cloud.google.com/logging), providing centralized, queryable logs for troubleshooting and historical analysis.
* Cloud Monitoring — Expose environment and worker metrics to [Cloud Monitoring](https://cloud.google.com/monitoring) and create alerting policies for task failures, scheduler latency, CPU/memory saturation, and other operational thresholds.

### Recommended metrics and alerts

* Scheduler health: heartbeat, DAG parse time, and DAG queue length
* Worker resources: CPU, memory, and pod restarts
* Task-level indicators: failure rate, average duration, retry counts

Create metric-based or log-based alerts to notify teams immediately when critical thresholds are crossed rather than waiting for downstream failures.

### Troubleshooting and error tracking

* Use aggregated log queries to identify recurring errors and reduce mean time to resolution (MTTR).
* Combine Airflow UI task logs with Cloud Logging entries for environment-level context.
* Use Cloud Monitoring dashboards to visualize trends and correlate spikes in failures with resource or scheduling events.

Sample exam-style question: How does Cloud Composer provide monitoring and logging capabilities?\
Answer: Through the Airflow UI, [Cloud Logging](https://cloud.google.com/logging), [Cloud Monitoring](https://cloud.google.com/monitoring), and the Cloud Composer UI in the GCP Console.

<Frame>
  <img alt="A slide titled &#x22;Monitoring&#x22; showing five colored rounded boxes labeled: &#x22;Task status and duration,&#x22; &#x22;Comprehensive logging,&#x22; &#x22;Alerting and notifications,&#x22; &#x22;Performance metrics,&#x22; and &#x22;Error tracking.&#x22;" />
</Frame>

***

## Security and IAM

Security is critical for production environments. Cloud Composer relies on IAM roles, service accounts, and network controls to protect access and limit blast radius.

### IAM Roles and responsibilities

Use predefined Composer roles to grant the appropriate level of access:

| Role                    | Purpose                                                  | Typical assignment                                                             |
| ----------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `roles/composer.admin`  | Full administrative control over Composer environments   | Environment operators and platform admins                                      |
| `roles/composer.user`   | Access to the Airflow UI; trigger DAGs and view DAG runs | Data analysts or pipeline operators who should not change environment settings |
| `roles/composer.worker` | Used by internal Composer components that execute tasks  | Assigned to system components, not humans                                      |

> Note: Access to the Airflow UI may also require additional network/IAP or Cloud Storage permissions depending on your environment configuration.

### Service accounts and Workload Identity

* Airflow tasks should run using dedicated service accounts with the least privilege required to access resources such as BigQuery, Cloud Storage, Pub/Sub, and Secret Manager.
* Prefer Workload Identity for Kubernetes-based environments to avoid embedding node-level credentials and to grant per-task identities with fine-grained IAM bindings.

### Network controls and isolation

* Use VPC configuration and private Composer environments to keep webserver and scheduler traffic internal.
* Protect Airflow UI with IAP or private connectivity to avoid public exposure.

Example: If a finance analyst only needs to trigger an existing DAG to refresh a dashboard, assign the `roles/composer.user` role and ensure network/IAP access is configured. This grants safe, limited access without environment modification rights.

<Callout icon="warning">
  Restrict task-run service accounts with least-privilege IAM and avoid granting broad roles like Owner to task identities. Use Workload Identity to minimize credential exposure.
</Callout>

<Frame>
  <img alt="A slide titled &#x22;Security and IAM&#x22; showing five colored tiles labeled composer.admin, composer.worker, composer.user, Service accounts, and VPC controls. The slide is © KodeKloud." />
</Frame>

***

## Cost Optimization

Controlling costs is essential for long-term sustainability. Apply practical strategies across sizing, scaling, and DAG design.

### Practical cost strategies

* Right-size environments: pick machine types and node counts that align with workload patterns; avoid oversized defaults for small or sporadic pipelines.
* Scale based on workload: enable autoscaling for workers so capacity grows only when tasks demand it.
* Manage unused environments: stop, delete, or use ephemeral environments for dev/test to avoid continuous charges.
* Monitor usage: track worker CPU, memory, and task concurrency to inform resizing decisions.
* Optimize DAGs: refactor long-running tasks, minimize unnecessary task count, and design dependencies that reduce parallelism when not needed.

Sample exam-style question: What is a simple way to reduce Cloud Composer cost in a testing environment?\
Answer: Downscale the environment and configure autoscaling for workers so resources match demand.

<Frame>
  <img alt="A presentation slide titled &#x22;Cost Optimization.&#x22; It shows five colorful boxes with tips: &#x22;Right-size environments,&#x22; &#x22;Schedule-based scaling,&#x22; &#x22;Auto-pause unused,&#x22; &#x22;Monitor resource usage,&#x22; and &#x22;Optimize DAG design.&#x22;" />
</Frame>

***

## Summary

* Monitoring: combine the Airflow UI, Cloud Logging, and Cloud Monitoring to keep pipelines healthy and reduce MTTR.
* Security & IAM: use predefined Composer roles, dedicated service accounts, Workload Identity, and VPC/private environments to enforce least privilege and network isolation.
* Cost optimization: right-size environments, enable autoscaling, manage unused resources, and optimize DAG design.

<Callout icon="lightbulb">
  Tip: When preparing for exams or production deployment, map monitoring tools, IAM roles, and cost controls to specific Composer features (Airflow UI, Cloud Logging/Monitoring, predefined IAM roles, service accounts, and network settings).
</Callout>

Further reading and references:

* Cloud Composer documentation: [https://cloud.google.com/composer](https://cloud.google.com/composer)
* Cloud Logging: [https://cloud.google.com/logging](https://cloud.google.com/logging)
* Cloud Monitoring: [https://cloud.google.com/monitoring](https://cloud.google.com/monitoring)
* Workload Identity: [https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity)

A later lesson will review Cloud Composer production best practices to help you operate Composer effectively in your organization.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/ff8693f0-36fe-4cca-9b05-f27ffa81ccb4/lesson/36de5951-f8ed-49d4-91c6-0c15d77fb52b" />
</CardGroup>
