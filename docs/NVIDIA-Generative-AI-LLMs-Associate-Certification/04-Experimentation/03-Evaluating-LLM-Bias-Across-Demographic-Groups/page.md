# Evaluating LLM Bias Across Demographic Groups

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-[AWS_SECRET_ACCESS_KEY]-LLM-Bias-Across-Demographic-Groups/page

Guidelines for detecting and measuring LLM performance disparities across demographic groups via stratified evaluations, group-level metrics, statistical testing, and privacy-aware practices.

Question 6.

Which approach is most effective for evaluating an LLM's performance across diverse demographic groups to identify potential biases?

* Testing on a single, large, randomly selected dataset?
* Disaggregated evaluation using stratified test sets representing different demographic groups?
* Asking the model to self-evaluate its biases, or measuring only the overall accuracy on the complete dataset?

<Callout icon="lightbulb">
  Disaggregated evaluation using stratified test sets representing different demographic groups is the most effective approach.
</Callout>

## Why disaggregated (stratified) evaluation matters

A single, large random test set produces aggregate metrics (e.g., overall accuracy) that can mask important performance differences across demographic groups. A model may appear to perform well in aggregate while systematically underperforming on minority or intersectional groups—disaggregated evaluation surfaces those disparities.

Key reasons to prefer stratified evaluation:

* It isolates group-level performance so you can detect and quantify disparities.
* It supports targeted diagnostics (e.g., error types by group) and remediation.
* It enables fairness-aware metrics (not just accuracy) to be computed per group.

## What a robust disaggregated evaluation includes

* Stratified test sets that represent the demographic groups of interest (including intersectional slices where relevant).
* Multiple metrics per group:
  * Performance: accuracy, precision, recall, F1.
  * Error analysis: false positive/negative rates.
  * Calibration: confidence vs accuracy per group.
  * Fairness metrics: statistical parity difference, equalized odds, demographic parity, predictive parity—choose depending on your deployment context.
* Statistical rigour:
  * Confidence intervals or hypothesis testing to determine whether observed gaps are statistically significant.
  * Adequate sample sizes for each subgroup; if some groups are small, consider targeted data collection.
* Qualitative review:
  * Examine representative failures from each group to understand root causes.
* Data quality and labeling consistency:
  * Ensure labels and metadata are consistent across groups to avoid evaluation artifacts.

## Quick comparison

| Approach                                   |                                                               Strengths | Weaknesses                                                      | Recommendation                                                        |
| ------------------------------------------ | ----------------------------------------------------------------------: | --------------------------------------------------------------- | --------------------------------------------------------------------- |
| Single, random dataset (aggregate metrics) |                                        Simple to run; large sample size | Can hide group-level disparities; gives false sense of fairness | Not sufficient alone—use as complement to disaggregated evaluation    |
| Disaggregated, stratified evaluation       | Reveals group disparities; supports fairness metrics and targeted fixes | Requires careful data collection and sufficient subgroup sizes  | Recommended primary approach for bias detection                       |
| Model self-evaluation                      |                                                       Fast and low-cost | Unreliable introspection; prompt-sensitive; can be manipulated  | Not recommended as sole approach; can be used as supplementary signal |

## Example evaluation workflow (high-level)

1. Define demographic groups and intersectional slices to analyze.
2. Create or sample stratified test sets that ensure adequate representation for each slice.
3. Run model inference and compute per-group metrics.
4. Compute fairness metrics and statistical tests (e.g., difference in means with confidence intervals, bootstrap).
5. Perform qualitative error analysis on representative failures.
6. Report both aggregate and disaggregated results; iterate on mitigation strategies.

## Example: compute group-level metrics (Python/pseudocode)

```python theme={null}
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score
