# Understanding Bigtable

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Database-SQL-NoSQL-and-memory/Understanding-Bigtable/page

Overview of Google Cloud Bigtable, a highly scalable wide-column NoSQL database optimized for low-latency, petabyte-scale time-series and high-throughput workloads, not suited for multi-row transactional relational use.

Welcome back.

In this lesson we continue our discussion of semi-structured data options in GCP and focus on one of Google Cloud's most powerful NoSQL databases: Google Cloud Bigtable.

## What is Bigtable?

Bigtable is Google’s wide-column NoSQL database designed for very large-scale analytical and operational workloads. Originally developed to power Google services (Search, Apps, etc.), Bigtable is optimized for low-latency access and massive throughput at petabyte scale. Use Bigtable when you need fast reads/writes over very large datasets, especially time-series patterns.

## Key characteristics

* Time-series friendly\
  Bigtable is an excellent fit for time-series data such as IoT sensor readings, financial market ticks, and performance telemetry. It stores and serves large volumes of time-ordered data with efficient range scans and millisecond reads.

* Not intended for full transactional/RDBMS workloads\
  Bigtable does not offer multi-row ACID transactions, complex joins, or relational schema features. It does support atomic operations at the single-row level.

  <Callout icon="warning">
    Do not use Bigtable where frequent multi-row transactions, referential integrity, or complex relational queries are required. For transactional relational workloads consider Cloud Spanner or a managed relational database.
  </Callout>

* Wide-column storage model\
  Data is organized into rows with flexible columns grouped into column families. Column families let you group related columns and tune storage/performance settings at the family level. Proper design of row keys and column families is essential for performance.

* Massive horizontal scalability\
  Bigtable can store petabytes of data and handle millions of reads/writes per second. Capacity grows horizontally: add nodes to increase throughput and storage.

<Callout icon="lightbulb">
  Exam tip: If a question mentions petabyte-scale data with low-latency access for analytical or operational processing, Bigtable is a likely answer.
</Callout>

* Low latency\
  Bigtable is built for millisecond response times, making it suitable for real-time dashboards, anomaly detection, and live monitoring.

* High availability and durability\
  Bigtable can replicate data across zones and across clusters to provide durability and fault tolerance so your application can remain available even if a zone fails.

To summarize, Bigtable is a highly scalable wide-column NoSQL database optimized for fast analytical and operational workloads, especially time-series patterns. It excels at massive, low-latency read/write workloads but is not a substitute for a transactional relational database.

<Frame>
  <img alt="A presentation slide titled &#x22;BigTable: Key Features – Wide-Column NoSQL Database&#x22; showing six feature boxes (BigTable for Time-Series Data, Not for Transactional DB, Wide-Column Store, Massive Scalability, Low Latency, High Availability) each with a short description." />
</Frame>

## Quick comparison: when to choose Bigtable

| Use case                                      |                                                           Why Bigtable fits | Alternatives                                                          |
| --------------------------------------------- | --------------------------------------------------------------------------: | --------------------------------------------------------------------- |
| Time-series telemetry, monitoring, metrics    | Efficient range scans, optimized for ordered row keys and high ingest rates | `BigQuery` for analytics, `Cloud Spanner` for relational transactions |
| High-throughput key-value workloads           |                                   Low-latency reads/writes at massive scale | `Cloud Bigtable` vs `Firestore` (Firestore offers richer querying)    |
| Large-scale analytical processing (streaming) |                                    Horizontal scaling and low-latency scans | `BigQuery` for ad-hoc analytics and SQL-based analysis                |

## Design notes & best practices

* Row key design matters: design keys to avoid hotspots (use time bucketing, hashed prefixes, or reverse timestamps when appropriate).
* Use column families to group related columns and apply storage settings.
* Use single-row atomic mutations for safe updates; avoid patterns that require multi-row transactions.
* Monitor node utilization and scale horizontally by adding/removing nodes to match throughput.

## Links and references

* [Cloud Bigtable documentation](https://cloud.google.com/bigtable/docs)
* [Cloud Spanner (for distributed transactions)](https://cloud.google.com/spanner)
* [BigQuery (for large-scale analytics)](https://cloud.google.com/bigquery)
* [Firestore (document DB on GCP)](https://cloud.google.com/firestore)

Further material covers how Bigtable stores data and examines the Bigtable data model and column families.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/8113b673-3c60-4b57-ae81-fd9533eba836/lesson/e3bfb5af-985c-49b0-84b4-3a465ad33e2e" />
</CardGroup>
