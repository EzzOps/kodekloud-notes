# Dataproc Cluster Optimization and Sizing

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Processing/Dataproc-Cluster-Optimization-and-Sizing/page

Guidance for right‑sizing and optimizing Google Dataproc clusters by matching machine types to workloads, measuring bottlenecks, and using autoscaling, preemptible and ephemeral clusters to reduce cost.

Welcome — this lesson outlines a repeatable approach to right-sizing and optimizing Dataproc clusters so they run efficiently and cost-effectively. If your organization manages many clusters (for example 15–20), a consistent process helps avoid wasted spend and unpredictable job performance.

Start by answering two high-level questions:

* What does the workload look like? — CPU‑bound, memory‑bound, I/O‑bound, or mixed?
* How are clusters used? — interactive, recurring batch, ad‑hoc, long‑lived, or short‑lived?

## Machine types — choose based on workload characteristics

Select worker machine types that align with workload behavior rather than picking instances at random. Below is a quick reference to guide machine selection:

| Machine family   | Typical use case                                                                      | Example                |
| ---------------- | ------------------------------------------------------------------------------------- | ---------------------- |
| Standard         | Balanced CPU and memory for general-purpose Spark jobs                                | `N1-standard`          |
| Memory-optimized | Large in-memory computation or heavy caching (Spark RDD/DataFrame cache)              | `N1-highmem`           |
| CPU-optimized    | Compute-heavy workloads such as large aggregations or CPU-bound ML training           | `N1-highcpu`           |
| Custom           | Exact vCPU and RAM combinations to avoid over-provisioning when you know requirements | `Custom machine types` |

Pick CPU-optimized workers for CPU-heavy MLlib training and memory-optimized workers for large in-memory caching or joins. When your job profile is unclear, start with balanced machines and iterate.

<Frame>
  <img alt="A presentation slide titled &#x22;Machine Type Selection&#x22; showing four categories—Standard, Memory, CPU-Optimized, and Custom Machines—with example instance names (N1-standard, N1-highmem, N1-highCPU) and brief descriptions of their use (balanced CPU/RAM, high RAM, high CPU, tailor resources)." />
</Frame>

## Cluster architecture and sizing tips

A Dataproc cluster typically has:

* Master node(s): run resource managers, job schedulers, metadata services, and UI endpoints.
* Worker nodes: execute Spark/YARN tasks and store local shuffle/cache data.

Practical sizing guidelines:

* Start small: one master and 2–3 workers to validate job behavior and collect metrics.
* Measure first: monitor CPU, memory, disk I/O, shuffle, and GC to find bottlenecks before scaling.
* Scale thoughtfully: increasing node count or size may not proportionally reduce job time due to task scheduling, shuffle overhead, and data skew.
* Match resources to workload: scale vCPUs for compute-bound stages and RAM for in-memory or caching stages.
* Consider data locality and disk throughput for I/O-heavy workloads; local SSD or higher network bandwidth may help.

<Frame>
  <img alt="A simple cluster architecture diagram showing a Master orchestration node at the top connected to three Worker nodes. Below it are sizing tips noting one master stores metadata, multiple workers process data, and workers should scale with data size." />
</Frame>

## Additional optimization patterns

* Autoscaling: Use Dataproc autoscaling policies to adjust worker counts based on pending tasks and measured utilization.
* Preemptible (spot) workers: Use preemptible VMs for cost savings on fault‑tolerant stages; they can be revoked at any time.
* Ephemeral clusters: Create clusters on demand for scheduled or ad‑hoc batch jobs and delete them after completion to eliminate idle costs.
* Long‑lived clusters: Appropriate for many interactive users or shared jobs — ensure monitoring, idle-node policies, and cleanup routines.
* File sizing and partitioning: Avoid many small files; aim for tens-to-hundreds of MB per file and partition data to match query access patterns.
* Instrumentation: Collect metrics (CPU, memory, disk, shuffle, GC) and job logs to identify hotspots and guide tuning decisions.

<Callout icon="lightbulb">
  When using preemptible workers, plan for worker eviction: design jobs to be fault tolerant or ensure critical stages run on non‑preemptible nodes.
</Callout>

## A recommended iterative approach

1. Start small — deploy one master and 2–3 workers to characterize job behavior and gather baseline metrics.
2. Measure — inspect stage times, task distribution, CPU/memory/disk utilization, shuffle volumes, and GC.
3. Diagnose bottlenecks — determine whether the workload is CPU‑bound, memory‑bound, I/O‑bound, or suffering from data skew/small files.
4. Adjust resources — change worker machine types (CPU vs memory), tune Spark settings, or increase node counts based on measured bottlenecks.
5. Optimize for cost — introduce autoscaling and preemptible workers for noncritical work; prefer ephemeral clusters for scheduled batches.
6. Repeat — continuously measure after each change to validate improvement and avoid over‑provisioning.

<Frame>
  <img alt="A presentation slide titled &#x22;Sizing Strategy&#x22; showing two approaches: &#x22;Start Small&#x22; (e.g., N1-standard-4 master, 2–3 workers, monitor CPU/memory, scale up if needed) and &#x22;Right Sizing&#x22; (analyze workload, match machine type, avoid over-provisioning, prevent resource waste). The slide lists practical tips for choosing and adjusting machine sizes." />
</Frame>

That concludes this lesson on Dataproc cluster optimization and sizing. Storage patterns and recommended storage options for Dataproc are covered in a separate lesson.

## Links and references

* [Dataproc documentation](https://cloud.google.com/dataproc/docs)
* [Dataproc autoscaling policies](https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/autoscaling)
* [Preemptible VMs (Compute Engine)](https://cloud.google.com/compute/docs/instances/preemptible)
* [Compute Engine machine types](https://cloud.google.com/compute/docs/machine-types)
* [Spark tuning and performance best practices](https://spark.apache.org/docs/latest/tuning.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/0883bfdc-7d2f-4371-910d-b996380ce4ac/lesson/db6895bc-c005-4eaa-beb7-e699eb8bec95" />
</CardGroup>
