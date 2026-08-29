# ML Pipeline

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Machine-Learning-Prerequisites/ML-Pipeline/page

Overview of an end-to-end machine learning pipeline from problem framing through data prep, training, deployment, and monitoring, with Amazon SageMaker tooling for each stage.

This lesson follows a practical, end-to-end machine learning (ML) pipeline: from identifying a business problem to deploying and monitoring a model in production. It also maps each stage to Amazon SageMaker features you can use for development, scalable training, hosting, and monitoring.

## 1. Start with the business problem (and validate that ML is appropriate)

Before any data is collected, define the business question and evaluate whether ML is the right approach. Sometimes deterministic rules or traditional software solve the problem better; in other cases, ML offers cost-effective automation or higher accuracy.

Common business domains and ML motivations:

* Healthcare — automate medical image review when clinician resources are constrained to reduce diagnostic delays.
* Telecommunications — predict customer churn so you can make targeted retention offers before contracts expire.
* Real estate — estimate property prices quickly from structured features when an on-site valuation is impractical.

<Frame>
  <img alt="A presentation slide titled &#x22;ML Project Approach: From Problem to Deployment&#x22; showing three example domains—Healthcare, Telecommunications, and Real Estate—with brief problem statements. The problems note delayed medical scan assessments due to lack of trained staff, high customer churn hurting profitability, and no quick way to estimate property prices without a site visit." />
</Frame>

## 2. Frame the ML task

Translate the business requirement into an ML problem type and confirm that the available data can support it. Below is a quick reference mapping of task types to typical algorithms and example outputs.

| ML Task                   | Typical Output                            | Example Algorithms / Models                                                                        |
| ------------------------- | ----------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Regression                | Numeric value (e.g., house price)         | Linear regression, Random Forest, Gradient Boosting (XGBoost/LightGBM), Neural nets                |
| Classification            | Category or label (binary/multi-class)    | Logistic regression, Decision Trees, XGBoost, Neural nets                                          |
| Image tasks               | Class labels or bounding boxes            | Convolutional Neural Networks (ResNet, EfficientNet), Object detection models (Faster R-CNN, YOLO) |
| Time series / Forecasting | Predicted future values                   | ARIMA, Prophet, LSTM/Transformer models, Gradient boosting on lag features                         |
| NLP                       | Classification, extraction, or generation | Transformer models (BERT, GPT), RNNs, Logistic regression with TF-IDF for simple tasks             |

If the business task is, for example, multi-class medical-scan classification, the problem maps to image classification. Predicting churn is a classification task (often binary). Estimating prices is usually regression.

## 3. Source and prepare data (data engineering)

Data pipelines and reliable data collection are foundational. Roles and responsibilities typically split as:

* Data engineers: build ETL/ELT pipelines, extract from databases/logs/object stores, clean and transform source data, and automate scheduled delivery for training/retraining.
* Data scientists: explore data, create features, prototype models.
* ML engineers: productionize pipelines, training jobs, and serving infrastructure.

Key responsibilities of data engineering:

* Extract data from operational stores, logs, or object storage.
* Normalize/transform formats (e.g., JSON → CSV, Parquet).
* Ensure reproducibility and lineage for training and retraining.

<Frame>
  <img alt="A presentation slide titled &#x22;ML Project Approach: From Problem to Deployment&#x22; showing a left-hand flow from Business problem → ML problem framing → Data collection and preparation. The right panel highlights the Data Engineer role and tasks: creating data pipelines, extracting data from sources, and transforming data (e.g., JSON to CSV)." />
</Frame>

## 4. Feature engineering and exploratory data analysis (EDA)

Data scientists perform EDA and create features that improve model performance. Typical activities:

* Inspect dataset composition, distributions, data types, and missing values.
* Identify correlated or redundant features and reduce dimensionality when appropriate.
* Remove irrelevant or privacy-sensitive columns (PII, account numbers).
* Create derived features (e.g., account\_age\_days from account\_creation\_date).
* Scale or normalize numeric features when magnitudes differ widely.
* Encode categorical variables (one-hot, ordinal, learned embeddings).

Engage domain experts early to validate assumptions and help interpret feature importance.

<Frame>
  <img alt="A presentation slide titled &#x22;ML Project Approach: From Problem to Deployment&#x22; showing a flowchart from business problem → ML problem framing → data collection/preparation → feature engineering. On the right is a &#x22;Data Scientist&#x22; panel listing five tasks: perform EDA, identify correlations, drop irrelevant features, synthesize new features, and scale data." />
</Frame>

## 5. Model training: iterate, evaluate, and choose

Model training tunes parameters (e.g., weights and biases) using optimizers like gradient descent. The process is iterative: test algorithms, adjust features and hyperparameters, and evaluate results.

Important choices during training:

* Algorithm selection (linear models, gradient-boosting, neural nets, etc.).
* Feature set and preprocessing pipeline.
* Hyperparameters (learning rate, epochs, regularization, etc.).

Standard experimental protocol:

* Split data into training, validation, and test sets (example ratios: 70% train / 20% validation / 10% test).
* Train on the training set, tune on validation, measure final performance on the test set.
* Never leak test data into training or hyperparameter tuning.

