# Load a CSV file into a DataFrame
data = pd.read_csv('example.csv')

# Display the first 5 rows of the dataset
print("Preview of the dataset:")
print(data.head())

# Check for missing values
print("\nMissing values in each column:")
print(data.isnull().sum())

# Fill missing values in a column with the mean
data['column_name'] = data['column_name'].fillna(data['column_name'].mean())

# Create a new column based on an existing one
data['new_column'] = data['column_name'] * 2

print("\nUpdated dataset preview:")
print(data.head())
```

scikit-learn provides standard preprocessing utilities (scalers, encoders) and many modeling algorithms. Example: standardizing features with StandardScaler.

```python theme={null}
from sklearn.preprocessing import StandardScaler

# Sample data: two features (e.g., height and weight)
data = [[1.8, 75], [1.6, 60], [1.7, 68], [1.5, 50]]

# Initialize the scaler
scaler = StandardScaler()

# Fit the scaler to the data and transform it
scaled_data = scaler.fit_transform(data)

print("Original data:")
print(data)

print("\nScaled data:")
print(scaled_data)
```

Using these tested implementations reduces the chance of bugs and speeds up experimentation.

## Outliers: detection and handling

An outlier is a value that deviates significantly from the rest of a distribution. Outliers can distort summary statistics such as the mean. For example:

2, 5, 7, 10, 15, 30, 8953

Including 8953 makes the mean \~1288.9 (misleading); excluding it yields a mean of 11.5 for the remaining values. Deleting data outright is not always appropriate—consider the cause and the downstream impact before removing values.

<Frame>
  <img alt="A slide titled &#x22;Handling Outliers&#x22; showing the dataset [2, 5, 7, 10, 15, 30, 8953] with 8953 highlighted as an extreme outlier. It illustrates that including the outlier produces a misleading mean (~1288) while excluding it gives a more representative mean (11.5)." />
</Frame>

When you detect an outlier, first validate it:

* Was it a data-entry error or a pipeline corruption? If so, correct or remove it.
* If the value is valid but extreme, choose a strategy: capping (Winsorization), clipping, transformation (log, sqrt), or use robust methods (robust scalers, median-based statistics).

Winsorization example: cap extreme values to a sensible threshold (e.g., replace 8953 with a value like 30) or use a transformation such as log to compress the range.

<Frame>
  <img alt="A slide titled &#x22;Handling Outliers&#x22; showing a numeric sequence with a large outlier (8953) labeled &#x22;Outlier is valid.&#x22; Below it is an explanation of capping (Winsorization) with the outlier replaced by a threshold value (30)." />
</Frame>

### IQR method (practical outlier detector)

The Interquartile Range (IQR) method is robust and easy to implement.

IQR steps:

* Sort data.
* Q2 = median (50th percentile).
* Q1 = median of the lower half (25th percentile).
* Q3 = median of the upper half (75th percentile).
* IQR = Q3 − Q1.
* Outlier bounds: \[Q1 − 1.5*IQR, Q3 + 1.5*IQR].

Example with \[2, 5, 7, 10, 15, 30, 90]:

* Sorted: \[2, 5, 7, 10, 15, 30, 90]
* Q1 = 5, Q2 = 10, Q3 = 30 → IQR = 25
* Bounds: \[-32.5, 67.5] → 90 is an outlier.

<Frame>
  <img alt="A slide illustrating how to compute the interquartile range (IQR) from the dataset [2, 5, 7, 10, 15, 30, 90]. It shows Q1=5, Q2=10, Q3=30, IQR=25, bounds -32.5 and 67.5, and flags 90 as an outlier." />
</Frame>

IQR detection and Winsorization with pandas and NumPy:

```python theme={null}
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler

# Sample data with an outlier
data = {'Feature': [1, 2, 3, 4, 5, 100]}  # 100 is an outlier
df = pd.DataFrame(data)

