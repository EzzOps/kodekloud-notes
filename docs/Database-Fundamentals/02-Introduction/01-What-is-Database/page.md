# python
import os
import pandas as pd
from datetime import datetime

data_folder = "data"
archive_folder = os.path.join(data_folder, "archive")
insights_folder = "insights"
logs_folder = "logs"
log_path = os.path.join(logs_folder, "ingest_log.csv")

# Ensure folders exist
for folder in [data_folder, archive_folder, insights_folder, logs_folder]:
    os.makedirs(folder, exist_ok=True)
print("Folder structure and paths set up.")

# Find the orders file in the data folder
files = os.listdir(data_folder)
file_name = next((f for f in files if "orders" in f.lower()), None)

if not file_name:
    print("❌ No orders file found.")
else:
    file_path = os.path.join(data_folder, file_name)
    file_id = os.path.splitext(file_name)[0]
    print(f"✅ Found file: '{file_name}'")

    # Check ingest log for duplicates
    if os.path.exists(log_path):
        log = pd.read_csv(log_path)
        if file_name in log["file_name"].values:
            print(f"❌ File '{file_name}' already ingested - skipping.")
        else:
            print(f"File '{file_name}' not ingested before - proceed to next step.")
    else:
        print("No ingest log found — proceed to ingestion.")
```

Resolve column conflicts before merging

* When merging lookup/reference tables into fact tables, shared column names like `name` can cause overwrites or confusing duplicated columns. Rename these fields in reference tables first.

> **lightbulb** Rename columns early (e.g., `name` → `product_name` / `customer_name`) so merges produce predictable columns and you avoid accidental overwrites.

<Frame>
  <img alt="The image shows a man standing in front of a computer screen displaying a Jupyter Notebook interface with a list of CSV files and a script for data transformation tasks." />
</Frame>

Cleaning orders

* Remove rows with invalid `customer_id` or `product_id`, record dropped rows for auditing, and save the cleaned orders file. This pattern preserves traceability and keeps your downstream joins reliable.

```python theme={null}
# python
# Assumptions: orders_raw, customers, products are pre-loaded DataFrames
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Work on a copy to preserve raw data
orders = orders_raw.copy()

# Identify invalid customer_id rows
valid_customer_ids = set(customers["customer_id"].unique())
invalid_customer_mask = ~orders["customer_id"].isin(valid_customer_ids)
invalid_customer_rows = orders[invalid_customer_mask]

# Identify invalid product_id rows
valid_product_ids = set(products["product_id"].unique())
invalid_product_mask = ~orders["product_id"].isin(valid_product_ids)
invalid_product_rows = orders[invalid_product_mask]

# Combine invalid rows (avoid duplicates if a row fails both checks)
dropped_rows = pd.concat([invalid_customer_rows, invalid_product_rows]).drop_duplicates(subset=["order_id"])

# Report and save dropped rows
if not dropped_rows.empty:
    dropped_path = os.path.join(output_folder, "orders_dropped.csv")
    dropped_rows.to_csv(dropped_path, index=False)
    print(f"✗ Removed {len(dropped_rows)} rows; saved details to: {dropped_path}")
else:
    print("✅ No rows were dropped due to invalid customer_id or product_id.")

# Remove invalid rows from orders
orders_clean = orders.loc[~orders["order_id"].isin(dropped_rows["order_id"])].reset_index(drop=True)

# (Optional) Drop helper columns, parse dates, etc.
if "order_date_parsed" in orders_clean.columns:
    orders_clean = orders_clean.drop(columns=["order_date_parsed"])

# Save cleaned orders
cleaned_path = os.path.join(output_folder, "orders_clean.csv")
orders_clean.to_csv(cleaned_path, index=False)
print(f"Saved cleaned orders to: {cleaned_path}")
```

Rename reference columns (examples)

* Keep a consistent naming pattern to make downstream analysis and dashboards easier to read.

| Original column       | Recommended rename                             |
| --------------------- | ---------------------------------------------- |
| `name` (in products)  | `product_name`                                 |
| `name` (in customers) | `customer_name`                                |
| `id` or `product_id`  | `product_id` (keep consistent across datasets) |

Merge, compute, and preview

* Merge reference data into the cleaned orders with left joins so you retain all order rows and attach product and customer attributes. Then compute a `line_total` column.

```python theme={null}
# python
# Load cleaned orders (if not already in memory)
orders = pd.read_csv(cleaned_path)

# Rename 'name' column in products and customers to avoid conflict
products_renamed = products.rename(columns={"name": "product_name"})
customers_renamed = customers.rename(columns={"name": "customer_name"})

