# python
import boto3

# Define your Model Package Group Name
model_package_group_name = "kodekloud-model-package-group"

# Initialize the SageMaker client
sagemaker_client = boto3.client("sagemaker")

# Create the Model Package Group
response = sagemaker_client.create_model_package_group(
    ModelPackageGroupName=model_package_group_name,
    ModelPackageGroupDescription="A description of the model package group.",
)

print("Model Package Group ARN:", response["ModelPackageGroupArn"])
```

<Callout icon="lightbulb">
  I am using Boto3 here because older codebases (before the SageMaker SDK added native model registry support around 2021–2022) often used Boto3 for model registry operations. If you are starting fresh today, you can use the [SageMaker Python SDK](https://sagemaker.readthedocs.io/) which now includes first-class model registry support.
</Callout>

Registering a model package (create a version)
A model package ties together the model artifact (S3 tarball), a container image to serve the model, supported content/response MIME types, and an initial approval status (PendingManualApproval, Approved, or Rejected).

```python theme={null}
# python
import boto3
from sagemaker import Session, image_uris

# Initialize clients/sessions
sagemaker_client = boto3.client("sagemaker")
sagemaker_session = Session()  # uses current boto3 credentials

bucket = sagemaker_session.default_bucket()
prefix = "house-price-linearlearner"

# S3 location of your model artifact
model_artifact = (
    f"s3://{bucket}/{prefix}/output/linear-learner-2025-01-15-10-20-05-283/output/model.tar.gz"
)

# Retrieve an inference container image URI for the framework
inference_image_uri = image_uris.retrieve(framework="linear-learner", region="us-east-01")

# Create the model package (version)
model_package_response = sagemaker_client.create_model_package(
    ModelPackageGroupName=model_package_group_name,
    ModelPackageDescription="House price linear learner model",
    InferenceSpecification={
        "Containers": [
            {
                "Image": inference_image_uri,
                "ModelDataUrl": model_artifact,
            }
        ],
        "SupportedContentTypes": ["text/csv"],
        "SupportedResponseMIMETypes": ["text/csv"],
    },
    ModelApprovalStatus="PendingManualApproval",
)

