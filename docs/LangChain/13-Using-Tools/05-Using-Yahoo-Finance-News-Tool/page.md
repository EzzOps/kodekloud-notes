# Configure the underlying Wikipedia API wrapper
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)

# Create the tool that uses the wrapper
tool = WikipediaQueryRun(api_wrapper=api_wrapper)
```

You can inspect the tool's metadata (name, description, and the expected arguments):

```python theme={null}
print(tool.name)
print(tool.description)
print(tool.args)
```

Expected console output:

```text theme={null}
wikipedia
A wrapper around Wikipedia. Useful for when you need to answer general questions about people, places, companies, facts, historical events, or other subjects. Input should be a search query.
{'query': {'title': 'Query', 'type': 'string'}}
```

To run the tool, call its `run` method with a dictionary whose key is the argument name (`"query"`) and whose value is the search string. For example, to fetch the top summary for "Neural Network":

```python theme={null}
result = tool.run({"query": "Neural Network"})
print(result)
```

The returned `result` contains the text retrieved from Wikipedia (bounded by `doc_content_chars_max`).

> **lightbulb** The Wikipedia tool returns external content suitable for RAG workflows. Tune `top_k_results` and `doc_content_chars_max` to control coverage and token consumption. Use the retrieved text as context to an LLM or to populate a retrieval index.

> **warning** The tool only retrieves content from Wikipedia; it does not call an LLM. Always validate returned facts and be mindful of freshness, attribution, and rate limits when using third-party content.

## Practical notes and recommended patterns

* Retrieval-only: The Wikipedia tool fetches content only. To generate answers or reason over content, pass the retrieved text into an LLM chain, prompt, or an agent that calls the LLM.
* RAG integration: Combine multiple sources (Wikipedia + other knowledge sources) and index them in a vector store for more robust retrieval.
* Tool composition: Wrap the Wikipedia tool invocation in functions or chaining mechanisms (e.g., LCEL or LangChain chains) and combine it with other tools (search, calculators, or user prompts) for multi-step agents.
* Rate limits & caching: Respect Wikipedia API rate limits and consider caching frequently fetched pages to reduce network load and latency.

## Links and references

* LangChain Integrations: [https://docs.langchain.com](https://docs.langchain.com)
* Wikipedia: [https://www.wikipedia.org](https://www.wikipedia.org)
* DALL·E: [https://openai.com/dall-e](https://openai.com/dall-e)
* Bash: [https://www.gnu.org/software/bash/](https://www.gnu.org/software/bash/)
* Twilio: [https://www.twilio.com](https://www.twilio.com)

This demonstrates the basic usage of the Wikipedia tool. The next section will cover combining multiple tools into an agent for more advanced workflows.

- [Watch Video](https://learn.kodekloud.com/user/courses/langchain/module/06905b96-585d-4c9e-835a-d8fcaca76e2a/lesson/dd8b1038-f63d-4623-9cac-2378b7808082)


# Using Yahoo Finance News Tool

Source: https://notes.kodekloud.com/docs/LangChain/Using-Tools/Using-Yahoo-Finance-News-Tool/page

Explains a lightweight Yahoo Finance News Tool that scrapes and returns recent headlines and short summaries for a given stock ticker, with usage, features, and best practices.

This lesson covers the Yahoo Finance News Tool — a lightweight utility that scrapes and returns recent headlines and short summaries for a given stock ticker from Yahoo Finance. It's particularly useful when building finance-focused [agents](https://learn.kodekloud.com/user/courses/ai-agents) or assistants that need up-to-date news context about a company.

## Quick start

Example usage:

```python theme={null}
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool

tool = YahooFinanceNewsTool()
res = tool.run("NVDA")
print(res)
```

Example output:

```plaintext theme={null}
Nvidia (NVDA) Rises But Trails Market: What Investors Should Know
Nvidia (NVDA) closed at $877.57 in the latest trading session, marking a +0.03% move from the prior day.
```

## What the tool returns

This tool scrapes the Yahoo Finance news pages for the provided ticker (for example, `NVDA`) and returns the most relevant or trending news headlines with short summary lines. The returned text commonly includes:

* Headline(s)
* Short summary or status lines (e.g., recent close price and percent change)
* Brief context that helps determine relevance for trading or research

## How it works

* It performs HTTP requests to the public Yahoo Finance news pages for the ticker.
* The tool extracts headlines and short metadata/summaries and formats them as plain text to be consumed directly or fed into an agent pipeline.
* Designed for quick lookups; it is not a full news-aggregation system.

## Feature summary

| Feature        | Details                                                                          |
| -------------- | -------------------------------------------------------------------------------- |
| Input          | A stock ticker symbol (e.g., `NVDA`)                                             |
| Output         | Plain text containing headline(s) and short summaries                            |
| Source         | Yahoo Finance news pages (e.g., `https://finance.yahoo.com/quote/<TICKER>/news`) |
| Typical fields | Headline, short summary/status (close price, percent change)                     |
| Use cases      | Real-time agent context, stock research assistants, quick news checks            |

## Why it is useful

* Adds timely news context to trading agents or research workflows.
* Helps agents detect sentiment shifts or material events that may influence decisions.
* Lightweight and easy to integrate into a toolchain or agent toolkit.

## Best practices

* Cache results to reduce repeated scraping for the same ticker within short time windows.
* Implement error handling and retries for transient network errors.
* Combine with price/time-series tools for richer decision-making context rather than relying on headlines alone.

## Notes and considerations

> **lightbulb** The tool scrapes publicly available pages on Yahoo Finance. Be mindful of rate limits and Yahoo's terms of service. Because scraped content can change rapidly, consider caching results and adding robust network error handling in production systems.

> **warning** This tool is a scraper of third‑party web pages. Always review Yahoo Finance's terms of service before using scraped data in production, and avoid excessive request rates. For high-volume or commercial use, seek official APIs or licensing options.

## Links and references

* [Yahoo Finance](https://finance.yahoo.com/)
* [KodeKloud — AI Agents course](https://learn.kodekloud.com/user/courses/ai-agents)

Use this tool as part of a balanced data strategy: combine headlines with authoritative APIs, price data, and internal models to make informed decisions.

- [Watch Video](https://learn.kodekloud.com/user/courses/langchain/module/06905b96-585d-4c9e-835a-d8fcaca76e2a/lesson/4bc275cc-00ed-474e-b48c-dc83b001b510)
