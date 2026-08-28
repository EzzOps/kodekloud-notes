# Creating Performance Baselines

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/Creating-Performance-Baselines/page

Guide on creating and using baseline models to evaluate machine learning performance, from naive and heuristic to model-based and SOTA baselines, with examples and a practical checklist.

A baseline model is a simple, well-defined reference used to evaluate whether a new model provides meaningful improvement. In practice, you feed the same input to both a BaselineModel and your TrainModel and compare their predictions and metrics. The purpose of a baseline is to establish a minimum acceptable performance and to justify added model complexity when the trained model exceeds that baseline.

<Frame>
  <img alt="The image illustrates a flowchart showing a baseline concept overview, where input data is processed through a baseline model and a trained model to generate and compare predictions." />
</Frame>

## Common baseline types

Use increasingly stronger baselines as you progress: start simple and advance toward more competitive references. Below is a concise description of common baseline classes.

| Baseline Type     |                               Purpose / When to Use | Typical Example                                    |
| ----------------- | --------------------------------------------------: | -------------------------------------------------- |
| Naive             |            Quick sanity check to set a very low bar | Always predict the majority class (classification) |
| Random            |           Establish a minimum floor for performance | Random class labels or random regression values    |
| Heuristic         |          Capture simple domain rules; interpretable | Rule-based formula like `y = 2x`                   |
| SimpleModel       |     Lightweight ML models providing data-driven fit | Linear/logistic regression, decision stump, k-NN   |
| HumanLevel        |           Compare model to human expert performance | Expert label accuracy in medical imaging           |
| SOTA              | Benchmark against best published or industry models | Top-performing research model or leaderboard entry |
| Business-as-usual |       Compare to the system currently in production | Existing model or rule set serving customers       |

<Callout icon="lightbulb">
  Choose baselines appropriate to your problem and dataset. Start with the simplest (naive) and progress to heuristics, simple models, and SOTA baselines until you establish a realistic target for development and deployment.
</Callout>

## Why baselines matter (example)

Suppose a baseline reaches 70% accuracy and your trained model reaches 85% accuracy — a 15 percentage-point improvement. That gap quantifies the model’s added value and helps decide whether extra complexity is justified.

<Frame>
  <img alt="The image illustrates a comparison between a baseline model with 70% accuracy and a trained model with 85% accuracy, highlighting a 15% improvement in accuracy indicating meaningful learning." />
</Frame>

## Naive baselines by problem type

Naive baselines are fast to compute and useful as the first checkpoint. They intentionally ignore patterns in the features and act as a simple reference.

| Problem Type             | Naive Strategy                                      |
| ------------------------ | --------------------------------------------------- |
| Classification           | Predict the majority class                          |
| Regression               | Predict the global mean or median of the target     |
| Time series              | Predict the last observed value (persistence model) |
| Ranking / Recommendation | Rank items by global popularity                     |

The plot below illustrates a naive regression baseline predicting the global mean as a constant (dashed line) while the actual target values vary over time. This highlights how naive approaches provide a minimal benchmark that more sophisticated models should surpass.

<Frame>
  <img alt="The image is a line graph comparing &#x22;Naive Regression Baseline vs Actual&#x22; values over different time steps, with actual values depicted as a solid line and the naive baseline as a dashed line. The graph includes labeled axes for target value and time step." />
</Frame>

## Heuristic baselines

Heuristic baselines apply simple, interpretable rules derived from domain knowledge (for example, `y = 2x`). They often outperform naive baselines because they encode known relationships and provide a stronger, explainable benchmark. Use these to confirm whether model complexity is adding value beyond simple rules.

## Model-based baselines

Model-based baselines use basic machine learning algorithms to create a data-adaptive reference. These typically outperform naive and heuristic baselines and are essential for structured data problems.

Common simple-model baselines:

* Linear regression / logistic regression for tabular data
* Decision stumps (single-level decision trees)
* k-Nearest Neighbors (kNN), often with k=1 or small k

These model families are lightweight, fast to train, and help set realistic expectations before moving to more complex architectures.

<Frame>
  <img alt="The image describes three simple machine learning models: linear/logistic regression for structured data, decision stumps (single-level decision trees), and nearest neighbor approaches (kNN with k=1)." />
</Frame>

A model-based baseline such as linear regression adapts to the data and typically produces a better fit than a heuristic rule. The example below shows a linear baseline described by `y = 2.00x + 0.43` (dashed line) compared to actual values — a clear, data-driven reference.

<Frame>
  <img alt="The image shows a graph comparing model-based baseline values (a dashed blue line) and actual values (an orange line with dots) plotted against a feature (x-axis) and target value (y-axis). The baseline model follows the equation (y = 2.00x + 0.43)." />
</Frame>

## State-of-the-art (SOTA) baselines

SOTA baselines benchmark your approach against the best published or industry-standard models. These are useful to determine whether your model is competitive:

* If SOTA = 90% and your model = 85% → further improvements needed.
* If your model approaches SOTA, you may focus on deployment, inference optimization, or cost/performance trade-offs.

<Frame>
  <img alt="The image compares a baseline model with 90% accuracy to a trained model with 85% accuracy, highlighting the concept of state-of-the-art (SOTA) baselines." />
</Frame>

## Practical checklist for baselines

* Establish at least one simple baseline (naive or random) before model tuning.
* Iterate: naive → heuristic → simple model → SOTA as needed.
* Use the baseline gap (performance delta) to quantify business value and justify complexity.
* Report baselines alongside model metrics in documentation and model cards for transparency.
* Re-evaluate baselines when data, labels, or business objectives change.

Resources and further reading:

* [Model evaluation best practices](https://en.wikipedia.org/wiki/Cross-validation_\(statistics\))
* [When to compare with SOTA models](https://www.semanticscholar.org/)

By defining clear baselines early, you save development time, avoid unnecessary complexity, and focus on changes that deliver measurable value.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f3f28bdc-5ae5-43bb-85b6-01f7b1bfb71b/lesson/6100322a-02dc-4b1d-8645-0e6f8785398e" />
</CardGroup>
