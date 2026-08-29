# python
import os
import pandas as pd
import shutil
from datetime import datetime

# Define folders and paths
data_folder = "data"
archive_folder = os.path.join(data_folder, "archive")
insights_folder = "insights"
logs_folder = "logs"
log_path = os.path.join(logs_folder, "ingest_log.csv")

# Create folders if they don't exist
for folder in [data_folder, archive_folder, insights_folder, logs_folder]:
    os.makedirs(folder, exist_ok=True)

print("✓ Folder structure and paths set up.")

# Find the orders file in data_folder (any filename containing 'orders')
files = os.listdir(data_folder)
file_name = next((f for f in files if "orders" in f and f.lower().endswith(".csv")), None)

if not file_name:
    raise FileNotFoundError("No orders file found in the data folder.")
else:
    file_path = os.path.join(data_folder, file_name)
    file_id = os.path.splitext(file_name)[0]
    print(f"✅ Found file: {file_name}")

# Load existing ingest log if it exists
if os.path.exists(log_path):
    log = pd.read_csv(log_path)
else:
    log = pd.DataFrame()
```

## Pipeline policy: drop-and-log

For this lesson the pipeline policy is to drop rows that fail validation and log them. Dropping is acceptable when only a small fraction of rows are bad and when you retain the dropped rows for later review or repair.

> **warning** Dropping rows can bias downstream analytics if many rows are removed. Always log discarded rows and their reasons so the data owner can correct the source or you can implement targeted fixes later.

## Load the datasets and save a raw copy

```python theme={null}
# python
# Load data from the located file and lookup tables
orders_path = file_path  # the file we found above
products_path = os.path.join("data", "products.csv")
customers_path = os.path.join("data", "customers.csv")

orders = pd.read_csv(orders_path)
products = pd.read_csv(products_path)
customers = pd.read_csv(customers_path)

# Keep a raw copy for logging or later re-ingestion
orders_raw = orders.copy()
```

## Row-level checks — what to validate

Below is a concise summary of common checks and the typical remediation action.

| Check                             |                                                                               What to look for | Typical action                                                     |
| --------------------------------- | ---------------------------------------------------------------------------------------------: | ------------------------------------------------------------------ |
| Required columns / missing values | Missing required fields like `order_id`, `customer_id`, `product_id`, `quantity`, `order_date` | Drop rows missing required fields; log dropped rows                |
| Dates                             |                                              Invalid formats, time-only values, parse failures | Use `pd.to_datetime(..., errors='coerce')`, drop rows with `NaT`   |
| Numeric fields                    |                                        Non-numeric values, negative quantities, fractional IDs | Coerce to numeric, drop invalids, cast to integer after validation |
| Duplicates                        |                                                 Exact duplicate rows (or duplicate `order_id`) | Drop duplicates and keep the first occurrence                      |
| Foreign keys                      |                                       `customer_id` or `product_id` not found in lookup tables | Drop rows with invalid foreign keys—or flag them for manual review |

### 1) Missing required columns / missing values

Decide which columns are mandatory. If a required column is missing from the file entirely, you should either raise an error or log and skip processing (depending on your pipeline policy). Here we assume the columns exist and drop rows with nulls in required fields.

```python theme={null}
# python
required_columns = ["order_id", "customer_id", "product_id", "quantity", "order_date"]

# Validate required columns exist
missing_columns = [c for c in required_columns if c not in orders.columns]
if missing_columns:
    raise KeyError(f"Missing required columns: {missing_columns}")

# Identify rows with missing required fields
missing_mask = orders[required_columns].isnull().any(axis=1)
dropped_missing_ids = orders.loc[missing_mask, "order_id"].tolist()

if dropped_missing_ids:
    print(f"🗑️ Removed {len(dropped_missing_ids)} rows with missing required fields: {dropped_missing_ids}")

# Drop them
orders = orders[~missing_mask]
```

### 2) Invalid dates

Use pandas to parse dates. `errors='coerce'` converts unparsable values to `NaT`, which you can then drop. If you require strict formats, pass a `format=` argument.

<Frame>
  <img alt="The image shows a person standing next to a screenshot of a Jupyter Notebook interface with Python code aimed at cleaning data through row-level and table-level checks. The code involves dropping rows with missing data and invalid entries." />
</Frame>

```python theme={null}
# python
# Convert order_date to datetime, invalid parsing will be NaT
orders["order_date_parsed"] = pd.to_datetime(orders["order_date"], errors="coerce")
invalid_dates_mask = orders["order_date_parsed"].isna()
dropped_date_ids = orders.loc[invalid_dates_mask, "order_id"].tolist()

if dropped_date_ids:
    print(f"🗑️ Removed {len(dropped_date_ids)} rows with invalid order_date: {dropped_date_ids}")

