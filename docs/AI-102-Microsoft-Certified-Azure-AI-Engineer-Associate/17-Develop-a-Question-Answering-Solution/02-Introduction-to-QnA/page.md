# Introduction to QnA

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Develop-a-Question-Answering-Solution/Introduction-to-QnA/page

Explains QnA systems and knowledge bases, contrasts static answers with dynamic language understanding, and guides building, testing, publishing, and integrating KBs via APIs and SDKs.

In this lesson, we’ll explain how Question Answering (QnA) systems let AI answer user questions using structured information sources such as knowledge bases. You’ll learn the architecture, the difference between static QnA and dynamic language understanding, and practical steps to create, test, and publish a knowledge base for production use.

Imagine a common scenario for a bank customer asking questions like:

* How do I reset my net banking password?
* What is the interest rate for savings accounts?
* How do I block a lost debit card?

A QnA system can automatically return accurate, prewritten answers to these queries by searching a curated knowledge base that contains help documents, FAQs, and policy guides. This structured content is what the QnA engine searches to find the best match and deliver the response.

<Frame>
  <img alt="A diagram titled &#x22;Introduction to Q&A&#x22; showing a chat app asking &#x22;What's the weather?&#x22; and receiving &#x22;It's 22°C.&#x22; The question is sent via an SDK/REST API to a knowledge base (KB) that stores the question–answer pair." />
</Frame>

APIs and SDKs enable developers to integrate QnA capabilities into mobile apps, chatbots, and web forms. SDKs (available in multiple languages) abstract away HTTP details and let you focus on designing a great user experience instead of low-level plumbing.

## How a QnA flow typically works

1. User submits a natural-language question via app, website, or chatbot.
2. The client sends the query to a QnA endpoint (REST API or SDK).
3. The QnA service searches the knowledge base for matching Q\&A entries.
4. The service returns the best matched answer, often with a confidence score.
5. The client displays the answer; fallback logic handles low-confidence cases.

## Question Answering vs Language Understanding

It’s important to distinguish a traditional QnA system from more general language-understanding solutions. The primary difference is whether responses are static (prewritten and stored) or dynamically generated based on intent, context, and live data.

| Aspect                 | Static QnA (Knowledge Base)                                      | Dynamic Language Understanding                                                            |
| ---------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Response type          | Prewritten answers stored in KB                                  | Generated responses using models + live data                                              |
| When to use            | FAQ, policy, onboarding, repetitive queries                      | Personalized recommendations, real-time data, complex reasoning                           |
| Speed & predictability | Fast and predictable                                             | More flexible but may be slower/less predictable                                          |
| Example                | “How do I reset my password?” → stored reset instructions + link | “Should I take an umbrella today?” → detect intent, call weather API, reply with forecast |

Example flows:

* Static QnA: User asks “How do I reset my password?” The system matches the question to a stored Q\&A pair and returns the prewritten answer with a reset link.
* Dynamic language understanding: User asks “Should I take an umbrella today?” The system detects the intent (“weather forecast”), extracts the location (e.g., “New York”), calls a weather API, and generates a context-aware response.

<Frame>
  <img alt="A diagram titled &#x22;Question Answering vs Language Understanding&#x22; showing a chat example where a user asks &#x22;Should I take an umbrella today?&#x22; and the system replies &#x22;No need for an umbrella. The forecast shows clear skies in New York.&#x22; To the right is a flowchart showing steps: system detects intent, extracts location (&#x22;New York&#x22;), and checks real-time weather conditions." />
</Frame>

Language understanding and QnA are complementary. Use the knowledge base for authoritative, static answers and use intent/entity extraction plus APIs for personalized, real-time responses.

## Creating a Knowledge Base

A well-structured knowledge base is the heart of an effective QnA system. Building one typically follows these four steps:

1. Set up resources
   * Deploy a language service (for example, Azure AI Language Services) in your cloud account to provide QnA and language capabilities.
2. Initialize a project
   * Use a management tool like Language Studio to create a new QnA project. Language Studio provides a no-code, web-based UI for managing QnA content.
3. Populate the knowledge base
   * Import FAQs, upload PDFs and text documents, and add chit-chat/fallback phrases for conversational behavior.
4. Refine content
   * Edit responses, add alternative phrasings, and align tone with your brand for clarity and consistency.

Best practices for KB entries:

| Content Type      | Purpose                           | Example                                     |
| ----------------- | --------------------------------- | ------------------------------------------- |
| FAQ pair          | Direct answers to common queries  | "How to reset password" → steps + link      |
| Document excerpts | Longer policy excerpts or guides  | Banking fees PDF sections                   |
| Chit-chat         | Friendly fallbacks for small talk | "Thanks for your help!" → "You're welcome!" |

<Frame>
  <img alt="A four-step flowchart titled &#x22;Creating a Knowledge Base&#x22; showing: 1) Set up resource (Deploy Azure AI Language Service), 2) Initialize project (Open Language Studio & create a project), 3) Populate the knowledge base (import FAQs, upload documents, chit‑chat integration), and 4) Refine content (edit & enhance responses)." />
</Frame>

Keep answers concise and aligned to your brand voice. Use clear titles and tags to make QnA entries easy to search and maintain.

## Testing and Publishing Your Knowledge Base

Testing and monitoring ensure your knowledge base behaves correctly in production. Key validation tasks include:

* Evaluate confidence scores: Every returned candidate can include a confidence score. Use these scores to determine when to accept the top answer, show multiple options, ask a clarifying question, or escalate to a human agent.
* Add alternative phrasings: Users ask the same question in many ways. Add synonyms and alternate wordings to improve recall and retrieval accuracy.

<Frame>
  <img alt="A slide titled &#x22;Testing a Knowledge Base&#x22; with two dark rounded panels. The left panel reads &#x22;Evaluate Confidence Scores&#x22; (inspect responses and confidence levels for accuracy) and the right reads &#x22;Refine with Alternative Phrases&#x22; (adjust phrases to improve model responses)." />
</Frame>

<Callout icon="lightbulb">
  Monitor confidence thresholds and design fallback behavior (for example: ask a clarifying question or route to a human agent) when scores are low.
</Callout>

Publishing makes your knowledge base available for integration:

* Generate a REST API endpoint so applications can query the knowledge base over HTTP.
* Enable SDK compatibility — Azure and other providers supply SDKs in multiple languages to speed integration and reduce boilerplate code.

<Frame>
  <img alt="A presentation slide titled &#x22;Publishing a Knowledge Base&#x22; showing two dark panels. The panels list &#x22;Generate REST API Endpoint&#x22; (provides an HTTP-based interface for application integration) and &#x22;Enable SDK Compatibility&#x22; (allows seamless integration with various programming environments)." />
</Frame>

After publishing, integrate the service into your chatbot, mobile app, or web form and continuously monitor logs and user feedback to refine answers, update content, and adjust confidence thresholds.

## Links and References

* [Azure AI Language Services](https://learn.microsoft.com/azure/cognitive-services/language-service/)
* [Language Studio (Azure)](https://learn.microsoft.com/azure/cognitive-services/language-service/language-studio-overview)
* [Designing conversational FAQ systems — best practices](https://learn.microsoft.com/azure/ai-services/qna-maker/overview)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/f55ce98d-afd9-45b6-8f51-9668bad8705d/lesson/00b9392d-089f-4de9-a6d3-53f7dec78b51" />
</CardGroup>
