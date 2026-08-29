# Using System Messages

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Apply-Prompt-Engineering/Using-System-Messages/page

Explains system messages that set persistent assistant role, tone, constraints, and output format, with best practices and examples for effective prompt engineering

System messages are a powerful prompt-engineering technique that set persistent instructions for an AI assistant before any user interaction begins. They define the assistant’s role, tone, and behavior for the entire session, making responses predictable and aligned with your application’s needs—whether that’s customer support, tutoring, travel planning, or virtual assistance. System messages are commonly used with chat completion APIs such as [OpenAI Chat Completions](https://platform.openai.com/docs/guides/chat) and [Azure OpenAI Service](https://learn.microsoft.com/azure/cognitive-services/openai/).

<Frame>
  <img alt="A dark presentation slide with the KodeKloud logo at the top and the centered title &#x22;Using a System Message.&#x22; Small copyright text appears in the lower-left corner." />
</Frame>

What a system message does:

* Sets a persistent instruction for the assistant’s role and tone.
* Applies across the session until changed or overridden.
* Helps ensure consistent structure, style, and constraints in replies.

Example scenario

* Imagine an assistant instructed to behave like a friendly, budget-focused travel planner. The system message drives that behavior across multiple user turns, so the assistant consistently prioritizes low-cost options and a conversational tone.
* The same pattern applies to roles such as professional customer support agents, technical tutors, or financial advisors—each role is defined via the system message.

Example: customer support system message
Below is a minimal conversation that uses a system message to make the assistant act as a professional customer support agent for an electronics store. The assistant responds formally and concisely to a laptop-charging question.

```json theme={null}
[
  {
    "role": "system",
    "content": "You are a professional customer support assistant for an online electronics store. Keep responses formal, concise, and helpful."
  },
  {
    "role": "user",
    "content": "My laptop isn't charging. What should I do?"
  },
  {
    "role": "assistant",
    "content": "I'm sorry to hear that. Please try these steps:\n1. Ensure the charger is properly connected to both the laptop and the power outlet.\n2. Try a different power outlet.\n3. Inspect the charging cable and connector for visible damage or debris.\n4. If your laptop has a removable battery, reseat it and try powering on with the charger.\n5. Restart the laptop and check whether the operating system reports the charger.\nIf the issue persists, please provide your laptop model and the charger type so I can assist further."
  }
]
```

<Callout icon="lightbulb">
  System messages set a persistent instruction for the assistant's role and tone at the start of a conversation. They help ensure consistent, role-specific responses across the session until the system message is changed or overridden.
</Callout>

When to use system messages

* Role enforcement: Make the assistant act as an expert, support agent, tutor, or persona.
* Tone control: Ensure replies are formal, informal, concise, or verbose.
* Safety and constraints: Enforce policies, data-handling rules, or response formats.
* Structured output: Require JSON, YAML, or a specific bullet/step format.

Best practices and considerations

| Aspect                     | Recommendation                                                        | Example                                                       |
| -------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------- |
| Keep it concise            | Use short, precise instructions to avoid unintended behavior          | "Be a formal support agent. Keep replies ≤ 6 sentences."      |
| Be explicit about format   | If you need structured output, request it in the system message       | "Return answers as numbered steps. Use JSON for diagnostics." |
| Avoid sensitive data       | Do not include secrets or private information in system messages      | N/A                                                           |
| Combine with user messages | Use system messages for role/tone, then refine with user instructions | System: role; User: specific request details                  |
| Test iteratively           | Try variations to find the most reliable phrasing for your use case   | A/B test different tones, verbosity, or constraints           |

Practical tips

* Use a system message to set non-negotiable constraints (e.g., safety rules, legal disclaimers).
* Reserve conversation-specific details for the user message so the system message remains reusable.
* If the assistant must return machine-readable output, enforce that format explicitly in the system message.

Further reading and references

* [OpenAI Chat Completions Guide](https://platform.openai.com/docs/guides/chat)
* [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/cognitive-services/openai/)
* [Prompt engineering techniques and best practices](https://platform.openai.com/docs/guides/prompt-design)

Summary
System messages are a foundational tool for controlling assistant behavior across a session. Use them to define role, tone, constraints, and output format—keeping the message concise and explicit will yield the most consistent results.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/d00afd7f-6d8d-4be7-a3f1-5523f484ea72/lesson/9c93d170-947a-4d47-8ba9-9cdd401eab6e" />
</CardGroup>