orders = orders[~invalid_dates_mask]
```

Tip: to avoid accepting time-only strings like `"10:45"`, either validate the parsed timestamp's date components (year/month/day) or use a strict `format` parameter. See pandas docs: [https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to\_datetime.html](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html)

### 3) Numeric fields: customer\_id, product\_id, quantity

Coerce numeric fields and drop rows that fail numeric validation. For `quantity`, enforce strictly positive values (> 0). For IDs, require non-negative integers. Use temporary checked columns during validation and remove them afterwards.

```python theme={null}
# python
numeric_fields = ["customer_id", "product_id", "quantity"]
invalid_numeric_mask = pd.Series(False, index=orders.index)

for field in numeric_fields:
    # Coerce to numeric; invalid parsing becomes NaN
    orders[f"{field}_checked"] = pd.to_numeric(orders[field], errors="coerce")

    # Invalid if NaN or negative (for quantity require > 0; for IDs require >= 0)
    if field == "quantity":
        invalids = orders[f"{field}_checked"].isna() | (orders[f"{field}_checked"] <= 0)
    else:
        invalids = orders[f"{field}_checked"].isna() | (orders[f"{field}_checked"] < 0)

    if invalids.any():
        dropped = orders.loc[invalids, "order_id"].tolist()
        print(f"🗑️ Removed {len(dropped)} rows with invalid {field}: {dropped}")
        invalid_numeric_mask |= invalids

# Drop all rows that failed any numeric checks
orders = orders[~invalid_numeric_mask]

# Convert checked numeric columns to integers (safe now)
orders["customer_id"] = orders["customer_id_checked"].astype(int)
orders["product_id"] = orders["product_id_checked"].astype(int)
orders["quantity"] = orders["quantity_checked"].astype(int)

# Drop helper checked columns
orders.drop(columns=[f"{field}_checked" for field in numeric_fields], inplace=True)
```

Note: If you must disallow fractional IDs, check that the checked numeric values equal their integer cast before accepting them; `astype(int)` will silently truncate floats.

### 4) Duplicates

Remove exact duplicate rows (or duplicates by `order_id` if that’s your unique key). Make sure any helper columns that could affect duplicate detection are dropped before running this check.

```python theme={null}
# python
duplicates_mask = orders.duplicated(keep="first")
duplicate_ids = orders.loc[duplicates_mask, "order_id"].tolist()

if duplicate_ids:
    print(f"🗑️ Removed {len(duplicate_ids)} duplicate rows: {duplicate_ids}")

orders = orders[~duplicates_mask]
```

## Table-level checks — foreign keys

Verify that `customer_id` and `product_id` exist in their respective lookup tables. Make sure lookup key dtypes match (both int or both string) to avoid false negatives.

```python theme={null}
# python
# Customers
valid_customer_ids = set(customers["customer_id"])
invalid_customer_mask = ~orders["customer_id"].isin(valid_customer_ids)
dropped_customer_ids = orders.loc[invalid_customer_mask, "order_id"].tolist()

if dropped_customer_ids:
    print(f"❌ Removed {len(dropped_customer_ids)} rows with invalid customer_id: {dropped_customer_ids}")

orders = orders[~invalid_customer_mask]

# Products
valid_product_ids = set(products["product_id"])
invalid_product_mask = ~orders["product_id"].isin(valid_product_ids)
dropped_product_ids = orders.loc[invalid_product_mask, "order_id"].tolist()

if dropped_product_ids:
    print(f"❌ Removed {len(dropped_product_ids)} rows with invalid product_id: {dropped_product_ids}")

orders = orders[~invalid_product_mask]
```

## Cross-checks and saving dropped rows for audit

Compare the raw copy to the cleaned dataframe to extract and save exactly what was removed during cleaning. This creates an auditable CSV that the data owner can inspect and use to fix source issues.

```python theme={null}
# python
dropped_order_ids = set(orders_raw["order_id"].tolist()) - set(orders["order_id"].tolist())
if dropped_order_ids:
    dropped_rows = orders_raw[orders_raw["order_id"].isin(dropped_order_ids)]
    dropped_path = os.path.join(insights_folder, "ordersDropped.csv")
    dropped_rows.to_csv(dropped_path, index=False)
    print(f"Saved dropped rows ({len(dropped_rows)}) to {dropped_path}")
else:
    print("No rows were dropped during cleaning.")
```

## Final tidy-up, save cleaned data, archive raw file, update log

Remove any temporary helper columns, reset the index, save the cleaned file to `insights/`, archive the original raw file, and append an entry to the ingest log.

```python theme={null}
# python
# Remove helper columns and reset index
if "order_date_parsed" in orders.columns:
    orders.drop(columns=["order_date_parsed"], inplace=True)

orders = orders.reset_index(drop=True)

# Save cleaned orders
cleaned_path = os.path.join(insights_folder, f"{file_id}_cleaned.csv")
orders.to_csv(cleaned_path, index=False)
print(f"Saved cleaned data to {cleaned_path}")

# Archive the raw source file
os.makedirs(archive_folder, exist_ok=True)
shutil.move(file_path, os.path.join(archive_folder, file_name))
print(f"Moved raw file to {archive_folder}/{file_name}")

# Update ingest log
status = "cleaned"
row_count = len(orders)
log_entry = pd.DataFrame([{
    "file_name": file_name,
    "status": status,
    "rows": row_count,
    "timestamp": datetime.now().replace(microsecond=0).isoformat()
}])

