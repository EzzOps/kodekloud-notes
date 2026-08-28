# imports and session setup
import boto3
import sagemaker
from sagemaker import get_execution_role
from sagemaker.session import Session
from sagemaker import Model, ModelPackage

sagemaker_session = Session()
role = get_execution_role()

print(role)
```

The printed value is the IAM execution role ARN associated with your notebook environment.

## 2. Legacy model package (Model.create)

If you already have a trained model artifact saved in S3 and want a quick way to create a SageMaker model package (legacy flow), call `Model.create()` by supplying the S3 model artifact and the appropriate container image for the framework.

* model artifact (output of a training job)
* container image URI for the training framework (for example, Linear Learner)

Example:

```python theme={null}
# Reference model artifact in S3 (this is the trained model output)
model_artifact = 's3://sagemaker-eu-central-1-485186561655/house-price-linearlearner-demo/output/linear-learner-2025-05-06-13-48-11-566/output/model.tar.gz'

# Determine region and fetch container image URI for the Linear Learner framework
region = sagemaker_session.boto_region_name
container_image_uri = sagemaker.image_uris.retrieve(framework="linear-learner", region=region)

print(f"SageMaker Linear Learner Image URI: {container_image_uri}")

# Assign a meaningful name to the model
model_name = 'kodekloud-house-prices-demo'

# Create the SageMaker model (legacy model package)
model = Model(
    image_uri=container_image_uri,
    model_data=model_artifact,
    role=role,
    name=model_name
)

# Register the model package (legacy)
model.create()
```

After calling `model.create()`, the model package shows up in the SageMaker console under Inference → Models, and you can create an endpoint directly from that model object for quick testing.

<Frame>
  <img alt="A screenshot of the Amazon S3 web console showing the contents of an &#x22;output/&#x22; folder. It lists a single object named &#x22;model.tar.gz&#x22; (1.2 KB) with actions like Copy S3 URI, Download, Open, and Delete." />
</Frame>

<Frame>
  <img alt="A screenshot of the Amazon SageMaker console showing a model page titled &#x22;kodekloud-house-prices-demo&#x22; with model settings, container details, S3 model data location, and network information. The page also shows action buttons (Create endpoint, Create batch transform job) and a large mouse cursor." />
</Frame>

<Callout icon="lightbulb">
  Model.create is great for rapid prototyping and one-off endpoints. For production tracking, reproducibility, and approval workflows, prefer the SageMaker Model Registry with Model.register.
</Callout>

## 3. Model Registry: create a Model Package Group and register a model version

The Model Registry stores model versions inside a Model Package Group and provides metadata, metrics, versioning, lineage, and approval workflows. Use the Boto3 SageMaker client to create a model package group, then call `Model.register()` to add a model version.

Create the package group:

```python theme={null}
# Create a model package group using the low-level boto3 client
model_package_group_name = 'house-price-model-registry-demonstration'
model_package_group_description = 'KodeKloud model package group for house price prediction'

sagemaker_client = boto3.client('sagemaker')

try:
    sagemaker_client.create_model_package_group(
        ModelPackageGroupName=model_package_group_name,
        ModelPackageGroupDescription=model_package_group_description
    )
    print(f'Created Model Package Group: {model_package_group_name}')
except sagemaker_client.exceptions.ResourceInUse:
    print(f'Model Package Group {model_package_group_name} already exists.')
```

Register the model artifact into the registry as a model package version. Set an initial approval status (for example, `PendingManualApproval`) and attach any custom metadata you want to track.

```python theme={null}
# Register the model into the model registry
model_approval_status = "PendingManualApproval"
customer_metadata_properties = {"ModelType": "HousePricePrediction"}

model_package = model.register(
    content_types=["text/csv"],
    response_types=["text/csv"],
    inference_instances=["ml.t2.medium", "ml.m5.large"],
    transform_instances=["ml.m5.large"],
    model_package_group_name=model_package_group_name,
    approval_status=model_approval_status,
    customer_metadata_properties=customer_metadata_properties,
)