Iterate when performance is insufficient: collect more data, revise features, or try alternative models. Only move forward when business success criteria are satisfied.

<Frame>
  <img alt="A flowchart titled &#x22;ML Project Approach: From Problem to Deployment&#x22; that outlines steps from business problem and ML problem framing through data collection, feature engineering, model training and evaluation. It ends with a decision node (&#x22;Are business goals met?&#x22;) leading to model testing, deployment, predictions, and monitoring." />
</Frame>

## 6. Data-preparation checklist (practical questions to answer)

When preparing data, explicitly resolve these questions:

* Are all columns relevant or privacy-sensitive? What can be dropped?
* Are features highly correlated or likely to introduce multicollinearity?
* How will you handle missing values (drop, impute, or flag missingness)?
* How will categorical variables be encoded for the chosen algorithms?
* Do numerical features require scaling?

<Frame>
  <img alt="A presentation slide titled &#x22;End-to-End ML Process With Amazon SageMaker&#x22; focusing on Data Preparation, with a spreadsheet icon on the left. On the right is a checklist of questions about column relevance, correlations, missing data handling, categorical-to-numeric transformation, and numerical scaling." />
</Frame>

## 7. Training at scale with Amazon SageMaker

For prototyping, Jupyter notebooks are ideal: they enable EDA, quick experiments, and iterative development. For heavier training workloads, use managed training infrastructure.

How SageMaker helps:

* Prototype locally or in SageMaker notebooks and then submit managed training jobs that run on scalable CPU/GPU instances.
* Use built-in algorithms (XGBoost, Linear Learner, KNN, etc.) or bring your own training code and frameworks.
* Obtain reproducible training artifacts that can be deployed to hosting endpoints.

Typical cycle: select algorithm → engineer features → tune hyperparameters → validate on held-out data.

<Frame>
  <img alt="Slide titled &#x22;End-to-End ML Process With Amazon SageMaker&#x22; showing the Model Training step with two options: Direct Training via a Jupyter Notebook and Delegated Training via a SageMaker Training Job (icons shown)." />
</Frame>

Jupyter notebooks remain central for interactive dev, while SageMaker training jobs provide scalability and reproducibility.

<Frame>
  <img alt="A presentation slide titled &#x22;End-to-End ML Process With Amazon SageMaker&#x22; showing tabs for Data Preparation and Model Training. The center shows a Jupyter icon with a circular workflow labeled Select Algorithm, Engineer Features, Tune Hyperparameters, and Test Accuracy." />
</Frame>

## 8. Deployment and continuous monitoring

When a model artifact meets your success criteria, host it to serve predictions. SageMaker simplifies hosting by deploying your model and inference code into a managed container running behind an endpoint.

Monitoring and lifecycle management:

* Log inference inputs and outputs for auditing and root-cause analysis.
* Compare predictions to ground-truth labels as they become available to measure real performance.
* Detect data and concept drift and trigger alerts or automated retraining pipelines.
* Automate retraining when drift or performance degradation crosses defined thresholds.

<Frame>
  <img alt="A flowchart titled &#x22;End-to-End ML Process With Amazon SageMaker&#x22; showing stages like Data Preparation, Model Training, Model Deployment, and Model Monitoring. It shows New Data feeding a Trained Model, tracking predictions, checking for drift, and either continuing if no drift or retraining the model if drift is found." />
</Frame>

SageMaker supports the complete lifecycle: notebooks for development, managed training jobs for scale, endpoints for low-latency hosting, and monitoring tools for drift detection and pipeline orchestration.

> **lightbulb** Always define success criteria with your business stakeholders before deployment (e.g., target accuracy, acceptable error margins, latency/SLA targets). These criteria decide whether a model is production-ready.

## Summary

* Begin with a clear business problem and validate whether ML is the right solution.
* The ML pipeline is iterative: collect and prepare data, engineer features, experiment with models and hyperparameters, and evaluate on held-out data.
* Production models require monitoring and retraining to address drift and maintain performance.
* Amazon SageMaker provides tools across this pipeline: notebooks, scalable training jobs, managed endpoints, and monitoring capabilities.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary.&#x22; It lists four ML takeaways: ML starts with a business problem, the ML process is iterative, feedback loops are essential, and Amazon SageMaker facilitates the ML pipeline." />
</Frame>

This completes the lesson on the machine learning pipeline. Future lessons will dive deeper into the mathematical foundations and practical SageMaker examples for training and deployment.

## Links and references

* Amazon SageMaker documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* Machine learning basics: [https://developers.google.com/machine-learning/crash-course](https://developers.google.com/machine-learning/crash-course)
* scikit-learn documentation: [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/)
* XGBoost: [https://xgboost.readthedocs.io/](https://xgboost.readthedocs.io/)
* Practical guide to feature engineering: [https://feature-engine.readthedocs.io/](https://feature-engine.readthedocs.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/40da1d46-e900-4426-973b-a9a38c3e505d/lesson/8f1a1144-63aa-4917-b342-32e4279bcb81)
