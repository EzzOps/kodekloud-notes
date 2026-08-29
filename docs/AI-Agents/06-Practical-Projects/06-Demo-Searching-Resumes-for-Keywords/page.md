# Example iPhone-style user agent string and viewport
iphone_user_agent = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/15.0 Mobile/15E148 Safari/604.1"
)

viewport = {"width": 375, "height": 812}

# Example URL: OpenAI Wikipedia page
url = "https://en.wikipedia.org/wiki/OpenAI"

# Run the async agent
asyncio.run(browse_and_display_then_summarize(iphone_user_agent, url, viewport))
```

When executed, the notebook will show the rendered page screenshot (using the supplied user agent and viewport), print the first portion of the scraped Wikipedia text, and print the GPT-4–generated summary.

From this base you can extend the agent to:

* scrape and aggregate content from multiple pages,
* index or store extracted highlights,
* generate study aids, flashcards, or quizzes automatically,
* add navigation logic to follow links, handle pagination, or respect robots.txt.

<Frame>
  <img alt="The image shows a Jupyter Notebook interface displaying some text about OpenAI, its AI models, and corporate structure. The content includes an extracted Wikipedia entry and a GPT-generated summary." />
</Frame>

## Links and references

* Playwright Documentation: [https://playwright.dev/](https://playwright.dev/)
* OpenAI API Keys guide: [https://platform.openai.com/docs/guides/api-keys](https://platform.openai.com/docs/guides/api-keys)
* Python dotenv: [https://pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/)

Thank you for reading.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents/module/a433ab93-c13a-4a03-adf7-f89a6f61ced3/lesson/f84c4ced-5cb6-435a-8346-1e01ffaad9aa)


# Demo Searching Resumes for Keywords

Source: https://notes.kodekloud.com/docs/AI-Agents/Practical-Projects/Demo-Searching-Resumes-for-Keywords/page

Guide to building a Python agent that extracts keywords from job descriptions using OpenAI and scans PDF resumes for matches, reporting filenames, lines, keywords, and pages.

Welcome back.

In this guide we'll build a smart resume-screener agent in Python that:

* Extracts the most relevant keywords from a job description using an OpenAI GPT model,
* Scans all PDF resumes in a folder for those keywords, and
* Reports which resumes mention those keywords (including file name, matched keyword, matching line, and page number).

This workflow is useful for recruiters, hiring managers, and automated HR screening pipelines. Below is a cleaned, consolidated, and better-organized version of the code with step-by-step explanation.

> **lightbulb** Before running the code, install PyMuPDF (fitz) and any other dependencies you need. For example:

  ```bash theme={null}
  pip install pymupdf python-dotenv openai
  ```

  See the packages: [PyMuPDF](https://pypi.org/project/PyMuPDF/), [python-dotenv](https://pypi.org/project/python-dotenv/), and the [OpenAI Python client](https://github.com/openai/openai-python). Also set your OpenAI API key in an environment variable (for example, in a `.env` file): `OPENAI_API_KEY=your_key_here`. See OpenAI's API key docs: [https://platform.openai.com/docs/api-keys](https://platform.openai.com/docs/api-keys).

Dependencies at a glance:

| Package              | Purpose                                       | Install                     |
| -------------------- | --------------------------------------------- | --------------------------- |
| PyMuPDF (`fitz`)     | Read and extract text from PDF files          | `pip install pymupdf`       |
| python-dotenv        | Load environment variables from a `.env` file | `pip install python-dotenv` |
| OpenAI Python client | Call OpenAI APIs for keyword extraction       | `pip install openai`        |

## 1) Load environment variables and imports

Start by loading environment variables and importing required modules. This section sets up dotenv and common utilities.

```python theme={null}
from dotenv import load_dotenv
import os
import re
import asyncio
from pathlib import Path

