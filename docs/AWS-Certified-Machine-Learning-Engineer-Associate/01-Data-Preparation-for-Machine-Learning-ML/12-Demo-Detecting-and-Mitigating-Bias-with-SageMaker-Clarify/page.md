# python
feature_definitions = [
    {"FeatureName": "PassengerId", "FeatureType": "Integral"},
    {"FeatureName": "Fare", "FeatureType": "Fractional"},
    {"FeatureName": "Sex", "FeatureType": "String"},
    {"FeatureName": "EventTime", "FeatureType": "String"},  # ISO 8601 timestamps recommended
    {"FeatureName": "Age", "FeatureType": "Fractional"},
    {"FeatureName": "Survived", "FeatureType": "Integral"},
]
```

<Callout icon="lightbulb">
  Record event times consistently (preferably in ISO 8601 format). Consistent timestamps ensure time-travel queries and offline joins return the expected historical state.
</Callout>

Ingesting records and reusing features

After creating a feature group, ingest records into the online and/or offline stores using the SageMaker Feature Store APIs or the SageMaker Python SDK. Once populated, these features become reusable across training pipelines and real-time inference endpoints, eliminating duplication of feature engineering logic and improving reliability.

Next steps and recommended actions

* Populate the feature group with ingested records (real-time or batch ingest).
* Use the offline store S3 dataset for batch training and backtesting.
* Use the online store for low-latency inference lookups.
* Implement IAM-based access control, monitoring, and alerts for feature group usage and costs.
* Review AWS documentation for advanced topics such as feature transformations, point-in-time joins, and cross-account access:
  * [Amazon SageMaker Feature Store — Documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html)
  * [SageMaker Python SDK — Feature Store examples](https://sagemaker.readthedocs.io/en/stable/feature_store.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/b0bccb0b-700e-4c43-942d-36400f08a2b1" />
</CardGroup>


# Demo Detecting and Mitigating Bias with SageMaker Clarify

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Demo-Detecting-and-Mitigating-Bias-with-SageMaker-Clarify/page

Demo of detecting and mitigating dataset bias using Amazon SageMaker Clarify in Data Wrangler, illustrated with a Titanic example and mitigation techniques like over and undersampling.

In this lesson we demonstrate how to detect dataset bias with Amazon SageMaker Clarify from within Data Wrangler (launched via SageMaker Canvas), and how to apply simple mitigation steps before training. We use a Canvas-imported Titanic dataset as a running example and show how to interpret Clarify’s bias report so you can make targeted corrections to your data pipeline.

Why this matters

* Detecting representation and label disparities early prevents biased behavior from being learned and amplified by models.
* Clarify integrates into the data preparation workflow in Data Wrangler, letting you inspect, mitigate, and re-evaluate bias without leaving the visual flow.

Getting started

1. In the AWS console, open Amazon SageMaker: [https://learn.kodekloud.com/user/courses/aws-sagemaker](https://learn.kodekloud.com/user/courses/aws-sagemaker).
2. Under Applications, open Canvas.
3. From Canvas, launch Data Wrangler and create a new data flow. For this demo, we start from a Canvas dataset containing the Titanic data (import completed successfully).
4. Verify your dataset’s column types (numerical vs categorical) and clean any parsing issues before running the analysis.

Configuring a Clarify bias analysis

* In Data Wrangler, open the Analysis section and choose the Bias report (SageMaker Clarify).
* Choose the label (the column your model predicts): `survived`.
  * Set the label value indicating the positive outcome to `1` (survived = `1`).
* Choose the sensitive attribute (the column to analyze for bias): `sex`.
  * Set the attribute value to analyze (for example, `male`) — Clarify will compare this group against the remainder of the dataset (the reference group).
* Optionally configure mitigation options (oversampling or undersampling) to rebalance the dataset automatically after the imbalance is identified.

Viewing the bias report
Once the analysis completes, Clarify generates a bias report with multiple metrics describing group representation and disparate outcomes. Below is the bias report produced for the Titanic dataset in Data Wrangler.

<Frame>
  <img alt="The image shows a screenshot of the Amazon SageMaker Data Wrangler interface, displaying a bias report in the &#x22;Test-flow&#x22; for a dataset named &#x22;Titanic.&#x22; The report analyzes bias in the &#x22;Sex&#x22; column, focusing on metrics like Class Imbalance (CI), Difference in Positive Proportions in Labels (DPL), and Jensen-Shannon Divergence (JS)." />
</Frame>

Understanding Clarify’s key metrics
The following table summarizes the most important metrics you’ll see in the Clarify bias report and what each one implies for data quality and fairness.

| Metric                                             |                                                  What it measures | Interpretation and recommended action                                                                                                                                                                                   |
| -------------------------------------------------- | ----------------------------------------------------------------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Class Imbalance (CI)                               |         Relative representation of the specified group vs. others | Negative CI means the specified group (e.g., `male`) is under-represented. Example: `CI = -0.29` indicates fewer `male` samples. Consider oversampling the under-represented group or collecting more data.             |
| Difference in Positive Proportions in Labels (DPL) | Difference in positive outcome rates (label = `1`) between groups | Large positive or negative DPL indicates one group receives better/worse outcomes in the dataset. If DPL is substantial, inspect labeling process and consider resampling or label correction strategies.               |
| Jensen–Shannon (JS) Divergence                     | Symmetric measure of how label distributions differ across groups | JS is bounded and easier to interpret than KL divergence. Higher JS means label distributions differ across groups; reducing CI and DPL typically lowers JS. Use mitigation and re-run analysis to verify improvements. |

Practical mitigation workflows

* Oversampling: Increase the number of records for the under-represented group by duplicating samples or synthetically generating new ones. This raises the group’s presence and can reduce CI and DPL.
* Undersampling: Reduce the number of records from an over-represented group. This simplifies class balance but may remove informative samples—use cautiously.
* Re-labeling and data-quality fixes: If disparities are due to label errors or historical bias in labeling, correct labels or adjust features that encode biased signals.
* Re-run Clarify: After any mitigation, re-run the bias analysis inside Data Wrangler to quantify the effect on CI, DPL, and JS.

Recommended checks before training

* Confirm column types and missing-value handling for the features used in Clarify.
* Validate that the chosen sensitive attribute and reference groups match your fairness goals (e.g., `sex`, `race`, `age` buckets).
* Monitor how mitigation affects downstream model performance (accuracy, precision/recall) and fairness metrics simultaneously.

Quick checklist

* [ ] Verify dataset imports and column types in Data Wrangler.
* [ ] Select `survived` as label and set positive label = `1`.
* [ ] Select sensitive attribute `sex` and choose the group to analyze (e.g., `male`).
* [ ] Inspect CI, DPL, JS in Clarify report.
* [ ] Apply oversampling/undersampling or data fixes if needed.
* [ ] Re-run Clarify and compare metrics.
* [ ] Proceed to model training only after acceptable parity is achieved or mitigation is documented.

Next steps and resources

* If you detect meaningful imbalance or disparate outcomes, apply mitigation techniques in Data Wrangler (oversampling/undersampling) and re-run the Clarify analysis to validate improvements.
* Use bias analysis as a standard gating step before training models to avoid amplifying dataset imbalances in production.

<Callout icon="lightbulb">
  Always analyze your training dataset for representation and label disparities before proceeding to model training. Small corrections to class balance and label proportions can significantly reduce biased model behavior downstream.
</Callout>

Links and references

* [Amazon SageMaker — KodeKloud course page](https://learn.kodekloud.com/user/courses/aws-sagemaker)
* SageMaker Clarify documentation (AWS): [https://docs.aws.amazon.com/sagemaker/latest/dg/clarify.html](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify.html)
* Data Wrangler overview (AWS): [https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html](https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/46c26552-96e1-4dfa-9b6b-bab69153386b" />
</CardGroup>
