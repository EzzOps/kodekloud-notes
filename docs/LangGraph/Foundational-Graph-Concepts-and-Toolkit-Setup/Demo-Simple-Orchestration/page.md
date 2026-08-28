# Core dependencies
pip install --upgrade langgraph langchain openai

# Optional utilities (recommended)
pip install --upgrade tqdm rich langsmith python-dotenv
```

## Virtual environments

Use a virtual environment to isolate dependencies. Two common approaches:

Using venv (standard library):

```bash theme={null}
python -m venv .venv

# Activate:
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Using Conda:

```bash theme={null}
conda create -n langgraph-env python=3.10 -y
conda activate langgraph-env
```

## API keys and secure storage

To call OpenAI models (e.g., GPT-4, GPT-3.5), you need an API key from the OpenAI dashboard: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

Important best practices:

* Never hard-code API keys in source files.
* Use environment variables or a secrets manager for production.
* For local development, use a `.env` file with `python-dotenv` and add `.env` to `.gitignore`.

Example `.env` file:

```text theme={null}
OPENAI_API_KEY=[OPENAI_API_KEY]
```

Load it in Python:

```python theme={null}
from dotenv import load_dotenv
load_dotenv()
```

<Callout icon="lightbulb">
  Store secrets in environment variables or a secure secrets manager. Use `python-dotenv` only for local development; never commit `.env` to version control.
</Callout>

Recommended project layout

* Keep an organized layout from the start. Example structure:

```text theme={null}
my-project/
├─ notebooks/         # Jupyter notebooks for experiments
├─ src/               # Reusable code and utilities
├─ data/              # Any data files
├─ .env               # Local environment variables (gitignored)
└─ README.md
```

<Frame>
  <img alt="The image is a slide featuring the title &#x22;API Keys and Setup&#x22; alongside the logos for OpenAI ChatGPT 4.0 and LangSmith." />
</Frame>

## Quick system test

Create a lightweight script to validate imports, verify the OpenAI API key is present, and make a minimal Chat API call. Save this as `system_test.py` and run it after activating your virtual environment and setting `OPENAI_API_KEY` or creating a `.env`.

```python theme={null}
# system_test.py
import os
import sys

# Optional: load .env for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Check Python version
print("Python:", sys.version.splitlines()[0])

# Import and check core packages
try:
    import langgraph
    print("langgraph: imported", getattr(langgraph, "__version__", "version unknown"))
except Exception as e:
    print("langgraph: import failed:", e)

try:
    import langchain
    print("langchain: imported", getattr(langchain, "__version__", "version unknown"))
except Exception as e:
    print("langchain: import failed:", e)

try:
    import openai
    print("openai: imported", getattr(openai, "__version__", "version unknown"))
except Exception as e:
    print("openai: import failed:", e)

# Verify OpenAI API key is set
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("OPENAI_API_KEY is not set. Set it as an environment variable or in a .env file.")
    sys.exit(1)

openai.api_key = api_key

# Make a minimal test call to the Chat API (use gpt-3.5-turbo to reduce likelihood of missing access)
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": "Say hello in one sentence."}],
        max_tokens=50,
        temperature=0.0,
    )
    reply = response.choices[0].message.content.strip()
    print("OpenAI call successful. Model reply:", reply)
except Exception as e:
    print("OpenAI call failed:", e)
    sys.exit(1)
```

Expected minimal output (example):

```bash theme={null}
Python: 3.10.12 (or similar)
langgraph: imported version unknown
langchain: imported 0.x.x
openai: imported x.y.z
OpenAI call successful. Model reply: Hello! I'm here to help.
```

<Callout icon="warning">
  Using the OpenAI API may incur charges. Monitor usage and billing in your OpenAI dashboard, and prefer small test calls when validating integration.
</Callout>

If the script runs and the OpenAI call succeeds, your development environment is ready for the rest of the LangGraph material. If you see import errors, confirm your virtual environment is activated and the packages installed without errors.

Additional references

* OpenAI API keys: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
* Python virtual environments: [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)
* Conda docs: [https://docs.conda.io/](https://docs.conda.io/)
* LangChain docs: [https://docs.langchain.com/](https://docs.langchain.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-2a76-40f7-be25-905be94f24f8/lesson/f9665406-3363-428f-9b22-b558cb0ddf71" />
</CardGroup>


# Demo Simple Orchestration

Source: https://notes.kodekloud.com/docs/LangGraph/Foundational-Graph-Concepts-and-Toolkit-Setup/Demo-Simple-Orchestration/page

Minimal tutorial showing how to orchestrate a typed-state LLM call using LangGraph with the OpenAI Responses API

This lesson demonstrates a minimal, production-accurate example of using LangGraph to orchestrate a single LLM call via the OpenAI Responses API. The objective is to show:

* LangGraph's execution model and how a typed state flows through a node.
* How nodes return partial updates that are merged into a global state.
* How to wire a real model call cleanly and composably.

This example is intentionally minimal so you can extend it later with routing, tools, memory, retries, or observability.

<Callout icon="lightbulb">
  Ensure you have an OpenAI API key and the required packages installed. The examples below use the modern OpenAI Responses API via the OpenAI Python client and LangGraph.
</Callout>

## Quick setup

Install the dependencies (uncomment if running in a fresh environment):

```bash theme={null}
