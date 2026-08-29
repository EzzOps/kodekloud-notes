# Replace "N A" with NaN and impute size with column mean
df['size'] = pd.to_numeric(df['size'].replace("N A", pd.NA))
df['size'] = df['size'].fillna(df['size'].mean())

# Fill missing bedrooms with median
df['bedrooms'] = df['bedrooms'].fillna(df['bedrooms'].median())

# Normalize price and size
scaler = StandardScaler()
df[['price', 'size']] = scaler.fit_transform(df[['price', 'size']])
```

<Frame>
  <img alt="The image shows a data transformation example with two tables: the top table displays unprocessed housing data, while the bottom table shows the normalized version of the same data." />
</Frame>

Feature engineering — example derivatives for housing data

* House age = current year − year built
* Size per bedroom = total area ÷ number of bedrooms

These derived features often encode domain knowledge that improves predictive power.

<Frame>
  <img alt="The image illustrates a real-world example of feature engineering, displaying a table with house age and size per bedroom, along with formulas for calculating house age and size per bedroom." />
</Frame>

Additional practical tips

* Preserve a raw data snapshot so you can re-run preparation if assumptions change.
* Automate and version your preprocessing (e.g., with pipelines) to ensure reproducibility.
* Validate assumptions continuously (missingness patterns, covariate shift, label quality).
* Monitor models in production for data drift and trigger re-preparation when distributions change.

> **warning** Avoid data leakage: do not compute statistics (e.g., scaling parameters or imputation values) using the full dataset including test/validation sets. Fit transformers on training data only and apply them to validation/test sets.

Summary

* Cleaning removes errors and harmonizes formats.
* Transformation converts raw values into model-ready features.
* Feature engineering creates context-rich inputs that improve learning.
* Labeling provides correct targets for supervised models.
* Validation ensures data quality and model generalizability.

Further reading and references

* [Kaggle: Data Cleaning](https://www.kaggle.com/learn/data-cleaning)
* [Scikit-learn: Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
* [UCI Machine Learning Repository](https://archive.ics.uci.edu/)

Careful data preparation is not optional—it's essential for building fair, accurate, and maintainable machine learning systems.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/420f5a74-c182-4969-8965-e58fa0d6ce5d)


# Introduction to Data Transformation and Cleaning

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Introduction-to-Data-Transformation-and-Cleaning/page

Overview of data cleaning and transformation techniques for preparing datasets for reliable machine learning, including AWS tools and practical examples.

Models only learn from the data you provide. If that data is inaccurate, inconsistent, or full of errors, the model will be unreliable. In short: bad data equals bad models. Data cleaning and transformation are essential steps that prevent poor-quality data from undermining the entire machine learning pipeline.

Data cleaning identifies and fixes problems such as missing values, inconsistent formats, duplicates, outliers, and type mismatches. Once cleaned, data is transformed to meet algorithm requirements (scaling, encoding, aggregation, parsing, binning), producing a reliable foundation for feature engineering and modeling.

<Frame>
  <img alt="The image outlines the process of data cleaning, highlighting issues such as missing values, inconsistent formats, duplicates, and outliers in datasets." />
</Frame>

> **lightbulb** Clean, well-documented data is the first and most important step toward building reliable ML systems. Invest time here to avoid compounding issues downstream.

<Frame>
  <img alt="The image explains data cleaning, detailing issues like missing values, inconsistent formats, duplicates, outliers, and data type mismatches in datasets." />
</Frame>

Quick reference — common problems and actions

| Problem                     | Typical fixes                                                           |
| --------------------------- | ----------------------------------------------------------------------- |
| Missing values              | Drop rows/columns, impute (mean/median/mode), or model-based imputation |
| Duplicates                  | Remove exact duplicates or dedupe based on key subset                   |
| Inconsistent formats        | Parse and normalize (e.g., dates to ISO 8601)                           |
| Outliers                    | Detect with IQR/domain thresholds; cap, transform, or remove            |
| Type mismatches             | Strip non-numeric characters and cast to numeric/datetime               |
| Categorical inconsistencies | Map variants/typos to a controlled vocabulary                           |

Common cleaning techniques (expanded)

* Missing values: remove or impute (median is robust for skewed data).
* Duplicates: deduplicate using full-row or subset-based logic.
* Outliers: apply domain thresholds, IQR, or winsorization.
* Type conversions: ensure numeric, datetime, and categorical dtypes are correct.
* Standardization: normalize inconsistent string formats (dates, currencies).
* Controlled vocabulary: normalize typos and synonyms to canonical category values.

Missing values
Missing values can distort statistics and models. Choose between removing affected rows/columns (simpler, destructive) or imputing (preserves sample size). Imputation methods include mean, median, mode, forward/backfill, or model-based techniques.

> **warning** Dropping rows with missing values is irreversible for that dataset copy and can bias results if missingness is not random. Prefer imputation or analyze missingness patterns first.

Example — drop or impute with pandas:

```python theme={null}
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [29, None, 45]
})
