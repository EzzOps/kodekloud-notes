# BigQuery ML for Data Engineers

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Machine-Learning-Options/BigQuery-ML-for-Data-Engineers/page

Explains how data engineers can build, evaluate, and serve machine learning models inside BigQuery using SQL to reduce data movement, streamline pipelines, and integrate with Google Cloud services

Welcome back.

In this lesson we’ll examine BigQuery ML from a data engineer’s perspective: how it fits into warehouse-centric architectures, why it reduces operational friction, and how you can operate models using familiar SQL.

As data engineers, your core responsibilities usually include managing data warehouses, building reliable pipelines, and preparing clean, queryable data for downstream teams (analytics, data science, product, etc.). Adding ML capability to that stack should ideally minimize data movement and integrate with existing processes.

<Frame>
  <img alt="The slide titled &#x22;BigQuery ML for Data Engineers&#x22; shows an icon labeled &#x22;Data Engineers&#x22; on the left and two gray callouts on the right reading &#x22;Build pipelines for downstream usage&#x22; and &#x22;Work with data warehouses.&#x22;" />
</Frame>

Traditional ML workflows often extract data from the warehouse, re-clean or transform it, move it into a separate data science environment, and train models there. That pattern introduces latency, duplicate data, synchronization problems, and additional cost.

<Frame>
  <img alt="A presentation slide titled &#x22;BigQuery ML for Data Engineers&#x22; showing a row of blue arrow-shaped icons representing a data pipeline. The steps are labeled &#x22;Extract data out of the warehouse,&#x22; &#x22;Clean the data again,&#x22; &#x22;Move it to a data science environment,&#x22; and &#x22;Train the model separately,&#x22; with notes that the process is time-consuming and costly." />
</Frame>

BigQuery ML reduces that friction by enabling you to build, evaluate, and serve ML models directly inside BigQuery using SQL. This keeps data where it already lives and lets teams iterate faster.

Key advantages

* Keep data inside the warehouse for better security, governance, and lower latency.
* Use SQL-first commands such as `CREATE MODEL`, `ML.EVALUATE`, and `ML.PREDICT`.
* Reduce repeated ETL/ELT operations and operational overhead for both engineers and data scientists.

<Callout icon="lightbulb">
  BigQuery ML lets you prototype and deploy many common ML workflows from the BigQuery console, removing data-copy steps and accelerating iteration.
</Callout>

How BigQuery ML fits into the stack

1. BigQuery ML (in-warehouse training and serving)
   * Models live alongside your tables and views and benefit from BigQuery’s storage, IAM, and query optimizations.

2. SQL-based engine
   * Operate models with SQL statements (train, evaluate, predict). Teams comfortable with SQL can quickly adopt ML.

3. Ecosystem integration
   * BigQuery ML integrates with scheduled queries, Cloud IAM, audit logs, and can export models to Vertex AI for advanced workflows.

Common SQL commands and their purpose

| Command        | Purpose                                | Quick example                                                                                                    |
| -------------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `CREATE MODEL` | Train a model from a SQL query         | `CREATE MODEL mydataset.model_name OPTIONS(model_type='logistic_reg') AS SELECT * FROM mydataset.training_table` |
| `ML.EVALUATE`  | Compute evaluation metrics for a model | `SELECT * FROM ML.EVALUATE(MODEL mydataset.model_name, (SELECT * FROM mydataset.eval_table))`                    |
| `ML.PREDICT`   | Generate predictions on new data       | `SELECT * FROM ML.PREDICT(MODEL mydataset.model_name, (SELECT * FROM mydataset.new_data))`                       |

Example: training a simple classification model

```sql theme={null}
CREATE OR REPLACE MODEL `myproject.mydataset.churn_model`
OPTIONS(
  model_type='logistic_reg',
  input_label_cols=['churn']
) AS
SELECT
  user_id,
  IF(churned_at IS NOT NULL, 1, 0) AS churn,
  num_sessions,
  avg_session_length,
  country
FROM `myproject.mydataset.user_activity`
WHERE event_date BETWEEN '2024-01-01' AND '2024-03-31';
```

You can then evaluate:

```sql theme={null}
SELECT *
FROM ML.EVALUATE(MODEL `myproject.mydataset.churn_model`,
  (SELECT * FROM `myproject.mydataset.user_activity_eval`));
```

And predict:

```sql theme={null}
SELECT *
FROM ML.PREDICT(MODEL `myproject.mydataset.churn_model`,
  (SELECT user_id, num_sessions, avg_session_length, country FROM `myproject.mydataset.user_activity_new`));
```

<Frame>
  <img alt="A slide titled &#x22;BigQuery ML – Overview&#x22; showing three colored columns that summarize BigQuery ML features: learning directly in the BigQuery warehouse, SQL-based ML commands (CREATE MODEL, ML.EVALUATE, ML.PREDICT), and ecosystem integration (dataset access, scheduled queries, export to Vertex AI). The slide is branded © KodeKloud." />
</Frame>

Cost, governance, and operational reminders

* Training and prediction consume BigQuery compute (slots) and incur query costs comparable to other BigQuery operations. Monitor usage and budget accordingly.
* Use Cloud IAM roles and dataset-level controls to govern who can create, export, or run models.
* For advanced model types (deep learning, custom training/serving), export models to Vertex AI or integrate with other Google Cloud services.

<Callout icon="warning">
  Training and serving models in BigQuery consume compute and may increase costs. Monitor query cost, slot usage, and apply least-privilege access controls.
</Callout>

Resources and further reading

* BigQuery ML documentation: [https://cloud.google.com/bigquery-ml](https://cloud.google.com/bigquery-ml)
* BigQuery overview: [https://cloud.google.com/bigquery](https://cloud.google.com/bigquery)
* Vertex AI (for exporting models and advanced ML workflows): [https://cloud.google.com/vertex-ai](https://cloud.google.com/vertex-ai)

That’s the high-level view of BigQuery ML for data engineers. In follow-up lessons we’ll explore specific model families, hyperparameter tuning, and how to operationalize models (scheduling training, CI/CD for models, and serving strategies). Thanks for reading.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/d3b59481-7d71-43fa-b0d2-f0bd4e263fa4/lesson/94bf234f-5015-45c1-8529-506c8cb92430" />
</CardGroup>
