# Bash examples
export OPENAI_API_KEY="sk-..."         # OpenAI
export GOOGLE_API_KEY="ya29...."       # Google Generative AI (API key)
# or
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"  # for service accounts
```

Which Google method you need depends on the LangChain integration and the client library. Consult the Google Generative AI docs and LangChain docs for the correct authentication flow:

* Google Generative AI docs: [https://developers.generativeai.google/](https://developers.generativeai.google/)
* LangChain Python docs: [https://python.langchain.com/en/latest/](https://python.langchain.com/en/latest/)

Environment variables quick reference:

| Environment variable             | Provider             | Purpose / Notes                                   |
| -------------------------------- | -------------------- | ------------------------------------------------- |
| `OPENAI_API_KEY`                 | OpenAI               | API key used by OpenAI wrappers                   |
| `GOOGLE_API_KEY`                 | Google Generative AI | API key option for some clients                   |
| `GOOGLE_APPLICATION_CREDENTIALS` | Google Generative AI | Path to service account JSON for server-side auth |

If you must set keys inside a Python session for testing (not recommended for production), use `os.environ`:

```python theme={null}
import os
# os.environ["OPENAI_API_KEY"] = "sk-..."
# os.environ["GOOGLE_API_KEY"] = "ya29...."
```

***

## 2) Imports and minimal LangChain pattern

LangChain exposes provider-specific LLM wrappers. The typical pattern is:

1. Import the provider wrapper (e.g., `OpenAI` or `GoogleGenerativeAI`).
2. Instantiate the wrapper (optionally specifying model and parameters).
3. Call the wrapper with a prompt and handle the response.

Below are two minimal, copy-paste-ready examples demonstrating this pattern.

***

## 3) Example: OpenAI LLM (text-generation)

This example shows the simplest flow to instantiate an OpenAI wrapper, call it with a prompt, and print the response.

```python theme={null}
from langchain import OpenAI
import os

# Optional: set API key in-session (prefer exporting in your shell)
# Instantiate the OpenAI wrapper. You can pass model and parameters if needed.
llm = OpenAI()  # Uses OPENAI_API_KEY from environment; defaults to a model configured by the LangChain package
prompt = "What would be a good company name for a company that makes toys for kids?"

# Call the LLM and print the result
response = llm(prompt)
print(response)
```

Sample output (one possible response):

```text theme={null}
Playful Pals Toys
```

Notes:

* If you need deterministic output or other behavior, pass parameters like `temperature` or an explicit `model` when instantiating `OpenAI(temperature=0.0, model="gpt-4o-mini")`.
* Some LangChain releases also expose chat-specific wrappers (e.g., `ChatOpenAI`) which are better suited for chat-native models.

***

## 4) Example: Google Generative AI (Gemini)

Switching to Google Generative AI (Gemini) is straightforward: import the Google wrapper, instantiate with the desired Gemini model, and keep the same prompt and call flow.

```python theme={null}
from langchain import GoogleGenerativeAI  # confirm exact import in your LangChain version
import os

# Optional: set in-session (prefer exporting in your shell)
# os.environ["GOOGLE_API_KEY"] = "ya29...."
# Instantiate with an explicit Gemini model
llm = GoogleGenerativeAI(model="gemini-pro")
prompt = "What would be a good company name for a company that makes toys for kids?"

response = llm(prompt)
print(response)
```

Sample output (one possible response):

```text theme={null}
1. Joyful Creations
2. Imagination Unbound
3. Wonder & Play
4. Kiddie's Delight
5. Playful Wonders
6. Tiny Treasures
7. Learning Adventures
8. Whimsical Wonders
9. Spark of Imagination
10. Happy Hearts
```

Tips:

* Choose the Gemini model appropriate for your use case (e.g., `gemini-ultra`, `gemini-pro`, etc.). Model names and availability can vary by account and LangChain version.
* If authentication fails, verify the environment variable method (API key vs service account) required by your client and LangChain integration.

***

## 5) Switching providers on the fly

LangChain’s wrapper abstraction lets you swap LLM providers with minimal code change. Keep prompts and high-level logic the same; only change the import and instantiation.

Example (switching to Google from OpenAI):

```python theme={null}
# from langchain import OpenAI
from langchain import GoogleGenerativeAI
import os

