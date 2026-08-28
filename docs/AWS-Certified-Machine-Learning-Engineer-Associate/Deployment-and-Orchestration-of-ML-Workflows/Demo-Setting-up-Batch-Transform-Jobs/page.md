# Replace the payload with your model's expected input format
payload = json.dumps({"instances": [[1.0, 2.0, 3.0]]})

response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType="application/json",
    Body=payload
)

result = response["Body"].read().decode("utf-8")
print(result)
```

Operational best practices and tips

* Monitor endpoint metrics (latency, invocation count, error rate) in CloudWatch to detect regressions and to drive autoscaling or variant adjustments.
* Implement structured logging and content validation (request/response schema checks) to avoid corrupt data reaching models.
* Use model shadowing for safe evaluation of new model versions: route a small percentage of live traffic to the shadow variant and compare metrics before full rollout.
* For GPU workloads or strict latency SLAs, prefer provisioned hosting with appropriate instance types and consider autoscaling policies.
* Track costs: provisioned endpoints incur instance-hour charges even when idle — serverless endpoints can reduce idle cost but may have different performance profiles.

<Callout icon="warning">
  Provisioned endpoints incur ongoing instance costs. Ensure you choose instance sizes and scaling policies that match your throughput and latency requirements to avoid unnecessary spend.
</Callout>

Troubleshooting checklist

* Endpoint stuck in creating: check IAM permissions, VPC configuration (if using VPC endpoints), and service limits (quota on instance types).
* Invocation errors: validate ContentType, payload format, and model input schema.
* High latency: review instance family and size, enable provisioned concurrency or add instances, and profile model performance.

Summary
This lesson covered how to take a model from SageMaker Studio or JumpStart and expose it as a real-time endpoint. We reviewed:

* Preparing and registering models
* Choosing between serverless and provisioned hosting
* Configuring encryption and KMS keys
* Using model variants for safe deployments (blue-green / canary)
* Invoking endpoints with the AWS SDK

Links and references

* SageMaker Studio and Endpoints: [https://learn.kodekloud.com/user/courses/aws-sagemaker](https://learn.kodekloud.com/user/courses/aws-sagemaker)
* boto3 documentation: [https://boto3.amazonaws.com/v1/documentation/api/latest/index.html](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
* AWS CLI: [https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
* CloudWatch monitoring: [https://learn.kodekloud.com/user/courses/aws-cloudwatch](https://learn.kodekloud.com/user/courses/aws-cloudwatch)

For next steps, try deploying a small model as a serverless endpoint, monitor its metrics in CloudWatch, then experiment with a shadow variant to test a model update with live traffic.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/0801c849-dbe1-46e9-9f00-138951f185e6" />
</CardGroup>


# Demo Setting up Batch Transform Jobs

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Deployment-and-Orchestration-of-ML-Workflows/Demo-Setting-up-Batch-Transform-Jobs/page

Tutorial for configuring and launching Amazon SageMaker Batch Transform jobs to run offline inference on S3 datasets, covering instance choices, input and output setup, monitoring, and cost optimization.

In this lesson we’ll walk through creating a Batch Transform job in Amazon SageMaker to run offline inference on a dataset stored in Amazon S3. Batch Transform is ideal when you already have a trained model and need to score many records at once (for example, a CSV with thousands of rows). Follow the numbered steps below to create, configure, and monitor a Batch Transform job.

<Frame>
  <img alt="The image shows the Amazon SageMaker AI console page, highlighting its features for building, training, and deploying machine learning models at scale. The sidebar includes options for model training, deployment, and data preparation." />
</Frame>

1. Choose the model and instance type

* Select the model you previously created in SageMaker. This model will be hosted by the transform job for batch inference.
* Choose an instance type that balances throughput and cost. Instance selection has a direct impact on job runtime and hourly cost.
* If your model needs GPU acceleration, select a GPU instance family (for example, `ml.g4dn.*` or `ml.p3.*`). For CPU inference, pick an `ml.m5.*` or similar instance.

Recommended instance choices and typical use cases:

| Instance family               | Use case                                                         |
| ----------------------------- | ---------------------------------------------------------------- |
| `ml.m5.large`, `ml.m5.xlarge` | CPU-based models, low to medium throughput                       |
| `ml.c5.*`                     | Compute-optimized CPU workloads                                  |
| `ml.g4dn.*`                   | GPU inference for computer vision or large deep learning models  |
| `ml.p3.*`                     | High-performance GPU for heavy-weight models or high concurrency |

<Frame>
  <img alt="This image shows a dropdown menu in the AWS SageMaker console for selecting instance types. Various instance options like &#x22;ml.m5.large&#x22; and &#x22;ml.m5.xlarge&#x22; are visible." />
</Frame>

<Callout icon="lightbulb">
  Instance sizing example: `ml.m5.xlarge` provides 4 vCPUs and 16 GiB memory, while `ml.m5.large` provides 2 vCPUs and 8 GiB memory. Pricing varies by region; always confirm current costs on the [SageMaker pricing page](https://aws.amazon.com/sagemaker/pricing/) before launching jobs.
</Callout>

2. Review instance specifications and pricing

* Verify vCPU, memory, and estimated hourly price for the instance class you selected.
* Choose the smallest instance or smallest cluster of instances that meets your performance goals to reduce costs.
* Consider parallelism: using multiple instances or larger instances may finish jobs faster but can increase total cost if not optimized.

<Frame>
  <img alt="The image shows a web page from Amazon SageMaker's pricing section displaying various instance types, their specifications in terms of vCPUs and memory (GiB), and corresponding hourly prices." />
</Frame>

3. Configure input data (S3)

* Batch Transform reads input objects from S3. Configure the following fields:
  * S3 input URI: the S3 path or prefix containing your input files (for example, `s3://your-bucket/raw-data/titanic.csv`).
  * Split type: determines how SageMaker splits input files into invocation payloads. Use `Line` for typical CSVs where each line is one record; use `None` if the model expects the entire file as a single payload.
  * Compression: set to `None` unless your files are compressed.
  * Content type: set to `text/csv`, `application/jsonlines`, etc., to match your model input formatter.
