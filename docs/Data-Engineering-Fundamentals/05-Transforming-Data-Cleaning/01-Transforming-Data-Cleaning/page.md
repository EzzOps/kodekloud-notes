# serve.py
import os
import matplotlib.pyplot as plt

def run(top_products, top_customers, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Save summaries to CSV
    tp_csv = os.path.join(output_folder, "top_products.csv")
    tc_csv = os.path.join(output_folder, "top_customers.csv")
    top_products.to_csv(tp_csv, index=False)
    top_customers.to_csv(tc_csv, index=False)
    print(f"Saved analytics to: {tp_csv} and {tc_csv}")

    # Create bar chart for top products
    plt.figure(figsize=(8, 4))
    plt.bar(top_products["product_name"], top_products["total_revenue"], color="skyblue")
    plt.title("Top Products by Revenue")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    products_chart = os.path.join(output_folder, "top_products.png")
    plt.savefig(products_chart)
    plt.close()
    print(f"Saved product chart to: {products_chart}")

    # Create bar chart for top customers
    plt.figure(figsize=(8, 4))
    plt.bar(top_customers["customer_name"], top_customers["total_spend"], color="salmon")
    plt.title("Top Customers by Spend")
    plt.ylabel("Spend")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    customers_chart = os.path.join(output_folder, "top_customers.png")
    plt.savefig(customers_chart)
    plt.close()
    print(f"Saved customer chart to: {customers_chart}")
```

Notes on Matplotlib usage

* Build charts in layers: create a figure, plot the data, add title/labels, adjust layout with `tight_layout()`, then `savefig()` and `close()`.
* Rotate x-axis labels with `plt.xticks(rotation=45, ha="right")` to prevent overlap when names are long.
* Keep charts simple and readable — these are for quick insights or slide decks, not exploratory notebooks.

Connecting the serve step to the pipeline
Import and call `serve.run` from your pipeline orchestration script (e.g., `run_pipeline.py`). Use consistent variable names for paths and outputs so each stage knows where to read and write.

A concise example of `run_pipeline.py` that runs ingest → clean → transform → serve:

```python theme={null}
# run_pipeline.py
import os
from pipeline import ingest, clean, transform, serve

# Define folders and paths
data_folder = "data"
archive_folder = os.path.join(data_folder, "archive")
insights_folder = os.path.join(data_folder, "insights")
logs_folder = "logs"

products_path = os.path.join(data_folder, "products.csv")
customers_path = os.path.join(data_folder, "customers.csv")
log_path = os.path.join(logs_folder, "ingest_log.csv")

def run_pipeline():
    # Step 1: Find a new orders file to process
    files = [f for f in os.listdir(data_folder) if f.startswith("orders") and f.endswith(".csv")]
    file_name = files[0] if files else None

    if not file_name:
        print("🚫 No orders file found - exiting.")
        return

    print(f"🛠️ Starting pipeline for: {file_name}")

    try:
        # Each stage returns or writes its outputs in a predictable place
        output_folder = ingest.run(file_name, data_folder, archive_folder, insights_folder, log_path)
        clean.run(products_path, customers_path, output_folder)
        top_products, top_customers = transform.run(products_path, customers_path, output_folder)
        serve.run(top_products, top_customers, output_folder)

        print(f"✅ Pipeline completed for: {file_name}")
    except Exception as e:
        print(f"❗ Pipeline failed: {e}")

if __name__ == "__main__":
    run_pipeline()
```

When you run the pipeline for November you'll see console output confirming each stage and messages from the serve step indicating that CSVs and PNG charts were saved to the output folder.

<Frame>
  <img alt="The image shows a person in front of a computer screen displaying code related to a data engineering pipeline project. The project involves data ingestion, cleaning, transformation, serving, and automation using Python, pandas, and matplotlib." />
</Frame>

README: make it useful and short
A README should tell someone what the project does, how to run it, and where to find outputs — in a few lines.

Essential sections

* Project summary (1–2 sentences)
* Pipeline steps (ingest, clean, transform, serve)
* How to run locally (command)
* Outputs and folder structure
* Quick troubleshooting or notes (optional)
* Example screenshots (optional)

Example README content (Markdown):

````markdown theme={null}
## What it does
Ingests monthly orders CSVs, cleans and enriches the data, computes top products and top customers, and saves CSV summaries and PNG charts.

## Pipeline steps
1. ingest: locate and archive new orders, update ingest log
2. clean: normalize product and customer data
3. transform: compute summaries (top products/customers)
4. serve: save CSVs and charts to the output folder

## Run locally
```bash
python run_pipeline.py
```text

## Outputs
- data/insights/YYYY-MM-DD/top_products.csv
- data/insights/YYYY-MM-DD/top_customers.csv
- data/insights/YYYY-MM-DD/top_products.png
- data/insights/YYYY-MM-DD/top_customers.png
````

<Callout icon="lightbulb">
  Keep the README short and focused: how to run, what to expect, and where to find results. Example screenshots and a brief folder tree are helpful.
</Callout>

Version control
Commit your README and pipeline code to Git so others can reproduce and contribute. Minimal workflow:

```bash theme={null}
git add .
git commit -m "Add serving step and README"
git push origin main
```

<Frame>
  <img alt="The image shows a person standing in front of a screen displaying a README file with CSV file listings and bar charts illustrating the top products by revenue and top customers by spend." />
</Frame>

Why this matters

* Clear outputs and a short README make your pipeline usable by analysts, product managers, and developers.
* CSVs are interoperable; PNGs are easy to preview and paste into reports.
* Version-controlled code ensures reproducibility and easy collaboration.

Recap

* Serving turns pipeline outputs into usable assets: CSV summaries, PNG charts, and concise documentation.
* Use Matplotlib to convert numeric summaries into clear visuals saved as PNGs.
* Keep README focused: what it does, steps, how to run, and where outputs live.
* Commit to Git so your work is shareable and reproducible.

Congratulations — you delivered a working data pipeline and made its outputs accessible to others.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/data-engineering-fundamentals/module/85073c4f-111a-4323-a685-c0a9303e55e2/lesson/836f2a01-a89d-45bd-b1e5-19f82a12475a" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/data-engineering-fundamentals/module/85073c4f-111a-4323-a685-c0a9303e55e2/lesson/684df290-e717-41b5-954b-008f6534fc8e" />
</CardGroup>


# Transforming Data Cleaning

Source: https://notes.kodekloud.com/docs/Data-Engineering-Fundamentals/Transforming-Data-Cleaning/Transforming-Data-Cleaning/page

Practical, repeatable data cleaning of incoming orders using pandas, validating columns rows and tables, dropping and logging invalid rows, and saving cleaned data and audit artifacts.

Last month you successfully ingested July's orders. This month’s August orders arrived from multiple humans and systems — and of course some rows look a little off: missing customer IDs, non-existent customers, strange product IDs, negative quantities, and malformed dates. Manual line-by-line fixes aren't feasible at scale.

In this lesson we cover practical, repeatable data cleaning using pandas. We'll focus on common dirty-data patterns (missing values, invalid types, duplicates, mismatched foreign keys), the three levels of validation (column, row, table), and a pragmatic strategy: drop rows that fail validation while logging everything dropped so it can be reviewed and corrected later.

<Frame>
  <img alt="The image shows a person standing next to a presentation slide with a cartoon dog and text discussing data validation concepts." />
</Frame>

## High-level plan

1. Load orders, customers, and products tables.
2. Keep a raw copy of the orders data for auditing and possible re-ingestion.
3. Row-level checks: missing required fields, invalid dates, invalid numeric values, duplicates.
4. Table-level checks: foreign keys (customer\_id, product\_id) must exist in lookup tables.
5. Log and save dropped rows for auditing.
6. Save cleaned dataset and update ingestion logs.

<Callout icon="lightbulb">
  Before you start, activate your environment and ensure pandas is installed. This process is repeatable and should be run as part of your ETL pipeline. Use the raw copy of the incoming file for traceability and audits.
</Callout>

## Initial setup — prepare folders and find the orders file

Create required folders, locate the orders CSV (any filename containing `orders`), and load an ingest log if present.

```python theme={null}
