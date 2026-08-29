# imports and basic configuration
import os
import shutil
from datetime import datetime
import pandas as pd

# Define folders and paths
data_folder = "data"
archive_folder = os.path.join(data_folder, "archive")
insights_folder = "insights"
logs_folder = "logs"
log_path = os.path.join(logs_folder, "ingest_log.csv")

# Create folders if they don't exist
for folder in [data_folder, archive_folder, insights_folder, logs_folder]:
    os.makedirs(folder, exist_ok=True)

print("✅ Folder structure and paths set up.")
```

## 2) Locate the orders file

This example looks for any filename in `data/` containing the substring `orders`.

```python theme={null}
# Find the file
files = os.listdir(data_folder)
file_name = next((f for f in files if "orders" in f), None)

if not file_name:
    print("🚨 No orders file found.")
else:
    file_path = os.path.join(data_folder, file_name)
    file_id = os.path.splitext(file_name)[0]
    print(f"📥 Found file: {file_name}")
```

## 3) Idempotency check — consult the ingest log

Before proceeding, confirm the file hasn't been processed already by checking `logs/ingest_log.csv`.

```python theme={null}
# Check log for duplicates (idempotency)
if file_name and os.path.exists(log_path):
    log_df = pd.read_csv(log_path)
    if file_name in log_df["file_name"].values:
        print(f"🛑 File '{file_name}' already ingested - exiting.")
        already_ingested = True
    else:
        print("✅ File not ingested before - proceed to next step.")
        already_ingested = False
else:
    already_ingested = False
```

## 4) Load and validate schema

This pipeline requires a specific column order to detect accidental format changes early.

```python theme={null}
if file_name and not already_ingested:
    # Load orders file
    orders = pd.read_csv(file_path)

    # Expected schema (column order matters here)
    expected_cols = ['order_id', 'customer_id', 'product_id', 'quantity', 'order_date']
    actual_cols = list(orders.columns)

    schema_ok = expected_cols == actual_cols

    if not schema_ok:
        print("❌ Schema validation failed.")
        if set(expected_cols) != set(actual_cols):
            print(f"⚠️ Columns mismatch.\n Expected: {expected_cols}\n Found: {actual_cols}")
        else:
            print("⚠️ Columns present but in the wrong order.")
        status = "Schema Failed"
        row_count = 0
    else:
        print("✅ Schema validation passed.")
        status = "Success"
        row_count = len(orders)
```

## 5) Partition, save, archive, and log

If the schema validation passes, save a processed copy partitioned by month, move the raw file to `archive/`, and append an entry to the ingest log for observability.

```python theme={null}
if file_name and not already_ingested and schema_ok:
    # Build month partition from first order_date value
    order_date = pd.to_datetime(orders["order_date"].iloc[0])
    month_folder = f"{order_date.year}_{order_date.month:02}"
    output_folder = os.path.join(insights_folder, month_folder)
    os.makedirs(output_folder, exist_ok=True)

    # Save processed copy
    output_path = os.path.join(output_folder, "orders.csv")
    orders.to_csv(output_path, index=False)
    print(f"✔ Saved orders data to: {output_path}")

    # Archive raw data
    shutil.move(file_path, os.path.join(archive_folder, file_name))
    print(f"✔ Moved raw file to archive/{file_name}")

    # Log the outcome
    log_entry = pd.DataFrame([{
        "file_name": file_name,
        "status": status,
        "rows": row_count,
        "timestamp": datetime.now().replace(microsecond=0).isoformat()
    }])

    if os.path.exists(log_path):
        log_df = pd.read_csv(log_path)
        log_df = pd.concat([log_df, log_entry], ignore_index=True)
    else:
        log_df = log_entry

    os.makedirs(logs_folder, exist_ok=True)
    log_df.to_csv(log_path, index=False)
    print(f"✔ Logged ingestion to {log_path}")
