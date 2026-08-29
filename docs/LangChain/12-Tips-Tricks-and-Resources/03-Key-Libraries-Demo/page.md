# Key Libraries Demo

Source: https://notes.kodekloud.com/docs/LangChain/Tips-Tricks-and-Resources/Key-Libraries-Demo/page

Explains LangChain library organization, core implementation-agnostic abstractions, and how provider-specific integrations extend them with examples in a short notebook-style demo.

In this lesson we inspect how the LangChain libraries are organized and how responsibilities are split across packages. We'll walk through a short Jupyter notebook–style example to highlight the core abstractions vs. provider-specific implementations.

LangChain Core provides the essential building blocks — lightweight, implementation‑agnostic definitions that the rest of the ecosystem builds on. These include message types, prompt templates, tool wrappers, base classes for language models and embeddings, and other foundational pieces. Think of this package as the platform capabilities expressed as reusable modules and base abstractions.

Here are some canonical imports that illustrate the kinds of definitions provided by the core package:

```python theme={null}
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_core import language_models
```

Quick reference:

| Symbol / Module                             |                   Role | Typical Use                                                      |
| ------------------------------------------- | ---------------------: | ---------------------------------------------------------------- |
| `AIMessage`, `HumanMessage`                 |          Message types | Represent chat-style exchanges between model and user            |
| `ChatPromptTemplate`, `MessagesPlaceholder` | Prompt building blocks | Compose chat prompts and inject dynamic message history          |
| `tool`                                      |       Decorator/helper | Wrap a Python function as an agent-callable tool                 |
| `language_models`                           |        Base interfaces | Define LM/embedding behaviors for concrete adapters to implement |

These are the base definitions from which concrete implementations (for example, specific LLM clients or cloud connectors) are derived. Keeping these abstractions in a small core package helps maintain stability and encourages consistent patterns across integrations.

<Callout icon="lightbulb">
  LangChain Core is intentionally implementation-agnostic. Integrations and provider-specific implementations are provided by separate packages so the core remains lightweight and stable.
</Callout>

The LangChain Community and other integration packages contain concrete implementations and connectors — for example, helpers and clients for OpenAI, other cloud providers, and third‑party tools. Those packages import the core abstractions shown above and extend them with provider-specific behavior, authentication, and convenience helpers.

Links and references

* [LangChain course on KodeKloud](https://learn.kodekloud.com/user/courses/langchain)
* [LangChain documentation (core concepts)](https://learn.kodekloud.com/user/courses/langchain)
* [LangChain community integrations and adapters](https://learn.kodekloud.com/user/courses/langchain)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/b5f7771a-fdbc-45b1-a786-6c84bb7ffc76/lesson/f16a86c1-c3fa-45fe-b348-31f0f35783cb" />
</CardGroup>
