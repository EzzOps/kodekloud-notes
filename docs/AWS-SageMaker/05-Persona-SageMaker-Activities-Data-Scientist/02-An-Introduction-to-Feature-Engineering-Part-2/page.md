# Sample dataset
data = {
    'Bedrooms': [2, 3, 4, None],
    'Price': [200000, 250000, None, 150000],
    'Neighborhood': ['Downtown', None, 'Suburb', 'Rural']
}

df = pd.DataFrame(data)

print("Original DataFrame:")
print(df)

# Drop rows with any missing values
df_dropped_rows = df.dropna()
print("\nDataFrame after dropping rows with missing values:")
print(df_dropped_rows)

# Drop columns with any missing values
df_dropped_columns = df.dropna(axis=1)
print("\nDataFrame after dropping columns with missing values:")
print(df_dropped_columns)
```

### Imputation with scikit-learn's SimpleImputer

Imputation preserves dataset size and often helps models when applied sensibly. Choose strategy per feature type:

* Numeric: mean, median (robust to outliers), or a constant.
* Categorical: most\_frequent (mode) or a special token.

```python theme={null}
import pandas as pd
from sklearn.impute import SimpleImputer

# Sample house price dataset with missing values
data = {
    "Bedrooms": [3, 2, None, 4, 3, None, 5],
    "Bathrooms": [2, None, 1, 3, None, 2, 4],
    "Price": [250000, 180000, 220000, 350000, 275000, 300000, None],
    "Location": ["Urban", "Suburban", "Urban", None, "Urban", "Rural", "Suburban"]
}

df = pd.DataFrame(data)
print("Before Imputation:\n", df)

# Impute numerical features using the mean
num_imputer = SimpleImputer(strategy="mean")
df[["Bedrooms", "Bathrooms", "Price"]] = num_imputer.fit_transform(
    df[["Bedrooms", "Bathrooms", "Price"]]
)

# Impute categorical features using the mode (most frequent value)
cat_imputer = SimpleImputer(strategy="most_frequent")
df[["Location"]] = cat_imputer.fit_transform(df[["Location"]])

print("\nAfter Imputation:\n", df)
```

> **lightbulb** Imputation strategy matters. For skewed numeric features, prefer median over mean. For time-series or grouped data, consider group-wise imputation (e.g., median per region) rather than a global statistic.

## Standardizing numeric features

Standardization (zero mean, unit variance) helps gradient-based optimizers converge faster and benefits distance-based algorithms.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Standardizing Numeric Features&#x22; showing a flow from &#x22;Handle Scale Differences&#x22; to a &#x22;Standardize Features&#x22; button. It lists benefit 01 as &#x22;Gradient-based optimization (Faster convergence).&#x22;" />
</Frame>

Example using StandardScaler (sklearn.preprocessing):

```python theme={null}
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Sample DataFrame
data = {'Age': [25, 30, 35, 40],
        'Income': [50000, 60000, 75000, 100000]}

df = pd.DataFrame(data)

# Initialize StandardScaler
scaler = StandardScaler()

# fit_transform returns a NumPy array; convert back to DataFrame
df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