print("Model Package ARN:", model_package_response["ModelPackageArn"])
```

Approval workflow and CI/CD integration

* After creating a model package with ModelApprovalStatus="PendingManualApproval", a governance reviewer inspects the model in SageMaker Studio (explainability, bias, metrics, lineage).
* If approved, Studio can change the approval state to "Approved", which you can wire into CI/CD (for example, a pipeline triggered on approval to deploy the approved model).
* If rejected, the version can be blocked from deployment, or a rollback/alternative version can be selected.

<Frame>
  <img alt="A screenshot of a &#x22;Workflow: Using Model Registry&#x22; interface showing a model version page with Train/Evaluate/Audit sections and a metrics table of performance values. A Deploy dropdown marked &#x22;Pending Approval&#x22; is highlighted, with a note that changing to &#x22;Approved&#x22; triggers the CI/CD pipeline for deployment." />
</Frame>

Why use model package groups?

* Organization: Group related models by function, project, or product to reduce clutter.
* Versioning: Keep each model version with its artifacts, metrics, and metadata for traceability.
* Governance: Separate development and review responsibilities; reviewers can validate explainability and bias before approval.
* Integration: Use approval-state events to trigger CI/CD pipelines for automated rollout or controlled deployment.

A model registry converts scattered artifacts into a structured, auditable, and deployable catalog of models.

<Frame>
  <img alt="A funnel diagram titled &#x22;Results: Efficient Model Management and Deployment&#x22; showing raw model icons entering the funnel and passing through layers labeled Organization, Governance, and Integration to produce a deployable, version-controlled model at the bottom. The graphic illustrates the process of refining raw models into production-ready, managed models." />
</Frame>

Alternatives and integration options

* Self-managed registries: Build a tracking/catalog solution with [AWS DynamoDB](https://aws.amazon.com/dynamodb/) or a relational database.
* MLflow: Open-source experiment tracking and model registry ([mlflow.org](https://mlflow.org/)).
* SageMaker Model Registry: Built into SageMaker and integrates with AWS IAM, Studio, SDKs, and CI/CD pipelines — ideal for AWS-centric workflows.

Choose and standardize on an approach to avoid losing model lineage and to enforce governance and deployment patterns.

<Frame>
  <img alt="A slide titled &#x22;Results: Efficient Model Management and Deployment&#x22; showing a &#x22;Model Registry Approach&#x22; where arrows from &#x22;Self-Managed&#x22; and &#x22;MLFlow&#x22; flow into the &#x22;SageMaker Model Registry.&#x22;" />
</Frame>

Summary of benefits

* Faster deployment via approval-triggered pipelines and automation.
* Robust version control and better artifact management.
* Clear collaboration between data scientists and governance teams.
* Seamless rollback or replacement using versioned model packages.
* Improved governance and compliance through audit trails and access controls.

<Frame>
  <img alt="A slide titled &#x22;Results: Efficient Model Management and Deployment&#x22; showing SageMaker Model Registry in the center with five surrounding benefits: Faster Deployment, Efficient Model Management, Improved Collaboration, Seamless Rollback, and Governance & Compliance." />
</Frame>

What we covered in this lesson

* The distinct roles and interfaces for interacting with a model registry (data scientist vs governance officer).
* How to create a Model Package Group and register a Model Package programmatically.
* How SageMaker Model Registry supports approvals, audit trails, explainability/bias artifacts, and integration with CI/CD.
* Alternatives such as MLflow or custom registries, and reasons to choose the built-in SageMaker Model Registry if you operate primarily in AWS.

Further reading and references

* [SageMaker Model Registry documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html)
* [SageMaker Python SDK](https://sagemaker.readthedocs.io/)
* [Boto3 SageMaker client](https://boto3.amazonaws.com/v1/documentation[AWS_SECRET_ACCESS_KEY].html)
* [MLflow project and model registry](https://mlflow.org/)
* [AWS DynamoDB overview](https://aws.amazon.com/dynamodb/)

A follow-up lesson will demonstrate a full end-to-end example: registering a model, running a governance review, and triggering a deployment pipeline after approval.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/36db8fab-85cc-40f0-8594-573631b0425b/lesson/e9896936-f010-4b3e-8c69-e1c6546f0b45" />
</CardGroup>


# Keeping Track of Models Using the SageMaker Model Registry

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-Data-Scientist/Keeping-Track-of-Models-Using-the-SageMaker-Model-Registry/page

Managing model versions and approvals using Amazon SageMaker Model Registry for organized tracking, deployment automation, governance, and rollback

In this lesson, we'll learn how to keep track of multiple models and their versions using the Amazon SageMaker Model Registry.

What we'll cover:

* The challenge of managing many model artifacts and versions.
* How the SageMaker Model Registry registers, annotates, and controls model promotion.
* How registry-driven approvals enable organized management, collaboration, rollback, and faster deployment of retrained models.

Let's begin.

A common scenario: a data scientist runs experiments and produces many candidate model artifacts in S3. Which artifact should go into production?

You might choose a winner based on evaluation metrics or allow an AutoML workflow to pick one. For example, you might decide that model version 2.1 is the best candidate to deploy.

Models typically degrade over time as data drifts. Monitoring may detect degradation and trigger retraining that produces a new artifact (for example, v3.1). That raises operational and governance questions:

* Which version is currently approved for production?
* Which new version should replace it?
* Is an approval process required before deployment?
* How do we automate the swap (deploy new model / retire old model) reliably?

If your organization runs many projects and retrains frequently, artifacts accumulate quickly:

```bash theme={null}
model_v1.tar.gz
model_v2.tar.gz
model_v3.tar.gz
model_v1.1.tar.gz
model_v2.1.tar.gz
model_v3.1.tar.gz
```

How do you organize these models, map them to projects, and determine the active production version? Ideally, you also want to view each candidate’s metrics and metadata to make informed selections.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Managing Model Versions and Ensuring Compliance&#x22; showing six model archive icons (e.g., model_v1.tar.gz, model_v2.1.tar.gz) on the left. On the right are three questions: How do we organize these models? What are the regulatory compliance requirements? Which model should be deployed?" />
</Frame>

Solution overview: the SageMaker Model Registry

The SageMaker Model Registry is designed to solve these problems by providing:

* A single source of truth for model artifacts and versions.
* The ability to annotate models with evaluation metrics, tags, and rich metadata.
* Approval states that gate deployment to production and can trigger automation.

A registered model becomes a control point: approving a model package can start a deployment pipeline; rejecting a package can initiate rollback or withdrawal procedures.

<Frame>
  <img alt="A slide titled &#x22;Solution: SageMaker Model Registry&#x22; showing three feature boxes — &#x22;Tracks Models&#x22;, &#x22;Manages Versions&#x22;, and &#x22;Approval States&#x22; — flowing into a highlighted &#x22;Model Registry&#x22; tile. The design uses a dark background with teal/accented boxes." />
</Frame>

Model Registry and SageMaker Studio

In SageMaker Studio, the Model Registry is exposed via the Studio UI, letting you inspect registered models, their metadata, and approval states. Note: models trained in SageMaker are not automatically registered — registration must be done explicitly through the console, the SDK, or programmatically from pipelines.

<Frame>
  <img alt="A screenshot titled &#x22;Solution: SageMaker Model Registry&#x22; showing the AWS SageMaker Studio Models page. The interface displays the Registered models tab (empty), with buttons to register or deploy models and a left-hand navigation menu." />
</Frame>

<Callout icon="lightbulb">
  You must create a Model Package Group (sometimes called a model group) and then register model packages (versions) under that group. Registration can be done via the SageMaker console, the SDK ([boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) / [sagemaker Python SDK](https://sagemaker.readthedocs.io/en/stable/)), or programmatically (for example, from CI/CD pipelines).
</Callout>

What is a Model Package Group?

A Model Package Group is a logical collection that groups related model versions. How you structure groups depends on your organizational and team conventions. Common strategies include grouping by project, business problem, or model type.

Model group structuring options:

| Grouping strategy    | Use case                                                    | Example                   |
| -------------------- | ----------------------------------------------------------- | ------------------------- |
| Per project          | Keep all versions for a single product or team in one place | `fraud-detection-project` |
| Per business problem | Group models by the problem they solve across teams         | `time-series-forecasting` |
| Per model type       | Organize models of similar architecture or task             | `nlp-classifiers`         |

Choose a grouping strategy that maps to ownership, governance requirements, and traceability needs.

<Frame>
  <img alt="A slide titled &#x22;Solution: SageMaker Model Registry&#x22; showing three ways to structure model groups: Per Project, Per Business Problem, and Per Model Type, each with a short description. It visually branches from a central &#x22;Ways to structure model groups&#x22; node to the three options." />
</Frame>

Conceptual relationship between components

* Model artifact: the artifact stored in S3 (for example, model.tar.gz or model\_v2.1.tar.gz).
* Model Package Group: the logical container for related models.
* Model Package (model version): registering an artifact in a package group creates a Model Package entry (a version) inside that group.

Each time you register a package in the same group, you create a new version entry under that group.

<Frame>
  <img alt="A diagram titled &#x22;Solution: SageMaker Model Registry.&#x22; It shows a Model Artifact being registered to create a Model Version inside a Model Package Group within the SageMaker Model Registry." />
</Frame>

Model lifecycle and approval states

When a model package is registered you can annotate it with evaluation metrics, tags, and other metadata. SageMaker Model Registry tracks approval status for each package, commonly using:

| Approval state        | Description                             | Typical action                                           |
| --------------------- | --------------------------------------- | -------------------------------------------------------- |
| PendingManualApproval | Awaiting human review before production | Trigger manual review or a governance workflow           |
| Approved              | Cleared for production deployment       | Trigger CI/CD or pipeline deployment                     |
| Rejected              | Not approved for production             | Block deployment; optionally trigger rollback or retrain |

Approval states enforce governance and separation of duties: data scientists register and annotate models, and authorized governance or ops roles change approval to Approved to allow deployment. This prevents unvetted models from reaching production.

The Model Registry addresses real-world ML lifecycle challenges:

* Model versioning: maintain curated, versioned model packages in groups.
* Deployment & rollback: approval states act as triggers for automated rollout or rollback via CI/CD and pipelines.
* Collaboration & governance: approval workflows + IAM enforce separation of duties and auditability.
* Consistency & provenance: centralized metadata stores training, evaluation, lineage, and version history.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: SageMaker Model Registry&#x22; outlining challenges (Model Versioning, Deployment & Rollback, Collaboration & Governance, Consistency). It shows the model registry benefits: tracks and organizes versions, simplifies deployment and rollback, enhances collaboration/governance, and ensures consistency." />
</Frame>

Practical notes and recommended next steps

* Create a Model Package Group for each logical set of related models (per your chosen strategy).
* Register model packages by providing the artifact S3 URI, inference container image, and metadata (metrics, tags, training/job lineage).
* Include evaluation metrics and tags so stakeholders can select models easily in the registry UI.
* Automate promotion and deployment using CI/CD pipelines and AWS EventBridge: when a model package’s approval state becomes Approved, trigger deployment pipelines; when Rejected, trigger withdrawal or rollback workflows.
* Use IAM policies and fine-grained permissions to ensure only authorized roles can change approval states—this provides governance and traceability.
* Integrate model monitoring and drift detection to close the loop: monitoring can trigger retraining, which registers a new package and starts the review pipeline.

With the SageMaker Model Registry you get an auditable, enforceable, and automatable system for managing model versions, approvals, and lifecycle transitions—rather than ad hoc S3 folders with unclear provenance.

Links and references

* [SageMaker Model Registry (AWS Docs)](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html)
* [SageMaker Studio (AWS Docs)](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html)
* [Amazon EventBridge (AWS Docs)](https://docs.aws.amazon.com/eventbridge/latest/userguide/what-is-amazon-eventbridge.html)
* [boto3 SDK](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
* [sagemaker Python SDK](https://sagemaker.readthedocs.io/en/stable/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/36db8fab-85cc-40f0-8594-573631b0425b/lesson/8b2a6bb9-aaf5-4e0e-96af-c5d0f35f7c39" />
</CardGroup>
