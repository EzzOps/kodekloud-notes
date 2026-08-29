# DynamoDB Pricing Throughput

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/AWS-Databases-Part-1/DynamoDB-Pricing-Throughput/page

Explains DynamoDB capacity modes, throughput measurement, calculating RCUs and WCUs with examples, plus throttling causes, mitigations, and best practices for provisioning or on demand use.

This guide explains DynamoDB capacity modes, how throughput is measured, and how to calculate Read Capacity Units (RCUs) and Write Capacity Units (WCUs) for provisioned tables. You’ll learn the formulas, example calculations, and common causes/mitigations for throttling.

DynamoDB supports two capacity modes:

* Provisioned mode — you specify reads and writes per second (RCUs/WCUs) ahead of time and pay for that capacity whether fully used or not. Provisioned mode also provides temporary burst capacity.
* On-demand mode — DynamoDB automatically scales reads and writes and you pay per request. This mode is suitable for unpredictable traffic but can cost more per request than provisioned capacity.

Use provisioned mode when you can predict traffic and want lower per-request costs; use on-demand when traffic is spiky or unpredictable.

<Frame>
  <img alt="A presentation slide titled &#x22;DynamoDB Scalability&#x22; with two panels for Read Capacity Units (RCUs) and Write Capacity Units (WCUs). The slide notes one RCU = one strongly consistent read (or two eventually consistent reads) per second for items up to 4 KB (max 3,000 RCUs), and one WCU = one write per second for items up to 1 KB." />
</Frame>

## Key definitions and quick reference

| Term                      | What it represents                                                                                                                | Sizing increment                    |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| WCU (Write Capacity Unit) | One write per second for items up to 1 KB                                                                                         | `1 KB` increments (always round up) |
| RCU (Read Capacity Unit)  | One strongly consistent read per second for items up to 4 KB — or two eventually consistent reads per second for items up to 4 KB | `4 KB` increments (always round up) |

> **lightbulb** Always round up fractional units. WCUs are measured in 1 KB increments; RCUs are measured in 4 KB increments. For eventually consistent reads, each RCU supports two reads per second for items up to 4 KB.

## Write Capacity Unit (WCU) — calculation and examples

WCU sizing is based on 1 KB increments. For each write you must calculate how many 1 KB chunks the item consumes, round up, then multiply by the number of writes per second.

Formula:

```text theme={null}
Required_WCUs = writes_per_second × ceil(item_size_kB / 1)
```

Examples:

* 20 writes/sec, item size 4.5 KB\
  per-item WCUs = `ceil(4.5 / 1) = 5` → total = `20 × 5 = 100 WCUs`
* 5 writes/sec, item size 3 KB\
  per-item WCUs = `ceil(3 / 1) = 3` → total = `5 × 3 = 15 WCUs`
* 120 writes/min → 120/60 = 2 writes/sec, item size 3 KB\
  per-item WCUs = `ceil(3 / 1) = 3` → total = `2 × 3 = 6 WCUs`

<Frame>
  <img alt="A presentation slide titled &#x22;Write Capacity Units (WCUs) – Examples&#x22; with three colored example boxes that show calculations of required WCUs for different write rates and item sizes. For instance, it shows 20 items/sec at 4.5 KB = 100 WCUs, 5 items/sec at 3 KB = 15 WCUs, and 120 items/min at 3 KB = 6 WCUs." />
</Frame>

## Strongly consistent vs eventually consistent reads

* Strongly consistent read: always returns the latest committed write and costs 1 RCU per 4 KB read (per read per second).
* Eventually consistent read: may return stale data right after a write (reads from replicas that lag). One RCU supports two eventually consistent reads per second for items up to 4 KB.

To request a strongly consistent read in an API call, set `ConsistentRead = true` (or the equivalent parameter in your SDK).

<Frame>
  <img alt="An infographic titled &#x22;Strongly Consistent Read vs Eventually Consistent Read&#x22; explaining that eventual reads may return stale data while strongly consistent reads return correct data. To the right is a diagram of a user writing to a primary datastore that replicates to two read replicas." />
