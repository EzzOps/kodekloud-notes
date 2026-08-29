# Using SageMaker Script Mode with Frameworks

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/Using-SageMaker-Script-Mode-with-Frameworks/page

Guide to using Amazon SageMaker Script Mode to run existing training scripts in prebuilt framework containers for managed scalable training, experiment tracking, and easy deployment.

Amazon SageMaker Script Mode lets you run your existing training scripts inside SageMaker’s managed environment with minimal changes by using SageMaker’s pre-built framework containers. This approach simplifies migrating from local development to cloud training while leveraging managed infrastructure, scalability, and experiment tracking.

<Frame>
  <img alt="The image illustrates a flow of script mode execution for custom training scripts on SageMaker, involving Amazon S3 for data storage." />
</Frame>

Key benefits of Script Mode:

* Minimal code changes — keep your existing `train.py` and other modules.
* Managed infrastructure — SageMaker handles instance provisioning and lifecycle.
* Scalability — run on CPU or GPU instances, and scale to distributed training.
* Experiment tracking — logs, metrics, and artifacts are collected automatically.
* Flexibility — include third‑party libraries and arbitrary training logic.

<Frame>
  <img alt="The image lists the advantages of script mode, including minimal code changes, managed infrastructure, scalability, experiment tracking, and flexibility, each with an icon." />
</Frame>

How Script Mode works

With Script Mode, you bring your training entry point (for example, `train.py`) and SageMaker runs it inside a managed container that already includes the specified framework and Python runtime. Typically you provide:

* `train.py` — required training entry point
* `inference.py` — optional inference handler for deployment
* `requirements.txt` — optional list of additional Python packages

The SageMaker Estimator acts as the recipe for the training job. When you create an Estimator you configure:

* Script to run (`entry_point`)
* Framework / container (e.g., TensorFlow, PyTorch)
* Compute resources (instance type and count)
* Data locations (S3 URIs for channels such as `train` and `validation`)
* Hyperparameters (epochs, learning rate, batch size)
* IAM role (permissions to access S3 and other AWS services)

<Frame>
  <img alt="The image illustrates the workflow of AWS SageMaker's Script Mode, showing how a developer uses SageMaker Estimator to configure and upload training scripts and data to Amazon S3, which runs in a SageMaker Training Job." />
</Frame>

Estimator components

<Frame>
  <img alt="The image outlines the components of a SageMaker Estimator, including script to run, framework/container, compute resources, data location, hyperparameters, and IAM role." />
</Frame>

Below is a concise reference for common Estimator parameters and their purpose.

| Parameter           |                                      Purpose | Example                                  |
| ------------------- | -------------------------------------------: | ---------------------------------------- |
| `entry_point`       |              Training script file to execute | `train.py`                               |
| `source_dir`        |   Directory with additional code and modules | `src/`                                   |
| `role`              |             IAM role for training job access | `arn:aws:iam::123456:role/SageMakerRole` |
| `instance_type`     |             Compute instance to run training | `ml.p3.2xlarge`                          |
| `instance_count`    | Number of instances for distributed training | `1`                                      |
| `framework_version` |      Framework version used by the container | `2.3`                                    |
| `py_version`        |          Python runtime inside the container | `py310`                                  |
| `hyperparameters`   |        Hyperparameters passed to your script | `{"epochs": 5, "lr": 0.001}`             |
| `channels`          |     S3 input channels mapped at `fit()` time | `{"train": "s3://bucket/train/"}`        |

Example: launching a PyTorch training job using the SageMaker Python SDK

```python theme={null}
from sagemaker.pytorch import PyTorch

estimator = PyTorch(
    entry_point="train.py",           # your training script
    source_dir="src",                 # directory with your code (optional)
    role="arn:aws:iam::123456:role/SageMakerRole",
    instance_type="ml.m5.xlarge",     # compute instance
    instance_count=1,
    framework_version="2.3",          # framework version (example)
    py_version="py310",               # python runtime in container
    hyperparameters={
        "epochs": 5,
        "lr": 0.001
    }
)
