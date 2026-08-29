# Output:
# [[0.  ]
#  [0.25]
#  [0.5 ]
#  [0.75]
#  [1.  ]]
```

Use Min–Max when you want all features to share a common bounded scale (for instance, when feeding input into models or visualizations that assume 0–1 ranges).

***

## Normalization (Row-wise, Unit Norm)

Normalization rescales each sample (row) to unit length (norm = 1). This is a row-wise operation and is useful when vector direction matters more than magnitude — for example, cosine-similarity comparisons in NLP or when working with TF-IDF vectors.

* Formula: x' = x / ||x|| where ||x|| is typically the Euclidean (L2) norm
* Operates row-wise (sample-wise)
* Use case: Sparse data, text (TF-IDF), or any vector-space model where magnitude is irrelevant and only direction matters

<Frame>
  <img alt="A slide titled &#x22;Normalization Scaling&#x22; explaining that normalization scales each data row to length 1 and is used for sparse data (e.g., NLP, image pixels). It also shows the formula x' = x / ||x|| and notes dividing each value by the row's Euclidean norm." />
</Frame>

How the Euclidean norm works:

* For a row \[200000, 3], the L2 norm is sqrt(200000^2 + 3^2) ≈ 200000.x
* Dividing each element by that norm produces a unit-length vector (sum of squared components = 1)

Example (scikit-learn Normalizer):

```python theme={null}
import pandas as pd
from sklearn.preprocessing import Normalizer

# Example data: [house_price, num_bedrooms]
data = pd.DataFrame({
    'house_price': [200000, 300000, 400000, 500000, 600000],
    'num_bedrooms': [3, 4, 5, 6, 7]
})

normalizer = Normalizer()
normalized_data = normalizer.fit_transform(data)
normalized_df = pd.DataFrame(normalized_data, columns=data.columns)

print("Original data:\n", data)
print("\nNormalizer normalized data:\n", normalized_df)
```

> **lightbulb** Normalization is not the same as min–max scaling. Normalization rescales rows (samples) to unit length; min–max rescales features (columns) to a fixed range.

***

## Standardization (Z-score, Feature-wise)

Standardization centers each feature on zero mean and scales to unit variance. This is a column-wise transformation and is often the default preprocessing for many statistical and machine learning algorithms.

* Formula: z = (x − μ) / σ where μ is the feature mean and σ is the feature standard deviation
* Operates column-wise (feature-wise)
* Use case: Models that assume centered inputs or benefit from normalized variance (linear/logistic regression, SVM, PCA, gradient-based methods)

<Frame>
  <img alt="A presentation slide titled &#x22;Standardization Formula&#x22; showing the z-score equation z = (x − μ) / σ. It also lists that μ is the mean of the feature and σ is its standard deviation." />
</Frame>

Why standardize?

* Improves convergence for gradient-based optimizers
* Prevents features with larger numeric scales from dominating models
* Makes feature variances comparable

Example (scikit-learn StandardScaler):

```python theme={null}
from sklearn.preprocessing import StandardScaler