</Frame>

## Read Capacity Unit (RCU) — calculation and examples

Recommended approach: compute per-read RCU-equivalents, then apply consistency rules and round up.

Steps:

1. Compute per-read RCU-equivalents:

```Python theme={null}
per_read_equivalents = ceil(item_size_kB / 4)
```

2. For strongly consistent reads:

```text theme={null}
Required_RCUs = reads_per_second × per_read_equivalents
```

3. For eventually consistent reads:

```text theme={null}
Required_RCUs = ceil( (reads_per_second × per_read_equivalents) / 2 )
```

Examples:

* 20 reads/sec, eventually consistent, item size 8 KB\
  `per_read_equivalents = ceil(8 / 4) = 2`\
  per-second demand = `20 × 2 = 40` → divide by 2 → `40 / 2 = 20 RCUs`
* 10 reads/sec, strongly consistent, item size 12 KB\
  `per_read_equivalents = ceil(12 / 4) = 3` → total = `10 × 3 = 30 RCUs`
* 30 reads/sec, strongly consistent, item size 9 KB\
  `per_read_equivalents = ceil(9 / 4) = 3` → total = `30 × 3 = 90 RCUs`

<Frame>
  <img alt="A slide titled &#x22;Read Capacity Units (RCUs) – Examples&#x22; showing three colored example boxes. Each box gives a read-throughput scenario with item sizes and RCU calculations (e.g., 20 items/sec at 8 KB = 20 RCUs; 10 items/sec at 12 KB = 30 RCUs)." />
</Frame>

## Throttling: ProvisionedThroughputExceededException

When your application exceeds provisioned RCUs or WCUs, DynamoDB returns a `ProvisionedThroughputExceededException`. Common causes include:

* Aggregate throughput (table-level RCUs/WCUs) exceeded.
* Hot partition(s): a single partition key receiving a disproportionate number of requests.
* Low partition key cardinality or uneven key distribution.
* Very large items that consume many RCUs/WCUs per operation.

Mitigations:

* Re-design partition keys to distribute traffic (increase cardinality or add sharding/suffixes).
* Implement exponential backoff and retries on throttled requests.
* For read-heavy workloads, consider DynamoDB Accelerator (DAX) to reduce RCU consumption — DAX provides cached, eventually consistent reads only and does not reduce WCUs.

> **warning** If you’re being throttled, don’t retry aggressively. Use exponential backoff with jitter and monitor throttled request metrics to identify hot keys or insufficient capacity.

<Frame>
  <img alt="A presentation slide titled &#x22;Throttling&#x22; showing the error &#x22;ProvisionedThroughputExceededException.&#x22; It lists causes (e.g., exceeding provisioned RCU/WCU, hot/insufficient partition keys, large items) on the left and solutions (distribute partition keys, exponential backoff, use DAX) on the right." />
</Frame>

## Summary and best practices

* Choose provisioned mode when you can predict throughput and want lower per-request cost; choose on-demand for highly variable or unpredictable traffic.
* WCUs are measured per 1 KB (round up); RCUs are measured per 4 KB (round up).
* Eventually consistent reads use half the RCUs of strongly consistent reads for the same item size (one RCU → two eventual reads/sec for ≤4 KB).
* Avoid hot partitions by increasing partition key cardinality or adding traffic-distributing patterns (hash suffix, composite keys).
* Implement exponential backoff and jitter for retries; monitor throttling and CloudWatch metrics (ConsumedReadCapacityUnits, ConsumedWriteCapacityUnits, ThrottledRequests).
* Consider DAX for read-heavy workloads to lower RCU usage — but remember DAX offers eventually consistent cached reads and does not reduce write costs.

## Links and references

* [Amazon DynamoDB Pricing](https://aws.amazon.com/dynamodb/pricing/)
* [DynamoDB Developer Guide — Read/Write Capacity Modes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html)
* [DynamoDB Best Practices for Designing and Architecting](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/001734a9-f7c2-4943-83a3-d64621fedfd2/lesson/0c798276-cbd7-4429-a66e-24fcc89d1257)
