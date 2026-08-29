# Example data
data = pd.DataFrame({
    'Neighborhood': ['Downtown', 'Suburbs', 'Rural'],
    'Price': [300000, 200000, 150000]
})

# One-hot encoding
encoder = OneHotEncoder(sparse_output=False)  # or sparse=False for older scikit-learn
encoded = encoder.fit_transform(data[['Neighborhood']])

# Add encoded features back to the DataFrame
encoded_columns = encoder.get_feature_names_out(['Neighborhood'])
encoded_df = pd.DataFrame(encoded, columns=encoded_columns)
data = pd.concat([data, encoded_df], axis=1).drop(columns=['Neighborhood'])

print(data)
```

Key notes:

* One-hot encoding removes implied order by creating independent binary features.
* It expands the feature space — each unique category becomes a column.

> **lightbulb** Use one-hot encoding for nominal categorical variables (no natural order). Be mindful that one-hot can significantly increase dimensionality when the category count grows.

## High cardinality and the downside of one-hot encoding

One-hot encoding works well for low-cardinality features, but when a categorical feature has many unique values (high cardinality) it produces a wide, sparse dataset. This can increase model complexity, memory usage, and training time without improving predictive power—especially for features such as postcodes, user IDs, or product SKUs.

<Frame>
  <img alt="A presentation slide titled &#x22;Target Encoding&#x22; shows a table illustrating one-hot encoding of postcodes for three IDs (columns for Postcode 1001/1002/1003 with 1s and 0s). A caption below notes that one-hot encoding creates a wide dataset with many columns for each unique postcode." />
</Frame>

When cardinality is high, consider compact encodings like target (mean) encoding or hashing tricks.

## Target encoding (mean encoding)

Target encoding replaces each category with a statistic of the target variable computed over that category—most commonly the mean target value. This reduces dimensionality while preserving the relationship between the categorical feature and the target.

Typical steps:

1. Group data by the categorical variable (e.g., postcode).
2. Compute the mean (or other statistic) of the target for each group.
3. Replace the categorical value with that statistic.

<Frame>
  <img alt="A presentation slide titled &#x22;Target Encoding&#x22; that lists three steps: group data by a categorical variable (e.g., postcode), calculate the mean (or other statistic) of the target (e.g., house price) for each group, and replace the categorical value with its mean target value. The steps are shown as three numbered boxes with brief explanations." />
</Frame>

Benefits:

* Dimensionality reduction: one numeric column instead of many indicator columns.
* Preserves a relationship between the categorical feature and the target.
* Efficient for high-cardinality features.

<Frame>
  <img alt="A presentation slide titled &#x22;Target Encoding&#x22; with three numbered panels. The panels list benefits: 01 Dimensionality reduction (one column instead of many), 02 Preserves relationships (captures connection between feature and target), and 03 Efficient (handles high cardinality better)." />
</Frame>

Example — replace postcodes with mean house price:

* Compute the mean house price per postcode.
* Substitute that mean as the encoded value for every row with that postcode.

<Frame>
  <img alt="A presentation slide titled &#x22;Target Encoding&#x22; showing a table that replaces postcodes with mean house prices. The table lists example postcodes (A1, B2, C3) with their house prices and the corresponding target-encoded mean values." />
</Frame>

Simple implementation with pandas:

```python theme={null}
import pandas as pd

# Example data
data = {
    'Postcode': ['A1', 'B2', 'A1', 'C3', 'B2'],
    'HousePrice': [300000, 250000, 320000, 150000, 270000]
}
df = pd.DataFrame(data)

# Global mean of house prices (fallback)
global_mean = df['HousePrice'].mean()

# Calculate the mean house price per postcode
postcode_means = df.groupby('Postcode')['HousePrice'].mean()

# Replace each postcode with its target mean and fill unseen with global mean
df['TargetEncodedPostcode'] = df['Postcode'].map(postcode_means).fillna(global_mean)

