# Demystifying Advanced SageMaker

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Wrap-Up/Demystifying-Advanced-SageMaker/page

Overview of SageMaker advanced features, comparing foundation models, Bedrock, and HyperPod clusters with guidance on fine‑tuning, hosting, scaling, and decision criteria.

In this lesson we summarize several advanced Amazon SageMaker features visible in the console, organized around common problems and pragmatic solutions. The goal is to give a high‑level, actionable view of when to use foundation models, Bedrock, and HyperPod clusters — and how to choose between them.

Topics covered:

* Foundation models and fine‑tuning
* Bedrock as an alternative for hosted foundation models
* HyperPod clusters for large‑scale distributed training
* How to decide between SageMaker and Bedrock for different needs

## Problem → Solution: foundation models

### Problem 1 — Why building models from scratch is expensive

Traditional ML workflows often require:

* Large, well‑labeled datasets
* Significant compute (often GPUs) for training
* Specialized expertise to build, tune, and deploy models
* Long development cycles before a model is production ready

These constraints can make building models from scratch slow and costly.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Traditional Machine Learning Models&#x22; that lists four challenges: extensive labeled data for training, high computational resources, expertise to fine-tune and deploy models, and long development cycles before production." />
</Frame>

### Solution — Foundation models

A foundation model is a large, pre‑trained model that you can use as‑is or adapt for a specific task. SageMaker supports importing and hosting many foundation models (both open source and vendor artifacts), enabling rapid experimentation and deployment for NLP, vision, speech, code generation, and more.

Common examples:

