# Example: Using SageMaker Experiments with an Estimator (XGBoost)
import sagemaker
from sagemaker.experiments.run import Run
from sagemaker.experiments.experiment import Experiment
from sagemaker.experiments.trial import Trial
from sagemaker.estimator import Estimator

# Initialize SageMaker session and role
sagemaker_session = sagemaker.Session()
role = "arn:aws:iam::123456789012:role/service-role/AmazonSageMaker-ExecutionRole"

# Create or get an Experiment
experiment = Experiment.create(
    experiment_name="house-price-prediction-exp",
    description="Tracking different ML model runs for house price prediction",
    sagemaker_boto_client=sagemaker_session.boto3_client("sagemaker"),
)

# Create a Trial within the Experiment
trial = Trial.create(
    trial_name="trial-001",
    experiment_name=experiment.experiment_name,
    sagemaker_boto_client=sagemaker_session.boto3_client("sagemaker"),
)

# Define hyperparameters
hyperparameters = {
    "eta": 0.1,               # learning rate (XGBoost uses 'eta' for learning rate)
    "max_depth": 5,
    "num_round": 100,         # number of boosting rounds
    "early_stopping_rounds": 10,
}

# Define the Estimator (XGBoost built-in example)
estimator = Estimator(
    image_uri=sagemaker.image_uris.retrieve("xgboost", sagemaker_session.boto_region_name, version="1.3-1"),
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path="s3://my-bucket/house-price-model/",
    hyperparameters=hyperparameters,
    sagemaker_session=sagemaker_session,
)

# Associate Estimator Training Job with the Trial and log hyperparameters/metrics.
# Execute estimator.fit() inside the Run context so the training job is associated automatically.
with Run(
    experiment_name=experiment.experiment_name,
    trial_name=trial.trial_name,
    sagemaker_session=sagemaker_session,
) as run:
    # Log hyperparameters explicitly (optional — some are auto-captured)
    for name, value in hyperparameters.items():
        run.log_parameter(name, value)

    # Start the training job (the job will be recorded as a trial component)
    estimator.fit("s3://my-bucket/house-price-data/")
```

Practical notes on the example:

* Always call estimator.fit(...) inside the Run context. That ensures the training job becomes a trial component and training metadata are captured automatically.
* The SDK often captures container image, algorithm name, and training-job identifiers for you; explicitly logging hyperparameters and custom metrics improves clarity and searchability.
* Use algorithm-appropriate hyperparameter names (e.g., XGBoost uses "eta" and "num\_round").

## Where do results appear?

SageMaker stores experiment metadata and metrics in the backend. Visualization availability depends on your Studio experience:

* SageMaker Studio Classic: exposes the original SageMaker Experiments visual dashboard with charts and comparison views.
* Newer Studio experiences: may surface MLflow or other experiment UIs; consider integrating MLflow or a third-party tool if you rely on a consistent UI.

> **lightbulb** If you depend on Studio UI visualizations, verify which experiment-tracking UI your Studio instance exposes. Many teams adopt MLflow or tools like Weights & Biases for a stable, long‑term visualization and collaboration experience.

Using the Studio Classic UI (or equivalent tracking UIs) you can:

* Visualize metrics across trials (line charts, bar charts).
* Compare multiple runs with side-by-side metric views and confusion matrices.
* Filter runs by metric thresholds or parameter values to find promising experiments quickly.

<Frame>
  <img alt="A presentation slide titled &#x22;Results: Experiment Tracking and Future Outlook&#x22; showing two dark-themed experiment-tracking dashboards with charts, tables, and a confusion matrix. Below are three highlighted benefits: &#x22;Experiment management streamlines ML workflows,&#x22; &#x22;Speeds up model development,&#x22; and &#x22;Enhances decision-making.&#x22;" />
</Frame>

## Summary and recommended next steps

* Experiment tracking is essential to organize model development and to make results reproducible.
* SageMaker Experiments (via the SDK) provides a hierarchical model: Experiment → Trial (use Run contexts) → Trial Component.
* Execute training and evaluation jobs inside Run contexts to automatically capture hyperparameters, metrics, and artifacts.
* Because Studio experiences are evolving, evaluate whether to use the native SageMaker Experiments UI, MLflow, or a third-party tool depending on your long-term needs for UI continuity and collaboration.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; showing five numbered takeaways about experimentation tracking, SageMaker Experiments vs. MLflow, required SDK classes, the SageMaker Classic UI limitation, and strong metric visualizations." />
</Frame>

Further reading and references:

* SageMaker Experiments docs: [https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-experiments.html](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-experiments.html)
* MLflow: [https://mlflow.org/](https://mlflow.org/)
* Weights & Biases: [https://wandb.ai/](https://wandb.ai/)
* Neptune: [https://neptune.ai/](https://neptune.ai/)
* TensorBoard: [https://www.tensorflow.org/tensorboard](https://www.tensorflow.org/tensorboard)

This concludes the lesson on experiment management with SageMaker Experiments.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/36db8fab-85cc-40f0-8594-573631b0425b/lesson/357b8bee-03ad-422e-8aa5-7fc20a4d6645)


# Keeping Track of Models Using the SageMaker Model Registry Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-Data-Scientist/Keeping-Track-of-Models-Using-the-SageMaker-Model-Registry-Part-2/page

Describes how data scientists and governance officers use the SageMaker Model Registry to register, review, approve, version, and deploy models with governance and CI/CD examples

This lesson explains how different personas interact with the SageMaker Model Registry, shows example code for programmatic model registration, and outlines governance and integration options to turn ad-hoc artifacts into versioned, deployable models.

Who uses the model registry?

* Data scientist (code-first): Trains models, registers versions programmatically via SDKs/CLI, and links artifacts and container images for inference.
* Governance officer (UI-first): Reviews explainability, bias reports, metadata, and audit trails in SageMaker Studio, then approves or rejects models for production.

Persona comparison

| Persona            | Primary interface             | Main actions                                                                                        |
| ------------------ | ----------------------------- | --------------------------------------------------------------------------------------------------- |
| Data scientist     | SDKs / Boto3 / Notebooks / CI | Train models, create model package groups, register model packages, attach metrics and artifacts    |
| Governance officer | SageMaker Studio UI           | Inspect explainability & bias reports, review metadata & lineage, set approval state for production |

Code-based persona (data scientist)

* Typical tools: [SageMaker Python SDK](https://sagemaker.readthedocs.io/), [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html), CI/CD pipelines.
* Common workflow: create a Model Package Group, register model packages (versions), attach metadata/metrics, and set an initial approval state.

Create a Model Package Group (Boto3 example)
This logical grouping helps organize related model versions for a project or product.

```python theme={null}
