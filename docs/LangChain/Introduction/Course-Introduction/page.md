# Simple output (with Unicode)
print("Hello, I'm Python!")

# Input and assignment
name = input('What is your name?\n')
print(f'Hi, {name}.')
```

Verify the Python installation:

```bash theme={null}
python -V
# Example output:
# Python 3.11.4
```

<Frame>
  <img alt="The image shows a webpage from python.org offering the download of Python 3.11.4 for macOS. It includes a section listing active Python releases and their maintenance statuses." />
</Frame>

## 2) pip and creating a virtual environment

Modern Python installers include pip, which you’ll use to install libraries. Always use a virtual environment to isolate dependencies per project.

Create and activate a virtual environment (Unix/macOS):

```bash theme={null}
python -m venv venv
ls
# venv
source venv/bin/activate
# Your shell prompt will indicate the active venv, e.g. (venv) user@host:~$
```

On Windows (PowerShell):

```powershell theme={null}
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Using a venv prevents global package conflicts and makes dependency management reproducible.

## 3) Install the OpenAI Python package and Jupyter

With the virtual environment activated, install the required packages:

```bash theme={null}
pip install openai jupyter
```

If the wheels are cached, pip will reuse them and the install will be fast.

Tip: consider pinning package versions in a `requirements.txt` for reproducible installs:

```text theme={null}
openai==0.xx.x
jupyter
```

Then install via:

```bash theme={null}
pip install -r requirements.txt
```

## 4) Create an OpenAI API key

1. Sign in to the OpenAI platform: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Create a new API key and give it a descriptive name (e.g., `KodeKloud-dev`).
3. Copy the secret value immediately — you will not be able to view the full secret after you close the dialog.

<Frame>
  <img alt="The image shows the OpenAI platform interface, featuring links to a quickstart tutorial, examples, and sections on building applications and ChatGPT plugins." />
</Frame>

<Frame>
  <img alt="The image shows a webpage where a user is creating a new secret API key, with a dialog box for naming the key." />
</Frame>

<Callout icon="lightbulb">
  Keep your API key secret. Copy it now because you will not be able to see it again after closing the creation dialog.
</Callout>

Example: export the key for the current shell session (do not paste a real key here — use the key you copied):

```bash theme={null}
# Bash / macOS / Linux
export OPENAI_API_KEY="sk-REDACTED-YOUR-KEY-HERE"
```

For PowerShell (temporary for the session):

```powershell theme={null}
$env:OPENAI_API_KEY = "sk-REDACTED-YOUR-KEY-HERE"
```

To persist the key across sessions:

* Add the export line to your shell startup file (e.g., `~/.bashrc`, `~/.zshrc`) on macOS/Linux.
* Or add the PowerShell line to your PowerShell profile for Windows.

<Frame>
  <img alt="The image shows a webpage displaying API key management on the OpenAI platform, with options to create a new secret key and set the default organization." />
</Frame>

<Callout icon="warning">
  Do not commit your API key to version control or paste it into public forums. Use environment variables or a secrets manager for production applications.
</Callout>

## 5) Test the API from the command line (curl)

Use curl to verify the environment and the `OPENAI_API_KEY` variable. This example calls the Chat Completions endpoint (gpt-3.5-turbo) and asks a simple timezone question.

```bash theme={null}
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful AI assistant that answers questions related to timezones."
      },
      {
        "role": "user",
        "content": "If it is 9AM in London, what time is it in Hyderabad? Be concise."
      }
    ]
  }'
```

A typical (abridged) JSON response:

```json theme={null}
{
  "id": "chatcmpl-7hDVmftC9Jqr7aLxW01vXdxJq5D1i",
  "object": "chat.completion",
  "created": 1690534398,
  "model": "gpt-3.5-turbo-0613",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "2:30 PM in Hyderabad"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 43,
    "completion_tokens": 6,
    "total_tokens": 49
  }
}
```

Understanding the `usage` block (prompt\_tokens, completion\_tokens, total\_tokens) helps you optimize prompts and control costs.

## 6) Test from a Jupyter notebook (Python)

Start Jupyter:

```bash theme={null}
jupyter notebook
```

Open a new notebook (e.g., "Test") and run this code in a cell. The code reads the API key from the environment and uses the OpenAI Python client to create a chat completion.

<Frame>
  <img alt="The image shows a Jupyter Notebook interface, with a toolbar and an empty code cell ready for input. The notebook is open in a web browser window titled &#x22;Test.&#x22;" />
</Frame>

```python theme={null}
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI assistant that answers questions related to timezones."
        },
        {
            "role": "user",
            "content": "If it is 9AM in London, what time is it in Hyderabad? Be concise."
        }
    ]
)

print(response)
```

Example returned JSON (abridged):

```json theme={null}
{
  "id": "chatcmpl-7hDXEkgRe0PrrmFlawWjKjxAraTNE",
  "object": "chat.completion",
  "model": "gpt-3.5-turbo-0613",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "It is 2:30 PM in Hyderabad."
      }
    }
  ],
  "usage": {
    "prompt_tokens": 43,
    "completion_tokens": 10,
    "total_tokens": 53
  }
}
```

This confirms:

* Command-line access with curl is functional.
* Python access via the OpenAI client works inside Jupyter.
* The `OPENAI_API_KEY` environment variable is being used correctly.

Next steps: we will dive deeper into tokenization, prompt design, and cost optimization for production-ready applications.

## Links and references

* [OpenAI API Keys & Usage](https://platform.openai.com/account/api-keys)
* [Python Downloads](https://www.python.org/downloads/)
* [Jupyter Documentation](https://jupyter.org/documentation)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/d5e8b9a9-2511-4d5a-881b-aeeedeb44a4d/lesson/66ce9135-5ded-4123-9234-cfb7335f37c1" />
</CardGroup>


# Course Introduction

Source: https://notes.kodekloud.com/docs/LangChain/Introduction/Course-Introduction/page

Introductory course teaching how to build modern AI applications with LangChain, covering models, prompts, chains, memory, tools, agents, and hands-on labs

Welcome to the LangChain course. I'm Janakiram MSV, and I'll be your instructor.

This course teaches you how to build modern AI applications using LangChain — the orchestration framework that helps developers connect large language models (LLMs) to databases, APIs, and the web to create powerful generative AI experiences.

What you'll learn

* Core building blocks of LLM applications (models, inputs, outputs)
* LangChain expression language (LCEL)
* Chains, memory, tools, and agents
* Prompt engineering and output parsing
* Hands-on demos and practical exercises with notebooks

This course highlights common elements across applications like OpenAI ChatGPT, Google Gemini, and Microsoft Copilot and shows how LangChain helps you compose these pieces into full applications.

This course covers modules such as model, input, output, and the LangChain expression language (LCEL).

<Frame>
  <img alt="The image shows a person speaking, wearing a KodeKloud T-shirt, with a presentation slide next to them titled &#x22;Building Blocks of LLM Apps&#x22; and including topics like &#x22;Common Elements&#x22; and &#x22;Key Components of LangChain&#x22;." />
</Frame>

Course format

* Theory lecture: concise explanation of the concept
* Demo: instructor walkthrough implementing the concept
* Practical exercise: hands-on labs managed by KodeKloud

Each topic follows this pattern so you can immediately apply what you learn in the notebooks provided.

Example: Building a simple chat prompt
Below is a compact example that demonstrates how to build a chat prompt template using LangChain prompt primitives and format it with variables like `subject` and `concept`.

```python theme={null}
