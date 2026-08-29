# Using Tavily Search Tool

Source: https://notes.kodekloud.com/docs/LangChain/Using-Tools/Using-Tavily-Search-Tool/page

Guide to using the Tavily Search API with LangChain to fetch, aggregate, and cite web search results for retrieval augmented generation while securely managing API keys

Tavily Search API connects large language models (LLMs) to the web, enabling fast, persistent web search results you can inject as context for retrieval-augmented generation (RAG) workflows. This guide shows how to fetch results from Tavily and use them with an LLM (for example, via LangChain) to create search-augmented prompts or document stores.

<Frame>
  <img alt="The image is a webpage for Tavily AI, promoting a search API that connects large language models to the web for efficient, quick, and persistent search results. It features buttons to open GitHub and join the community." />
</Frame>

Overview

* Use Tavily to perform web searches and collect the returned page snippets and URLs.
* Store your Tavily API key securely (environment variable recommended) and never commit secrets to source control.
* Aggregate, chunk, or index the returned content to provide up-to-date, cited context to your LLM.

Getting your API key

1. Sign up for Tavily and visit your dashboard.
2. Copy the API key and set it as an environment variable on your machine or deployment environment (example below).

<Frame>
  <img alt="The image shows a web page interface for &#x22;Tavily AI&#x22; with an &#x22;Overview&#x22; section displaying a &#x22;Researcher&#x22; plan, API usage details, and an API key authentication area. There are menu options on the left and a contact button at the bottom." />
</Frame>

<Callout icon="lightbulb">
  Tavily often provides a free developer tier (for example, 1,000 calls/month at the time of writing). Store your API key in an environment variable such as `TAVILY_API_KEY` and avoid hard-coding secrets in source files.
</Callout>

Quick example using the LangChain community tool wrapper

* The LangChain community package provides a `TavilySearchResults` wrapper to simplify queries and return structured results.
* The wrapper typically reads the `TAVILY_API_KEY` environment variable when initialized.

Setup and usage

1. Export your API key locally:

```bash theme={null}
export TAVILY_API_KEY="your_api_key_here"
```

2. Minimal Python usage:

```python theme={null}
