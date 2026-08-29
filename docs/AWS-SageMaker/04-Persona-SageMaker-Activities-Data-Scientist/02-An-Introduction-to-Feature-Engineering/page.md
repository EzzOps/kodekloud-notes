# An Introduction to Feature Engineering

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-Data-Scientist/An-Introduction-to-Feature-Engineering/page

Introduction to feature engineering techniques with pandas and scikit-learn, covering encoding, transformations, aggregations, normalization, and SageMaker Processing for reproducible production pipelines

Feature engineering is the process of transforming prepared dataset columns into representations that are more useful for a chosen machine learning algorithm. It sits between dataset preparation (cleaning, imputation) and model training. Good feature engineering can improve predictive performance, reduce training time, and make models more robust.

<Frame>
  <img alt="A dark-blue presentation slide from KodeKloud. The title reads &#x22;Feature Engineering – Introduction&#x22; with the subtitle &#x22;Theory&#x22; and the KodeKloud logo at the top." />
</Frame>

We will show practical examples using pandas and scikit-learn and demonstrate how to scale these transformations using SageMaker Processing jobs. Typical feature-engineering tasks include encoding categorical variables, selecting or creating features, transforming skewed data, aggregating information, and scaling numeric inputs.

<Frame>
  <img alt="A presentation slide titled &#x22;Agenda&#x22; listing four items: Problem (prepared data may not be enough), Solution (apply feature engineering), Workflow (using Pandas, sklearn, and SageMaker Processing Jobs), and Results (better model performance and faster training). The design shows numbered blue markers down the left with the agenda text on a light background." />
</Frame>

## Why feature engineering matters

Even after basic cleaning (e.g., filling missing values), raw data often needs further transformation:

* Irrelevant or redundant features slow training and may reduce model quality.
* Noise or outliers can bias learning and harm generalization.
* Categorical features must be encoded in ways that reflect their semantics (ordinal vs nominal). Poor choices can mislead models.
* Strongly skewed numeric inputs can violate algorithmic assumptions and reduce performance.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Raw Data May Be Inadequate for ML&#x22; showing skewed data (unbalanced distribution, data bias) feeding an ML model. The right panel lists ML model impacts like affected assumptions and biased predictions." />
</Frame>

## Common feature-engineering activities

|                Activity | Purpose                                                                       | Typical methods / tools                                                 |
| ----------------------: | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
|       Feature selection | Remove irrelevant or redundant inputs to speed training and avoid overfitting | Correlation analysis, feature importance, recursive feature elimination |
|    Categorical encoding | Represent categorical data numerically                                        | One-hot, ordinal, target encoding, hashing, embeddings                  |
|      Feature extraction | Create informative features from raw values                                   | Date parts, text lengths, tokenization, embeddings                      |
|  Feature transformation | Reduce skew and stabilize variance                                            | log, sqrt, power transforms, Box-Cox                                    |
|    Feature interactions | Capture multiplicative or composite effects                                   | Multiplication, concatenation, polynomial features                      |
|  Aggregation / grouping | Add group-level statistics                                                    | groupby / pivot\_table (mean, sum, count)                               |
| Scaling / normalization | Put features on comparable scales                                             | StandardScaler, MinMaxScaler                                            |

<Callout icon="lightbulb">
  When features have very high cardinality (for example, postal codes or item IDs), prefer techniques that limit dimensionality (target encoding, hashing, or learned embeddings) instead of naive one-hot encoding, which explodes feature count.
</Callout>

## Hands-on examples (pandas + scikit-learn)

Start by loading a small sample dataset into a pandas DataFrame for local experimentation:

```python theme={null}
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
