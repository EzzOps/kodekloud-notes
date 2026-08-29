# Launch the training job (uploads source_dir, provisions compute, runs training)
estimator.fit('s3://my-bucket/my-training-data/')
```

This pattern—create an Estimator, set data channels, compute sizing, entry point, and hyperparameters, then call fit()—treats training as a first-class object. SageMaker handles the container lifecycle, resource provisioning, and logging so you can iterate faster.

> **warning** Replace placeholder values (ECR image URIs, IAM role ARNs, and S3 paths) with your environment-specific resources. Ensure the IAM role has permissions for S3, ECR, CloudWatch, and SageMaker actions.

<Frame>
  <img alt="A &#x22;Summary&#x22; slide listing five AWS SageMaker features: SageMaker Training Jobs, ready-made container images, SDK Estimator class, HyperParameter Tuning Jobs, and total control of compute sizing and scale-out. Each item is numbered with teal markers down the center and the slide has a dark left panel labeled &#x22;Summary.&#x22;" />
</Frame>

Next steps and references

* Try this end-to-end in SageMaker Studio to see training job logs, metrics, and artifacts in real time.
* For more details:
  * [SageMaker Training Jobs documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/training.html)
  * [SageMaker Python SDK](https://sagemaker.readthedocs.io/)
  * [HyperParameter Tuning Jobs](https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning.html)

That wraps up this overview of training models using SageMaker managed training jobs. A future demonstration will walk through a complete Studio workflow: launching a training job, monitoring logs and metrics, and evaluating the resulting model artifacts.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/36db8fab-85cc-40f0-8594-573631b0425b/lesson/77609944-7909-4bdd-9a39-45d08af7655f)


# Training Model in SageMaker Studio and Monitoring Training Jobs

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-Data-Scientist/Training-Model-in-SageMaker-Studio-and-Monitoring-Training-Jobs/page

How to run and monitor managed training jobs in Amazon SageMaker Studio, including setup, SDK examples, scaling, cost optimization, logging, checkpoints, and storing artifacts in S3

In this lesson we'll walk through how to train a model in Amazon SageMaker Studio and how to monitor training jobs. This is a central lesson: everything up to this point prepares you for controlled, reproducible model training at scale.

We will cover:

* Common challenges for ML model training (compute, algorithms, training code, and iteration).
* The SageMaker solution: managed training jobs.
* How to kick off and monitor training from a SageMaker Studio Jupyter notebook using the SageMaker Python SDK.
* How training jobs produce optimized model artifacts and how compute resources are provisioned and released automatically.

> **lightbulb** This guide assumes you have a prepared dataset in S3 and a SageMaker execution role. If you need setup instructions, see the [SageMaker getting started documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/gs.html).

## Why training is hard (common problems)

Training at scale introduces operational, cost, and iteration challenges that slow down ML delivery:

* Infrastructure: deciding where to store training data and where to run training jobs.
* Experimentation scale: hundreds or thousands of permutations of algorithms, datasets, and hyperparameters.
* Data movement: copying large datasets to local machines is slow, expensive, or restricted by policies.
* Local compute limits: laptops and small workstations are often insufficient for larger models — leading to long training times and limited reproducibility.

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Problem: ML Infrastructure and Iterations&#x22; with four numbered panels describing issues: Infrastructure Complexity, Slow Experimentation, Data Processing Overhead, and Training Limitations. Each panel includes an icon and a short explanation about time-consuming infrastructure, tedious manual testing, cumbersome data preprocessing, and slow local training." />
</Frame>

Beyond training, you must also consider deployment and production monitoring: hosting the model for inference, detecting model drift, tracking data distribution changes, and sizing resources to balance performance and cost. When iterating on many models you also need model lifecycle management—tracking which models are in training, approved for production, deployed, or flagged for retraining.

<Frame>
  <img alt="A slide titled &#x22;Problem: ML Infrastructure and Iterations&#x22; displaying four numbered panels. They list Deployment Challenges, Monitoring and Debugging Issues, High Costs, and Workflow Inefficiencies, each with a short explanatory sentence." />
</Frame>

## SageMaker managed training jobs: concept and benefits

SageMaker simplifies these concerns by encapsulating training in a managed training job. A training job ties together four core ingredients:

| Resource               | Purpose                                                    | Example                                         |
| ---------------------- | ---------------------------------------------------------- | ----------------------------------------------- |
| Compute infrastructure | Right-sized instances, optionally distributed              | ml.c5.12xlarge, multi-instance training         |
| Training dataset       | Prepared features and labels stored in S3                  | s3://my-bucket/data/processed.csv               |
| Algorithm              | Built-in or custom container for training                  | XGBoost, TensorFlow, custom Docker image        |
| Training script        | Orchestration that loads data, trains, and emits artifacts | Python training script that writes model.tar.gz |

A SageMaker training job provisions the compute, pulls the chosen container (or your custom image), runs the training script, stores inputs/outputs in S3, and tears down compute when the job completes. This provides scalability, reproducibility, and cost control.

What is a training job?

* A managed request to run training on temporary, dedicated compute.
* Defined from a notebook or CI pipeline, but the heavy compute runs on managed instances (not on your notebook kernel).
* Configured with instance type/count, algorithm image, S3 input locations, and S3 output for artifacts.

<Frame>
  <img alt="A diagram illustrating an AWS SageMaker training jobs workflow, showing containers from an Elastic Container Registry feeding into a SageMaker Training Job and JupyterLab space. It also shows S3 storage for input data (processed.csv) and model output (model.tgz)." />
</Frame>

Benefits of SageMaker training jobs:

* Right-size compute and pay only for the time used.
* Easily run distributed training across multiple instances.
* Use built-in algorithm containers to reduce boilerplate.
* Support for popular frameworks (TensorFlow, PyTorch, scikit-learn).
* Managed hyperparameter tuning to accelerate experiments.
* Integration with S3 for efficient data access and artifact storage.
* Optionally use Spot instances for cost savings (with trade-offs).

## Example: define and run a training job from a SageMaker Studio notebook

Below is a concise Python example using the SageMaker Python SDK (v2). Update the role, bucket, and S3 URIs for your environment.

```python theme={null}
