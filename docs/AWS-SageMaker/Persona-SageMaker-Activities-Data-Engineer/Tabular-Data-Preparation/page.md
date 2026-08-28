# python
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput
import sagemaker

# Initialize session and role (works in SageMaker notebook environment)
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

# Define input/output S3 locations
input_s3_uri = "s3://your-bucket/raw-data/source.csv"
output_s3_uri = "s3://your-bucket/processed-data/"

# Small example processing script: read CSV, sample 70%, scale numeric columns, write CSV
processing_script = """
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

input_dir = "/opt/ml/processing/input"
output_dir = "/opt/ml/processing/output"

os.makedirs(output_dir, exist_ok=True)
df = pd.read_csv(os.path.join(input_dir, "source.csv"))

# Random sample 70% for training
df_sample = df.sample(frac=0.7, random_state=42)

# Apply StandardScaler to numeric columns
num_cols = df_sample.select_dtypes(include=['int64', 'float64']).columns
scaler = StandardScaler()
df_sample[num_cols] = scaler.fit_transform(df_sample[num_cols])

# Write processed CSV
df_sample.to_csv(os.path.join(output_dir, "processed.csv"), index=False)
"""

# Save the script locally
with open("processing_script.py", "w") as f:
    f.write(processing_script)

# Create an SKLearnProcessor
sklearn_processor = SKLearnProcessor(
    framework_version="1.2-1",    # adjust to available SDK/framework versions
    instance_type="ml.m5.large",
    instance_count=1,
    role=role,
    sagemaker_session=sagemaker_session
)

# Run the processing job
sklearn_processor.run(
    code="processing_script.py",
    inputs=[ProcessingInput(source=input_s3_uri, destination="/opt/ml/processing/input/")],
    outputs=[ProcessingOutput(source="/opt/ml/processing/output/", destination=output_s3_uri)]
)

print("SKLearn processing job submitted.")
```

Key notes:

* The script runs inside the managed container on the provisioned instance.
* Processing containers expect input/output under /opt/ml/processing/input and /opt/ml/processing/output.
* SKLearnProcessor chooses a managed scikit-learn image that matches the framework\_version.

## Processor classes — when to use each

The SageMaker SDK exposes processor classes that map to common use cases. This table helps choose the right processor:

| Processor class     | Use case                                                           | Example                                          |
| ------------------- | ------------------------------------------------------------------ | ------------------------------------------------ |
| SKLearnProcessor    | Tabular preprocessing, feature engineering, scaling, imputation    | Use for pandas + scikit-learn transforms         |
| PySparkProcessor    | Large-scale distributed ETL using Spark                            | Multi-node transformations, aggregations, joins  |
| PyTorchProcessor    | GPU-accelerated preprocessing for images or model-based transforms | Image feature extraction with pretrained models  |
| TensorFlowProcessor | TensorFlow-based preprocessing or GPU tasks                        | Text sequence transforms or TF-based feature ops |
| ScriptProcessor     | Custom dependencies or runtime — provide an ECR image              | Bring-your-own Docker image for specialized libs |

<Frame>
  <img alt="A slide titled &#x22;Workflow: Frameworks&#x22; showing a table that maps SDK classes to their best use cases, key features, and example use cases. Rows list SKLearnProcessor, PySparkProcessor, PyTorchProcessor, TensorFlowProcessor, and ScriptProcessor with short descriptions." />
</Frame>

### ScriptProcessor (custom container) example

Use ScriptProcessor when you require a custom image in ECR.

```python theme={null}
# python
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
import sagemaker

sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

input_s3_uri = "s3://your-bucket/raw-data/"
output_s3_uri = "s3://your-bucket/processed-data/"

# Custom ECR container URI (replace with your account and region)
custom_container_uri = "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-processing-container:latest"

script_processor = ScriptProcessor(
    image_uri=custom_container_uri,
    instance_type="ml.m5.large",
    instance_count=1,
    role=role,
    sagemaker_session=sagemaker_session
)

script_processor.run(
    code="processing_script.py",  # your script that expects /opt/ml/processing input/output paths
    inputs=[ProcessingInput(source=input_s3_uri, destination="/opt/ml/processing/input/")],
    outputs=[ProcessingOutput(source="/opt/ml/processing/output/", destination=output_s3_uri)]
)

