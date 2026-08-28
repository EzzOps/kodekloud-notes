# load and peek at data
import pandas as pd
df = pd.read_csv("data/train.csv")
df.head()
df.describe()

# split for quick validation
from sklearn.model_selection import train_test_split
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)
```

For visual diagnostics:

```python theme={null}
import seaborn as sns
sns.pairplot(df.sample(500), hue="target")
```

Scikit-learn becomes a productivity multiplier for preprocessing and baseline models — use its transformers to avoid hand-implementing common steps.

<Frame>
  <img alt="A slide titled &#x22;Data Scientist&#x22; showing a workflow from a green user icon to a &#x22;Data Exploration&#x22; box. To the right is a panel with Jupyter and Python logos and a numbered list of tools: Pandas, NumPy, Matplotlib, and Scikit-learn." />
</Frame>

## Feature engineering

Once the dataset is understood, feature engineering prepares inputs for modeling. Common steps:

* Drop non-predictive columns and reduce cardinality where appropriate.
* Convert categorical variables to numeric form (one-hot, ordinal, target encoding, or embeddings).
* Handle missing values (imputation strategies: mean, median, model-based).
* Normalize / standardize numeric features.
* Create derived features (date/time decompositions, feature crosses).
* Reduce dimensionality (feature selection, PCA, or regularization-aware models).

<Callout icon="lightbulb">
  Always confirm the encoding strategy is appropriate for the model and data. For example, one-hot encoding can explode dimensionality for high-cardinality categorical features—consider alternatives like embedding-based approaches or feature hashing in those cases.
</Callout>

<Frame>
  <img alt="A dark-themed slide titled &#x22;Data Scientist&#x22; showing two main tasks—Data Exploration and Feature Engineering—linked from a user icon. To the right it lists responsibilities: transforms data for training, selects relevant features, and formats data appropriately." />
</Frame>

Example: simple preprocessing pipeline with scikit-learn:

```python theme={null}
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

num_cols = ["age", "income"]
cat_cols = ["gender", "region"]

num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

cat_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", num_pipeline, num_cols),
    ("cat", cat_pipeline, cat_cols)
])
```

When datasets have hundreds of features, prioritizing feature selection and dimensionality reduction is essential to avoid overfitting and to improve training convergence.

## Model training, evaluation, and iteration

Data scientists run experiments across algorithms (e.g., XGBoost, LightGBM, or deep learning) and hyperparameters. Each run produces model artifacts and evaluation metrics; when using managed training, artifacts commonly persist to object storage (e.g., Amazon S3).

Standard evaluation patterns:

* Hold-out split (typical: 70% train / 20% validation / 10% test) or cross-validation.
* Monitor validation metrics to compare runs and avoid overfitting.
* Track hyperparameters (learning rate, epochs/rounds, batch size, regularization) and their impact.

Hyperparameter tuning is iterative—automated search (random, grid, Bayesian) is used to find strong configurations efficiently.

<Frame>
  <img alt="An infographic titled &#x22;Data Scientist&#x22; showing a person icon linked to three boxes: Data Exploration, Feature Engineering, and Model Training and Evaluation. To the right it lists responsibilities like choosing algorithms, training models, tuning hyperparameters, and iterating based on results." />
</Frame>

Small example: train a baseline sklearn model and save results:

```python theme={null}
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

