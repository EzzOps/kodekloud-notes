# OpenAI API and Libraries

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Getting-Started-with-OpenAI/OpenAI-API-and-Libraries/page

Programmatic access to OpenAI’s models for integrating GPT features into applications using official SDKs and community libraries.

Programmatic access to OpenAI’s models enables seamless integration of GPT-powered features into your applications. In this guide, we’ll cover how to install and use the official OpenAI SDKs for Python and Node.js, leverage the OpenAI CLI for quick API operations, and explore community-maintained libraries.

## Official SDKs

For the latest SDKs, visit the [OpenAI documentation under “Libraries”](https://platform.openai.com/docs/libraries). Below is a quick overview:

| Language | Package | Install Command      | Documentation                                                              |
| -------- | ------- | -------------------- | -------------------------------------------------------------------------- |
| Python   | openai  | `pip install openai` | [Python SDK Guide](https://platform.openai.com/docs/libraries/python)      |
| Node.js  | openai  | `npm install openai` | [Node.js SDK Guide](https://platform.openai.com/docs/libraries/javascript) |

### Python SDK

#### Installation

```bash theme={null}
pip install openai
```

This single package provides both:

* The Python client library (`import openai`)
* The `openai` CLI tool for tasks like generating completions or fine-tuning models

<Callout icon="triangle-alert">
  Never commit your `OPENAI_API_KEY` in plaintext. Always load it from an environment variable or a secrets manager.
</Callout>

#### Quickstart Example

```python theme={null}
import os
import openai
