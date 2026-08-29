# Project 2 Translating an Article

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Text-Generation/Project-2-Translating-an-Article/page

Build an article translation tool using OpenAI's chat completion API to translate foreign-language articles into English.

Translate any foreign‐language article into English using OpenAI’s chat completion API. In this tutorial, you’ll:

1. Set up the OpenAI Python client
2. Load the article text into a variable
3. Craft a translation prompt
4. Implement an `article_translator` function
5. Execute the function and display the result

***

## 1. Prerequisites

* Python 3.7+
* An [OpenAI API key](https://platform.openai.com/account/api-keys)
* The `openai` Python package installed:
  ```bash theme={null}
  pip install openai
  ```

<Callout icon="triangle-alert">
  Never hard-code your API key in source files. Use environment variables or a secrets manager:

  ```bash theme={null}
  export OPENAI_API_KEY="sk-..."
  ```
</Callout>

***

## 2. Initialize the OpenAI Client

Import and configure the client with your API key.

```python theme={null}
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

***

## 3. Prepare the Article Text & Prompt

Chat models cannot fetch URLs directly, so load your article content into a string. Later, you can extend this for web scraping or file input.

```python theme={null}
