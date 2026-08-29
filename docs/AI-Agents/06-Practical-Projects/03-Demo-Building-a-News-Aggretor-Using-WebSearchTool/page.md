# Loads variables from .env into the environment during local development
load_dotenv()

# Verify that an API key is present (prints True/False)
print(bool(os.environ.get("OPENAI_API_KEY")))
```

## Simple async agent (illustrative)

This example shows a minimal async agent pattern. Framework APIs differ — adapt to LangChain, CrewAI, AutoGen, or your chosen SDK.

```python theme={null}
import asyncio
from agents import Agent, Runner, WebSearchTool

fav_stock = ["Google", "Apple", "Nvidia"]

async def main():
    agent = Agent(
        name="Stock News Expert",
        instructions=(
            "You are a stock news expert. Review recent news for the given companies "
            "and summarize key events."
        ),
        tools=[WebSearchTool()]  # Provide any necessary tools as a list
    )

    runner = Runner(agent=agent)
    # Run the agent on the list of stock names (frameworks may vary)
    await runner.run(tasks=fav_stock)

if __name__ == "__main__":
    asyncio.run(main())
```

## Utility example — language and emotion detection (OpenAI Chat API)

This synchronous example demonstrates how to call a chat model to parse language and emotional tone. Adapt to your SDK version (e.g., the OpenAI Python SDK or HTTP API). See OpenAI Chat API docs: [https://platform.openai.com/docs/api-reference/chat](https://platform.openai.com/docs/api-reference/chat)

```python theme={null}
import os
import re
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def analyze_language_and_emotion(text: str) -> dict:
    system_msg = (
        "You are an AI that analyzes messages. Detect the language (e.g., English, French) "
        "and describe the emotional tone in one word (e.g., joyful, sad, angry, professional, excited, persuasive). "
        "Respond in the format:\nLanguage: <language>\nEmotion: <emotion>"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Here is the message:\n{text}"}
        ],
        temperature=0.3
    )

    content = response["choices"][0]["message"]["content"].strip()

    language_match = re.search(r"Language:\s*(\w+)", content, re.IGNORECASE)
    emotion_match = re.search(r"Emotion:\s*(\w+)", content, re.IGNORECASE)

    return {
        "language": language_match.group(1) if language_match else "Unknown",
        "emotion": emotion_match.group(1) if emotion_match else "Unknown"
    }
```

## Labs, demos, and practical projects

Hands-on labs guide you from local prototypes to deployable agents. You’ll practice building task-driven agents, multi-role simulations, and integrating external tools and APIs. Labs emphasize reproducibility and safe testing practices.

<Frame>
  <img alt="The image shows a split-screen with a setup interface on the left and a Jupyter Notebook on the right, with a person speaking in a small overlay in the bottom right corner." />
</Frame>

## Quick client initialization (OpenAI Python SDK)

A compact example to initialize an SDK client. If you use an async client or a different vendor, adapt accordingly.

```python theme={null}
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE")  # optional custom base URL
)
```

## Best practices and next steps

* Use small iterative experiments to validate agent behaviors before scaling.
* Log agent actions and decisions for auditing and debugging.
* Evaluate agents with both automated metrics and human review to ensure reliability and safety.
* Integrate secret management, rate-limiting, and cost controls early in your deployment pipeline.

At KodeKloud, we foster an active community where you can ask questions, share code, and collaborate on projects. Join peers and instructors to accelerate your learning.

Let's begin this journey — build with curiosity and guardrails, and unlock what AI agents can do for you.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents/module/69bfe34f-1c9c-4e8b-ac41-4f6038b22625/lesson/6c97089c-d184-4da3-afa5-a3e6f5510353)


# Demo Building a News Aggretor Using WebSearchTool

Source: https://notes.kodekloud.com/docs/AI-Agents/Practical-Projects/Demo-Building-a-News-Aggretor-Using-WebSearchTool/page

Guide to building a stock news aggregator that searches the web for company updates, summarizes one sentence per stock, classifies sentiment, and exports results to Excel

Welcome back.

In this lesson we build a lightweight stock news tracker that:

* searches the web for the latest updates on a list of companies,
* summarizes one interesting story for each company,
* analyzes the sentiment of that summary (positive / neutral / negative),
* exports the aggregated results into a clean Excel file for further review.

Create a new notebook (or script) and name it `Stock News Pro`. Save it and make sure your environment contains your [OpenAI API key](https://platform.openai.com/account/api-keys) (for example, in a `.env` file).

> **lightbulb** Make sure your `.env` contains a valid [API key](https://platform.openai.com/account/api-keys) (for example `OPENAI_API_KEY=...`). This lesson uses an agents package that provides an Agents SDK and a `WebSearchTool` to perform live web queries.

## Overview

This guide is organized into four clear steps:

1. Setup and imports
2. Main logic (single async function that performs search, summarize, classify, and collect)
3. Running the script (script vs. notebook)
4. Output format and where files are saved

Follow the sections below to implement the tracker end-to-end.

## 1 — Setup and imports

Load environment variables and import the core libraries:

```python theme={null}
