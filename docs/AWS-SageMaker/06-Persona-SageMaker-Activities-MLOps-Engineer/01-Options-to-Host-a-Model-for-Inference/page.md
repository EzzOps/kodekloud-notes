# Initialize the SageMaker client
sagemaker_client = boto3.client("sagemaker")

# Define your model name (this model must already exist in SageMaker)
model_name = "linear-learner-model"

# Define the endpoint configuration name
endpoint_config_name = "linear-learner-endpoint-config"

# Create the endpoint configuration
response = sagemaker_client.create_endpoint_config(
    EndpointConfigName=endpoint_config_name,
    ProductionVariants=[
        {
            "VariantName": "AllTraffic",
            "ModelName": model_name,               # Reference to the existing model
            "InstanceType": "ml.m5.large",        # Choose an appropriate instance type
            "InitialInstanceCount": 1              # Number of instances for the endpoint
        }
    ]
)

print(f"Endpoint configuration '{endpoint_config_name}' created successfully.")
```

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: Creating SageMaker Endpoints With boto3&#x22; showing three teal boxes numbered 01–03. The steps state that endpoint config defines endpoint properties, boto3 provides create_endpoint_config, and endpoint config specifies compute properties." />
</Frame>

## Config ≠ Endpoint

Creating an Endpoint Configuration does not provision the actual serving endpoint. An Endpoint is a separate resource that references the Endpoint Configuration and must be created explicitly.

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: Creating SageMaker Endpoints With boto3&#x22; showing that a SageMaker Endpoint Config must be referenced when creating a SageMaker Endpoint, illustrated by two labeled boxes connected with a dashed arrow. The slide includes the note &#x22;Config ≠ Endpoint&#x22; and a small copyright credit to KodeKloud." />
</Frame>

## Boto3: create the Endpoint

After the Endpoint Configuration exists, create the Endpoint and point it at that config:

```python theme={null}
# Define the endpoint name
endpoint_name = "linear-learner-endpoint"

# Create the endpoint using the previously created configuration
response = sagemaker_client.create_endpoint(
    EndpointName=endpoint_name,
    EndpointConfigName=endpoint_config_name  # Reference to the endpoint configuration
)

print(f"Endpoint '{endpoint_name}' is being created. This may take a few minutes...")
```

The endpoint provisioning takes a few minutes. Monitor status via the AWS Management Console (SageMaker → Inference → Endpoints) or SageMaker Studio (Deployments). Both UIs reflect the same underlying Endpoint object and offer a "Create endpoint" button if you prefer a UI approach.

## Invoke a SageMaker Endpoint with Boto3 Runtime

To send prediction requests to a deployed endpoint using Boto3, use the SageMaker Runtime client (sagemaker-runtime) and its invoke\_endpoint method. Ensure the payload and ContentType header match your model's expected serialization:

```python theme={null}
import boto3
import json

# Initialize the SageMaker Runtime client
sagemaker_runtime = boto3.client("sagemaker-runtime")

# Define the endpoint name (must be an existing deployed endpoint)
endpoint_name = "my-deployed-endpoint"

# Sample input data (formatted as JSON)
payload = json.dumps([[5.1, 3.5, 1.4, 0.2]])  # Example for a model expecting numerical inputs

# Send request to the endpoint
response = sagemaker_runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType="application/json",  # Adjust based on your model's expected format
    Body=payload
)

# Read and decode the response
result = json.loads(response["Body"].read().decode())

