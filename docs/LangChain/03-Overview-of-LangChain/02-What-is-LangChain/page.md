# What is LangChain

Source: https://notes.kodekloud.com/docs/LangChain/Overview-of-LangChain/What-is-LangChain/page

Explains LangChain framework and SDK for integrating LLMs, embeddings, vector databases, and external data to build production-ready generative AI applications.

This lesson builds on the core building blocks of generative AI applications. Before diving deeper into each component, this article clarifies what LangChain is and how it helps you build production-ready LLM applications.

LangChain is a framework and SDK that simplifies integrating large language models (LLMs) with applications. Think of it as middleware between your application and the critical elements of any generative AI system: language models, embeddings, vector databases, and external data sources. Instead of wiring your app directly to each provider, LangChain manages those integrations so you can focus on application logic and orchestration.

<Frame>
  <img alt="The image is titled &#x22;Understanding LangChain&#x22; and features icons representing four components: Embeddings, External Data, Vector Databases, and Language Models." />
</Frame>

Why use LangChain?

* It abstracts provider-specific APIs, reducing boilerplate code.
* It lets you swap LLMs, embedding providers, or vector databases with minimal changes.
* It provides patterns and primitives for retrieval-augmented generation (RAG), chains, agents, and more.
* It acts as an orchestration layer that coordinates interactions across the GenAI stack.

Core components at a glance

| Component        | Purpose                                                                   | Example use                                                    |
| ---------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Embeddings       | Convert text to vector representations for semantic search and similarity | Use OpenAI or other embedding models to encode documents       |
| Vector Databases | Store and query embeddings for nearest-neighbor retrieval                 | `FAISS`, `Pinecone`, `Weaviate` for fast semantic search       |
| External Data    | Connectors to files, databases, APIs, and knowledge bases                 | Ingest PDFs, web pages, or SQL data for context enrichment     |
| Language Models  | Generate or transform text using LLMs                                     | `OpenAI` GPT models or alternative LLM providers for responses |

If you come from a database or application-development background, a useful analogy is that LangChain functions like ODBC/JDBC for LLM applications: change the configuration to use a different backend while keeping most of your application code intact.

LangChain is not just a client library; it’s also an orchestration layer. It coordinates how prompts, retrieval, and reasoning steps flow together—like a choreographer connecting components and sequencing interactions.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;Understanding LangChain&#x22; with a logo, and icons representing &#x22;Framework,&#x22; &#x22;SDK,&#x22; and &#x22;Middleware.&#x22;" />
</Frame>

A brief history and ecosystem
LangChain emerged in late 2022 and quickly became one of the fastest-growing open-source projects in the LLM space. Its rapid adoption coincided with ChatGPT’s mainstream release, which accelerated community contributions and integrations across vendors.

<Frame>
  <img alt="The image highlights &#x22;The Rise of LangChain,&#x22; with logos of LangChain and ChatGPT, mentioning their respective releases in late October 2022 and November 2022." />
</Frame>

Because of that momentum, LangChain is now a standard tool for building applications that interact with LLMs across industries: search assistants, knowledge bases, summarizers, agents, and more.

LangChain provides SDKs for both Python and JavaScript. This lesson focuses on the Python implementation and its integration with OpenAI. While LangChain supports many LLMs and providers, this article concentrates on the patterns and examples commonly used with OpenAI’s models.

<Callout icon="lightbulb">
  This lesson focuses on LangChain's Python SDK and examples using OpenAI. If you plan to use other providers (e.g., Anthropic, Cohere, local LLMs), the same core concepts apply—LangChain adapters make switching providers straightforward.
</Callout>

<Frame>
  <img alt="The image features the text &#x22;The Rise of LangChain&#x22; with logos for LangChain and OpenAI, and an icon labeled &#x22;Application.&#x22;" />
</Frame>

Practical considerations

* LangChain reduces integration complexity, but you still need to manage API keys, rate limits, and costs for LLM and embedding providers.
* When switching providers, review differences in tokenization, embedding dimensions, and model behavior—LangChain standardizes interfaces but does not hide model-specific characteristics.

<Callout icon="warning">
  Never commit API keys or credentials to source control. Use environment variables, secret managers, or your platform’s secret store to keep keys secure.
</Callout>

Further reading and references

* LangChain Documentation: [https://langchain.readthedocs.io/](https://langchain.readthedocs.io/)
* OpenAI Platform Docs: [https://platform.openai.com/docs/](https://platform.openai.com/docs/)
* If you’re new to OpenAI, consider the [Introduction to OpenAI](https://learn.kodekloud.com/user/courses/introduction-to-openai) course on KodeKloud.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/ab7ff6ea-63e2-4d3b-af7c-ed22616cc3b6/lesson/185f55c8-b528-4016-a4ea-e35690c295f4" />
</CardGroup>
