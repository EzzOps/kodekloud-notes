# python
from dotenv import load_dotenv
import os

load_dotenv()  # loads environment variables from .env into os.environ
```

Then import the remaining dependencies:

```python theme={null}
# python
import asyncio
import pandas as pd
from pathlib import Path

from agents import Agent, Runner, WebSearchTool, trace
```

Define the list of favorite stocks we want to track:

```python theme={null}
# python
fav_stocks = ["Google", "Apple", "Nvidia"]
```

## 2 — Main logic

Below is a single consolidated async function that:

1. Creates an `Agent` with the `WebSearchTool`.
2. For each stock:
   * searches the web and requests one recent update in a single sentence,
   * extracts the summary,
   * asks the agent to classify sentiment (positive / neutral / negative),
   * maps the sentiment to an emoji,
   * extracts a source link if available,
   * appends the result to the `results` list.
3. Converts the list to a pandas `DataFrame` and exports it to Excel (both the current working directory and the user's Downloads folder when possible).

```python theme={null}
# python
async def main():
    agent = Agent(
        name="Stock News Expert",
        instructions="You are a stock news expert. Review the most recent news on these stocks/companies and provide concise answers.",
        tools=[WebSearchTool(user_location={"type": "approximate", "city": "New York City"})],
    )

    results = []

    with trace("Stock news summary"):
        for stock in fav_stocks:
            query = f"Search the web for news about '{stock}' and give me 1 recent update in a sentence."
            result = await Runner.run(agent, query)
            summary = (result.final_output or "").strip()

            # Ask for sentiment and expect only: positive, neutral, or negative
            sentiment_query = (
                f"What is the sentiment of this sentence? '{summary}' "
                "Answer only with: positive, neutral, or negative."
            )
            sentiment_result = await Runner.run(agent, sentiment_query)
            sentiment = (sentiment_result.final_output or "").strip().lower()

            # Map sentiment to an emoji for quick visual scanning
            sentiment_emoji = {
                "positive": "✅",
                "neutral": "😐",
                "negative": "❌",
            }
            sentiment_display = f"{sentiment.capitalize()} {sentiment_emoji.get(sentiment, '')}"

            # Extract a link from sources if present
            link = None
            if hasattr(result, "sources") and result.sources:
                try:
                    # result.sources is often a list of source dicts; attempt to get a URL
                    if isinstance(result.sources, list) and result.sources:
                        link = result.sources[0].get("url")
                    elif isinstance(result.sources, dict):
                        link = result.sources.get("url")
                except Exception:
                    link = None

            results.append({
                "Stock": stock,
                "News": summary,
                "Sentiment": sentiment_display,
                "Link": link
            })

    # Convert results to DataFrame and save to Excel
    df = pd.DataFrame(results)
    filename = "Stock_News_Summary_Pro.xlsx"
    df.to_excel(filename, index=False)
    print(f"News saved to {filename}")

    # Also save a copy to the user's Downloads folder (convenience)
    downloads_path = Path.home() / "Downloads" / filename
    try:
        df.to_excel(downloads_path, index=False)
        print(f"Saved to {downloads_path}")
    except Exception as e:
        print(f"Could not save to Downloads: {e}")
```

<Callout icon="warning">
  The script performs live web searches using the `WebSearchTool`. Expect variability in outputs and occasional missing source links. Monitor API usage and rate limits for your API key to avoid unexpected charges.
</Callout>

## 3 — Running the script

If you are running this as a standalone script, start the async function like this:

```python theme={null}
# python
if __name__ == "__main__":
    asyncio.run(main())
```

If you are in a Jupyter notebook, run the coroutine directly with:

```python theme={null}
# python
await main()
```

## 4 — What the output looks like

When the script finishes you will see the Excel files (if both saves succeeded):

| Location                  | Filename                      |
| ------------------------- | ----------------------------- |
| Current working directory | `Stock_News_Summary_Pro.xlsx` |
| User's Downloads folder   | `Stock_News_Summary_Pro.xlsx` |

Each Excel file contains the following columns:

| Column    | Description                                            | Example                                   |
| --------- | ------------------------------------------------------ | ----------------------------------------- |
| Stock     | The company name being tracked                         | `Apple`                                   |
| News      | The one-sentence recent update returned by the agent   | `Apple announces new AI features in iOS.` |
| Sentiment | Sentiment label with emoji (e.g., "Positive ✅")        | `Positive ✅`                              |
| Link      | Source URL if available (`None` or blank if not found) | `https://example.com/news/article`        |

This output is ready for sorting, filtering, or importing into other analytics tools.

## Links and references