print(df_scaled)
```

## Where to run these transformations

Choose the execution environment based on dataset size and reproducibility requirements.

| Resource Type      | Use Case                                                | Example                                    |
| ------------------ | ------------------------------------------------------- | ------------------------------------------ |
| Local Jupyter      | Small exploratory datasets and rapid iteration          | Jupyter Notebook / JupyterLab              |
| Managed processing | Large datasets or heavy compute, reproducible pipelines | SageMaker Processing                       |
| Low-code GUI       | Users who prefer point-and-click transformation         | SageMaker Data Wrangler / SageMaker Canvas |

<Frame>
  <img alt="A slide titled &#x22;Standardization Workflow&#x22; showing a dashed box labeled &#x22;SageMaker Processing Locations&#x22; with three numbered tiles: 1) Jupyter Notebook, 2) SageMaker processing job, and 3) Data Wrangler built-in transformation." />
</Frame>

Relevant links:

* [pandas](https://pandas.pydata.org/)
* [scikit-learn](https://scikit-learn.org/stable/)
* [Jupyter Notebook](https://jupyter.org/)
* [SageMaker Processing](https://docs.aws.amazon.com/sagemaker/latest/dg/processing.html)
* [Data Wrangler](https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html)
* [SageMaker Canvas](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-canvas.html)

## Categorical data: encoding strategies

Most ML algorithms require numeric inputs, so convert categorical variables to numbers. Choose an encoding based on cardinality and whether categories are ordered.

* Ordinal encoding: use when categories have a meaningful order (e.g., low \< medium \< high).
* One-hot encoding: creates binary indicator columns for unordered categories.
* Dense embeddings: learned vector representations for high-cardinality categories (useful with neural nets).

| Encoding Type | Best For                           | Notes                                   |
| ------------- | ---------------------------------- | --------------------------------------- |
| Ordinal       | Ordered categories                 | Keeps ordering but assumes uniform gaps |
| One‑hot       | Low cardinality, tree-based models | Increases feature width                 |
| Embeddings    | Neural networks; high-cardinality  | Compact, captures relationships         |

One-hot increases width proportional to cardinality; embeddings are compact and can capture semantic relationships in neural models.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Categorical Data – Encoding&#x22; showing a table of sample house data with columns ID, Bedrooms, Price and one‑hot encoded location columns (Downtown, Suburb, Rural). The table lists four rows of example values (e.g., 2 bedrooms, 200,000, Downtown = 1)." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Categorical Data – Encoding&#x22; that compares One‑Hot Encoding (used with decision trees/XGBoost, which ignores relationships) to Dense Embeddings (used with neural networks, which capture relationships and patterns). The slide has a dark teal background and a small &#x22;© Copyright KodeKloud&#x22; note." />
</Frame>

### One-hot encoding example with pandas.get\_dummies

Use drop\_first=True when you need to avoid perfect multicollinearity for linear models.

```python theme={null}
import pandas as pd

# Sample dataset
data = {
    'Bedrooms': [2, 3, 4, 5],
    'Neighborhood': ['Downtown', 'Suburb', 'Suburb', 'Rural'],
    'Price': [200000, 250000, 300000, 150000]
}

df = pd.DataFrame(data)

print("Original DataFrame:")
print(df)

# Apply one-hot encoding to the 'Neighborhood' column
df_encoded = pd.get_dummies(df, columns=['Neighborhood'], drop_first=True)

print("\nDataFrame after One-Hot Encoding:")
print(df_encoded)
```

## Handling outliers

Choose an approach depending on whether you need to preserve rows:

* IQR filtering — removes extreme outliers (row loss).
* Percentile capping (winsorization) — replaces outliers with percentile boundaries (no row loss).

<Frame>
  <img alt="A presentation slide titled &#x22;Choosing a Method&#x22; showing two outlier-handling approaches: the IQR Method (&#x22;Removes extreme outliers&#x22;) and the Capping Method (&#x22;Replaces outliers with reasonable values&#x22;)." />
</Frame>

### IQR filtering example

```python theme={null}
import pandas as pd

# Example dataset with house prices
data = {
    'House_Size': [800, 1500, 1200, 1000, 5000, 1800, 3000, 2500, 1200, 1100],
    'Price': [200000, 350000, 280000, 250000, 2000000, 400000, 600000, 550000, 270000, 260000]
}

df = pd.DataFrame(data)

# Calculate Q1 (25th percentile) and Q3 (75th percentile)
Q1 = df['Price'].quantile(0.25)
Q3 = df['Price'].quantile(0.75)
IQR = Q3 - Q1

# Define the upper and lower bounds for outliers (1.5 * IQR)
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter out rows that have prices outside the bounds
df_filtered = df[(df['Price'] >= lower_bound) & (df['Price'] <= upper_bound)]

print("Original dataset:\n", df)
print("\nFiltered dataset (without outliers):\n", df_filtered)
```

### Percentile capping (clip) example

```python theme={null}
# Calculate the 1st (1%) and 99th (99%) percentiles
lower_percentile = df['Price'].quantile(0.01)
upper_percentile = df['Price'].quantile(0.99)

# Cap the outliers at these percentiles using clip
df_capped = df.copy()
df_capped['Price'] = df_capped['Price'].clip(lower=lower_percentile, upper=upper_percentile)

