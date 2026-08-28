# python
# Step 0: Imports and session setup
import time
import json
import boto3
import sagemaker
from sagemaker import get_execution_role, Model
from sagemaker.session import Session

sagemaker_session = Session()
role = get_execution_role()

# Define S3 bucket and prefix (use no leading slash to avoid double-slashes)
s3_bucket = sagemaker_session.default_bucket()
s3_prefix = "model"

print("Using role:", role)
print("Using bucket:", s3_bucket, "prefix:", s3_prefix)
```

Upload the local model artifact to S3 and look up the appropriate container image for the framework (Linear Learner in this example). We use `sagemaker.image_uris.retrieve` to get the correct ECR image URI for the current region.

```python theme={null}
# python
# Step 1: Upload model artifact and get container image URI
local_file_path = "model.tar.gz"  # local file produced by training/export
s3_uri = sagemaker_session.upload_data(local_file_path, bucket=s3_bucket, key_prefix=s3_prefix)
print(f"File uploaded to: {s3_uri}")

model_artifact = f"s3://{s3_bucket}/{s3_prefix}/model.tar.gz"
region = sagemaker_session.boto_region_name

# Retrieve the Linear Learner image URI for the region
container_image_uri = sagemaker.image_uris.retrieve(framework="linear-learner", region=region)

print(f"SageMaker Linear Learner Image URI: {container_image_uri}")

# Name for the model package
model_name = "house-prices-inference-demo"
```

Create and register the SageMaker model (model package) using the SageMaker SDK `Model` class. Calling `model.create()` registers this model in SageMaker (visible under Inference -> Models).

```python theme={null}
# python
# Step 2: Create SageMaker Model (model package)
model = Model(
    image_uri=container_image_uri,
    model_data=model_artifact,
    role=role,
    name=model_name
)

# Register the model in SageMaker (create_model)
model.create()
print(f"Model registered with name: {model_name}")
```

You can verify the registered model in the SageMaker console. The next image shows the model details page where the container image and S3 model data location are associated with the model.

<Frame>
  <img alt="A screenshot of the Amazon SageMaker console showing the &#x22;house-prices-inference-demo&#x22; model details, including ARN, container image and model data location. The left navigation pane and top toolbar with SageMaker services (JumpStart, Inference, Training, etc.) are also visible." />
</Frame>

Create an endpoint configuration using Boto3. Endpoint configurations describe one or more production variants (models + instance types + instance counts + weights). Here we create a single variant that receives all traffic.

```python theme={null}
# python
# Step 3: Create Endpoint Configuration using Boto3
sagemaker_client = boto3.client("sagemaker")

endpoint_config_name = "my-endpoint-config-using-boto3"

create_endpoint_config_response = sagemaker_client.create_endpoint_config(
    EndpointConfigName=endpoint_config_name,
    ProductionVariants=[
        {
            "InstanceType": "ml.t2.medium",
            "InitialVariantWeight": 1.0,
            "InitialInstanceCount": 1,
            "ModelName": model_name,
            "VariantName": "AllTraffic"
        }
    ]
)

print("Endpoint configuration created:", create_endpoint_config_response["EndpointConfigArn"])
```

Create the endpoint using the endpoint configuration. Endpoint creation is asynchronous — provisioning and starting the model container typically takes several minutes.

```python theme={null}
# python
# Step 4: Create the endpoint
endpoint_name = "my-endpoint-using-boto3"

create_endpoint_response = sagemaker_client.create_endpoint(
    EndpointName=endpoint_name,
    EndpointConfigName=endpoint_config_name
)

print(f"Creating endpoint: {endpoint_name}")
print("Create endpoint response ARN:", create_endpoint_response.get("EndpointArn"))
```

You can inspect endpoint creation progress in the SageMaker console (Endpoints) or poll programmatically. The following screenshot shows an endpoint in the Creating state.

<Frame>
  <img alt="Screenshot of the Amazon SageMaker console showing &#x22;Endpoint configuration settings&#x22; for &#x22;my-endpoint-config-using-boto3.&#x22; The page lists data capture options and a Production variant with the model &#x22;house-prices-inference-demo.&#x22;" />
</Frame>

Below is a helper to poll the endpoint until it's InService. Waiting prevents invocation errors while the endpoint is still provisioning.

```python theme={null}
# python
# Step 5: Wait until the endpoint is InService (simple polling)
def wait_for_endpoint_in_service(sagemaker_client, endpoint_name, timeout_minutes=15):
    timeout = time.time() + timeout_minutes * 60
    while time.time() < timeout:
        resp = sagemaker_client.describe_endpoint(EndpointName=endpoint_name)
        status = resp["EndpointStatus"]
        print(f"Endpoint status: {status}")
        if status == "InService":
            print("Endpoint is InService.")
            return True
        if status in ("Failed", "OutOfService"):
            raise RuntimeError(f"Endpoint entered terminal state: {status}")
        time.sleep(30)
    raise TimeoutError(f"Timed out waiting for endpoint {endpoint_name} to become InService")

