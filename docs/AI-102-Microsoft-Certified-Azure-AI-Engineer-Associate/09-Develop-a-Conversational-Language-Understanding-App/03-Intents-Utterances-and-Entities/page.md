# Intents Utterances and Entities

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Develop-a-Conversational-Language-Understanding-App/Intents-Utterances-and-Entities/page

Describes intents, utterances, and entities in conversational AI and guidance for designing intent classification and entity extraction to build reliable NLU systems

Intents, utterances, and entities are the three foundational building blocks of conversational language understanding systems. Understanding how they work together helps you design accurate intent classification and reliable entity extraction pipelines for chatbots, virtual assistants, and other conversational applications.

* Keywords: intents, utterances, entities, conversational AI, natural language understanding (NLU), entity extraction, intent classification, slot filling.

## What is an utterance?

An utterance is the raw piece of natural language input a user speaks or types to your application. It can be a question, command, or statement.

Examples of utterances:

* "What's the weather like tomorrow?"
* "Turn on the bedroom light."
* "Set the heater to 25 degrees Celsius."

## What is an intent?

An intent represents the user's goal or purpose behind an utterance—the action the user wants the system to perform. Correct intent classification tells your system which flow, API call, or response to trigger.

Example intents:

* `GetWeather` — user requests weather information
* `TurnOnDevice` — user issues a device activation command
* `AdjustDevice` — user requests a device setting change

Mapping utterances to intents is the primary routing mechanism in an NLU system.

## What is an entity?

Entities are structured, named data extracted from an utterance that provide context for an intent. Entities (also called slots) make responses precise and actionable.

Examples:

* Utterance: "What time is it in Paris?" → Intent: `GetTime`, Entity: `Location = Paris`
* Utterance: "Will it rain tomorrow?" → Intent: `GetWeather`, Entity: `Time = tomorrow`
* Utterance: "Set the heater to 25 degrees Celsius." → Intent: `AdjustDevice`, Entities: `Device = heater`, `Value = 25°C`

<Frame>
  <img alt="A slide titled &#x22;Utterances, Intents, and Entities in Language Models&#x22; showing three labeled panels: 01 Utterances (&#x22;what users say in natural language&#x22;), 02 Intents (&#x22;the purpose or action behind an utterance&#x22;), and 03 Entities (&#x22;extract details from user input, making AI responses more precise&#x22;)." />
</Frame>

## Quick reference table: utterances → intents → entities

| Utterance                               | Likely Intent | Extracted Entity Example          |
| --------------------------------------- | ------------- | --------------------------------- |
| "What's the weather like tomorrow?"     | GetWeather    | Time = `tomorrow`                 |
| "What time is it in Paris?"             | GetTime       | Location = `Paris`                |
| "Turn on the bedroom light."            | TurnOnDevice  | Device = `bedroom light`          |
| "Set the heater to 25 degrees Celsius." | AdjustDevice  | Device = `heater`, Value = `25°C` |

## Pre-built entity types and why they matter

Many platforms (including Azure Language services) provide pre-built entity extractors that recognize common data types without custom training. These speed up development and improve accuracy for standard patterns.

> **lightbulb** Pre-built entity extractors accelerate development by automatically detecting common data formats—numbers, dates, emails, phone numbers, and URLs—so you can focus training on domain-specific entities.

Common pre-built entity types and examples:

| Entity Type     | Use Case                          | Example                                                                               |
| --------------- | --------------------------------- | ------------------------------------------------------------------------------------- |
| Quantities      | Percentages, counts, measures     | "Increase brightness to 50%" → Quantity = `50%`                                       |
| Date & Time     | Absolute and relative expressions | "Remind me tomorrow at 7 p.m." → DateTime = `tomorrow at 7 p.m.`                      |
| Email Addresses | Contact extraction                | "Contact me at [user@domain.com](mailto:user@domain.com)" → Email = `user@domain.com` |
| Phone Numbers   | Local and international formats   | "Call +1 234 567 8900" → PhoneNumber = `+1 234 567 8900`                              |
| URLs            | Web addresses in text             | "Check out [https://example.com](https://example.com)" → URL = `https://example.com`  |

<Frame>
  <img alt="A presentation slide titled &#x22;Prebuilt Entity Components&#x22; containing three boxed panels. They list &#x22;Quantities&#x22; (numerical values), &#x22;Date and Time&#x22; (specific and relative times), and &#x22;Email Addresses,&#x22; each with a simple icon." />
</Frame>

## Tips for designing intents and entities

* Keep intents focused and action-oriented (e.g., `GetWeather`, `BookFlight`, `AdjustDevice`).
* Design entities as the minimal pieces of context needed to fulfill the intent (e.g., `Location`, `Time`, `Device`, `Value`).
* Use pre-built entities where applicable and reserve custom entities for domain-specific concepts.
* Provide diverse utterance examples during training to cover synonyms, colloquialisms, and different phrasing.

> **warning** Ambiguous utterances can lead to incorrect routing or extraction. Add disambiguation prompts in your dialog flow (e.g., "Do you mean Paris, France or Paris, Texas?") and validate critical entities before taking irreversible actions.

## Where to learn more

* Azure Language Understanding docs: [https://learn.microsoft.com/azure/cognitive-services/language-service/](https://learn.microsoft.com/azure/cognitive-services/language-service/)
* General NLU concepts: [https://en.wikipedia.org/wiki/Natural\_language\_understanding](https://en.wikipedia.org/wiki/Natural_language_understanding)
* Best practices for building conversational AI: search for "intent classification and entity extraction" in developer documentation and platform-specific guides

By combining clearly defined intents, well-scoped entities, and representative utterances—while leveraging pre-built extractors where suitable—you can significantly improve both the accuracy and usability of your conversational applications.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/3b91e872-14ae-4fc5-bdad-5c0927439d61/lesson/fac52baf-21bb-4109-bee1-c38390a29650)
