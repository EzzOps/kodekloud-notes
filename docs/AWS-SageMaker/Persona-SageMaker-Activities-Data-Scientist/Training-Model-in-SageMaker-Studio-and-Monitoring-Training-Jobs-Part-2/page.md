# Example hyperparameter trials (illustrative)
# Trial 1
learning_rate = 0.01
mini_batch_size = 32
epochs = 10

# Trial 2
learning_rate = 0.01
mini_batch_size = 64
epochs = 10

# Trial 3
learning_rate = 0.1
mini_batch_size = 64
epochs = 20
```

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Training Is Time-Consuming and Expensive.&#x22; It shows two icons with captions: &#x22;High Effort — Evaluating input combinations is costly&#x22; and &#x22;Too Many Permutations — Experts narrow down training iterations.&#x22;" />
</Frame>

What AutoML / Autopilot solves

* Automates preprocessing and feature engineering.
* Selects algorithms suited to your tabular problem.
* Trains multiple candidate models and tunes hyperparameters.
* Produces a ranked leaderboard so you can pick the best candidate quickly.
* Exposes model artifacts and notebooks for inspection and further customization.

<Frame>
  <img alt="Slide titled &#x22;Solution: Automation With AutoML&#x22; showing three automation approaches for SageMaker AutoML. The three boxes list: 1) AutoML HyperParameter Tuning Job using SageMaker SDK from a Jupyter Notebook, 2) AutoML AutoPilot using SageMaker SDK from a Jupyter Notebook, and 3) AutoML AutoPilot using SageMaker Canvas." />
</Frame>

Why use the SageMaker SDK with Autopilot

* Programmatic control: integrate Autopilot into CI/CD pipelines and automated workflows.
* Access to artifacts: notebooks, model artifacts, and details about candidate models.
* Customization: you can set guardrails (max candidates, runtime) and then inspect and refine outputs manually.
* Seamless deployment: take the best candidate and create a SageMaker Model/endpoint.

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Solution: Automation With AutoML&#x22; that highlights &#x22;Enhance AutoML with the SDK.&#x22; It lists six benefits — more control, seamless integration, access to model artifacts, customizable preprocessing, retrieval of candidates with metrics, and easy connection to SageMaker/existing code." />
</Frame>

Autopilot pipeline (tabular data)

* Preprocessing and feature engineering
* Algorithm selection
* Training multiple candidate models
* Hyperparameter tuning
* Leaderboard of top candidates

This automation is ideal for rapid prototyping and proving whether your data contains predictive signal before investing in heavy engineering.

<Frame>
  <img alt="An infographic titled &#x22;Solution: AutoML AutoPilot&#x22; that says it automatically builds, trains, and tunes ML models from raw tabular data. It shows five steps with icons: preprocessing/feature engineering, selecting the best algorithm, training multiple models, hyperparameter tuning, and providing a leaderboard of top models." />
</Frame>

Terminology

* AutoML (general): automation techniques applied to machine learning workflows.
* Autopilot (specific): Amazon SageMaker’s AutoML implementation for tabular data.
* In the SageMaker SDK you may see both “AutoML” and “Autopilot” references; the module is typically sagemaker.automl.

<Callout icon="lightbulb">
  Autopilot is excellent for rapid prototyping and automating many training details, but if you require fine-grained control over feature engineering or model internals you should extract the candidate artifacts and continue development manually.
</Callout>

When to use Autopilot vs custom training

| Use case                                                      | Autopilot (Autopilot / AutoML)         | Custom training                    |
| ------------------------------------------------------------- | -------------------------------------- | ---------------------------------- |
| Rapid prototyping / proof of concept                          | Ideal — minimal code, fast results     | Overkill                           |
| Tabular datasets with clear target column                     | Best fit                               | Possible but slower                |
| Need full control over feature engineering or model internals | Not ideal — more limited customization | Preferred                          |
| Want quick candidate models and leaderboard to iterate from   | Yes                                    | Manual selection required          |
| Integration into automated pipelines                          | Yes, via SageMaker SDK                 | Yes, but more manual orchestration |

Quick reference: common Autopilot parameters

| Parameter                        | Purpose                                                                   | Example                 |
| -------------------------------- | ------------------------------------------------------------------------- | ----------------------- |
| target\_attribute\_name          | Label column name in your dataset                                         | "target\_column"        |
| problem\_type                    | Problem type (BinaryClassification, Regression, MulticlassClassification) | "BinaryClassification"  |
| max\_candidates                  | Max number of candidate models to explore                                 | 10                      |
| max\_runtime\_per\_training\_job | Timeout per training job in seconds                                       | 3600                    |
| output\_path                     | S3 path for model artifacts and outputs                                   | s3://your-bucket/output |

Example: run an Autopilot job with the SageMaker SDK

* Best practice: import the AutoML class explicitly from the submodule to make intent clear.

```python theme={null}
import sagemaker
from sagemaker.automl import AutoML

# Initialize the AutoML (Autopilot) job
auto_ml = AutoML(
    role=sagemaker.get_execution_role(),
    target_attribute_name="target_column",             # Label column in your CSV
    output_path="s3://your-bucket/output",             # Where model artifacts will be stored
    problem_type="BinaryClassification",               # e.g., "BinaryClassification", "Regression"
    max_candidates=10,                                 # Max number of candidate models to explore
    max_runtime_per_training_job=3600,                 # Timeout per training job (seconds)
    sagemaker_session=sagemaker.Session()
)

