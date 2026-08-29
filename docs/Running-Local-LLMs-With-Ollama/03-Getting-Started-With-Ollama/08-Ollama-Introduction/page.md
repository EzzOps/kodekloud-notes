# At the prompt, type:
show info
```

<Frame>
  ![The image shows a "Model Info Page" for Meta's Llama 3.2, detailing its specifications and features, with a Meta logo and a brief description of the model's capabilities.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883705/notes-assets/images/Running-Local-LLMs-With-Ollama-Models-and-Model-Parameters/llama-3-2-model-info-page.jpg)
</Frame>

Understanding these terms will help you select a model that aligns with your application’s requirements and hardware constraints. Let’s break them down.

## Architecture

A model’s architecture is its blueprint, defining the core design and the family it belongs to. For example, LLaMA 3.1, 3.2, and 3.3 all share the **LLaMA** architecture—Meta’s transformer-based model line.

<Callout icon="lightbulb">
  If you’ve already built pipelines around one architecture, sticking with the same family ensures consistent behavior.
</Callout>

<Frame>
  ![The image is a slide titled "Architecture" with three bullet points describing aspects of a model's design, its family, and its relation to the Llama family of models by Meta.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883706/notes-assets/images/Running-Local-LLMs-With-Ollama-Models-and-Model-Parameters/architecture-model-design-bullet-points.jpg)
</Frame>

Learn more about transformers in the [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) documentation.

## Parameters

Parameters are the “knowledge” learned during training, stored as numerical weights. Think of a model as a library: each parameter is like a book on the shelf. More parameters = more books = more stored information.

* **3.2 B parameters** means 3.2 billion “books.”
* For comparison, **GPT-3** has **175 B parameters**.

<Frame>
  ![The image is a slide titled "Parameters" with a description stating, "The 'knowledge' stored and learned during the training."](../../../../images/kodekloud.com/kk-media/image/upload/v1752883707/notes-assets/images/Running-Local-LLMs-With-Ollama-Models-and-Model-Parameters/parameters-knowledge-training-slide.jpg)
</Frame>

Larger models typically yield better accuracy but require more memory and compute power.

<Callout icon="triangle-alert">
  High-parameter models can exceed your machine’s RAM and slow down inference. Choose a smaller model if you have limited resources.
</Callout>

<Frame>
  ![The image compares two models with different parameter sizes, illustrating a smaller model with million parameters and a larger GPT-3 model with billion parameters, totaling 3.2 billion parameters.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883708/notes-assets/images/Running-Local-LLMs-With-Ollama-Models-and-Model-Parameters/model-comparison-parameters-gpt3.jpg)
</Frame>

## Weights

Weights determine the strength of connections within the neural network. During training, these values are optimized—much like refining a recipe by adjusting ingredient ratios to get the best flavor.

* Each input feature is an ingredient.
* The weight assigns its importance in the final prediction.

<Frame>
  ![The image illustrates "Weights in LLM" with a brain icon labeled "Decision-making Brain" at the center, surrounded by a gradient arc from green (high) to red (low).](../../../../images/kodekloud.com/kk-media/image/upload/v1752883710/notes-assets/images/Running-Local-LLMs-With-Ollama-Models-and-Model-Parameters/weights-in-llm-decision-making-brain.jpg)
</Frame>

Once training finishes, weights are fixed. If the model “knows” that 2 + 2 = 4, that pathway has a high weight compared to incorrect routes.

## Context Length

Context length (or context window) is the maximum number of tokens the model can process at once. Think of it as how much of your book you can feed to the model at a time.

* **131,072 tokens** ≈ 100K–130K words.

<Frame>
  ![The image is a slide titled "Context Length," explaining how much a model can "remember" and process at once, with an example text about a dog named Max in a village. It includes an icon labeled "Writing a Book."](../../../../images/kodekloud.com/kk-media/image/upload/v1752883710/notes-assets/images/Running-Local-LLMs-With-Ollama-Models-and-Model-Parameters/context-length-model-memory-example.jpg)
</Frame>

Larger context lengths maintain coherence over longer documents or conversations but also increase memory usage.

<Frame>
  ![The image explains context length, showing that a model can process 131,072 tokens, equivalent to 100,000–130,000 words.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883711/notes-assets/images/Running-Local-LLMs-With-Ollama-Models-and-Model-Parameters/context-length-model-tokens-explanation.jpg)
</Frame>

<Callout icon="lightbulb">
  For long transcripts or codebases, choose a model with an extended context window to avoid cutting off important information.
</Callout>

## Embedding Length

When processing text, each token is converted into a vector of fixed length—this is the embedding length. Larger embeddings capture richer contextual information.

* **3,072-dimensional vector** → each token is represented in 3,072 dimensions.

<Frame>
  ![The image explains "Embedding Length," indicating that a vector representation of each token has a length of 3,072.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883712/notes-assets/images/Running-Local-LLMs-With-Ollama-Models-and-Model-Parameters/embedding-length-vector-representation.jpg)
</Frame>

Big embeddings help the model understand subtle nuances but increase computational load.

## Quantization

Quantization reduces numeric precision (e.g., from 32-bit floats to 4-bit integers) to save memory and speed up inference. It’s similar to compressing an image: you lose a bit of detail but gain storage and performance benefits.

<Frame>
  ![The image explains quantization, highlighting the reduction of precision from 32-bit to 4-bit to save memory and speed up processing.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883713/notes-assets/images/Running-Local-LLMs-With-Ollama-Models-and-Model-Parameters/quantization-precision-reduction-diagram.jpg)
</Frame>

<Callout icon="lightbulb">
  Quantized models (e.g., Q4, Q8) strike a balance between speed and accuracy, ideal for local development.
</Callout>

***

Next, we’ll navigate back to the Ollama website to explore additional models and run a second experiment on our local machine.

<Frame>
  ![The image outlines two next steps: exploring different models on the Ollama website and running a second model on a local machine.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883714/notes-assets/images/Running-Local-LLMs-With-Ollama-Models-and-Model-Parameters/ollama-next-steps-models-running.jpg)
</Frame>

***

## Links and References

* [Ollama Documentation](https://ollama.com/docs/)
* [Transformer Architecture](https://arxiv.org/abs/1706.03762)
* [Quantization Techniques for LLMs](https://www.tensorflow.org/model_optimization/quantization)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/running-local-llms-with-ollama/module/836a96fe-9951-42b6-83ba-a602299c87c9/lesson/1c40541c-995a-42a4-b393-e99e3cb97b17" />
</CardGroup>


# Ollama Introduction

Source: https://notes.kodekloud.com/docs/Running-Local-LLMs-With-Ollama/Getting-Started-With-Ollama/Ollama-Introduction/page

This guide introduces Ollama, an open-source solution for running and developing large language models locally, addressing AI development challenges.

Welcome to this guide on Ollama, the open-source solution for running and developing large language models (LLMs) locally. We’ll start by examining the challenges in AI development today, then see how Ollama addresses them without vendor lock-in or high cloud costs.

## Current AI Development Challenges

As AI adoption grows, developers face multiple hurdles when building and testing LLM-powered applications:

1. **Complex local setup**\
   Traditional apps spin up a local database, but most LLMs run on remote servers, complicating offline development.

<Frame>
  ![The image lists current problems in the AI space, including difficulties in local development, dependency on internet access, and challenges in experimenting with and customizing LLM models.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883715/notes-assets/images/Running-Local-LLMs-With-Ollama-Ollama-Introduction/ai-problems-local-development-llm.jpg)
</Frame>

2. **Internet dependency & vendor lock-in**\
   Relying on an external LLM service means constant connectivity, shared billing info, and limited flexibility when new models appear.

<Frame>
  ![The image illustrates current problems in the AI space, showing a flow from a large language model (LLM) and OpenAI to a user named Jane, highlighting issues related to internet access and cost.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883716/notes-assets/images/Running-Local-LLMs-With-Ollama-Ollama-Introduction/ai-problems-llm-openai-jane.jpg)
</Frame>

3. **DIY cloud infrastructure is costly**\
   Hosting your own GPU-backed servers requires significant time, expertise, and budget.

<Frame>
  ![The image illustrates current problems in the AI space, highlighting cloud infrastructure, time, and cost issues associated with a person named Jane.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883717/notes-assets/images/Running-Local-LLMs-With-Ollama-Ollama-Introduction/ai-problems-cloud-infrastructure-jane.jpg)
</Frame>

4. **High compute costs & compliance risks**\
   Cloud GPUs rack up bills quickly, and sending sensitive data externally can conflict with GDPR or HIPAA requirements.

<Frame>
  ![The image lists five current problems in the AI space, including difficulties in local development, internet dependency, cumbersome model customization, high cloud computing costs, and data protection challenges.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883718/notes-assets/images/Running-Local-LLMs-With-Ollama-Ollama-Introduction/ai-problems-local-dev-internet-dependency.jpg)
</Frame>

Now that these pain points are clear, let’s explore how Ollama provides a seamless local LLM workflow.

## What Is Ollama?

Ollama is an open-source CLI and API that lets you run, experiment with, and fine-tune LLMs on your own machine. It supports macOS, Windows, Linux, and Docker:

* Access models from various vendors—no single-source lock-in
* Interact via an OpenAI-compatible API for easy integration
* Leverage a growing community of plugins and integrations

<Frame>
  ![The image is an infographic about "Ollama," an open-source tool for running and developing LLMs locally. It highlights its compatibility with various platforms, support for different LLM models, and a large community for integrations.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883719/notes-assets/images/Running-Local-LLMs-With-Ollama-Ollama-Introduction/ollama-open-source-llm-infographic.jpg)
</Frame>

In short, Ollama replaces costly cloud services or DIY infrastructure with a local, secure, and flexible environment for AI development.

## Use Cases

### 1. Developing AI Applications

Build and test AI features entirely offline, free from API charges and data egress:

* No upfront payment or account setup
* Full data privacy—everything runs on your device
* Smooth production transition via OpenAI-compatible endpoints

<Frame>
  ![The image is a comparison between OpenAI and Ollama, highlighting features such as API access, payment requirements, data privacy, and compatibility.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883721/notes-assets/images/Running-Local-LLMs-With-Ollama-Ollama-Introduction/openai-ollama-comparison-features.jpg)
</Frame>

Ollama also supports fine-tuning, enabling you to customize models for:

| Use Case           | Description                       |
| ------------------ | --------------------------------- |
| Chatbots           | Domain-specific conversational AI |
| Virtual Assistants | Task automation and scheduling    |
| Content Generators | Blog posts, marketing copy, more  |
| Code Analyzers     | Static analysis, code completion  |

<Frame>
  ![The image lists four types of fine-tuning models: Chatbots, Virtual Assistants, Content Generators, and Code Analyzers, each with a corresponding icon.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883722/notes-assets/images/Running-Local-LLMs-With-Ollama-Ollama-Introduction/fine-tuning-models-chatbots-virtual-assistants.jpg)
</Frame>

<Callout icon="lightbulb">
  With Ollama’s offline mode, your app’s performance is consistent—no more flakey internet. Switch models on the fly, from code-focused to image-capable, and find the best fit.
</Callout>

<Frame>
  ![The image is a slide titled "More About Ollama," highlighting its offline functionality for consistent performance and its ability to run various models fine-tuned for code and images.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883722/notes-assets/images/Running-Local-LLMs-With-Ollama-Ollama-Introduction/more-about-ollama-offline-functionality.jpg)
</Frame>

### 2. Privacy-Centric Platforms

Organizations like Growmore handle highly sensitive data and require in-house AI solutions. Ollama enables:

* Local or on-prem deployment
* GDPR & HIPAA compliance by keeping data internal
* Secure employee-facing chatbots without external API calls

<Frame>
  ![The image is a diagram titled "Ollama on Data Privacy," showing the relationship between organizations, chatbots, and users, with references to GDPR and HIPAA compliance.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883723/notes-assets/images/Running-Local-LLMs-With-Ollama-Ollama-Introduction/ollama-data-privacy-diagram.jpg)
</Frame>

### 3. Exploring AI Advancements

Stay ahead of the curve by testing new models as they emerge:

* Benchmark performance across architectures
* Fine-tune for niche tasks and industries
* Compare behavior side by side to pick the ideal model

<Frame>
  ![The image is a slide titled "Exploring AI Advancements," highlighting three points: testing model performance, fine-tuning for tasks, and understanding behavior in unique scenarios.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883724/notes-assets/images/Running-Local-LLMs-With-Ollama-Ollama-Introduction/exploring-ai-advancements-slide.jpg)
</Frame>

## Benefits of Ollama

| Benefit        | Why It Matters                                       |
| -------------- | ---------------------------------------------------- |
| Secure         | Keeps all data and inference on your local machine   |
| Cost-effective | Free, open source, and no hidden cloud charges       |
| Efficient      | Quick setup, rapid model swaps, and zero vendor lock |

<Frame>
  ![The image is a slide titled "Ollama – Benefits," highlighting three benefits: Secure, Cost-effective, and Efficient, each with corresponding icons.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883725/notes-assets/images/Running-Local-LLMs-With-Ollama-Ollama-Introduction/ollama-benefits-secure-cost-effective-efficient.jpg)
</Frame>

## Get Started

To begin running LLMs locally with Ollama, download the installer for your platform at [ollama.com](https://ollama.com) and follow the setup guide. In the next section, we’ll walk through installing Ollama and launching your first local model. Happy coding!

## Links and References

* [OpenAI service](https://openai.com)
* [GDPR](https://gdpr.eu)
* [HIPAA](https://www.hhs.gov/hipaa/index.html)
* [Ollama Official Website](https://ollama.com)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/running-local-llms-with-ollama/module/836a96fe-9951-42b6-83ba-a602299c87c9/lesson/7dc953fc-f816-41ad-8e06-66127d2b72d2" />
</CardGroup>