* [OpenAI API keys](https://platform.openai.com/account/api-keys)
* Pandas documentation: [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
* Python asyncio: [https://docs.python.org/3/library/asyncio.html](https://docs.python.org/3/library/asyncio.html)

That’s it — you now have a working stock news tracker that searches headlines, summarizes one recent update per company, classifies sentiment, and exports the results to Excel for later analysis. Hope you enjoyed this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents/module/a433ab93-c13a-4a03-adf7-f89a6f61ced3/lesson/a2ef1e56-45a5-4172-8f3e-f8bc485dbc36" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/ai-agents/module/a433ab93-c13a-4a03-adf7-f89a6f61ced3/lesson/b0b26272-8019-4ea2-b8ba-5aeebd0ac0f8" />
</CardGroup>


# Demo Exploring Computer Tools Playwright

Source: https://notes.kodekloud.com/docs/AI-Agents/Practical-Projects/Demo-Exploring-Computer-Tools-Playwright/page

Shows how to build a Python Playwright browser agent that renders pages, captures screenshots, scrapes text, and summarizes content with GPT-4 in a Jupyter notebook.

Welcome back.

In this lesson we'll build a compact, practical AI browser agent using Python and Playwright. This example shows how to programmatically render a page, capture a screenshot, extract on-page text, and summarize it with GPT-4. Before you begin, review the Playwright documentation for installation details, browser support, device descriptors, and advanced selectors.

<Frame>
  <img alt="This image shows a webpage from the Playwright documentation, specifically the installation page, with sections on how to install Playwright and related learning topics." />
</Frame>

<Callout icon="lightbulb">
  Install Playwright and its browser binaries once per environment. In Jupyter notebooks, prefix shell commands with `!`.
</Callout>

## Installation and imports

Run these commands in a Jupyter notebook cell to install Playwright, its browser binaries, and python-dotenv:

```python theme={null}
!pip install playwright python-dotenv --quiet
!playwright install --quiet
```

Quick reference — common setup commands:

| Task                           | Command                                         |
| ------------------------------ | ----------------------------------------------- |
| Install packages               | `!pip install playwright python-dotenv --quiet` |
| Install Playwright browsers    | `!playwright install --quiet`                   |
| Load environment vars (Python) | `from dotenv import load_dotenv; load_dotenv()` |

Now import the modules you will use and load environment variables:

```python theme={null}
from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
import openai
from IPython.display import Image, display
```

Keep your [OpenAI API key](https://platform.openai.com/docs/guides/api-keys) in an environment variable (for example, `OPENAI_API_KEY`). Set the key for the `openai` library as shown below.

<Callout icon="warning">
  Never commit API keys to source control. Use environment variables or a secrets manager, and avoid printing your key in logs.
</Callout>

```python theme={null}
openai.api_key = os.environ.get("OPENAI_API_KEY")
```

## The browsing-and-summarizing function

Below is a complete asynchronous function you can place in a single Jupyter cell. It:

* launches a headless Chromium browser with Playwright,
* sets a custom user-agent and viewport,
* navigates to a URL and waits for DOMContentLoaded,
* captures and displays a full-page screenshot in the notebook,
* scrapes the first three paragraph elements from the Wikipedia content block (`#mw-content-text p`),
* sends the scraped text to GPT-4 for summarization,
* prints the extracted snippet and the GPT-4 summary.

Place the whole function in one cell and run it.

```python theme={null}
async def browse_and_display_then_summarize(user_agent: str, url: str, viewport: dict):
    """
    Launch Playwright Chromium, visit `url` with provided `user_agent` and `viewport`,
    take a screenshot, scrape the first three paragraphs under #mw-content-text,
    and generate a GPT-4 summary of the scraped text.
    """
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=user_agent,
            viewport=viewport,
        )

        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded")

        # Capture and display screenshot in the notebook
        screenshot_bytes = await page.screenshot(type="png", full_page=True)
        display(Image(data=screenshot_bytes))

        # Scrape the first three paragraph elements from Wikipedia content
        paragraphs = await page.query_selector_all("#mw-content-text p")
        text_content = ""
        for tag in paragraphs[:3]:
            text = await tag.inner_text()
            text_content += text.strip() + "\n\n"

        # Close resources
        await context.close()
        await browser.close()

    # Print a snippet of the extracted text for verification
    print("\nExtracted Wikipedia Text (first 800 chars):\n")
    print(text_content[:800] + ("..." if len(text_content) > 800 else "") + "\n")

    # Ask GPT-4 to summarize the scraped text
    print("\nGPT-4 Summary:\n")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Summarize the given Wikipedia text in plain English."},
            {"role": "user", "content": text_content},
        ],
        temperature=0.5,
    )

    # Extract and print the model's summary
    summary_text = response["choices"][0]["message"]["content"]
    print(summary_text)

    return summary_text
```

## Example: user agent, viewport, and running the agent

Create a user-agent string that simulates an iPhone-like browser and a viewport dictionary that mimics an iPhone 12 resolution. Then run the asynchronous function with `asyncio.run`.

```python theme={null}