* LLaMA (Meta) — [https://ai.meta.com/llama/](https://ai.meta.com/llama/)
* Falcon — [https://falconllm.tii.ae/](https://falconllm.tii.ae/)
* Stable Diffusion — [https://stability.ai/blog/stable-diffusion-public-release](https://stability.ai/blog/stable-diffusion-public-release)
* Vendor-hosted models like GPT‑4 (OpenAI) and Claude (Anthropic)

Availability for self‑hosting depends on licensing and vendor restrictions: open models are more likely to be imported and hosted in your SageMaker account, while some proprietary models are only offered via vendor APIs.

Two ways to use foundation models in SageMaker:

* Host a model artifact in SageMaker and create an endpoint for inference.
* Fine‑tune the model in SageMaker and then deploy the tuned artifact.

Fine‑tuning tip: use parameter‑efficient methods (for example LoRA or other PEFT techniques) so you only update a small subset of parameters. This reduces compute, storage, and cost compared to full‑parameter retraining: run a standard SageMaker training job, produce a custom artifact, and deploy it to an endpoint.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Foundation Models&#x22; with a subheading &#x22;Models for text, vision, and speech.&#x22; Below are three circular icons labeled Natural Language Processing (NLP), Image Generation, and Code Generation." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Foundation Models&#x22; showing a &#x22;Ready-to-use models&#x22; label and icons for several AI models. The slide displays GPT-4, LLaMA, Claude, FalconGPT, Stable Diffusion, and Falcon." />
</Frame>

### Browsing and selecting models in SageMaker Studio

In SageMaker Studio you can browse providers and models, inspect metadata, and import model artifacts directly into your account. Provider cards indicate model counts and sometimes show whether a model is “Bedrock Ready,” helping you select an appropriate model for import or hosted inference.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Foundation Models&#x22; showing a dashboard of provider cards for various AI model vendors (Hugging Face, Meta, Stability AI, Cohere, TensorFlow, PyTorch, etc.). Each card displays the provider logo, a short description, and the number of available models." />
</Frame>

## Bedrock — a hosted alternative for foundation models

Amazon Bedrock is a separate AWS service that provides managed access to Bedrock‑ready foundation models via a unified API. Key benefits:

* Standardized API with pay‑per‑call pricing (no infra provisioning)
* Automatic scaling and fully managed hosting
* Ability to swap provider/model identifiers without changing client logic beyond the model name

Bedrock is ideal when you want quick, hosted access to vendor models and do not need custom infra control or deep fine‑tuning.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Bedrock Alternative for Foundation Models&#x22; with an Amazon Bedrock logo. It lists five benefits: consistent API access to Bedrock-ready models, auto-scaling pay-per-call, no infrastructure setup, no endpoint provisioning, and simple API calls as an alternative to SageMaker endpoints." />
</Frame>

<Callout icon="lightbulb">
  Bedrock and SageMaker solve different needs: choose Bedrock for simple, hosted model access with pay‑per‑call billing and minimal infrastructure work. Choose SageMaker if you require full control over model artifacts, training workflows, VPC isolation, or advanced fine‑tuning.
</Callout>

### Decision table: SageMaker vs Bedrock

| Resource  | Best for                                     | When to choose                                                                                           |
| --------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Bedrock   | Managed, hosted model inference              | Quick prototyping or production inference without infra management; pay-per-call billing                 |
| SageMaker | Full control (training, hosting, networking) | Custom training/fine‑tuning, private deployments (VPC), specialized endpoints, or self‑hosting artifacts |

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Bedrock Alternative for Foundation Models&#x22; showing three teal-highlighted boxes with icons and captions: &#x22;Provision an endpoint,&#x22; &#x22;Deploy the model,&#x22; and &#x22;Manage scaling and costs.&#x22; Each box contains a simple line icon (shield/hand, rocket, and money bags with a gear)." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Foundation Models&#x22; that lists three SageMaker use cases: full model control (deploy a custom Sonnet), heavy fine-tuning (more access than Bedrock), and private deployment (SageMaker endpoint for security/compliance)." />
</Frame>

## Problem → Solution: HyperPod for massive distributed training

### Problem — training very large models is hard

Training extremely large models often requires:

* Huge compute and memory capacity (multi‑GPU, multi‑node)
* Efficient, low‑latency, high‑bandwidth networking
* Orchestration across hundreds or thousands of nodes
* Fault tolerance and automatic recovery to protect long-running jobs

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Training Large-Scale Foundation Models&#x22; that lists requirements for training such models: massive compute resources with high memory and parallel processing, distributed multi‑GPU training, optimized cost‑efficient infrastructure, and seamless orchestration of thousands of compute instances." />
</Frame>

### Solution — HyperPod clusters

HyperPod clusters are a managed, high‑performance compute environment inside SageMaker built for coordinating very large distributed training jobs. Highlights:

* SLURM‑based controller to orchestrate controller and worker nodes
* Job resilience with automatic restarts and node reallocation on failure
* Network topology optimized for low latency and high bandwidth
* Integration with shared storage (for example Amazon FSx for Lustre) and lifecycle scripts stored in Amazon S3

HyperPod is designed for large runs (hundreds of nodes, many GPUs). For single‑node or small multi‑GPU jobs, standard SageMaker training jobs are simpler and more cost‑effective.

<Frame>
  <img alt="An AWS architecture diagram of an Amazon SageMaker HyperPod HPC cluster. It shows users connecting via AWS Systems Manager into a VPC with Amazon FSx for Lustre, controller/login/worker nodes running Slurm components, and lifecycle scripts stored in an S3 bucket." />
</Frame>

### When to use HyperPod

* Use HyperPod for large foundation model training across many nodes when you need optimized networking and strong fault recovery.
* Avoid HyperPod for short experiments or models that fit on a few GPUs — prefer regular SageMaker training jobs in those cases.

## Summary and quick recommendations

* Foundation models give immediate access to large pre‑trained models for NLP, vision, speech, and code tasks; you can self‑host in SageMaker or call vendor models via Bedrock.
* Fine‑tuning with PEFT methods (for example LoRA) makes customizing foundation models practical without re‑training billions of weights.
* Bedrock is a fully managed, pay‑per‑call service suitable for teams that want hosted model access with minimal infra management.
* HyperPod clusters provide SLURM‑based orchestration and optimized networking for very large, distributed training jobs that require fault tolerance and high throughput.

## Links and references

* SageMaker documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* Amazon Bedrock overview: [https://aws.amazon.com/bedrock/](https://aws.amazon.com/bedrock/)
* SLURM scheduler: [https://slurm.schedmd.com/](https://slurm.schedmd.com/)
* Amazon FSx for Lustre: [https://aws.amazon.com/fsx/lustre/](https://aws.amazon.com/fsx/lustre/)
* LoRA paper: [https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)
* PEFT (Hugging Face PEFT): [https://github.com/huggingface/peft](https://github.com/huggingface/peft)

Use these links to dive deeper into specific features and to evaluate architecture choices for your workloads.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/b8b80e38-7fae-401c-a5ff-d6f0af493cea/lesson/39dd4850-289f-4a6c-8f7e-e70e2ea5a2db" />
</CardGroup>
