# prometheus.yml (datacenter 1)
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
        labels:
          app: "prometheus"

  - job_name: "node"
    static_configs:
      - targets: ["192.168.64.8:9100", "192.168.64.8:9101"]
```

Example configuration for Datacenter 2 (Prometheus 2)

```yaml theme={null}
# prometheus.yml (datacenter 2)
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
        labels:
          app: "prometheus"

  - job_name: "node"
    static_configs:
      - targets: ["192.168.64.10:9100", "192.168.64.10:9101"]
```

Both local Prometheus servers scrape only their local nodes. This pattern limits cross-datacenter network load and distributes scraping work.

You can verify each Prometheus is scraping its targets (example UI view):

<Frame>
  <img alt="This image shows a Prometheus monitoring interface displaying the status of various endpoints, including nodes and Prometheus instances, with their last scrape times and states indicated as &#x22;UP&#x22;." />
</Frame>

## Problem: multiple UIs and potential overload

If you need to inspect metrics from many datacenters, opening each Prometheus UI is inconvenient. A global Prometheus can scrape the local Prometheus servers' federation endpoint (`/federate`) to provide a single view.

Initial global Prometheus scrape job for federation (example)

```yaml theme={null}
# prometheus.yml (global)
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
        labels:
          app: "prometheus"

  - job_name: "prometheus-federation"
    metrics_path: "/federate"
    honor_labels: true
    params:
      'match[]':
        - '{job="node"}'
    static_configs:
      - targets: ["172.16.17.128:9090", "172.16.17.129:9090"]
```

This configuration instructs the global Prometheus to query each local Prometheus at `/federate` and request timeseries that match `job="node"`.

Querying the global Prometheus for a node metric (example UI):

<Frame>
  <img alt="The image shows the Prometheus query interface open in a web browser, with a query being entered for metrics starting with &#x22;node&#x22;. Various metric options and their statuses are displayed below the query box." />
</Frame>

Example result returned by the global Prometheus after federation:

```Prometheus theme={null}
node_memory_MemAvailable_bytes{instance="192.168.64.10:9100", job="node"}
node_memory_MemAvailable_bytes{instance="192.168.64.10:9101", job="node"}
node_memory_MemAvailable_bytes{instance="192.168.64.8:9100", job="node"}
node_memory_MemAvailable_bytes{instance="192.168.64.8:9101", job="node"}
```

This shows timeseries from both datacenters are visible in the global Prometheus. However, federating instance-level metrics like these introduces important design risks.

## Why federating instance-level metrics is dangerous

* High cardinality: sending every node/instance metric to a central Prometheus multiplies label combinations and can overwhelm the server.
* Duplicate metric collisions: if multiple sources expose the same metric name and identical label sets (e.g., `job="node"`), the global Prometheus may receive samples with the same metric+labels and identical timestamps but different values. Prometheus treats this as conflicting samples and drops them, logging errors.

Example of ingestion error logs (cleaned):

```plaintext theme={null}
time=2025-07-14T23:36:41.358Z level=INFO   source=checkpoints.go:192 msg="Error on ingesting samples with different value but same timestamp" component="scrape manager" scrape_pool=prometheus-federation
time=2025-07-14T23:36:41.358Z level=WARN   source=scrape.go:1096       msg="Error on ingesting samples with different value but same timestamp" component="scrape manager" scrape_pool=prometheus-federation target="http://172.16.17.129:9090/federate?match%3D%7B__name%3D~" num_dropped=2
```

<Callout icon="warning">
  If the same metric name and label set are produced by multiple sources, Prometheus can reject samples with identical timestamps but differing values. This commonly occurs when federating raw instance-level metrics.
</Callout>

<Callout icon="lightbulb">
  Best practice: Do not federate high-cardinality, instance-level metrics to a single global Prometheus. Instead, federate aggregated, lower-cardinality metrics computed locally (recording rules) and include a distinguishing label (for example `datacenter="dc1"`).
</Callout>

## Solution: aggregate locally with recording rules and add a datacenter label

1. On each local Prometheus, define recording rules that aggregate instance-level series (sums, rates, etc.).
2. Add a `datacenter` label to those recorded metrics to identify their origin.
3. Configure the global Prometheus to federate only those recorded (aggregated) metric names.

Example recording rules file (rules.yaml) — Datacenter 1

```yaml theme={null}
groups:
  - name: aggregated-node-metrics
    rules:
      - record: node:cpu_seconds:sum_rate5m
        expr: sum(rate(node_cpu_seconds_total[5m])) by (job)
        labels:
          datacenter: "dc1"
      - record: node:memory_MemAvailable_bytes:sum
        expr: sum(node_memory_MemAvailable_bytes) by (job)
        labels:
          datacenter: "dc1"