# Print the model's prediction
print(result)
```

<Frame>
  <img alt="A slide titled &#x22;Workflow: Creating Inference Request With boto3&#x22; showing a four-step flow: 1) Input Data, 2) invoke_endpoint(), 3) SageMaker Endpoint, and 4) Response Parsed. The steps are displayed as teal chevrons with numbered blue circles." />
</Frame>

## SageMaker Python SDK: Model.deploy (higher-level)

The SageMaker Python SDK provides an ML-focused abstraction. Instead of manually creating an Endpoint Configuration, you define a Model object and call deploy; the SDK creates the Endpoint Configuration and Endpoint for you. This reduces boilerplate and lets you focus on model code and iteration.

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: Creating SageMaker Endpoints With SageMaker SDK&#x22; showing three numbered panels. The panels note: (1) SageMaker SDK provides a more abstract level, (2) endpoint config isn't explicitly defined but is still created, and (3) the model object is defined first then deploy is called." />
</Frame>

## Example: create a Model and deploy it (SageMaker SDK)

This example shows how to use the SageMaker SDK to create a Model pointing to a model artifact in S3 and an inference container image, then deploy it as an endpoint.

```python theme={null}
import sagemaker
from sagemaker import Model

# Initialize SageMaker session and role
sagemaker_session = sagemaker.Session()
iam_role = "arn:aws:iam::123456789012:role/service-role/AmazonSageMaker-ExecutionRole"

# Define the S3 location of your trained model artifact (output from a training job)
model_artifact_s3_uri = "s3://your-bucket/path-to-model/model.tar.gz"

# Retrieve an appropriate container image for inference (e.g., linear-learner)
container_image_uri = sagemaker.image_uris.retrieve(
    framework="linear-learner",
    region=sagemaker_session.boto_region_name
)

# Create the Model object
model = Model(
    image_uri=container_image_uri,
    model_data=model_artifact_s3_uri,
    role=iam_role,
    sagemaker_session=sagemaker_session
)
```

Deploying returns a Predictor-like object that simplifies inference calls—the SDK handles serialization for you.

```python theme={null}
# Deploy the model as an endpoint
predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name="linear-learner-endpoint"
)

print("Endpoint deployed successfully!")
```

Using the returned predictor:

```python theme={null}
response = predictor.predict([[5.1, 3.5, 1.4, 0.2]])  # Example input data
print(response)
```

## Mixed approach: custom infra with Boto3, inference with SageMaker SDK

If you need a custom Endpoint Configuration the SageMaker SDK cannot express, combine the two approaches: create the configuration and endpoint with Boto3, then use the SageMaker SDK's Predictor to call that existing endpoint for ergonomic inference code:

```python theme={null}
from sagemaker.predictor import Predictor

# If endpoint already exists (created by Boto3), create a Predictor wrapper
predictor = Predictor(endpoint_name="existing-custom-endpoint", sagemaker_session=sagemaker_session)

