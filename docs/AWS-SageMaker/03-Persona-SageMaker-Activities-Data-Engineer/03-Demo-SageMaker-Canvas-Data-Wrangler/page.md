# Typical imports used in the exported notebook
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.dataset_definition.inputs import AthenaDatasetDefinition, DatasetDefinition, RedshiftDatasetDefinition

import time
import uuid
import boto3
import sagemaker
import os
import json
from pprint import pprint
```

Define the S3 bucket and create a unique export prefix:

```python theme={null}
# Define the S3 bucket used to store export outputs
bucket = "kodekloud-sagemaker-demystified"

# Create a unique export name and S3 prefix
flow_export_id = f"{time.strftime('%d-%H-%M-%S', time.gmtime())}{str(uuid.uuid4())[:8]}"
flow_export_name = f"flow-{flow_export_id}"

# Output_name is auto-generated from the select node's ID + output name from the flow file.
output_name = "3e5d1454-c172-4b12-b0c9-99b2e4d040d1.default"

s3_output_prefix = f"export-{flow_export_name}/output"
s3_output_base_path = f"s3://{bucket}/{s3_output_prefix}"
print(f"Processing output base path: {s3_output_base_path}\nThe final output location will contain additional subdirectories.")
```

Configure the ProcessingOutput that writes results to S3:

```python theme={null}
processing_job_output = ProcessingOutput(
    output_name=output_name,
    source="/opt/ml/processing/output",
    destination=s3_output_base_path,
    s3_upload_mode="EndOfJob"
)
```

Provide the exported `.flow` file as a ProcessingInput:

```python theme={null}
# The flow file's S3 location (from the Data Wrangler export)
flow_s3_uri = "s3://kodekloud-sagemaker-demystified/output_1746186367/kk-house-price-flow.flow"
print(f"Data flow is located at {flow_s3_uri}")

# Provide the flow file as a ProcessingInput to the SageMaker Processing job
flow_input = ProcessingInput(
    source=flow_s3_uri,
    destination="/opt/ml/processing/flow",
    input_name="flow",
    s3_data_type="S3Prefix",
    s3_input_mode="File",
    s3_data_distribution_type="FullyReplicated"
)
```

## Inspect the .flow file (JSON) locally

The `.flow` file is JSON and contains the pipeline metadata, nodes, operators, and parameters. Loading and pretty-printing it in the notebook helps you review the exact transformations and execution settings:

```python theme={null}
import json
from pprint import pprint

with open('kk-house-price-flow.flow') as f:
    data = json.load(f)

