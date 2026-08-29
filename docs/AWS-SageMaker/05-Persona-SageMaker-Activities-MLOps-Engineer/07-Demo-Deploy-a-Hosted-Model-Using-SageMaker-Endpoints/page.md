# boto3-based inference invocation using SageMaker runtime
import boto3
import json

# endpoint_name should match the endpoint you created earlier
# e.g., endpoint_name = 'my-endpoint-using-boto3'
# Example CSV input (features expected by the model)
input_data = (
    '51.6215527,-0.2466031,2.0,6.0,517.0,3.0,289000.0,27.393364928999096,'
    '1055000.0,37.01298701298701,285000.0,1354000.0,1.0,0.0,0.1,0.0,0.0,0.0,'
    '0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0'
)

# Create the SageMaker runtime client for real-time invocation
sagemaker_runtime_client = boto3.client('sagemaker-runtime')

response = sagemaker_runtime_client.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType='text/csv',
    Body=input_data
)

# Decode and print the response
prediction_payload = response['Body'].read().decode('utf-8')
print(f'Predicted house price: {prediction_payload}')
```

Example console output:

```text theme={null}
Predicted house price: {"predictions": [{"score": 1789161.25}]}
```

The response above is a JSON payload containing a numeric score (approx. 1,789,161.25). In this demo, the model is a linear regression predictor that returns a `predictions` array with a `score` field.

## Use the SageMaker Python SDK (Model.deploy + Predictor)

The SageMaker Python SDK provides a higher-level API to create and deploy models. `Model.deploy(...)` will create the EndpointConfiguration and Endpoint in one call. Behavior varies by the `Model` class used:

* Framework-specific model classes (e.g., `sagemaker.xgboost.XGBoostModel`, `sagemaker.sklearn.SKLearnModel`, `sagemaker.pytorch.PyTorchModel`, `sagemaker.tensorflow.TensorFlowModel`) — `model.deploy(...)` returns a `Predictor` instance.
* The base `sagemaker.model.Model` class — `model.deploy(...)` returns `None`; you must instantiate a `Predictor` and attach it to the created endpoint name.

Quick reference table

| Method                             | Use case                                       | Returns                                                    |
| ---------------------------------- | ---------------------------------------------- | ---------------------------------------------------------- |
| `boto3` + `sagemaker-runtime`      | Low-level control / direct invocation          | Raw response stream; you decode bytes                      |
| `sagemaker.model.*.Model.deploy()` | Quick deployment for framework-specific models | `Predictor` (if framework-specific) or `None` (base Model) |
| `sagemaker.predictor.Predictor`    | Explicit client for requests                   | `predict()` returns bytes or str (decode if bytes)         |

Example that handles both deploy return cases:

```python theme={null}
# Using the SageMaker SDK to deploy and call an endpoint
from sagemaker.predictor import Predictor

# Deploy the model (creates endpoint config + endpoint)
# If 'model' is framework-specific, this returns a Predictor; otherwise returns None.
predictor_return = model.deploy(
    initial_instance_count=1,
    instance_type='ml.m5.large',
    endpoint_name='my-endpoint-using-sagemaker-sdk'
)

print(f"Return type from model.deploy(): {type(predictor_return)}")

# If deploy returned None (base Model class), create a Predictor manually:
predictor = predictor_return
if predictor is None:
    predictor = Predictor(endpoint_name='my-endpoint-using-sagemaker-sdk')

print(f"Predictor type: {type(predictor)}")

# Set content type as required by the model
predictor.content_type = 'text/csv'

# Reuse the same input_data from the boto3 example
response = predictor.predict(input_data)

# predictor.predict may return bytes; decode if necessary
if isinstance(response, (bytes, bytearray)):
    response_text = response.decode('utf-8')
else:
    response_text = response

print(f"Prediction result: {response_text}")
```

Example console output:

```text theme={null}
Return type from model.deploy(): <class 'NoneType'>
Predictor type: <class 'sagemaker.base_predictor.Predictor'>
Prediction result: b'{"predictions": [{"score": 1789161.25}]}'
```

If the SDK returns bytes, decode as shown to parse it as JSON and extract the numeric score.

## Visual confirmation in the SageMaker console

Once your SDK-created endpoint starts provisioning, check the SageMaker console to confirm status. The screenshot below shows one endpoint InService and another Creating while the SDK-created endpoint is provisioning.

<Frame>
  <img alt="A screenshot of the Amazon SageMaker &#x22;Endpoints&#x22; console showing two endpoints named &#x22;my-endpoint-using-boto3&#x22; and &#x22;my-endpoint-using-sagemaker-sdk.&#x22; The first endpoint is marked InService and the second is marked Creating, with a large mouse pointer visible." />
</Frame>

Inspecting the endpoint configuration created by the SDK reveals the production variant using your model and the selected instance type (for example, `ml.m5.large`).

<Frame>
  <img alt="Screenshot of the Amazon SageMaker console showing an endpoint configuration for &#x22;my-endpoint-using-sagemaker-sdk.&#x22; It shows a Production variant hosting the model &#x22;house-prices-inference-demo&#x22; on an ml.m5.large instance and data capture set to No." />
</Frame>

## Cleanup — remove endpoints and endpoint configurations

Running endpoints incurs charges. Use the snippet below to enumerate endpoints and delete each endpoint and its EndpointConfiguration. Confirm you want to remove these resources in the current AWS account/region before running it.

<Callout icon="warning">
  Deleting an endpoint is asynchronous. After calling `delete_endpoint`, the endpoint transitions to Deleting and may take time to reach Deleted. If you attempt to delete the endpoint configuration while the endpoint is still deleting, `delete_endpoint_config` may fail because the configuration is still in use. Poll `describe_endpoint` (or use a waiter) and wait for the endpoint to reach a terminal Deleted state before deleting the endpoint configuration.
</Callout>

```python theme={null}
# Cleanup endpoints and their configurations
endpoints = sagemaker_client.list_endpoints(MaxResults=100)['Endpoints']