# Use predictor.predict which will handle serialization depending on the predictor implementation
result = predictor.predict([[5.1, 3.5, 1.4, 0.2]])
print(result)
```

This hybrid approach gives you advanced infrastructure control while keeping inference client code clean.

<Frame>
  <img alt="A flowchart titled &#x22;Workflow: SDK Workflow&#x22; comparing three approaches (pure boto3, pure SageMaker SDK, and a mixed approach) for deploying and invoking AWS SageMaker endpoints. It shows steps like create_endpoint_config, create_endpoint, model deploy/returning a Predictor object, and calling invoke_endpoint/predict, split into &#x22;Infrastructure deploy&#x22; and &#x22;Calling the endpoint for inference prediction.&#x22;" />
</Frame>

## Why use SageMaker Endpoints?

SageMaker Endpoints are the native, managed option for real-time inference. Key benefits:

* Deploy quickly: minimal infra code required to go from a trained model to a hosted endpoint.
* Scalable: integrates with autoscaling to handle traffic spikes and variable load.
* Easy updates: supports multiple production variants, enabling canary, blue-green, and A/B testing.
* Cost control: right-size instances and use autoscaling to reduce hosting costs.
* Production-ready: built for enterprise workloads and integrated with AWS monitoring and security.

> **warning** Running real-time endpoints incurs compute and networking costs while the instances are provisioned. Use autoscaling, smaller instance types for development, or alternatives (asynchronous/batch inference) when strict real-time latency is not required.

<Frame>
  <img alt="A presentation slide titled &#x22;Results&#x22; showing five numbered benefit cards. They list: Deploy Quickly (no infrastructure worries), Scalable (handles traffic spikes), Easy Updates (shortens feedback loop), Cost-Effective (dynamic scaling), and Real-World Use (used by VW Group and NASCAR for inference hosting)." />
</Frame>

## Key takeaways

* Amazon SageMaker Endpoints provide managed hosting for real-time inference and can be created via Boto3 (fine-grained control) or the SageMaker Python SDK (higher-level abstraction).
* With Boto3: create an Endpoint Configuration, then create an Endpoint, and invoke it via the sagemaker-runtime client.
* With the SageMaker SDK: create a Model object and call deploy; the SDK creates the Endpoint Configuration and Endpoint for you, returning a Predictor that simplifies inference calls.
* You can mix approaches: use Boto3 to provision custom infra and the SageMaker SDK Predictor for ergonomics when invoking the endpoint.
* Consider alternatives (asynchronous inference, batch transform) for workloads that do not require low-latency, always-on endpoints.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; that lists five key points about Amazon SageMaker hosting. It notes that models can be hosted on any compute platform, SageMaker Endpoints are the native hosting option using an Endpoint Configuration, endpoints can be created with boto3 or the SageMaker SDK, and inference handler code is provided automatically." />
</Frame>

## Further reading and references

* Boto3 SageMaker client documentation: [https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html)
* SageMaker Python SDK docs: [https://sagemaker.readthedocs.io/en/stable/](https://sagemaker.readthedocs.io/en/stable/)
* SageMaker real-time endpoints overview: [https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html](https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html)
* SageMaker Studio: [https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html)

This wraps up the lesson. Next topics to consider: asynchronous inference and batch transform jobs, which are excellent alternatives when real-time low-latency serving is not required.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/772ec99e-54ee-4f4f-8b2a-08b5bc4d4a32/lesson/8b5b06b8-568a-49b2-a4b2-fe2d6c536d89)


# Options to Host a Model for Inference

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-MLOps-Engineer/Options-to-Host-a-Model-for-Inference/page

Describes options for hosting ML models for inference and recommends AWS SageMaker Endpoints for managed, low latency, autoscaling production deployments.

You now have a trained model artifact registered in a model registry with tracked metadata and lineage. The next step is hosting that model so it can accept requests and return predictions. This guide explains the hosting problem, common hosting choices, and why Amazon SageMaker Endpoints are a production-ready managed hosting option on AWS.

At a high level, hosting a model requires:

* Compute to run the model (VM, container, or managed instance).
* An inference handler: code that accepts requests, pre-processes input, calls the model, then post-processes output.
* A transport layer for clients to access the handler (HTTP API, message queue, batch jobs, etc.).

The inference handler acts as the bridge between a caller and the model: deserialize incoming data, format it for the model, invoke the model, then serialize the response back to the client.

<Frame>
  <img alt="A diagram titled &#x22;Problem: Hosting Model for Inference&#x22; showing an inference request (house features like bedrooms, bathrooms, square footage, neighborhood) flow into an inference handler and compute platform/model, producing an inference response with a predicted price and the same input features." />
</Frame>

The diagram above illustrates a typical request flow: a client submits features (e.g., bedrooms: 3, bathrooms: 2, square footage: 3,000, neighborhood: suburban) to the inference handler running on your compute platform. The handler prepares model inputs, runs inference, and returns a predicted price (e.g., \$300,000) plus any metadata.

Where to host the model and inference handler? Options include on-premises servers, other cloud providers, or several AWS compute services. Each choice has trade-offs in cost, operational complexity, latency, scalability, and integration with your CI/CD pipeline.

| Hosting Option        | Best for                                               | Example / Notes                                      |
| --------------------- | ------------------------------------------------------ | ---------------------------------------------------- |
| On-Premises           | Organizations with data residency or strict compliance | Full control, higher ops burden                      |
| Other Cloud Providers | Multi-cloud strategies or vendor preference            | Depends on provider-managed services                 |
| AWS EC2               | Custom, long-running VMs                               | Flexible but requires OS/container management        |
| AWS ECS / EKS         | Containerized deployments with orchestration           | Better automation; still manage nodes or use Fargate |
| SageMaker Endpoints   | Managed ML inference with minimal infra ops            | Low-latency, autoscaling, versioning support         |

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Hosting Model for Inference&#x22; showing an inference_handler_code and model inside a compute platform. The right side lists three hosting options: On‑Premises, Another Cloud Provider, and AWS (EC2, ECS, EKS)." />
</Frame>

If you're starting on AWS, SageMaker Endpoints are a great place to begin. SageMaker provides a managed hosting option that reduces operational overhead: you supply the compute and container image (or use a built-in container), and SageMaker provisions and manages instances and containers for you.

> **lightbulb** If you are new to ML production on AWS, start with a SageMaker Endpoint to minimize infrastructure work and get predictable, low-latency inference quickly.

Key benefits of SageMaker Endpoints:

* Fully managed hosting: SageMaker provisions instances and containers and manages lifecycle, OS, and patching.
* Low-latency, real-time predictions for synchronous workflows (e.g., fraud detection, personalization).
* Autoscaling: scale instance count automatically in response to traffic.
* Safe updates: built-in mechanisms to roll out new model versions (supporting blue/green, canary, or A/B strategies).
* Flexible pricing: pay-as-you-go for instances; use serverless/async/batch options for cost-efficient non-real-time use cases.

SageMaker follows the same managed pattern used for training and processing jobs: you declare resources and the container image, and SageMaker creates managed compute, runs the workload, and exposes endpoints. For inference, SageMaker deploys containers that host the model artifact and your inference handler (or a SageMaker-provided serving stack). You do not need to manage the underlying OS or instances.

<Frame>
  <img alt="The slide titled &#x22;Solution: SageMaker Endpoints&#x22; shows two managed ML instances (ml.m5.large) running container images that include a Model and inference_handler_code. To the right is a five-point list of benefits: fully managed hosting, low-latency real-time predictions, automatic scaling, updates without downtime, and pay-only-for-used-resources." />
</Frame>

Additional SageMaker capabilities and common serving patterns:

* Real-time endpoints: synchronous, low-latency responses with instance-backed hosting.
* Serverless inference: run model code without provisioning instances (good for low or spiky traffic).
* Asynchronous endpoints: submit requests and retrieve results later (useful for long-running or variable-latency inference).
* Batch Transform jobs: high-throughput offline inference over large datasets.
* Multi-Model Endpoints (MME): host many small models on the same endpoint and load them on-demand to reduce cost.

Autoscaling and cost-control considerations:

* Choose instance type and initial count (e.g., ml.m5.large) based on latency and memory/CPU requirements.
* Use SageMaker autoscaling to adjust instance count to traffic.
* For workloads that are infrequent or bursty, evaluate serverless or asynchronous endpoints to avoid always-on instance costs.

Updating endpoints and model rotation:

* SageMaker supports programmatic endpoint updates for rolling new model versions into production.
* Typical flow: create a new model resource (pointing to the new model artifact and container), create a new endpoint configuration, then call UpdateEndpoint to switch traffic.
* This supports deployment strategies used in DevOps: canary releases, blue/green swaps, and A/B tests.

Example: Creating and updating a SageMaker endpoint using boto3

* Steps:
  1. Create a Model resource that references your model artifact and container image.
  2. Create an Endpoint Configuration specifying instance type and count.
  3. Create the Endpoint from that configuration.
  4. To deploy a new model, create a new Model + Endpoint Configuration and call UpdateEndpoint.

```python theme={null}
import boto3

sagemaker = boto3.client("sagemaker")
role_arn = "arn:aws:iam::123456789012:role/SageMakerExecutionRole"
model_name = "house-price-model-v1"
container_image = "123456789012.dkr.ecr.us-west-2.amazonaws.com/my-serving-image:latest"
model_artifact_s3 = "s3://my-bucket/models/house-price/model.tar.gz"
