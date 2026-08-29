# Demo Generate Dummy Data for the Project

Source: https://notes.kodekloud.com/docs/Fundamentals-of-MLOps/Automating-Insurance-Claim-Reviews-with-MLflow-and-BentoML/Demo-Generate-Dummy-Data-for-the-Project/page

This guide explains how to generate a synthetic healthcare claims dataset for analysis, including setup, data creation, and export to CSV.

Welcome to this guide on how to generate a synthetic healthcare claims dataset for your project. In this tutorial, you'll learn how to set up your development environment, create realistic synthetic data with anomalies, and export it to a CSV file for further analysis or model training.

***

## Step 1: Installing Required Packages

Begin by creating a new file named `requirements.txt` in your VS Code editor. Add the following package list to the file:

```text theme={null}
mlflow
pandas
numpy
bentoml
```

Save the file and open your terminal. Then run the command below to install all required packages:

```bash theme={null}
$ pip3 install -r requirements.txt
Collecting mlflow (from -r requirements.txt (line 1))
  Downloading mlflow-2.18.0-py3-none-any.whl.metadata (29 kB)
Requirement already satisfied: pandas in /home/codespace/.local/lib/python3.12/site-packages (from -r requirements.txt (line 2)) (2.2.3)
Requirement already satisfied: numpy in /home/codespace/.local/lib/python3.12/site-packages (from -r requirements.txt (line 3)) (2.1.1)
Collecting bentoml (from -r requirements.txt (line 4))
  Downloading bentoml-1.3.15-py3-none-any.whl.metadata (16 kB)
Collecting mlflow-skinny==2.18.0 (from mlflow->-r requirements.txt (line 1))
  Downloading mlflow_skinny-2.18.0-py3-none-any.whl.metadata (10 kB)
Downloading mlflow_skinny-2.18.0-py3-none-any.whl (30 kB)
```

The command above installs all dependencies mentioned in your `requirements.txt` file. Once the installation is complete, you are ready to move on to generating synthetic data.

***

## Step 2: Generating Synthetic Health Claims Data

Create a new Python file named `synthetic_health_claims.py`. This script generates a synthetic dataset with both normal claims and anomalous claims to simulate outlier events.

### How the Script Works

* Imports necessary libraries and sets a random seed for reproducibility.
* Generates 1,000 normal claim records with fields such as `claim_id`, `claim_amount`, `num_services`, `patient_age`, `provider_id`, and `days_since_last_claim`.
* Introduces 50 anomalous entries with significantly higher claim amounts and additional service counts.
* Combines, shuffles, and exports the dataset to a CSV file.

### Code Implementation

```python theme={null}
import pandas as pd
import numpy as np
