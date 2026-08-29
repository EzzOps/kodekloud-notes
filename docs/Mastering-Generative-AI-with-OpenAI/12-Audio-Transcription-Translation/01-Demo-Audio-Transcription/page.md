# Demo Audio Transcription

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Audio-Transcription-Translation/Demo-Audio-Transcription/page

This tutorial teaches how to transcribe audio using OpenAIs Whisper API with a sample audio clip.

In this tutorial, you’ll learn how to transcribe a short audio clip using OpenAI’s Whisper API. We’ve prepared a trimmed MP3 of the first five minutes of Steve Jobs’ Stanford commencement speech for this demo.

## Prerequisites

* Python 3.7+
* An active [OpenAI API key](https://platform.openai.com/account/api-keys)
* `openai` Python package (`pip install openai`)
* `IPython` for in-notebook audio playback (`pip install ipython`)

## 1. Play Audio Locally

Before sending the file to Whisper, verify playback in an IPython environment:

```python theme={null}
import IPython

file_name = "data/jobs.mp3"
IPython.display.Audio(file_name)
```

## 2. Transcribe with Whisper

Whisper currently offers the `whisper-1` model for speech-to-text. Set your API key in the environment, then transcribe:

```python theme={null}
import openai
import os
