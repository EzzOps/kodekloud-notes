# Demo Connecting to Local LLMs

Source: https://notes.kodekloud.com/docs/Cline/Introduction-to-Cline/Demo-Connecting-to-Local-LLMs/page

Guide to connecting Cline to local LLMs like LM Studio and Ollama, configuring runtimes, workflows, and troubleshooting to run models locally for privacy and cost savings.

This guide shows how to connect Cline to local large language models (LLMs) so you can run models on your own machine instead of relying on hosted services. Running local LLMs is useful for experimenting with custom models from sources like [Hugging Face](https://huggingface.co/), reducing API costs, and keeping data on-premises for privacy or compliance.

We cover two common local runtimes: LM Studio and Ollama. Each section shows the configuration steps in Cline, example requests, and troubleshooting tips.

## LM Studio — load and call a local model

[LM Studio](https://lmstudio.ai/) provides a GUI for running LLMs locally and exposes a simple HTTP API. In Cline you select Local LLMs as the provider and point the app at LM Studio’s base URL.

Steps to use LM Studio with Cline:

1. Install and open LM Studio on your machine.
2. Load the model you want to run (for example, Gemma 3 27B — the UI shows context length, GPU settings, and a Load Model button).
3. Start LM Studio’s server and copy the server Base URL into Cline’s Local LLMs settings.
4. Start Cline’s developer server (recommended) so you can view logs while testing requests.

<Frame>
  <img alt="A dark-mode app window (LM Studio) with a modal for loading the &#x22;Gemma 3 27B Instruct QAT&#x22; model, showing context length and GPU settings and a highlighted &#x22;Load Model&#x22; button. The main pane shows a purple robot icon with the text &#x22;No chat selected&#x22; and a &#x22;Create a New Chat&#x22; button." />
</Frame>

Typical LM Studio connection details:

```text theme={null}
Base URL:
http://127.0.0.1:1234

Example model IDs:
meta-llama-3-1-8b-instruct
gemma-3-27b-it-qat
```

Example local workflow in Cline

* User prompt:

```text theme={null}
Create a "Hello World" script in Python.
```

* Cline sends the request to the LM Studio API and returns a proposed file. Example result saved by Cline:

```python theme={null}
