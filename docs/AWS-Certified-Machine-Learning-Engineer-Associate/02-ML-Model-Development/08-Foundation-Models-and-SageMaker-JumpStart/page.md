# Foundation Models and SageMaker JumpStart

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/Foundation-Models-and-SageMaker-JumpStart/page

Overview of foundation models and using Amazon SageMaker JumpStart to browse, deploy, and fine tune large pretrained models with deployment, cost, and best practice guidance

Foundation models are large neural networks trained on extremely large and diverse datasets. They provide a reusable base that can be adapted to many downstream tasks. The high-level workflow for building and applying foundation models:

* Collect massive amounts of raw data from web crawls, books, code repositories, images, and other sources.
* Clean and preprocess this data to produce high-quality training corpora.
* Pre-train models at scale using high-performance accelerators (GPUs or TPUs).
* Adapt the pre-trained model for specific tasks via fine-tuning, prompt engineering, or few-/zero-shot techniques.
* Deploy the adapted model to production for inference in real-world applications.

<Frame>
  <img alt="The image is a diagram titled &#x22;Foundation Models – Introduction&#x22; showing a sequential process involving massive data collection, preprocessing, and pretraining on GPUs/TPUs. It illustrates the initial steps of building foundation models." />
</Frame>

Common real-world applications powered by foundation models:

* Conversational AI and chatbots that generate human-like responses.
* Text summarization to extract key insights from long documents.
* Computer vision tasks: image classification, object detection, and multimodal understanding.
* Semantic search that captures intent and context rather than keyword matches.
* Developer tools for code generation, completion, and debugging assistance.

Key characteristics of foundation models:

* Fine-tunable: Can be specialized for tasks such as summarization, translation, and image captioning.
* Large scale: Trained on data sources like `Common Crawl`, book corpora, code, and images; model sizes range from billions to trillions of parameters.
* High compute requirements: Training and many inference workloads benefit from GPU/TPU acceleration.
* Transfer learning: Support few-shot and zero-shot learning to accelerate adaptation to new tasks.
* Multimodal capabilities: Some models support text, image, audio, and video modalities enabling cross-modal generation and understanding.

<Frame>
  <img alt="The image lists characteristics of foundation models, highlighting features such as their massive scale, pretraining and fine-tuning capabilities, multimodal support, and role as a base for downstream models." />
</Frame>

Popular foundation-model families (proprietary and open-weight):

* AI21 J2 (J2-Jumbo): [https://www.ai21.com/](https://www.ai21.com/)
* Amazon Titan (via Amazon Bedrock): [https://aws.amazon.com/bedrock/](https://aws.amazon.com/bedrock/)
* Anthropic Claude: [https://www.anthropic.com/](https://www.anthropic.com/)
* Cohere Command: [https://cohere.ai/](https://cohere.ai/)
* Meta LLaMA: [https://ai.meta.com/llama/](https://ai.meta.com/llama/)
* Mistral: [https://mistral.ai/](https://mistral.ai/)
* Stable Diffusion (multimodal image generation): [https://stability.ai/](https://stability.ai/)

Many of these models are available through managed platforms such as Amazon Bedrock and integrated services such as SageMaker JumpStart.

## SageMaker JumpStart overview

[SageMaker JumpStart](https://aws.amazon.com/sagemaker/jumpstart/) is a curated model and solution hub inside Amazon SageMaker that accelerates prototyping by providing pre-trained models, solution templates, and example notebooks. JumpStart supports both open-source and commercial models and lets you evaluate and deploy models quickly using the SageMaker SDK or Studio UI.

<Frame>
  <img alt="The image shows the SageMaker JumpStart interface displaying a selection of AI model providers like Introduction to OpenAI, Meta, Hugging Face, and AWS, each with options to view models." />
</Frame>

Primary benefits of JumpStart:

* Low-friction experimentation: no heavy setup required to start evaluating models.
* Seamless SageMaker Studio integration for interactive development.
* Simplified endpoint deployment for real-time inference.
* Fine-tuning support for customizing models to your data and tasks.
* Ready-made templates and solutions for common ML problems (fraud detection, churn prediction, sentiment analysis, etc.).

<Frame>
  <img alt="The image outlines the key benefits of JumpStart: no setup required, hosted in SageMaker Studio, easy model deployment as endpoints, and support for fine-tuning select models." />
</Frame>

## Browsing, selecting, and deploying models

From the JumpStart dashboard you can browse foundation-model listings, inspect model cards (which describe inputs/outputs, cost, and resource needs), and use example notebooks. When you choose a model you can deploy it to a SageMaker inference endpoint directly from Studio. The UI typically exposes settings such as endpoint name, instance type, and inference configuration (UI details may change over time).

<Frame>
  <img alt="The image shows a screenshot from SageMaker Studio, depicting the process of deploying a model to an endpoint, with settings for endpoint name, instance type, and inference type displayed." />
</Frame>

## Example: load, deploy, and invoke a JumpStart model

A typical workflow using the SageMaker JumpStart SDK looks like this:

```python theme={null}
from sagemaker.jumpstart.model import JumpStartModel
