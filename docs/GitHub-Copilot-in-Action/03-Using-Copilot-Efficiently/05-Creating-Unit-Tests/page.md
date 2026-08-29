# Initialize FastAPI router instance
router = APIRouter()

@router.post("/getfakedata")
async def generate_fake_data(request: FakeDataRequest) -> dict:
    """
    Generate fake data based on the provided request parameters.

    Args:
        request (FakeDataRequest): Request model containing the `count`
            parameter specifying the number of fake data items to generate.

    Returns:
        dict: JSON response containing:
            - data: list of generated fake data items

    Example:
        Request: POST /getfakedata
        {
            "count": 5
        }
        Response:
        {
            "data": [...generated items...]
        }
    """
    # Retrieve fake data using repository function
    data = get_fake_data(request.count)

    # Return data wrapped in response dictionary
    return {"data": data}
```

This before/after demonstrates how small docstrings and targeted comments improve clarity for maintainers and API consumers.

## 4. Generate or improve README.md with GitHub Copilot

Copilot and similar assistants can quickly scaffold a README. Use a clear prompt and then verify every section (dependencies, setup steps, env vars, example calls).

Typical steps:

1. Create `README.md`.
2. Prompt: "Generate a README for a FastAPI-based fake data generator repository."
3. Edit the generated content to match your repo (e.g., exact dependencies, environment variables, and example commands).

Example README snippet (cleaned and reviewed):

````markdown theme={null}
A FastAPI-based service that generates and serves realistic fake data for development and testing purposes.

## Features

- Generate fake personal data (names, emails, ages, cities, occupations)
- REST API endpoints for programmatic access
- SQLite database storage (optional)
- Customizable data generation parameters

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```sh
git clone https://github.com/yourusername/fake-data-generator.git
cd fake-data-generator
```text

2. Create and activate a virtual environment:
```sh
python3 -m venv venv
source venv/bin/activate
```text

3. Install dependencies:
```sh
pip install -r requirements.txt
```text

## Usage

1. Start the FastAPI server:
```sh
uvicorn main:app --reload
```text

2. Call the endpoint:
```sh
curl -X POST "http://0.0.0.0:8000/getfakedata" \
  -H "Content-Type: application/json" \
  -d '{"count": 5}'
```text
````

Always verify and adapt the generated README content — don’t publish without confirming accuracy.

## 5. Console and runtime notes

When running a FastAPI app with uvicorn you typically see logs like:

```Python theme={null}
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:56608 - "POST /getfakedata HTTP/1.1" 200 OK
```

Common runtime issues:

* 422 Unprocessable Entity: request JSON does not match the expected Pydantic model.
  * Inspect the Pydantic model (e.g., `FakeDataRequest`) for required fields.
  * Confirm request keys and types match the model.
  * Update docstrings and README examples to reflect the actual schema.

## 6. Practical tips

* Use consistent import styles (absolute or relative) across the codebase to avoid confusion in docs and examples.
* Document public modules, exported functions, and class methods — not just endpoints.
* Prefer short, testable docstrings that are easy to keep up-to-date.
* When using AI to generate docs or READMEs:
  * Provide a precise prompt and example inputs/outputs.
  * Review outputs for factual accuracy and completeness.
* Include exact setup steps, environment variables, and curl/postman examples in README for better onboarding.

Table — Common docstring styles at-a-glance:

| Style                      | Typical Use                             | Example notes                                   |
| -------------------------- | --------------------------------------- | ----------------------------------------------- |
| PEP 257 (reStructuredText) | Python stdlib, formal docs              | Emphasizes short summary + extended description |
| Google                     | Readable, widely used in many teams     | Clear Args/Returns/Examples sections            |
| NumPy                      | Scientific code, arrays & return shapes | Includes Parameters/Returns/Examples with types |

## Links and References

* [FastAPI documentation](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi)
* [GitHub Copilot guide](https://learn.kodekloud.com/user/courses/github-copilot-in-action)
* [Uvicorn — ASGI server](https://www.uvicorn.org/)
* [Pydantic documentation](https://docs.pydantic.dev/)

## Conclusion

Automated tools like GitHub Copilot can speed up writing in-code documentation and README scaffolding. They provide useful stubs and suggestions, but the final verification and refinement step is essential to ensure accuracy. With short, consistent docstrings, selective inline comments, and validated AI outputs, you can maintain a codebase that’s easier for current and future maintainers to understand.

Thank you for reading this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-copilot-in-action/module/5c3827f4-b200-4c22-90bb-e7c6540d96d8/lesson/c0d28a3e-a97f-4387-b3cd-6e237ca6e097" />
</CardGroup>


# Creating Unit Tests

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-in-Action/Using-Copilot-Efficiently/Creating-Unit-Tests/page

Guide on refactoring a FastAPI app for testability and writing pytest unit tests that mock the SQLite database to produce fast deterministic endpoint tests

In this lesson you'll learn how to build reliable unit tests for a FastAPI service using pytest and how to structure your code so tests run deterministically. We demonstrate a refactor from a scattered multi-file layout into a single, testable `main.py` and then add unit tests that mock the database layer. You can accelerate test scaffolding with GitHub Copilot; always review any generated tests.

<Frame>
  <img alt="A presentation slide titled &#x22;Creating Unit Tests&#x22; with a dark curved shape on the right containing the word &#x22;Demo&#x22; in bright blue. A small copyright notice (&#x22;© Copyright KodeKloud&#x22;) appears in the bottom left." />
</Frame>

## Overview

* Goal: Make endpoints and DB access easy to test by isolating business logic.
* Approach: Refactor into a single `app/main.py` that contains:
  * A Pydantic request model
  * A context manager for SQLite connections
  * A `fetch_fake_data` helper returning rows as dictionaries
  * A POST endpoint `/api/v1/getfakedata` with input validation and error handling
* Test strategy: Use `pytest` + `fastapi.testclient.TestClient` and patch DB calls to keep tests fast and deterministic.

Related resources:

* FastAPI docs: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
* pytest docs: [https://docs.pytest.org/](https://docs.pytest.org/)
* SQLite docs: [https://www.sqlite.org/docs.html](https://www.sqlite.org/docs.html)
* GitHub Copilot in Action course: [https://learn.kodekloud.com/user/courses/github-copilot-in-action](https://learn.kodekloud.com/user/courses/github-copilot-in-action)

## Original (messy) example

This example illustrates the problem of splitting routing and logic across nested modules — making tests harder to write and maintain.

```python theme={null}
from fastapi import APIRouter, HTTPException
from ..models.fake_data_request import FakeDataRequest
from ...data.fake_data_repository import get_fake_data