```

For Datacenter 2, create the same rules but set `datacenter: "dc2"`.

Include the rules file in each local Prometheus configuration:

```yaml theme={null}
# prometheus.yml (datacenter 1) - include recorded rules
rule_files:
  - "rules.yaml"
```

Restart the local Prometheus servers so they evaluate the recording rules and publish the aggregated metrics. Each local Prometheus will now expose recorded metrics such as:

```PromQL theme={null}
node:cpu_seconds:sum_rate5m{job="node", datacenter="dc1"}
node:memory_MemAvailable_bytes:sum{job="node", datacenter="dc1"}
```

Adjust the global Prometheus federation scrape to request only the recorded metric names:

```yaml theme={null}
# prometheus.yml (global) - federate only aggregated metric names
scrape_configs:
  - job_name: "prometheus-federation"
    metrics_path: "/federate"
    honor_labels: true
    params:
      'match[]':
        - '{__name__="node:cpu_seconds:sum_rate5m"}'
        - '{__name__="node:memory_MemAvailable_bytes:sum"}'
    static_configs:
      - targets: ["172.16.17.128:9090", "172.16.17.129:9090"]
```

With this setup:

* Local Prometheus instances compute aggregated metrics and attach a `datacenter` label.
* The global Prometheus federates only aggregated metrics (low cardinality).
* The `datacenter` label distinguishes origins and prevents ingestion conflicts.

Example query on the global Prometheus, asking for memory available from datacenter 2:

```PromQL theme={null}
node:memory_MemAvailable_bytes:sum{datacenter="dc2", job="node"}
```

Example returned value:

```text theme={null}
158975425656
```

## Quick reference: federation do's and don'ts

| Action                          | Recommendation | Example / Note                                                                                                              |
| ------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Federate instance-level metrics | Don't          | Avoid federating `node_*` per-instance series in bulk.                                                                      |
| Federate aggregated metrics     | Do             | Record aggregation locally, e.g. `node:memory_MemAvailable_bytes:sum`.                                                      |
| Distinguish origin              | Do             | Add `datacenter: "dc1"` as a label on recorded rules.                                                                       |
| Global match filters            | Use            | In global `params.match[]` request only recorded metric names, e.g. `'{__name__="node:cpu_seconds:sum_rate5m"}'`.           |
| Prevent collisions              | Use            | Ensure global Prometheus never receives identical metric+label combinations from different sources without an origin label. |

## Summary: recommended workflow

1. Keep local scraping per datacenter for instance-level metrics.
2. Create recording rules locally that aggregate instance-level metrics and add a `datacenter` label.
3. Federate only the aggregated recorded metrics to the global Prometheus.
4. Query the global Prometheus for datacenter-level metrics to get a single pane of glass without overwhelming it.

## Links and references

* Prometheus federation docs: [https://prometheus.io/docs/prometheus/latest/federation/](https://prometheus.io/docs/prometheus/latest/federation/)
* Prometheus recording rules: [https://prometheus.io/docs/practices/rules/](https://prometheus.io/docs/practices/rules/)
* Prometheus best practices (scalability & federation): [https://prometheus.io/docs/introduction/overview/](https://prometheus.io/docs/introduction/overview/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/def44ace-3439-4128-88c2-b701bf182baf/lesson/7d338452-830c-41ae-a26c-e2a1b53f47f3" />
</CardGroup>


# Horizontal Sharding

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Scaling-Long-Term-Storage/Horizontal-Sharding/page

Guide to horizontally sharding Prometheus scrape jobs using hashmod relabeling to distribute targets across multiple instances.

This lesson shows how to horizontally shard a heavy Prometheus scrape job so that no single Prometheus instance becomes a bottleneck. We use Prometheus `relabel_configs` with the `hashmod` action to split a single job's targets across multiple Prometheus servers.

Why shard?

* Large scrape jobs with many targets can increase CPU, memory, and scrape latency for a single Prometheus server.
* Sharding distributes scraping load across N Prometheus instances while keeping a single shared target list.

Key terms

* hashmod: a relabel action that computes `hash(target) % modulus` and stores the result in a label.
* shard index: the integer (0..N-1) assigned to a Prometheus instance that determines which subset of targets it keeps.
* `__address__`: the label containing the target address (host:port).

Overview

1. Compute a hashmod of each target address and store it in a temporary label (commonly `__tmp_hashmod`).
2. Keep only targets whose hashmod equals the shard index assigned to that Prometheus instance.
3. Repeat the same scrape configuration on each instance, changing only the `keep` `regex` to the instance’s shard index.

Example: initial single-instance scrape configuration

```yaml theme={null}
scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
        labels:
          app: "prometheus"

  - job_name: "node"
    static_configs:
      - targets:
        - "192.168.64.8:9100"
        - "192.168.64.8:9101"
        - "192.168.64.10:9100"
        - "192.168.64.10:9101"