print(f"Model package version ARN: {model_package.model_package_arn}")
```

After registration, the version appears in SageMaker Studio → Model Registry under the specified Model Package Group with the approval status you supplied.

<Frame>
  <img alt="A screenshot of the Amazon SageMaker Model Registry &#x22;Version 1&#x22; overview showing a model training status and tabs for Overview/Activity/Lineage. The main panel displays a metrics table with entries like validation:mae, validation:mse, validation:r2 and their numeric values." />
</Frame>

In the Model Registry UI you can inspect:

* Metrics collected during training (MAE, MSE, R2, etc.),
* Artifacts (training and validation datasets, model artifact S3 paths),
* Hyperparameters used during training,
* The container image associated with the model,
* Activity feed (registration, approval, deployment events),
* Lineage that links datasets, training jobs, and containers to the model.

<Frame>
  <img alt="A screenshot of an AWS SageMaker Studio model version overview displaying hyperparameters (epochs = 10, mini_batch_size = 32, predictor_type = regressor) with Training marked &#x22;Complete&#x22; and Deploy &#x22;Pending Approval.&#x22; The left sidebar shows navigation items (Performance, Artifacts, Hyperparameters) and a large mouse cursor is visible." />
</Frame>

## 4. Approve a model version (in the UI) and deploy the latest approved version

Once a model version is approved in the Model Registry UI (for example, change status from `PendingManualApproval` → `Approved`), you can programmatically find the latest approved version and deploy it.

<Callout icon="warning">
  Approving a model should follow your organization's validation and governance processes. Only approve models that meet performance, fairness, and security requirements.
</Callout>

List the latest approved model packages in the package group (sorted by creation time) and select the most recent:

```python theme={null}
# List the latest approved model packages in the package group (descending by creation time)
response = sagemaker_client.list_model_packages(
    ModelPackageGroupName=model_package_group_name,
    ModelApprovalStatus='Approved',
    SortBy='CreationTime',
    SortOrder='Descending'
)

if not response.get('ModelPackageSummaryList'):
    raise RuntimeError('No approved model packages found.')

latest_approved_model_package_arn = response['ModelPackageSummaryList'][0]['ModelPackageArn']
print(f'Latest Approved Model Package ARN: {latest_approved_model_package_arn}')
```

Create a ModelPackage object from the approved ARN and deploy it to a real-time endpoint:

```python theme={null}
# Create a ModelPackage object and deploy it
model_package = ModelPackage(
    role=role,
    model_package_arn=latest_approved_model_package_arn,
    sagemaker_session=sagemaker_session
)