* Example: if your Titanic dataset is in S3, copy the input URI such as `s3://.../raw-data/titanic.csv` and paste it into the input location field.

Best practices:

* Use one record per line (`Line`) for large CSVs so records are processed independently.
* Partition large datasets into multiple objects to allow parallel processing by multiple instances.

<Frame>
  <img alt="The image shows the Amazon S3 web interface with a bucket named &#x22;raw-data&#x22; containing two objects: &#x22;titanic.csv&#x22; and a folder named &#x22;titanic/&#x22;." />
</Frame>

4. Configure output location

* Set an S3 output prefix where Batch Transform writes predictions (for example, `s3://your-bucket/predictions/` or `s3://your-bucket/processed/`).
* Use separate prefixes for intermediate/processed output and final predictions to keep raw and derived data organized.

5. Additional configuration options

* Accept header: request a particular response content type for output (for example, `application/jsonlines`).
* Logging & buckets: optionally specify alternate buckets or prefixes for logs and job outputs.
* Input/Output filters and JoinSource:
  * Use input/output filters when you need to transform or filter record fields before sending to the model or after receiving predictions.
  * Use `JoinSource` to include input record fields alongside the model’s prediction in the final output if you want joined results.
* If your data is already clean and self-contained, these optional settings can usually be left unset.

<Frame>
  <img alt="The image is a screenshot of the AWS SageMaker console showing a form for creating a batch transform job, including options for configuration and environment variables." />
</Frame>

6. Launch and monitor

* After selecting the model, instance type, and input/output paths and configuring optional settings, create the Batch Transform job.
* Monitor job status from the SageMaker console under Inference → Batch transform jobs.
* When the job completes, download and inspect the output files in the S3 output prefix you provided.

Monitoring tips:

* Check the job status and logs in the SageMaker console.
* Use Amazon CloudWatch for detailed logs and metrics (invocations, errors, instance utilization).
* If results look incorrect, inspect the content-type, split type, and any input filters to ensure inputs match model expectations.

<Callout icon="warning">
  Be mindful of cost: long-running or large Batch Transform jobs can incur significant charges. Terminate or delete any resources (models, endpoints, or unused S3 objects) you no longer need to avoid ongoing costs.
</Callout>

Checklist before launching

| Step            | Verify                                                                       |
| --------------- | ---------------------------------------------------------------------------- |
| Model readiness | Model artifact and container image are registered in SageMaker               |
| Input format    | S3 files, `Content-Type`, and `SplitType` match the model's expected payload |
| Instance sizing | Selected instance type provides required CPU/GPU and memory                  |
| Output path     | S3 output prefix exists and has correct permissions                          |
| Logging         | CloudWatch or S3 logging configured if you need audit/troubleshooting info   |

Further reading and references

* [Amazon SageMaker Batch Transform](https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html)
* [Amazon SageMaker Pricing](https://aws.amazon.com/sagemaker/pricing/)
* [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/index.html)

That’s it — you’ve configured and launched a Batch Transform job in SageMaker. Monitor the job, inspect the outputs in S3, and optimize instance sizing or input partitioning as needed to balance cost and throughput.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/e14f74a9-cd62-49ca-b511-f534c1fb4137" />
</CardGroup>
