# Model Evaluation Techniques and Metrics

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/Model-Evaluation-Techniques-and-Metrics/page

Overview of machine learning model evaluation techniques, metrics, validation strategies, and monitoring practices to assess and compare model performance for classification and regression tasks

Evaluation is a critical phase in the machine learning lifecycle that measures how well a model performs on a task and guides decisions about deployment, tuning, or redesign. Effective evaluation compares model predictions to ground truth, quantifies different error types, and helps select the best candidate among multiple models.

<Frame>
  <img alt="The image is a flowchart illustrating the process of inputting data into a model to produce predictions, with the question &#x22;Why Evaluate ML Models?&#x22; It emphasizes that evaluation helps determine a model's performance on a task." />
</Frame>

In practice, we often run the same dataset through several candidate models (for example, Model A and Model B) to produce predictions. Raw predictions are not enough: you must evaluate them against ground truth and compare models using appropriate metrics that reflect your business goals and risk tolerance.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Why Evaluate ML Models?&#x22; showing input data being processed by Model A and Model B, both producing predictions that are then compared for accuracy." />
</Frame>

This comparison reveals which model generalizes better, whether further training or feature engineering is needed, and which candidate is safest for production.

## Confusion Matrix (Classification Diagnostics)

A confusion matrix decomposes binary classification outcomes into four categories:

* True Positive (TP): predicted positive, actual positive
* False Negative (FN): predicted negative, actual positive
* False Positive (FP): predicted positive, actual negative
* True Negative (TN): predicted negative, actual negative

The confusion matrix not only gives overall accuracy but helps identify specific mistakes (e.g., many false positives vs. many false negatives), which is essential when different errors carry different business costs.

<Frame>
  <img alt="The image displays a confusion matrix with categories for true positives (TP), false negatives (FN), false positives (FP), and true negatives (TN), highlighting the correct prediction of the positive class." />
</Frame>

Key classification metrics derived from the confusion matrix:

| Metric                    | Formula                                                | When to prefer                                                |
| ------------------------- | ------------------------------------------------------ | ------------------------------------------------------------- |
| Accuracy                  | `Accuracy = (TP + TN) / (TP + TN + FP + FN)`           | Balanced classes and you need an overall score                |
| Precision                 | `Precision = TP / (TP + FP)`                           | False positives are costly (e.g., fraud alerts)               |
| Recall (Sensitivity, TPR) | `Recall = TP / (TP + FN)`                              | Missing positives is risky (e.g., disease screening)          |
| F1 score                  | `F1 = 2 * (Precision * Recall) / (Precision + Recall)` | Need a balance between precision and recall (imbalanced data) |

* Choose metrics that reflect business priorities: reducing false negatives vs. false positives has different operational consequences.
* For highly imbalanced datasets, avoid relying solely on accuracy.

<Frame>
  <img alt="The image shows three performance metrics—Accuracy, Precision, and Recall (Sensitivity)—along with their respective formulas involving true positives, true negatives, false positives, and false negatives." />
</Frame>

## Receiver Operating Characteristic (ROC) and AUC

An ROC curve evaluates a classifier's ability to separate positive and negative classes across all decision thresholds. It plots:

* y-axis: True Positive Rate (TPR or Recall)
* x-axis: False Positive Rate (FPR)

Formulas:

```text theme={null}
TPR (Recall) = TP / (TP + FN)
FPR = FP / (FP + TN)
```

The Area Under the ROC Curve (AUC-ROC) is a single-number summary: closer to 1.0 is better; 0.5 indicates random performance. Use ROC-AUC to compare classifiers when class distribution remains similar between training and production.

<Frame>
  <img alt="The image displays a Receiver Operating Characteristic (ROC) curve, highlighting an Area Under the Curve (AUC) of 0.90, indicating model performance between true positive and false positive rates." />
</Frame>

Tip: When positive class is rare, consider Precision-Recall curves (AUC-PR) as they can be more informative than ROC.

## Learning Curves (Bias–Variance Diagnosis)

Learning curves plot model performance on training and validation (or cross-validation) sets as a function of training set size. Typical patterns:

