# Demo Hands on with Dataproc

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Processing/Demo-Hands-on-with-Dataproc/page

Hands-on demo showing how to run a PySpark job on Google Cloud Dataproc to aggregate CSV orders from Cloud Storage and write results back to Cloud Storage

Welcome — in this hands-on demo you'll learn how to run a simple PySpark job on Google Cloud Dataproc that reads data from Cloud Storage, aggregates it, and writes results back to Cloud Storage. Dataproc is a fully managed, scalable service for running Apache Spark, Apache Hadoop, and related open-source data-engineering tools.

What you'll do

* Create a Cloud Storage bucket and upload input data plus a PySpark script.
* Create a Dataproc cluster (single-node or multi-node).
* Submit a PySpark job to the cluster that reads from Cloud Storage, aggregates totals per customer, and writes results back to Cloud Storage.
* Inspect the job using the Dataproc Console and Spark History Server, then verify output in Cloud Storage.

Prerequisites

* A GCP project with billing enabled.
* Permissions to create Storage buckets and Dataproc clusters (roles like Storage Admin and Dataproc Editor are helpful).
* Cloud SDK (`gcloud`) installed if you plan to submit jobs from the CLI.

## Create a Cloud Storage bucket

Open the GCP Console, search for “Storage”, and create a new bucket. Choose a globally unique name and a region (this demo uses `us-central1`). Configure the storage class and other options as needed, then create the bucket.

<Frame>
  <img alt="A screenshot of the Google Cloud Console &#x22;Create a bucket&#x22; page showing the selected location (us-central1 — Iowa), storage-class choices (Standard, Nearline, Coldline, Archive) and an estimated price ($0.020 per GB‑month). The UI also shows options for Autoclass or setting a default storage class." />
</Frame>

## Prepare the input data

Create a small CSV file named `orders.csv` with order data. Example contents:

```csv theme={null}
order_id,customer_id,amount
101,1,500.00
102,2,150.50
103,1,300.00
104,3,1200.00
105,2,50.00
```

Upload `orders.csv` to the bucket you created (e.g., `gs://<your-bucket>/orders.csv`).

## PySpark job (process\_orders.py)

Create a PySpark script `process_orders.py`. The script below reads a CSV from Cloud Storage, aggregates total spend per customer, and writes the result back to Cloud Storage as CSV.

```python theme={null}
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as _sum

if len(sys.argv) != 3:
    print("Usage: process_orders.py <input_gcs_path> <output_gcs_path>")
    sys.exit(-1)

input_path = sys.argv[1]
output_path = sys.argv[2]

spark = SparkSession.builder.appName("OrderAggregation").getOrCreate()