```

There it is. After a successful run:

* `insights/` contains the processed file partitioned by month (e.g., `insights/2023_07/orders.csv`).
* `archive/` contains the original raw file.
* `logs/ingest_log.csv` records `file_name`, `status`, `rows`, and `timestamp`.

<Frame>
  <img alt="The image shows a person standing in front of a computer screen displaying a file explorer and a CSV file. The person is wearing a black shirt with a &#x22;KodeKloud&#x22; logo." />
</Frame>

## Try a schema failure simulation

To demonstrate the schema checks, temporarily remove `customer_id` from `expected_cols` and rerun the schema-check section. The pipeline will report what's missing and prevent ingestion — giving you a chance to fix the source file before the data is promoted.

<Callout icon="warning">
  Altering `expected_cols` simulates schema drift. In a production pipeline, implement more granular validation (types, null checks, referential integrity) and automated alerts rather than manual schema edits.
</Callout>

## Why this pattern works

This simple ingestion pipeline enforces three core guarantees:

* Idempotency: the ingest log prevents duplicate ingestion runs.
* Schema awareness: explicit column checks catch accidental format drift early.
* Observability: each run is recorded with status, row count, and timestamp.

Schema validation here is column-level. For production-grade ingestion, add:

* Row-level checks (nulls, data types).
* Referential checks against `customers` and `products`.
* Duplicate detection and deduplication strategies.
* Error handling and retry logic.
* Metrics export to monitoring systems.

## Quick reference table

|           Concern | Implementation in this demo                  | Extend for production                                       |
| ----------------: | -------------------------------------------- | ----------------------------------------------------------- |
|       Idempotency | `logs/ingest_log.csv` checks for `file_name` | Use unique file IDs, checkpoints, or commit logs            |
| Schema validation | Exact column order check (`expected_cols`)   | Schema registry, Avro/Parquet schemas, type checks          |
|      Partitioning | `insights/YYYY_MM/orders.csv`                | Partition by date and other dimensions for query efficiency |
|     Observability | Log entry with status, rows, timestamp       | Metrics, alerts, structured logs and tracing                |

## Links and references

* [Pandas documentation](https://pandas.pydata.org/)
* [Jupyter Project](https://jupyter.org/)
* For production ingestion patterns and best practices, consult blog posts and docs on data pipelines, schema registries, and observability tooling.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/data-engineering-fundamentals/module/0340c50b-2dcb-4cd0-86c5-6570c8c4382e/lesson/5bfb150d-9573-45ca-b523-a16c8fb94ded" />
</CardGroup>


# Ingesting Data

Source: https://notes.kodekloud.com/docs/Data-Engineering-Fundamentals/Ingesting-Data/Ingesting-Data/page

Guide to data ingestion for analytics covering batch versus stream, idempotency, schema validation, observability, and a practical Jupyter Pandas demo.

Let's say you've just joined a small coffee startup as a trainee data engineer.

Roastflow sells beans online — multiple roasts, grind types, and bundles — through a Shopify store. They run paid ads on Instagram and TikTok, but no one is reliably tracking which campaigns actually drive purchases.

It's late summer, and leadership has given you until the end of the year to build a data pipeline that provides reliable monthly sales insight. Before you can answer those business questions, you need to bring data together cleanly, consistently, and without duplication — and that all starts with ingestion.

<Frame>
  <img alt="The image includes a diagram illustrating a data pipeline process with various elements like calendar months, monthly sales graph, and a section labeled &#x22;Clean.&#x22; A person is also present, gesturing as if explaining the concept." />
</Frame>

Ingestion is the first step in a data pipeline: capture, validate, and land raw data so downstream analytics can run reliably.

By the end of this lesson you will be able to:

* Differentiate between batch and streaming data ingestion.
* Describe the three core principles of robust ingestion: idempotency, schema-awareness, and observability.
* Ingest and clean order data using Jupyter, Python, Pandas, and Matplotlib.

<Frame>
  <img alt="The image shows a person wearing a &#x22;KodeKloud&#x22; shirt next to a presentation that includes a cartoon cat and text about differentiating between batch and streaming data ingestion." />
</Frame>

First, distinguish how data is generated from how it is processed. Generation and processing are independent choices.

At Roastflow, some sources are bursty: monthly order exports from Shopify, or ad-spend spreadsheets dropped in Google Drive by marketing. Other sources are continuous: website clicks, pageviews, and real‑time events.

<Frame>
  <img alt="The image illustrates various data metrics such as monthly orders, ad spend, and website clicks associated with a coffee shop graphic. A person is standing to the right wearing a KodeKloud shirt." />
</Frame>

Even when generation is continuous, we can choose a processing strategy: collect and process in batches or process events as they arrive.

<Frame>
  <img alt="The image features a person wearing a &#x22;KodeKloud&#x22; T-shirt alongside illustrations labeled &#x22;Monthly Orders,&#x22; &#x22;Ad Spend,&#x22; &#x22;Website Click,&#x22; and &#x22;Pageviews,&#x22; depicting various digital marketing and online activities." />
</Frame>

Two primary ingestion approaches:

* Batch processing — accumulate data and process it in scheduled chunks (hourly, daily, weekly).
* Stream processing — process individual events continuously, or in very small micro-batches.

Batch is often simpler and reliable for routine analytics (e.g., daily sales reports). Streaming suits near real-time needs (live dashboards, user tracking), but is typically more complex to build and operate.

<Frame>
  <img alt="The image features a person speaking in front of graphics illustrating concepts of streaming data processing, message queues, and data lakes. A series of dots and a logo for KodeKloud are also visible." />
</Frame>

In production, many "real-time" pipelines still use batching for efficiency — for example, accumulating events for one-minute micro-batches. Understanding the difference between how data is generated (burst vs continuous) and how it's processed (batch vs stream) is key to designing the right pipeline for Roastflow.

Analogy: batch = reservoir released on a schedule; stream = water flowing through a turbine and processed immediately. Streaming provides immediate insights but increases operational complexity; batch is easier to manage and scales well for reporting.

<Frame>
  <img alt="The image contrasts batch and streaming data processing, highlighting features like reliability versus instant updates, and routine analytics versus management difficulty. A person wearing a &#x22;KodeKloud&#x22; shirt is gesturing in front of the comparison." />
</Frame>

As a data engineer you'll work with both approaches depending on the use case.

Core properties of a robust ingestion step
A dependable ingestion process should meet three requirements:

1. Idempotent — safe to run multiple times without producing duplicates.
2. Schema-aware — validates the structure and basic quality of data.
3. Observable — logs enough metadata to trace, debug, and replay.

Let's unpack each.

Idempotency
Idempotency ensures repeating the same ingestion with the same input does not change the final state. Practically this means:

* No unintended duplicates.
* Existing records are not corrupted by repeated runs.
* Safe replays and retries without manual cleanup.

<Callout icon="warning">
  Idempotency is critical for reliable pipelines. Without it, retries (common after failures) can introduce duplicate revenue or user records, skewing analytics and costing money.
</Callout>

Schemas
A schema defines expectations about data shape and basic quality checks. Apply validations at multiple levels:

| Schema Level | Typical Checks                                                            |
| ------------ | ------------------------------------------------------------------------- |
| Column-level | Are expected columns present? Types correct? Required fields non-null?    |
| Row-level    | Business rules per row (quantities >= 0, timestamps valid, email formats) |
| Table-level  | Primary key uniqueness, foreign key consistency across tables             |

<Frame>
  <img alt="The image shows a presentation slide on database schemas with levels (Column, Row, Table) and related questions, alongside a person wearing a KodeKloud shirt." />
</Frame>

You can extend these checks with cross-table constraints and domain-specific rules, but column/row/table checks are the backbone of schema-aware ingestion.

<Frame>
  <img alt="The image features a section labeled &#x22;02 Schemas&#x22; with categories such as Column Level, Row Level, Table Level, Cross-Table Relationships, and Business-Specific Rules on the left, and a person standing on the right wearing a KodeKloud shirt." />
</Frame>

Observability
Observability means recording metadata about each ingestion action: file names, timestamps, row counts, success/failure status, and error details. Good logs let you audit, investigate, and replay data when necessary.

<Frame>
  <img alt="The image features a presentation slide on 'Observability' with a list related to files or processes, and a person standing to the right wearing a KodeKloud t-shirt." />
</Frame>

Quiz — quick comprehension check

Which two statements are true?

A. Batch data is ingested continuously as soon as it's generated.\
B. Streaming data is ideal for real-time user tracking or live dashboards.\
C. A good ingestion step should be schema-aware, observable, and idempotent.\
D. Idempotency means applying the same operation multiple times produces the same result before storing the data.

Correct answers: B and C.

* B is true: streaming supports real-time use cases like live dashboards.
* C is true: ingestion should avoid duplicates, validate structure, and log sufficiently.
* A is false: continuous ingestion describes streaming, not batch.
* D is misleading: idempotency ensures the same final state after repeated runs, not a description of pre-storage transformation.

Quick recap

* Batch: process data in scheduled chunks (e.g., monthly exports, uploaded spreadsheets).
* Stream: process data continuously (e.g., real-time click tracking).
* Batch is often simpler and reliable for routine analytics; streaming gives immediate insights but adds complexity.
* Ingestion must be idempotent, schema-aware, and observable.

<Frame>
  <img alt="The image describes the differences between batch processing and stream processing, with a person standing next to the text boxes on a black background." />
</Frame>

<Frame>
  <img alt="The image features a person wearing a TekKloud t-shirt and two informational cards about ingestion, focusing on idempotency and schema-awareness. There is also an illustration of a person working on a laptop." />
</Frame>

Practical demo: Jupyter + Pandas ingestion pattern
You'll build a simple but realistic ingestion in Jupyter to illustrate the concepts without being tied to specific cloud services. The micro-pipeline will:

* Read messy order CSV exports.
* Validate columns and basic row rules.
* Deduplicate (idempotent behavior) based on a unique key.
* Log ingestion metadata for observability.
* Produce a cleaned dataset ready for analytics (e.g., top products by revenue).

Example Pandas pattern (conceptual):

```python theme={null}
import pandas as pd
from pathlib import Path
import json
import hashlib
from datetime import datetime

