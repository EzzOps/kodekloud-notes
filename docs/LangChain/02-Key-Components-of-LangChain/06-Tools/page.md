# Tools

Source: https://notes.kodekloud.com/docs/LangChain/Key-Components-of-LangChain/Tools/page

Explains LangChain tools that connect LLMs to external APIs and services, built-in and custom tool creation, usage patterns, security practices, and organizing tools into reusable toolkits

In this lesson we cover tools — a core LangChain concept that extends a large language model’s capabilities by connecting it to external functions, services, and APIs. Tools let your LLM access real-world data sources (APIs, databases, internal services) and perform actions (I/O, computation, side effects), enabling richer, production-ready AI workflows.

<Frame>
  <img alt="The image displays a section labeled &#x22;Tools&#x22; with icons for &#x22;Functions,&#x22; &#x22;Services,&#x22; and &#x22;API&#x22; beneath it." />
</Frame>

LangChain ships with many ready-made tools for popular services such as Wikipedia, YouTube, and Google Search. Use these built-ins to quickly add search and knowledge retrieval to your agents without building integrations from scratch.

<Frame>
  <img alt="The image shows the LangChain logo alongside icons for Wikipedia, YouTube, and Google Search, labeled as tools." />
</Frame>

For private systems or custom workflows, implement a custom tool. A typical tool:

* Accepts text or structured arguments,
* Calls an external API, queries a database, or runs application logic,
* Returns text or structured data (JSON, lists, etc.) that the LLM can consume.

Below is a minimal example showing the decorator-based pattern for creating a simple custom tool in Python. This pattern wraps your function so it can be invoked by LangChain agents and pipelines:

```python theme={null}
