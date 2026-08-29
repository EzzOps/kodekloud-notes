# Create a SageMaker session (uses local AWS config/credentials)
sagemaker_session = sagemaker.Session()

# Model metadata
model_name = "your-model-name"
model_data = "s3://your-bucket/path/to/model.tar.gz"
role = "arn:aws:iam::your-account-id:role/SageMakerRole"

# Construct the SageMaker Model object (container image must implement the inference contract)
model = sagemaker.Model(
    image_uri="your-container-image-uri",
    model_data=model_data,
    role=role,
    sagemaker_session=sagemaker_session
)

# Serverless settings: memory per invocation and max concurrent requests
serverless_config = ServerlessInferenceConfig(
    memory_size_in_mb=2048,
    max_concurrency=5
)

# Deploy to a serverless endpoint (SageMaker creates the endpoint and underlying infra)
predictor = model.deploy(
    endpoint_name="your-serverless-endpoint-name",
    serverless_inference_config=serverless_config,
    predictor_cls=Predictor
)

print(f"Serverless endpoint deployed: {predictor.endpoint_name}")
```

Key operational notes:

* memory\_size\_in\_mb controls the per-invocation memory allocation; CPU is tied to memory in the serverless execution environment.
* max\_concurrency caps parallel invocations; excess requests may be throttled with HTTP 429 responses.
* You don’t choose instance types or counts — the service abstracts the topology.

Next problem: complex processing during inference

Some real-time systems (for example, fraud detection on credit-card transactions) require significant preprocessing at inference time. Typical challenges include:

* Feature mismatch: training and inference use different feature definitions or derivations.
* Slow data fetching: inference requires queries to multiple databases or external APIs.
* Redundant computation: expensive feature transformations are repeated at inference time even though they could be precomputed.

<Frame>
  <img alt="A slide titled &#x22;Problem 3: Processing in Inference&#x22; showing a fraud detection system that must evaluate real-time transactions. To the right it lists three challenges: feature mismatch, slow data fetching (multiple DBs/APIs), and redundant computation of feature transformations." />
</Frame>

Solution: SageMaker Feature Store

SageMaker Feature Store provides a centralized repository for features used in both training and inference. For real-time detection you typically use the online store (backed by Amazon DynamoDB) to achieve single-digit millisecond lookups at scale. The Feature Store helps you:

* Ensure consistent feature definitions between training and inference.
* Precompute expensive transformations and write them to the store so inference can fetch them quickly.
* Reduce inference latency by retrieving features instead of recomputing them on the critical path.
* Scale feature lookups to production traffic levels.

<Frame>
  <img alt="An infographic titled &#x22;Solution 3: SageMaker Feature Store&#x22; showing five colored panels that list benefits of the feature store. The panels note precomputed online features for faster inference, feature consistency for training and inference, low-latency lookups for real-time detection, scalability to millions of features, and reduced manual effort." />
</Frame>

Feature Store benefits (at a glance)

| Benefit                        | Why it matters                                                  |
| ------------------------------ | --------------------------------------------------------------- |
| Precomputed online features    | Faster inference: lookups are cheaper than recomputations       |
| Training/inference consistency | Same features used for model training and serving reduces drift |
| Low-latency lookups            | Online store (DynamoDB) supports single-digit ms lookups        |
| Scalability                    | Supports many feature groups and high query volume              |
| Centralized workflows          | Simplifies operations & reduces duplicated engineering work     |

How the feature store fits into an inference pipeline

In a fraud-detection example you might maintain two feature groups:

* Batch feature group — weekly aggregates and historical signals computed in batch.
* Online feature group — near-real-time aggregates (e.g., last 10 minutes) written by a streaming processor or Lambda as transactions arrive.

A streaming preprocessor (Kinesis/BK/managed streaming + Lambda or a streaming job) computes incremental features and writes them to the online store. At inference time, the model lookup flow becomes:

1. Receive transaction and identifier (e.g., card or customer ID).
2. Query the online feature store for recent aggregates and signals.
3. Enrich the incoming request with retrieved features.
4. Call the model with the enriched feature vector for a prediction.

This avoids recomputing expensive transformations on the critical path and guarantees that training and inference use the same feature definitions.

<Frame>
  <img alt="A diagram titled &#x22;Solution 3: SageMaker Feature Store&#x22; showing two feature groups (online and batch) feeding a Lambda that produces input features for a model. The model outputs a fraud prediction (is_fraud, 98%)." />
</Frame>

Example pipeline integration

A typical flow that integrates the Feature Store across training and inference:

* Extract historical transactions from the source datastore.
* Derive features and populate:
  * training feature groups (for offline model training),
  * batch aggregates and the online feature store (for runtime lookups).
* Train the model using feature store data (ensures feature parity).
* Serve the model in production and read online features at prediction time.

<Frame>
  <img alt="A diagram titled &#x22;Solution 3: SageMaker Feature Store&#x22; showing a fraud-detection data pipeline: historical transactions are processed into training features (including fraud_label and ratio features) and weekly aggregates, which feed a training job that produces a trained model and populate an online feature store." />
</Frame>

Next steps and resources

This guide introduced serverless inference and how the SageMaker Feature Store can reduce latency and duplication in real-time pipelines. For hands-on examples, sample notebooks, and end-to-end code demonstrating batch ingestion, streaming processing, populating the store, and using the online store during inference, see the AWS Samples repository:

* SageMaker Feature Store examples: [https://github.com/aws/amazon-sagemaker-examples](https://github.com/aws/amazon-sagemaker-examples)

Additional references:

* Amazon SageMaker documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* SageMaker Feature Store docs: [https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html)
* AWS DynamoDB: [https://aws.amazon.com/dynamodb/](https://aws.amazon.com/dynamodb/)

> **lightbulb** Use serverless inference to minimize costs for intermittent, unpredictable real-time workloads. For real-time systems requiring consistent, precomputed features (like fraud detection), use SageMaker Feature Store to centralize feature engineering and reduce inference-time overhead.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/772ec99e-54ee-4f4f-8b2a-08b5bc4d4a32/lesson/b910b5cc-5119-4bb7-b40f-f5ebfe23feb9)


# Advanced Inference Options Part 3

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-MLOps-Engineer/Advanced-Inference-Options-Part-3/page

Explains Amazon SageMaker inference pipelines for chaining preprocessing, model serving, and postprocessing in a single real-time endpoint, including deployment, comparisons, and best practices.

In this lesson we examine a common advanced inference scenario: processing input data around a model. When raw input can't be consumed directly by a model, you need preprocessing (scaling, encoding, feature engineering) before inference — and often post-processing (formatting, thresholding, filtering) after the model returns predictions.

Two core questions arise:

* Where should preprocessing and post-processing run?
* How can you combine those steps into a single inference request?

Amazon SageMaker addresses this with SageMaker Inference Pipelines — a mechanism for chaining multiple containers (preprocess → model → postprocess) so a single real-time inference request flows through them in sequence. Note that a SageMaker inference pipeline is distinct from a SageMaker Pipeline used for training and CI/CD orchestration; the inference pipeline specifically composes multiple containers for one inference request.

> **lightbulb** A SageMaker inference pipeline composes a sequence of containers (preprocessing → model → postprocessing) for one real-time request. It is different from a SageMaker Pipeline used to manage training and orchestration workflows.

## Conceptual flow

A SageMaker real-time endpoint can host multiple containers on the same instance. You define the execution order so each incoming request is passed through the containers in sequence:

1. The endpoint receives the inference request and forwards it to the first container (preprocessing).
2. The preprocessing container transforms the raw input (scaling, encoding, feature generation) and returns transformed data.
3. The transformed data is passed to the model container, which runs inference and emits predictions.
4. The model output is forwarded to the postprocessing container, which formats or filters predictions for the client.

This encapsulates the complete inference path — raw input to client-ready output — inside a single real-time request. SageMaker abstracts data transfer between containers, so you can focus on the data-science workflow without managing low-level container plumbing.

> **lightbulb** SageMaker handles the inter-container data flow. Containers simply accept input and return output; SageMaker wires them together in the order you specify.

## Defining an inference pipeline

You define the pipeline in a JSON file that lists the containers in the sequence you want them to run. When you call deploy() on your model (for example with the SageMaker Python SDK), you provide a reference to that pipeline JSON. Deployment and endpoint configuration are otherwise the same — the pipeline JSON tells SageMaker which containers to invoke and in what order.

Example pipeline definition (JSON):

```json theme={null}
{
  "InferencePipelineModelName": "my-inference-pipeline",
  "ModelContainers": [
    {
      "ModelName": "preprocessing-container",
      "Image": "preprocessing-image-uri",
      "Environment": {
        "PREPROCESSING_PARAMS": "value"
      }
    },
    {
      "ModelName": "model-container",
      "Image": "model-image-uri",
      "Environment": {
        "MODEL_PARAMS": "value"
      }
    },
    {
      "ModelName": "postprocessing-container",
      "Image": "postprocessing-image-uri",
      "Environment": {
        "POSTPROCESSING_PARAMS": "value"
      }
    }
  ]
}
```

Notes:

* The array order in "ModelContainers" defines execution sequence; output from container N becomes the input for container N+1.
* Each container must implement the SageMaker inference contract (process input, produce output).
* You can set container-specific Environment variables to configure behavior (e.g., scaling parameters or model hyperparameters).

## Deployment overview

Typical steps to deploy an inference pipeline:

1. Build container images for preprocessing, model serving, and postprocessing.
2. Upload images to a container registry (ECR).
3. Create a pipeline JSON that references each container image and configuration.
4. Use the SageMaker SDK or API to create the Inference Pipeline Model and deploy a real-time endpoint that uses it.
5. Send inference requests to the endpoint — each request will traverse preprocess → model → postprocess automatically.

## How inference pipelines compare with other SageMaker inference options

Below is a concise comparison to help decide the right option for your workload.

| Option                        | Best for                                                                | Key characteristics                                                                                           |
| ----------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| SageMaker Batch Transform     | Offline, large-scale predictions                                        | No persistent endpoint; spins up compute, processes data, writes outputs, then tears down resources.          |
| Asynchronous Inference        | Large payloads or non-immediate results                                 | Returns acknowledgement; results delivered later (SNS, S3). Payloads up to \~1 GB; backend can scale to zero. |
| Serverless Endpoints          | Real-time with unpredictable/bursty traffic                             | Scales compute on demand; reduces always-on cost; may incur cold-start latency.                               |
| SageMaker Feature Store       | Low-latency feature retrieval for online inference                      | Stores pre-computed features (aggregates) usable by both training and online inference.                       |
| SageMaker Inference Pipelines | Wrapping preprocessing/postprocessing with model for real-time requests | Chains containers in a single real-time request (preprocess → model → postprocess).                           |

Use inference pipelines when you want to encapsulate preprocessing and postprocessing close to the model, keep the inference request flow simple for clients, and avoid introducing a separate preprocessing service or feature store for simple transformations.

## Best practices and considerations

* Keep preprocessing/postprocessing lightweight for low-latency requirements; heavy transformations may increase response times.
* If preprocessing requires heavy computation or shared historical data, consider using a Feature Store or Batch/Asynchronous pipelines instead.
* Monitor and log each container’s behavior to diagnose latency or serialization issues between stages.
* Ensure all containers conform to SageMaker’s expected input/output formats so the pipeline passes data correctly.

## Links and references

* [AWS SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* [SageMaker Feature Store](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html)
* [SageMaker Asynchronous Inference](https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html)
* [SageMaker Batch Transform](https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html)
* [KodeKloud SageMaker course](https://learn.kodekloud.com/user/courses/aws-sagemaker)

This concludes the lesson. In the next article we'll walk through creating a hosted endpoint using SageMaker.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; showing a numbered list of five Amazon SageMaker capabilities. The items are SageMaker Batch Transform, Asynchronous Inference, Serverless Endpoints, Feature Store, and Inference Pipelines for pre-/post-processing." />
</Frame>

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/772ec99e-54ee-4f4f-8b2a-08b5bc4d4a32/lesson/d09941c5-366a-423c-8826-971b2e3a9299)
