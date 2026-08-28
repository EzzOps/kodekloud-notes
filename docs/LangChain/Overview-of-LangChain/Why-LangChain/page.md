# Why LangChain

Source: https://notes.kodekloud.com/docs/LangChain/Overview-of-LangChain/Why-LangChain/page

Overview of LangChain, a framework for building portable, composable generative AI apps with unified data connectors, prompt tooling, and agent orchestration.

LangChain is an abstraction layer for building production-grade applications with generative AI. Think of it as the ODBC/JDBC of GenAI: it decouples your application from fast-moving models, embedding providers, vector stores, and external APIs so you can swap components without rewriting core logic.

<Callout icon="lightbulb">
  LangChain makes it easy to experiment and iterate: swap models, vector stores, or search providers with minimal changes to application code while keeping data flows and business logic intact.
</Callout>

## Core value: portability and composability

The GenAI ecosystem includes many language models, embedding services, and data connectors. Directly wiring each provider into your app quickly becomes complex and brittle. LangChain provides consistent primitives (chains, agents, tools, retrievers, etc.) so you interact with a stable API rather than every vendor-specific SDK.

This is particularly important when you must integrate on-prem or cloud-hosted enterprise data: databases, CSV/JSON exports, PDFs, Office documents, web pages, and third‑party APIs. LangChain centralizes the plumbing needed to ingest, transform, and inject that context into model prompts.

<Frame>
  <img alt="The image illustrates how a LangChain LLM (large language model) processes various document types such as DOC, PDF, JSON, CSV, XML, PPT, and XLS." />
</Frame>

## Integrations: one API for many data sources

LangChain lets you connect to diverse data sources without hardcoding each integration into your business logic. Examples include:

* Databases (SQL, NoSQL)
* Local or cloud-hosted files (PDFs, Word, PowerPoint, Excel)
* Web pages and search engines
* External REST/GraphQL APIs and custom tool endpoints

<Frame>
  <img alt="The image lists reasons for using LangChain, featuring icons for database, files, web search, and API." />
</Frame>

## Swap providers easily

Because LangChain abstracts provider details, you can swap search or model backends without changing your chaining, prompting, or retrieval logic. For example, swap between:

* [Bing Search](https://www.bing.com/)
* [DuckDuckGo](https://duckduckgo.com/)
* [SerpAPI](https://serpapi.com/)

Such interchangeability accelerates A/B testing, cost optimization, and resilience.

<Frame>
  <img alt="The image features the Bing Search Engine logo with the text &#x22;Why LangChain?&#x22; and a colorful abstract graphic on a terminal window." />
</Frame>

## Simplifying prompts, transforms, and response handling

LangChain provides utilities for advanced prompt engineering, response parsing, and output formatting. Rather than handling these aspects ad hoc, LangChain offers reusable components:

* Prompt templates and prompt chains
* Output parsers and schema validation
* Data transforms (text chunking, embeddings, reranking)

A powerful pattern is to use the LLM itself to detect missing context. When a prompt lacks required inputs, the model can indicate what’s missing and LangChain can fetch those dependencies (call APIs, query databases, or read files), then re-run the chain—closing the loop for more complete, reliable responses.

<Frame>
  <img alt="The image highlights why to use LangChain, featuring icons labeled &#x22;Building&#x22; and &#x22;Simplifying&#x22; around the LangChain logo with a parrot emoji." />
</Frame>

## Closing the loop: from assistants to autonomous agents

LangChain enables building agents that do more than single-turn Q\&A. Agents can:

* Plan multi-step actions
* Orchestrate tool calls (APIs, database lookups, web searches)
* Maintain state and follow multi-step reasoning
* Execute tasks on behalf of users

This “identify-missing-info → fetch/compute → act” loop is a foundation for building autonomous systems that go beyond simple chatbots.

<Frame>
  <img alt="The image illustrates a concept where a parrot and chain icon next to &#x22;LangChain&#x22; interacts with a neural brain icon labeled &#x22;LLM,&#x22; accompanied by a speech bubble saying &#x22;Hey! I need this!&#x22;" />
</Frame>

Agents orchestrated by LangChain can combine reasoning with tool usage to perform lookups, take actions, and return structured results—making them an important step toward more general-purpose AI systems.

<Frame>
  <img alt="The image is a slide with the title &#x22;Why LangChain?&#x22; featuring a gradient banner labeled &#x22;Artificial General Intelligence&#x22; and an icon with two flexing arms labeled &#x22;Agents,&#x22; accompanied by a robot head." />
</Frame>

## Quick reference — Where LangChain helps most

| Area                            | Benefit                                        | Examples                            |
| ------------------------------- | ---------------------------------------------- | ----------------------------------- |
| Model and embedding portability | Swap providers without touching business logic | OpenAI, Anthropic, Cohere           |
| Data ingestion                  | Unified adapters for files, DBs, web, and APIs | PDFs, Excel, SQL, REST endpoints    |
| Prompt engineering & parsing    | Reusable templates and reliable output parsing | Prompt templates, JSON/YAML parsers |
| Agents & orchestration          | Multi-step workflows and tool usage            | Search + DB lookup + API calls      |

This article will continue with concrete examples and a tutorial on building agents using LangChain—showing how the framework helps you build robust, production-ready intelligent applications.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/ab7ff6ea-63e2-4d3b-af7c-ed22616cc3b6/lesson/a1b0bfdd-c32b-4575-b19d-ce8a6985abe2" />
</CardGroup>
