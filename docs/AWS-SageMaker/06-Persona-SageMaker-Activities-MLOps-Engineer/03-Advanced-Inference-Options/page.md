# Advanced Inference Options

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-MLOps-Engineer/Advanced-Inference-Options/page

Explains SageMaker advanced inference options, focusing on Batch Transform for cost-effective offline, periodic, and high-throughput predictions, including workload distribution, transient instances, and mini-batching.

In this lesson we cover advanced inference strategies available in Amazon SageMaker for scenarios where a continuously running real-time endpoint is not the best fit. We’ll explain when to use batch (offline) inference, how SageMaker Feature Store and Inference Pipelines fit into the flow, and how these options can lower cost and improve efficiency compared to a 24/7 endpoint.

Topics covered:

* Batch inference with SageMaker Batch Transform
* How Batch Transform distributes work and uses transient compute
* Mini-batching behavior inside instances
* When to choose batch vs. real-time inference

Problem: inference might not be real time
If you collect data over a time window and want to predict on the accumulated dataset, you don’t need an always-on SageMaker Endpoint. Running an endpoint 24/7 while waiting to collect data is often inefficient and costly.

<Frame>
  <img alt="A slide comparing two inference workflows: the left shows batch prediction (incoming data → batch inference → batch predictions) and the right shows real-time prediction (incoming data → SageMaker Endpoint → instant prediction). The slide is titled &#x22;Problem 1: Inference Might Not Be in Real Time&#x22; and asks &#x22;Do we need SageMaker Endpoint?&#x22;" />
</Frame>

When to use Batch Transform vs. a real-time endpoint

| Resource Type                  | Best for                                            | Typical pattern                                          |
| ------------------------------ | --------------------------------------------------- | -------------------------------------------------------- |
| SageMaker Batch Transform      | Offline or periodic predictions on accumulated data | Store inputs in S3 → run batch job → write outputs to S3 |
| SageMaker Endpoint (real-time) | Low-latency, per-request inference                  | Continuous endpoint serving real-time requests           |

SageMaker Batch Transform (offline / periodic inference)
SageMaker Batch Transform is a managed service for non-real-time inference. Provide input files in Amazon S3 and a pre-registered SageMaker model; Batch Transform launches managed compute instances, runs inference on the input, writes outputs back to S3, and then shuts down those instances. This avoids the cost of a continuously running endpoint by using transient compute only when needed.

Key benefits:

* Cost-effective for periodic or bulk prediction jobs
* Managed lifecycle: instances spin up to run the job and terminate after completion
* Supports parallelism across instances when you provide multiple input files
* Mini-batching within an instance improves throughput for models that accept batched input

<Frame>
  <img alt="A diagram titled &#x22;Solution 1: Batch Inference&#x22; showing S3 input data flowing into a Batch Transform Agent that runs a container hosting a model. The processed output is saved back to S3, with a transformer-managed instance that spins up for processing and stops." />
</Frame>

Example: Start a Batch Transform job with the SageMaker Python SDK
Replace the placeholders below with your model name and S3 paths. The Transformer object references a SageMaker model you have already created or registered.

```python theme={null}
import sagemaker
from sagemaker.transformer import Transformer
