# python
import os
import anthropic

# Prefer environment variable; replace with a secure source in real projects.
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "<YOUR_CLAUDE_API_KEY>")

# Initialize client
# Depending on the SDK version this may be `anthropic.Client(...)` or `anthropic.Anthropic(...)`.
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# System prompt defines the assistant's role/personality.
system_prompt = "You are a helpful research assistant. Answer clearly and concisely."

# Short-term chat history (list of {"role": "user" | "assistant", "content": str})
message_history = []

def run_claude_agent(message_history, user_input):
    """
    Append the user input to the message history, send the conversation
    (with system prompt) to Claude, append the assistant reply to history,
    and return the assistant reply.
    """
    # Add user message to history
    message_history.append({"role": "user", "content": user_input})

    # Send request to Claude
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=500,
        temperature=0.7,
        system=system_prompt,        # Some SDKs take system separately; follow your SDK docs
        messages=message_history     # messages should use "user" and "assistant" roles
    )

    # Extract assistant text from response.
    # SDK response formats vary between versions; try common patterns.
    assistant_reply = ""
    if hasattr(response, "content") and len(response.content) > 0:
        first = response.content[0]
        # Some SDKs return objects with a 'text' attribute or dicts with 'text'
        assistant_reply = getattr(first, "text", None) or (first.get("text", "") if isinstance(first, dict) else str(first))
    else:
        # Fallback: represent the raw response
        assistant_reply = str(response)

    # Add assistant reply to history and return
    message_history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply

# Interactive chat loop
if __name__ == "__main__":
    print("Start chatting with the Claude agent. Type 'exit' or 'quit' to end.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting Claude agent, goodbye!")
            break

        reply = run_claude_agent(message_history, user_input)
        print("\nClaude:", reply, "\n")
