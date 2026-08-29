# Example using the OpenAI Python client configured for Azure OpenAI
# Install: pip install openai (or the appropriate OpenAI SDK)
import os
from openai import OpenAI

# Set these environment variables or replace with your values
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_BASE = os.getenv("AZURE_OPENAI_API_BASE")  # e.g., "https://<your-resource-name>.openai.azure.com/"
AZURE_OPENAI_API_VERSION = "2025-01-01-preview"  # ensure this matches a supported API version for your deployment
DEPLOYMENT_NAME = "your-deployment-name"  # the Azure deployment (model alias) name

client = OpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_base=AZURE_OPENAI_API_BASE,
    api_type="azure",
    api_version=AZURE_OPENAI_API_VERSION
)

messages = [
    {"role": "system", "content": "You are a travel planner that helps people plan trips."},
    {"role": "user", "content": "Plan a 10-day trip to Scotland"}
]

response = client.chat.completions.create(
    model=DEPLOYMENT_NAME,
    messages=messages,
    max_tokens=800,
    temperature=0.7,
    top_p=0.95,
)

# Print the top choice's message content
print(response.choices[0].message.content)
```

> **warning** Keep secrets out of source control. Use environment variables, Azure Key Vault, or managed identities for authentication. Also confirm the AZURE\_OPENAI\_API\_VERSION is supported for your deployment to avoid runtime errors.

Notes and best practices:

* Replace AZURE\_OPENAI\_API\_BASE, AZURE\_OPENAI\_API\_KEY, and DEPLOYMENT\_NAME with your actual Azure values.
* If you prefer Microsoft’s Azure SDK, see the azure.ai.openai package samples in the Azure docs and use AzureKeyCredential or managed identity for authentication: [https://learn.microsoft.com/azure/cognitive-services/openai/](https://learn.microsoft.com/azure/cognitive-services/openai/)
* Tune parameters such as max\_tokens, temperature, and top\_p to control response length and creativity.
* Use system messages to set behavior (role, tone, constraints) and include examples or templates for predictable formatting.
* Test prompts in the playground with representative inputs and edge cases before deploying.

## Links and references

* Azure OpenAI Service documentation: [https://learn.microsoft.com/azure/cognitive-services/openai/](https://learn.microsoft.com/azure/cognitive-services/openai/)
* OpenAI Python client: [https://pypi.org/project/openai/](https://pypi.org/project/openai/)

Azure OpenAI Studio’s Chat Playground simplifies prompt experimentation, iterative tuning, and behavior validation. With these techniques, you can design effective prompts, test completions, and prepare models for integration into applications. The next topic will show how to integrate OpenAI into an application and call the API programmatically.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/f28c5dfe-9fe8-486d-bc61-eade55096b1c/lesson/89a00472-29cb-45b1-aba4-44320e56eb82)


# What Is Generative AI

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Get-Started-with-Azure-OpenAI-Service/What-Is-Generative-AI/page

Overview of generative AI, its evolution, key model types, applications, capabilities, risks, and responsible deployment practices

Generative AI refers to a class of artificial intelligence systems that create new content—text, images, audio, code, or other media—by learning the underlying patterns of existing data. In this lesson you'll learn what generative AI means, how it evolved from earlier AI techniques, and why it’s reshaping creative and productivity workflows today.

We’ll start with a concise timeline showing how AI has progressed over time.

* 1950s — Classical AI: rule-based systems and symbolic reasoning intended to encode expert knowledge explicitly.
* 1990s — Machine Learning: statistical methods that learn patterns and relationships from data rather than relying solely on hand-coded rules.
* 2010s — Deep Learning: multilayer neural networks that learn hierarchical features from very large datasets, enabling breakthroughs in vision, speech, and language.
* 2020s — Generative AI: models that synthesize novel content (text, images, audio, code) by learning the distribution of training data and sampling from it.

<Frame>
  <img alt="A slide titled &#x22;What is Generative AI?&#x22; showing an evolutionary timeline of silhouettes from Artificial Intelligence (1950s) to Machine Learning (1990s), Deep Learning (2010s), and Generative AI (2020s). It also includes a brief definition noting machine learning is a subset of AI that learns from data to make decisions or predictions." />
</Frame>

Deep learning, which rose to prominence in the 2010s, uses deep neural networks to process vast datasets and learn complex representations. These networks power image recognition, speech recognition, translation, and other applications that require understanding high-dimensional data.

How generative AI differs

* Traditional ML models are often discriminative: they classify or predict a label for input data (for example, "spam" vs "not spam").
* Generative models learn an approximation of the full data distribution and can sample from that distribution to produce entirely new examples that resemble the training data.

Common classes of generative models

* Variational Autoencoders (VAEs): learn latent representations and generate samples by decoding from the latent space.
* Generative Adversarial Networks (GANs): use a generator and discriminator in competition to produce highly realistic images and other media.
* Transformer-based models and Large Language Models (LLMs): use attention mechanisms and massive training corpora to generate coherent text and support tasks like summarization, translation, and code generation.

> **lightbulb** Generative models approximate the data distribution and produce novel—but statistically plausible—outputs when sampling from that learned distribution. This enables creation of new images, text, audio, or code that resemble the training examples.

Practical examples and popular tools

* ChatGPT — conversational text generation and assistants. [OpenAI ChatGPT](https://openai.com/chatgpt)
* DALL·E — image synthesis from text prompts. [DALL·E](https://openai.com/dall-e)
* GitHub Copilot — AI-assisted code completion and generation. [GitHub Copilot](https://github.com/features/copilot)

Key capabilities enabled by generative AI

* Content creation: synthetic images, text drafts, music, and video.
* Code generation and automation: boilerplate, function suggestions, and auto-completion.
* Data augmentation: generating synthetic examples for training or simulation.
* Personalization: adapting content to user preferences at scale.

Risks and best practices
Generative AI can produce realistic outputs that are fluent and persuasive, but important risks remain:

* Hallucinations: models may assert incorrect facts as if they are true.
* Biases: models can reproduce or amplify biases in their training data.
* Copyright and provenance: generated content may inadvertently reproduce copyrighted material.
  Careful validation, human-in-the-loop review, and responsible deployment are essential.

> **warning** Generative AI is powerful but not infallible. Outputs can be factually incorrect, biased, or inappropriate—always validate and apply safeguards before using generated content in critical or public contexts.

Quick reference table

| Era                      | Characteristic                               | Typical techniques               |
| ------------------------ | -------------------------------------------- | -------------------------------- |
| 1950s — Classical AI     | Rule-based, symbolic reasoning               | Expert systems, logic-based AI   |
| 1990s — Machine Learning | Statistical pattern learning                 | SVMs, decision trees, clustering |
| 2010s — Deep Learning    | Learned hierarchical features                | CNNs, RNNs, deep neural networks |
| 2020s — Generative AI    | Content synthesis from learned distributions | VAEs, GANs, Transformers / LLMs  |

Further reading and references

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (general reference)
* [OpenAI Documentation](https://platform.openai.com/docs/)
* [Transformer Models and Attention Mechanisms](https://arxiv.org/abs/1706.03762) (Vaswani et al.)

This overview gives you the conceptual timeline and technical distinctions needed to understand why generative AI is a transformative area of modern AI research and product development.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/f28c5dfe-9fe8-486d-bc61-eade55096b1c/lesson/c9ee803d-7fb7-4e8a-993c-188130800450)
