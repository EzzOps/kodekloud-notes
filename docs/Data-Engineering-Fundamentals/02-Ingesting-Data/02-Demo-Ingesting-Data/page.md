# ingest.py (setup and find file)
import os
import pandas as pd
import shutil
from datetime import datetime

data_folder = "data"
archive_folder = os.path.join(data_folder, "archive")
insights_folder = "insights"
logs_folder = "logs"
log_path = os.path.join(logs_folder, "ingest_log.csv")

for folder in [data_folder, archive_folder, insights_folder, logs_folder]:
    os.makedirs(folder, exist_ok=True)

print("✅ Folder structure and paths set up.")

# Find an orders file
files = os.listdir(data_folder)
file_name = next((f for f in files if "orders" in f and f.endswith(".csv")), None)
```

Design each module as an importable function (e.g., `run`) that:

* Accepts explicit parameters (file name, folder paths, etc.)
* Returns outputs the caller needs (usually an `output_folder` path)
  This makes dependencies explicit and facilitates unit testing.

```python theme={null}
# Example signature to use in ingest.py, clean.py, transform.py
def run(file_name: str, data_folder: str, archive_folder: str, insights_folder: str, log_path: str):
    """
    Ingest stage should:
      - Read the CSV
      - Validate schema
      - Save a copy to insights/<year>/<month>/
      - Move raw file to archive/
      - Append or update the ingest log
      - Return output folder path for downstream stages
    """
    file_path = os.path.join(data_folder, file_name)
    # ... validate and process ...
    return os.path.join(insights_folder, "2025", "10")
```

A simple orchestrator script

Create `run_pipeline.py` that imports each module and calls their `run` functions in order. This file orchestrates the end-to-end flow for a single file:

```python theme={null}
# run_pipeline.py
import os
from pipeline import ingest, clean, transform

data_folder = "data"
archive_folder = os.path.join(data_folder, "archive")
insights_folder = "insights"
logs_folder = "logs"

products_path = os.path.join(data_folder, "products.csv")
customers_path = os.path.join(data_folder, "customers.csv")
log_path = os.path.join(logs_folder, "ingest_log.csv")

def run_pipeline():
    # Find a new orders file to process
    files = os.listdir(data_folder)
    file_name = next((f for f in files if "orders" in f and f.endswith(".csv")), None)

    if not file_name:
        print("No orders file found.")
        return

    print(f"📦 Starting pipeline for: {file_name}")

    try:
        output_folder = ingest.run(file_name, data_folder, archive_folder, insights_folder, log_path)
        clean.run(products_path, customers_path, output_folder)
        transform.run(products_path, customers_path, output_folder)
        print(f"✔️ Pipeline completed for: {file_name}")
    except Exception as e:
        print(f"✖️ Pipeline failed: {e}")

if __name__ == "__main__":
    run_pipeline()
```

How modules coordinate

Each module receives the specific inputs it needs and returns outputs for downstream stages. The call sequence inside `run_pipeline.py` becomes explicit and easy to follow:

```python theme={null}
# Example call sequence inside run_pipeline()
output_folder = ingest.run(file_name, data_folder, archive_folder, insights_folder, log_path)
clean.run(products_path, customers_path, output_folder)
transform.run(products_path, customers_path, output_folder)
```

This pattern makes reasoning about data flow and side effects easier and supports testing modules independently.

Idempotency and state tracking

To avoid reprocessing the same file, maintain an ingest log or state file that records processing status for each file (e.g., `ingested`, `cleaned`, `transformed`). This allows resuming a failed pipeline without duplicating work.

> **lightbulb** Use an ingest log or state-tracking file to make your pipeline idempotent: the orchestrator can check previous state and skip already-completed steps.

A simple CSV ingest log is often enough for small pipelines. Example `ingest_log.csv`:

```plaintext theme={null}
file_name,status,rows,timestamp
orders_2025_06.csv,Success,3,2025-05-24T08:00:00
orders_2025_07.csv,Success,30,2025-09-29T11:41:07
orders_2025_08.csv,Success,75,2025-09-29T11:42:36
orders_2025_09.csv,Success,50,2025-09-30T03:15:23
orders_2025_10.csv,Success,50,2025-10-27T08:47:49
```

Using this safety mechanism, the pipeline is safe to run multiple times without double-processing files.

<Frame>
  <img alt="The image shows a person standing in front of a computer screen displaying a code editor with a directory structure and a terminal window. The person is wearing a shirt with a logo and appears to be explaining or demonstrating something related to the code on-screen." />
</Frame>

Scheduling and orchestration

Right now you still manually trigger the pipeline:

```bash theme={null}
python run_pipeline.py
```

For recurring automation, you have several options depending on scale and requirements.

* Simple server scheduling: use cron on Unix-like systems.
* Cloud scheduler: use AWS EventBridge (or similar) to trigger cloud jobs.
* Full workflow orchestration: use Apache Airflow or Prefect for complex dependencies, retries, monitoring, and team collaboration.

Cron example: edit your crontab with `crontab -e` and add a line to run the script at midnight on the first of every month (replace with your interpreter and absolute path):

```bash theme={null}
0 0 1 * * /usr/bin/python3 /home/youruser/code/run_pipeline.py
```

Cron schedule fields are: minute, hour, day of month, month, day of week. For monthly runs at midnight on the first day:

```plaintext theme={null}
0 0 1 * *
```

<Frame>
  <img alt="The image shows a diagram explaining time units like seconds and minutes, and a person on the right wearing a &#x22;KodeKloud&#x22; shirt gesturing while talking." />
</Frame>

When to use an orchestrator

* Use cron or EventBridge for simple periodic tasks (backups, monthly reports).
* Use Airflow, Prefect, or other orchestrators when you need:
  * Directed acyclic graphs (DAGs) of dependent tasks
  * Retry policies and alerting
  * Visibility and centralized logs
  * Parallel task execution and resource management

<Frame>
  <img alt="The image shows a person wearing a &#x22;KodeKloud&#x22; shirt standing next to an illustration of a person typing on a laptop, with logos of Apache Airflow and Prefect, and labeled sections such as &#x22;More Steps,&#x22; &#x22;Dependencies,&#x22; and &#x22;Teams Involved.&#x22;" />
</Frame>

Running the pipeline (example)

To process October’s orders, run:

```bash theme={null}
python run_pipeline.py
```

A successful run prints step-by-step logs and outcomes:

```bash theme={null}
root@host01 ~/code via 🐍 v3.12.3 (venv) ➔ python run_pipeline.py
File not found in log - proceeding.
Starting pipeline for: orders_2025_10.csv
File not ingested before - proceed to next step.
Schema validation passed.
Saved orders data to: insights/2025_10/orders_ingested.csv
Moved raw file to archive/orders_2025_10.csv
Logged ingestion to logs/ingest_log.csv

