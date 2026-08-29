# X, y = your dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# L2 regularization (Ridge)
ridge = Ridge(alpha=1.0)  # alpha scales the L2 penalty (λ)
ridge.fit(X_train, y_train)
y_pred_ridge = ridge.predict(X_test)
print("Ridge MSE:", mean_squared_error(y_test, y_pred_ridge))

# L1 regularization (Lasso)
lasso = Lasso(alpha=0.1)  # alpha scales the L1 penalty
lasso.fit(X_train, y_train)
y_pred_lasso = lasso.predict(X_test)
print("Lasso MSE:", mean_squared_error(y_test, y_pred_lasso))
```

Regularization beyond linear models

* Dropout (deep learning): randomly disables a subset of neurons during each training step, preventing co-adaptation and reducing overfitting.

<Frame>
  <img alt="The image illustrates the dropout technique in neural networks, showing network nodes before and after dropout is applied, with some nodes randomly deactivated to prevent co-adaptation." />
</Frame>

* Early stopping: track validation loss or metrics and stop training when improvement stalls to prevent overfitting from excessive epochs.
* Data augmentation (images): artificially expand training data with random transforms — flips, rotations, crops, brightness/gamma changes — to improve model robustness.

Applying regularization in AWS SageMaker
AWS SageMaker built-in algorithms and frameworks expose hyperparameters for common regularization techniques. Use these to control model capacity and generalization when training at scale.

* Linear Learner supports both L1 and L2:
  * L1: absolute weight penalty, useful for sparsity and feature selection.
  * L2: squared weight penalty, shrinks coefficients to reduce variance.

<Frame>
  <img alt="The image is a slide titled &#x22;Applying Regularization in SageMaker&#x22; describing L1 regularization, which adds an absolute weight penalty, creates sparse models, and is beneficial for feature selection." />
</Frame>

Example: Linear Learner via the SageMaker SDK

```python theme={null}
from sagemaker import LinearLearner

linear = LinearLearner(
    role='SageMakerRole',
    instance_count=1,
    instance_type='ml.m5.large',
    predictor_type='binary_classifier',
    l1=0.01,   # L1 regularization strength
    l2=0.1,    # L2 regularization strength
    epochs=20
)
```

XGBoost regularization parameters (summary)

|   Parameter | Meaning                            | Typical effect                             |
| ----------: | ---------------------------------- | ------------------------------------------ |
|     `alpha` | L1 regularization term on weights  | Encourages sparsity in leaf weights        |
|    `lambda` | L2 regularization term on weights  | Shrinks leaf weights to reduce overfitting |
|     `gamma` | Minimum loss reduction for a split | Controls how easily new splits are created |
| `max_depth` | Maximum tree depth                 | Direct control of model complexity         |

Example: XGBoost estimator in SageMaker

```python theme={null}
import sagemaker

region = sagemaker.Session().boto_region_name
role = "SageMakerRole"

