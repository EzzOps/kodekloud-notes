# Initialize SageMaker session
sagemaker_session = sagemaker.Session()

# Replace with your existing SageMaker model name
model_name = "your-trained-model"

# S3 input and output locations (replace with your bucket/paths)
input_s3_path = "s3://your-bucket/input-data/"
output_s3_path = "s3://your-bucket/output-data/"

# Create a Transformer object (this does NOT start the job yet)
transformer = Transformer(
    model_name=model_name,
    instance_count=1,
    instance_type="ml.m5.large",      # Choose an appropriate instance type
    output_path=output_s3_path,
    accept="application/json",         # What the container will return
)

# Start the Batch Transform job
transformer.transform(
    data=input_s3_path,
    content_type="text/csv",  # e.g., "text/csv" or "application/json"
    split_type="Line",        # how to split input files for processing
    # Optional parameters for filtering/formatting:
    # input_filter="$[0:2]",    # optional: select fields from input (depends on your model/container)
    # output_filter="$[2:]",    # optional: select fields from output
    # join_source="Input",      # optional: include original input in the output
)

# Wait for completion (optional - blocks until job finishes)
transformer.wait()
print(f"Batch Transform job completed! Results at {output_s3_path}")
```

> **lightbulb** Replace placeholders like model\_name and S3 paths with your own values. Ensure the model container supports the specified content\_type / accept values and can process batched input if you enable mini-batching. See the SageMaker Batch Transform docs for available parameters.\
  (Reference: [https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html](https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html))

Notes about the example

* The Transformer object configures the job; calling transform() actually starts it.
* SageMaker launches the specified instance\_count of identical instances, distributes input files across them, and terminates instances after processing.
* Use transformer.wait() to block until the job completes and results are written to S3.

How Batch Transform distributes work
When you request multiple instances, SageMaker distributes whole input files across instances (parallel file-level distribution). For example, if you supply two CSV files and request two instances, each instance will typically process one file. If you provide a single large file, SageMaker will not split that file across instances by default; instead, one instance will process it. To achieve parallelism you can:

* Provide multiple input files in your S3 prefix, or
* Pre-split large files into smaller chunks that can be distributed across instances.

<Frame>
  <img alt="A slide titled &#x22;Workload Distribution in Batch Transform&#x22; showing a flowchart where a Start Batch Job launches multiple instances (Instance 1, Instance 2) and each instance processes a different file (input1.csv, input2.csv). The left side notes explain SageMaker starts compute instances and that one file uses only one instance." />
</Frame>

Temporary (transient) instances
Batch Transform does not create a permanent SageMaker endpoint. Instances are launched for the duration of the batch job and terminated when processing completes, so you only pay for the compute time that you actually use.

<Frame>
  <img alt="A slide titled &#x22;Temporary Instances&#x22; that lists benefits (no permanent SageMaker endpoint, instances run only for processing, and shut down automatically). To the right is a flowchart showing a batch job starting parallel instances that do processing, complete the job, and then shut down." />
</Frame>

Mini-batching inside a single instance
Within a single instance, Batch Transform can further split large input files into smaller "mini-batches" that are sent to the model container sequentially. This reduces memory pressure, improves caching, and increases throughput compared to sending a single huge request.

You can control batching behavior using transform parameters and container logic. If your model requires one-record-per-invocation, disable mini-batching; otherwise, enable mini-batching to improve performance for models that support batched input.

<Frame>
  <img alt="A presentation slide titled &#x22;S3 Input Processing in Mini-Batches&#x22; with three bullet points about splitting large files into mini-batches, sending them for inference, and optimizing performance. On the right is a flowchart showing S3 input location → splitting into mini-batches → Mini-Batch 1/2/3 → processing." />
</Frame>

Best practices and considerations

* Use Batch Transform for periodic, offline, and high-throughput inference jobs to reduce cost and simplify operations.
* Ensure your model container supports the expected content\_type and batched inputs (or adapt the container).
* For parallelism, provide many input files or pre-split large files—Batch Transform maps files to instances.
* Monitor job logs and output artifacts in S3 to validate results and troubleshoot issues.
* For workflows that need pre- or post-processing steps, consider SageMaker Inference Pipelines (covered in other lessons) or preprocess inputs before invoking Batch Transform.

> **lightbulb** Batch Transform is ideal when predictions can be performed offline or in scheduled batches. It reduces cost by avoiding always-on endpoints and supports parallel processing and mini-batching for efficiency. Always confirm that your model container and input formats are compatible with batched requests before enabling mini-batching.

Links and references

* SageMaker Batch Transform documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html](https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html)
* SageMaker inference overview: [https://docs.aws.amazon.com/sagemaker/latest/dg/inference.html](https://docs.aws.amazon.com/sagemaker/latest/dg/inference.html)
* SageMaker Python SDK: [https://sagemaker.readthedocs.io/](https://sagemaker.readthedocs.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/772ec99e-54ee-4f4f-8b2a-08b5bc4d4a32/lesson/f4644015-b6ff-48f0-9172-a90dc41b230f)


# Automate ML Pipeline with SageMaker Pipeline

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-MLOps-Engineer/Automate-ML-Pipeline-with-SageMaker-Pipeline/page

Describes automating ML workflows with Amazon SageMaker Pipelines, using scripts and the Python SDK for reproducible, scalable pipelines integrated with CI/CD and AWS services

In this lesson we introduce Amazon SageMaker Pipelines — a native SageMaker feature that automates and orchestrates activities across an entire ML pipeline.

What you'll learn:

* Why automation matters for ML workflows
* How SageMaker Pipelines fits into an enterprise deployment lifecycle
* Options for running notebook code inside pipelines (notebooks vs. scripts)
* A concise SDK example showing how to build and run a pipeline

***

## Why automate ML workflows?

Manual notebook-driven experimentation (running cells by hand) is error-prone and difficult to reproduce. Automation provides:

* Reproducibility and lineage: with the same inputs (data version, algorithm version, scripts) you should reproduce the same model artifact.
* Scalability: automation enables large-scale experiments and workloads.
* Integration: pipelines connect natively with AWS services like S3, Lambda, Step Functions, and the SageMaker Model Registry.

Links and references:

* [S3 Overview](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [AWS Lambda Docs](https://learn.kodekloud.com/user/courses/aws-lambda)
* [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
* [SageMaker Model Registry](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html)

<Frame>
  <img alt="A slide titled &#x22;Problem: Manual Release Process&#x22; showing two parallel ML release pipelines with dataset and algorithm versions feeding processing jobs, training jobs, and resulting model artifacts. Script files and their version numbers (e.g., processing_script.py v1.0, training_script.py v1.0/v1.1) are shown under the jobs." />
</Frame>

Typical manual flow:

* Choose a dataset (versioned)
* Pick an algorithm and its version
* Run data processing (scaling, encoding, imputation)
* Run a training job (possibly hyperparameter tuning)
* Store and register model artifacts
* Repeat when code, data, or algorithm versions change

Each component should be versioned to track model lineage and enable reproducibility. However, manually invoking these steps (for example, by running notebook cells) makes consistent, repeatable runs and scale-out difficult.

***

## Solution: SageMaker Pipelines

SageMaker Pipelines lets you declare a sequence of steps and run them deterministically:

* Define processing, training, evaluation, registration, and (optionally) deployment steps.
* Provide inputs such as dataset S3 paths, script locations, algorithm versions, and hyperparameters.
* Execute the pipeline programmatically or via orchestration systems (CI/CD, Step Functions, Airflow).

Benefits include automation, reproducibility, scalability, and native AWS integrations.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: SageMaker Pipelines&#x22; showing four colored icons and headings: Automation, Reproducibility, Scalability, and Integration, each with a short description. The slide highlights benefits like reduced manual effort, consistent workflows, efficient large‑scale processing, and integration with AWS services." />
</Frame>

***

## How pipelines fit into an enterprise lifecycle

* Development: data scientists iterate interactively in notebooks (exploration, prototyping).
* Beta / Pre-production: start productionizing by replacing manual steps with automated pipelines for retraining, evaluation, and model registration in staging.
* Production: approved model versions in the Model Registry are promoted and deployed automatically. The registry approval can trigger a deployment pipeline.

Use separate pipelines for training and deployment for clearer responsibilities: training pipelines produce registered model versions; a deployment pipeline consumes approved versions.

<Frame>
  <img alt="A slide titled &#x22;Solution: SageMaker Pipelines&#x22; showing three colored environment boxes — Development, Beta, and Production — each describing training and deployment approaches. Below is a Model Registry with Model v1/v2/v3 and arrows indicating automated pipelines feeding the registry and an approval step promoting a model to production." />
</Frame>

***

## Why use scripts (not notebooks) as pipeline steps?

Each pipeline step usually maps to a standalone Python script, not an interactive notebook. Scripts are preferred because:

* Deterministic execution (no interactive prompts)
* Easier to add error handling, logging, and retries
* More robust for automation and production debugging
* Better suited for CI/CD and version control

> **lightbulb** Refactoring notebook code into well-defined Python scripts improves maintainability. Use an IDE like SageMaker Studio Code Editor or VS Code for development and debugging before integrating into pipelines.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: SageMaker Pipelines&#x22; about refactoring Jupyter Notebooks to Python scripts. It lists benefits—scalability and repeatability, easier troubleshooting and debugging, a shift to automation and robustness—and notes this is done in SageMaker Studio Code Editor (VSCode)." />
</Frame>

Alternative approaches for using notebook code inside pipelines:

* Run notebooks via processing jobs with papermill (an orchestration workaround that still carries notebook limitations).
* Newer native support: SageMaker Pipelines can run Jupyter notebooks as steps in some regions — convenient but not always available and notebook code commonly lacks production-grade error handling.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: SageMaker Pipelines&#x22; showing item &#x22;02 Processing Jobs as a Workaround&#x22; with two notes: it was used to run Jupyter notebooks via SageMaker Pipelines and allowed orchestration but was a temporary fix. The slide has a dark teal background and a KodeKloud copyright mark." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: SageMaker Pipelines&#x22; highlighting &#x22;03 Native Support for Jupyter Notebooks.&#x22; It notes that SageMaker Pipelines can run Jupyter notebooks directly, but refactoring is still useful for error handling/maintainability and notebooks aren’t always production-ready." />
</Frame>

> **warning** Notebooks can be executed by pipelines in some regions, but they often lack structured error handling and are less portable. For production pipelines, prefer dedicated scripts stored in a Git repository.

***

## Recommended script-to-step mapping

Store scripts in a Git repo and invoke them from pipeline steps. Example mapping:

| Pipeline Step       | Typical Script Filename | Purpose                                     |
| ------------------- | ----------------------- | ------------------------------------------- |
| Data cleaning       | clean.py                | Data validation and cleaning                |
| Feature engineering | feature.py              | Feature transforms and feature store writes |
| Training            | train.py                | Estimator creation and training logic       |
| Evaluation          | evaluation.py           | Model scoring, metrics, and validation      |
| Model registration  | register.py             | Register model in the Model Registry        |
| Deployment          | deploy.py               | Deploy model to an endpoint (optional)      |

<Frame>
  <img alt="A slide titled &#x22;Solution: SageMaker Pipelines&#x22; showing a linear workflow of steps — Clean Data, Feature Engineer, Train, Register, and Deploy — with arrows pointing down. Each step maps to a corresponding Python script (clean.py, feature.py, train.py, register.py, deploy.py) stored in a Git-compatible version repository." />
</Frame>

***

## Creating pipelines: Visual Editor vs. SDK

* Studio Visual Editor: drag-and-drop, low-code, quick visualization. Good for simple pipelines but limited customization and binding arbitrary scripts to arbitrary step types.
* SageMaker Python SDK (recommended): define ProcessingStep, TrainingStep, RegisterModel, etc., in code. This gives full control, versioning in code, parameterization, and reuse.

<Frame>
  <img alt="A screenshot of the SageMaker Pipelines visual UI showing pipeline step types on the left and a workflow diagram in the center. The diagram connects steps labeled &#x22;Train model&#x22;, &#x22;Register model&#x22;, and &#x22;Deploy model (endpoint)&#x22;, with a settings/details pane visible on the right." />
</Frame>

***

## Example: Build a SageMaker Pipeline using the SDK

Below is a concise, complete example that defines a data preprocessing ProcessingStep, a TrainingStep, a model evaluation ProcessingStep, and a RegisterModel step. Finally, these steps are assembled into a Pipeline object and executed.

Assumptions:

* SDK imports, `role`, `pipeline_session`, `bucket`, `input_data`, `train_instance_type`, and `train_instance_count` are already defined and configured.

```python theme={null}