```

## Key implementation notes

* Many Anthropic SDKs accept a separate `system` parameter instead of a message with `"role": "system"`. If you include a `"system"` role inside `messages` when the SDK expects a `system` parameter, you may see errors. Always consult the documentation for the SDK version you're using.
* Use `"user"` and `"assistant"` roles in the `messages` list to preserve conversation state and allow Claude to reference earlier turns.
* Tune `max_tokens` to control the maximum reply length and `temperature` to adjust randomness.
* SDK class and method names may change between versions — e.g., `anthropic.Client` vs `anthropic.Anthropic`. If you encounter import errors or an unexpected response structure, check [docs.anthropic.com](https://docs.anthropic.com) for version-specific examples.

## Quick reference: common troubleshooting

| Symptom                    | Likely cause                               | Quick fix                                                                                             |
| -------------------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| ImportError on `anthropic` | Package not installed or wrong environment | Run `!pip install anthropic` in the notebook kernel and restart kernel                                |
| Authentication error       | Missing or invalid API key                 | Ensure `CLAUDE_API_KEY` env var is set; avoid committing credentials                                  |
| Unexpected response format | SDK version differences                    | Print `response` to inspect structure and adapt parsing; consult SDK docs                             |
| SDK method not found       | Version mismatch                           | Check release notes or use the version documented on [docs.anthropic.com](https://docs.anthropic.com) |

## Try it out

After starting the interactive loop, try asking Claude a question such as:

* "Give me a recipe for banana bread."
* "Summarize the key points from this paragraph."
* "Draft a short email asking for a meeting."

The notebook will display the assistant's reply and preserve the chat history so Claude can use earlier context. Type `exit` or `quit` to end the session.

## Extending the agent

From this minimal example you can extend your agent in many ways:

* Persist chat history to disk or a database for longer-term context.
* Add tools or retrieval layers (e.g., vector DB + semantic search) to ground responses in external data.
* Implement streaming responses (if supported by your SDK) for real-time UI updates.
* Post-process model outputs to extract structured data, generate artifacts (tables, charts), or call downstream APIs.

## Wrapping up

This guide demonstrated a minimal Claude chat agent in a Jupyter notebook:

* Define a system role to shape behavior.
* Maintain a message history to give Claude conversational context.
* Send the system prompt and messages via `client.messages.create`.
* Append assistant replies to history.
* Use an interactive loop to simulate chat sessions.

Next steps: explore the model and SDK options in the Anthropic docs, experiment with different system prompts for specialized behavior, and add retrieval or post-processing layers to build more capable assistants.

## Links and references

* Anthropic documentation: [https://docs.anthropic.com](https://docs.anthropic.com)
* Anthropics Python package on PyPI: [https://pypi.org/project/anthropic/](https://pypi.org/project/anthropic/)

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents/module/d2a91525-d4e7-4c2a-866a-e7a9d34b538c/lesson/e6fad41a-3b51-43f1-b004-df93029163a1)


# Demo How to Use Poe

Source: https://notes.kodekloud.com/docs/AI-Agents/API-Integrations-Tools/Demo-How-to-Use-Poe/page

Guide to using Poe to build, test, embed, and monetize conversational AI bots with server and embedded options, UI walkthrough, and integration guidance

Welcome back.

In this lesson we’ll walk through how to use Poe (Platform for Open Exploration) — Quora’s chatbot platform — to create, test, and embed conversational AI agents. This guide covers the core capabilities, the user interface, a quick hands-on demo to build a prompt bot, and links to further documentation.

What is Poe?

Poe is a chat-first platform that lets you interact with powerful large language models (LLMs) such as GPT-4, Claude, and others via a polished chat UI. Poe supports:

* Server bots: you host the backend logic and Poe provides the front-end chat experience.
* Embedded bots: embed a Poe widget into your web app or notebook.
* Creator features: monetization and subscription options for bot creators.

What Poe can do

* Build server bots: Host your backend LLM, call external APIs and tools, manage conversation state, and stream multi-message responses while Poe handles the chat UI.
* Embed bots: Use Poe’s embed API to place bots in websites, apps, or dashboards. Any bot you publish on Poe can be embedded and customized.
* Monetize: Optional creator monetization and subscription controls let you charge for access or messages.

Feature summary

| Capability      | Use case                                   | Quick example                                            |
| --------------- | ------------------------------------------ | -------------------------------------------------------- |
| Server bots     | Custom backend, tools, APIs                | Host your own LLM and stream responses to Poe’s frontend |
| Embedded widget | Add a chat UI to a website or SaaS product | Embed a bot with a few configuration options             |
| Monetization    | Charge users or set message limits         | Enroll in Poe’s creator program and set message prices   |

Explore the UI

The Poe interface makes it easy to create different bot types — prompt bots, image/video generation bots, roleplay bots, server bots, and canvas apps. The left navigation groups your bots, subscriptions, and settings so you can manage projects and billing in one place.

<Frame>
  <img alt="The image shows a user interface on the Poe website, featuring options to create various types of bots or apps, such as &#x22;Prompt bot,&#x22; &#x22;Image generation bot,&#x22; and &#x22;Video generation bot.&#x22; On the left is a navigation menu with options including &#x22;Bots and apps,&#x22; &#x22;Subscribe,&#x22; and &#x22;Settings.&#x22;" />
</Frame>

You can also browse available LLMs (e.g., Claude, Gemini, GPT-4 variants) and review creator-focused features such as monetization settings and enrollment options.

<Frame>
  <img alt="The image shows a webpage from Poe offering a Creator Monetization program, detailing how users can earn money by enrolling, setting message prices, limiting messages, sharing bots, and getting paid for subscriptions and user engagement. The page includes side navigation options and download links for various apps." />
</Frame>

Quick walkthrough — create a simple prompt bot

This step-by-step example demonstrates how fast it is to set up a prompt bot and test its behavior.

1. Click Create and choose “Prompt bot.”
2. Enter a name (for example: “Teach Me Many Things”).
3. Add a description and a persona/system instruction. Example:
   * “You are a Poe bot that will teach me how to code. You should respond as thoroughly as possible, but always speak as if you are Jar Jar Binks.”
4. Choose a base model (for example, GPT-4 or a lightweight GPT-4 variant).
5. Optionally add an initial message such as “Hi there, how can I help?”
6. Review advanced settings (keep defaults for this demo) and click Publish → Continue without editing.

Test the bot

After publishing, test the bot in Poe’s chat interface. For this demo we asked:

“Can you teach me how to make a grilled cheese sandwich?”

The bot returned a step-by-step recipe while adhering to the specified persona, showing how system instructions influence tone and content.

<Frame>
  <img alt="The image shows a chat conversation on a platform called Poe, where a user is asking how to make a grilled cheese sandwich. The response provides a list of ingredients and step-by-step instructions for making the sandwich." />
</Frame>

Integration options

* Embed: Use Poe’s embedded API to include the chat widget in web apps or notebooks.
* Server API: Connect a backend to Poe’s RESTful endpoints to send/receive messages, stream responses, and manage conversation state.
* Tools & APIs: Integrate external APIs and tools on your hosted backend for richer agent capabilities.

> **lightbulb** Before integrating or publishing bots, review Poe’s documentation for API usage, authentication, rate limits, and billing. Keep your API keys secret and follow security best practices when embedding or hosting bots.

Next steps and references

* Read Poe’s Quick Start and API docs for authentication, generating API keys, and handling streaming responses: [https://poe.com/docs](https://poe.com/docs)
* Explore sample projects and community examples to learn advanced patterns like tool integration and multi-step pipelines.

That’s a concise introduction to building, testing, and embedding bots on Poe. Explore the documentation and try creating a few bot personas to understand how system instructions and model selection shape responses.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents/module/d2a91525-d4e7-4c2a-866a-e7a9d34b538c/lesson/63f535ae-d096-42c4-a138-3c6c088b98c4)
