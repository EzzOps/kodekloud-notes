# Why Machine Learning in GCP Data Professional

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Machine-Learning-Options/Why-Machine-Learning-in-GCP-Data-Professional/page

Explains why and how data engineers use machine learning on GCP, highlighting BigQuery ML, SQL-first workflows, pipeline automation, model lifecycle, serving, and production integration.

Welcome back. In this lesson we’ll explain why machine learning (ML) matters for data professionals working with Google Cloud Platform (GCP), and how ML integrates into the data engineering lifecycle.

Think about this for a second: as data engineers you already build pipelines, manage ingestion, and optimize data lakes and warehouses. Why add ML on top of that? The answer is simple — businesses want actionable intelligence: predictions, automation, and analytics that directly influence outcomes.

<Frame>
  <img alt="Slide titled &#x22;Role of ML in Modern Data Engineering&#x22; with a simple icon labeled &#x22;Data Engineers&#x22; on the left. On the right are three blue rounded boxes listing responsibilities: &#x22;Optimize data lakes and warehouses,&#x22; &#x22;Manage ingestion,&#x22; and &#x22;Build pipelines.&#x22;" />
</Frame>

Business use cases commonly powered by ML include predicting customer churn, spotting fraud, and recommending products — all of which turn raw data into measurable business value.

<Frame>
  <img alt="A presentation slide titled &#x22;Role of ML in Modern Data Engineering&#x22; listing business needs—insights, predictions and automations; predicting customer churn; spotting fraud; and recommending what users buy next—connected by lines to a purple &#x22;Machine Learning&#x22; icon. The layout shows these use cases feeding into an ML module." />
</Frame>

The good news: enabling ML on GCP typically does not require becoming a full-time data scientist. Data engineers can leverage existing skills — especially SQL and pipeline automation — to enable and operationalize ML.

<Frame>
  <img alt="A slide titled &#x22;Role of ML in Modern Data Engineering&#x22; with a central purple &#x22;Machine Learning&#x22; icon. Two arrows point out: left shows a red cross with &#x22;Doesn't mean becoming a hardcore data scientist,&#x22; and right shows a green check with &#x22;Use the skills you already have, especially SQL.&#x22;" />
</Frame>

<Callout icon="lightbulb">
  As a data engineer you typically enable ML by preparing clean features, automating training and deployment pipelines, and integrating models into applications — you don’t always need to design model architectures from scratch.
</Callout>

How ML fits into typical data engineering workflows

* Data preparation: clean, normalize, and store features at the correct granularity for training.
* Automated ML pipelines: schedule training, retraining, dataset versioning, and CI/CD-style promotion to production.
* Serving and integration: expose batch or online predictions to applications via APIs, scheduled queries, or exported models.
* Monitoring and governance: track model performance, data drift, and ensure reproducibility and access controls.

You might not author every model, but you design and operate the systems that make models reliable and useful. ML depends on robust data engineering to function at scale.

Why BigQuery ML is attractive to data engineers

* SQL-first: create and train models using familiar SQL, eliminating heavy context switching.
* Data-in-place: training runs where your data lives, minimizing data movement and simplifying governance.
* Production-ready: integrates with scheduling, IAM, and existing orchestration tools.
* Cost-effective at scale: leverages BigQuery’s execution engine and billing model for large datasets.

BigQuery ML lets data professionals build models directly inside the data warehouse, bridging data engineering and ML workflows.

A simple BigQuery ML workflow

1. Create a model using SQL.
2. Evaluate the model with built-in evaluation functions.
3. Generate batch predictions with `ML.PREDICT` or enable low-latency serving via model export / Vertex AI integration.
4. Retrain, monitor, and automate model lifecycle tasks inside your existing pipelines.

Example: create and use a basic linear regression model in BigQuery ML

```sql theme={null}
-- Create a linear regression model (training runs inside BigQuery)
CREATE OR REPLACE MODEL `my_project.my_dataset.sales_model`
OPTIONS(model_type='linear_reg', input_label_cols=['sales']) AS
SELECT
  feature_1,
  feature_2,
  sales
FROM
  `my_project.my_dataset.sales_table`;
```

Evaluate the model:

```sql theme={null}
SELECT *
FROM ML.EVALUATE(MODEL `my_project.my_dataset.sales_model`,
  (SELECT feature_1, feature_2, sales FROM `my_project.my_dataset.eval_table`));
```

Generate batch predictions on new data:

```sql theme={null}
SELECT *
FROM ML.PREDICT(MODEL `my_project.my_dataset.sales_model`,
  (SELECT feature_1, feature_2 FROM `my_project.my_dataset.new_data`));
```

BigQuery ML supports multiple model families suitable for different tasks. Below is a quick reference.

| Model family                       | Typical use cases                            | Brief notes / when to choose                         |
| ---------------------------------- | -------------------------------------------- | ---------------------------------------------------- |
| Linear & Logistic Regression       | Regression, binary classification            | Fast, interpretable; good baseline for tabular data  |
| Boosted Tree Models (XGBoost-like) | Complex tabular classification/regression    | Handles non-linearities and interactions well        |
| k-means Clustering                 | Customer segmentation, anomaly grouping      | Unsupervised grouping of similar records             |
| ARIMA\_PLUS (time series)          | Forecasting demand, sales, capacity          | Built-in seasonality & trend modeling                |
| Deep Neural Networks (DNN)         | Complex feature interactions, large datasets | Use when feature richness or nonlinearity demands it |

BigQuery ML provides training, evaluation, and prediction functions directly in SQL, making it straightforward to integrate modeling into existing ETL/ELT pipelines and scheduler systems.

<Frame>
  <img alt="An infographic titled &#x22;Role of ML in Modern Data Engineering&#x22; that outlines key points across three columns: Data-Driven Decisions, ML Integration, and BigQuery ML Advantage. Each column lists brief bullet points about skills, workflows, and benefits (e.g., SQL-based ML, pipeline orchestration, and extracting insights)." />
</Frame>

Summary

* Machine learning on GCP enables data engineers to convert raw data into actionable intelligence without radically changing tooling.
* BigQuery ML is a practical first step: it keeps data in-place, uses SQL, and integrates with production workflows and governance controls.
* As a data engineer you make ML reliable by delivering high-quality features, automating model lifecycle tasks, and operationalizing predictions.

We’ll dive deeper into BigQuery ML for data engineers in the next lesson — covering collaboration patterns with data scientists and production deployment strategies using GCP services.

References and further reading

* [BigQuery ML documentation](https://cloud.google.com/bigquery-ml)
* [Vertex AI overview](https://cloud.google.com/vertex-ai)
* [Google Cloud: Machine Learning solutions](https://cloud.google.com/solutions/machine-learning)

That’s it for this lesson. See you in the next one.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/d3b59481-7d71-43fa-b0d2-f0bd4e263fa4/lesson/06900a3e-8dc1-41b6-8ef8-4b23fb909999" />
</CardGroup>
