# Thanos

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Scaling-Long-Term-Storage/Thanos/page

Describes Thanos roles and benefits with Prometheus, enabling unified querying, HA deduplication, and cost effective long term metric storage to object stores

This lesson covers the essentials of Thanos: what it is, why you’d use it with Prometheus, and the core components to understand for reliable long‑term metric storage and unified querying.

> **lightbulb** For the exam you do not need to memorize Thanos's entire internals. Focus on its purpose—providing long‑term storage and a single query layer for multiple Prometheus instances—and the main benefits summarized below.

Why use Thanos with Prometheus?

* Single pane of glass: Query metrics from many Prometheus instances through one Thanos Query endpoint instead of logging into each Prometheus server.
* High‑availability deduplication: When you run Prometheus in HA (multiple Prometheus servers scraping the same targets), Thanos can deduplicate duplicate series so dashboards and alerts reflect a single logical view.
* Cost‑effective long‑term storage: Thanos uploads Prometheus TSDB blocks to object stores (AWS S3, Azure Blob Storage, GCS) so local disk usage on each Prometheus server doesn’t grow without bound.

Key terminology and components

| Component      | Responsibility                                                                                                   | Typical deployment                                                        |
| -------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Thanos Sidecar | Runs alongside each Prometheus, uploads TSDB blocks to object storage and serves recent local data over gRPC     | Deployed as a sidecar container in the same pod as Prometheus             |
| Thanos Store   | Reads historical TSDB blocks from object storage and serves them over gRPC                                       | Stateless component that accesses object store buckets                    |
| Thanos Query   | Query frontend that understands PromQL, federates queries across sidecars and stores, and performs deduplication | Single (or HA) entry point for dashboards and API clients (e.g., Grafana) |

Architecture overview

* Thanos Sidecar: Deployed with each Prometheus server. Uploads local blocks to long‑term object storage and exposes the instance’s recent data to Thanos Query.
* Thanos Store: Loads historical blocks from object storage (S3, GCS, Azure Blob) and serves those blocks to Thanos Query.
* Thanos Query: The PromQL‑aware query frontend that merges results from sidecars (recent data) and stores (historical data), deduplicates series, and returns unified results to clients such as Grafana.

Typical query flow: a user issues a PromQL query to Thanos Query, which fans out the query to relevant sidecars for recent data and to the Thanos Store for historical blocks, then merges and deduplicates results before returning them.

<Frame>
  <img alt="The image depicts a diagram of Thanos architecture, showing the interaction between Prometheus servers, Thanos Sidecars, a central storage bucket, Thanos Store, Thanos Query, and a Grafana client." />
</Frame>

Prometheus TSDB blocks, compaction, and Thanos
Prometheus writes TSDB blocks (commonly every 2 hours). Prometheus also performs block compaction to merge small blocks into larger ones for better query efficiency. However, compaction rewrites, merges, or deletes blocks while the Thanos Sidecar is concurrently uploading them, which can cause transient upload races or failures.

To keep block layouts stable for Thanos uploads, many deployments disable Prometheus automatic compaction by setting the minimum and maximum block duration to the same value. For example:

```bash theme={null}
--storage.tsdb.min-block-duration=2h
--storage.tsdb.max-block-duration=2h
```

Setting both flags to the same duration (here, `2h`) prevents Prometheus from running compaction and keeps block boundaries stable while Thanos uploads blocks to object storage.

> **warning** Disabling compaction reduces Prometheus's on‑disk optimizations and can affect local query performance or disk usage patterns. Test this configuration in staging and monitor resource use before applying in production.

Best practices and exam focus

* Focus on what Thanos does and the benefits it adds to Prometheus: unified querying, deduplication for HA, and long‑term storage in object stores.
* Know the roles of Sidecar, Store, and Query as the main Thanos building blocks.
* Understand why you might disable Prometheus compaction when integrating with Thanos and be aware of the operational tradeoffs.

References

* Thanos documentation: [https://thanos.io/](https://thanos.io/)
* Prometheus TSDB concepts: [https://prometheus.io/docs/introduction/overview/](https://prometheus.io/docs/introduction/overview/)

Summary

* Thanos provides a global view across multiple Prometheus servers, deduplicates HA series, and enables durable, cost‑effective long‑term storage by backing Prometheus blocks up to object stores.
* For exam purposes, prioritize understanding Thanos’s purpose and the core components rather than its full internal architecture.

<Frame>
  <img alt="The image shows a &#x22;Prometheus Compaction&#x22; interface with a &#x22;Enable Compaction&#x22; button and three 2-hour blocks. A Prometheus logo is visible on the left." />
</Frame>

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/def44ace-3439-4128-88c2-b701bf182baf/lesson/1035ade6-c5f7-4c58-8f4d-a8f59891cb97)