print("Custom container processing job submitted!")
```

<Callout icon="warning">
  When using ScriptProcessor with a custom ECR image, ensure the execution role has permission to pull from ECR and that the image is compatible with SageMaker's processing lifecycle. Also review instance costs for large or GPU-powered instances.
</Callout>

### PyTorch processor (GPU) example

Use for GPU-accelerated preprocessing like image feature extraction:

```python theme={null}
# python
from sagemaker.pytorch.processing import PyTorchProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput
import sagemaker

sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

input_s3_uri = "s3://your-bucket/images/"
output_s3_uri = "s3://your-bucket/image-features/"

pytorch_processor = PyTorchProcessor(
    framework_version="2.0.0",
    py_version="py310",
    instance_type="ml.g4dn.xlarge",  # GPU instance for fast processing
    instance_count=1,
    role=role,
    sagemaker_session=sagemaker_session
)

pytorch_processor.run(
    code="processing_pytorch.py",
    inputs=[ProcessingInput(source=input_s3_uri, destination="/opt/ml/processing/input/")],
    outputs=[ProcessingOutput(source="/opt/ml/processing/output/", destination=output_s3_uri)]
)

print("PyTorch processing job submitted!")
```

### PySpark processor (multi-node) example

Use for distributed ETL and scale-out across nodes:

```python theme={null}
# python
from sagemaker.spark.processing import PySparkProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput
import sagemaker

sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

input_s3_uri = "s3://your-bucket/raw-data/"
output_s3_uri = "s3://your-bucket/processed-data/"

spark_processor = PySparkProcessor(
    base_job_name="spark-processing-job",
    framework_version="3.3",
    instance_count=2,           # leverage multiple instances for distributed processing
    instance_type="ml.m5.xlarge",
    role=role,
    sagemaker_session=sagemaker_session
)

# Ensure you have a processing_pyspark.py that Spark can submit
spark_processor.run(
    submit_app="processing_pyspark.py",
    inputs=[ProcessingInput(source=input_s3_uri, destination="/opt/ml/processing/input/")],
    outputs=[ProcessingOutput(source="/opt/ml/processing/output/", destination=output_s3_uri)]
)