# Merge product info into orders (left join preserves all orders)
orders = orders.merge(
    products_renamed[["product_id", "product_name", "price"]],
    on="product_id",
    how="left"
)

# Merge customer info into orders
orders = orders.merge(
    customers_renamed[["customer_id", "customer_name"]],
    on="customer_id",
    how="left"
)

# Calculate line total
orders["line_total"] = orders["quantity"] * orders["price"]

# Preview selected columns (first 10 rows)
orders_preview = orders[["order_id", "customer_name", "product_name", "quantity", "price", "line_total"]].head(10)
print("Order Calculations (first 10 rows):")
print(orders_preview.to_string(index=False))
```

Aggregate to answer business questions

* Use groupby + sum to compute total revenue by product and total spend by customer, then sort and select the top 3.

```python theme={null}
# python
# Top 3 products by total revenue
top_products = (
    orders.groupby("product_id", as_index=False)["line_total"]
    .sum()
    .rename(columns={"line_total": "total_revenue"})
    .merge(products_renamed[["product_id", "product_name"]], on="product_id", how="left")
    .sort_values("total_revenue", ascending=False)
    .head(3)
)

# Top 3 customers by total spend
top_customers = (
    orders.groupby("customer_id", as_index=False)["line_total"]
    .sum()
    .rename(columns={"line_total": "total_spend"})
    .merge(customers_renamed[["customer_id", "customer_name"]], on="customer_id", how="left")
    .sort_values("total_spend", ascending=False)
    .head(3)
)

print("\nTop 3 Products by Revenue:")
print(top_products[["product_name", "total_revenue"]].to_string(index=False))