def ingest_file(path, existing_keys=set()):
    df = pd.read_csv(path)
    # Column-level check
    required_columns = {"order_id", "product_id", "quantity", "price", "order_ts"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Row-level check
    df = df[df["quantity"] >= 0]
    df = df.dropna(subset=["order_id", "product_id", "order_ts"])

    # Idempotent dedupe: keep rows not already seen
    df["unique_key"] = df["order_id"].astype(str) + "-" + df["product_id"].astype(str)
    df = df[~df["unique_key"].isin(existing_keys)]

    # Observability: write a small log for this ingestion
    log = {
        "file": str(path),
        "timestamp": datetime.utcnow().isoformat(),
        "rows_in": int(df.shape[0]),
        "rows_out": int(df.shape[0]),
        "status": "success"
    }
    Path("ingest_logs").mkdir(exist_ok=True)
    with open(Path("ingest_logs") / f"{Path(path).stem}.json", "w") as f:
        json.dump(log, f)

    return df
```

This pattern:

* Validates schema basics before transforming.
* Filters invalid rows.
* Removes duplicates using a stable, unique key (idempotency).
* Emits a minimal log for observability.

<Callout icon="lightbulb">
  Use a stable unique key (e.g., `order_id + product_id`) for deduplication. In production, consider deterministic hashing and persistent storage of seen keys (or de-duplication via database constraints) for stronger guarantees.
</Callout>

Next steps and references

* Start by cataloging your sources (Shopify exports, ad-spend sheets, website events) and classify each as batch or stream.
* Design ingestion jobs with idempotency in mind: deterministic keys, safe upserts, or dedupe strategies.
* Implement schema checks early and fail fast on critical errors so dirty data doesn't propagate.
* Capture minimal but consistent ingestion logs for every run to enable replay and debugging.

Further reading:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (infrastructure reference)
* [Pandas documentation](https://pandas.pydata.org/docs/)
* [Designing Data-Intensive Applications](https://dataintensive.net/) (conceptual systems design)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/data-engineering-fundamentals/module/0340c50b-2dcb-4cd0-86c5-6570c8c4382e/lesson/a32356eb-4fce-499a-9e19-a1ecbaa6415b" />
</CardGroup>
