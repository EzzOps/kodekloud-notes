# Demo Automatic Language Recognition and Translation

Source: https://notes.kodekloud.com/docs/AI-Agents/Advanced-Agents-Projects/Demo-Automatic-Language-Recognition-and-Translation/page

Asynchronous Python pipeline that transcribes WAV audio, detects language and emotion, translates to English, and generates concise summaries and suggested titles using OpenAI models.

Welcome back.

In this lesson we'll build an asynchronous audio-to-insight pipeline that:

* Accepts a WAV audio file
* Transcribes the audio
* Detects the spoken language and a prevailing emotion/tone
* Translates the transcription into English
* Generates a concise summary and a suggested title

This design separates each step into small, composable async functions so you can reuse or replace individual components (for example swapping models or custom agents).

<Callout icon="lightbulb">
  Store your [OpenAI API key](https://platform.openai.com/account/api-keys) in a `.env` file (for example `OPENAI_API_KEY=<your_key>`). This lesson will load environment variables via [python-dotenv](https://pypi.org/project/python-dotenv/).
</Callout>

Quick overview — Pipeline steps and the corresponding functions:

| Step | Purpose                                     | Function                       |
| ---- | ------------------------------------------- | ------------------------------ |
| 1    | Transcribe WAV audio to text                | `transcribe_audio`             |
| 2    | Detect language and one-word emotional tone | `analyze_language_and_emotion` |
| 3    | Translate text to English                   | `translate_text`               |
| 4    | Produce suggested title and short summary   | `generate_title_and_summary`   |

## Setup and imports

Load environment variables, initialize the OpenAI client, and import utilities. This example uses the modern [OpenAI Python client](https://github.com/openai/openai-python) (`OpenAI()`), plus an assumed `agents` package providing `Agent` and `Runner` as used in the original material.

```python theme={null}
from dotenv import load_dotenv
import os
from pathlib import Path
import asyncio
import re