Cleaning started...
Removed 1 rows with missing values: [1184]
Removed 2 rows with invalid quantity: [1191, 1199]
Saved 10 dropped rows to: insights/2025_10/orders_dropped.csv
Cleaned data saved to: insights/2025_10/orders_clean.csv

Top 3 Products by Revenue:
    product_name         total_revenue
0   Blue Milk Latte           103.5
1   Wookiee Cappuccino         73.5
2   Tatooine Mocha             72.0

Top 3 Customers by Spend:
    customer_name            total_spend
0   Chewbacca Kashyyyk           63.6
1   Leia Organa Alderaan         59.5
2   Darth Vader Mustafar         53.5

Pipeline completed for: orders_2025_10.csv
root@host01 ~/code via 🐍 v3.12.3 (venv) ➔
```

If the pipeline is re-run, the ingest log prevents duplication:

```bash theme={null}
root@host01 ~/code via 🐍 v3.12.3 (venv) ➔ python run_pipeline.py
File 'orders_2025_10.csv' has already been ingested - skipping.
```

Quick reference: module responsibilities

| Module         | Responsibility                                          | Example output                                            |
| -------------- | ------------------------------------------------------- | --------------------------------------------------------- |
| `ingest.py`    | Read CSV, validate, archive raw file, update ingest log | `insights/2025/10/orders_ingested.csv`                    |
| `clean.py`     | Remove/correct invalid rows, save dropped rows          | `insights/2025/10/orders_clean.csv`, `orders_dropped.csv` |
| `transform.py` | Join with `products.csv`/`customers.csv`, compute KPIs  | Top products/customers reports                            |

Recap

* Manual pipelines are fragile: they depend on human sequencing and can cause mistakes.
* Modular automation makes pipelines readable, testable, and maintainable.
* Use an ingest log or state file to make your pipeline idempotent and resumable.
* Scheduler/orchestrator choice depends on complexity: cron/EventBridge for simple schedules; Airflow/Prefect for DAGs, retries, monitoring, and team workflows.

Next: complete the hands-on exercise to refactor your single-file pipeline into modular stages and add a simple ingest log.

- [Watch Video](https://learn.kodekloud.com/user/courses/data-engineering-fundamentals/module/14818bf3-8df7-4848-a54e-732b8386e8c5/lesson/153a949c-fb3e-472d-91ba-a7bc00eadf0f)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/data-engineering-fundamentals/module/14818bf3-8df7-4848-a54e-732b8386e8c5/lesson/7b8016b2-a667-4731-b6ad-7cdd8438b29f)


# Demo Ingesting Data

Source: https://notes.kodekloud.com/docs/Data-Engineering-Fundamentals/Ingesting-Data/Demo-Ingesting-Data/page

Demo of a simple idempotent data ingestion pipeline using pandas with schema validation, monthly partitioning, file archiving, and ingest logging for observability.

Welcome back. Before we begin, make sure your notebook environment is active.

If you're following along in a Jupyter Notebook, install pandas:

```bash theme={null}
pip install pandas
```

> **lightbulb** Pandas is the go-to library for tabular data processing (CSV, Excel, etc.). Use it to read, validate, and write CSV files in ingestion pipelines. See the official docs: [https://pandas.pydata.org/](https://pandas.pydata.org/).

Scenario: It's August 1st and July's batch of orders has just arrived from the sales team, alongside two supporting files: `products` and `customers`. You drop these into a Jupyter project and build a simple, robust ingestion pipeline.

The orders file contains these fields: `order_id`, `customer_id`, `product_id`, `quantity`, and `order_date`. The `customer_id` and `product_id` keys link across files, so when RoastFlow (our example company) updates a product price, they update the `products` table once and references remain consistent.

Pipeline design principles:

* Idempotency — prevent double-ingestion.
* Schema awareness — validate the presence and expected order of columns.
* Observability — log what was ingested and when.

High-level pipeline steps:

1. Import libraries and configure paths.
2. Create project folders (`data`, `archive`, `insights`, `logs`).
3. Locate the latest orders file in the `data` folder.
4. Check the ingest log to avoid duplicates (idempotency).
5. Load and validate the schema.
6. Save a processed copy into `insights` partitioned by month.
7. Archive the raw file.
8. Append an entry to the ingest log (observability).

<Frame>
  <img alt="The image shows a person standing next to a Jupyter notebook interface on a screen, with some commented lines of code visible. The person is wearing a shirt with a &#x22;KodeKloud&#x22; logo." />
</Frame>

Below is a concise, corrected implementation of the ingestion logic that follows the steps above. Read each section to see how idempotency, schema checks, and logging are implemented.

## 1) Imports, configuration, and folder setup

```python theme={null}
