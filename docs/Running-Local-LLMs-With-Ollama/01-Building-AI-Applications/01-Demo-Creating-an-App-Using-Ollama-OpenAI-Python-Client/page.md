# Demo Creating an App Using Ollama OpenAI Python Client

Source: https://notes.kodekloud.com/docs/Running-Local-LLMs-With-Ollama/Building-AI-Applications/Demo-Creating-an-App-Using-Ollama-OpenAI-Python-Client/page

Guide to building a Flask AI Poem Generator using the OpenAI Python client and local Ollama backend, covering setup, example code, environment configuration, and production considerations

This guide demonstrates how to structure a small web application that uses the OpenAI Python client to talk to a local Ollama backend (or switch later to OpenAI's hosted API with minimal changes). We’ll build a simple Flask-based AI Poem Generator that sends user prompts to a chat completion endpoint and renders the model's output.

Using a client library (instead of curl) helps keep your app code clean and portable across local development and hosted providers.

<Frame>
  <img alt="A slide titled &#x22;What to expect&#x22; showing bidirectional arrows between an Ollama icon and the OpenAI logo, paired with a Python logo. Two checked items on the right read &#x22;The way of Programming&#x22; and &#x22;Structuring your code.&#x22;" />
</Frame>

## What you’ll need

* Python 3.8+ installed
* Ollama running locally for local development (optional if you target OpenAI hosted APIs)
* Familiarity with virtual environments and Flask

Useful references:

* [OpenAI Python client docs](https://platform.openai.com/docs/api-reference)
* [Ollama docs](https://docs.ollama.ai/) (for running a local model server)
* [Flask documentation](https://flask.palletsprojects.com/)

## Project setup

1. Create a project folder, for example:

```bash theme={null}
mkdir -p ~/code/ollama-app
cd ~/code/ollama-app
```

2. Create and activate a virtual environment:

```bash theme={null}
python -m venv ollama-app
source ollama-app/bin/activate
```

3. Install dependencies:

```bash theme={null}
pip install openai flask python-dotenv
```

4. Open your editor and create `server.py` at the project root.

<Frame>
  <img alt="A screenshot of Visual Studio Code's welcome page showing the &#x22;Visual Studio Code — Editing evolved&#x22; header with Start options (New File, Open, Clone Git Repository) and a Recent files list. The left sidebar shows an Explorer with a folder named &#x22;OLLAMA-APP&#x22; and the right side has a &#x22;Get Started with VS Code&#x22; walkthrough card." />
</Frame>

## server.py — full implementation

This example exposes a single route ("/"): GET renders a small form, POST sends the prompt to the chat completions endpoint using the OpenAI Python client and displays the returned poem.

```python theme={null}
