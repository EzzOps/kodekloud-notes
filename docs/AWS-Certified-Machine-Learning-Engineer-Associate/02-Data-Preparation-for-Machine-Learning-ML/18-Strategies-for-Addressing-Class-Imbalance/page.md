# Strategies for Addressing Class Imbalance

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Strategies-for-Addressing-Class-Imbalance/page

Overview of methods to address class imbalance in machine learning, covering resampling like oversampling and SMOTE, algorithmic weighting and cost-sensitive learning, evaluation metrics and best practices

Class imbalance occurs when one class (the majority) greatly outnumbers another (the minority). This is common in domains such as fraud detection, rare disease diagnosis, and anomaly detection. Imbalanced classes can bias models toward the majority class, producing deceptively high overall accuracy while failing to detect the minority class—the class you often care most about.

<Frame>
  <img alt="The image is an introduction to the concept of class imbalance in data, illustrating it with colored circles and highlighting three issues: bias to the majority class, poor detection of the minority class, and effects on rare events like fraud and disease." />
</Frame>

Why this matters: if a dataset has 99% negatives and 1% positives, a model that always predicts negative achieves 99% accuracy yet is useless for detecting positives. For imbalanced datasets, accuracy is not a reliable metric—use targeted metrics that reflect minority-class performance.

<Frame>
  <img alt="The image lists metrics better than accuracy for evaluating models: Precision, Recall, F1 Score, and AUC-ROC." />
</Frame>

Key evaluation metrics for imbalanced problems

* Precision = TP / (TP + FP) — of predicted positives, how many are correct.
* Recall (Sensitivity) = TP / (TP + FN) — of actual positives, how many we detected.
* F1 Score = 2 \* (Precision \* Recall) / (Precision + Recall) — harmonic mean of precision and recall; useful when both false positives and false negatives matter.
* ROC AUC — area under the ROC curve (TPR vs FPR) across thresholds; good for overall separability.
* PR AUC (Precision-Recall AUC) — often more informative than ROC AUC when the positive class is rare.

> **lightbulb** When the minority class detection is critical, prioritize precision, recall, F1 and PR AUC over plain accuracy. Use ROC AUC to compare separability and PR AUC to evaluate performance on rare positives.

Approaches to handle class imbalance fall into two categories:

* Data-level strategies (resampling): alter the training data distribution.
* Algorithm-level strategies: change the learning algorithm or loss to account for imbalance.

Data-level strategies (resampling)

<Frame>
  <img alt="The image outlines three data-level strategies: Random Oversampling, Random Undersampling, and SMOTE, each focused on balancing class distributions in datasets." />
</Frame>

* Random oversampling: duplicate minority-class examples to rebalance classes. Pros: simple, effective for small imbalances. Cons: increases overfitting risk (exact duplicates).
* Random undersampling: remove majority-class examples to balance classes. Pros: faster training, less storage. Cons: may discard useful information.
* SMOTE (Synthetic Minority Oversampling Technique): synthesize new minority examples by interpolating between a sample and its k nearest minority neighbors. Pros: generates diverse minority examples, reduces overfitting compared with naive duplication. Cons: can create borderline/noisy samples and is sensitive to k and feature scaling.

Important: Always split into train/test (preferably stratified) before applying oversampling. Applying oversampling to the entire dataset before splitting causes data leakage and inflated performance.

> **warning** Never oversample (including SMOTE) before splitting your data. Apply resampling only to the training set to avoid information leakage into your validation/test sets.

How SMOTE works

SMOTE generates a synthetic sample by selecting a minority-class sample, choosing one of its k nearest minority neighbors, and interpolating a new point along the line segment between them. This produces plausible, non-duplicate minority samples and can help classifiers generalize better to minority regions.

<Frame>
  <img alt="The image outlines the advantages and disadvantages of the Synthetic Minority Oversampling Technique (SMOTE), highlighting that it creates diverse examples and reduces overfitting risk, but may generate borderline samples." />
</Frame>

Advantages of SMOTE:

* Produces new, diverse minority examples (reduces overfitting compared with duplication).
* Can improve classifier sensitivity to minority examples.

Drawbacks and cautions:

* May generate noisy/borderline samples that cross class boundaries if classes overlap.
* Sensitive to the number of neighbors (k) and to feature scaling—standardize features first.
* For structured data (tabular), SMOTE works well; for images/text, use domain-specific augmentation.

Example: apply SMOTE only on the training set (using imbalanced-learn)

```python theme={null}
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
