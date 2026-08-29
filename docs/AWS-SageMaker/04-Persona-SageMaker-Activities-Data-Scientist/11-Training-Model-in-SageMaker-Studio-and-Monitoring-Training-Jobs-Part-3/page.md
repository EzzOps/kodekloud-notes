# linear_learner_estimator.py
import sagemaker
from sagemaker.inputs import TrainingInput
from sagemaker.amazon.linear_learner import LinearLearner

# SageMaker session and role
session = sagemaker.Session()
role = 'arn:aws:iam::123456789012:role/SageMakerRole'  # replace with your role or use get_execution_role()

# Define S3 paths
s3_input_path = 's3://your-bucket/house-price-data/input/'
s3_output_path = 's3://your-bucket/house-price-data/output/'

# Create a Linear Learner estimator (using hyperparameters dictionary)
linear_estimator = LinearLearner(
    role=role,
    instance_count=1,
    instance_type='ml.m5.large',
    predictor_type='regressor',  # 'regressor' for linear regression
    output_path=s3_output_path,
    sagemaker_session=session,
    hyperparameters={
        'epochs': 20,
        'optimizer': 'adam',
        'learning_rate': 0.01,
        'wd': 0.001,               # weight decay (L2)
        'normalize_data': True,
        'loss': 'absolute_loss'
    }
)

# Prepare data input
train_input = TrainingInput(s3_input_path, content_type='text/csv')

# Launch the training job
linear_estimator.fit({'train': train_input})

print(f"Model artifacts saved to: {s3_output_path}")
```

This simple example will:

* Provision the instance(s),
* Pull the LinearLearner container,
* Read training data from S3,
* Run training using the specified hyperparameters,
* Write the model artifact (TGZ) to the specified output path.

Using the SDK keeps your code compact and focused on the ML task rather than infrastructure plumbing.

## Custom containers and the base Estimator

If you need a custom container image or an algorithm wrapper not available as a convenience class, use the Estimator base class and supply an image URI. The example below shows how to retrieve a SageMaker-provided XGBoost image URI and construct a base Estimator.

```python theme={null}
# custom_estimator_xgboost.py
import sagemaker
from sagemaker import Estimator

session = sagemaker.Session()
role = 'arn:aws:iam::123456789012:role/SageMakerRole'  # replace as needed

# Retrieve the SageMaker XGBoost image for the current region and a specified version
xgboost_image_uri = sagemaker.image_uris.retrieve('xgboost', session.boto_region_name, version='1.0-1')

estimator = Estimator(
    image_uri=xgboost_image_uri,
    role=role,
    instance_count=1,
    instance_type='ml.m5.large',
    output_path='s3://your-bucket/output/',
    sagemaker_session=session
)

# Launch the training job with a custom container image (S3 path or TrainingInput accepted)
estimator.fit({'train': 's3://your-bucket/input/train.csv'})