data = [[1], [2], [3], [4], [5]]  # Example single-feature values
scaler = StandardScaler()
standardized_data = scaler.fit_transform(data)
print("Standardized data:\n", standardized_data)
```

After standardization, most values are typically within a few standard deviations of the mean (not strictly limited to \[-1, 1]).

<Frame>
  <img alt="A slide titled &#x22;Understanding Standardization&#x22; showing two tables of house size and bedroom counts before and after standardization. The right table lists standardized z-scores and notes both features have mean 0 and standard deviation 1." />
</Frame>

Standardization and the normal distribution:

* For approximately normal features: \~68% of values fall within ±1σ, \~95% within ±2σ, and \~99.7% within ±3σ.
* Centering helps many algorithms behave more predictably and improves numerical stability.

<Frame>
  <img alt="A bell-shaped normal distribution chart titled &#x22;Understanding Standardization&#x22; showing the ±1σ, ±2σ, and ±3σ intervals with segment percentages (34.1%, 13.6%, 2.1%, 0.1%). It highlights that about 68% of values fall within ±1σ of the mean." />
</Frame>

<Frame>
  <img alt="A stylized normal (bell) curve titled &#x22;Understanding Standardization,&#x22; showing shaded regions and percentage labels for each standard-deviation band (34.1%, 13.6%, 2.1%, 0.1%) illustrating the 99.7% empirical rule." />
</Frame>

***

## Quick Comparison: Scaling vs Normalization vs Standardization

| Method                    | Goal                                                 | Focus                 | Output Range                              | When to use                                                                                                   |      |                   |                                                                          |                                                                               |
| ------------------------- | ---------------------------------------------------- | --------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ---- | ----------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| Min–Max Scaling           | Rescale features to a fixed range                    | Column-wise (feature) | Bounded, typically \[0, 1]                | When bounded inputs are required or for algorithms sensitive to absolute ranges (k-NN, SVM, neural nets)      |      |                   |                                                                          |                                                                               |
| Normalization (Unit norm) | Scale each sample to unit length (                   |                       | x                                         |                                                                                                               | = 1) | Row-wise (sample) | Usually values in \[0,1] for non-negative data; interpreted as direction | For sparse or text data (TF-IDF) and when cosine similarity/direction matters |
| Standardization (Z-score) | Center features to mean 0 and scale to unit variance | Column-wise (feature) | Unbounded, usually within a few σ of mean | For algorithms that assume centered inputs or use variance information (linear/logistic regression, SVM, PCA) |      |                   |                                                                          |                                                                               |

<Frame>
  <img alt="A slide titled &#x22;Comparison&#x22; showing a table that compares three preprocessing techniques—Scaling, Normalization, and Standardization—by their goal, range, focus (columns or rows), and when to use them. The table highlights differences like scaling to a specific range (e.g., 0–1), normalization giving row unit length, and standardization centering data to mean=0, std=1." />
</Frame>

***

## Summary & Recommendations

* Choose Min–Max scaling when you need bounded features (0–1) or are feeding values to models sensitive to absolute ranges.
* Use Normalization (unit norm) when working with sparse vectors or text (TF-IDF), and when only vector direction matters.
* Prefer Standardization for algorithms that assume zero-mean or when stabilizing and speeding up gradient-based training.

Further reading and references:

* [scikit-learn: MinMaxScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html)
* [scikit-learn: Normalizer](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.Normalizer.html)
* [scikit-learn: StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)
* [Kubernetes Basics — for related deployment examples (if deploying models)](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

This lesson covered min–max scaling, normalization, and standardization — how they work, why they matter, and practical examples using scikit-learn. Choose the technique that matches your data characteristics and the algorithm’s sensitivity to feature scales.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/40da1d46-e900-4426-973b-a9a38c3e505d/lesson/e8f396cd-7b54-4690-ae78-ae27bb25ab81)


# How Much Math Do I Need Part 3

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Machine-Learning-Prerequisites/How-Much-Math-Do-I-Need-Part-3/page

Describes categorical encoding methods for machine learning, comparing label, one-hot, and target encoding, with advice on high cardinality, smoothing, and preventing target leakage

Encoding is the final data-transformation technique covered here that relies on basic mathematical ideas. Encoding converts categorical (text) features into numeric values so most machine learning algorithms (which operate on numbers) can use them. For example, categorical color labels like "red" or "green" must be converted into numeric representations such as 0, 1, 2 before training.

Why encoding matters:

* Machine learning models require numeric input.
* Different encoding strategies introduce different assumptions (e.g., order vs. independence).
* Choosing the right encoding affects model performance, dimensionality, and risk of leakage.

## Label encoding

Label encoding assigns a unique integer to every category in a feature. Consider a `Neighborhood` feature with values "Downtown", "Suburbs", and "Rural". Label encoding might map these to 1, 2, and 3 respectively:

<Frame>
  <img alt="The image is a &#x22;Label Encoded&#x22; diagram showing neighborhood categories (Downtown, Suburbs, Rural) mapped to numeric labels 1, 2, and 3. A caption advises using the encoded numerical feature of neighborhood for training the model." />
</Frame>

Example mapping:

* Downtown → 1
* Suburbs → 2
* Rural → 3

After encoding you can drop the original categorical column and keep the numeric labels for training.

Pros:

* Simple and compact (single column).

Cons:

* Imposes an ordinal relationship (1 \< 2 \< 3) that may not be meaningful. Models could interpret the numeric order as a ranking or distance, biasing predictions.

When to use:

* When the categorical variable is ordinal (has a meaningful order), or when the algorithm you use can handle nominal labels without misinterpreting ordering.

## One-hot encoding

To avoid introducing a false order, one-hot encoding creates binary indicator columns (flags) for each category. For `Neighborhood` you would create `Neighborhood_Downtown`, `Neighborhood_Suburbs`, and `Neighborhood_Rural`. Each row has a 1 for the category it belongs to and 0 for the others. After adding the new columns you drop the original categorical column.

Example using scikit-learn:

```python theme={null}
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
