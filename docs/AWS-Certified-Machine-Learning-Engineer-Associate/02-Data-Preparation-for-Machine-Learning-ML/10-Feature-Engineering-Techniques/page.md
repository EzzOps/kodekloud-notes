# Feature Engineering Techniques

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Feature-Engineering-Techniques/page

Guide to transforming raw data into informative machine learning features, covering techniques, benefits, examples, and production tooling for scalable, validated feature engineering

Feature engineering is the process of converting raw data into informative, model-ready features that help machine learning models discover patterns and make accurate predictions. Think of feature engineering as designing the best inputs (tools) for your model so it can solve the problem more effectively.

> **lightbulb** Feature engineering is both art and science: start with domain knowledge, iterate with experiments, and automate or store reliable features for reuse. Use simple features first—well-crafted features often beat higher model complexity.

<Frame>
  <img alt="The image illustrates the process of feature engineering, showing the transformation of raw data into meaningful features for use in machine learning models." />
</Frame>

Example scenario

* Imagine you work at a space agency and must predict whether a rocket launch will succeed. Raw sensor readings (temperature, humidity, wind, fuel levels, mass, radius, etc.) are useful but often insufficient by themselves.
* Feature engineering turns those raw signals into features that capture domain-relevant patterns—e.g., air density, thrust-to-weight ratio, wind shear index, and fuel margin—so a model can better assess risk.

Where feature engineering fits in the ML pipeline

* Raw data (often messy and unstructured) → Cleaning (fix missing values, remove errors) → Transformation (convert to structured, machine-readable form) → Feature engineering (derive meaningful features) → Model training & evaluation.

<Frame>
  <img alt="The image illustrates the stages of a machine learning pipeline, including raw data, cleaning, transformation, feature engineering, and model training. Each stage is represented by an icon and numbered sequentially." />
</Frame>

Why invest in feature engineering?

* Higher accuracy: Features that encode signal make patterns easier to learn.
* Faster training: Compact, relevant features reduce computation.
* Lower overfitting: Removing noisy or irrelevant inputs improves generalization.
* Better transfer: Robust features often generalize better to new data.

Table — Key benefits summary

| Benefit        | Why it matters                                | Example                                             |
| -------------- | --------------------------------------------- | --------------------------------------------------- |
| Accuracy       | Encodes signal into model inputs              | Thrust-to-weight ratio predicts lift-off capability |
| Efficiency     | Reduces input dimensionality and compute      | Aggregated metrics replace many raw sensors         |
| Generalization | Removes noisy features that cause overfitting | Drop faulty sensor readings                         |
| Reusability    | Store engineered features for multiple models | Central feature repository (Feature Store)          |

Transform raw signals into domain-aware features

* Raw sensors: temperature, humidity, wind speed, fuel level, mass, radius.
* Derived features that capture risk:
  * Temperature + humidity (+pressure) → air density
  * Thrust and mass → thrust-to-weight ratio
  * Wind speed profile → wind shear index
  * Fuel level → fuel margin

<Frame>
  <img alt="The image shows a table titled &#x22;Engineered Features (After Feature Engineering)&#x22; displaying data on launches, including Air Density, Thrust-to-Weight Ratio, Wind Shear Index, and Fuel Margin for three launch IDs." />
</Frame>

Common feature-engineering categories

* Transformation — rescaling or normalizing values so features are comparable.
* Encoding — converting categorical/textual data into numeric form (one-hot, ordinal).
* Extraction — deriving signals from raw fields (timestamps → hour/day).
* Creation — combining variables using domain knowledge (mass & radius → gravity).
* Selection — removing redundant/noisy features to reduce variance.
* Dimensionality reduction — compressing features with PCA, SVD, etc.

<Frame>
  <img alt="The image shows a flowchart illustrating five key steps: Transformation, Creation, Selection, Encoding, and Extraction, leading to Reduction." />
</Frame>

Practical examples and techniques

* Transformation
  * Min-max scaling to \[0,1] or z-score standardization to center/scale features.
  * Use scaling consistently between training and inference (save scalers).

* Encoding
  * One-hot encoding turns categories into binary vectors so models can use them.
  * Example: Planet types (Gas, Rock, Ice) → binary features for each category.

<Frame>
  <img alt="The image shows a feature encoding process that translates different planet types (Gas, Rock, Ice) into binary signals for Earth computers. It includes a table illustrating the binary representation for each planet type." />
</Frame>

* Extraction
  * From timestamps extract components such as hour-of-day, day-of-week, elapsed time, or cyclical encodings (sin/cos for time-of-day) to capture periodicity.

<Frame>
  <img alt="The image shows a slide about &#x22;Feature Extraction&#x22; focusing on extracting time-based data from space mission logs, with a table listing timestamps." />
</Frame>

* Creation
  * Build domain-specific features (e.g., compute gravity from mass and radius) to surface relationships not obvious from raw inputs.

* Selection
  * Filter out redundant or faulty sensors. If Sensor A is faulty and highly correlated with other sensors, remove it and keep unique signals like Sensor B.

<Frame>
  <img alt="The image shows a concept of feature selection for sensors on a spacecraft, illustrating the removal of redundant sensor data, keeping only unique data from Sensor B." />
</Frame>

* Dimensionality reduction
  * Use PCA or similar methods when many features are correlated. This reduces noise and model complexity while preserving variance (analogous to converting RGB to grayscale when color adds little value).

Scaling feature engineering for production (AWS tooling)

* Amazon SageMaker Data Wrangler — visual/no-code data cleaning, transformation, and feature engineering.
* Amazon SageMaker Feature Store — centralized, consistent feature repository for sharing and reusing features across teams and models.
* Amazon SageMaker Processing — scalable, code-based preprocessing and transformation jobs.
* AWS Glue / Amazon EMR — managed ETL and big-data processing for large-scale feature pipelines.

Links and references

* [Amazon SageMaker Data Wrangler](https://aws.amazon.com/sagemaker/data-wrangler/)
* [Amazon SageMaker Feature Store](https://aws.amazon.com/sagemaker/feature-store/)
* [Amazon SageMaker Processing](https://aws.amazon.com/sagemaker/processing/)
* [AWS Glue](https://aws.amazon.com/glue/)
* [Amazon EMR](https://aws.amazon.com/emr/)

> **warning** Beware of data leakage: create features using only training-period information. Using future labels or post-event data leaks can inflate validation metrics and produce poor real-world performance.

Best practices checklist

* Start with domain knowledge and simple features.
* Validate each feature with holdout/temporal validation.
* Persist proven features in a feature store for reproducibility.
* Automate pipelines for consistent preprocessing at training and inference.
* Monitor feature drift and data quality in production.

Feature engineering is iterative and domain-driven. Well-crafted features often allow simpler models to outperform complex ones trained on raw data—invest time in features, validate them carefully, and automate what proves reliable.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/16eb3cb9-5245-45f9-b94e-21bead86acc1)
