# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic normal claim data
num_samples = 1000
data = {
    'claim_id': np.arange(1, num_samples + 1),
    'claim_amount': np.random.normal(1000, 250, num_samples),
    'num_services': np.random.randint(1, 10, num_samples),
    'patient_age': np.random.randint(18, 90, num_samples),
    'provider_id': np.random.randint(1, 50, num_samples),
    'days_since_last_claim': np.random.randint(0, 365, num_samples),
}

# Convert normal data to DataFrame
df = pd.DataFrame(data)

# Introduce anomalies (e.g., very high claim amounts)
num_anomalies = 50
anomalies = {
    'claim_id': np.arange(num_samples + 1, num_samples + num_anomalies + 1),
    'claim_amount': np.random.normal(10000, 2500, num_anomalies),  # Much higher amounts
    'num_services': np.random.randint(10, 20, num_anomalies),
    'patient_age': np.random.randint(18, 90, num_anomalies),
    'provider_id': np.random.randint(1, 50, num_anomalies),
    'days_since_last_claim': np.random.randint(0, 365, num_anomalies),
}

# Convert anomalies to DataFrame
df_anomalies = pd.DataFrame(anomalies)

# Combine and shuffle the dataset
df = pd.concat([df, df_anomalies]).reset_index(drop=True)
df = df.sample(frac=1).reset_index(drop=True)

# Save the dataset to CSV
df.to_csv('synthetic_health_claims.csv', index=False)
print("Synthetic data generated and saved to 'synthetic_health_claims.csv'.")
```

To run the script, execute the following command in your terminal:

```bash theme={null}
$ python3 synthetic_health_claims.py
Synthetic data generated and saved to 'synthetic_health_claims.csv'.
```

<Callout icon="lightbulb">
  This script creates a balanced dataset containing both normal and anomalous data points, ideal for training and testing anomaly detection models.
</Callout>

***

## Step 3: Preparing Data for Model Experiment

After generating the initial synthetic dataset, you might want to simulate a different testing scenario by modifying the dataset. In this step, we introduce a smaller set of anomalies (5 records) and omit the `num_services` field to tailor the dataset for a specific model experiment.

### Code Implementation for Model Experiment

```python theme={null}
import pandas as pd
import numpy as np

# Assumption: The normal data (df) and the variable num_samples (e.g., num_samples = 1000)
# Introduce a smaller set of anomalies for the experiment
num_anomalies = 5
anomalies = {
    'claim_id': np.arange(num_samples + 1, num_samples + num_anomalies + 1),
    'claim_amount': np.random.normal(10000, 2500, num_anomalies),  # Significantly higher amounts
    'patient_age': np.random.randint(10, 20, num_anomalies),
    'provider_id': np.random.randint(1, 50, num_anomalies),
    'days_since_last_claim': np.random.randint(0, 365, num_anomalies)
}

# Convert new anomalies to a DataFrame
df_anomalies = pd.DataFrame(anomalies)

# Combine with the existing data
df = pd.concat([df, df_anomalies]).reset_index(drop=True)

# Save the updated dataset to CSV
df.to_csv('synthetic_health_claims.csv', index=False)
print("Synthetic data for the experiment generated and saved to 'synthetic_health_claims.csv'.")
```

Run the updated script with the command below:

```bash theme={null}
$ python3 synthetic_health_claims.py
Synthetic data for the experiment generated and saved to 'synthetic_health_claims.csv'.
```

<Callout icon="lightbulb">
  The modified dataset now includes an updated anomaly configuration, which is useful for various experimental setups in model validation.
</Callout>

***

In this guide, we demonstrated how to create a comprehensive synthetic dataset with both normal and anomalous healthcare claims. The resulting CSV file, `synthetic_health_claims.csv`, can now be used in your data analysis or machine learning projects. For more insights on data preparation and anomaly detection, explore our related articles and documentation.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/e6813732-5ba7-496f-84db-2272a4c2b188/lesson/a7c02846-a52c-46ed-b9c5-ab142d3f0a65" />
</CardGroup>


# Demo Register the Model and Setup BentoML for Serving ML Models

Source: https://notes.kodekloud.com/docs/Fundamentals-of-MLOps/Automating-Insurance-Claim-Reviews-with-MLflow-and-BentoML/Demo-Register-the-Model-and-Setup-BentoML-for-Serving-ML-Models/page

This tutorial covers registering a machine learning model with BentoML and deploying a service for predictions.

Welcome to this tutorial on serving machine learning models with BentoML. In this guide, you'll learn how to download a model, register it with BentoML, and deploy a service to handle predictions. This step-by-step lesson is designed for improved performance tracking and production-grade serving.

────────────────────────────────────────
Step 1: Download and Prepare the Model
────────────────────────────────────────

Begin by downloading your machine learning model (for example, a pickle file named `model.pkl`) from your chosen source. Once downloaded, place the model file into your project's root directory using VS Code or your preferred editor.

────────────────────────────────────────
Step 2: Register the Model with BentoML
────────────────────────────────────────

Create a Python script (e.g., `register_model.py`) to load your pickle file and register it with BentoML. Use the code below:

```python theme={null}
import bentoml
import pickle