print(df)
```

Practical considerations:

* Smoothing: combine per-category statistics with the global statistic to reduce variance for rare categories.
* Handling unseen categories: use a global mean or a special fallback value.
* Use regularization or weight by category size to prevent noisy estimates from small groups.

> **warning** Target encoding can leak target information if applied naively (computing encodings on the full dataset). Prevent leakage using out-of-fold (cross-validated) encodings, train-only computations, or smoothing techniques.

## Quick comparison of encoding strategies

| Encoding method  | Best for                                           | Pros                                   | Cons                                                        |
| ---------------- | -------------------------------------------------- | -------------------------------------- | ----------------------------------------------------------- |
| Label encoding   | Ordinal categories                                 | Compact, simple                        | Imposes order that may be meaningless                       |
| One-hot encoding | Low-cardinality nominal categories                 | No implicit order, interpretable       | Can explode feature space for high cardinality              |
| Target encoding  | High-cardinality categories correlated with target | Compact, captures target relationships | Risk of target leakage, needs smoothing/out-of-fold schemes |

## Summary / Practical checklist

* Outliers: detect with methods like IQR; decide whether to drop, cap (Winsorize), or otherwise transform them.
* Scaling: pick scaling appropriate to model type — standardization (zero mean, unit variance), min-max scaling, or normalization (e.g., L2) for distance-based methods.
* Categorical data: convert categories to numeric values using an encoding strategy that matches the data and model:
  * Label encoding for ordinal categories.
  * One-hot encoding for low-cardinality nominal features.
  * Target encoding (with out-of-fold or smoothing) for high-cardinality features.
* Avoid leakage: never compute encodings on the full dataset before splitting; use cross-validation/out-of-fold approaches.
* Tools: use libraries like [pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/), and [scikit-learn](https://scikit-learn.org/stable/) for preprocessing tasks.

Useful references:

* [pandas documentation](https://pandas.pydata.org/)
* [NumPy documentation](https://numpy.org/)
* [scikit-learn preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)

We'll also take a look at why [AWS SageMaker](https://learn.kodekloud.com/user/courses/aws-sagemaker), the product, is seen as so mysterious and intimidating and help get you past that barrier.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/40da1d46-e900-4426-973b-a9a38c3e505d/lesson/59da636a-4af2-443c-b811-272436ab5966)


# How Much Math Do I Need

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Machine-Learning-Prerequisites/How-Much-Math-Do-I-Need/page

Explains practical amount of math needed for machine learning, prioritizing data preparation, basic statistics, encoding, outlier handling, scaling, and when deeper math is required

This lesson explains the amount of mathematics you need to be productive with machine learning (ML). We'll outline where math shows up across the ML workflow, point out which techniques are most useful for common tasks, and highlight practical steps you can apply immediately when preparing data, building models, and deploying them (for example, with SageMaker).

The goal is pragmatic: learn enough math to demystify model behavior, prepare data effectively, and produce reliable predictions. You do not need to master advanced mathematics up-front to get started; you can build useful models by focusing on data preparation, basic statistics, and standard preprocessing tools. If you later specialize as a data scientist, you can deepen your knowledge of linear algebra, probability, calculus, and optimization.

> **lightbulb** A pragmatic path: learn the math you need for practical steps today (data cleaning, encoding, scaling, evaluation). Deeper math (linear algebra, probability, optimization) is valuable later for advanced model design and research.

<Frame>
  <img alt="A slide titled &#x22;Which Math for Which Purpose?&#x22; comparing two lists: one for model development and optimization (Linear Algebra, Probabilities, Statistics, Calculus — e.g., differentiation, and Numerical Methods — e.g., gradient descent) and one for data preparation (Statistics, Linear Algebra, Encoding)." />
</Frame>

## Two realistic learning paths

Which path you choose depends on your role and goals. Below is a concise comparison.

| Role                        | Required math focus                                                       | Typical tasks                                                                                     |
| --------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Data Scientist              | Linear algebra, probability, statistics, calculus, numerical optimization | Build and customize models, tune hyperparameters, design new algorithms                           |
| SageMaker / ML Practitioner | Basic statistics, encoding techniques, data preparation, model evaluation | Prepare datasets, use built-in algorithms, integrate models into applications, deploy and monitor |

<Frame>
  <img alt="An infographic titled &#x22;How Much Math Do You Need for ML?&#x22; comparing two paths: the Data Scientist path (needs linear algebra, statistics, probability and deeper ML math) and the SageMaker User path (can use built-in algorithms, needs minimal math, and focuses on data preparation and model deployment)." />
</Frame>

If your aim is to be a model developer, invest time in linear algebra, probability, and statistics—these explain training behavior and model limitations. If your priority is rapid prototyping or deploying models into applications, concentrate on data preparation, evaluation, and leveraging tested implementations (for example, SageMaker built-ins).

Useful references:

* [Amazon SageMaker documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* [Pandas documentation](https://pandas.pydata.org/docs/)
* [scikit-learn documentation](https://scikit-learn.org/stable/)

## What happens during training (intuitively)

For tabular data, many models express predictions as functions of weighted inputs. A simple linear-style model looks like:

f(x) = w1*x1 + w2*x2 + w3\*x3 + ... + b

Training adjusts the weights (w1, w2, ...) and bias b to make predictions f(x) close to known target values. The model uses a loss function (e.g., mean squared error) to quantify prediction error and applies numerical optimization (such as gradient descent) to reduce that loss iteratively.

<Frame>
  <img alt="A slide titled &#x22;How Much Math Do You Need for ML?&#x22; illustrating a simple linear model: input features feed into f(x)=w1x1+w2x2+...+b to produce a predicted output which is compared to the actual output. Below are the steps: 1) adjust weights and bias, 2) repeat until loss is minimized." />
</Frame>

You do not need to derive optimization routines from scratch to use ML effectively, but understanding how they work helps with debugging, tuning, and diagnosing problems.

## Focus: data preparation techniques that matter most

For most practical ML tasks, applying a small set of preprocessing techniques will yield large improvements in model performance. Key techniques:

* Encoding: convert categorical variables into numeric representations (one-hot, ordinal, target encoding).
* Outlier management: detect and handle extreme values (capping, clipping, transforms, or robust methods).
* Feature scaling: standardization, min-max scaling, or robust scaling depending on algorithm sensitivity.

Which transforms matter depends on the algorithm. Linear and distance-based algorithms (k-NN, SVM, linear regression) are sensitive to feature scale; tree-based models (random forests, XGBoost) are less so.

<Frame>
  <img alt="A diagram titled &#x22;Data Preparation Math&#x22; showing raw data flowing into a &#x22;Transformed Data&#x22; box that lists Applying Encoding, Outlier Management, and Scaling Techniques. The transformed data then flows to an &#x22;ML Model Training&#x22; box." />
</Frame>

### Python tools commonly used

Pandas and scikit-learn are the standard libraries for preprocessing and basic modeling.

<Frame>
  <img alt="A presentation slide titled &#x22;Python Libraries&#x22; with the Python logo centered. Two rounded boxes below list &#x22;Pandas&#x22; (1) on the left and &#x22;Scikit Learn&#x22; (2) on the right." />
</Frame>

Pandas provides DataFrames for easy manipulation of tabular datasets. Example workflow using pandas:

```python theme={null}
import pandas as pd