# Call the waiter (this may take several minutes)
wait_for_endpoint_in_service(sagemaker_client, endpoint_name)
```

You can also view the endpoint from SageMaker Studio’s Endpoints list as it transitions to InService.

<Frame>
  <img alt="Screenshot of the AWS SageMaker Studio &#x22;Endpoints&#x22; console in dark mode, showing one endpoint named &#x22;my-endpoint-using-boto3&#x22; with status &#x22;Creating.&#x22; The left navigation pane displays SageMaker apps and deployment options, and there are Create endpoint and Delete buttons at the top right." />
</Frame>

When the endpoint is InService, invoke it using the SageMaker runtime (boto3 client `sagemaker-runtime`). Note: Boto3's SageMaker client handles creation/describing of endpoints and endpoint configurations; `sagemaker-runtime` is used for invoking inferences.

```python theme={null}
# python
# Step 6: Invoke the endpoint (once InService)
sagemaker_runtime_client = boto3.client("sagemaker-runtime")

# Example CSV input (features should match the model's expected format)
input_data = "51.6215527,-0.2466031,2.0,6.0,517.0,3.0,289000.0,27.393364928909996,1055000.0,37.01298701298701,285000.0,1354000.0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"

response = sagemaker_runtime_client.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType="text/csv",
    Body=input_data
)

