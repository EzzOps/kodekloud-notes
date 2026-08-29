# OpenAI Python client
from openai import OpenAI

# Optional display in notebooks
from IPython.display import Image, display

# Agent & Runner (kept as in the original content)
from agents import Agent, Runner

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

<Callout icon="warning">
  Be mindful of API usage and costs when using large models like `gpt-4` and uploading audio files. Use lower-cost models for development and testing if desired.
</Callout>

## Transcription (Whisper)

We create an async helper to upload a WAV file to the Whisper transcription model and return the transcription text. The function validates the path and handles common return shapes from the client.

```python theme={null}
async def transcribe_audio(file_path: str) -> str:
    """
    Transcribe a WAV file using the Whisper model and return the transcription text.
    """
    # Ensure the file exists
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    # The client returns an object with a text attribute for the transcript
    return getattr(transcript, "text", transcript.get("text") if isinstance(transcript, dict) else None)
```

Reference: Whisper docs — [https://platform.openai.com/docs/models/whisper-1](https://platform.openai.com/docs/models/whisper-1)

## Language and Emotion Analysis

Use a chat model to detect the language and provide a one-word emotional descriptor. The function uses a deterministic temperature (0.3) and extracts values using tolerant regular expressions to handle slightly varied replies.

```python theme={null}
async def analyze_language_and_emotion(text: str) -> dict:
    """
    Ask a chat model to detect the language and a one-word emotional tone for the given text.
    Returns: {"language": "<language>", "emotion": "<emotion>"}
    """
    system_msg = (
        "You're an AI that analyzes messages. Detect the language (e.g., English, French) "
        "and describe the emotional tone in one word (e.g., joyful, sad, angry, professional, excited, persuasive). "
        "Respond in the format:\nLanguage: <language>\nEmotion: <emotion>"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Here is the message:\n{text}"}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()

    # Tolerant regex to capture "Language: ..." and "Emotion: ..." (allow multi-word and punctuation)
    language_match = re.search(r"(?i)^\s*Language[:\-\s]*([^\r\n]+)", content, re.MULTILINE)
    emotion_match = re.search(r"(?i)^\s*Emotion[:\-\s]*([^\r\n]+)", content, re.MULTILINE)

    return {
        "language": language_match.group(1).strip() if language_match else "Unknown",
        "emotion": emotion_match.group(1).strip() if emotion_match else "Unknown"
    }
```

Note: temperature is set to 0.3 to favor more deterministic outputs, which helps reliable parsing of the model response.

## Translator Agent and translate\_text

This example uses a simple Agent to translate text into English and a Runner to execute it. The Agent/Runner implementation is assumed from the original content; if your agents package returns different shapes, adapt the result extraction accordingly.

```python theme={null}
translator_agent = Agent(
    name="Translator",
    instructions="Translate the input text into English. Only return the translated result."
)

async def translate_text(text: str) -> str:
    """
    Use the Agent Runner to translate text into English.
    Returns the final translated string returned by the agent.
    """
    result = await Runner.run(translator_agent, input=text)
    # Handle common return shapes: string, object with attribute, or dict
    if isinstance(result, str):
        return result
    return getattr(result, "final_output", result.get("final_output") if isinstance(result, dict) else None)
```

If your agents/runner implementation differs, adapt the return extraction accordingly.

## Title and Summary Generation

Ask a chat model to provide a concise summary and a suggested title. Temperature is slightly higher for creativity (0.5).

```python theme={null}
async def generate_title_and_summary(text: str) -> str:
    """
    Generate a concise summary and a suggested title for the given text.
    Returns a string containing both title and summary.
    """
    system_msg = "You are a helpful AI assistant. Summarize the user's message and suggest a title for it."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Here's the text:\n\n{text}"}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content.strip()
```

Tip: If you prefer structured outputs (e.g., JSON with `title` and `summary`), ask the model to respond in JSON and parse the result. For simple display, the free-text response above often suffices.

## Full pipeline: process\_audio\_translation

This orchestrator composes the previous functions into a complete asynchronous flow. Each step's output is printed; you can replace prints with logging, storage, or event emissions for production usage.

```python theme={null}
async def process_audio_translation(file_path: str):
    """
    Full pipeline for an audio file:
      1. Transcribe audio
      2. Analyze language and emotion
      3. Translate into English
      4. Generate title and summary
    Prints each result step to the console.
    """
    # 1) Transcribe
    transcript = await transcribe_audio(file_path)
    print(f"Transcript:\n{transcript}\n")

    # 2) Language & emotion analysis
    analysis = await analyze_language_and_emotion(transcript)
    print(f"Detected language: {analysis['language']}")
    print(f"Detected emotion: {analysis['emotion']}\n")

    # 3) Translate to English
    translation = await translate_text(transcript)
    print(f"Translation:\n{translation}\n")

    # 4) Title & summary
    extras = await generate_title_and_summary(translation)
    print(f"Title and Summary:\n{extras}\n")
```

## Run the pipeline

Pass in the full path to your WAV file. In Jupyter or other async-capable REPLs you can `await` the function directly.

```python theme={null}
# Replace with the path to your WAV file
audio_path = "/Users/gavinridgeway/Documents/Anaconda/AiAgent/final_fixed.wav"

await process_audio_translation(audio_path)
```

If running from a standard Python script, wrap the call in asyncio:

```python theme={null}
if __name__ == "__main__":
    audio_path = "/path/to/your/file.wav"
    asyncio.run(process_audio_translation(audio_path))
```

## Troubleshooting common issues

* File not found: ensure the `file_path` is correct and accessible by your process.
* UnboundLocalError or NameError: double-check variable names and that you return the expected attributes (for example `result.final_output`).
* API key errors: confirm `OPENAI_API_KEY` is set and loaded via `load_dotenv()` or environment variables.
* Agent/Runner differences: the `agents` package usage (Agent, Runner) is retained from the original content — adapt `Runner.run()` and result access if your agents library returns different shapes.
* Unexpected model output format: prefer instructing the model to respond in a strict format (for example `Language: <language>\nEmotion: <emotion>` or JSON), then validate with regex or a JSON parser.

## Example output (expected)

After running on a French sample, the pipeline prints something like:

* Transcript: "Apprendre à programmer, c'est comme avoir un super-pouvoir..."
* Detected language: French
* Detected emotion: Encouraging
* Translation: "Learning to program is like having a superpower..."
* Title and Summary: (a short summary and a suggested title)

You now have a working asynchronous pipeline that transcribes audio, detects language and emotion, translates into English, and generates a title plus a short summary.

## Links and References

* [OpenAI API docs](https://platform.openai.com/docs/)
* Whisper model: [https://platform.openai.com/docs/models/whisper-1](https://platform.openai.com/docs/models/whisper-1)
* GPT models: [https://platform.openai.com/docs/models](https://platform.openai.com/docs/models)
* [python-dotenv](https://pypi.org/project/python-dotenv/)
* Jupyter: [https://jupyter.org](https://jupyter.org)

If you want to extend this pipeline: consider adding speaker diarization, punctuation normalization, or persisting outputs to a database for downstream search and analytics.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents/module/05e40a2e-53c7-4eff-8df8-6aee856da058/lesson/3ab717f6-b27d-4258-920b-ef6f63b356d5" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/ai-agents/module/05e40a2e-53c7-4eff-8df8-6aee856da058/lesson/ee5a9e22-e696-4ec5-a2a2-1a1e16e98922" />
</CardGroup>


# Demo Building a Multi Agent System

Source: https://notes.kodekloud.com/docs/AI-Agents/Advanced-Agents-Projects/Demo-Building-a-Multi-Agent-System/page

Guide to building a recruiter multi agent system that extracts job keywords, scans PDF resumes, transcribes interviews, analyzes alignment, and orchestrates tools into a consolidated report

Welcome back. In this lesson we’ll build a practical multi‑agent system that helps a recruiter automate screening and interview analysis.

What is a multi‑agent system?

A multi‑agent system is composed of multiple specialized agents (or tools), each with a narrow role. Agents coordinate by passing tasks or data downstream, while a coordinator (or orchestrator) agent controls the overall workflow and composes a final result.

Project overview

We’ll assemble a recruiter-focused system that does the following:

* Extract relevant skills and responsibilities from a job description.
* Scan local PDF resumes for matches to those skills.
* Transcribe an interview audio file and analyze whether the interview questions align with the job posting.
* Produce a consolidated report with extracted keywords, resume matches, and interview relevance feedback.

This guide contains the end-to-end implementation and an example runner to execute the workflow.

<Callout icon="lightbulb">
  Ensure your environment variables are configured (for example via a `.env` file). Set your OpenAI API key at a minimum. Also update `RESUME_DIR` and `INTERVIEW_AUDIO_PATH` to match your local filesystem.
</Callout>

## Table: Tools and Responsibilities

| Tool name                               | Responsibility                                                       | Returns / Example                                                                        |
| --------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `extract_keywords_from_job_description` | Extract 10–15 skills, tools, responsibilities from a job description | `["Python","React","REST APIs", ...]`                                                    |
| `scan_resumes_for_keywords`             | Scan all PDF resumes in `RESUME_DIR` and return matches              | `[{ "filename": "resume.pdf", "keyword": "Python", "match_snippet": "...", "page": 2 }]` |
| `transcribe_interview`                  | Transcribe interview audio using OpenAI speech-to-text               | `"Full transcript text..."`                                                              |
| `analyze_interview_relevance`           | Compare transcript to job description and return recommendations     | `"Assessment: ... actionable suggestions ..." `                                          |

## Imports and configuration

Start by loading environment variables and importing required libraries. Adjust imports if your project uses different modules or versions.

```python theme={null}
from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
import re
from pathlib import Path

from agents import Agent, Runner, ModelSettings
from agents.tool import function_tool

import fitz  # PyMuPDF for reading PDFs
import openai
```

Set the resume directory and other paths (update to suit your environment):

```python theme={null}
RESUME_DIR = Path("/Users/gavinridgeway/Documents/Anaconda/AiAgent/Resume")
```

## Tool 1 — Scan resumes for keywords

This tool opens each PDF in `RESUME_DIR`, searches for each keyword (case-insensitive), and returns matches containing filename, keyword, surrounding snippet, and page number.

```python theme={null}
@function_tool(name_override="scan_resumes_for_keywords")
def scan_resumes_for_keywords(keywords: list[str]) -> list[dict]:
    """
    Scan all PDF resumes in RESUME_DIR for keyword occurrences.

    Returns a list of dicts:
    [
      {
        "filename": "resume.pdf",
        "keyword": "Python",
        "match_snippet": "...context around the match...",
        "page": 2
      },
      ...
    ]
    """
    results: list[dict] = []

    for file in RESUME_DIR.glob("*.pdf"):
        try:
            doc = fitz.open(str(file))
        except Exception as e:
            # Skip files that can't be opened
            continue

        for page in doc:
            text = page.get_text() or ""
            for kw in keywords:
                idx = text.lower().find(kw.lower())
                if idx >= 0:
                    start = max(0, idx - 75)
                    snippet = text[start:start + 250].strip()
                    results.append({
                        "filename": file.name,
                        "keyword": kw,
                        "match_snippet": snippet,
                        "page": page.number + 1
                    })
        doc.close()

    return results
```

Best practices:

* Normalize keywords before searching to improve match quality.
* Consider using more advanced NLP (lemmatization, fuzzy matching) for improved recall.

## Tool 2 — Extract keywords from a job description

Use the LLM to extract 10–15 focused skills, tools, and responsibilities. Provide a clear system instruction and parse the model output into a clean list.

```python theme={null}
@function_tool(name_override="extract_keywords_from_job_description")
def extract_keywords_from_job_description(job_text: str) -> list[str]:
    """
    Use the LLM to extract 10-15 key skills/tools/responsibilities from the job_text.
    Returns a list of keywords.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Extract 10–15 key skills, tools, and responsibilities from this job description."
            },
            {"role": "user", "content": job_text},
        ],
        temperature=0.3
    )

    response_text = response["choices"][0]["message"]["content"]
    lines = response_text.splitlines()
    # Strip bullets, numbering, and any leading/trailing whitespace
    keywords = [line.strip(" -•*0123456789.").strip() for line in lines if line.strip()]
    return keywords
```

Tip: If the LLM returns multi-word phrases, keep them as-is (e.g., `REST APIs`, `containerization`) to preserve context for resume scanning.

## Tool 3 — Transcribe interview audio

Transcribe interviews using OpenAI’s speech-to-text model. This function returns the transcription text extracted from the audio file.

```python theme={null}
@function_tool(name_override="transcribe_interview")
def transcribe_interview(file_path: str) -> str:
    """
    Transcribe an audio file (wav, mp3, etc.) using OpenAI's Whisper model.
    Returns the transcript text.
    """
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe(model="whisper-1", file=audio_file)
    # The response includes a 'text' field
    return transcript.get("text", "").strip()
```

Note: Transcription quality depends on audio clarity, sampling rate, and accents. Preprocessing (noise reduction, splitting long files) can improve results.

## Tool 4 — Analyze interview relevance

Compare the transcript against the job description and return a human-readable assessment that highlights areas that were strong, missing, or overemphasized, plus actionable suggestions.

```python theme={null}
@function_tool(name_override="analyze_interview_relevance")
def analyze_interview_relevance(interview_text: str, job_description: str) -> str:
    """
    Using the LLM, evaluate how well the interview questions align with the job description.
    Return a detailed, human-readable assessment.
    """
    system_msg = (
        "You are an HR assistant. Evaluate how well the interview questions align with the job description. "
        "Be specific and helpful. Mention which areas were strong, which were missing, and provide actionable suggestions."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {
                "role": "user",
                "content": f"Interview:\n\n{interview_text}\n\nJob Description:\n\n{job_description}"
            }
        ],
        temperature=0.4
    )

    return response["choices"][0]["message"]["content"].strip()
```

Suggestion: For more structured outputs, ask the LLM to return a JSON object with keys like `strengths`, `gaps`, and `recommendations`, then parse it programmatically.

## Coordinator agent — The AI Recruiter Assistant

Now compose the tools into a coordinator Agent that orchestrates the full workflow. The agent pulls together keyword extraction, resume scanning, transcription, and interview analysis, and returns a consolidated report.

```python theme={null}
recruiter_agent = Agent(
    name="Ai Recruiter Assistant",
    instructions="""
You are helping a recruiter. Workflow:
1) Extract keywords from the job description.
2) Scan local resumes for keyword matches.
3) Transcribe the interview audio file.
4) Analyze how well the interview questions align with the job description.
Return a single consolidated report containing:
- Extracted keywords
- Resume keyword matches (filename, keyword, snippet, page)
- Interview transcript summary and alignment feedback
Be concise but thorough; include actionable suggestions where appropriate.
""",
    tools=[
        extract_keywords_from_job_description,
        scan_resumes_for_keywords,
        transcribe_interview,
        analyze_interview_relevance
    ],
    model="gpt-4",
    model_settings=ModelSettings(truncation="auto")
)
```

Design note: Keeping each `@function_tool` narrow and focused makes it easy to test, reuse, and replace components (for example, swapping Whisper for another transcription service).

## Running the system

Create the job description and set the interview audio path. Update paths and job text to match your use case.

```python theme={null}
JOB_DESCRIPTION = """
We're hiring a full-stack engineer with experience in React, Python, REST APIs, and deployment on cloud platforms like AWS or GCP.
The role involves building scalable services, collaborating with product and design, and occasionally supporting data engineering tasks.
Experience with containerization, CI/CD, and monitoring is a plus.
"""

INTERVIEW_AUDIO_PATH = "/Users/gavinridgeway/Documents/Anaconda/AiAgent/Resume/audio_interview.MP3"

prompt = f"""
Please process this job description:
{JOB_DESCRIPTION}

Then scan local resumes for matches using scan_resumes_for_keywords. Finally, transcribe the audio file at:
{INTERVIEW_AUDIO_PATH}
and analyze whether the interview questions align with the job description.
"""
```

The Runner interface is asynchronous. Use an async entrypoint to execute the agent and print the final report. Modify this to fit your runtime or Runner API if necessary.

```python theme={null}
async def main():
    result = await Runner.run(recruiter_agent, input=prompt)
    # The Runner returns a structured result — print the final output from the agent.
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## Example output (what to expect)

When executed, the agent should produce:

* A list of extracted keywords from the job description (10–15 items).
* Resume matches found in your PDF files, each with filename, keyword, snippet, and page number.
* A transcript of the interview audio.
* A detailed analysis explaining which interview questions aligned with the job description and which areas were under- or over-emphasized, including actionable suggestions.

Example scenario: The system might identify candidates matching “React” and “REST APIs” while noting the interview focused heavily on data-analysis topics (SQL, Excel), indicating a misalignment with the software engineering role.

## Recap & next steps

* Each `@function_tool` acts as a specialized sub-agent (resume scanning, keyword extraction, transcription, interview analysis).
* The `Agent` object composes these tools and orchestrates the full pipeline.
* Tools are modular and reusable—swap or extend them as needed.

Possible enhancements:

* Improve keyword extraction (synonyms, fuzzy matching, weighted scoring).
* Parse resumes into structured fields (name, email, experience years) for richer filtering.
* Add automated candidate ranking and prioritization.
* Request structured analysis output (JSON) from the LLM for programmatic post-processing.

## Links and references

* [OpenAI API keys](https://platform.openai.com/account/api-keys)
* [OpenAI Speech-to-Text guide](https://platform.openai.com/docs/guides/speech-to-text)
* [OpenAI Chat guide](https://platform.openai.com/docs/guides/chat)
* [PyMuPDF (fitz) documentation](https://pymupdf.readthedocs.io/)
* [dotenv (python-dotenv)](https://pypi.org/project/python-dotenv/)

<Callout icon="warning">
  Be mindful of API usage and costs. Transcribing long audio files and multiple LLM calls can incur charges—batch and rate-limit requests where possible. Also ensure you have consent and comply with relevant privacy requirements when processing candidate data.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents/module/05e40a2e-53c7-4eff-8df8-6aee856da058/lesson/aca371c3-b1a0-44dd-bcf3-4f5c3b47758f" />
</CardGroup>
