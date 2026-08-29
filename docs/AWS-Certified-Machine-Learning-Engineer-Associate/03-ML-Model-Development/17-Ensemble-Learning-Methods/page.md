# 1) Create a model (example container and model data)
aws sagemaker create-model \
  --model-name my-jumpstart-model \
  --primary-container Image=123456789012.dkr.ecr.us-west-2.amazonaws.com/my-container:latest,ModelDataUrl=s3://my-bucket/model.tar.gz \
  --execution-role-arn arn:aws:iam::123456789012:role/SageMakerExecutionRole

# 2) Create an endpoint configuration
aws sagemaker create-endpoint-config \
  --endpoint-config-name my-endpoint-config \
  --production-variants VariantName=AllTraffic,ModelName=my-jumpstart-model,InitialInstanceCount=1,InstanceType=ml.m5.large

# 3) Create the endpoint
aws sagemaker create-endpoint \
  --endpoint-name my-model-endpoint \
  --endpoint-config-name my-endpoint-config
```

> **lightbulb** Tip: Update the execution role to include `s3:GetObject` / `s3:PutObject` if you plan to import datasets, save checkpoints, or store evaluation outputs in S3.

> **warning** Warning: Real-time endpoints (especially with larger instances or multiple replicas) incur ongoing hourly charges. Delete endpoints when they are no longer needed to avoid unexpected costs.

## Links and References

* Amazon SageMaker JumpStart documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jumpstart.html](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jumpstart.html)
* Amazon SageMaker Studio overview: [https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html)
* SageMaker instance types: [https://docs.aws.amazon.com/sagemaker/latest/dg/instance-types.html](https://docs.aws.amazon.com/sagemaker/latest/dg/instance-types.html)
* Amazon S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f3f28bdc-5ae5-43bb-85b6-01f7b1bfb71b/lesson/b10c20e1-3622-4a72-8761-0d2daa8dfadb)


# Ensemble Learning Methods

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/Ensemble-Learning-Methods/page

Overview of ensemble learning methods—bagging, boosting, and stacking— their principles, advantages, and practical examples for improving model accuracy, robustness, and generalization

Ensemble learning refers to a family of machine learning techniques that combine multiple models—called base learners or weak learners—to produce a single, stronger predictor. Rather than relying on one model, ensembles aggregate complementary strengths across models to improve accuracy, robustness, and generalization.

Why ensembles work (detailed)

* Error reduction: Individual models incur bias (systematic errors) and variance (sensitivity to data noise). Aggregating multiple models reduces random errors because mistakes often cancel out when averaged or voted upon.
* Diversity of models: Different model architectures and training samples capture different data patterns. When base learners are diverse (i.e., they make different errors), combining them improves reliability.
* Bias–variance trade-off: Ensembles can lower variance by averaging many models while keeping bias in check, improving performance on unseen data.
* Robustness: Outliers or unusual inputs rarely fool all models simultaneously; ensembles reduce single-model brittleness.
* Wisdom of the crowd: Aggregating multiple independent estimators tends to outperform a single expert model when errors are not perfectly correlated.

<Frame>
  <img alt="The image explains five reasons why ensembles work in machine learning: error reduction, diversity of models, bias-variance tradeoff, robustness, and wisdom of the crowd (intuition)." />
</Frame>

Common ensemble strategies include bagging, boosting, and stacking. Each uses different techniques to create diversity and to combine base learners.

## Bagging (Bootstrap Aggregating)

Bagging builds several base learners in parallel using bootstrap samples of the training set (samples drawn with replacement). Each model is trained independently on its own sample and predictions are aggregated—by majority vote for classification or averaging for regression.

Key points:

* Creates diverse training sets using bootstrap sampling.
* Trains base learners in parallel, so it scales efficiently.
* Primarily reduces variance and helps prevent overfitting.
* Random Forest extends bagging by adding feature randomness (selecting a random subset of features per split) to further decorrelate trees.

<Frame>
  <img alt="The image is a flowchart depicting the bagging process, where input data is used to train multiple models on random subsets, aggregate their predictions, and produce final predictions." />
</Frame>

The aggregated prediction from multiple base learners is usually more stable and accurate than any single learner.

Random Forest example (bagging variant)

* Input data is resampled to create multiple datasets.
* Each dataset trains a separate decision tree.
* Each tree yields an output (e.g., prediction A, prediction B, prediction C).
* Final prediction is produced by majority voting (classification) or averaging (regression).

Example: Scikit-learn RandomForestClassifier (Python)

```python theme={null}
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)
rf.fit(X_train, y_train)
preds = rf.predict(X_test)
```

## Boosting

Boosting trains base learners sequentially. Each subsequent model focuses on the errors of the previous models, increasing the importance of mispredicted instances. The ensemble prediction is a weighted combination of all learners.

Key points:

* Models are built in sequence and each corrects previous errors.
* Often framed as stage-wise optimization of a differentiable loss (e.g., gradient boosting).
* Typically reduces bias and can achieve very high accuracy, but requires careful regularization to avoid overfitting.

<Frame>
  <img alt="The image illustrates a &#x22;Boosting Overview,&#x22; showing a flow from input data to a model, which corrects errors and produces predictions. The process involves subsequent model steps for further error correction." />
</Frame>

Popular boosting algorithms:

* AdaBoost: Reweights training instances to emphasize previously misclassified samples.
* Gradient Boosting: Adds learners that minimize residual error by optimizing a loss function stage-wise.
* XGBoost: A highly optimized and regularized implementation of gradient boosting with efficient handling of sparse data and parallelism.
* LightGBM: Designed for speed and low memory usage; uses histogram-based techniques and leaf-wise tree growth.

<Frame>
  <img alt="The image lists popular boosting algorithms: AdaBoost, Gradient Boosting, XGBoost, and LightGBM, each with brief descriptions of their features or advantages." />
</Frame>

In boosting (for example, XGBoost), decision trees are trained sequentially; each new tree focuses on correcting the residuals of the ensemble so far. Stage-wise weighted outputs are summed to form the final prediction.

Example: XGBoost (Python)

```python theme={null}
import xgboost as xgb
dtrain = xgb.DMatrix(X_train, label=y_train)
param = {"objective": "binary:logistic", "max_depth": 6, "eta": 0.1}
bst = xgb.train(param, dtrain, num_boost_round=100)
preds = bst.predict(xgb.DMatrix(X_test))
```

## Stacking (Stacked Generalization)

Stacking constructs a two-level model: several different base models (e.g., tree-based, linear, neural) are trained on the same data, and a meta-model (blender) is trained to combine their predictions. The meta-model learns how to weight and correct base model outputs for improved ensemble performance.

Key best practices:

* Use out-of-fold (cross-validated) predictions from base models to train the meta-model to prevent information leakage.
* Choose diverse base models to maximize complementary strengths.
* Keep the meta-model relatively simple to avoid overfitting on the meta-level dataset.

<Frame>
  <img alt="The image illustrates a stacking overview in machine learning, where input data is processed through multiple models to generate outputs combined by a meta-model to produce final predictions." />
</Frame>

> **warning** When implementing stacking, always use out-of-fold predictions from base models to train the meta-model. Training the meta-model on predictions from base models made on the same data those base models were trained on introduces target leakage and results in overly optimistic performance estimates.

## Summary comparison (high-level)

* Bagging
  * Training: Parallel on bootstrap samples
  * Best for: Reducing variance
  * Examples: Random Forest
  * Aggregation: Majority vote or averaging

* Boosting
  * Training: Sequential, each model focuses on previous errors
  * Best for: Reducing bias and maximizing accuracy
  * Examples: AdaBoost, Gradient Boosting, XGBoost, LightGBM
  * Aggregation: Weighted sum of learners

* Stacking
  * Training: Multiple diverse base models + meta-model
  * Best for: Combining heterogeneous models for incremental gains
  * Requirements: Careful cross-validation (out-of-fold predictions) to avoid overfitting

| Ensemble Type | Training Strategy                          | Typical Use Case                     | Pros                                    | Cons                                                |
| ------------- | ------------------------------------------ | ------------------------------------ | --------------------------------------- | --------------------------------------------------- |
| Bagging       | Parallel on bootstrap samples              | Reduce variance, prevent overfitting | Simple, parallelizable, robust          | Limited bias reduction                              |
| Boosting      | Sequential, focus on residuals             | Improve accuracy, reduce bias        | High accuracy, handles complex patterns | Can overfit; needs regularization                   |
| Stacking      | Train diverse base models, then meta-model | Combine heterogeneous strengths      | Flexible, can yield best performance    | Complex; risk of information leakage without OOF CV |

> **lightbulb** Choose an ensemble strategy based on your problem: use bagging to reduce variance, boosting to reduce bias and maximize accuracy, and stacking to combine diverse models for possible incremental performance gains. Validate thoroughly (cross-validation, holdout sets) and tune regularization to prevent overfitting.

## Further reading and references

* [Scikit-learn Ensemble Methods](https://scikit-learn.org/stable/modules/ensemble.html)
* [XGBoost Documentation](https://xgboost.readthedocs.io/)
* [LightGBM Documentation](https://lightgbm.readthedocs.io/)
* [Kaggle: Ensemble Learning Guides and Competitions](https://www.kaggle.com/)

These resources provide implementation details, advanced hyperparameter tuning strategies, and practical examples for applying ensemble methods to real-world problems.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f3f28bdc-5ae5-43bb-85b6-01f7b1bfb71b/lesson/81b62de3-ca61-470e-bea9-6945d474d8d0)