print("Training completed. Model artifacts saved to S3.")
```

## Hyperparameters — controlling training behavior

Hyperparameters are preset configuration values that control training behavior. They are passed to the training container and affect optimization, regularization, preprocessing, and loss computation. Many convenience estimator classes accept a hyperparameters dictionary; otherwise set them in your training script or container.

Common hyperparameters and considerations:

|                     Hyperparameter | Purpose                                         | Typical considerations                                                                           |
| ---------------------------------: | ----------------------------------------------- | ------------------------------------------------------------------------------------------------ |
|                             epochs | Number of full passes over the training dataset | Higher values can improve fit but may overfit; common ranges vary by dataset size (e.g., 10–100) |
|                     learning\_rate | Step size for weight updates                    | Too large can overshoot; too small slows convergence                                             |
|                          optimizer | Optimization algorithm (e.g., 'adam', 'sgd')    | Different optimizers converge differently; choose based on task and dataset                      |
|           batch\_size (mini-batch) | Number of samples per parameter update          | Affects memory footprint and convergence stability                                               |
|                  wd (weight decay) | L2 regularization strength                      | Penalizes large weights to reduce overfitting                                                    |
| normalize\_data / normalize\_label | Preprocessing flags                             | Use only if your dataset hasn't been pre-normalized externally                                   |

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: HyperParameters&#x22; that defines hyperparameters as preset configurations for a machine learning algorithm before training. It lists three points: algorithm-specific settings for model training; can be set explicitly for LinearLearner; and SageMaker uses defaults if not specified." />
</Frame>

## Regularization and preprocessing hyperparameters

Regularization helps prevent overfitting and improves generalization:

* L1 regularization (sparsity): pushes some weights toward zero, which can effectively remove irrelevant features.
* L2 regularization (weight decay): penalizes large weights to produce smoother models.

Preprocessing flags (for example, normalize\_data or normalize\_label) instruct the container to perform scaling/normalization before training. Use these only if your data pipeline hasn't already standardized the features/labels.

## Loss function

The loss function describes what the training process minimizes. For regression, common choices include:

* absolute loss (L1): sum of absolute residuals — more robust to outliers
* squared loss (L2): sum of squared residuals — penalizes large errors more heavily

Selecting a loss function affects sensitivity to outliers and convergence dynamics.

## Automated hyperparameter tuning (SageMaker Hyperparameter Tuning)

Manually searching hyperparameters is time-consuming. SageMaker Hyperparameter Tuning automates this by launching multiple training jobs (trials) across a defined hyperparameter search space and selecting the best trial based on an objective metric (for example, validation RMSE or validation accuracy).

You must define:

* objective\_metric\_name: the metric to optimize and whether to minimize or maximize,
* hyperparameter\_ranges: continuous or discrete ranges for each hyperparameter,
* max\_jobs: total number of trials,
* max\_parallel\_jobs: number of concurrent trials,
* metric\_definitions: regex patterns to extract the objective metric from training logs (ensure the regex matches the container’s log format).

Example: building a HyperparameterTuner around an XGBoost estimator.

```python theme={null}
# hyperparameter_tuning_xgboost.py
import sagemaker
from sagemaker import Estimator
from sagemaker.tuner import HyperparameterTuner, ContinuousParameter, IntegerParameter

session = sagemaker.Session()
role = 'arn:aws:iam::123456789012:role/SageMakerRole'  # replace as needed

# Create the XGBoost estimator (using SageMaker-provided XGBoost container)
xgboost_image_uri = sagemaker.image_uris.retrieve('xgboost', session.boto_region_name, version='1.0-1')
xgboost_estimator = Estimator(
    image_uri=xgboost_image_uri,
    role=role,
    instance_count=1,
    instance_type='ml.m5.large',
    output_path='s3://your-bucket/output/',
    sagemaker_session=session
)

# Define hyperparameter search space
hyperparameter_ranges = {
    'learning_rate': ContinuousParameter(0.01, 0.2),
    'max_depth': IntegerParameter(3, 12)  # max_depth is an integer parameter
}

# Define tuner
tuner = HyperparameterTuner(
    estimator=xgboost_estimator,
    objective_metric_name='validation:accuracy',  # metric to optimize
    hyperparameter_ranges=hyperparameter_ranges,
    max_jobs=10,
    max_parallel_jobs=2,
    # Ensure the regex matches how the training container logs the metric
    metric_definitions=[{
        'Name': 'validation:accuracy',
        'Regex': 'validation-accuracy:([0-9\\.]+)'
    }]
)