for ep in endpoints:
    endpoint_name = ep['EndpointName']
    print(f"Deleting endpoint: {endpoint_name}")

    # Get the endpoint config name
    endpoint_desc = sagemaker_client.describe_endpoint(EndpointName=endpoint_name)
    endpoint_config_name = endpoint_desc['EndpointConfigName']

    # Delete endpoint
    sagemaker_client.delete_endpoint(EndpointName=endpoint_name)

    # Delete endpoint config
    print(f"Deleting endpoint config: {endpoint_config_name}")
    sagemaker_client.delete_endpoint_config(EndpointConfigName=endpoint_config_name)

print("Cleanup complete.")
```

Example console output:

```text theme={null}
Deleting endpoint: my-endpoint-using-sagemaker-sdk
Deleting endpoint config: my-endpoint-using-sagemaker-sdk
Deleting endpoint: my-endpoint-using-boto3
Deleting endpoint config: my-endpoint-config-using-boto3
Cleanup complete.
```

## Summary

* Use the SageMaker Runtime client (`boto3.client('sagemaker-runtime')`) to invoke real-time endpoints with `invoke_endpoint(...)`.
* The SageMaker Python SDK (`Model.deploy(...)`) simplifies endpoint creation by creating both the EndpointConfiguration and Endpoint in one step.
* If you deployed with a framework-specific `Model` class, `deploy()` returns a `Predictor`. If you used the base `Model` class, `deploy()` returns `None` and you must construct a `Predictor` bound to the endpoint name before calling `predict`.
* Always delete endpoints and endpoint configurations after demos or tests to avoid ongoing charges.

## Links and references

* [Amazon SageMaker documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* [SageMaker Runtime API — invoke-endpoint](https://docs.aws.amazon.com/sagemaker/latest/dg/API_runtime_InvokeEndpoint.html)
* [SageMaker Python SDK — Predictor class](https://sagemaker.readthedocs.io/en/stable/predictors.html)

A lab exercise is available that walks through creating SageMaker endpoints hands-on.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/772ec99e-54ee-4f4f-8b2a-08b5bc4d4a32/lesson/2975caaf-6a71-4230-9a96-49c80595eaac" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/772ec99e-54ee-4f4f-8b2a-08b5bc4d4a32/lesson/f2c12563-97a5-4f50-b4c5-922ad3dae76d" />
</CardGroup>


# Demo Deploy a Hosted Model Using SageMaker Endpoints

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-MLOps-Engineer/Demo-Deploy-a-Hosted-Model-Using-SageMaker-Endpoints/page

Tutorial for deploying a trained model to Amazon SageMaker by registering model packages, creating endpoint configurations and endpoints, and invoking predictions using Boto3 and the SageMaker Python SDK

In this lesson we'll deploy a trained model to Amazon SageMaker by creating SageMaker model packages, endpoint configurations, and endpoints. The walkthrough shows how to perform the steps from SageMaker Studio (Jupyter notebook) and how to programmatically create and test endpoints using the Boto3 SDK and the SageMaker Python SDK.

Objectives

1. Build a SageMaker model package that associates a model artifact (model.tar.gz) with a container image.
2. Create an endpoint configuration and endpoint using the Boto3 SDK.
3. Create and test an endpoint using the SageMaker SDK and compare using the Predictor / runtime invocation.

<Frame>
  <img alt="A presentation slide titled &#x22;Demo Steps&#x22; listing three numbered steps: confirm the model package is available, run a Jupyter notebook with boto3 to create and test SageMaker endpoint config/endpoints, and run a notebook with the SageMaker SDK to create and test an endpoint using the Predictor class. The slide has a dark background with teal accent bars and a copyright notice for KodeKloud." />
</Frame>

We run the demonstration from a Jupyter notebook inside SageMaker Studio. Open your Studio environment, create or open a notebook, and run the cells in order.

<Frame>
  <img alt="A screenshot of a JupyterLab/SageMaker workspace launcher showing notebook, console, and other file types (Python, Glue, Spark) as clickable tiles. The left pane shows a file browser with folders and notebooks for a &#x22;sagemaker-demystified&#x22; project." />
</Frame>

Step-by-step code (consolidated and corrected)

* The following code is intended to run in Jupyter Notebook cells in SageMaker Studio.
* It covers: imports, uploading a local model artifact to S3, fetching the correct container image URI, registering the model (model package), creating an endpoint configuration with Boto3, creating the endpoint, waiting for it to become InService, and invoking the endpoint.

```python theme={null}
