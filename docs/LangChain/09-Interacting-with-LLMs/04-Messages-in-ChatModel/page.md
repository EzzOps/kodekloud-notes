# example_chat_messages.py
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

# Optional: set the API key from Python (best practice is to use environment variables)
# Initialize the chat model (adjust parameters like temperature, model name as needed)
model = ChatOpenAI()

# Define the assistant persona and the user's prompt
sysmsg = "You are a Physics teacher."
humanmsg = "Explain the concept of a galaxy."

messages = [
    SystemMessage(content=sysmsg),
    HumanMessage(content=humanmsg),
]

# Invoke the model with the list of messages.
# Many LangChain chat model wrappers provide `predict_messages` which returns an AIMessage-like object.
response = model.predict_messages(messages)

# Inspect the returned AIMessage object
print(response)            # full AIMessage representation
print(response.content)    # just the textual content returned by the model
```

Note: If your SDK exposes a different method (e.g., `generate` or `chat`), adapt the invocation accordingly.

## Example API response (illustrative)

The returned object is commonly an AIMessage-like structure. Example content (actual output varies):

```python theme={null}
AIMessage(
    content="A galaxy is a massive ensemble of stars, stellar remnants, interstellar gas, dust, dark matter, and other celestial objects bound together by gravity. Galaxies come in several shapes — spiral, elliptical, and irregular — and form the large-scale structure of the universe. The Milky Way, our home galaxy, is a spiral galaxy..."
)
```

## Message roles — quick reference

| Role          | Purpose                                                     | Typical use                                                    |
| ------------- | ----------------------------------------------------------- | -------------------------------------------------------------- |
| SystemMessage | Defines persona, global instructions, or assistant behavior | `SystemMessage(content="You are a concise technical writer.")` |
| HumanMessage  | The user's prompt or question                               | `HumanMessage(content="Explain recursion in simple terms.")`   |
| AIMessage     | The model's response (returned by the API)                  | Inspect with `response.content`                                |

## Key points & troubleshooting

* Keep SDK imports and method names up to date with the official docs. If `from langchain.schema import SystemMessage, HumanMessage` fails, consult the package docs for the correct path.
* If you receive authentication or quota errors, verify that `OPENAI_API_KEY` is set in the environment and that your account has available quota.
* For multi-turn conversations, append subsequent `HumanMessage` and `AIMessage` instances to the `messages` list to preserve context across turns.
* Adjust model parameters (temperature, max tokens, model name) via the chat model constructor or call arguments depending on your SDK.

## Further reading

* [LangChain Documentation](https://learn.kodekloud.com/user/courses/langchain)
* [OpenAI API Reference](https://platform.openai.com/docs)
* SDK-specific migration guides and release notes (check the package repo or docs for breaking changes)

That completes a concise walkthrough of constructing and exchanging messages with a chat-based language model. Subsequent sections can cover conversation history management, system-level instructions for role-based behavior, and advanced prompt design patterns.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/c67000e4-0960-4e50-a4e4-b8cb159f2f1e" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/0dfdfd01-a5b0-4e95-9ccd-49e5189bcd2e" />
</CardGroup>


# Messages in ChatModel

Source: https://notes.kodekloud.com/docs/LangChain/Interacting-with-LLMs/Messages-in-ChatModel/page

Explains chat model message types, ordered message lists, and best practices for building multi-turn conversational prompts and personas using LangChain

In this lesson we explain how chat-oriented language models receive and organize information using structured messages. Understanding message types and the ordered message list is essential when building reliable, multi-turn conversational applications with libraries like LangChain.

## Core message types

A chat conversation is typically composed from three message types:

* System message — a global instruction that defines the assistant's persona, behavior, or tone for the session (for example, "You are a dietician" or "You are a physics teacher").
* Human message — the user's input or prompt. Human messages are sent repeatedly as the conversation continues.
* AI message — the model's responses generated in reply to the human messages and shaped by the system message.

The system message plus the sequence of human (and AI) messages form the prompt sent to the model. Place the system message at the start of the conversation so it can influence subsequent replies. Because models are stateless across independent sessions, re‑include the system message at the beginning of each new session if you need to preserve the same persona.

<Frame>
  <img alt="The image is a flowchart illustrating message types in a chat model, including system, human, and AI messages, with an application interacting with a dietician and a chat model." />
</Frame>

## Quick reference table

| Message type   | Purpose                                          | Example                                                                      |
| -------------- | ------------------------------------------------ | ---------------------------------------------------------------------------- |
| System message | Set global behavior or persona for the assistant | `You are a professional dietician who gives concise, evidence-based advice.` |
| Human message  | User's prompt / follow-up questions              | `What is a healthy breakfast for someone trying to lose weight?`             |
| AI message     | Model-generated reply                            | `A healthy breakfast might include...`                                       |

## Example: building a chat prompt in LangChain (Python)

In LangChain, chat prompts for chat models are represented as ordered lists of message objects. Below is a simple Python example showing how to build that list and call the chat model.

```python theme={null}
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
