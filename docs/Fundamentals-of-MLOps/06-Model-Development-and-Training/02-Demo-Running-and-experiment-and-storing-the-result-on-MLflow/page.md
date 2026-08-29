# Demo Running and experiment and storing the result on MLflow

Source: https://notes.kodekloud.com/docs/Fundamentals-of-MLOps/Model-Development-and-Training/Demo-Running-and-experiment-and-storing-the-result-on-MLflow/page

This article demonstrates running a local experiment with MLflow, logging metrics, and analyzing results using scikit-learn.

Hello and welcome back.

In this lesson, we demonstrate how to run an experiment locally and store its results in an MLflow service configured earlier. We'll use scikit-learn for this example and learn how to log key metrics, store models, and view experiments in the MLflow UI.

Let’s jump into our VS Code editor.

## Preparing Your Environment

Before running any experiment, ensure you choose an appropriate use case and data science package. In this example, we use scikit-learn.

<Callout icon="triangle-alert">
  If you install scikit-learn in the same terminal session running the MLflow UI, the UI will stop. For example, executing:

  ```bash theme={null}
  $ mlflow ui
  [2024-11-05 18:33:22 +0000] [7842] [INFO] Starting gunicorn 23.0.0
  [2024-11-05 18:33:22 +0000] [7842] [INFO] Listening at: http://127.0.0.1:5000 (7842)
  [2024-11-05 18:33:22 +0000] [7842] [INFO] Using worker: sync
  [2024-11-05 18:33:22 +0000] [7848] [INFO] Booting worker with pid: 7848
  [2024-11-05 18:33:22 +0000] [7863] [INFO] Booting worker with pid: 7863
  [2024-11-05 18:33:22 +0000] [7864] [INFO] Booting worker with pid: 7864
  ```

  will halt the UI. Always open a new terminal for installing additional packages.
</Callout>

## Creating the Experiment File

Create a new file named `example_mlflow.py` in your VS Code editor and paste the code below. This script sets the MLflow tracking URI, creates synthetic regression data, splits it into training and testing sets, and defines a helper function to train models, make predictions, log metrics, and store models in MLflow.

```python theme={null}
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, explained_variance_score
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import mlflow
import mlflow.sklearn
import numpy as np