predictor = model_package.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name="latest-house-price-model"
)
```

Deployment can take several minutes. Once deployed, the endpoint will appear under Endpoints in SageMaker Studio/Console.

<Frame>
  <img alt="Screenshot of the Amazon SageMaker Studio model version overview for a &#x22;House Price&#x22; model, showing container locations and available instance types. A &#x22;Deploy — Approved&#x22; panel is highlighted with a large cursor over the Deploy button." />
</Frame>

Deploying a model created from a Model Registry package will also create a model entry under the legacy Models console (Inference → Models), since the deployed artifact is a managed model package.

<Frame>
  <img alt="A screenshot of the Amazon SageMaker &#x22;Models&#x22; console in a web browser showing two model entries (house-price-model-registry-demonstratio... and kodekloud-house-prices-demo) with the left navigation menu visible. A large black mouse cursor is shown near the center of the screen." />
</Frame>

After deployment you can confirm the endpoint status:

<Frame>
  <img alt="A screenshot of the Amazon SageMaker Studio &#x22;Endpoints&#x22; page showing one deployed endpoint named &#x22;latest-house-price-model&#x22; with status &#x22;In service.&#x22; The dark-themed UI includes a left navigation sidebar and a large mouse cursor hovering over the endpoint list." />
</Frame>

## Quick comparison: Model.create vs Model.register

| Resource                            | Use Case                                           | Benefits                                                                    |
| ----------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------------- |
| Model.create (legacy model package) | Rapid prototyping, one-off endpoints               | Fast, minimal workflow to create a model package and deploy                 |
| Model.register + Model Registry     | Production model lifecycle, versioning, governance | Versioning, approval workflows, metrics, lineage, metadata, reproducibility |

## Summary

* Model.create is a quick, legacy method to create model packages for prototyping and rapid testing.
* Model.register combined with the SageMaker Model Registry is the recommended approach for production: it provides robust versioning, approval workflows, stored metrics, activity logs, and lineage for reproducibility.
* After a model version is approved in the registry, you can programmatically fetch the latest approved package and deploy it as a real-time endpoint.

We will also explore different hosting options—real-time endpoints and batch transforms—and when to choose each approach.

## Links and references

* SageMaker Model Registry: [https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html)
* SageMaker Python SDK: [https://sagemaker.readthedocs.io/](https://sagemaker.readthedocs.io/)
* Boto3 SageMaker client: [https://boto3.amazonaws.com/v1/documentation[AWS_SECRET_ACCESS_KEY].html](https://boto3.amazonaws.com/v1/documentation[AWS_SECRET_ACCESS_KEY].html)
* SageMaker Hosting (endpoints and batch transforms): [https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html](https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/36db8fab-85cc-40f0-8594-573631b0425b/lesson/a5157b31-a690-4f07-a0ee-c1a8cfd8f212" />
</CardGroup>


# Demo Training Your Model in SageMaker Studio Using Python SDK

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-Data-Scientist/Demo-Training-Your-Model-in-SageMaker-Studio-Using-Python-SDK/page

Shows how to train and tune a Linear Learner model in Amazon SageMaker Studio using the SageMaker Python SDK Estimator with CSV data uploads and S3 model artifacts

In this lesson we'll train a model in Amazon SageMaker Studio using the SageMaker Python SDK. This guide walks through a compact, runnable notebook flow that demonstrates:

* Defining and running a training job with the SageMaker SDK's Estimator class.
* Launching a Hyperparameter Tuning job to explore multiple hyperparameter combinations in parallel.
* Inspecting and retrieving model artifacts produced by training.

What you'll do (high-level):

1. Open a Jupyter notebook in SageMaker Studio.
2. Prepare data: split into train/validation/test (≈ 70% / 20% / 10%).
3. Create and run a SageMaker training job using Estimator — provide the container image, compute resources, and IAM role.

<Frame>
  <img alt="A presentation slide titled &#x22;Demo Steps&#x22; listing three numbered steps: 01 Open Notebook, 02 Data Preparation (split dataset 70% train / 20% validation / 10% test), and 03 Create Training Job (use Estimator, specify container image, compute size, and IAM role). The slide has a dark teal background with horizontal highlighted bars and a small &#x22;© Copyright KodeKloud&#x22; note." />
</Frame>

Overview and approach

* We'll use the generic Estimator from the SageMaker SDK, so we must provide the container image URI for the training algorithm. For this demo we use SageMaker's built-in Linear Learner (regression).
* Workflow: set hyperparameters (mini-batch size, epochs, etc.), upload CSV data to Amazon S3, call estimator.fit(...), then inspect the model artifact (model.tar.gz) in S3.
* To accelerate experimentation, we create a Hyperparameter Tuning job to run multiple training jobs in parallel and pick the best model by an objective metric (e.g., validation RMSE).

Open SageMaker Studio, select a notebook server from the JupyterLab launcher, and open the notebook that will contain the demo code.

<Frame>
  <img alt="Screenshot of a JupyterLab interface running in AWS SageMaker, showing the Launcher with notebook and console kernels (Python, Glue, Spark) and various file-type tiles. The left sidebar shows a file browser with a highlighted notebook file (training_demo2.ipynb)." />
</Frame>

Compact, runnable notebook flow

* The sequence below contains the main notebook steps: imports, session/role setup, load & split data, save CSVs, upload to S3, define estimator, and run training.
* This example assumes a preprocessed CSV file (preprocessed.csv) is available in the notebook filesystem.

```python theme={null}