xgboost = sagemaker.estimator.Estimator(
    image_uri=sagemaker.image_uris.retrieve("xgboost", region, version="1.3-1"),
    role=role,
    instance_count=1,
    instance_type='ml.m5.large',
    hyperparameters={
        "objective": "binary:logistic",
        "alpha": 0.5,   # L1 regularization
        "lambda": 1.0,  # L2 regularization (note: key is a string)
        "gamma": 0,
        "max_depth": 6
    }
)
```

Other regularization-related training knobs in SageMaker and deep learning:

* `weight_decay`: commonly used for L2 regularization.
* `num_layers`: increasing layers raises capacity and overfitting risk.
* `mini_batch_size`: affects gradient estimates and training stability.
* `epochs`: more epochs increase risk of overfitting (use early stopping).
* `learning_rate`: impacts optimization dynamics; lower rates can act like a regularizer.

ResNet-based image classification example (SageMaker built-in image classifier)

* `weight_decay` implements L2 regularization.
* `learning_rate` controls the optimizer behavior (not a regularization parameter, but relevant to convergence).

```python theme={null}
image_classifier.set_hyperparameters(
    num_layers=18,
    use_pretrained_model=1,
    image_shape='3,224,224',
    num_classes=2,
    mini_batch_size=32,
    epochs=10,
    learning_rate=0.001,  # optimizer learning rate (not L2)
    weight_decay=0.0001,  # L2 regularization (weight decay)
    top_k=2
)
```

Tuning regularization strengths

* Use automated hyperparameter tuning (AWS SageMaker Automatic Model Tuning or other HPO frameworks) to search for optimal values of `alpha`, `lambda`, `weight_decay`, dropout rate, etc.
* Start with reasonable defaults and sweep logarithmically (e.g., `1e-4` to `1e0`) for penalty strengths.

> **lightbulb** When supplying XGBoost hyperparameters in a Python dict, use string keys for parameters like `"lambda"` because `lambda` is a reserved keyword in Python. For example: `{"lambda": 1.0}`.

Further reading and references

* [Scikit-learn documentation](https://scikit-learn.org/stable/)
* [XGBoost documentation](https://xgboost.readthedocs.io/en/latest/)
* [ResNet paper (He et al.)](https://arxiv.org/abs/1512.03385)
* AWS SageMaker resources and tutorials: [SageMaker documentation](https://aws.amazon.com/sagemaker/)

Use regularization as part of a broader model-validation strategy: combine cross-validation, monitoring of validation metrics, early stopping, and automated tuning to achieve robust models that generalize well.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f3f28bdc-5ae5-43bb-85b6-01f7b1bfb71b/lesson/d0bf73a9-46c3-4f93-8720-618a63734587)


# SageMaker Built in Algorithms

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/SageMaker-Built-in-Algorithms/page

Overview of Amazon SageMaker built-in algorithms, their use cases, supported data types, benefits, and example usage for scalable training, model families like tabular, NLP, vision, time-series, and unsupervised

Amazon SageMaker provides a suite of built-in algorithms that are pre-packaged in containers and optimized for scalable training. These algorithms let you focus on preparing data and choosing hyperparameters while SageMaker manages dependencies, distributed training, and infrastructure. They support multiple input modes (file and pipe) and are suitable for tabular, text (NLP), image (vision), unsupervised, and time-series problems. You can launch them programmatically from the SageMaker SDK or from the console, and they integrate with other SageMaker services like Pipelines and Clarify.

<Frame>
  <img alt="The image is an introduction slide about Amazon SageMaker's built-in algorithms, highlighting features like being prebuilt and containerized, optimized for performance, scalable training, flexible data input, and wide use cases." />
</Frame>

What are foundation models?

Foundation models are very large, general-purpose neural networks trained on broad, diverse datasets. They provide high-quality base capabilities (for example, language understanding or image feature extraction) and can be fine-tuned for downstream tasks such as classification, summarization, retrieval, or question answering.

Why use SageMaker built-in algorithms?

* Reduce engineering overhead: no custom low-level training loop required for many common tasks.
* Optimized performance: containers are tuned for distributed training and production-ready performance.
* Easy to launch: accessible via the SageMaker SDK or the AWS console for fast experimentation.
* Scalable: run across multiple instances, GPUs, or CPUs for larger datasets and faster training.
* Ecosystem integration: works with [SageMaker Pipelines](https://aws.amazon.com/sagemaker/pipelines/) for CI/CD and [SageMaker Clarify](https://aws.amazon.com/sagemaker/clarify/) for bias and explainability.

<Frame>
  <img alt="The image outlines five benefits of using built-in algorithms, including no need to write training code, optimized performance, ease of use with SDK or console, scalability, and integration with SageMaker Pipelines and Clarify." />
</Frame>

These integrations simplify end-to-end ML workflows and improve transparency and monitoring for trained models.

Supported data types and algorithm families

You will commonly find built-in algorithms that address the following categories: tabular, text (NLP), time series, unsupervised learning, and vision. Each family targets specific input formats and use cases.

Tabular ML

Tabular (structured) data is organized in rows and columns—like CSV, SQL tables, or spreadsheet files. Typical tabular use cases include customer segmentation, fraud detection, and churn prediction. SageMaker includes efficient algorithms for regression, classification, ranking, and embeddings for categorical features.

<Frame>
  <img alt="The image outlines types of machine learning algorithms that work with tabular data, highlighting use cases such as customer segmentation, fraud detection, and churn prediction. It mentions the use of structured data organized in rows and columns, like CSV files, SQL tables, and Excel sheets." />
</Frame>

Common tabular algorithms in SageMaker:

* Linear Learner — classification and regression with linear models.
* XGBoost — gradient-boosted decision trees (classification/regression).
* Factorization Machines — effective for sparse features and recommendation systems.
* K-Nearest Neighbors (KNN) — instance-based classification and regression for small/medium datasets.
* Object2Vec — learn embeddings for categorical and tabular features.

<Frame>
  <img alt="The image lists four types of machine learning algorithms for tabular data: Linear Learner, XGBoost, Factorization Machines, and K-Nearest Neighbors (KNN), each with a brief description of their use cases." />
</Frame>

Text (NLP)

Text-based ML handles unstructured natural language data: emails, reviews, articles, and social media. Use cases include sentiment analysis, document classification, spam detection, translation, and summarization. SageMaker offers built-in algorithms and JumpStart models for many NLP tasks.

<Frame>
  <img alt="The image is a diagram showcasing types of machine learning algorithms for text, highlighting use cases such as document classification, sentiment analysis, and spam detection, with examples including emails, reviews, news articles, and tweets." />
</Frame>

Text algorithms and approaches:

* BlazingText — fast word2vec-style embeddings and text classification.
* Sequence-to-sequence models — translation and abstractive summarization.
* BERT-based classifiers — available via [Amazon SageMaker JumpStart](https://aws.amazon.com/sagemaker/jumpstart/).
* LDA — topic modeling for unsupervised text clustering.
* Object2Vec — embeddings when combining text with categorical/tabular features.

Time Series

Time-series models learn trends and seasonality from timestamped data and forecast future values. Typical applications include IoT sensor monitoring, inventory/sales forecasting, and financial time-series forecasting.

<Frame>
  <img alt="The image explains types of machine learning algorithms focusing on timeseries, highlighting use cases such as IoT sensor monitoring, stock price forecasting, and sales prediction, with examples like temperature, stock prices, or foot traffic data." />
</Frame>

Unsupervised Learning

Unsupervised learning uncovers patterns without labeled targets. Typical tasks include clustering, dimensionality reduction, anomaly detection, and topic discovery. These techniques are useful for customer segmentation, exploratory data analysis, and streaming anomaly detection.

<Frame>
  <img alt="The image describes unsupervised machine learning, highlighting its ability to find hidden patterns in data without labeled outputs, with use cases such as topic modeling, customer segmentation, and anomaly detection. Examples of methods include clustering, dimensionality reduction, and association rules." />
</Frame>

Common unsupervised algorithms:

* K-Means — clustering.
* PCA (Principal Component Analysis) — dimensionality reduction for visualization and preprocessing.
* Random Cut Forest (RCF) — anomaly detection for time-series and streaming use cases.
* LDA — unsupervised topic modeling for text.

Vision ML

Vision ML works with images and video data for tasks such as classification, detection, segmentation, and embedding-based retrieval. Use cases include medical imaging, satellite image analysis, OCR, and visual search.

Vision capabilities include:

* Image classification (single-label/multi-label).
* Object detection (SSD-based models).
* Semantic segmentation — pixel-wise classification, valuable in medical and remote-sensing domains.
* Image embeddings (Object2Vec) — for similarity search and retrieval.

Consolidated algorithm summary

| Category     | Algorithms / Models                                                  | Typical Use Cases                                                        |
| ------------ | -------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Tabular      | Linear Learner, XGBoost, Factorization Machines, KNN, Object2Vec     | Classification, regression, recommendation, ranking                      |
| Text (NLP)   | BlazingText, Seq2Seq, BERT (JumpStart), LDA, Object2Vec              | Classification, sentiment, translation, summarization, topic modeling    |
| Time Series  | Forecasting algorithms, RCF                                          | Forecasting, monitoring, anomaly detection                               |
| Unsupervised | K-Means, PCA, RCF, LDA                                               | Clustering, dimensionality reduction, anomaly detection, topic discovery |
| Vision       | Image classification, SSD object detection, segmentation, embeddings | Detection, segmentation, visual search, medical imaging                  |

SageMaker built-in containers and input formats

Built-in algorithms expect specific input formats depending on the algorithm: CSV, libsvm, RecordIO, or TFRecord. Check the algorithm documentation for required channel names (for example, `train` and `validation`) and input format before launching training jobs.

> **lightbulb** Built-in and framework containers often expect specific data formats (e.g., CSV, RecordIO, or libsvm). Check the algorithm documentation for required input formats and channel names before running training.

SageMaker SDK example: train XGBoost in Script Mode

This concise example shows how to run a SageMaker XGBoost training job using the SageMaker Python SDK in Script Mode. Replace the placeholder values for the IAM role and S3 paths with your own.

```python theme={null}
from sagemaker.xgboost import XGBoost
