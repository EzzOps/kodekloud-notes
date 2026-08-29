# BigQuery ML Workflow

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Machine-Learning-Options/BigQuery-ML-Workflow/page

Describes a BigQuery ML SQL workflow to create train evaluate and predict models with hyperparameter tuning metrics and production deployment guidance

Hello and welcome back.

In this lesson we'll explore a practical and efficient BigQuery ML workflow. You'll see how to create, train, evaluate, and use models entirely with SQL inside BigQuery. This workflow is ideal for analysts and data engineers who want to keep modeling close to their data without moving large datasets.

Here is the BigQuery ML workflow we will follow step by step.

We start with CREATE MODEL. Here you declare the model name, type (for example, regression or classification), and supply the SELECT query that provides features and labels. Choosing relevant features is critical because they determine what the model learns.

Next is model training. BigQuery automatically runs training when you execute CREATE MODEL. BigQuery ML supports automated hyperparameter tuning for many built-in model types (for example via the `search_trials` option), so manual tuning is often unnecessary.

After training, evaluate the model with ML.EVALUATE. This returns performance metrics—accuracy, precision/recall for classification, mean squared error for regression, and other useful diagnostics. If the metrics are unsatisfactory, iterate: refine features or data and retrain.

Finally, use ML.PREDICT to generate batch predictions on new data. For online (real-time) prediction, export the trained model for serving in a system such as [Vertex AI](https://cloud.google.com/vertex-ai). The workflow is cyclical: create → train → evaluate → predict, and repeat as you collect more data or adjust features.

<Frame>
  <img alt="A BigQuery ML workflow diagram with four colored sequential boxes labeled Create Model, Model Training, ML.EVALUATE, and ML.PREDICT. Each box includes short notes about defining training data and parameters, automatic training and hyperparameter tuning, model performance/metrics, and making batch or real-time predictions." />
</Frame>

## 1. CREATE MODEL — define and train

The CREATE MODEL statement both defines and (by default) trains the model. Specify the model identifier, chosen `OPTIONS` (for example, `model_type`), and a SELECT query that returns training examples with features and the target label.

> **lightbulb** If you know SQL, you already understand most of BigQuery ML: you declare the model name, set options, and provide a training query. BigQuery handles training and optional hyperparameter tuning.

Example: create a linear regression model

```sql theme={null}
CREATE MODEL `project.dataset.model_name`
OPTIONS(model_type='linear_reg') AS
SELECT
  feature1,
  feature2,
  target
FROM `project.dataset.training_data`;
```

Notes:

* `project.dataset.model_name`: destination model identifier in BigQuery.
* `OPTIONS(model_type='linear_reg')`: chooses a built-in model type. Other options include `logistic_reg`, `boosted_trees_classification`, `boosted_trees_regression`, `dnn_classifier`, etc.
* The SELECT statement supplies training rows. Include feature columns and the label column.

Tip: you can control hyperparameter tuning with options such as `search_trials` and configure input preprocessing with `input_label_cols`, `data_split_method`, and other model-specific options.

## Common BigQuery ML model types

| Model Type                     | Use Case                         | Notes                                     |
| ------------------------------ | -------------------------------- | ----------------------------------------- |
| `linear_reg`                   | Regression (continuous target)   | Fast, interpretable baseline              |
| `logistic_reg`                 | Binary classification            | Simple probability estimates              |
| `boosted_trees_classification` | Classification with tabular data | Handles nonlinearities and interactions   |
| `boosted_trees_regression`     | Regression with tabular data     | Strong performance on structured features |
| `dnn_classifier`               | High-dim / complex patterns      | Requires more data and tuning             |

## 2. ML.EVALUATE — inspect model performance

After training, run ML.EVALUATE to compute metrics on a held-out evaluation dataset. Pass the model identifier and a query that returns the same features plus the true target.

Example: evaluate the model

```sql theme={null}
SELECT *
FROM ML.EVALUATE(
  MODEL `project.dataset.model_name`,
  (
    SELECT
      feature1,
      feature2,
      target
    FROM `project.dataset.eval_data`
  )
);
```

What ML.EVALUATE returns:

* For classification: accuracy, precision, recall, AUC, and confusion matrix details.
* For regression: mean squared error (MSE), mean absolute error (MAE), and explained variance.
* Additional model-specific diagnostics may be available (e.g., feature importance for tree models).

Best practice: always evaluate on a dataset that was not used for training (a validation or test split). You can split data using SQL (for example, `WHERE RAND() < 0.8` for training and `>= 0.8` for evaluation) or use BigQuery ML's built-in `data_split_method`.

## 3. ML.PREDICT — generate predictions

Use ML.PREDICT to make batch predictions. It returns the input features plus predicted values (and class probabilities for classification models).

Example: predict using the model

```sql theme={null}
SELECT *
FROM ML.PREDICT(
  MODEL `project.dataset.model_name`,
  (
    SELECT
      feature1,
      feature2
    FROM `project.dataset.new_data`
  )
);
```

Output:

* Regression models return predicted numeric values in `predicted_<label>`.
* Classification models return predicted class and probabilities (for example, `predicted_label`, `probability`).

For production real-time serving, export the model to a serving platform (for example, [Vertex AI Prediction](https://cloud.google.com/vertex-ai/docs/predictions)), or use BigQuery ML's REST APIs where appropriate.

## Putting it all together

* CREATE MODEL: defines and trains using a SELECT query.
* ML.EVALUATE: returns metrics to judge model quality.
* ML.PREDICT: generates predictions for new inputs.

This loop—create → train → evaluate → predict—is straightforward in BigQuery ML and keeps modeling close to your data.

> **warning** Be mindful of query and training costs: BigQuery charges for processed bytes and model training. Use appropriate data sampling, partitioning, and test splits to control cost. For online serving, plan model export and monitoring (latency, payload size, and versioning).

## Production considerations and next steps

* Prepare stable training and validation datasets, maintain data versioning, and log model metrics.
* Monitor model drift: schedule periodic evaluation and retraining as data distribution changes.
* For large-scale or low-latency serving, export models to a serving platform (for example, Vertex AI) and implement A/B tests and model promotion workflows.

## Links and references

* [BigQuery ML documentation](https://cloud.google.com/bigquery-ml/docs)
* [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)
* [BigQuery pricing](https://cloud.google.com/bigquery/pricing)

Further material will cover designing an optimal BigQuery ML workflow for production: preparing training and validation datasets, monitoring, and interview-focused considerations.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/d3b59481-7d71-43fa-b0d2-f0bd4e263fa4/lesson/c4fec3eb-6f9b-494d-b45e-be607696034d)