# llm = OpenAI()
llm = GoogleGenerativeAI(model="gemini-pro")
prompt = "What would be a good company name for a company that makes toys for kids?"
print(llm(prompt))
```

This prints the result from whichever LLM wrapper is currently assigned to `llm`. The same pattern applies when swapping embeddings, vector stores, or other pipeline components — typically only the instantiation/import changes.

> **lightbulb** When swapping providers, ensure you have installed the provider-specific client package and set the corresponding environment variables for authentication.

***

## 6) Quick comparison: OpenAI vs Google Generative AI (Gemini)

| Aspect             |                              OpenAI | Google Generative AI (Gemini)                                     |
| ------------------ | ----------------------------------: | ----------------------------------------------------------------- |
| Common wrapper     |                            `OpenAI` | `GoogleGenerativeAI`                                              |
| Authentication     |                    `OPENAI_API_KEY` | `GOOGLE_API_KEY` or `GOOGLE_APPLICATION_CREDENTIALS`              |
| Chat-native models |     Use `ChatOpenAI` when available | Gemini may require chat-style wrapper or specific model parameter |
| Model selection    |          Pass `model="gpt-4o"` etc. | Pass `model="gemini-pro"` etc.                                    |
| Notes              | Popular for many LangChain examples | May require service account auth on server-side environments      |

***

## 7) Best practices and final notes

* Use environment variables for credentials; never commit keys to source control.
* Pass model-specific parameters (temperature, max tokens) at instantiation when deterministic or constrained behavior is required (e.g., `OpenAI(temperature=0.2)`).
* Prefer chat-specific wrappers for chat-native models when available.
* This lesson focuses on invoking LLMs with simple prompts. Subsequent lessons will cover chat-style APIs, embeddings, vector stores, and chaining LangChain components to build more advanced pipelines.

Recommended reading and references:

* LangChain docs: [https://python.langchain.com/en/latest/](https://python.langchain.com/en/latest/)
* OpenAI docs: [https://platform.openai.com/docs](https://platform.openai.com/docs)
* Google Generative AI docs: [https://developers.generativeai.google/](https://developers.generativeai.google/)

- [Watch Video](https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/9e76504b-2c1a-48b2-a099-b53c1c5bf71b)


# Messages in ChatModel Demo

Source: https://notes.kodekloud.com/docs/LangChain/Interacting-with-LLMs/Messages-in-ChatModel-Demo/page

Guide to using message objects and best practices for constructing prompts with chat models, including examples, environment setup, and troubleshooting for SDKs like LangChain

In this lesson we'll examine message objects and best practices for constructing prompts for chat-based models. The goal is to demonstrate the typical flow: import message classes, initialize a chat model, create `SystemMessage` and `HumanMessage` objects, send them to the model, and inspect the returned AI message.

> **lightbulb** Module and API names in SDKs such as [LangChain](https://learn.kodekloud.com/user/courses/langchain) change frequently. If an import or method shown here fails, consult the latest SDK documentation and adapt import paths or method names accordingly.

## Prerequisites

* An OpenAI-compatible API key available in your environment.
* A compatible version of the chat SDK you plan to use (e.g., LangChain). If imports differ, check the package docs.

> **warning** If the model call fails with authentication errors, confirm that your `OPENAI_API_KEY` is set and that your SDK supports the provider and model you are calling.

## Environment variable

Set your OpenAI API key in the shell before running Python examples.

macOS / Linux (bash/zsh):

```bash theme={null}
export OPENAI_API_KEY="your_api_key_here"
```

Windows (PowerShell):

```powershell theme={null}
$env:OPENAI_API_KEY = "your_api_key_here"
```

You can also set the key programmatically in Python (not recommended for production):

```python theme={null}
import os
os.environ["OPENAI_API_KEY"] = "your_api_key_here"
```

## Minimal Python example

This example shows a compact, runnable pattern using message objects and a chat model. Adjust imports and model initialization for your SDK version if necessary.

```python theme={null}
