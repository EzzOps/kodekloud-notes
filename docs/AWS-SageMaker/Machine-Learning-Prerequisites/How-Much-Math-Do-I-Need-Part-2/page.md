# How Much Math Do I Need Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Machine-Learning-Prerequisites/How-Much-Math-Do-I-Need-Part-2/page

Explains min–max scaling, normalization, and standardization for preparing numerical features, when to use each technique, and scikit-learn examples.

When preparing numerical data for machine learning, one of the fundamental preprocessing steps is scaling. Feature scaling makes numeric attributes comparable so that models don't give undue importance to features that simply have larger numeric ranges.

This guide covers the three most common scaling techniques:

* Min–Max scaling (feature-wise)
* Normalization (row-wise / unit norm)
* Standardization (z-score, feature-wise)

We explain what each method does, when to use it, and include practical scikit-learn examples.

Why scale?

* Algorithms that rely on distances (k-NN, k-means, SVM) or gradient-based optimization often perform better when features are on similar scales.
* Without scaling, a feature with large numeric values (e.g., house size in square feet) can dominate another feature with smaller numeric ranges (e.g., number of bedrooms), even if both are equally informative.

Use case example: house price prediction with numeric features that differ in magnitude — house size (hundreds to thousands) and number of bedrooms (1–10). Scaling ensures no single feature dominates the model simply because of its numeric range.

<Frame>
  <img alt="A presentation slide titled &#x22;Scaling&#x22; showing the min–max scaling formula on the left. On the right are two feature panels for &#x22;House Size&#x22; and &#x22;No. of Bedrooms&#x22; with slider-like buttons showing normalized values 0.0, 0.25, 0.50, 0.75, and 1.0." />
</Frame>

***

## Min–Max Scaling (Feature-wise)

Min–Max scaling rescales each feature independently to a fixed range, typically \[0, 1]. This preserves the relationships among the original values but bounds them.

* Formula: x' = (x − min(x)) / (max(x) − min(x))
* Operates column-wise (feature-wise)
* Use case: When you need bounded inputs or your algorithm is sensitive to absolute value ranges (k-NN, SVM, neural networks with activation functions)

Example (scikit-learn MinMaxScaler):

```python theme={null}
from sklearn.preprocessing import MinMaxScaler

data = [[1], [2], [3], [4], [5]]  # Example single-feature values
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)
print(scaled_data)