# Start the Autopilot job asynchronously (wait=False)
auto_ml.fit(
    inputs="s3://your-bucket/training-data.csv",
    job_name="my-first-automl-job",
    wait=False
)
```

Inspecting Autopilot progress and candidates

* After starting the job, you can describe the Autopilot job, list candidates, and pick the best candidate programmatically.

```python theme={null}
# Introspection (method names may vary by SDK version)
# Describe the job status
desc = auto_ml.describe_auto_ml_job()
print("Status:", desc.get("AutoMLJobStatus"))

# List candidates (example)
candidates = auto_ml.list_candidates()
print("Candidates:", [c["CandidateName"] for c in candidates])

# Get the best candidate (highest-ranked by objective)
best = auto_ml.best_candidate()
print("Best candidate:", best["CandidateName"])
print("Objective metric:", best.get("FinalAutoMLJobObjectiveMetric"))
```

Deploying the best candidate

* Extract the model artifact and container image from the best candidate and create a SageMaker Model, then deploy to an endpoint.

```python theme={null}
from sagemaker.model import Model

# Model artifact and inference container (from best candidate)
model_artifact = best["ModelArtifacts"]["S3ModelArtifacts"]
image_uri = best["InferenceContainers"][0]["Image"]

# Create a SageMaker Model object
model = Model(
    model_data=model_artifact,
    role="your-sagemaker-execution-role",
    image_uri=image_uri
)

# Deploy the model (creates a real-time endpoint)
predictor = model.deploy(initial_instance_count=1, instance_type="ml.m5.large")
```

Best practices and tips

* Explicit imports: import exact classes/functions you use for clarity and to avoid accidental submodule side effects.
* Use guardrails: set max\_candidates and runtime limits to control cost.
* Inspect artifacts and notebooks produced by Autopilot to learn what preprocessing and features were used.
* Use Autopilot outputs as a starting point — you can register models in the [SageMaker Model Registry](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html) and iterate further.

Small import example (clarity):

```python theme={null}
# Less explicit
import os
os.path.join("a", "b")

# More explicit
from os.path import join
join("a", "b")
```

<Callout icon="warning">
  Autopilot automates many steps but is not a silver bullet. It can reduce time-to-insight for tabular problems, but you should still validate candidate models, check fairness/robustness, and apply custom feature engineering for production-ready models.
</Callout>

What Autopilot gives you

* An end-to-end automated pipeline from raw tabular data to trained and evaluated candidate models.
* A leaderboard of ranked candidates and metrics.
* Programmatic access to model artifacts so you can register, deploy, or refine models further.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; that lists four numbered points about AutoML and AutoPilot in SageMaker. It notes availability in SageMaker AI Canvas and SDK, hyperparameter optimization and training control, settings for problem type and I/O channels, and that models can be created manually or with AutoPilot." />
</Frame>

Summary

* AutoML is the general concept of automating machine learning tasks; Autopilot is SageMaker’s AutoML for tabular data.
* You can use Autopilot through SageMaker Canvas (low-code) or programmatically through the SageMaker SDK.
* Autopilot handles preprocessing, feature engineering, algorithm selection, hyperparameter tuning, and candidate ranking.
* Control inputs like problem type, input data location, output path, and constraints such as max candidates and runtime to manage cost and runtime.
* Use Autopilot for speed and prototyping; refine the best candidate with custom data science work when you need production-grade control.

Links and references

* SageMaker Autopilot (AutoML): [https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-what-is.html](https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-what-is.html)
* SageMaker SDK documentation: [https://sagemaker.readthedocs.io/](https://sagemaker.readthedocs.io/)
* SageMaker Canvas: [https://aws.amazon.com/sagemaker/canvas/](https://aws.amazon.com/sagemaker/canvas/)
* SageMaker Model Registry: [https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html)

You may also want to explore the SageMaker model registry and why model metadata and lineage matter for production workflows.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/36db8fab-85cc-40f0-8594-573631b0425b/lesson/a70660ca-23c4-4f16-b75b-03d49b805ccd" />
</CardGroup>


# Training Model in SageMaker Studio and Monitoring Training Jobs Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-Data-Scientist/Training-Model-in-SageMaker-Studio-and-Monitoring-Training-Jobs-Part-2/page

Explains creating and running SageMaker training jobs with Estimator classes, custom containers, hyperparameters, and automated hyperparameter tuning, plus examples and S3/IAM configuration reminders

How do you create a SageMaker training job? Programmatically — using an estimator object from the SageMaker Python SDK. An estimator encapsulates the training-job configuration: compute resources (for example, ml.c5.24xlarge), input data locations (Amazon S3 paths), and the output location where the model artifact (TGZ) will be saved.

When you call an estimator’s fit(), SageMaker provisions the requested instance(s), pulls the chosen container image with the algorithm, runs training, and tears down the instances when the job completes. Because SageMaker manages the underlying Amazon EC2 instances, you don’t manage them directly and are billed only while the training resources are running.

<Frame>
  <img alt="A slide titled &#x22;Workflow: Estimator Object Class&#x22; that explains an estimator represents a machine learning training job. Three boxes note its responsibilities: sets up computing resources, manages data input and storage, and runs training on AWS SageMaker." />
</Frame>

## Estimator class and convenience subclasses

The Estimator base class represents generic training jobs. SageMaker also provides convenience subclasses for many built-in algorithms and frameworks (for example, LinearLearner, XGBoost wrappers, scikit-learn, PyTorch, TensorFlow). These subclass wrappers automatically pick the correct container image for the algorithm so you don’t need to specify an image URI manually.

Below is a concrete example using the LinearLearner estimator subclass for a regression task. It shows creating the estimator, specifying instance type/count, S3 input/output, hyperparameters, and launching training with .fit().

<Callout icon="lightbulb">
  Replace the example role ARN with your execution role or use get\_execution\_role() in a SageMaker notebook. Ensure the Amazon S3 paths exist and are accessible to the execution role.
</Callout>

```python theme={null}
