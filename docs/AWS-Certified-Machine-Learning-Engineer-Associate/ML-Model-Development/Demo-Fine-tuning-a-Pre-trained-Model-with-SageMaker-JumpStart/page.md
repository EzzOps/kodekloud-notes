# Demo Fine tuning a Pre trained Model with SageMaker JumpStart

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/Demo-Fine-tuning-a-Pre-trained-Model-with-SageMaker-JumpStart/page

Guide to fine-tuning pre-trained models using AWS SageMaker JumpStart, covering artifacts, compute, hyperparameters, training workflow, and LoRA customization

Fine-tuning adapts a pre-trained model to your specific dataset and task so you avoid training from scratch. It is typically faster, less expensive, and often yields better results when labeled data is limited.

<Frame>
  <img alt="The image shows the AWS SageMaker Studio interface, specifically the Models section, where users can discover, evaluate, and deploy different models like Qwen3.5-4B and Nvidia Nemotron3 Nano Omni. Various navigation and customization options are visible on the sidebar." />
</Frame>

Why start from pre-trained checkpoints? Organizations and open-source projects have already trained large models and released checkpoints with solid baseline performance. Using JumpStart models lets you leverage that prior compute and expertise—then adapt the checkpoint to your domain, labels, or task through fine-tuning.

<Callout icon="lightbulb">
  Pre-trained checkpoints save time and GPU compute. Fine-tuning adapts an existing model to new labels, domains, or tasks without starting from random initialization.
</Callout>

Some JumpStart entries are inference-only (evaluation/deployment artifacts), while others include training workflows. For example, a Table Transformer Detection model in JumpStart may be offered primarily for evaluation and deployment:

<Frame>
  <img alt="The image shows a SageMaker Studio interface featuring the &#x22;Huggingface Od Microsoft Table Transformer Detection&#x22; model, with options for evaluation, deployment, and training. It provides a description of the Table Transformer model fine-tuned for table detection." />
</Frame>

When a model supports training, SageMaker JumpStart provides a guided job-creation workflow. You will supply three primary artifacts and a compute configuration.

<Frame>
  <img alt="The image shows a screenshot of the AWS SageMaker Studio interface, specifically the section for creating a training job. It includes options for setting model and dataset artifact locations, along with various configuration settings." />
</Frame>

Required artifacts and where to put them:

|                 Artifact | Description                                                                                      | Example                             |
| -----------------------: | ------------------------------------------------------------------------------------------------ | ----------------------------------- |
|     Input model artifact | The pre-trained checkpoint (weights, config, tokenizer). Typically an S3 prefix.                 | `s3://my-bucket/models/pretrained/` |
|         Training dataset | Your labeled data for fine-tuning. Format depends on model (CSV, JSONL, TFRecord, images, etc.). | `s3://my-bucket/data/training/`     |
| Output artifact location | Where SageMaker writes fine-tuned checkpoints and metadata.                                      | `s3://my-bucket/models/finetuned/`  |

Think of artifacts as serialized model state. Each training run produces new files (updated weights, optimizer state, tokenizer changes, training logs and metrics).

You also select compute for training. JumpStart exposes recommended defaults such as `ml.m5.xlarge` (CPU) or GPU instances like `ml.p3.2xlarge`. Choose instance type and count based on model size, memory/GPU needs, and budget.

<Frame>
  <img alt="The image shows the interface of Amazon SageMaker Studio, specifically the section for creating a training job, including settings for output artifact location, compute instance type, and hyperparameters." />
</Frame>

Hyperparameters — what to configure and why

* For classical models (e.g., linear classifiers) you’ll often choose penalty/regularization, tolerance, and solver parameters.
* For deep models, tune learning rate, batch size, number of epochs, weight decay, and optimizer type.

Example hyperparameter block for a linear classifier (illustrative):

```JavaScript theme={null}
{
  "penalty": "l2",
  "C": 1.0,            // inverse of regularization strength (scikit-learn style)
  "tol": 1e-4,
  "l1_ratio": 0.15     // used only if penalty == 'elasticnet'
}
```

Notes:

* Some libraries (e.g., scikit-learn) use `C` as the inverse of regularization strength; other frameworks use `alpha` or `lambda`.
* Always start with default values and run small experiments to find good hyperparameters before scaling up.

After launching the job, monitor training status, logs, and metrics in Studio’s training jobs view.

<Frame>
  <img alt="The image shows a screenshot of the AWS SageMaker Studio interface, where a new training job is being created with specified hyperparameters." />
</Frame>

JumpStart lists created jobs (including JumpStart-created training jobs and other job types) in the Studio Jobs view. From there you can inspect job state, stream logs, and follow links to input/output artifacts and metrics.

For large generative models, JumpStart also supports model customization strategies. Low-Rank Adaptation (LoRA) is a widely-used technique that injects low-rank update matrices into transformer layers instead of modifying full model weights. LoRA drastically reduces GPU memory usage and the storage required for fine-tuned weights by saving only the low-rank adapters.

<Frame>
  <img alt="The image shows a screenshot of the AWS SageMaker Studio interface for creating a custom machine learning model, with options for model customization techniques like supervised fine-tuning and reinforcement learning." />
</Frame>

<Callout icon="warning">
  Fine-tuning large models (even with LoRA) can be expensive in GPU time and data transfer. Monitor costs, run small experiments first, and cap runtimes or instance counts for early trials.
</Callout>

Quick checklist before you submit a JumpStart fine-tuning job:

| Step | Action                                                                                                     |
| ---- | ---------------------------------------------------------------------------------------------------------- |
| 1    | Confirm the chosen JumpStart model supports training/fine-tuning.                                          |
| 2    | Upload or reference the pre-trained checkpoint in S3 (input model artifact).                               |
| 3    | Upload or reference the training dataset in S3.                                                            |
| 4    | Provide an output S3 location for resulting artifacts.                                                     |
| 5    | Choose instance types and count appropriate for the model.                                                 |
| 6    | Set hyperparameters (learning rate, batch size, regularization or `C`, `tol`, `l1_ratio` when applicable). |
| 7    | Submit the training job and monitor logs, metrics, and outputs.                                            |

Links and references

* SageMaker JumpStart — model catalog, fine-tuning, and deployment: [https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart.html](https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart.html)
* LoRA: [https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)
* scikit-learn regularization reference: [https://scikit-learn.org/stable/modules/linear\_model.html](https://scikit-learn.org/stable/modules/linear_model.html)

This article explained how to prepare and submit a fine-tuning job in SageMaker JumpStart, how artifacts map to S3 locations, the compute and hyperparameter choices you’ll configure in Studio, and model customization options such as LoRA.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f3f28bdc-5ae5-43bb-85b6-01f7b1bfb71b/lesson/8f32012e-a8c9-44e1-af7b-d71a17b62259" />
</CardGroup>
