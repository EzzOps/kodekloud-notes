# Designing Pipeline with Prometheus and Thanos

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/System-Design/Designing-Pipeline-with-Prometheus-and-Thanos/page

Guide to building a scalable Prometheus metrics pipeline with Thanos and S3 for long term storage, global querying, downsampling, and Grafana integration in Kubernetes

When you run hundreds of microservices in production, collecting observability data becomes essential to understand health and performance.

* Logs tell the story of what happened: which requests were served, what errors occurred, and where failures originated.
* Metrics provide numeric measurements: request rates, memory usage, request latency, error counts, and more.

Without metrics and logs you lack the signals needed to debug failures or make capacity decisions. But at scale, simply collecting metrics becomes its own engineering challenge. This guide explains a practical metrics pipeline for Kubernetes that keeps Prometheus fast and replaceable while retaining months of historical data using Thanos and object storage.

Imagine a Kubernetes cluster with more than one hundred microservices, each exposing a `/metrics` endpoint. Prometheus scrapes these endpoints on a regular interval (commonly every 15s), performs an HTTP GET, parses the metrics, and stores samples with timestamps.

<Frame>
  <img alt="The image shows a visual representation of a Kubernetes cluster with a focus on metrics for an &#x22;orders&#x22; service, displaying statistics like total HTTP requests, request latency, memory in use, and total errors." />
</Frame>

A naive representation of raw Prometheus samples looks like:

```text theme={null}
12:04:01 http_requests_total 437
12:04:16 memory_in_use 23%
12:04:31 http_requests_total 451
12:04:46 request_latency_ms 18ms
12:05:01 http_requests_total 466
```

Prometheus does not keep each sample as an individual file or row. Instead, it groups samples into time-series blocks in the local TSDB on the Prometheus pod. Older blocks are removed once they pass the configured retention window, so a single Prometheus pod is constrained by disk size and retention settings.

<Frame>
  <img alt="The image is an illustration of a Kubernetes cluster using Prometheus for metrics storage, highlighting the need for historical data for debugging and capacity planning over a span of 15 minutes to 6 months." />
</Frame>

With hundreds of services exporting many metrics, local disk fills quickly and old blocks are pruned. Increasing disk only delays the problem; it does not provide a scalable long-term store. The typical, battle-tested pattern is:

* Keep Prometheus short-lived and low-retention (fast local queries).
* Offload older sealed blocks to cheap object storage (e.g., Amazon S3) for long-term retention and queryability.

Prometheus has no native S3 backend—this is where Thanos complements Prometheus.

Thanos is an open-source, modular extension for Prometheus that adds long-term storage, global querying, downsampling, and high availability. Thanos is composed of small, purpose-built components that you deploy alongside Prometheus and your object storage.

<Frame>
  <img alt="The image illustrates a Kubernetes cluster integrated with Prometheus for metrics collection, and an overview of Thanos, an open-source add-on for Prometheus. It also shows Amazon S3 as a storage option." />
</Frame>

Key Thanos components and their responsibilities:

|      Component | Role                                          | Purpose                                                                                                                                                                 |
| -------------: | --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Thanos Sidecar | Runs alongside each Prometheus instance       | Uploads sealed Prometheus blocks to S3 and exposes Prometheus's TSDB/query API over gRPC for Thanos Query to read recent data.                                          |
|  Store Gateway | Reads Thanos block format from object storage | Makes historical blocks in S3 queryable, serving long-term data to the query layer.                                                                                     |
|   Thanos Query | Single query front-end                        | Fans out PromQL queries to sidecars (recent data) and Store Gateways (historical data), merges timelines, and deduplicates series from replicated Prometheus instances. |
|      Compactor | Background processing for blocks              | Merges small blocks, downsamples older data to lower resolution, and enforces configured retention policies on the object store.                                        |

When a user or Grafana queries Thanos Query, the component aggregates responses from local sidecars and the Store Gateway, merges timelines, and removes duplicates so the result is a single consistent timeseries regardless of the underlying storage source.

<Frame>
  <img alt="The image is a diagram showing a Kubernetes cluster setup with Prometheus and Thanos for monitoring, depicting the flow of metrics data to an Amazon S3 storage and user queries through Thanos components." />
</Frame>

Grafana integration is straightforward: Grafana queries a metrics backend and does not store metrics itself. Point Grafana at Thanos Query and run PromQL exactly as you would against Prometheus. Thanos Query will return merged, deduplicated results, so dashboards present a seamless timeline across short-term and long-term data.

For short-term availability and to avoid data loss before sidecars upload sealed blocks, run multiple Prometheus replicas (for example, two replicas scraping the same targets). When replicas scrape the same targets, give each an `external_labels` value (for example, `replica="prometheus-1"`) so Thanos Query can deduplicate overlapping series at query time.

To keep the object store efficient and performant, add the Thanos Compactor. The compactor:

* Merges many small blocks into larger ones to reduce object count and improve query performance.
* Performs downsampling for older data (e.g., reducing resolution from 15s to 5m).
* Enforces the long-term retention policy for historical data (for example, six months).

This Prometheus + Thanos architecture (sidecar + S3 + store gateway + query + compactor) yields a scalable, queryable metrics platform: high-resolution recent data remains on Prometheus local disk, while months of historical data live cheaply in S3 and remain queryable.

Ready to build it? The best way to learn is by doing. The guided walkthrough below incrementally constructs the pipeline so you can observe each component as you add it.

<Callout icon="lightbulb">
  This walkthrough uses a pre-provisioned Kubernetes cluster with a handful of services and a Prometheus instance. Each step includes the commands you need, tips, and links to the Prometheus UI, Thanos Query, and Grafana so you can follow along interactively.
</Callout>

The walkthrough scales the example to a manageable size: a cluster with four small services and a single Prometheus already scraping them. You will add Thanos components, configure S3 uploads, introduce replication, and enable compaction to evolve the system from a local-only Prometheus to a full Thanos-backed pipeline. The environment provides one-click access to the Prometheus UI, Thanos Query, and Grafana dashboards so you can inspect results without hunting for ports or URLs.

<Frame>
  <img alt="The image shows a training module interface from KodeKloud on building a metrics pipeline with Prometheus and Thanos, featuring a task description on the left and a terminal window on the right. The task involves comparing Thanos and Prometheus in Grafana with step-by-step instructions." />
</Frame>

Common commands you will use when exploring the cluster:

```bash theme={null}
kubectl get pods -n apps
kubectl get pods -n monitoring
kubectl logs -n monitoring prometheus-monitoring-kube-prometheus-0
```

I strongly recommend completing the walkthrough end-to-end. Expect challenges—debugging integration issues is the fastest way to understand how each component fits together and how the full pipeline behaves in production.

Links and references

* Prometheus: [https://prometheus.io](https://prometheus.io)
* Thanos: [https://thanos.io](https://thanos.io)
* Grafana: [https://grafana.com](https://grafana.com)
* Amazon S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)
* PromQL basics: [https://prometheus.[SECRET_REDACTED]/](https://prometheus.[SECRET_REDACTED]/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/ef53ec43-96e9-4d1b-8a6e-e6eb97b0d0dc/lesson/4c1d9c1d-8fe7-4812-826d-f96feec2c731" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/ef53ec43-96e9-4d1b-8a6e-e6eb97b0d0dc/lesson/52f83eb4-1ef7-4cc3-a427-44ed868a4644" />
</CardGroup>
