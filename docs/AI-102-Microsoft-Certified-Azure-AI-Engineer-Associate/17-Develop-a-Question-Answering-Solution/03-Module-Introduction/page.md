# Module Introduction

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Develop-a-Question-Answering-Solution/Module-Introduction/page

Guide to building and maintaining a question answering knowledge base with Azure AI Language, covering ingestion, multi-turn context, ranking, publishing, security, and active learning

Develop a question-answering (QA) solution with Azure AI Language.

In this lesson you'll learn how to build an automated QA system that provides precise, context-aware answers from semi-structured sources such as FAQs, manuals, and document collections. Azure AI Language uses natural language processing to extract concise answers and rank multiple candidate responses so your application can surface the most relevant information.

<Callout icon="lightbulb">
  Question answering (QA) is optimized for retrieving factual answers from documents. It's ideal for scenarios like knowledge bases, product documentation, and support FAQs where users expect direct, concise responses.
</Callout>

<Frame>
  <img alt="A presentation slide titled &#x22;Learning Objectives&#x22; that lists three goals: understand question answering in Azure AI Language, differentiate between question answering and conversational AI, and build a knowledge base. The slide has numbered blue markers along a vertical line and a dark left sidebar." />
</Frame>

Key topics covered in this module:

* What question answering (QA) is and how Azure AI Language implements it.
* Differences between QA and conversational AI systems.
* How to construct, test, publish, and maintain a knowledge base.
* Adding multi-turn (contextual) support and implementing active learning for continuous improvement.

## QA vs Conversational AI

Understanding the differences helps you choose the right architecture.

|       Capability | Question Answering                                   | Conversational AI (Dialog)                              |
| ---------------: | ---------------------------------------------------- | ------------------------------------------------------- |
|     Primary goal | Retrieve factual answers from documents              | Manage interactive dialogues and tasks                  |
|         Best for | FAQs, manuals, knowledge bases                       | Virtual assistants, task flows, open-ended chat         |
| Context handling | Typically query → answer; can add multi-turn context | Designed for turn-taking, slot-filling, complex context |
|  Success metrics | Answer precision and coverage                        | Task completion, user satisfaction, conversation flow   |

## Build a Knowledge Base — Step-by-step

Follow these high-level steps to create a robust QA solution:

1. Collect and prepare sources
   * Gather FAQs, manuals, support docs, and structured Q\&A pairs.
   * Clean or redact sensitive data (PII) before ingestion.
2. Ingest content into the knowledge base
   * Upload documents and define metadata to improve retrieval.
   * Use embeddings and semantic ranking where available.
3. Configure retrieval and scoring
   * Tune retrieval parameters (top-K, similarity thresholds).
   * Adjust answer ranking and confidence thresholds.
4. Enable multi-turn context
   * Store conversational history and link follow-up queries to prior turns.
   * Use context-aware retrieval to resolve pronouns and references.
5. Test, refine, and iterate
   * Preview responses, inspect low-confidence answers, and refine sources.
   * Update or split documents, add canonical Q\&A pairs, and republish.

Testing and refinement are crucial: iterate on source quality, tune scoring, and improve phrasing to reduce ambiguity and increase answer relevance.

## Multi-turn Conversations

Multi-turn capabilities allow the QA system to maintain context across follow-up questions. Implement context windows that include a configurable number of prior turns (queries and answers), then:

* Use context to re-run retrieval with augmented prompts.
* Resolve referents (e.g., “it”, “that”) by including prior user utterances.
* Limit context length to manage latency and cost.

## Publish and Integrate

When your knowledge base is polished:

* Publish it to generate REST endpoints and API keys or use SDKs for your preferred language.
* Secure access with proper authentication, role-based access, and key rotation.
* Integrate the published KB into web apps, mobile apps, or bots using the provided endpoints.

<Callout icon="warning">
  When publishing and exposing a knowledge base, ensure sensitive or personally identifiable information (PII) is removed or handled according to your organization’s data policies. Review access controls and rotate keys as needed.
</Callout>

<Frame>
  <img alt="A presentation slide titled &#x22;Learning Objectives&#x22; with a dark left panel and a light right background. It lists three numbered items: &#x22;05 Test and deploy a knowledge base,&#x22; &#x22;06 Utilize a published knowledge base,&#x22; and &#x22;07 Implement active learning.&#x22;" />
</Frame>

## Active Learning and Continuous Improvement

Active learning closes the loop between real user behavior and knowledge base updates:

* Capture telemetry: log low-confidence answers, unanswered queries, and user feedback.
* Human-in-the-loop review: surface candidate queries for content authors to review and label.
* Update sources: add new Q\&A pairs, rephrase answers, or include additional document excerpts.
* Republish: push updates and continue monitoring performance.

A regular cadence of telemetry analysis plus human review ensures your QA system stays current and accurate.

## Links and References

* [Azure AI Language Documentation](https://learn.microsoft.com/azure/ai-services/language/)
* [Designing effective knowledge bases](https://learn.microsoft.com/azure/ai-services/language/question-answering/overview)
* [Best practices for securing Azure resources](https://learn.microsoft.com/azure/security/)

| Resource Type | Use Case                     | Example                                                                                                               |
| ------------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Documentation | Learn core concepts and APIs | [Azure AI Language](https://learn.microsoft.com/azure/ai-services/language/)                                          |
| Tutorials     | Step-by-step KB creation     | [Question Answering quickstart](https://learn.microsoft.com/azure/ai-services/language/question-answering/quickstart) |
| Security      | Keys, roles, and policies    | [Azure security best practices](https://learn.microsoft.com/azure/security/)                                          |

By the end of this module you should be able to design, build, publish, and maintain a question-answering knowledge base using Azure AI Language, with strategies for multi-turn context and active learning to keep answers accurate over time.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/f55ce98d-afd9-45b6-8f51-9668bad8705d/lesson/2a903f24-5bfc-4770-9401-a65b0cd6dedd" />
</CardGroup>