* High training score and much lower validation score => overfitting (high variance)
* Both low scores => underfitting (high bias)
* Validation score improves and plateaus as more data is added => model capacity may be adequate

Use learning curves to decide whether adding more data, regularization, or model complexity changes are needed.

<Frame>
  <img alt="The image shows a learning curve graph comparing training accuracy and cross-validation accuracy against the training set size. Each line has a shaded area representing variance or confidence intervals." />
</Frame>

## Regression Metrics (Continuous Targets)

Common metrics for regression tasks include:

```text theme={null}
MAE = (1/n) * Σ |y_i - ŷ_i|

MSE = (1/n) * Σ (y_i - ŷ_i)^2

RMSE = sqrt(MSE)

R^2 = 1 - (Σ (y_i - ŷ_i)^2 / Σ (y_i - ȳ)^2)
```

* MAE: average absolute deviations — robust to outliers compared with MSE.
* MSE: penalizes larger errors more — useful as an optimization objective.
* RMSE: same units as the target — easier to interpret.
* R^2: fraction of variance explained; values near 1 are good, 0 indicates performance equivalent to predicting the mean, and negative values indicate worse than the mean predictor.

<Frame>
  <img alt="The image explains the concept of Mean Squared Error (MSE), including its formula and characteristics, such as penalizing larger errors more and being sensitive to outliers." />
</Frame>

## Validation Strategies (Holdout vs. Cross-Validation)

Holdout Validation:

* Split the dataset into distinct subsets:
  * Training set: \~60–80% — used to train the model.
  * Test set: \~20–40% — used to evaluate final performance.
  * Optional validation set: held out from the training split for hyperparameter tuning.
* Pros: simple and fast; works well on large datasets.
* Cons: higher variance in estimates if dataset is small.

<Frame>
  <img alt="The image illustrates a flowchart of Holdout Validation, showing input data split into a training set (60-80%) to train a model, and a testing set (20-40%) to evaluate the model." />
</Frame>

K-Fold Cross-Validation:

* Split data into `k` folds (commonly `k = 5` or `k = 10`).
* For each fold: train on `k-1` folds and validate on the remaining fold.
* Average metrics across folds for a more robust estimate.
* Reduces evaluation variance and is especially valuable with limited data.

When to choose:

* Holdout: large datasets, need quick iteration.
* Cross-validation: limited data or when you need stable, lower-variance estimates.

<Frame>
  <img alt="The image is a comparison table between Holdout Validation and Cross-Validation, listing differences in simplicity, bias/variance, and data efficiency characteristics." />
</Frame>

## Practical Tooling and Monitoring (AWS)

AWS offers services to help evaluate, monitor, and detect issues in models:

* [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/): capture logs, metrics, and alerts for training jobs and deployed endpoints.
* [Amazon SageMaker Clarify](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify.html): bias detection, feature importance, and dataset imbalance reporting.
* [Amazon SageMaker Training Metrics](https://docs.aws.amazon.com/sagemaker/latest/dg/training-metrics.html): record accuracy, loss, and custom metrics during training.

Use monitoring to detect model drift, data-schema changes, and production performance regressions.

<Callout icon="lightbulb">
  Choose evaluation metrics and validation strategies that match your business goals and the risks of each type of error. For imbalanced problems, prefer precision/recall or AUC-PR and consider cross-validation to get stable estimates.
</Callout>

References and Further Reading

* Scikit-learn: Model evaluation — [https://scikit-learn.org/stable/modules/model\_evaluation.html](https://scikit-learn.org/stable/modules/model_evaluation.html)
* ROC curve and AUC — [https://en.wikipedia.org/wiki/Receiver\_operating\_characteristic](https://en.wikipedia.org/wiki/Receiver_operating_characteristic)
* Amazon SageMaker Clarify — [https://docs.aws.amazon.com/sagemaker/latest/dg/clarify.html](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify.html)
* Amazon CloudWatch — [https://aws.amazon.com/cloudwatch/](https://aws.amazon.com/cloudwatch/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f3f28bdc-5ae5-43bb-85b6-01f7b1bfb71b/lesson/6798b618-5eb8-448a-baa9-f027a7a602fa" />
</CardGroup>
