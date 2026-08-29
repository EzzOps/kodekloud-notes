# Load the model from the downloaded pickle file
model_path = "model.pkl"  # Update the path if needed
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

# Save the model to BentoML with a unique name
bento_model = bentoml.sklearn.save_model("health_insurance_anomaly_detector", model)

print(f"Model registered with BentoML: {bento_model}")
```

Run the script by executing:

```bash theme={null}
$ python3 register_model.py
```

If the model registration is successful, you'll see output similar to the following:

```plaintext theme={null}
2024/12/03 11:22:46 INFO mlflow.tracking.fluent: Experiment with name 'Health Insurance Claim Anomaly Detection' does not exist. Creating a new experiment.
2024/12/03 11:22:49 WARNING mlflow.models.model: Model logged without a signature and input example. Please set 'input_example' parameter when logging the model to auto infer the model signature.
Train Anomaly Percentage: 5.29%
Test Anomaly Percentage: 4.29%
Model metrics logged to MLflow.
View run bidi-... at http://127.0.0.1:5000/#/experiments/199595116865516564/runs/t8d3fcbfd4496503aeb75f4feeb7f
✅ Experiment at: http://127.0.0.1:5000/#/experiments/199595116865516564
Model registered with BentoML: health_insurance_anomaly_detector:your_model_tag_here
```

> **lightbulb** This output confirms successful integration with both MLflow (for experiment tracking) and BentoML (for model serving).

────────────────────────────────────────
Step 3: Verify Registration in BentoML
────────────────────────────────────────

After registration, ensure that the model is stored in the BentoML registry. Execute the following command:

```bash theme={null}
$ bentoml models list
```

A typical output should show your model details:

```plaintext theme={null}
Tag                                         Module          Size    Creation Time
health_insurance_anomaly_detector:5gxztv(rnq95z76)  bentoml.sklearn  1.39 MiB  2024-12-03 11:29:59
```

This confirms that your model artifact is securely stored in the BentoML repository. Although multiple experiments might be tracked with MLflow, only the model registered in BentoML is used for serving.

────────────────────────────────────────
Step 4: Create the BentoML Service for Serving
────────────────────────────────────────

Define a service to serve your model by creating a file (e.g., `service.py`) with the following content:

```python theme={null}
import bentoml
from bentoml.io import JSON, PandasDataFrame

# Load the registered model from BentoML registry using the latest version.
model_runner = bentoml.sklearn.get("health_insurance_anomaly_detector:latest").to_runner()

# Create a BentoML service and attach the model runner.
svc = bentoml.Service("health_insurance_anomaly_detection_service", runners=[model_runner])

# API endpoint for prediction using a Pandas DataFrame as input and JSON as output.
@svc.api(input=PandasDataFrame(), output=JSON())
def predict(data):
    predictions = model_runner.predict.run(data)
    return {"predictions": predictions.tolist()}
```

This service creates an endpoint (`/predict`) that accepts feature data in a Pandas DataFrame format and returns predictions in JSON.

────────────────────────────────────────
Step 5: Running the BentoML Service
────────────────────────────────────────

Start the BentoML service with live-reloading enabled to pick up any local changes automatically. Run:

```bash theme={null}
$ bentoml serve service.py --reload
```

By default, BentoML serves on port 3000. Open your browser and navigate to the BentoML UI. You will see the `/predict` endpoint readily available.

The API endpoint specifications are as follows:

| Endpoint      | Input           | Output |
| ------------- | --------------- | ------ |
| POST /predict | PandasDataFrame | JSON   |

> **lightbulb** This endpoint is intended for receiving feature data (for instance, from a CSV file uploaded by an insurance claims agent) and returning prediction results.

────────────────────────────────────────
Next Steps
────────────────────────────────────────

In this lesson, you registered a machine learning model with BentoML and created a simple prediction API. In the upcoming lesson, you'll learn how to integrate this API into a web application so insurance claims agents can upload CSV files and receive predictions effortlessly.

Happy serving!

For more information, refer to the official [BentoML Documentation](https://docs.bentoml.org/) and [MLflow Documentation](https://mlflow.org/docs/).

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/e6813732-5ba7-496f-84db-2272a4c2b188/lesson/79edd427-b092-42e5-9eb3-3af706b5f3ad)


# Demo Setup MLflow server and run the ML Experiment

Source: https://notes.kodekloud.com/docs/Fundamentals-of-MLOps/Automating-Insurance-Claim-Reviews-with-MLflow-and-BentoML/Demo-Setup-MLflow-server-and-run-the-ML-Experiment/page

This guide covers setting up an MLflow server and running a machine learning experiment for anomaly detection using synthetic health insurance claims data.

Welcome to this guide on setting up an MLflow server and running an end-to-end machine learning experiment. In this demo, we simulate health insurance claims data (with injected anomalies) and build an anomaly detection model using the Isolation Forest algorithm. Follow along to set up your MLflow server in VS Code, generate synthetic data, train a model, and log results to MLflow.

> **lightbulb** Before you begin, ensure that you have VS Code and the required Python libraries installed. This guide assumes you have the necessary setup to run MLflow and execute Python scripts.

***

## 1. Setting Up MLflow

Begin by launching the MLflow UI. Open the terminal in VS Code and run:

```bash theme={null}
mlflow ui
```

After executing the command, MLflow will start, and a pop-up notification should appear. Click on "open browser" to verify that the MLflow web UI is accessible. Once confirmed, create a new terminal in VS Code to continue with the next steps.

***

## 2. Generating Synthetic Data

If you haven't already generated the synthetic data, run the provided script. This script simulates health insurance claims, including some injected anomalies. Create a file named `synthetic_health_claims.py` and add the following content:

```python theme={null}
import pandas as pd
import numpy as np
