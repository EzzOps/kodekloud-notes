# Review and Improve Model

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Custom-Classification-and-Named-Entity-Extraction/Review-and-Improve-Model/page

Guide to evaluating and iteratively improving ML models with metrics, error analysis, data augmentation, monitoring, and practical steps for handling low training data and deployment

Reviewing and improving a machine learning model is a recurring, critical phase in any ML workflow. This guide walks through practical steps to evaluate model performance, find gaps, and iterate so the model produces accurate, robust predictions over time.

## Training and evaluation overview

After labeling data, train your model (or fine-tune a pretrained backbone) so it can generalize to unseen examples. Once training finishes, evaluate with metrics that match your task and business needs.

Key evaluation metrics:

| Metric                | Definition                                                                                | When to use                                                     |
| --------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Precision             | TP / (TP + FP) — proportion of predicted positives that are correct                       | When false positives are costly (e.g., spam detection)          |
| Recall                | TP / (TP + FN) — proportion of actual positives detected                                  | When missing true positives is costly (e.g., medical diagnosis) |
| F1 score              | 2 \* (Precision \* Recall) / (Precision + Recall) — harmonic mean of precision and recall | When you need a single balanced metric                          |
| NER F1 (entity-level) | F1 computed on exact span + label matches                                                 | Use for strict named-entity recognition evaluation              |

For named-entity recognition (NER), compute F1 at the entity level (exact span and label match) rather than token-level when you require strict evaluation of entity extraction.

Example: a trained model reporting 100% precision, 100% recall, and 100% F1 often warrants skepticism. Perfect scores commonly indicate one of the following:

* too small or overly simplistic dataset,
* data leakage between training and test sets,
* or an evaluation set that doesn't reflect real-world variability.

<Callout icon="warning">
  Perfect evaluation scores are typically a red flag. Before trusting such results, verify that there is no data leakage, confirm the evaluation set size and representativeness, and inspect your train/validation/test splits.
</Callout>

<Frame>
  <img alt="A presentation slide titled &#x22;Reviewing and Improving Model&#x22; showing four colored icons for ML Model Training, Performance Evaluation, Identify Data Gaps, and Model Iteration. The slide also includes the caption &#x22;Continuous improvement ensures higher model reliability!&#x22;" />
</Frame>

## Iterative improvement cycle

Improving a model is an iterative loop. A practical cycle looks like:

1. Train or fine-tune the model on labeled data.
2. Evaluate using appropriate metrics and robust held-out data (train/validation/test splits or cross-validation).
3. Perform error analysis to find systematic failures (missing categories, frequent misclassification, label bias).
4. Fix data gaps by:
   * adding labeled examples for underrepresented classes,
   * improving annotation quality and instructions (clear schema, training for annotators),
   * using data augmentation or synthetic examples where appropriate,
   * applying active learning to prioritize labeling informative samples.
5. Iterate: retrain with the improved dataset and tune hyperparameters, architectures, or regularization.
6. Monitor performance in production and repeat the loop as new data arrives.

Some practical notes for step 3 (error analysis):

* Create confusion matrices and per-class precision/recall to surface recurring mistakes.
* Inspect failure cases manually to discover annotation inconsistencies or ambiguous labels.
* Segment errors by features (e.g., text length, language, input source) to reveal hidden biases.

## Practical actions when the model UI flags "not enough training data"

If your model management UI reports insufficient training data, take these actions:

* Collect additional labeled examples that reflect real-world distributions and edge cases.
* Ensure the evaluation set is held out properly and mirrors production data.
* Improve annotation consistency: clear guidelines, multiple annotators, and adjudication for disagreements.
* Use cross-validation or enlarge holdout sets to stabilize metrics.
* Consider transfer learning or pretrained backbones to reduce labeled-data needs.
* Use ensembles or calibration techniques if score variance suggests instability.

<Callout icon="lightbulb">
  Prioritize collecting diverse, representative examples and targeted error analysis—these activities usually deliver greater improvements than only tuning hyperparameters.
</Callout>

## Monitoring and production

Continuous improvement is the backbone of reliable AI systems. In production, instrument the model to:

* log predictions and key inputs,
* sample and label prediction failures,
* track drift in input distributions and label distributions,
* trigger retraining (or human-in-the-loop review) when performance drops.

Automating monitoring and retraining pipelines helps maintain model quality as real-world data evolves.

## References and further reading

* scikit-learn: Precision, recall, F1 — [https://scikit-learn.org/stable/modules/model\_evaluation.html](https://scikit-learn.org/stable/modules/model_evaluation.html)
* Best practices for annotation and labeling — consider documentation from your annotation provider or tools such as [Label Studio](https://labelstud.io/)
* NER evaluation tools: seqeval or spaCy evaluation utilities

With these steps, you can complete the review-and-improve cycle for custom classification or NER models and establish a repeatable process for continual model quality.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/59765c98-dac0-42f2-bf92-2f6fd2dc38d2/lesson/82c5bd25-c98c-4331-b6c4-a2b521c8fbd5" />
</CardGroup>