print("Original dataset:\n", df)
print("\nDataset with capped outliers:\n", df_capped)
```

> **warning** Do not remove outliers blindly. Investigate whether extreme values are data errors, rare-but-valid cases, or important signals (e.g., luxury properties). Choose removal or capping based on domain context and downstream model sensitivity.

* IQR filtering removes extreme values (reduces dataset size).
* Capping replaces extreme values with boundary values (keeps row count).

## Results you can expect from good preparation

* Faster and more stable training (models can identify relationships more easily).
* Greater algorithm flexibility (prepared data works across SVMs, KNN, XGBoost, neural nets).
* Better generalization and predictive performance.
* Ability to retain more data via imputation rather than dropping records.

<Frame>
  <img alt="A presentation slide titled &#x22;Results&#x22; showing five cards that summarize benefits: faster training, wider algorithm compatibility, improved accuracy, more data to work with, and retaining data via imputation." />
</Frame>

## Summary

* Preparing tabular data substantially improves readiness for training and typically results in faster convergence and better model quality.
* Use imputation methods (mean, median, mode) to retain dataset size when sensible.
* Standardization (StandardScaler) prevents large-scale features from dominating learning.
* Convert categorical variables using one-hot, ordinal, or embeddings depending on model type and cardinality.
* Handle outliers with IQR filtering or percentile capping depending on whether you want to remove or preserve rows.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; listing five data-preparation steps for machine learning. The points cover data readiness for training, imputing missing values, standardizing numerical features, encoding categorical variables, and handling outliers." />
</Frame>

SageMaker Canvas and Data Wrangler provide GUI-based alternatives that can run many of these preparation steps for users who prefer low-code workflows.

References and further reading:

* [pandas Documentation](https://pandas.pydata.org/)
* [scikit-learn Documentation](https://scikit-learn.org/stable/)
* [Jupyter Project](https://jupyter.org/)
* [Amazon SageMaker Processing](https://docs.aws.amazon.com/sagemaker/latest/dg/processing.html)
* [SageMaker Data Wrangler](https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html)
* [SageMaker Canvas](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-canvas.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/dc8df298-eaee-4f8a-b1d0-0ec66f9c6d20/lesson/ad32c581-70b8-4944-8f54-2f4a93bc657e)


# An Introduction to Feature Engineering Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-Data-Scientist/An-Introduction-to-Feature-Engineering-Part-2/page

Explains how targeted feature engineering improves model accuracy, generalization, interpretability, and training efficiency, plus strategies for handling data issues and tools for scalable transformations.

What can you expect from a targeted feature engineering process? In short: more accurate, more reliable models whose predictions are easier to act on. Thoughtful feature engineering strengthens signal, reduces noise, and helps training discover true, generalizable patterns instead of memorizing idiosyncrasies in the training set. The result is faster convergence, fewer experiments to reach acceptable performance, and improved downstream business utility.

<Frame>
  <img alt="A presentation slide titled &#x22;Results: Feature Engineering&#x22; showing four numbered panels that list benefits: accurate and useful predictions; pattern detection and generalization; optimized parameters and bias; and higher training success." />
</Frame>

Impact on model performance and training

* Stronger features produce clearer correlations between inputs and targets, yielding more accurate predictions and lower error metrics (e.g., reduced mean squared error for regression).
* Feature engineering can reduce bias by exposing relevant signals, which leads to better-optimized model parameters and improved generalization.
* Well-crafted features often allow simpler models to achieve competitive performance and reduce the need for deeper architectures.
* Training usually converges faster on feature-engineered data, meaning fewer epochs and less hyperparameter tuning.

No feature engineering vs. feature engineering

| Without feature engineering                    | With feature engineering                                 |
| ---------------------------------------------- | -------------------------------------------------------- |
| Weak signals; unclear feature importance       | Stronger predictive signals and interpretable importance |
| Higher risk of overfitting or underfitting     | Better generalization to new data                        |
| Slower convergence; may require complex models | Faster convergence; simpler models often suffice         |
| Higher evaluation error (e.g., MSE)            | Lower evaluation error and better-explained variance     |

Why improved features help generalization

Overfitting happens when a model learns noise or peculiarities in training data rather than underlying patterns. Effective feature engineering reduces this risk by surfacing meaningful relationships and removing spurious signals—helping the model perform well on unseen data.

> **lightbulb** Overfitting is when a model memorizes training examples and performs poorly on new data. Thoughtful feature engineering mitigates overfitting by exposing true predictive signals and reducing noisy or irrelevant inputs.

Interpretable examples: house price prediction

When predicting house prices, unprocessed datasets can make model behavior opaque. With targeted features—such as neighborhood indices, room counts, lot area, and engineered temporal features—you gain clearer visibility into why the model outputs a price and which factors drive it. Often, a small number of well-designed features explain most of the predictive power in housing datasets.

<Frame>
  <img alt="A slide titled &#x22;Results: Feature Engineering&#x22; showing a before-vs-after comparison: before — overfitting, good performance on training but poor generalization, and unclear why house prices are predicted; after — model generalizes to unseen data, learns patterns, and identifies features like location, number of rooms, and lot size." />
</Frame>

Handling common data issues during feature engineering

Feature engineering extends basic cleaning to address domain-specific problems. Typical concerns and approaches:

* Missing values: apply per-feature strategies such as mean/median imputation, KNN imputation, or model-based methods; consider adding a missing-value indicator.
* Outliers/extreme values: use clipping, winsorizing, trimming, or model-based handling depending on whether extremes are valid signals.
* Categorical variables: choose one-hot, ordinal, target/mean encoding, or learned embeddings based on cardinality and model type.

| Data issue                     | Typical fixes                                                           |
| ------------------------------ | ----------------------------------------------------------------------- |
| Missing values                 | Mean/median imputation, KNN, model-based imputation, missing indicators |
| Outliers/extremes              | Clipping, winsorizing, trimming, or model-aware handling                |
| High-cardinality categorical   | Target encoding, hashing, or embeddings                                 |
| Skewed numerical distributions | Log transforms, power transforms, or quantile transforms                |

These decisions influence both predictive performance and interpretability—so combine domain knowledge with algorithmic considerations when choosing strategies.

<Frame>
  <img alt="A presentation slide titled &#x22;Results: Feature Engineering&#x22; that compares handling data issues before and after feature engineering. The left column lists problems (missing values, extreme values, unused categorical data) and the right column shows fixes (proper imputation, outlier handling, encoding of non-numeric variables)." />
</Frame>

Domain-driven feature engineering examples

* Retail: Customer spend is often driven by seasonality or promotions rather than static income. Time-based features—month, week-of-year, holiday flags, rolling aggregates—can dramatically outperform raw income variables.
* Banking and fraud detection: Velocity and patterns (transactions per day, time since last transaction, anomalous sequence patterns) often indicate fraud more reliably than single-transaction amounts. Aggregate and ratio features are especially valuable.

Think in terms of business behavior and craft features that capture actions and trends rather than only static attributes.

<Frame>
  <img alt="A slide titled &#x22;Results: Feature Engineering&#x22; says well‑designed features reveal key factors influencing outcomes to aid domain experts. It highlights retail (customer spending depends more on seasonal trends than income) and banking (transaction frequency is a stronger fraud indicator than transaction amount)." />
</Frame>

Summary: practical takeaways and tools

Key takeaways

* Cleaned data is a necessary starting point but not sufficient—feature engineering extracts predictive signals that raw cleaning does not.
* Typical feature engineering steps: drop irrelevant variables, transform skewed features (log, power), synthesize new features (ratios, differences, timestamps to ages), and choose appropriate encodings.
* Consider the model family: tree-based models, linear models, and neural networks expect different feature representations (e.g., scaling matters more for linear and neural models than for many tree models).

Recommended libraries and compute patterns

| Resource                  | Use case                                             |
| ------------------------- | ---------------------------------------------------- |
| pandas                    | Tabular data manipulation and feature construction   |
| NumPy                     | Numerical operations and vectorized transforms       |
| scikit-learn              | Preprocessing pipelines, encoders, and transformers  |
| SageMaker Processing Jobs | Scalable, managed data transforms for large datasets |

For large-scale transformations (e.g., applying min-max scaling or computing rollups on millions of rows), use managed batch processing (for example, a SageMaker Processing Job) instead of running heavy operations in an interactive notebook—this avoids resource contention and speeds up reproducible pipelines.

Links and further reading

* [pandas](https://pandas.pydata.org/)
* [NumPy](https://numpy.org/)
* [scikit-learn](https://scikit-learn.org/)
* [SageMaker Processing Jobs](https://docs.aws.amazon.com/sagemaker/latest/dg/processing-job.html)
* [Kubernetes Documentation](https://kubernetes.io/docs/) (for orchestration and deployment patterns)

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; showing four numbered points about ML workflows. It lists that feature choices depend on the algorithm, uses Pandas/NumPy/scikit-learn, SageMaker Processing Jobs enable large-scale transformations, and this leads to better models and faster training." />
</Frame>

Next steps

This lesson closes the conceptual overview of feature engineering benefits and practical choices. In a follow-up article we'll demonstrate concrete feature transformations, show code examples and reproducible pipelines, and explain how to operationalize features for both training and inference.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/36db8fab-85cc-40f0-8594-573631b0425b/lesson/a04c3797-36a2-44bd-9c3e-977138553f31)
