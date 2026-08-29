# SageMaker Clarify for Bias Detection

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/SageMaker-Clarify-for-Bias-Detection/page

Overview of SageMaker Clarify's tools to detect, measure, and explain dataset and model bias using pre and post training checks, SHAP explanations, metrics, and reports.

Bias in data produces unfair or discriminatory model predictions. When training data reflects historical or sampling biases, models can learn and amplify those patterns—affecting outcomes in hiring, lending, healthcare, and other high-stakes domains. Detecting bias early reduces harm and increases trust in AI systems.

<Callout icon="lightbulb">
  Use bias detection as an early, repeatable step in your ML pipeline. Combining dataset-level checks with model explainability helps teams find root causes and prioritize remediation.
</Callout>

<Frame>
  <img alt="The image explains the impact of bias in data on models, leading to unfair and discriminatory predictions." />
</Frame>

Why this matters: bias left unchecked can lead to systematic harm and regulatory or reputational risk. Detecting and addressing bias helps ensure more equitable outcomes and supports compliance efforts.

<Frame>
  <img alt="The image explains why bias detection matters, highlighting the importance of identifying bias in data to prevent harmful outcomes and build trust in AI systems." />
</Frame>

High-level workflow

* Data with bias → model training learns those patterns → downstream applications surface biased results.
* SageMaker Clarify provides automated analysis at both pre-training (dataset) and post-training (model/prediction) stages to detect, measure, and explain bias.

<Frame>
  <img alt="The image is a flowchart explaining SageMaker Clarify, demonstrating how bias in data leads to biased results through model training, specifically highlighting data collection, model training, and downstream impacts." />
</Frame>

Key capabilities

* Pre-training bias detection: analyze datasets for representation imbalances before training.
* Post-training bias detection: evaluate model outputs and fairness across subgroups after training.
* Explainability: use SHAP (Shapley) values to interpret model decisions and identify influential features.

These capabilities are packaged into reports and visualizations to help ML teams iterate on data and model choices.

<Frame>
  <img alt="The image describes SageMaker Clarify, highlighting its ability to detect bias in data and model predictions, use SHAP to explain model decisions, and generate reports to improve fairness." />
</Frame>

Where Clarify integrates

* Pre-training checks: run on raw or preprocessed datasets to surface class imbalances, label skews, or distribution drift.
* Post-training checks: run on model predictions to measure disparities in accuracy, precision, recall, and other performance metrics across protected or relevant subgroups.

<Frame>
  <img alt="The image explains SageMaker Clarify, a tool for detecting bias in pre-training data and ensuring fair predictions in post-training results. It illustrates the process flow from data input to result verification." />
</Frame>

Clarify supports four primary tasks

* Pre-training bias detection: inspect feature and label distributions for under/over-representation.
* Post-training bias detection: quantify fairness across model outputs and subgroups.
* Model explainability: identify features that drive predictions (global and local).
* Reporting: export bias and explainability reports for governance and audits.

<Frame>
  <img alt="The image describes SageMaker Clarify, highlighting its features: pre-training bias detection, post-training bias detection, and model explainability." />
</Frame>

Pre-training bias metrics

Pre-training checks reveal problems in the dataset itself that warrant remediation (resampling, reweighting, or feature engineering). Examples include:

| Metric                           | What it measures                                                       | Typical action                                     |
| -------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------- |
| Class imbalance                  | Uneven class frequency that may bias training towards majority classes | Resample or reweight classes                       |
| Label imbalance                  | Skew in target labels across subgroups                                 | Investigate labelling process; resample            |
| Kullback–Leibler (KL) divergence | Divergence between two distributions (e.g., subgroup vs. global)       | Identify features with divergent distributions     |
| Jensen–Shannon (JS) divergence   | Symmetric version of KL for comparing distributions                    | Highlight distributional differences across groups |
| Lp-norm distance                 | Distance measures on feature histograms or summary stats               | Detect large feature shifts or dominance           |

These dataset-level insights guide cleaning, collection augmentation, and rebalancing before training.

<Frame>
  <img alt="The image is a table detailing SageMaker Clarify pre-training bias metrics with columns for metrics, abbreviations, machine learning descriptions, and space analogies. Metrics include Class Imbalance, Label Imbalance, Kullback-Leibler Divergence, Jensen-Shannon Divergence, and Lp-norm Distance." />
</Frame>

Post-training bias metrics

After training, Clarify evaluates model behavior across groups. These metrics help detect potential unfair treatment in production and guide remediation such as threshold tuning, model retraining, or post-processing.

| Metric               | What it indicates                               | Remediation strategy                                          |
| -------------------- | ----------------------------------------------- | ------------------------------------------------------------- |
| Disparate impact     | Ratio of favorable outcomes between groups      | Adjust decision thresholds; consider relabeling               |
| Recall difference    | Difference in true positive rates across groups | Retrain with balanced data; tune classifier                   |
| Precision difference | Difference in positive predictive value         | Analyze confusion matrices; adjust loss or sampling           |
| Treatment equality   | Balance in false positive/negative trade-offs   | Post-process predictions or retrain with fairness constraints |

Use these metrics to prioritize where to take action and to quantify improvements over iterations.

<Frame>
  <img alt="The image is a table outlining SageMaker Clarify post-training bias metrics, including metric names, abbreviations, and what each one measures, such as Disparate Impact, Recall Difference, and Treatment Equality." />
</Frame>

Explainability (SHAP)

Explainability complements fairness metrics by attributing model behavior to input features:

* Global explanations: identify features that most influence model outputs across the dataset.
* Local explanations: explain why the model produced a specific prediction for an individual instance.

Using SHAP values helps uncover features or correlations that lead to disparate outcomes—enabling targeted fixes such as feature removal, transformation, or reweighting.

Clarify combines explainability with bias metrics to produce comprehensive reports for governance, audits, and cross-functional review. These reports document where bias exists, why it may be occurring, and what remediation steps were taken or recommended.

Additional resources

* SageMaker Clarify documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/clarify.html](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify.html)
* SHAP (Shapley) values: [https://shap.readthedocs.io/en/latest/](https://shap.readthedocs.io/en/latest/)

<Callout icon="warning">
  Automated metrics guide action but don’t replace domain expertise. Always combine statistical checks with stakeholder review and legal/regulatory guidance where needed.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/51b371a4-d904-4956-9a33-6e239bb8e6d6" />
</CardGroup>
