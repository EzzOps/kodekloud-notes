# example_tavily_search.py
from langchain_community.tools.tavily_search import TavilySearchResults
import os

# Optionally read the env var in code (not required if the wrapper reads it internally)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize the tool (wrapper may read TAVILY_API_KEY automatically)
tool = TavilySearchResults()

# Perform a search
response = tool.invoke({"query": "When is ICC Men's T20 World Cup 2024 starting?"})

# Inspect the response
print(type(response))         # typically a list
print(len(response))          # default number of results (usually 5)
print(response[0]['url'])     # first result URL
print(response[0]['content']) # first result content snippet
```

Example of the returned structure

* The `invoke` method returns a list of dictionaries. Each dictionary typically includes `url` and `content` keys (snippet of the page).
* Example (trimmed):

```json theme={null}
[
  {
    "url": "https://www.espncricinfo.com/series/icc-men-s-t20-world-cup-2024-1411166/match-schedule-fixtures-and-results",
    "content": "Get 2024 T20 World Cup schedule, fixtures, scorecard updates, and results on ESPNcricinfo. Track latest match scores, schedule, and results of ICC Men's T20 World Cup 2024."
  },
  {
    "url": "https://www.skysports.com/cricket/news/12123/13042693/icc-mens-t20-cricket-world-cup-2024-fixtures-schedule-and-start-times-with-all-matches-live-on-sky-sports",
    "content": "Group D - Sri Lanka vs Bangladesh (Dallas)\nSaturday June 8\nGroup A - Netherlands vs South Africa (New York)\nGroup B - Australia vs England (Barbados)\nSunday June 9\nGroup A - India vs Pakistan (New York)"
  }
]
```

Result fields summary

| Field     | Description                                             | Example                                                            |
| --------- | ------------------------------------------------------- | ------------------------------------------------------------------ |
| `url`     | Source page URL for the search result                   | `https://example.com/article`                                      |
| `content` | Text snippet or extract from the page (use for context) | `"Match schedule and results for ICC Men's T20 World Cup 2024..."` |

Combining and chunking results for RAG

* The default response often returns five results. Aggregate and chunk `content` fields, then include the most relevant chunks (with URLs) as context in your LLM prompt.
* Example: join all content into one string before chunking or indexing.

```python theme={null}
all_text = "\n\n".join(r["content"] for r in response)
sources = [r["url"] for r in response]

print("Combined text length:", len(all_text))
print("Sources:", sources)
```

Best practices and tips

* Prioritize relevance: sort or filter results by relevance before concatenating content.
* Chunking: split large combined text into smaller chunks that respect your LLM context window.
* Citation: always include source URLs in your final output so results are verifiable.
* Rate limits: respect Tavily's API rate limits; implement retries and backoff where appropriate.
* Security: keep API keys in secrets management (environment variables, secret managers, or vaults).

<Callout icon="warning">
  Never commit your `TAVILY_API_KEY` (or any secret) to version control. Use environment variables or a secrets manager in production to avoid accidental exposure.
</Callout>

Integrations and next steps

* Use Tavily results directly in prompts for short answers (with citations).
* For larger systems, index the returned snippets into a vector store and perform semantic retrieval before calling your LLM.
* Integrate the tool into a LangChain toolset or agent to automate search-and-answer workflows.

Further reading and references

* LangChain community tools and integration examples: [https://learn.kodekloud.com/user/courses/langchain](https://learn.kodekloud.com/user/courses/langchain)
* LangChain tools documentation: [https://python.langchain.com/](https://python.langchain.com/)

Key takeaways

* Tavily provides search results optimized for LLM-driven RAG workflows.
* Store your API key securely and use the `TavilySearchResults` wrapper to fetch structured results.
* Aggregate, chunk, and cite returned `content` and `url` fields when constructing LLM context for accurate, up-to-date answers.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/06905b96-585d-4c9e-835a-d8fcaca76e2a/lesson/539b06ca-74c9-4105-a342-f3d2444affb0" />
</CardGroup>


# Using Wikipedia Tool

Source: https://notes.kodekloud.com/docs/LangChain/Using-Tools/Using-Wikipedia-Tool/page

Guide to using LangChain's Wikipedia integration, showing configuration, API wrapper and tool usage, parameters, examples, and recommendations for retrieval augmented generation workflows.

In this lesson we review the Wikipedia integration in LangChain and show how to use the Wikipedia tool programmatically. The Wikipedia tool is useful for retrieving topical summaries, facts, and reference text that you can pass into an LLM or a retrieval-augmented generation (RAG) pipeline.

LangChain provides many integrations under the "Integrations" section of the docs: [https://docs.langchain.com](https://docs.langchain.com). Common examples include:

* Shell execution (e.g., [Bash](https://www.gnu.org/software/bash/))
* Web search providers ([Bing](https://www.bing.com), custom search APIs)
* ChatGPT plugins
* Image generation ([DALL·E](https://openai.com/dall-e))
* Cloud storage and document sources ([Google Drive](https://drive.google.com))
* Notification services ([Twilio](https://www.twilio.com))
* Knowledge sources ([Wikipedia](https://www.wikipedia.org), [YouTube](https://www.youtube.com), [Yahoo Finance](https://finance.yahoo.com))
* Human-in-the-loop tools (allowing workflows that prompt a human to act)

Quick integrations reference:

| Integration category |                          Use case | Example                                  |
| -------------------- | --------------------------------: | ---------------------------------------- |
| Shell / CLI          | Execute shell commands or scripts | `bash`                                   |
| Web search           |        Find and fetch web content | `Bing`, custom search APIs               |
| Image generation     |        Create images from prompts | [DALL·E](https://openai.com/dall-e)      |
| Cloud storage        |  Read documents from cloud drives | [Google Drive](https://drive.google.com) |
| Notifications        |             Send SMS/email alerts | [Twilio](https://www.twilio.com)         |
| Knowledge sources    |          Retrieve factual content | [Wikipedia](https://www.wikipedia.org)   |

All of the above are available as Python modules you can import and use directly. Below we demonstrate the Wikipedia tool and how to call it.

## Wikipedia tool: wrapper vs tool

The Wikipedia integration in LangChain is exposed in two layers:

* A utility wrapper (e.g., `WikipediaAPIWrapper`) that handles fetching pages and returning text.
* A tool wrapper (e.g., `WikipediaQueryRun`) that exposes a `run` interface used by agents or programmatic calls.

The wrapper supports configuration parameters such as `top_k_results` (how many search results to fetch) and `doc_content_chars_max` (limits the number of characters returned for each page). These let you balance coverage versus token usage when passing content to an LLM.

Parameter quick reference:

| Parameter               | Type    | Description                                 | Example |
| ----------------------- | ------- | ------------------------------------------- | ------- |
| `top_k_results`         | integer | Maximum number of search results to fetch   | `1`     |
| `doc_content_chars_max` | integer | Maximum characters to return from each page | `1000`  |

## Minimal example: import, configure, inspect, and call

Here is a concise example that demonstrates how to import, configure, inspect metadata, and call the Wikipedia tool:

```python theme={null}
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
