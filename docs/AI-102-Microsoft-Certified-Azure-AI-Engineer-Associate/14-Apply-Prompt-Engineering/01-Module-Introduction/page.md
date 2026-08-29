# Module Introduction

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Apply-Prompt-Engineering/Module-Introduction/page

Guide to prompt engineering for Azure OpenAI covering prompt design, endpoint differences, advanced techniques, safety, testing, and deploying reliable controllable AI outputs.

Applying prompt engineering

This module builds on techniques for integrating Azure OpenAI via REST APIs and SDKs and focuses on prompt engineering: the practice of crafting inputs that produce reliable, relevant, and controllable outputs from AI models. Prompt engineering helps you reduce unexpected responses, increase accuracy, and align model outputs with application requirements.

In this lesson we will:

* Define prompt engineering and explain its importance for production systems.
* Show how to design prompts tailored to different endpoints (for example, completions vs. chat).
* Explore advanced techniques to improve consistency, accuracy, and safety of model responses and how to apply them in real applications.

<Frame>
  <img alt="A presentation slide titled &#x22;Learning Objectives&#x22; with three numbered points: 01 Defining Prompt Engineering, 02 Optimizing for different Endpoints, and 03 Exploring advanced techniques." />
</Frame>

What you'll gain from this module

* Practical strategies to convert user intent into structured prompts.
* How to select and adapt prompts depending on whether you call completion, chat, or function-calling endpoints.
* Methods to increase output determinism (temperature & sampling strategies), enforce format constraints, and apply guardrails for safety and compliance.

| Learning Objective        | Why it matters                                                          | Example outcome                                                |
| ------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------- |
| Define prompt engineering | Establishes a repeatable process for creating effective inputs          | Clear, testable prompt templates                               |
| Optimize for endpoints    | Different endpoints expect different input formats and context handling | Correct use of `messages` for chat vs `prompt` for completions |
| Apply advanced techniques | Improve model reliability, reduce hallucination, and enforce structure  | Higher fidelity JSON outputs and safer responses               |

> **lightbulb** Prompt engineering is both art and engineering: iterate with small, measurable changes (e.g., tweak temperature, add examples, constrain formats) and validate outputs with automated tests before deploying.

Key topics covered (high-level)

* Prompt structure and components: system instructions, user instructions, examples, and constraints.
* Endpoint considerations: completions vs. chat — when to use each and how to format prompts.
* Advanced prompt patterns: few-shot examples, chain-of-thought prompting, step-by-step decomposition, and output validation.
* Safety and control: using instructions, post-processing, and automated checks to reduce harmful or incorrect outputs.
* Testing & monitoring: QA approaches to ensure prompt changes don’t degrade performance in production.

Recommended reading and references

* [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/cognitive-services/openai/) — official guidance on endpoints, SDKs, and deployment.
* [Prompting best practices — OpenAI](https://platform.openai.com/docs/guides/prompting) — general prompt design techniques.
* [Responsible AI and safety guidelines](https://learn.microsoft.com/azure/ai-responsible-ai/) — principles for building safe AI applications.

> **warning** Always validate generation outputs against concrete requirements (format, factuality, safety). Small prompt changes can substantially alter model behavior — use automated tests and monitoring before pushing updates to production.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/d00afd7f-6d8d-4be7-a3f1-5523f484ea72/lesson/27939164-af9f-43e4-bd5f-ff4e91a3fa11)