# Launch tuning job (passes training and validation data channels)
tuner.fit({
    'train': 's3://your-bucket/train-data/',
    'validation': 's3://your-bucket/validation-data/'
})
```

The tuner will run up to max\_jobs training trials and return the best hyperparameter set according to the specified objective metric. Ensure the metric extraction regex matches the container’s log output so SageMaker can parse the metric successfully.

## Quick summary

* Use estimator subclasses for built-in algorithms (LinearLearner, XGBoost wrappers, etc.) — the SDK chooses the correct container image.
* Use the base Estimator to supply a custom container image.
* Configure hyperparameters to control optimization, regularization, preprocessing, and loss.
* Use SageMaker Hyperparameter Tuning to automatically search for the best hyperparameters; define search space, objective metric, and job counts.
* Always ensure S3 data paths and IAM execution roles are correctly configured and permissioned.

## Links and references

* [AWS SageMaker Documentation](https://learn.kodekloud.com/user/courses/aws-sagemaker)
* [Amazon S3 Documentation](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [Amazon EC2 Documentation](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)
* [PyTorch on SageMaker](https://learn.kodekloud.com/user/courses/pytorch)
* SageMaker SDK: image\_uris.retrieve — see official SageMaker Python SDK docs for region-specific image URIs and supported frameworks.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/36db8fab-85cc-40f0-8594-573631b0425b/lesson/9dd805c2-653c-4793-a8ea-7b23f7dfefbe" />
</CardGroup>


# Training Model in SageMaker Studio and Monitoring Training Jobs Part 3

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-Data-Scientist/Training-Model-in-SageMaker-Studio-and-Monitoring-Training-Jobs-Part-3/page

Overview of Amazon SageMaker managed training jobs, Estimator usage, hyperparameter tuning, and compute sizing.

Managed training jobs in Amazon SageMaker help teams deliver models faster by offloading infrastructure and automating repetitive tasks. With SageMaker you can run optimized training at scale, explore hyperparameter combinations automatically, and pay only for the compute you consume—reducing idle EC2 capacity and cutting operational overhead. These advantages let data scientists focus on modeling, experimentation, and iteration instead of provisioning and managing infrastructure.

<Callout icon="lightbulb">
  Optimized training with managed jobs accelerates development and reduces cost by automating hyperparameter search and letting you right-size compute (instance type and instance count) per job.
</Callout>

Scalability is straightforward. Adjust an Estimator's instance\_type to scale up (more powerful CPU/GPU) or instance\_count to scale out (distributed training). For distributed jobs, SageMaker orchestrates containers across instances so your training script can process larger datasets with minimal changes.

<Frame>
  <img alt="A presentation slide titled &#x22;Results: Optimized Model Training With SageMaker&#x22; showing five benefit panels—Faster Time to Insights, Better Model Accuracy, Lower Costs, Higher Productivity, and Scalable Solutions—each with an icon and short explanation. It highlights outcomes like reduced development time, efficient tuning, cost savings, higher productivity, and handling larger/more complex data." />
</Frame>

What we covered in this lesson/article

* SageMaker training jobs run your training script inside managed containers. Point the job at your training data (commonly in S3), provide the algorithm or framework, and supply an entry point script. SageMaker pulls the correct container image for the specified framework or algorithm.
* The SageMaker Python SDK exposes an Estimator base class and framework-specific subclasses (e.g., TensorFlow, PyTorch). Instantiating an Estimator configures the container image, compute, and runtime behavior for your training job.
* Hyperparameter tuning can be automated with SageMaker HyperParameter Tuning Jobs. You provide ranges, maximum total/concurrent jobs, and a search strategy (e.g., grid or random). SageMaker runs parallel training jobs, evaluates the objective metric, and returns the best hyperparameter configuration.
* Compute sizing is an Estimator property. Use instance\_type and instance\_count to meet the scale of your workload (single-instance, multi-GPU, or distributed across instances).

Estimator parameters quick reference

| Parameter       | Purpose                                                        | Example                                                                 |
| --------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------- |
| image\_uri      | ECR container image used to run your training code             | `123456789012.dkr.ecr.us-west-2.amazonaws.com/my-training-image:latest` |
| role            | IAM role used by SageMaker to access S3, ECR, CloudWatch, etc. | `arn:aws:iam::123456789012:role/SageMakerRole`                          |
| instance\_type  | Compute instance type for training (CPU/GPU)                   | `ml.m5.xlarge`, `ml.p3.2xlarge`                                         |
| instance\_count | Number of instances for distributed training                   | `1`, `2`, `4`                                                           |
| entry\_point    | Training script that runs inside the container                 | `train.py`                                                              |
| source\_dir     | Directory packaged and uploaded with the training job          | `src/`                                                                  |
| hyperparameters | Dictionary of hyperparameters passed to your script            | `{'epochs': 10, 'learning_rate': 0.01}`                                 |

Example: configuring an Estimator (Python SDK)

```python theme={null}
from sagemaker.estimator import Estimator

estimator = Estimator(
    image_uri='123456789012.dkr.ecr.us-west-2.amazonaws.com/my-training-image:latest',
    role='arn:aws:iam::123456789012:role/SageMakerRole',
    instance_type='ml.m5.xlarge',
    instance_count=2,
    entry_point='train.py',
    source_dir='src',
    hyperparameters={'epochs': 10, 'learning_rate': 0.01}
)
