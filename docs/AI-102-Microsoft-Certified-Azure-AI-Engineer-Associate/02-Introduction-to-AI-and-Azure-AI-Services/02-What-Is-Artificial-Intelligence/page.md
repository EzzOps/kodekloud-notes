# What Is Artificial Intelligence

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Introduction-to-AI-and-Azure-AI-Services/What-Is-Artificial-Intelligence/page

Overview of artificial intelligence concepts, applications, developer skills, and responsible governance for building and deploying AI-powered systems.

Artificial intelligence (AI) is the practice of building software that mimics, augments, or automates human capabilities. Historically tasks like translating a sentence required a human translator—an approach that could be slow or expensive for rare languages or urgent needs. Modern AI systems automate translation, speech recognition, image text extraction, and many other tasks quickly and at scale.

Everyday AI examples:

* [Google Translate](https://translate.google.com) — translate pasted text, spoken words, or text captured from images.
* [Microsoft Copilot](https://www.microsoft.com/en-us/microsoft-365/copilot) — helps write emails, summarize documents, and generate Excel formulas from plain-English instructions.
* [GitHub Copilot](https://github.com/features/copilot) — suggests code while developers type.
* [ChatGPT](https://chat.openai.com/) — generates ideas, drafts content, and explains complex topics.
* [Google Lens](https://lens.google/) — recognizes objects and extracts or translates text from images.

<Frame>
  <img alt="A slide titled &#x22;What is Artificial Intelligence?&#x22; showing four AI tools—Microsoft Copilot, GitHub Copilot, ChatGPT, and Google Lens—with brief descriptions of their purposes (email/office assistant, coding assistant, chat/research assistant, and image/text identification)." />
</Frame>

AI powers these capabilities by combining models, data, and software interfaces so applications can perform tasks that previously required human judgment or effort.

> **lightbulb** AI enables faster, more accessible communication and automation—reducing manual effort for translation, transcription, image understanding, and conversational assistance.

## Core AI capability areas

AI systems typically focus on one or more capability areas. The table below summarizes common capability categories, their purpose, and example uses.

|                  Capability | What it does                                           | Real-world examples                                    |
| --------------------------: | ------------------------------------------------------ | ------------------------------------------------------ |
|           Visual perception | Detects and interprets visual information              | Object detection, OCR (text in images), face detection |
|               Text analysis | Processes and understands written language             | Summarization, translation, sentiment analysis         |
|          Conversation (NLP) | Engages through natural language                       | Virtual assistants, chatbots, conversational search    |
| Decision making & analytics | Makes recommendations or automated decisions from data | Recommender systems, anomaly detection, forecasting    |

Note: some applications combine multiple capabilities (for example, an app that recognizes a product from an image and then answers user questions about it).

> **warning** Some inferences—such as attempting to read emotions from facial expressions—are unreliable and ethically contentious. Design AI systems with care to avoid harm, bias, or false confidence.

## Skills software engineers need to work with AI

Working with AI in production requires both software engineering practices and conceptual understanding of models. Below is a practical breakdown you can use to evaluate or plan skill development.

| Skill category                  | Key details                                                                  | Why it matters                                                               |
| ------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Programming & integration       | Python, C#, JavaScript; using REST APIs and SDKs to call models and services | Enables building applications that call hosted models or embed ML components |
| DevOps & production engineering | Version control (Git), CI/CD, automated testing, monitoring                  | Ensures reliable deployments and observability for AI-enabled features       |
| Model lifecycle                 | Training, evaluating, deploying, updating models (even with prebuilt models) | Manages model quality and adapts to data drift or new requirements           |
| Model interpretation            | Understanding probability scores, confidence, and failure modes              | Helps users trust outputs and supports responsible decision-making           |
| Responsible AI practices        | Fairness, transparency, privacy, and governance                              | Reduces risk of bias, legal exposure, and user harm                          |

For example, practical learning paths cover how to start from a base model, deploy it, integrate it with an application via APIs or SDKs, and manage it in production. These are hands-on skills you’ll use to integrate AI responsibly into real systems.

<Frame>
  <img alt="A presentation slide titled &#x22;AI Skills for Software Engineers&#x22; showing two boxed lists: Technical Skills (programming in Python/C#/JavaScript, API/SDK integration, DevOps/CICD) on the left and AI Concepts & Principles (training/deploying models, interpreting predictions, ethical AI) on the right, with a central icon of a person wearing a hard hat on a computer screen." />
</Frame>

## Responsible AI & governance

Responsible AI is a cross-cutting requirement for production systems. Consider fairness, transparency, privacy, and accountability from design through deployment:

* Evaluate datasets for bias and representativeness.
* Expose confidence and limitations of model outputs to users.
* Log model decisions and monitor performance in production.
* Apply privacy-preserving techniques when handling sensitive data.

> **warning** Always test AI systems for failure modes and biased behavior before deployment. Ethical reviews and governance policies should be part of your release checklist.

## Links and references

* [Google Translate](https://translate.google.com) — translation and image text recognition
* [Microsoft Copilot](https://www.microsoft.com/en-us/microsoft-365/copilot) — productivity assistant
* [GitHub Copilot](https://github.com/features/copilot) — code completion and suggestions
* [ChatGPT](https://chat.openai.com/) — conversational AI and content generation
* [Google Lens](https://lens.google/) — image recognition and text extraction

These resources and concepts give you a foundation for understanding what AI is, how it’s applied in real products, and the practical skills required to build and govern AI-enabled systems.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/608629a7-1574-4eb2-95a4-f026fc8888b2/lesson/c94dcf21-9252-4dad-9691-a334c0643470)