if os.path.exists(log_path):
    log = pd.read_csv(log_path)
    log = pd.concat([log, log_entry], ignore_index=True)
else:
    log = log_entry

os.makedirs(logs_folder, exist_ok=True)
log.to_csv(log_path, index=False)
print(f"Logged ingestion to {log_path}")
```

## Example observations (illustrative)

* Missing data: rows with IDs 1035 and 1050 were dropped.
* Invalid dates: entries like "10:45" (time-only) were dropped.
* Invalid numbers: negative quantity or fractional IDs were removed.
* Duplicate rows: order ID 1072 appeared twice; one duplicate was removed.
* Missing foreign keys: orders referencing `customer_id = 999` or `product_id = 999` were dropped because those IDs don't exist in the lookup tables.

<Frame>
  <img alt="The image shows a person standing in front of a virtual background displaying a spreadsheet with order details, including columns for order ID, customer ID, product ID, quantity, and order date." />
</Frame>

When you open the cleaned file you should see the dirty rows removed. The cleaned dataset is now ready for the next step in your pipeline: enrichment, aggregation, and analytics.

## Recap — three levels of validation

Dirty data comes in many shapes: missing values, invalid formats (dates), negative or non-integer numbers, duplicates, or mismatched foreign keys. Apply validation at these three levels:

* Column-level: Are required columns present, and are their dtypes sensible?
* Row-level: Are the values in each row complete and valid?
* Table-level: Do foreign keys match values in lookup tables?

<Frame>
  <img alt="The image shows a man standing beside text boxes listing different forms of dirty data and levels of data validation. The text includes points on missing values, invalid formats, and validation at column, row, and table levels." />
</Frame>

Cleaning often means dropping bad rows, but always log what you discard so errors can be traced back and fixed.

<Frame>
  <img alt="The image shows a person speaking, with the text &#x22;Cleaning can mean dropping bad rows, but always log what you discard for transparency or fixing.&#x22; The KodeKloud logo is on the person's shirt." />
</Frame>

## Next steps and practice

Apply these techniques on sample files and iterate on rules that reflect your business requirements. Consider the following improvements over time:

* Soft-fail: flag and route suspicious rows for manual review instead of immediate deletion.
* Auto-repair: implement deterministic fixes (e.g., common date format corrections) with confidence scoring.
* Schema enforcement: use tools like Great Expectations, Apache Deequ, or declarative schemas to codify checks.
* Monitoring: track dropped-row counts over time to detect upstream regressions.

Links and references

* pandas to\_datetime: [https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to\_datetime.html](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html)
* pandas read\_csv / to\_csv: [https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read\_csv.html](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html)
* Great Expectations: [https://greatexpectations.io/](https://greatexpectations.io/)

Practice these techniques with a hands-on exercise to build a robust, auditable cleaning step in your ETL pipeline.

- [Watch Video](https://learn.kodekloud.com/user/courses/data-engineering-fundamentals/module/f17697f1-d2a6-4c31-ab29-55e51617dace/lesson/6085352b-f1be-456b-9438-66b6f7519242)


# Transforming Data Combining

Source: https://notes.kodekloud.com/docs/Data-Engineering-Fundamentals/Transforming-Data-Combining/Transforming-Data-Combining/page

Guide to cleaning and merging order, product, and customer tables with pandas to compute line totals and produce top product and customer revenue summaries

You've ingested and cleaned separate source files, but the business questions you need to answer require a single, enriched table. This lesson shows how to combine multiple tables, resolve column conflicts, compute derived fields, and produce summary tables for reporting and analysis using pandas.

What you'll learn:

* Rename conflicting fields to avoid ambiguity when merging datasets.
* Merge datasets (orders, products, customers) into a single, analyzable table.
* Compute derived metrics (line totals) and produce aggregation summaries (top products/customers).

<Frame>
  <img alt="The image features a man speaking next to a presentation slide with tips on managing datasets, accompanied by a cartoon wolf character." />
</Frame>

Prerequisites:

* Working in a Jupyter Notebook or similar environment.
* pandas installed: [https://pandas.pydata.org/](https://pandas.pydata.org/)
* Data files loaded or available in a `data` folder.

Scenario

* It's Oct 1 and September orders have arrived in your data folder. To answer:
  * Top 3 products by revenue — requires orders + products.
  * Top 3 customers by spend — requires orders + products + customers.
* Goal: produce a single orders table with `customer_id` and `product_id` replaced by human-readable `customer_name` and `product_name`, plus a `line_total` column computed as `quantity × price`.

High-level process

1. Locate incoming files and consult the ingest log to prevent duplicate processing.
2. Clean raw orders (drop invalid rows, fix date formats) and save the cleaned output.
3. Rename conflicting columns in reference tables (products, customers).
4. Merge product and customer reference data into cleaned orders.
5. Compute `line_total` and create aggregation summaries for reporting.

File discovery and ingest-log check

* Start by ensuring your folder structure exists and check whether the orders file was already ingested. This prevents duplicate processing and accidental reprocessing.

```python theme={null}