print("\nTop 3 Customers by Spend:")
print(top_customers[["customer_name", "total_spend"]].to_string(index=False))
```

Best practices recap

* Rename fields early to avoid column name collisions when joining data.
* Use left joins to retain all orders while bringing in reference data.
* Validate foreign keys (customer\_id, product\_id) and record dropped rows for traceability.
* Use grouping and aggregation to summarize revenue and spend for reporting or visualization.
* Keep consistent column naming across your pipeline for maintainability.

> **warning** Always check the ingest log and archive processed files to prevent duplicate ingestions and ensure idempotent pipelines.

Next steps

* Hands-on practice: run this workflow on a sample month of orders and verify the audit trail (dropped rows, ingest log).
* Extend: add date-based rollups (daily/monthly revenue), or create a dashboard-ready summary table.

Links and references

* [pandas documentation](https://pandas.pydata.org/)
* [Jupyter](https://jupyter.org/)
* For more on data validation and pipeline design, consult platform-specific guides (Airflow, Prefect) and your organization's ETL standards.

- [Watch Video](https://learn.kodekloud.com/user/courses/data-engineering-fundamentals/module/2ce5f2e5-ef3a-4e38-a1fd-e95790245533/lesson/cd8093c7-3de7-4750-9f96-454a214c884e)


# What is Database

Source: https://notes.kodekloud.com/docs/Database-Fundamentals/Introduction/What-is-Database/page

Explains what a database is and how structure such as fields, records, tables and types turns raw data into searchable, organized, useful information.

Imagine you're planning a trip.

You saved restaurant names in your Notes app, train times in a [WhatsApp message](https://www.whatsapp.com/), hotel details in an email, and there's a screenshot of your [Airbnb booking](https://www.airbnb.com/) somewhere. On the day of the trip you end up scrolling, searching, and probably swearing.

That's the problem with scattered data: the facts exist, but they're not organized, searchable, or connected. Services like [Booking.com](https://www.booking.com/) keep reservations organized, and your phone reminds you about upcoming flights or hotels—mostly thanks to databases.

<Frame>
  <img alt="The image shows a person standing next to a display that includes the word &#x22;database,&#x22; icons for &#x22;Flights&#x22; and &#x22;Hotels,&#x22; and a smartphone screen with the Booking.com interface. There's also an illustration of a person thinking beside a plant." />
</Frame>

In this article we'll answer: what is a database, how structure turns raw data into useful information, and where you already see databases at work.

<Frame>
  <img alt="The image features a person standing next to a list outlining three objectives about databases, and a cartoon cat character is on the left." />
</Frame>

By the end you'll understand why databases are everywhere and why their structure matters.

Practical example: Cody's vet visits

Cody was logging her pet's vet visits in [Google Sheets](https://www.google.com/sheets/about/), but entries were inconsistent:

* 17 July, checkup, Vet Adams, \$35
* 23-07-25, vaccination, 45, Vet Clark
* 30 July, Vet Brown, microchip, USD 100

The facts are present, but without headings, consistent ordering, or uniform formatting the sheet quickly becomes hard to search or summarize. The solution is structure: clearly defined headings (fields), consistent data formatting (types), and one record per visit (row).

Start by assigning clear headings: Date, Reason, Vet, Cost. Each heading is a field. Move each piece of data into the proper column so each row becomes a single record.

Next, enforce the right data type for each field to make sorting and querying reliable:

| Field  | Suggested data type      |
| ------ | ------------------------ |
| Date   | `date`                   |
| Reason | `text`                   |
| Vet    | `text`                   |
| Cost   | `number` (or `currency`) |

Other common types include `boolean` (true/false) and `integer` vs `float`. Exact names differ between database systems, but the purpose is the same: ensure the right kind of data goes into each field. Relational databases typically enforce this with a predefined schema; some NoSQL systems allow more flexible or dynamic structures.

<Frame>
  <img alt="The image shows a person standing beside a spreadsheet containing veterinary appointment data, including dates, reasons, vets, and costs. The spreadsheet is superimposed on a digital interface with a &#x22;KodeKloud&#x22; logo on the person's shirt." />
</Frame>

With headings and types in place, Cody can:

* sort visits by date,
* filter by reason (e.g., vaccination),
* calculate total spending by summing the `Cost` column.

That's the difference between data and information:

* Data: raw numbers, text, and dates.
* Information: structured, searchable, and meaningful data.

Core database concepts

| Term     | What it means                                                       | Example                                        |
| -------- | ------------------------------------------------------------------- | ---------------------------------------------- |
| Field    | A single column that defines one type of data                       | `Date`, `Name`, `Price`                        |
| Record   | A single row that contains values for all fields                    | One vet visit entry                            |
| Table    | A collection of related records                                     | `VetVisits` table                              |
| Database | One or more tables plus rules and indexes that make data manageable | App backend storing contacts, posts, or orders |

Everyday examples

* Contacts app: each person is a record with fields like name, phone, and email.
* Music playlist: song title, artist, and album are searchable fields.
* Social networks and e-commerce: databases track who follows whom, which photos were posted, product details, prices, reviews, and orders.

<Frame>
  <img alt="The image shows a person standing next to an illustration of a mobile music playlist app, highlighting aspects like play buttons, song details, and features such as fields, searchability, and filterability." />
</Frame>

Think about [Instagram](https://www.instagram.com/): over a billion users, each with posts, followers, and messages. Every like, comment, and follow is managed by databases so the app can display the correct feed and let you search for a friend or hashtag.

<Frame>
  <img alt="The image features a presentation slide with a graphic of a phone screen displaying an Instagram-like profile of a cartoon cat named Kodyland. It also includes the word &#x22;Database&#x22; and a person gesturing, likely explaining a concept related to &#x22;WHO follows WHOM.&#x22;" />
</Frame>

Similarly, [Amazon](https://www.amazon.com/) lists millions of products and processes hundreds of millions of orders. Product details, prices, inventory, reviews, and orders are tracked and updated in real time—only possible with robust databases.

<Frame>
  <img alt="The image features a smartphone displaying a grid of package icons with &#x22;Amazon&#x22; at the top, alongside text elements related to database functions like &#x22;Product Detail,&#x22; &#x22;Price,&#x22; &#x22;Review,&#x22; and &#x22;Order Placed.&#x22; A person stands beside the display wearing a &#x22;KodeKloud&#x22; shirt, suggesting an educational or professional tech context." />
</Frame>

Without databases it would be chaos: customers couldn't reliably search, see accurate prices, check availability, or have warehouses ship the right items.

Quick quiz

Which statement is true?

A. A field is a full row of data in a table.\
B. A record stores one specific piece of information.\
C. Structure helps turn data into useful information.

Correct answer: C. Structure lets a database organize raw facts into something we can search, sort, and use.

* Option A is backwards: a field is a single column (e.g., `Date` or `Name`).
* A record is a full row that stores all fields for a single entry (e.g., one vet visit).

Summary

* A database is a structured place to store and organize related information.
* Fields (columns) define the type of data; records (rows) hold complete entries.
* Structure—headings, data types, and consistency—turns raw data into useful information.
* Everyday apps (contacts, music, social media, e-commerce) rely on databases to function at scale.

We'll next explain how databases store structured data using keys, indexes, and relationships.

> **lightbulb** Databases enforce structure so you can reliably query, sort, and analyze data. Even simple apps depend on this structure to work correctly.

- [Watch Video](https://learn.kodekloud.com/user/courses/database-fundamentals/module/774d0759-f241-4acf-bf3c-3533b24824a4/lesson/13e006a3-c533-4ad0-ad6f-7da048d321ec)
