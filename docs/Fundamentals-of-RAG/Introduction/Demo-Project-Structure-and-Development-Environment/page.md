# downloads the model but does not start it
```

```bash theme={null}
C:\Users\jerem>ollama run qwen3:0.6b
pulling manifest
pulling 7f4030143c1c: 96%                     ...
# when download completes, you'll be placed into the model prompt
```

Once the `run` command finishes downloading, you'll be dropped into the model prompt and can start sending input (for example, "Tell me a funny joke about Python").

## Model catalog (web)

Browse available models, sizes, and suggested CLI commands at ollama.com/models. The web catalog is a good place to discover model details and recommended usage examples.

<Frame>
  <img alt="The image shows a webpage from ollama.com listing several AI models, each with descriptions, update information, and details on their characteristics and performance metrics." />
</Frame>

## Example model detail page (qwen3:0.6b)

Model detail pages show specifications and provide a copyable "Run" or "Pull" command for convenience.

<Frame>
  <img alt="The image shows a webpage for a language model called &#x22;qwen3:0.6b&#x22; on the Ollama platform, including details about downloads, model specifications, and parameters. There's also a visual with a cartoon bear labeled &#x22;Qwen3.&#x22;" />
</Frame>

## Monitoring and stopping models

* `ollama list` — models downloaded to your machine.
* `ollama ps` — currently running models and resource usage.
* `ollama stop <name>` — stop a running model.

Example outputs:

```bash theme={null}
C:\Users\jerem>ollama list
NAME               ID                SIZE    MODIFIED
qwen3:0.6b         7df6b6e09427      522 MB  43 seconds ago
deepseek-r1:latest 6995872bfe4c      5.2 GB  22 hours ago
gemma3:4b          a2af6cc3eb7f      3.3 GB  22 hours ago
```

```bash theme={null}
C:\Users\jerem>ollama ps
NAME         ID                SIZE     PROCESSOR  CONTEXT  UNTIL
qwen3:0.6b   7df6b6e09427      5.4 GB   100% GPU   32768    4 minutes from now
```

To stop a running model:

```bash theme={null}
C:\Users\jerem>ollama stop qwen3:0.6b
Stopping qwen3:0.6b...
C:\Users\jerem>ollama ps
# (no running models shown)
```

<Callout icon="warning">
  Locally running models can be resource intensive. If a model uses GPU resources, ensure your drivers and CUDA runtime are compatible. Also note the Ollama API defaults to `127.0.0.1:11434` (local only) — exposing this port to untrusted networks can be a security risk.
</Callout>

## Notes on model behavior and tuning

* Repetitive or very long outputs can usually be controlled by adjusting `temperature`, `top_p`, and stop tokens.
* Use clear prompts and explicit stop tokens to avoid unbounded generation.
* For deterministic or concise replies, lower `temperature` (e.g., `0.0–0.3`) and specify stop tokens.
* For more creative output, raise `temperature` and increase `top_p`.

## Next steps

* Programmatic usage: call the local Ollama HTTP API at `127.0.0.1:11434` from your application.
* Integrations: embed local models in microservices, chat UIs, or data pipelines.
* Explore the model catalog: [https://ollama.com/models](https://ollama.com/models) for more models, sizes, and recommended CLI commands.

Further reading and references:

* Ollama website: [https://ollama.com/](https://ollama.com/)
* Model catalog: [https://ollama.com/models](https://ollama.com/models)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/18c192ac-9730-42f7-9dbf-6c67f9ceeb61/lesson/69efc62d-e0ef-4e1b-a474-a6c762de50ab" />
</CardGroup>


# Demo Project Structure and Development Environment

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Introduction/Demo-Project-Structure-and-Development-Environment/page

Guide to setting up a Python project with the Ollama client, creating a virtual environment, and running single-shot generation and context-aware chat examples against a local Ollama server.

This guide shows how to set up a minimal Python project that communicates with a locally running Ollama server. You’ll create a virtual environment, install the official Ollama Python client, and run two example scripts:

* A single-request text generation (one-shot prompt)
* A context-aware chat loop that preserves conversation history

Environment note: this walkthrough was performed in Visual Studio Code on Windows using WSL. Your Ollama instance should be running locally and have at least one model available:

```bash theme={null}
jeremy@LEGION:/mnt/c/Users/jerem/Projects/ollama-test$ ollama list
NAME           ID             SIZE     MODIFIED
gemma3:latest  a2af66c2b7f    3.3 GB   6 hours ago
```

If you need general documentation, see the Ollama docs and Python venv docs:

* [Ollama documentation](https://docs.ollama.ai/)
* [Python venv documentation](https://docs.python.org/3/library/venv.html)

## 1) Create and activate a virtual environment

From your project directory create a virtual environment with Python 3:

```bash theme={null}
python3 -m venv venv
```

Activate the virtual environment:

* WSL / macOS / Linux:

```bash theme={null}
source venv/bin/activate
```

* Windows (PowerShell):

```powershell theme={null}
.\venv\Scripts\Activate.ps1
```

Quick reference commands:

| Purpose                       | Command                       |
| ----------------------------- | ----------------------------- |
| Create venv                   | `python3 -m venv venv`        |
| Activate (WSL/macOS/Linux)    | `source venv/bin/activate`    |
| Activate (Windows PowerShell) | `.\venv\Scripts\Activate.ps1` |
| Deactivate                    | `deactivate`                  |

## 2) Install the Ollama Python client

With the venv active, install the client:

```bash theme={null}
pip install ollama
```

<Callout icon="lightbulb">
  The Ollama Python package is a lightweight HTTP client that sends requests to your locally running Ollama background process. The package does not run models locally; it forwards requests to the Ollama server.
</Callout>

## 3) Simple generation example (single prompt)

Create a file named `main.py` and add:

```python theme={null}
import ollama