print("PySpark processing job submitted!")
```

## Monitoring processing jobs

You can monitor jobs in the AWS Console (SageMaker > Processing) to view job status, container image, role, entry point script, timestamps, and logs. Logs are available via CloudWatch — streaming them during runs is helpful for debugging.

<Callout icon="lightbulb">
  You can stream processing job logs via [CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html). Open the Processing job details in the console to find the CloudWatch log group and observe real-time output for troubleshooting.
</Callout>

Example console output you may see for a job:

```text theme={null}
sagemaker-scikit-learn-2025-02-05-17-44-36-577
arn:aws:sagemaker:eu-central-1:485186561655:processing-job/sagemaker-scikit-learn-2025-02-05-17-44-36-577
arn:aws:iam::485186561655:role/service-role/AmazonSageMaker-ExecutionRole-20241216T134619
492215442770.dkr.ecr.eu-central-1.amazonaws.com/sagemaker-scikit-learn:1.2-1-cpu-py3
ml.m5.large
python3
/opt/ml/processing/input/code/processing_script.py
Status: InProgress
```

<Frame>
  <img alt="A presentation slide titled &#x22;SageMaker Data Processing Jobs — Results&#x22; showing four numbered benefit panels. They list: faster preprocessing with scalable infrastructure; lower costs by using the right compute per task; more maintainable workflows by decoupling compute; and improved reproducibility with versioned and logged preprocessing." />
</Frame>

## Benefits recap

* Faster preprocessing using scalable, dedicated compute
* Lower operational cost by right-sizing compute for each task
* More maintainable workflows by decoupling preprocessing from interactive sessions
* Improved reproducibility via versioned scripts, container images, and logged runs

Key takeaways:

* Use processing jobs to delegate heavy preprocessing to managed containers and appropriately sized compute.
* Choose SKLearn/PySpark/PyTorch/TensorFlow processors for common frameworks; choose ScriptProcessor when you need a custom container.
* Scale out using PySparkProcessor (instance\_count > 1) for distributed workloads.
* Inside containers use /opt/ml/processing/input and /opt/ml/processing/output; inputs and outputs are typically S3 URIs.
* Monitor jobs in SageMaker console and CloudWatch for auditing and debugging.
* Modular, version-controlled preprocessing improves reproducibility across teams.

## Links and references

* [SageMaker processing jobs documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/processing-job.html)
* [SageMaker Python SDK documentation](https://sagemaker.readthedocs.io/en/stable/)
* [Amazon S3](https://aws.amazon.com/s3/)
* [AWS CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)

Next steps
A hands-on lab walks through creating and running SageMaker data processing jobs end-to-end.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/dc8df298-eaee-4f8a-b1d0-0ec66f9c6d20/lesson/c629a8d9-604f-4eea-b024-281ae8531a63" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/dc8df298-eaee-4f8a-b1d0-0ec66f9c6d20/lesson/c76f4f3c-7c00-4f80-8679-73c7c44e3fc9" />
</CardGroup>


# Tabular Data Preparation

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-Data-Engineer/Tabular-Data-Preparation/page

Guidelines and Python examples for cleaning and preparing tabular data for machine learning including missing value handling, categorical encoding, scaling, outlier treatment, and processing environments

This lesson is the first that frames data work from the perspective of a persona — typically a data engineer or data scientist. We cover the essential, repeatable steps that make tabular datasets usable for training machine learning models. A small amount of careful preparation often produces much better model performance than training directly on raw data.

In this lesson we will examine common checks and transforms, and provide concrete Python examples using pandas and scikit-learn (sklearn). Topics include:

* Handling missing values (drop vs. impute).
* Removing duplicate rows and redundant columns.
* Enforcing consistency of feature names and data formats.
* Detecting outliers and applying appropriate scaling.
* Sampling strategies for very large datasets.

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Problem: Data Needs Preparation&#x22; showing a &#x22;Data Cleanup&#x22; icon on the left and a numbered checklist on the right. The checklist asks: &#x22;Missing values?&#x22;, &#x22;Duplicate rows?&#x22;, &#x22;Redundant columns?&#x22;, and &#x22;Too much data?&#x22;." />
</Frame>

## Consistency checks

Before heavy EDA or modeling, look for inconsistent formatting or naming that will cause bugs or misleading statistics:

* Are categorical values consistent? (e.g., "suburban" vs "Suburb" vs "Suburban ")
* Are date formats uniform (MM/DD/YYYY, DD/MM/YYYY, ISO 8601)?
* Are numeric columns stored as numeric dtypes rather than strings?

Fixing these early prevents surprises downstream and simplifies feature engineering.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Data Needs Preparation&#x22; with a &#x22;Consistency Check&#x22; badge on the left. On the right are three checklist questions: &#x22;Uniform feature naming?&#x22;, &#x22;Date format consistency?&#x22;, and &#x22;Numeric values stored correctly?&#x22;." />
</Frame>

## Outliers and scaling

Outliers can skew summary statistics (mean, variance) and harm models that rely on gradient or distance calculations. Also watch for features on very different scales — e.g., square footage (hundreds to thousands) vs. number of bedrooms (1–10) — which normally need scaling for many algorithms.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Data Needs Preparation&#x22; highlighting &#x22;Outliers and Scaling&#x22; with a chart icon. It lists two points: &#x22;Handle extreme values?&#x22; and &#x22;Standardize numerical ranges?&#x22;." />
</Frame>

## Solution: Missing data

Missing values reduce the model’s ability to learn from the full dataset. Typical choices:

* Drop rows or columns with missing values (lossy).
* Impute (fill) missing values with reasonable estimates (preserves rows).

We commonly use pandas for manipulation and scikit-learn for imputation utilities. Examples below show both dropping and imputing.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Missing Data&#x22; showing two options—1) drop rows/columns and 2) impute missing data—plus a recommendation to use SageMaker JupyterLab with pandas for dropping and imputing." />
</Frame>

### Dropping rows or columns with pandas

Use dropna when you prefer to remove missing data entirely (be mindful of how much data is lost).

```python theme={null}
import pandas as pd
