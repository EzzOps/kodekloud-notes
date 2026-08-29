# Fine Tuning Pre Trained Models

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/Fine-Tuning-Pre-Trained-Models/page

Guide to fine-tuning pre-trained models for domain-specific tasks, workflows, SageMaker fine tuning options, modes like LoRA and full tuning, and best practices for training and deployment

Fine-tuning adapts a general-purpose, pre-trained model to a specific task or domain by modifying or adding task-specific layers and retraining on a smaller, domain-focused dataset. This transfer learning approach leverages the base model’s knowledge while tailoring behavior for applications such as healthcare, legal analysis, or specialized customer support.

When to fine-tune:

* You have a domain-specific dataset (medical notes, legal contracts, financial filings).
* The task requires domain-aware vocabulary, specialized patterns, or custom label spaces.
* You want faster convergence and better performance than training from scratch.

<Frame>
  <img alt="The image explains when to fine-tune a model, highlighting usefulness with domain-specific data (e.g., medical, legal) and capturing patterns a general model misses." />
</Frame>

Common examples:

* Fine-tuning on clinical records to build a diagnostic assistant.
* Fine-tuning on contracts to create compliance and clause-tagging tools.

<Frame>
  <img alt="The image is a flowchart illustrating the process of fine-tuning models for specific applications, showing how medical and legal datasets are used with a pre-trained model to create fine-tuned models for medical and legal apps." />
</Frame>

Core idea

* Reuse a pre-trained base model that encodes broad knowledge.
* Freeze or partially freeze base layers to preserve general features, if appropriate.
* Replace the classifier head or add task-specific layers to adapt to your outputs.
* Retrain (fine-tune) the network on your labeled domain data—this requires less time and data than training from scratch and often leads to better task-specific performance.

<Frame>
  <img alt="The image illustrates a &#x22;Fine-Tuned Model&#x22; composed of a &#x22;Pre-Trained Model&#x22; with separate annotations pointing to a &#x22;Base layer&#x22; and &#x22;Task-specific layers.&#x22;" />
</Frame>

Typical fine-tuning workflow

1. Load a pre-trained model from a model hub or from S3.
2. Optionally freeze base layers to retain core general knowledge.
3. Replace the classifier head or add task-specific layers.
4. Compile the model with a suitable optimizer and learning rate schedule.
5. Train on your domain dataset until convergence, monitoring validation metrics.
6. Save artifacts and deploy the updated model for inference.

This approach balances reuse of existing generalization with targeted adaptation to a new task.

<Frame>
  <img alt="The image outlines a &#x22;Fine-Tuning Workflow&#x22; for machine learning, listing six steps: loading a pre-trained model, optionally freezing base layers, replacing the classifier head, compiling with a new optimizer, training on a task-specific dataset, and saving and deploying the updated model." />
</Frame>

Use cases (examples and common tasks)

| Domain           | Typical Tasks                                                | Examples                                                |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------- |
| Healthcare       | Classification, information extraction, diagnosis assistance | Clinical note classification, medical entity extraction |
| Finance          | Sentiment analysis, document classification                  | Earnings call sentiment, risk-report classification     |
| E-commerce       | Recommendation, ranking, search relevance                    | Product ranking, personalized suggestions               |
| Legal            | Clause tagging, summarization, compliance checks             | Contract clause extraction, legal summarization         |
| Customer support | Intent detection, routing, automated responses               | Ticket triage, FAQ generation                           |

<Frame>
  <img alt="The image lists common use cases in various fields, including medical, finance, e-commerce, legal, and customer support, with specific tasks associated with each." />
</Frame>

Amazon SageMaker: fine-tuning options
SageMaker simplifies infrastructure, distributed training, and deployment. Choose an approach based on control, simplicity, and resources:

| Option                          | Description                                                          | Best for                                    |
| ------------------------------- | -------------------------------------------------------------------- | ------------------------------------------- |
| Script Mode                     | Provide your own training script and run on managed infrastructure.  | Full control and custom pipelines           |
| Hugging Face DLC                | Deep Learning Container support for transformers with minimal setup. | Transformer-based NLP tasks                 |
| Amazon JumpStart                | Low-code, pre-built fine-tuning workflows and UI.                    | Rapid prototyping and non-experts           |
| BYOC (Bring Your Own Container) | Custom Docker images for arbitrary environments.                     | Specialized dependencies or custom runtimes |

