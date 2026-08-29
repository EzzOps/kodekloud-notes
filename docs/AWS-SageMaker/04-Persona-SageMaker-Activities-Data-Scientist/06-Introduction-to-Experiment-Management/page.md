# notebook: train_linear_learner.py
import os
import pandas as pd
from sklearn.model_selection import train_test_split

import sagemaker
from sagemaker import get_execution_role
from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput

# Initialize SageMaker session and role
sagemaker_session = sagemaker.Session()
role = get_execution_role()

# Define the S3 bucket and prefix for storing data (use a consistent prefix)
bucket = sagemaker_session.default_bucket()
prefix = 'house-price-linear-learner-demo'

print(f"Using bucket: {bucket}")

# Load the dataset (assumes 'preprocessed.csv' is present in the notebook filesystem)
df = pd.read_csv('preprocessed.csv')

# Separate features and target
target_col = 'saleEstimate_currentPrice'
X = df.drop(columns=[target_col])
y = df[target_col]

# Split the data into train (~70%), validation (~20%), and test (~10%) using a two-step split
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
# X_temp is ~30% of data; here we split it so validation is ~20% and test is ~10% of the original
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.33, random_state=42)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Validation set: {X_val.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Recombine target as first column (many SageMaker built-in algos expect label in first column)
train_data = pd.concat([y_train.reset_index(drop=True), X_train.reset_index(drop=True)], axis=1)
val_data = pd.concat([y_val.reset_index(drop=True), X_val.reset_index(drop=True)], axis=1)
test_data = pd.concat([y_test.reset_index(drop=True), X_test.reset_index(drop=True)], axis=1)

# Save locally (no headers, no index for train/validation as required by many built-in algorithms)
os.makedirs('data', exist_ok=True)
train_csv = 'data/train.csv'
val_csv = 'data/validation.csv'
test_csv = 'data/test.csv'

train_data.to_csv(train_csv, index=False, header=False)
val_data.to_csv(val_csv, index=False, header=False)
test_data.to_csv(test_csv, index=False, header=False)

# Upload to S3
train_path = sagemaker_session.upload_data(train_csv, bucket=bucket, key_prefix=f'{prefix}/train')
val_path = sagemaker_session.upload_data(val_csv, bucket=bucket, key_prefix=f'{prefix}/validation')
test_path = sagemaker_session.upload_data(test_csv, bucket=bucket, key_prefix=f'{prefix}/test')

print(f"Train data uploaded to: {train_path}")
print(f"Validation data uploaded to: {val_path}")
print(f"Test data uploaded to: {test_path}")

# Retrieve the Linear Learner container image URI for the current region
linear_learner_container = sagemaker.image_uris.retrieve('linear-learner', sagemaker_session.boto_region_name)
```

Define the Estimator, set hyperparameters, and start training

* Below we configure the Estimator to use a single ml.m5.large instance for demonstration. Adjust instance type and count for larger jobs.

<Frame>
  <img alt="Screenshot of a JupyterLab/SageMaker workspace showing a CSV file (preprocessed.csv) preview with a left file browser and a large table of property data columns like latitude, longitude, bathrooms, bedrooms, floorAreaSqM and price. A mouse cursor highlights one of the cells in the table." />
</Frame>

```python theme={null}
# Define the LinearLearner estimator
linear_estimator = Estimator(
    image_uri=linear_learner_container,
    role=role,
    instance_count=1,
    instance_type='ml.m5.large',
    output_path=f's3://{bucket}/{prefix}/output',
    sagemaker_session=sagemaker_session
)

# Set hyperparameters for Linear Learner (regression)
linear_estimator.set_hyperparameters(
    predictor_type='regressor',  # regression task
    mini_batch_size=32,
    epochs=10
)

# Specify the input data channels for CSV files
train_input = TrainingInput(s3_data=train_path, content_type='text/csv')
val_input = TrainingInput(s3_data=val_path, content_type='text/csv')

# Start training
linear_estimator.fit({'train': train_input, 'validation': val_input})
```

Monitoring and model artifacts

* SageMaker creates a managed training job and provisions the compute instance(s). Monitor progress from SageMaker Studio (Jobs > Training) or the SageMaker Console training jobs page. Logs stream to the notebook cell output and include metrics such as validation RMSE and MSE.
* After training completes, the model artifact (model.tar.gz) is saved to the configured S3 output prefix.

<Frame>
  <img alt="A screenshot of the Amazon SageMaker Studio web interface showing a running training job named &#x22;linear-learner-2025-05-06-13-48-11-566&#x22; with the Hyperparameters tab displayed. The table lists hyperparameter names like epochs, mini_batch_size and predictor_type (set to &#x22;regressor&#x22;), and a large cursor is visible." />
</Frame>

Verify model artifact in the S3 Console (look under the training job's output prefix for model.tar.gz).

<Frame>
  <img alt="A screenshot of the Amazon S3 console showing the &#x22;output/&#x22; folder containing a single object named &#x22;model.tar.gz&#x22; (1.2 KB, last modified May 6, 2025). The UI shows S3 navigation on the left and action buttons (Copy S3 URI, Download, Open, Delete) across the top." />
</Frame>

Hyperparameter tuning to run many training jobs in parallel

* Define ranges for the hyperparameters you want SageMaker to explore (ContinuousParameter or IntegerParameter).
* Create a HyperparameterTuner and call fit(); the tuner launches multiple training jobs (up to max\_parallel\_jobs concurrently) and returns the best training job according to the specified objective metric.

```python theme={null}
from sagemaker.tuner import IntegerParameter, ContinuousParameter, HyperparameterTuner

# Define Hyperparameter Ranges to Tune
hyperparameter_ranges = {
    "learning_rate": ContinuousParameter(0.001, 0.1),
    "mini_batch_size": IntegerParameter(16, 512),
    "wd": ContinuousParameter(0.0001, 0.1),  # weight decay
}

# Create the Hyperparameter Tuner
tuner = HyperparameterTuner(
    estimator=linear_estimator,
    objective_metric_name="validation:rmse",
    objective_type="Minimize",
    hyperparameter_ranges=hyperparameter_ranges,
    max_jobs=6,            # total number of training jobs to run
    max_parallel_jobs=2,   # how many jobs to run in parallel
    strategy="Bayesian",   # Bayesian optimization strategy
)

# Launch the hyperparameter tuning job (this call blocks until the tuning job completes by default)
tuner.fit({"train": train_input, "validation": val_input})
print(f"Tuning job launched: {tuner.latest_tuning_job.name}")
```

<Callout icon="lightbulb">
  By default tuner.fit(...) waits until the tuning job finishes and blocks the notebook cell. To launch asynchronously, call tuner.fit(..., wait=False) so you can continue other work while the tuner runs.
</Callout>

Retrieve the best tuning job programmatically

* After tuning completes, use Boto3 or the SageMaker SDK to describe the tuning job and obtain the BestTrainingJob and its objective metric.

```python theme={null}
import boto3

tuning_job_name = tuner.latest_tuning_job.name
sm_client = boto3.client('sagemaker')

tuning_job_info = sm_client.describe_hyper_parameter_tuning_job(
    HyperParameterTuningJobName=tuning_job_name
)

best_training_job = tuning_job_info['BestTrainingJob']
best_model_job_name = best_training_job['TrainingJobName']
best_model_score = best_training_job['FinalHyperParameterTuningJobObjectiveMetric']['Value']

print(f"✅ Best model: {best_model_job_name} with score: {best_model_score}")
```

Practical notes and troubleshooting

* If your model shows large RMSE values, investigate feature scaling, outliers, target distribution, and whether a linear model is appropriate. Hyperparameter tuning speeds up exploration but cannot replace good feature engineering and the right model choice.
* Many built-in algorithms expect the label as the first column and CSV inputs without headers or index — ensure you follow the input formatting expected by the chosen algorithm.
* For faster iteration, use smaller subsets of data or fewer epochs during development, then scale up for final training runs.

Summary — what you accomplished

* Created a SageMaker training job with the Python SDK Estimator class.
* Retrieved the built-in Linear Learner container image and provided it to a generic Estimator.
* Uploaded train/validation/test CSVs to S3 and started training with estimator.fit(...).
* Launched a HyperparameterTuner to try multiple hyperparameter combinations in parallel and retrieved the best model.
* Verified the model artifact saved to S3 (model.tar.gz).

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; showing five numbered points about an ML training workflow. The points highlight a simplified training process, an Estimator class, hyperparameter control, familiar .fit() syntax, and scalable training for parallel hyperparameter tuning." />
</Frame>

Quick reference and links

| Resource                        | Purpose                                                     | Link                                                                                                                                                                                                           |
| ------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SageMaker Python SDK            | API reference for Estimator, inputs, and training workflows | [https://sagemaker.readthedocs.io/en/stable/](https://sagemaker.readthedocs.io/en/stable/)                                                                                                                     |
| Estimator class docs            | API for creating and running training jobs                  | [https://sagemaker.readthedocs.io/en/stable/api/training/estimators.html#sagemaker.estimator.Estimator](https://sagemaker.readthedocs.io/en/stable/api/training/estimators.html#sagemaker.estimator.Estimator) |
| SageMaker Hyperparameter Tuning | Tuner and strategies                                        | [https://sagemaker.readthedocs.io/en/stable/tuner.html](https://sagemaker.readthedocs.io/en/stable/tuner.html)                                                                                                 |
| Linear Learner algorithm        | Built-in algorithm overview for regression/classification   | [https://docs.aws.amazon.com/sagemaker/latest/dg/linear-learner.html](https://docs.aws.amazon.com/sagemaker/latest/dg/linear-learner.html)                                                                     |
| SageMaker Studio                | Studio overview and getting started                         | [https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html)                                                                                     |
| Boto3 SageMaker client          | Programmatic access to tuning job metadata                  | [https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html)                         |
| Amazon S3 Console guide         | Managing S3 artifacts and objects                           | [https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-console.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-console.html)                                                           |

Recommended next steps

* Try different instance types (e.g., ml.m5.2xlarge) and compare training time vs cost.
* Replace Linear Learner with other built-in algorithms or your own training container to evaluate model performance.
* Integrate model evaluation and model deployment (SageMaker endpoints or batch transform) as the next phase after training.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/36db8fab-85cc-40f0-8594-573631b0425b/lesson/f4417504-030b-41ea-b447-69ee00d7a012" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/36db8fab-85cc-40f0-8594-573631b0425b/lesson/2627dea6-db04-42c0-8379-874658b9f292" />
</CardGroup>


# Introduction to Experiment Management

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-Data-Scientist/Introduction-to-Experiment-Management/page

Guide to using Amazon SageMaker Experiments to track, log, and reproduce machine learning runs using the SDK, Run contexts, and compare results across trials.

In this lesson we cover Amazon SageMaker Experiments — a structured way to track iterative machine learning runs across datasets, algorithms, and hyperparameter combinations. Experiment management addresses the common challenge of rapidly iterating models and losing reproducibility or provenance for a particular training run.

What you'll learn:

* The problem of tracking iterative experiments in SageMaker Studio.
* How SageMaker Experiments helps with tracking and reproducibility.
* A code-first workflow using the SageMaker SDK.
* How to capture and compare runs to reproduce results.

<Frame>
  <img alt="A presentation slide titled &#x22;Agenda&#x22; with four numbered items. It lists: Problem — keeping track of iterative experiments in SageMaker Studio; Solution — using SageMaker Experiments; Workflow — utilizing SageMaker SDK classes; Results — ensuring reproducibility." />
</Frame>

## The problem: many iterative experiments, poor traceability

Data scientists and ML engineers routinely run multiple experiments that differ by:

* Model type (e.g., RandomForest, XGBoost)
* Hyperparameters and optimization schedules
* Feature engineering or preprocessing pipelines
* Dataset versions or label corrections

Example runs:

* Experiment 1: RandomForest with scaling and PCA
* Experiment 2: XGBoost without scaling with a different learning rate
* Experiment 3: XGBoost with alternate hyperparameters and feature set

Each run produces metrics (accuracy, RMSE, F1, etc.) and artifacts (trained model, logs). Without a structured tracking system, it is easy to lose which configuration produced the best model or how to reproduce a prior run.

<Frame>
  <img alt="A slide titled &#x22;Problem: Tracking Iterative Experiments&#x22; illustrating three example ML experiments that list model types (Random Forest, XGBoost), hyperparameters, datasets, and feature-engineering choices. It emphasizes how data scientists and ML engineers run multiple experiments to find the best model." />
</Frame>

Common ad-hoc solutions — spreadsheets, notes, ad-hoc directory naming — are error-prone and often omit important details such as algorithm/container versions, dataset commits, or the exact preprocessing code path.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Tracking Iterative Experiments&#x22; with a section &#x22;Without a Proper Structure.&#x22; It lists four issues: losing track of best settings, storing logs manually in spreadsheets, struggling to compare results, and difficulty reproducing experiments." />
</Frame>

## Solution: experiment management with SageMaker Experiments

SageMaker Experiments provides a built-in mechanism to record metadata, hyperparameters, metrics, and artifacts for each run so you can compare, analyze, and reproduce experiments.

Note: AWS Studio experiences are evolving. Some newer Studio versions surface MLflow integration or other experiment UIs instead of the native SageMaker Experiments dashboard. Confirm your Studio configuration and roadmap when selecting a tracking approach for long-term projects.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Using Experiment Management&#x22; warning about &#x22;SageMaker Experiments Uncertainty.&#x22; It lists three points: SageMaker Experiments worked well until mid‑2024, is now only visible in SageMaker Studio Classic (no longer supported), and the new SageMaker UI redirects to MLflow instead of SageMaker Experiments." />
</Frame>

<Callout icon="warning">
  SageMaker Studio Classic continues to expose the original SageMaker Experiments UI, but newer Studio experiences increasingly surface MLflow or third‑party integrations. Consider this when choosing an experiment-management tool for long‑term projects.
</Callout>

There are also popular third-party and open-source experiment-management systems that integrate with SageMaker:

| Tool                    | Type                            | Notes / Link                                                                                 |
| ----------------------- | ------------------------------- | -------------------------------------------------------------------------------------------- |
| MLflow                  | Open-source experiment tracking | [mlflow.org](https://mlflow.org/) — widely adopted and supported in some Studio experiences. |
| Weights & Biases (W\&B) | Commercial / hosted             | [wandb.ai](https://wandb.ai/) — rich visualizations, collaboration features.                 |
| Neptune AI              | Commercial / hosted             | [neptune.ai](https://neptune.ai/) — experiment metadata store and visualizations.            |
| TensorBoard             | Visualization                   | [TensorBoard](https://www.tensorflow.org/tensorboard) — common for TensorFlow workflows.     |
| ClearML                 | Open-source                     | [clear.ml](https://clear.ml/) — tracking, orchestration, and dataset management.             |

Why use experiment management?

* Automatically capture algorithm/container versions, hyperparameters, dataset identifiers, and training artifacts.
* Compare metrics and visualize trends across runs.
* Reproduce successful runs by restoring the recorded inputs and hyperparameters.
* Filter and analyze many runs (for example, show only runs with RMSE \< X).

<Frame>
  <img alt="A dark presentation slide titled &#x22;Solution: SageMaker Experiments&#x22; showing a circular workflow around a SageMaker Experiments icon with three steps labeled Track, Organize, and Compare. To the right are three highlighted points: store metadata and results; experiment with hyperparameters, datasets, algorithms and model architectures; and analyze and optimize ML workflows." />
</Frame>

## SageMaker Experiments: structure and terminology

SageMaker organizes experiment metadata with a small set of hierarchical objects:

| Object          | Purpose                                                                                                                      |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Experiment      | High-level collection grouping related trials (project or objective).                                                        |
| Trial           | A logical attempt or series of steps (often a single model run). The SDK also exposes a Run context for logging.             |
| Trial component | Child artifacts of a trial (e.g., preprocessing, training, evaluation). Many SDK jobs automatically create trial components. |

The experiment tracker manages relationships between these objects and provides hierarchical organization for artifacts, parameters, and metrics.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: SageMaker Experiments&#x22; showing a diagram of components—Experiment, Trial (Run in SDK), Trial Component (created automatically), and Experiment Tracker—with short descriptions. It also notes trial steps like data preprocessing, training, and evaluation and illustrates their relationships." />
</Frame>

## Using the SDK — a code-first workflow

Below is a concise example that demonstrates the typical pattern:

1. Create an Experiment and Trial.
2. Open a Run context.
3. Log parameters and metrics.
4. Execute a training job inside the Run so that SageMaker automatically associates the training job as a trial component.

```python theme={null}
