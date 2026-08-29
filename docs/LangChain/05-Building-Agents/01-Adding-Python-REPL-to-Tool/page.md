# Invoke with the default (gpt-3.5-turbo)
result_default = chain.invoke({"subject": "cat"})
print(result_default)
```

Example output (using the default model):

```python theme={null}
AIMessage(content="Whiskers soft and fine\nPurring gently in the sun\nGraceful feline friend", response_metadata={'model_name': 'gpt-3.5-turbo', 'token_usage': {'completion_tokens': 19, 'prompt_tokens': 13, 'total_tokens': 32}})
```

## Override the configurable field at runtime

Use `with_config(configurable={...})` to pass overrides for registered configurable fields. Keys in the dictionary must match the configurable field ids you registered (in this example, `"model_name"`):

```python theme={null}
# Force the chain to use GPT-4 for this invocation
result_gpt4 = chain.with_config(configurable={"model_name": "gpt-4"}).invoke({"subject": "cat"})
print(result_gpt4)
```

Example output (overridden to use GPT-4):

```python theme={null}
AIMessage(content="Soft purr in the night,\nEyes gleaming in moon's soft light,\nCat in calm delight.", response_metadata={'model_name': 'gpt-4', 'token_usage': {'completion_tokens': 22, 'prompt_tokens': 13, 'total_tokens': 35}})
```

<Callout icon="lightbulb">
  The configurable field `id` you register must match the parameter name the runnable expects at runtime (for example, `model_name` above). Use `with_config(configurable={...})` to override values per invocation.
</Callout>

## Practical considerations

| Topic           | Guidance                                                             | Example                                                           |
| --------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Cost management | Default to a cheaper model and override only when needed             | Default: `gpt-3.5-turbo`; override to `gpt-4` for complex prompts |
| Key matching    | Ensure configurable field ids match runnable parameter names         | Use `model_name` to override the `ChatOpenAI` model parameter     |
| Composition     | Combine configurable overrides with dynamic prompt inputs and memory | Use runtime `model_name` + user-specific prompts + stored memory  |
| Debugging       | Inspect `response_metadata` to confirm which model was used          | Check `response_metadata['model_name']` in the AIMessage          |

## When to use configurable fields

* You want per-invocation control over LLM models or other runtime settings.
* Your application serves varied tasks that require different capability levels.
* You want to avoid reinitializing runnables or changing deployment configuration mid-run.

## Links and references

* OpenAI Models Overview: [https://platform.openai.com/docs/models/overview](https://platform.openai.com/docs/models/overview)
* LangChain (core concepts and runnables): [https://langchain.readthedocs.io/](https://langchain.readthedocs.io/) (or the relevant repo/docs for your distribution)

Try different OpenAI model names from the models list to see how outputs and token usage change. This pattern provides runtime flexibility without changing deployed code.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/abd1e527-3f6e-4e04-b421-3b1f8de5c69d/lesson/d20a74d2-983f-41da-a5bb-026e3d541199" />
</CardGroup>


# Adding Python REPL to Tool

Source: https://notes.kodekloud.com/docs/LangChain/Building-Agents/Adding-Python-REPL-to-Tool/page

Guide for integrating a Python REPL into a LangChain agent to combine web search (Tavily) with exact programmatic computations for reliable multi-step answers

This guide shows how to add a Python REPL tool to a LangChain agent so it can perform exact computations (for example, date arithmetic) while still using the Tavily search tool for factual lookups. The agent will call Tavily for web/factual queries and call the Python REPL to run precise code when numeric or programmatic results are needed.

Overview

* Goal: Combine factual search (Tavily) with exact computation (Python REPL).
* Outcome: The agent can perform multi-step workflows like "find the event start date" → "compute days until start" with reliable numeric results.

Why add a Python REPL

* LLMs are powerful at reasoning and retrieval but not always exact with arithmetic or programmatic logic.
* A Python REPL enables running actual code for date math, precise calculations, and custom logic, improving reliability of results.

Table: Tools used

| Tool          | Purpose                                       | Example                                       |
| ------------- | --------------------------------------------- | --------------------------------------------- |
| Tavily search | Web / factual lookup                          | `TavilySearchResults()`                       |
| Python REPL   | Execute Python code for exact computation     | `PythonREPLTool()`                            |
| Chat LLM      | Natural language understanding and planning   | `ChatOpenAI()`                                |
| Agent Runner  | Orchestrates tool calls and maintains history | `AgentExecutor`, `RunnableWithMessageHistory` |

Step 1 — Imports and tool initialization
Import the required modules and initialize the Tavily search and Python REPL tools. The consolidated, corrected initialization looks like this:

```python theme={null}
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_openai import ChatOpenAI

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool

from langchain.agents import create_tool_calling_agent, tool
from langchain.agents import AgentExecutor

import os