# Decode and print response body
prediction = response["Body"].read().decode("utf-8")
print(f"Predicted house price: {prediction}")
```

Notes and recommendations

<Callout icon="lightbulb">
  If you want granular control over the endpoint configuration and lifecycle, use Boto3 (as shown). The SageMaker Python SDK provides higher-level abstractions for model + endpoint creation and also the Predictor class for inference, which can make development faster and code more concise. Choose the approach that best fits your automation, control, and CI/CD needs.
</Callout>

<Callout icon="warning">
  Creating endpoints incurs AWS costs while instances are running. Use minimal instance sizes for testing, delete endpoints when not in use, and ensure IAM roles used by Studio have just the permissions needed for deployment.
</Callout>

Quick reference table

|                             Resource / API | Purpose                                                           | Example                                        |
| -----------------------------------------: | ----------------------------------------------------------------- | ---------------------------------------------- |
|               SageMaker Model (SDK: Model) | Register model artifact + container image                         | `model.create()`                               |
| Boto3 sagemaker (create\_endpoint\_config) | Create endpoint configuration (variants, instance types)          | `sagemaker_client.create_endpoint_config(...)` |
|         Boto3 sagemaker (create\_endpoint) | Create endpoint (asynchronous)                                    | `sagemaker_client.create_endpoint(...)`        |
|       Boto3 sagemaker (describe\_endpoint) | Check endpoint status                                             | `sagemaker_client.describe_endpoint(...)`      |
|                    Boto3 sagemaker-runtime | Invoke endpoint for inference                                     | `sagemaker-runtime.invoke_endpoint(...)`       |
|           SageMaker Python SDK (Predictor) | High-level inference client (simplifies invocation/serialization) | `predictor.predict(...)`                       |

Summary

* Uploaded a local model artifact to S3, retrieved the appropriate container image URI, and registered a SageMaker model package.
* Created an endpoint configuration and endpoint using Boto3, polled until the endpoint became InService, and invoked the endpoint using the SageMaker runtime with CSV input.
* The SageMaker Python SDK provides higher-level operations and a Predictor class for simplified inference flows; comparing both patterns helps determine which integrates best with your automation strategy.

Further reading and references

* [Amazon SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* [Boto3 SageMaker client reference](https://boto3.amazonaws.com/v1/documentation[AWS_SECRET_ACCESS_KEY].html)
* [SageMaker Python SDK documentation](https://sagemaker.readthedocs.io/)
* [SageMaker runtime (invoke\_endpoint) API](https://boto3.amazonaws.com/v1/documentation[AWS_SECRET_ACCESS_KEY]-runtime.html)

You can now inspect the created model, endpoint configuration, and endpoint status in the Management Console, or proceed to implement the same flow using the SageMaker SDK’s high-level APIs and the Predictor class.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/772ec99e-54ee-4f4f-8b2a-08b5bc4d4a32/lesson/09a6960f-eb31-48e0-a5a8-43dfd433c521" />
</CardGroup>


# Demo End to End CICD ML Pipelines from SageMaker Project Templates

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-MLOps-Engineer/Demo-End-to-End-CICD-ML-Pipelines-from-SageMaker-Project-Templates/page

Demo of end-to-end SageMaker project templates provisioning CI/CD for ML workflows that build, register, approve and deploy models

This lesson walks through building a complete CI/CD workflow that integrates SageMaker Pipelines with AWS developer tools. Using a SageMaker Project template, we provision the infrastructure, trigger model builds, register models in the Model Registry, and deploy them across staging and production with a manual approval gate.

Core steps:

* Review built‑in SageMaker Project templates.
* Use a template that provisions a Git‑compatible repository (AWS CodeCommit in this demo).
* Inspect the CloudFormation template that the SageMaker Project uses and follow the resulting CI/CD flow (CodeCommit → CodePipeline → CodeBuild → SageMaker Pipelines → Model Registry → deployment).

Start in SageMaker Studio and confirm a clean environment (no model packages, no endpoints).

<Frame>
  <img alt="A dark-themed screenshot of the AWS SageMaker Studio Home dashboard showing onboarding panels, navigation sidebar (JupyterLab, RStudio, Code Editor, etc.), and a &#x22;Recent spaces&#x22; section. A large pointer/cursor is clicking the &#x22;Models&#x22; item in the left sidebar." />
</Frame>

At the start of the lesson there are no model packages or endpoints in the account.

<Frame>
  <img alt="A screenshot of the Amazon SageMaker Studio &#x22;Endpoints&#x22; page in dark mode showing no deployed endpoints. The left navigation pane with apps and deployment options is visible and there's a &#x22;Create endpoint&#x22; button at the top right." />
</Frame>

The Models view is empty as well.

<Frame>
  <img alt="A screenshot of the Amazon SageMaker &#x22;Models&#x22; page in the AWS console showing an empty models list. The left navigation menu (Admin configurations, JumpStart, Inference, etc.) and browser tabs are visible, with a large mouse cursor near the center." />
</Frame>

## Create a SageMaker Project from a Template

From SageMaker Studio navigate to Deployments → Projects and choose a project template. Templates are blueprints that create all required CI/CD and ML infra (for example: CodeCommit repos, CodeBuild projects, CodePipeline pipelines, S3 artifacts buckets, SageMaker Pipelines, IAM roles) using a CloudFormation stack.

<Callout icon="warning">
  Effective September 9, 2024, SageMaker project templates that create AWS CodeCommit repositories are deprecated. This demo uses a CodeCommit template to show the in-console experience, but for production consider third‑party Git providers (e.g., GitHub) with a CodeStar connection or equivalent.
</Callout>

Choose a template that creates both:

* a model‑build pipeline (trains and registers models), and
* a model‑deploy pipeline (staging → production with a manual approval gate).

Templates that integrate with third‑party Git providers will prompt for repo URLs and branches instead of creating CodeCommit repos.

<Frame>
  <img alt="A screenshot of the AWS SageMaker Studio &#x22;Create project&#x22; page showing a list of MLOps project templates (one highlighted) and a large left navigation sidebar with tools like JupyterLab and RStudio. A cursor is visible over the selected template." />
</Frame>

Supply a project name, description, and tags that fit your org conventions.

<Frame>
  <img alt="Screenshot of the AWS SageMaker Studio &#x22;Create project&#x22; page in dark mode, showing a left navigation sidebar and a central form. The form is filled with project name &#x22;kodekloud-sm-project&#x22;, description &#x22;Demonstration project&#x22;, and a tag owner=mlops." />
</Frame>

When the project is created, SageMaker launches a CloudFormation stack that provisions the resources described by the template. Open the CloudFormation console to monitor stack events and inspect created resources (S3 buckets, CodeCommit repos, CodeBuild projects, CodePipeline pipelines, SageMaker Pipelines, IAM roles, etc.).

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console showing a stack named &#x22;SC-485186561655-...&#x22; on the left and a list of resources (CodeCommit repositories, CodePipeline, CodeBuild projects, Event rules) with statuses like CREATE_IN_PROGRESS and CREATE_COMPLETE on the right. The browser tabs and AWS service icons are visible across the top." />
</Frame>

You can inspect the CloudFormation template (a declarative YAML manifest) used by the project. The template declares parameters for the SageMaker project and resources such as an artifacts S3 bucket, EventBridge rules, CodeCommit repositories, CodeBuild projects, and CodePipeline pipelines.

Example excerpt from the template:

```yaml theme={null}
Description: >
  Toolchain template which provides the resources needed to represent
  infrastructure as code. This template specifically creates a CI/CD pipeline
  to build a model using a SageMaker Pipeline and deploy the resulting trained
  ML Model from Model Registry to two stages in CD -- staging and production.

