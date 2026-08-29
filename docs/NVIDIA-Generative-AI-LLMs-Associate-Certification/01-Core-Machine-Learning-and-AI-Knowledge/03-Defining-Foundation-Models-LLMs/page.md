# Defining Foundation Models LLMs

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Core-Machine-Learning-and-AI-Knowledge/Defining-Foundation-Models-LLMs/page

Description of foundation models and LLMs pre-trained on broad data and adapted to diverse tasks through fine-tuning, prompting, and retrieval.

Question 13.

Which statement accurately describes foundation models in the context of large language models?

* Models that are trained exclusively on programming languages?
* Models that are trained from scratch for each specific application?
* Models that are pre-trained on broad data and can be adapted to specific tasks?
* Models that can only work with structured data?

Answer: Models that are pre-trained on broad data and can be adapted to specific tasks.

Explanation:
Foundation models are large models pre-trained on vast and diverse datasets to learn general-purpose representations and capabilities. After pre-training, these models are adapted to downstream tasks through techniques such as fine-tuning, prompt engineering, or by augmenting inference with external data (retrieval-augmented generation). This reuse—often called transfer learning—avoids the need to train new models from scratch for every use case. Foundation models are not restricted to programming languages or structured data; they are designed to generalize across many domains and modalities.

<Frame>
  <img alt="The image contains a question about foundation models in the context of large language models, highlighting their adaptability and transferability. An answer is provided, discussing pre-training on broad data and adaptation to specific tasks." />
</Frame>

Comparison of the answer choices:

| Statement                                                      | Correct? | Why                                                                                                                |
| -------------------------------------------------------------- | -------: | ------------------------------------------------------------------------------------------------------------------ |
| Models trained exclusively on programming languages            |       No | Foundation models are trained on broad, multimodal corpora, not limited to code.                                   |
| Models trained from scratch for each specific application      |       No | The point of foundation models is pre-training once and reusing/adapting broadly (transfer learning).              |
| Models pre-trained on broad data and adapted to specific tasks |      Yes | Pre-training captures general patterns; adaptation (fine-tuning, prompting, retrieval) tailors the model to tasks. |
| Models that can only work with structured data                 |       No | Foundation models handle unstructured text, images, code, and more; they are not limited to structured inputs.     |

Key points:

* Pre-training: Learn broad patterns and representations from large, diverse datasets to build general capabilities.
* Adaptation: Specialize foundation models using fine-tuning, prompt engineering, or retrieval-augmented inference.
* Transferability: Reuse a single pre-trained model across many tasks and domains rather than training separate models per task.

<Callout icon="lightbulb">
  Foundation models provide a flexible base: they can be adapted efficiently to many specific tasks while leveraging the broad knowledge acquired during pre-training.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/875d98e8-3b09-4f35-b877-2758b84443ca/lesson/0aaeb647-f783-48ad-8cb9-39c1e0e9154a" />
</CardGroup>