load_dotenv()  # Loads environment variables from .env into os.environ
```

Then import the agent and OpenAI client libraries and PyMuPDF. These imports provide the agent runtime, the OpenAI client, and PDF parsing.

```python theme={null}
from agents import Agent, Runner, ModelSettings
from agents.tool import function_tool
from openai import OpenAI
import fitz  # PyMuPDF
```

Create the OpenAI client and set the directory that contains your resumes. Replace the path with your local folder of PDFs:

```python theme={null}
client = OpenAI()
RESUME_DIR = Path("/Users/your_user/Path/To/Resumes")  # <-- change this to your folder
```

Security tip: Keep your `OPENAI_API_KEY` and any other secrets out of your repository (use `.env` or your platform's secret manager).

## 2) Define the PDF resume scanning tool

We expose a tool the agent can call: it opens each PDF in the folder, iterates pages and lines, and records matches for any of the provided keywords.

```python theme={null}
@function_tool(name_override="scan_resumes_for_keywords")
def scan_resumes_for_keywords(keywords: list[str]) -> list[dict]:
    """
    Scans all PDF files in RESUME_DIR for occurrences of any keyword in `keywords`.
    Returns a list of dicts with keys: filename, keyword, line, page.
    """
    results: list[dict] = []

    # Lower-case keywords for case-insensitive matching
    lowered_keywords = [kw.lower() for kw in keywords]

    for file in RESUME_DIR.glob("*.pdf"):
        try:
            doc = fitz.open(file)
        except Exception as e:
            # If a PDF cannot be opened, skip it (could log the error)
            continue

        for page in doc:
            text = page.get_text() or ""
            lines = text.splitlines()
            for line in lines:
                line_lower = line.lower()
                for kw in lowered_keywords:
                    if kw and kw in line_lower:
                        results.append({
                            "filename": file.name,
                            "keyword": kw,
                            "line": line.strip(),
                            "page": page.number + 1
                        })

        doc.close()
    return results
```

Notes:

* Only `*.pdf` files are scanned.
* Matching is case-insensitive and performed per line. This keeps context (the line and page) for every hit.
* Each result contains `filename`, `keyword`, `line`, and a 1-based `page` number.

## 3) Extract keywords from a job description using OpenAI

Define a function that calls the OpenAI chat completion endpoint to extract a list of the most important skills/technologies from the job description. The function normalizes and cleans numbered or bulleted lists returned by the model.

```python theme={null}
def extract_keywords_from_job_description(job_text: str, n_keywords: int = 15) -> list[str]:
    """
    Uses the OpenAI chat completions API (https://platform.openai.com/docs/guides/chat) to extract important skills/keywords
    from the provided job_text. Returns up to n_keywords items.
    """
    system_msg = (
        "You are a job recruiter. Extract the 10–15 most important skills, "
        "technologies, and keywords from the job description. Output them as a "
        "simple list (one per line or comma-separated)."
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": job_text}
        ],
        temperature=0.3
    )

    # Parse raw content and clean list items
    raw_output = response.choices[0].message.content or ""
    keywords: list[str] = []
    for line in raw_output.splitlines():
        # remove bullet/number prefixes like "1.", "-", "*", "•", "2)"
        cleaned = re.sub(r'^[\s\-\*\.\d\)\•]+', '', line).strip()
        if cleaned:
            # If the line contains multiple comma-separated items, split them too
            if "," in cleaned and len(cleaned.split(",")) > 1:
                for part in cleaned.split(","):
                    part_clean = part.strip()
                    if part_clean:
                        keywords.append(part_clean)
            else:
                keywords.append(cleaned)

    # Fallback: if the model returned a single-line comma-separated output
    if not keywords:
        for part in raw_output.split(","):
            part_clean = part.strip()
            if part_clean:
                keywords.append(part_clean)

    return keywords[:n_keywords]
```

Tips:

* Keep `temperature` low (e.g., 0.2–0.4) to improve determinism for extraction tasks.
* Consider adjusting the system prompt to include domain-specific terms or required exclusions.

## 4) Job description and running the agent

Use a job description (replace with one from your interface or user input), extract keywords, then create the agent and run the scan.

```python theme={null}
JOB_DESCRIPTION = """We're looking for a data scientist with experience in Python, machine learning,
data visualization, working with large datasets, SQL, version control (Git), and production deployment.
Experience with NumPy, pandas, and deploying models to cloud platforms is a plus."""