Parameters:
  SageMakerProjectName:
    Type: String
    Description: Name of the project
    MinLength: 1
    MaxLength: 32
    AllowedPattern: '^[a-zA-Z](-*[a-zA-Z0-9])*'
  SageMakerProjectId:
    Type: String
    Description: Service generated Id of the project.

Resources:
  MLOpsArtifactsBucket:
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain
    Properties:
      BucketName:
        Fn::Sub: sagemaker-project-${SageMakerProjectId}

  ModelBuildCodeCommitRepository:
    Type: AWS::CodeCommit::Repository
    Properties:
      RepositoryName:
        Fn::Sub: sagemaker-${SageMakerProjectName}-${SageMakerProjectId}-modelbuild
      RepositoryDescription:
        Fn::Sub: 'SageMaker Model building workflow infra-as-code for Project ${SageMakerProjectName}'
      Code:
        S3:
          Bucket: sagemaker-servicecatalog-seedcode-eu-central-1
          Key: toolchain/model-building-workflow-v1.0.zip
      BranchName: main

  SageMakerModelPipelineBuildProject:
    Type: AWS::CodeBuild::Project
    Properties:
      Name:
        Fn::Sub: sagemaker-${SageMakerProjectName}-${SageMakerProjectId}-modelbuild
      Description: 'Builds the model building workflow code repository, creates the SageMaker Pipeline and executes it'
```

When the stack completes, the new SageMaker Project appears in Studio.

<Frame>
  <img alt="A screenshot of the AWS SageMaker Studio &#x22;Projects&#x22; page showing a project named &#x22;kodekloud-sm-project&#x22; with status &#x22;Create completed.&#x22; The dark-themed interface includes a left navigation pane (JupyterLab, RStudio, etc.) and a large mouse cursor visible over the workspace." />
</Frame>

## Inspect the Generated Code Repositories

The CloudFormation stack created two source repositories (model‑build and model‑deploy). Open CodeCommit to review the seed code: buildspecs, helper scripts, CloudFormation templates, and the sample SageMaker pipeline code that the build runs.

<Frame>
  <img alt="A screenshot of the AWS CodeCommit web console showing the &#x22;sagemaker-kodekloud-sm-project-...&#x22; repository file listing and README preview. The Amazon Q generative assistant panel is visible on the right and a large black mouse cursor is over the file list." />
</Frame>

## CodePipeline: CI/CD Orchestration

The project provisions two CodePipeline pipelines:

* Model build pipeline — triggers on commits to the model‑build repo, runs CodeBuild to create and execute a SageMaker Pipeline that preprocesses, trains, evaluates, and registers a model.
* Model deploy pipeline — triggers on commits to the model‑deploy repo or on model approval events; packages CloudFormation templates and deploys staging and production endpoints. A manual approval action gates production.

Open CodePipeline to view pipeline stages and their status.

<Frame>
  <img alt="A screenshot of the AWS Management Console showing the CodePipeline Pipelines page with two pipelines listed — one marked Failed and the other In progress. The left sidebar shows developer tools navigation (Source, Artifacts, Build, Deploy, Pipeline) and there's a &#x22;Create pipeline&#x22; button in the top-right." />
</Frame>

When CodeCommit is seeded by the template, CodePipeline detects commits and starts the model build pipeline automatically.

<Frame>
  <img alt="A screenshot of the AWS CodePipeline console showing a pipeline named &#x22;sagemaker-kodekloud-sm-proj...&#x22; with Source and Build stages (Source succeeded, Build in progress). The browser window shows the AWS navigation bar and multiple open tabs." />
</Frame>

## CodeBuild: How the Pipeline Invokes a SageMaker Pipeline

During the build stage, CodePipeline invokes a CodeBuild project. CodeBuild executes the repository's buildspec.yml which installs dependencies and runs a helper that programmatically creates and executes the SageMaker Pipeline.

Representative buildspec from the model‑build repository:

```yaml theme={null}