X_train = preprocessor.fit_transform(train_df)
y_train = train_df["target"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# evaluate
X_val = preprocessor.transform(val_df)
y_val = val_df["target"]
print("val acc:", accuracy_score(y_val, model.predict(X_val)))

# save locally or upload to managed storage (S3) for later deployment
joblib.dump(model, "model.joblib")
```

Managed platforms provide additional capabilities — automated HPO, distributed training, and profiling/debugging tools — to scale these experiments.

## How Data Scientist tasks map to a managed ML platform

* Hosted, browser-based notebook environments (like SageMaker Studio) let data scientists author and run experiments with managed compute and seamless integrations.
* Model catalogs and prebuilt examples (JumpStart) accelerate prototyping using pre-trained models or templates.
* Managed training jobs provision compute (CPU/GPU), run training, and persist model artifacts to storage (S3).
* Automated hyperparameter optimization services search the configuration space efficiently.
* Training-level debuggers and profilers collect metrics and tensors during training to reveal bottlenecks.

<Frame>
  <img alt="A dark presentation slide titled &#x22;Data Scientist&#x22; showing five numbered cards that list AWS SageMaker components: SageMaker Studio, JumpStart, Training, Hyperparameter Optimization (HPO), and SageMaker Debugger. Each card includes a one-line description of the corresponding feature." />
</Frame>

Tool-to-use mapping (quick reference):

| Resource / Tool              | Use Case                                       | Example                                                                      |
| ---------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------- |
| Jupyter / JupyterLab         | Interactive exploration and notebooks          | [jupyter.org](https://jupyter.org)                                           |
| Pandas                       | Tabular data manipulation and EDA              | `df.describe()`, `df.groupby()`                                              |
| NumPy                        | Efficient numerical ops                        | Vectorized transforms                                                        |
| Matplotlib / Seaborn         | Visualizations and diagnostics                 | `sns.pairplot()`                                                             |
| scikit-learn                 | Preprocessing & baseline models                | Pipelines, transformers, `train_test_split`                                  |
| XGBoost / LightGBM           | Fast tree-based models for tabular data        | [XGBoost](https://xgboost.ai/), [LightGBM](https://lightgbm.readthedocs.io/) |
| Managed training (SageMaker) | Scalable compute for training, artifacts to S3 | [SageMaker Docs](https://docs.aws.amazon.com/sagemaker/latest/dg/)           |

## Personas and collaboration

Three complementary ML personas and their responsibilities:

* Data Engineer: builds repeatable ETL/ELT pipelines, cleans and transforms raw data, and delivers production-ready datasets for downstream modeling.
* Data Scientist: performs exploratory data analysis, feature engineering, model experimentation, and delivers trained models and documented notebooks.
* MLOps Engineer: automates end-to-end ML workflows (CI/CD for models), orchestrates training/deployments, manages model registry/versioning, and ensures safe production releases.

They collaborate closely: data engineers supply clean data; data scientists build and validate models (often with subject-matter experts); MLOps engineers operationalize models into production systems.

<Frame>
  <img alt="A slide titled &#x22;Key Differences in Responsibilities&#x22; showing a comparison table that contrasts Data Engineer, MLOps Engineer, and Data Scientist across aspects like Primary Focus, Output, Collaboration, and Key Deliverables. Each column summarizes each role’s focus (e.g., data pipelines, model deployment, model building), typical outputs, collaborators, and deliverables." />
</Frame>

## Recap

* Data engineers prepare repeatable data extraction and transformation pipelines to deliver clean datasets.
* Data scientists explore data, engineer features, run iterative training experiments with different algorithms and hyperparameters, and produce trained models and documented notebooks.
* MLOps engineers automate, test, version, and deploy models and pipelines for production usage.

This lesson mapped common managed ML platform features (notebooks, managed training, HPO, debugger) to the data scientist persona. Next, we'll cover what defines a managed service and how such platforms behave operationally.

## References and further reading

* Jupyter: [https://jupyter.org](https://jupyter.org)
* pandas documentation: [https://pandas.pydata.org/](https://pandas.pydata.org/)
* scikit-learn: [https://scikit-learn.org/](https://scikit-learn.org/)
* XGBoost: [https://xgboost.ai/](https://xgboost.ai/)
* LightGBM: [https://lightgbm.readthedocs.io/](https://lightgbm.readthedocs.io/)
* Amazon SageMaker docs: [https://docs.aws.amazon.com/sagemaker/latest/dg/](https://docs.aws.amazon.com/sagemaker/latest/dg/)
* Amazon S3 docs: [https://docs.aws.amazon.com/s3/index.html](https://docs.aws.amazon.com/s3/index.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/40da1d46-e900-4426-973b-a9a38c3e505d/lesson/a7f9edf9-0c01-497c-9e9f-cff67833f6a4" />
</CardGroup>


# Why Learn SageMaker by Persona

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Machine-Learning-Prerequisites/Why-Learn-SageMaker-by-Persona/page

Explains how to map Amazon SageMaker capabilities to Data Engineer, Data Scientist, and MLOps personas for reproducible, automated ML workflows, governance, deployment, monitoring, and CI CD

In this lesson we examine why it’s helpful to approach Amazon SageMaker by persona. Mapping SageMaker features to the activities different people perform in the ML lifecycle clarifies responsibilities and shows how each capability fits into real workflows: data preparation, training, deployment, and monitoring. We focus on three common personas—Data Engineer, Data Scientist, and MLOps Engineer—and explain which SageMaker tools each persona typically uses.

SageMaker can be used via the point-and-click Console or via the SageMaker SDK for Python (a code-first workflow). For reproducibility, version control, and automation—critical in production—we strongly recommend the code-first approach (typically from a Jupyter or JupyterLab environment).

<Callout icon="lightbulb">
  Prefer a code-first workflow using the SageMaker SDK from a notebook (Jupyter / JupyterLab) for reproducible, versioned, and automatable ML work. The Console is useful for exploration and quick experiments, but production-grade pipelines benefit from code, CI/CD, and infrastructure-as-code.
</Callout>

We summarize the three personas and their high-level responsibilities next:

<Frame>
  <img alt="A presentation slide titled &#x22;Personas – Introduction&#x22; listing three roles: Data Engineer, MLOps Engineer, and Data Scientist. Each role has bullet points summarizing responsibilities (data warehousing/ETL, ML pipelines/CI‑CD/versioning, and experimentation/feature engineering/training/inference)." />
</Frame>

|        Persona | Primary Focus                                 | Typical Responsibilities                                                                                      |
| -------------: | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
|  Data Engineer | Data ingestion, transformation, governance    | Build repeatable ETL/ELT pipelines, ensure PII / encryption / access controls, stage data in S3 or data lakes |
| Data Scientist | Experimentation and model development         | Feature engineering, training experiments, hyperparameter tuning, notebook-driven workflow                    |
| MLOps Engineer | Productionization, automation, and monitoring | CI/CD for models, model registry, deployment, autoscaling, drift detection, governance and traceability       |

Now we’ll examine each persona in detail and list the SageMaker capabilities they commonly use.

## Data Engineer

Data Engineers locate, ingest, and transform source data so it becomes reliable training data. Sources include relational databases (MySQL, PostgreSQL, SQL Server, Oracle) and non-relational stores (DynamoDB, MongoDB, Redis). Ingestion can be ad hoc exports for experimentation or fully automated pipelines for production retraining.

Transformations often required before training:

* Select relevant columns and types.
* Aggregate records or compute rolling statistics.
* Remove or obfuscate personally identifiable information (PII).
* Reformat to efficient columnar formats (Parquet) for large-scale training.

Amazon S3 is the common staging area for semi-structured datasets (CSV, Parquet, JSON). Data Engineers must apply governance (PII handling, encryption, IAM controls) before exposing datasets for model training or feature production.

<Frame>
  <img alt="A dark presentation slide titled &#x22;Data Engineer&#x22; with an icon of a table and padlock and the text: &#x22;Governance/Privacy constraints may require obfuscating or dropping parts of the source data.&#x22; A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom corner." />
</Frame>

In smaller teams, Data Scientists may perform extraction and preprocessing manually from notebooks. In larger organizations, Data Engineers design automated pipelines (Python scripts, orchestration tools, or AWS services like AWS Glue) to ensure fresh, consistent, and governed datasets are available for training and inference.

<Frame>
  <img alt="A slide titled &#x22;Data Engineer&#x22; comparing small organizations (where a data scientist handles data extraction and transformation manually) with large enterprises (where a data engineer builds an automated pipeline to ingest and transform training data)." />
</Frame>

Key SageMaker tools for Data Engineers:

* Data Wrangler: low-code visual transformations and repeatable ETL-like flows.
* SageMaker Processing: run scalable Spark or Python processing jobs outside notebooks.
* SageMaker Feature Store: persist and serve engineered features to ensure consistency across training and inference.
* SageMaker Pipelines: orchestrate extract/transform/load and handoffs into training/validation stages.

<Frame>
  <img alt="A slide titled &#x22;Data Engineer&#x22; showing four numbered SageMaker components—01 Data Wrangler, 02 SageMaker Processing, 03 SageMaker Feature Store, and 04 SageMaker Pipelines—with brief descriptions of each." />
</Frame>

## MLOps Engineer

MLOps Engineers focus on safely getting models from experiments into production and keeping them reliable, performant, and compliant. Their responsibilities span deployment, autoscaling, lifecycle automation, monitoring, and governance.

Core MLOps responsibilities:

* Design CI/CD pipelines that test code and data, run training, register models, and gate deployments.
* Manage a model registry for versioning artifacts and controlling approvals.
* Deploy models (SageMaker Endpoints or other hosting) with autoscaling, A/B/blue-green strategies, and rollback mechanisms.
* Monitor production models for performance drift, data drift, latency, fairness, and explainability; trigger retraining when necessary.
* Maintain lineage and traceability: which code, dataset, algorithm, and model created a prediction.

<Frame>
  <img alt="A slide titled &#x22;MLOps Engineer&#x22; that lists key governance responsibilities. The four boxes say: enforces governance policies across the ML pipeline; ensures traceability of models, datasets, and code versions; automates compliance checks in CI/CD; and monitors deployed models for drift, fairness, and explainability." />
</Frame>

MLOps best practices mirror DevOps: keep source code in Git, trigger pipelines on commits (linting, unit tests, security scans), and use automation to reduce manual risk. With ML, versioning applies both to code and to model artifacts/metadata (model registry).

An organization may include a compliance or governance officer who approves models for production. SageMaker Model Registry supports staged approvals (Pending → Approved/Rejected), enabling explicit sign-off for regulated environments.

<Frame>
  <img alt="An MLOps Engineer slide describing the Compliance Officer role in highly regulated environments. It lists three responsibilities: ensuring ML pipeline alignment with policies, approving or rejecting models for deployment, and monitoring ethical and legal compliance." />
</Frame>

SageMaker features commonly used by MLOps engineers:

* Model Registry: version models and manage approval workflows.
* SageMaker Pipelines: orchestrate training, validation, registration, and deployment steps.
* Endpoint deployment: host models for real-time inference (or integrate with other hosting).
* Model Monitor: continuously detect data or prediction drift and anomalies.
* SageMaker Clarify: run bias detection and explainability analyses during training and inference.

<Frame>
  <img alt="A slide titled &#x22;MLOps Engineer&#x22; showing five numbered SageMaker components—Model Registry, Pipelines, Endpoint Deployment, Model Monitor, and Clarify—each with a short description of its role." />
</Frame>

## Governance, Lineage, and Explainability

Governance must be enforced across the entire ML lifecycle—from data ingestion to deployment. Lineage is essential: for any prediction you should be able to trace the dataset, model version, training code, and algorithm that produced it. Capturing lineage enables reproducibility, auditing, and regulatory compliance.

Explainability and fairness are critical in regulated or high-stakes domains (finance, healthcare, hiring). Use tools like SageMaker Clarify to run bias detection and produce explainability reports. Model Monitor and telemetry help detect drift in input distributions or prediction quality; pipelines can automatically kick off retraining and redeployment when thresholds are breached.

<Callout icon="warning">
  Enforce governance and automated checks (data validation, fairness tests, security scans, lineage capture) inside CI/CD pipelines. Manual changes are a frequent source of risk—automation reduces errors and improves auditability.
</Callout>

Automation is central: build checks into pipelines so security, data-quality, and fairness tests run whenever code or data changes. When checks pass and approvals are granted, deployment steps proceed as defined—minimizing manual intervention and improving traceability.

***

By mapping SageMaker capabilities to the roles that use them, teams can design secure, repeatable ML workflows that support rapid experimentation and robust production operations.

## Links and references

* Amazon SageMaker documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* Amazon S3 overview: [https://docs.aws.amazon.com/s3/index.html](https://docs.aws.amazon.com/s3/index.html)
* SageMaker Clarify: [https://docs.aws.amazon.com/sagemaker/latest/dg/clarify.html](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify.html)
* SageMaker Pipelines: [https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html)
* SageMaker Model Monitor: [https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html)
* SageMaker Feature Store: [https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html)
* Data Wrangler: [https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html](https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html)
* SageMaker Processing: [https://docs.aws.amazon.com/sagemaker/latest/dg/processing.html](https://docs.aws.amazon.com/sagemaker/latest/dg/processing.html)
* [AWS CodePipeline (CI/CD Pipeline)](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline)
* [Amazon Simple Storage Service (Amazon S3)](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [Fundamentals of DevOps](https://learn.kodekloud.com/user/courses/fundamentals-of-devops)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/40da1d46-e900-4426-973b-a9a38c3e505d/lesson/6b3a27fe-3131-4617-befa-bec0c96747a7" />
</CardGroup>