[Amazon SageMaker](https://learn.kodekloud.com/user/courses/aws-sagemaker) handles distributed training, autoscaling of instances, and artifact storage integration with S3.

<Frame>
  <img alt="The image describes four methods for fine-tuning with SageMaker: Script Mode, Hugging Face DLC, JumpStart, and BYOC, each offering different capabilities for model customization and deployment." />
</Frame>

Typical SageMaker training flow

* Upload your dataset to S3.
* Specify a pre-trained base model or model artifact.
* Configure a training job (compute instance type, replicas, batch sizes, epochs, learning rate).
* Save output artifacts and model checkpoints back to S3 for deployment.

For large models, GPU instances such as `ml.p3.2xlarge` (or larger) are recommended to reduce training time.

Example: SageMaker Studio fine-tuning recipes\
The Studio UI exposes recipes for supervised fine-tuning (full and LoRA), Direct Preference Optimization (DPO) in full and LoRA variants, and reinforcement learning-based methods (reward optimization / RLHF).

<Frame>
  <img alt="The image displays a SageMaker Studio interface showing options for fine-tuning recipes to train an Amazon Nova model, offering various configurations for fine-tuning and reinforcement learning. The sidebar includes application shortcuts like JupyterLab and RStudio." />
</Frame>

Notes on fine-tuning modes

* LoRA (Low-Rank Adaptation): highly parameter-efficient—only a small set of adaptation parameters are learned; ideal for limited compute or many downstream tasks.
* Full-parameter supervised fine-tuning: updates all model weights; flexible but data- and compute-intensive.
* DPO (Direct Preference Optimization): aligns outputs to human preference datasets; available in full and LoRA modes.
* Reinforcement learning (e.g., RLHF): optimizes behavior via reward signals and iterative human feedback loops.

SageMaker supports multiple input modalities: text, images, and video. Configure distributed runs via YAML-like run configurations by specifying model type, replica count, dataset locations, and output paths.

Example run configuration

```yaml theme={null}
run:
  name: "my-lora-run"
  model_type: "amazon.nova-lite-v1:0:300k" # Model variant specification, do not change
change:
  model_name_or_path: "nova-lite/prod"     # Base model path, do not change
  replicas: 4                              # Number of compute instances (4, 8, 16)
  data_s3_path: ""                         # Customer data path
  output_s3_path: ""                       # Output artifact path
```

Hyperparameters and training settings

* `max_length` (sequence length): token window for input sequences.
* `global_batch_size` and per-GPU batch size: impact throughput and gradient stability.
* `max_epochs`: how many passes over the dataset.
* Dropout parameters (`hidden_dropout`, `attention_dropout`, `ffn_dropout`): reduce overfitting risk.

Example training config:

```yaml theme={null}
training_config:
  max_length: 32768
  global_batch_size: 64
trainer:
  max_epochs: 2
model:
  hidden_dropout: 0.0
  attention_dropout: 0.0
  ffn_dropout: 0.0
```

Optimizers and scheduler settings
SageMaker supports optimizers such as distributed fused Adam and AdamW. Tune learning rate, betas, epsilon, weight decay, and scheduler warm-up steps to stabilize training.

Example optimizer and scheduler config:

```yaml theme={null}
optim:
  lr: 5e-6
  name: distributed_fused_adam
  adam_w_mode: true
  eps: 1e-06
  weight_decay: 0.0
  betas:
    - 0.9
    - 0.999
sched:
  warmup_steps: 10
  constant_steps: 0
  min_lr: 5e-7
```

Best practices

* Choose LoRA for resource-constrained setups and when you need multiple task-specific adapters.
* Use full-parameter tuning when you have large, high-quality datasets and access to sufficient compute.
* Employ warm-up steps and a conservative initial learning rate to avoid unstable early updates.
* Monitor validation metrics and checkpoint frequently; save to S3 for reproducibility and deployment.

<Callout icon="lightbulb">
  Choose the fine-tuning strategy based on available compute, dataset size, and the degree of domain shift. Use LoRA for efficiency, and full-parameter fine-tuning when you have sufficient data and resources.
</Callout>

Further reading and references

* [Amazon SageMaker Documentation](https://learn.kodekloud.com/user/courses/aws-sagemaker)
* [Amazon S3 Basics](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f3f28bdc-5ae5-43bb-85b6-01f7b1bfb71b/lesson/d36cd57c-53f0-4d63-8d99-66443b78964e" />
</CardGroup>