```

This single Prometheus instance scrapes all node targets. To shard across multiple Prometheus servers, use `relabel_configs` with `hashmod`.

Full common configuration (applies to all Prometheus instances)

```yaml theme={null}
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
      - targets: ["alertmanager:9093"]

rule_files:
  - "rules.yml"

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
        labels:
          app: "prometheus"

  - job_name: "node"
    static_configs:
      - targets:
        - "192.168.64.8:9100"
        - "192.168.64.8:9101"
        - "192.168.64.10:9100"
        - "192.168.64.10:9101"
```

Sharding configuration details

* Use `modulus: N` where `N` is the number of Prometheus instances (shards).
* On each Prometheus instance, set the `keep` `regex` to the instance’s shard index (`0`..`N-1`).
* The first relabel writes the hashmod result into `__tmp_hashmod`. The second relabel filters targets based on that value.

Prometheus instance A (shard 0)

```yaml theme={null}
scrape_configs:
  - job_name: "node"
    static_configs:
      - targets:
        - "192.168.64.8:9100"
        - "192.168.64.8:9101"
        - "192.168.64.10:9100"
        - "192.168.64.10:9101"
    relabel_configs:
      # Step 1: hash the __address__ and write result into a temporary label
      - source_labels: [__address__]
        action: hashmod
        modulus: 2
        target_label: __tmp_hashmod

      # Step 2: keep only targets that map to shard 0
      - source_labels: [__tmp_hashmod]
        regex: "0"
        action: keep
```

Prometheus instance B (shard 1)

```yaml theme={null}
scrape_configs:
  - job_name: "node"
    static_configs:
      - targets:
        - "192.168.64.8:9100"
        - "192.168.64.8:9101"
        - "192.168.64.10:9100"
        - "192.168.64.10:9101"
    relabel_configs:
      - source_labels: [__address__]
        action: hashmod
        modulus: 2
        target_label: __tmp_hashmod

      - source_labels: [__tmp_hashmod]
        regex: "1"
        action: keep
```

How it works (step-by-step)

| Step | Action                                                                                | Result                                                                   |
| ---- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| 1    | Compute `hashmod(__address__) % modulus` via `hashmod` relabel action                 | Result (`0..N-1`) stored in `__tmp_hashmod`                              |
| 2    | Use `keep` relabel with `source_labels: [__tmp_hashmod]` and `regex: "<shard_index>"` | Only targets with matching hashmod are kept for that Prometheus instance |
| 3    | Repeat on each instance with `regex` set to its shard index                           | Targets are partitioned across the N Prometheus servers                  |

Best practices and considerations

* Set `modulus` equal to the number of Prometheus instances. For example, use `modulus: 4` for four shards.
* Hash-based distribution is near-uniform with many targets. If you have few targets, distribution may be uneven.
* Keep the static target list identical on all Prometheus servers; only the relabel `keep` regex differs.
* If you add or remove Prometheus instances (change `modulus`), hash assignments will change; expect some target movement between instances.

Verification

* Confirm shard behavior using Prometheus’s Status → Targets (Target Health) page for each instance. This page shows which targets each Prometheus server is scraping.
* Use the Prometheus UI and logs to verify that each instance scrapes only the expected subset of targets.

Links and references

* [Prometheus relabeling documentation](https://prometheus.[AWS_SECRET_ACCESS_KEY]configuration/#relabel_config)
* [Prometheus Status → Targets](https://prometheus.io/docs/operating/accessing/)
* [Prometheus best practices for scaling](https://prometheus.io/docs/introduction/overview/)

<Frame>
  <img alt="The image shows a Prometheus monitoring dashboard displaying target endpoints and their status, with all listed endpoints currently marked as &#x22;UP.&#x22;" />
</Frame>

<Callout icon="lightbulb">
  When choosing the `modulus`, make it equal to the number of Prometheus servers you plan to use. For large numbers of targets, `hashmod` yields an approximately even distribution; for a small number of targets the distribution may be uneven.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/def44ace-3439-4128-88c2-b701bf182baf/lesson/74055a28-cbf5-4021-bd6d-73fcac46c1f6" />
</CardGroup>