# Detect outliers using IQR
q1 = df['Feature'].quantile(0.25)
q3 = df['Feature'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

# Cap outliers using numpy.clip (Winsorization)
df['Feature_capped'] = np.clip(df['Feature'], lower_bound, upper_bound)

print("Q1:", q1, "Q3:", q3, "IQR:", iqr)
print("Lower bound:", lower_bound, "Upper bound:", upper_bound)
print("\nOriginal and capped values:")
print(df)
```

What this code does:

* Computes Q1 and Q3 using pandas quantile.
* Determines thresholds using the 1.5\*IQR rule.
* Uses np.clip to cap values to those thresholds (Winsorize).

Alternative strategies:

* Remove outliers if they are errors.
* Apply log or other transforms to reduce skew.
* Use RobustScaler in scikit-learn, which uses median and IQR for scaling.

<Callout icon="warning">
  Be careful removing data solely to improve model metrics. Validate outliers against domain knowledge—rare but correct observations may be important signals.
</Callout>

## Feature scaling: when and how

Feature scaling makes numeric features comparable. Algorithms that rely on distances (k-NN, clustering) or gradient updates (logistic regression, neural networks) benefit most.

Common scalers:

* StandardScaler: subtract mean, divide by standard deviation → zero mean, unit variance.
* MinMaxScaler: scale to \[0, 1] (or another fixed range).
* RobustScaler: subtract median, scale by IQR → less sensitive to outliers.

Choose based on data and algorithm:

* Use RobustScaler when outliers are present and you want robustness.
* Use StandardScaler for algorithms that assume Gaussian-like data or need standardized inputs.
* Use MinMaxScaler for bounded inputs (e.g., image pixel normalization to \[0,1]).

## Summary: what to prioritize

You do not need to master all mathematics before starting ML. Prioritize practical skills that improve model performance quickly:

* Basic statistics and exploratory data analysis (EDA)
* Handling missing values and outliers
* Encoding categorical variables correctly
* Applying appropriate scaling to numeric features

These skills will let you prepare robust datasets and train useful models. As you progress and need to optimize or invent models, deepen your study of linear algebra, probability, calculus, and numerical optimization.

Further reading and references:

* [scikit-learn preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
* [pandas user guide](https://pandas.pydata.org/docs/user_guide/index.html)
* [Amazon SageMaker examples and tutorials](https://github.com/aws/amazon-sagemaker-examples)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/40da1d46-e900-4426-973b-a9a38c3e505d/lesson/fa18dffb-5710-4faf-9abc-f3090d72c5fc" />
</CardGroup>


# ML Basics Fundamentals of Model Training and Inference Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Machine-Learning-Prerequisites/ML-Basics-Fundamentals-of-Model-Training-and-Inference-Part-2/page

Intro to multivariate linear regression using a car price example, covering feature encoding, scaling, training with gradient descent, and deploying models for inference

In the previous lesson we introduced linear regression with a single feature. Here we extend that to a more realistic dataset with multiple features. Using the car-price example, we show how feature encoding, scaling, training, and hosting come together to produce predictions.

## Multivariate inputs: moving to higher dimensions

Real datasets include many attributes: age, color, sunroof, mileage, alarm, and more. As you add features you move into higher-dimensional input space (five features ⇒ five dimensions). While visualization becomes difficult beyond three dimensions, the mathematics stays the same: the model combines numeric inputs with learned weights to make predictions.

To train models, every input must be numeric. Categorical and boolean features must be encoded; continuous features may need scaling. The diagram below illustrates encoding multiple car features before feeding them to a learning algorithm.

<Frame>
  <img alt="A slide diagram titled &#x22;Training With Multiple Features&#x22; showing example car features (Age, Color, Sunroof, Mileage, Alarm) being encoded into numerical data and then used for training a model. Two features (Color and Sunroof) are annotated as not having a numerical value and need encoding." />
</Frame>

## Encoding and preprocessing — best practices

Common encodings and preprocessing choices:

| Feature type            | Typical encoding                                 | When to use                                             |
| ----------------------- | ------------------------------------------------ | ------------------------------------------------------- |
| Categorical (unordered) | One-hot encoding                                 | Use for nominal categories like color                   |
| Categorical (ordered)   | Label / ordinal encoding                         | Use only when categories have natural order             |
| Boolean                 | 0 / 1                                            | Direct binary representation for flags (sunroof, alarm) |
| Numerical               | Scaling / normalization (standardize or min-max) | Keep feature magnitudes comparable (e.g., mileage)      |

Key points:

* One-hot is preferred for unordered categories to avoid implying an order.
* Boolean flags map cleanly to 0/1.
* Scale numeric features (e.g., express mileage in thousands or standardize) so learned weights have reasonable magnitudes.

## Feature symbols and weights

Assign a symbol to each input feature and a corresponding weight (coefficient) that indicates its influence:

* X1 = age
* X2 = color (encoded)
* X3 = sunroof (0/1)
* X4 = mileage
* X5 = alarm (0/1)

Weights w1 … w5 can be positive or negative. Some weights are expected to be large (e.g., mileage), others small (e.g., color). The next illustration highlights how mileage strongly influences price.

<Frame>
  <img alt="A slide titled &#x22;Training With Multiple Features&#x22; showing car features on the left (Age, Color, Sunroof, Mileage, Alarm) with Mileage highlighted. To the right are two car illustrations labeled with different mileages (100,000 vs 20,000) and corresponding prices (cheaper vs much more expensive)." />
</Frame>

## Linear model — combining features

A simple linear model predicts a target as a weighted sum of features plus a bias:

<Frame>
  <img alt="A slide titled &#x22;Training With Multiple Features&#x22; lists car-related features (Age, Color, Sunroof, Mileage, Alarm) paired with weights w1–w5. To the right is the linear model equation f(x) = w1x1 + w2x2 + w3x3 + w4x4 + w5x5 + b, showing how features are combined to make a prediction." />
</Frame>

Algebraically:

```python theme={null}
