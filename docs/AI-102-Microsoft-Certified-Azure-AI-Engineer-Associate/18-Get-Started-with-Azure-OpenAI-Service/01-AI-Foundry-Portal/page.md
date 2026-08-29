# AI Foundry Portal

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Get-Started-with-Azure-OpenAI-Service/AI-Foundry-Portal/page

Overview of Azure AI Foundry Portal for discovering, deploying, customizing, and testing generative AI models and workflows including chat, images, audio, embeddings, and fine-tuning.

AI Foundry Portal is the centralized web workspace for the Azure OpenAI service. This portal unifies tools to discover, test, customize, and deploy generative AI models—letting teams iterate quickly without building complex infrastructure. In this lesson you'll learn what the portal provides, how its main areas are organized, and where to start when evaluating models for chat, images, audio, embeddings, and fine-tuning.

Access the portal at [ai.azure.com](https://ai.azure.com) to browse the model catalog, provision deployments, run interactive playgrounds, connect models to applications, and monitor usage.

<Callout icon="lightbulb">
  You need an Azure subscription and appropriate permissions to access models and create deployments in the portal. Check with your Azure administrator if you cannot see the resources described here.
</Callout>

## Key capabilities at a glance

The Foundry Portal focuses on three core capabilities that support the model lifecycle:

* Model management: Browse, deploy, and manage foundation models and deployment configurations via a GUI.
* Integration: Connect models to Azure services and external data sources for tasks like document summarization, search, or API-driven automation.
* Customization: Fine-tune or adapt foundation models with your own domain data to align outputs with your organization’s tone and requirements.

Interactive playgrounds let you rapidly prototype: chat and assistant experiences, image generation (DALL·E), audio and transcription, completion tasks for summaries and code, embeddings for semantic search, and fine-tuning experiments.

Below is a concise overview of common generative model families you will find in the Foundry model catalog.

<Frame>
  <img alt="A presentation slide titled &#x22;Types of Generative AI Model&#x22; showing a two-column table. The left column lists model families (Base GPT, Multimodal AI, Vector Embeddings, Image Generation) and the right column provides short descriptions of each." />
</Frame>

## Model families — when to use each

Use the table below to quickly match a model family to common tasks and example models. This helps you pick the right family when evaluating options in the Model Catalog.

| Model Type        | Use Case                                                                         | Example Models                                 |
| ----------------- | -------------------------------------------------------------------------------- | ---------------------------------------------- |
| Base GPT          | Conversational agents, content generation, summarization, code generation        | GPT-4, GPT-4o-mini, GPT-3.5                    |
| Multimodal AI     | Transcription, audio processing, multi-input tasks combining text, images, audio | Whisper, multimodal GPT variants               |
| Vector embeddings | Semantic search, similarity, clustering, recommendation systems                  | Embeddings families (text-embedding-\* models) |
| Image generation  | Generate images from text prompts for UIs, marketing, or creative workflows      | DALL·E family                                  |

Model catalog highlights:

* Base-GPT: Chat-focused models for conversational agents and creative content.
* Multimodal: Models that understand or combine text, audio, and images.
* Vector embeddings: Encoded representations for search and retrieval.
* Image generation: Text-to-image models accessible through REST APIs.

## Exploring the portal UI

When you open the Foundry Portal and navigate to Playgrounds or Chat, you may see a "deployment needed" prompt if no deployment exists for the selected model. From that prompt you can create a deployment, configure options, and then test the model in playgrounds (chat, assistant, images, audio, completions, or fine-tuning).

<Frame>
  <img alt="A screenshot of the Azure AI &#x22;Chat playground&#x22; web interface in dark mode. The main panel shows a &#x22;Deployment needed&#x22; message with a folder icon and a &#x22;Create a deployment&#x22; button, plus a left navigation menu and an empty preview area." />
</Frame>

You do not need to create a deployment immediately—deployment creation and lifecycle management are covered later. For now, take note of the left navigation (Playgrounds, Model catalog, Tools, Shared resources) and the available playground types:

* Chat and Assistant: Build conversational experiences and multi-turn flows.
* Image generation: Generate visuals from prompts (DALL·E).
* Audio & transcription: Convert speech to text or synthesize audio.
* Completions & code: One-shot or streaming completions for text and code tasks.
* Fine-tuning & evaluation: Train and evaluate models against your dataset.
* Admin: Quota, safety & security settings, data files, and vector stores.

## Model Catalog — discover and compare models

The Model Catalog is a curated listing of available models and families. Use it to compare capabilities, supported modalities, and recommended use cases before choosing a model for a deployment.

<Frame>
  <img alt="A dark‑theme screenshot of the Azure AI Model Catalog in a browser, showing a grid of model tiles (gpt-4, gpt-4o-mini, gpt-3.5, DALL·E, Whisper, embeddings, etc.). The left sidebar shows navigation items like Model catalog, Playgrounds, Tools and Shared resources." />
</Frame>

When evaluating models, consider:

* Latency and cost profile (use smaller variants like GPT-4o-mini for interactive or lower-cost needs).
* Modality support (text-only vs. multimodal vs. audio).
* Fine-tuning and embedding support for search or retrieval augmentation.
* Safety and data handling configuration available in the portal’s admin settings.

## Next steps

* Browse the Model Catalog to identify the model family that fits your use case.
* Create a deployment and try the appropriate playground (chat, assistant, image, or audio) to validate model behavior interactively.
* Learn how to fine-tune models with your data and how to integrate deployments into applications using SDKs or REST APIs.
* Refer to Azure OpenAI documentation for detailed guides and API references: [Azure AI Documentation](https://learn.microsoft.com/azure/ai-services/).

Further reading and resources:

* [Azure OpenAI Service overview](https://learn.microsoft.com/azure/ai-services/openai/)
* [AI Studio / Foundry Portal (ai.azure.com)](https://ai.azure.com)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/f28c5dfe-9fe8-486d-bc61-eade55096b1c/lesson/a802875f-26eb-4e98-8c85-963f6cb3a151" />
</CardGroup>
