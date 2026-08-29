# Automation and Orchestration

Source: https://notes.kodekloud.com/docs/Data-Engineering-Fundamentals/Automation-and-Orchestration/Automation-and-Orchestration/page

Guide to modularizing and automating data pipelines with ingest, clean, transform stages, orchestrator scripts, idempotent state tracking, and scheduling options

Welcome back.

It’s the first of November — one month before the deadline — and October’s orders just arrived. Your pipeline already ingests, validates, cleans, and transforms raw CSVs into actionable insights, but you still run Jupyter Notebook cells by hand in the right order. Human-driven workflows work, but they’re error-prone and hard to scale.

In this lesson we’ll cover:

* Risks of a manual pipeline
* Benefits of automation
* How an orchestrator sequences and tracks pipeline steps
* A simple, modular pipeline pattern you can run locally or schedule in production

Initially you packaged everything into a single Python script and ran it like this:

<Frame>
  <img alt="The image features a person with a KodeKloud t-shirt standing next to a description of tasks related to data pipelines, accompanied by an animated cat character." />
</Frame>

```bash theme={null}
python pipeline.py
```

That made execution deterministic (all steps run every time) and reduced mistakes, but the file quickly became hard to read and maintain. Console output for the single-file run might look like:

```plaintext theme={null}
Schema validation passed.
Saved orders data to: insights/2025/10/orders.csv
Logged ingestion to logs/ingest_log.csv
Removed 1 rows with missing values in required fields: [1184]
Removed 2 rows with invalid quantity: [1191, 1199]
Removed 2 duplicate rows: []
Removed 4 rows with invalid customer_id: [1165, 1175, 1176, 1198]
Removed 1 rows with invalid product_id: [1201]
Saved 10 dropped rows to: insights/2025/10/orders_dropped.csv
Cleaned data saved to: insights/2025/10/orders_clean.csv

Order Calculations (first 10 rows):
 order_id  customer_name     product_name           quantity  price  line_total
 1154      Chewbacca         Blue Milk Latte           4      4.5      18.0
 1155      Darth Vader       Blue Milk Latte           1      4.5       4.5
 1156      Darth Vader       Blue Milk Latte           1      4.5       4.5
 1157      Leia Organa       Death Star Espresso       3      3.0       9.0
 1158      Han Solo          Tatooine Mocha            1      6.0       6.0
 1159      Padmé Amidala     Wookiee Cappuccino        4      4.5      18.0
 1160      Padmé Amidala     Death Star Espresso       1      3.0       3.0
 1161      Obi-Wan Kenobi    Tatooine Mocha            1      4.0       4.0

Top 3 Products by Revenue:
 product_name         total_revenue
 Blue Milk Latte           103.5
 Wookiee Cappuccino         73.5
 Tatooine Mocha             72.0

Top 3 Customers by Spend:
 customer_name    total_spend
 Chewbacca           62.0
 Leia Organa         59.5
 Darth Vader         53.0

root@host01 ~/code via 🐍 v3.12.3 (venv) $
```

Splitting into modules

To improve readability and reuse, break the single script into focused modules:

* `ingest.py` — read and validate raw file, archive it, and log ingestion
* `clean.py` — drop or correct invalid rows and save cleaned data
* `transform.py` — join cleaned orders to `products` and `customers`, compute metrics

Start by centralizing folder and path setup (either in each module or a shared helper). Example setup inside `ingest.py` to find an orders file:

```python theme={null}