pprint(data)
```

Key contents you will typically see:

* metadata (for example, an `instance_type` suggestion like "ml.m5.4xlarge")
* nodes list with SOURCE and TRANSFORM nodes (infer\_and\_cast\_type, drop column, impute, scale, ordinal encode, one-hot encode)
* operator implementations (often under `sagemaker.spark.*`)
* transform parameters and any trained parameters (e.g., learned imputations or encodings)

Example (truncated) pretty-printed snippet:

```python theme={null}
pprint(data)
# Example (truncated) output:
{
  'metadata': {'disable_limits': False,
               'disable_validation': True,
               'instance_type': 'ml.m5.4xlarge',
               'version': 1},
  'nodes': [
    {'inputs': [],
     'node_id': 'acd19907-5e1c-43d8-a793-eaa3a96090dd',
     'operator': 'sagemaker.s3.addsample_1',
     'outputs': [{'name': 'default',
                  'sampling': {'sample_size': 50000,
                               'sampling_method': 'sample_by_count'}}],
     'parameters': {'dataset_definition': {
         'datasetSourceType': 'S3',
         'name': 'kaggle_london_house_kodekloud.csv',
         's3ExecutionContext': {
             's3Uri': 's3://kodekloud-sagemaker-demystified/kaggle_london_house_price_data_sampled_data (1).csv',
             's3ContentType': 'csv',
             's3HasHeader': True,
             's3FieldDelimiter': ','
         }
     }},
     'type': 'SOURCE'
    },
    {'inputs': [{'name': 'default', 'node_id': 'acd19907-...'}],
     'node_id': '264941a0-5967-40e3-8ccd-ae155ed40af0',
     'operator': 'sagemaker.spark.infer_and_cast_type_0.1',
     'trained_parameters': {'schema': {
         'bathrooms': 'float',
         'bedrooms': 'float',
         ...
         'tenure': 'string'}},
     'type': 'TRANSFORM'
    },
    ...
    {'operator': 'sagemaker.spark.encode_categorical_0.1',
     'parameters': {'one_hot_encode_parameters': {
         'input_column': ['propertyType', 'tenure'],
         'drop_last': False,
         'output_style': 'Vector'
     }, 'operator': 'One-hot encode'},
     'type': 'TRANSFORM',
     'node_id': '3e5d1454-c172-4b12-b0c9-99b2e4d040d1'
    }
  ]
}
```

This JSON shows the exact transform sequence and parameters that Data Wrangler will run via a Spark-based processing job.

<Frame>
  <img alt="A screenshot of a development environment showing a file browser on the left and a code/editor pane on the right. A pointer is selecting a file named &#x22;kk-house-price-flow.flow&#x22; and the editor displays a long JSON-like flow/metadata file with many parameters." />
</Frame>

## Wrap-up and next steps

* The exported notebook plus the `.flow` file provide a reproducible way to run the same Data Wrangler transformations in a SageMaker Processing job.
* Hand the notebook to data scientists or integrate it into automated pipelines to produce transformed datasets for training.
* Always shut down idle SageMaker Canvas instances to avoid unnecessary charges.

| Export Target            |                                          Best For | Notes                                                     |
| ------------------------ | ------------------------------------------------: | --------------------------------------------------------- |
| Canvas dataset           |              Quick low-code iteration and sharing | Viewable from SageMaker Datasets page                     |
| Amazon S3                | Integrating with downstream processing or storage | Spark output uses `part-00000-...` prefixes               |
| Jupyter Notebook + .flow |            Reproducible code-based processing job | Notebook configures SageMaker Processing and uses `.flow` |

Links and references

* [Amazon SageMaker Data Wrangler](https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html)
* [Amazon SageMaker Canvas overview](https://docs.aws.amazon.com/sagemaker/latest/dg/canvas.html)
* [SageMaker Processing jobs](https://docs.aws.amazon.com/sagemaker/latest/dg/processing.html)
* [Amazon S3 documentation](https://docs.aws.amazon.com/s3/index.html)

<Callout icon="lightbulb">
  When copying S3 objects whose key contains spaces, quote the S3 URI (or URL-encode the path) so the CLI treats it as a single argument. Also ensure the IAM role or credentials used by your notebook/studio have access to the bucket.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/dc8df298-eaee-4f8a-b1d0-0ec66f9c6d20/lesson/73e19b8c-c347-45e3-9bfc-ae0d4689d324" />
</CardGroup>


# Demo SageMaker Canvas Data Wrangler

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-Data-Engineer/Demo-SageMaker-Canvas-Data-Wrangler/page

Demonstration of SageMaker Canvas Data Wrangler for no-code data preparation including DQI reporting, dropping and imputing features, scaling and encoding, and exporting ML-ready datasets.

In this lesson we'll demonstrate SageMaker Canvas Data Wrangler, a low-code visual tool for engineering and preparing datasets for machine learning (and for exporting them for training) — all without writing Python. This guide walks through:

* Launching SageMaker Canvas and opening Data Wrangler
* Generating a Data Quality and Insights (DQI) report to guide preprocessing
* Applying common transforms (drop columns, impute missing values, scale numeric features, encode categorical variables)
* Exporting the cleaned dataset (for example, to Amazon S3)

<Frame>
  <img alt="A presentation slide titled &#x22;Agenda&#x22; with four numbered items listed down the right side. The items cover: Launching SageMaker Canvas Data Wrangler; Generating Data Quality Reports; Transforming and Preparing Data for ML Training; and Exporting Transformed Data." />
</Frame>

Overview of practical steps:

1. Open Data Wrangler through SageMaker Canvas.
2. Add a data source (we use a London housing prices CSV).
3. Generate a DQI report to identify issues and recommended transforms.
4. Build a data flow to drop irrelevant or leaking columns, impute missing values, scale numeric features, and encode categorical features.
5. Export the processed dataset (S3 or Canvas model builder).

<Frame>
  <img alt="A presentation slide titled &#x22;Demo Steps&#x22; listing eight numbered data-preprocessing steps, including opening a Data Wrangler, adding a data source, creating a report, dropping columns, applying imputation and scaling, one-hot encoding, and exporting processed data." />
</Frame>

Getting started

We begin in Amazon SageMaker Studio. If you prefer JupyterLab or other Studio applications, those are launched from the Applications pane. Data Wrangler is accessed from the SageMaker Canvas application.

Canvas runs as a managed instance. If the Canvas instance is stopped, start it — this can take a minute or two. Be mindful of lifecycle and billing.

<Callout icon="warning">
  SageMaker Canvas is billed while the managed instance is running (per minute). The instance cost is roughly \$2 per hour (approximate). Stop the Canvas instance when not in use to avoid unintended charges.
</Callout>

When Canvas is running, click Open Canvas.

<Frame>
  <img alt="The image shows the Amazon SageMaker Studio Canvas dark-themed web dashboard with a highlighted &#x22;Open Canvas&#x22; button and a hand cursor. The main area outlines no-code ML features (prepare data, train models, predict outcomes) and learning resources, with a left sidebar of related apps and navigation." />
</Frame>

Inside Canvas, Data Wrangler appears in the left-hand navigation. Data Wrangler lets you visually author a sequence of transformations (a data flow) to convert raw source data into ML-ready features (drop columns, impute, scale, encode).

<Frame>
  <img alt="A screenshot of the Amazon SageMaker Canvas web interface with a large banner promoting &#x22;Amazon Q&#x22; and a &#x22;Get started&#x22; area. Below the banner are quick-action tiles like &#x22;Create a model&#x22; and &#x22;Explore Generative AI,&#x22; with navigation icons down the left side." />
</Frame>

Importing data

Click Import and prepare to start a new Data Wrangler flow. Data Wrangler supports tabular and image data; for this demo we import a CSV (tabular).

<Frame>
  <img alt="A screenshot of the Amazon SageMaker Data Wrangler interface showing a workflow (Import data → Prepare data → Scale data operations → Build models). A dropdown labeled &#x22;Import and prepare&#x22; is open with dataset options like Tabular and Image, and a hand cursor pointing at the Image option." />
</Frame>

Canvas connects to many sources (S3, Redshift, Athena, Snowflake, Databricks, Salesforce, etc.). Some connectors require configuration before use. For this walkthrough we select Amazon S3.

<Frame>
  <img alt="A screenshot of an &#x22;Import tabular data&#x22; interface showing a list of sample CSV datasets (name, columns, rows, cells, created, status). A hand-shaped cursor is clicking the &#x22;canvas-sample-diabetic-readmission.csv&#x22; entry." />
</Frame>

Choose the S3 bucket that holds your CSV and open the target file. Canvas shows a preview (first \~100 rows) so you can inspect columns before importing.

<Frame>
  <img alt="A data-import interface showing a pop-up to select a data source (Canvas Datasets, Amazon S3, Redshift, Snowflake, etc.) with a list of sample CSV datasets visible behind it. A hand-shaped cursor is pointing at the Redshift option." />
</Frame>

For this demonstration we use a Kaggle London housing price dataset. The preview includes fields such as full address, postcode, latitude, longitude, bedrooms, bathrooms, floor area (sq m), property type, energy rating, and sale/rental estimate columns.

<Frame>
  <img alt="A screenshot of a dataset import preview showing the first rows of a CSV (kaggle_london_house_price_data_sampled_data) with columns like latitude, longitude, bathrooms, bedrooms, floorAreaSqM and livingRooms. An import settings panel with sampling options is visible on the right and a cursor arrow hovers over the table." />
</Frame>

Name the dataset, for example `Kaggle_London_house_price_data_KodeKloud`. For faster exploration you can import a random sample instead of the full file — this speeds DQI report generation and interactive debugging. In the demo we import a sample of 50,000 rows.

<Callout icon="lightbulb">
  Importing a sampled subset is a practical way to iterate quickly. Use sampled data to test transforms and generate insights; then re-run transforms on the full dataset when you’re ready to export.
</Callout>

After importing, the Data Wrangler canvas displays the S3 source node and an inferred Data types node listing detected feature types. Build transforms by clicking the blue plus (+) after the Data types node.

Generating a DQI report

To determine required transforms, generate a Data Quality and Insights (DQI) report: Add → Get data insights. The DQI report analyzes dataset health, feature statistics, and potential model signals.

<Frame>
  <img alt="A screenshot of a Data Wrangler &#x22;Data flow&#x22; UI showing an S3 source (kaggle_london_house_...) connected to a &#x22;Data types&#x22; node. A context menu with options like &#x22;Add transform&#x22; and &#x22;Get data insights&#x22; is open, and a hand-cursor is selecting an item while a &#x22;Validation complete — 0 errors&#x22; message appears at the top." />
</Frame>

Create the DQI report (for example `DQI_report`). Choose the target column (`saleEstimate_currentPrice`) and the problem type (Regression). You can run the report against the sampled dataset for speed or the full dataset for completeness.

<Frame>
  <img alt="Screenshot of a web UI for creating a &#x22;Data Quality And Insights Report&#x22; (analysis name &#x22;dqi_report&#x22;) with the target column set to saleEstimate_currentPrice, problem type &#x22;Regression&#x22;, and data size &#x22;Sampled dataset&#x22;. The main pane shows &#x22;No Preview available&#x22; and a &#x22;Create&#x22; button is visible on the right." />
</Frame>

DQI report outputs

While the report runs, Canvas computes summary statistics and metadata. Typical outputs include:

* Dataset-level statistics (row count, missing %, duplicates)
* Feature counts by type (numeric, categorical, datetime)
* Per-feature statistics (mean, median, min/max, skew)
* Missing value and outlier detection, anomaly scores
* Feature predictive power and target leakage warnings
* Quick-model estimates (validation scores such as MSE, RMSE for baselining)

You get immediate summary stats and prioritized warnings to guide transformations.

<Frame>
  <img alt="Screenshot of a Data Wrangler summary for a file named kaggle_london_house_kodekloud.csv showing dataset statistics (28 features, 28,287 rows, 5.9% missing, 94.1% valid) and a feature-type count. Below the summary are high-priority warnings highlighting multiple target leakage and a skewed target." />
</Frame>

Interpreting high-priority warnings

In this dataset the DQI report flagged:

* Potential target leakage: columns that directly or indirectly reveal the target (e.g., saleEstimate\_lowerPrice and saleEstimate\_upperPrice). These must be removed.
* Skew and outliers in the target distribution — consider log transforms or robust metrics.
* Missingness in features such as `livingRooms` (≈14% missing) indicating imputation is needed.

<Frame>
  <img alt="A screenshot of a Data Wrangler / data flow interface showing the file &#x22;kaggle_london_house_kodekloud.csv&#x22; with a target-column summary (valid %, missing %, outliers, min/max/mean/median/skew). To the right is a histogram marking outliers, and below are sample rows of London property records with addresses, postcodes, coordinates and property attributes." />
</Frame>

The DQI report also includes a quick-model evaluation (R², MSE, RMSE, MAE) to give a baseline for expected predictive performance.

<Frame>
  <img alt="A screenshot of a &#x22;Quick model&#x22; results page in a data-wrangling tool showing a table of validation and train scores (R2, MSE, RMSE, MAE, max error, median absolute error). Below the table is a &#x22;Feature summary&#x22; section with explanatory text about prediction power and feature ordering." />
</Frame>

Review feature-level summaries to see prediction power and data quality. Remove features flagged for target leakage (e.g., `saleEstimate_lowerPrice`, `saleEstimate_upperPrice`) before training.

<Frame>
  <img alt="Screenshot of a Data Wrangler &#x22;Feature details&#x22; page for the numeric feature saleEstimate_lowerPrice, showing a stats table (min, max, mean, missing, outliers, prediction power) and a histogram with target distribution. A highlighted &#x22;Target leakage&#x22; warning is displayed beneath the table." />
</Frame>

<Frame>
  <img alt="Screenshot of an AWS SageMaker Data Wrangler report highlighting a &#x22;Target leakage&#x22; warning for the feature saleEstimate_upperPrice. It shows a table of numeric statistics (min, max, mean, missing, outliers) alongside a histogram and target distribution plot." />
</Frame>

Text and datetime features get specialized summaries (word clouds, temporal patterns). Use these insights to choose the right transforms.

<Frame>
  <img alt="A screenshot of an AWS SageMaker Data Wrangler data-flow report for a CSV (kaggle_london_house_kodekloud.csv) showing feature summary tables and charts. It displays statistics and histograms for fields like saleEstimate_valueChange.percentageChange and history_date with prediction-power metrics." />
</Frame>

Applying transforms — build the data flow

After reviewing the DQI report, return to the Data Wrangler canvas and add transforms in sequence. Inspect the output at each step to validate results.

<Frame>
  <img alt="The image shows an AWS SageMaker Data Wrangler screen with a dataset summary table and a horizontal bar chart of feature prediction power. The chart lists features (e.g., saleEstimate_lowerPrice, saleEstimate_upperPrice, fullAddress) ranked by their prediction power." />
</Frame>

Step 1 — Drop target-leakage and irrelevant columns

* Click the blue plus (+) after the Data types node → Add transform.
* Search for “drop” → choose “Manage columns: move, drop, duplicate or rename columns” → select Drop column.
* Remove columns that leak the target (e.g., `saleEstimate_lowerPrice`, `saleEstimate_upperPrice`), rental-specific columns, historical-change fields, and confidence metrics.
* Click Add to insert the Drop column transform into the flow.

<Frame>
  <img alt="A screenshot of AWS SageMaker Data Wrangler showing a preview of a &#x22;kaggle_london_house_kodekloud.csv&#x22; dataset with columns like fullAddress, postcode, country, outcode, latitude and longitude. The right side shows a &#x22;Manage columns&#x22; panel where several columns are selected to be dropped or kept." />
</Frame>

The Drop column step will appear downstream of the Data types node in the flow.

<Frame>
  <img alt="A screenshot of Amazon SageMaker Data Wrangler showing a data flow diagram with an S3 Source feeding a &#x22;Data types&#x22; step, which connects to a &#x22;Data Quality And Insights Report&#x22; and a &#x22;Drop column&#x22; transform. The interface shows validation complete with no errors." />
</Frame>

Step 2 — Impute missing values

* Add transform → search “impute” → choose Handle missing.
* Select the column (e.g., `livingRooms`).
* Pick an imputation strategy: mean, approximate median, mode, etc. Median-based strategies are robust to outliers; mean can be influenced by extreme values. For this demo, use approximate median.
* Add the transform and validate the updated distribution.

Step 3 — Scale numeric features

* Add transform → Process numeric.
* Choose a scaler (StandardScaler, RobustScaler, MinMaxScaler, MaxAbs). These correspond to standard scikit-learn scalers.
* Example: use MinMaxScaler for `floorAreaSqM` to bring values into a normalized range.
* Commit the transform and verify the numeric ranges.

Step 4 — Encode categorical features

* Add transform → search “encode” → choose Encode categorical.
* Encoding options: ordinal, one-hot, similarity encoding.
  * Use ordinal encoding for ordered categories (e.g., energy rating A→B→C).
  * Use one-hot encoding for nominal categories (e.g., `propertyType`, `tenure`).
* Select columns to encode and add the transformations.

<Frame>
  <img alt="Screenshot of AWS SageMaker Data Wrangler displaying a tabular view of a London housing dataset (columns like fullAddress, postcode, country, latitude, longitude) with distribution histograms. On the right is an &#x22;Encode categorical&#x22; pane showing options to one-hot encode selected columns." />
</Frame>

Transform summary

| Transform Type            | Purpose                               | When to use                                                                     |
| ------------------------- | ------------------------------------- | ------------------------------------------------------------------------------- |
| Drop columns              | Remove irrelevant or leaking features | Remove target-leakage columns, identifiers, or high-cardinality nuisance fields |
| Handle missing            | Impute missing values                 | Use median/mode/mean based on distribution and outliers                         |
| Process numeric (scaling) | Normalize or scale numeric features   | Use when features have different ranges or to speed model convergence           |
| Encode categorical        | Convert categorical to numeric        | One-hot for nominal, ordinal for ordered categories                             |

Validate outputs

As you add transforms, inspect the preview at each node to ensure transformations behave as expected and to catch validation errors early. Once the data flow is complete and validated, export the processed dataset.

Exporting processed data

Data Wrangler supports exporting transformed datasets to destinations such as S3, or you can feed the transformed output directly into Canvas model-building. Choose Export → Amazon S3 (or Canvas model) and specify the target location.

Summary

This demo covered:

* Launching SageMaker Canvas and opening Data Wrangler
* Creating a Data Quality and Insights (DQI) report to surface data issues and feature importance
* Applying common transforms: drop columns, impute missing values, scale numeric features, and encode categorical features
* Validating each step and exporting the final ML-ready dataset

<Frame>
  <img alt="A screenshot of an AWS SageMaker Data Wrangler report highlighting a &#x22;Target leakage&#x22; warning for the feature saleEstimate_upperPrice. It shows a table of numeric statistics (min, max, mean, missing, outliers) alongside a histogram and target distribution plot." />
</Frame>

Links and references

* SageMaker Canvas overview: [https://docs.aws.amazon.com/sagemaker/latest/dg/canvas.html](https://docs.aws.amazon.com/sagemaker/latest/dg/canvas.html)
* SageMaker Data Wrangler: [https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html](https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html)
* Amazon S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)

If you want the recommended next steps: run the full-data export, verify transforms on the full dataset, and use the processed dataset to train models in Canvas or SageMaker training jobs.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/dc8df298-eaee-4f8a-b1d0-0ec66f9c6d20/lesson/a8b69fcf-718c-4c17-8788-8e263c912789" />
</CardGroup>
