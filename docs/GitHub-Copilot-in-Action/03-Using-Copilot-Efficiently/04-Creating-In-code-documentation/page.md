# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Dict
from contextlib import contextmanager
from pathlib import Path

app = FastAPI(title="Fake Data API")

class DataRequest(BaseModel):
    count: int

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "db"
DB_PATH = DATA_DIR / "fakedata.db"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
```

Context manager for database connections
Use a context manager to ensure SQLite connections are opened and closed reliably. The docstring includes usage notes and exceptions to help maintainers and automated docs.

```python theme={null}
@contextmanager
def get_db_connection():
    """
    Create and manage a database connection as a context manager.

    This function establishes a connection to the SQLite database
    specified by DB_PATH, sets the row factory to sqlite3.Row for
    dictionary-like access to rows, and ensures the connection is
    properly closed after use.

    Usage:
        >>> with get_db_connection() as conn:
        ...     cursor = conn.cursor()
        ...     cursor.execute("SELECT 1")
        ...     rows = cursor.fetchall()

    Yields:
        sqlite3.Connection: An active connection to the SQLite database.

    Raises:
        sqlite3.Error: If there's an error connecting to or interacting
                       with the database.
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
```

Helper function to fetch random fake data
The helper includes a precise docstring describing parameters, return type, and possible database errors. This helps both readers and generated documentation.

```python theme={null}
def fetch_fake_data(count: int) -> List[Dict]:
    """
    Retrieve a number of randomly selected fake data entries from the DB.

    Parameters:
        count (int): The number of fake data entries to retrieve.

    Returns:
        List[Dict]: A list of dictionaries, each representing a single fake
                    data entry with keys: first_name, last_name,
                    email_address, age, city, occupation.

    Raises:
        sqlite3.Error: If there's an error executing the SQL query or
                       fetching the results from the database.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT first_name, last_name, email_address, age, city,
                   occupation
            FROM fake_data
            ORDER BY RANDOM()
            LIMIT ?
            """,
            (count,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
```

POST endpoint: docstrings, validation, and error handling
This POST endpoint demonstrates how to document an operation with a descriptive docstring and how to perform input validation and error handling. Note: FastAPI will use the function signature and Pydantic models for the OpenAPI schema; the extended YAML-style docstring below can be consumed by external tooling or for human readers, though FastAPI does not parse YAML blocks in docstrings into OpenAPI automatically.

```python theme={null}
@app.post("/api/v1/getfakedata")
async def get_fake_data(request: DataRequest):
    """
    Generate fake personal data entries from the database.

    ---
    tags:
      - Fake Data API
      - Data Generation

    summary: Retrieve randomly generated personal data entries

    description: |
      Endpoint generates and returns randomly selected fake personal
      data entries from a pre-populated database. Each entry contains
      personal information including name, email, age, location, and
      occupation. Rate limited to 1000 records per request.

    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              count:
                type: integer
                minimum: 1
                maximum: 1000
                description: Number of data entries to retrieve
          example:
            count: 2

    responses:
      '200':
        description: Successfully retrieved fake data entries
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  first_name:
                    type: string
                    example: "John"
                  last_name:
                    type: string
                    example: "Doe"
                  email_address:
                    type: string
                    format: email
                    example: "john.doe@example.com"
                  age:
                    type: integer
                    example: 30
                  city:
                    type: string
                    example: "New York"
                  occupation:
                    type: string
                    example: "Software Engineer"
      '400':
        description: Invalid request parameters
        content:
          application/json:
            example:
              detail: "Count must be between 1 and 1000"
      '404':
        description: No data found in database
        content:
          application/json:
            example:
              detail: "No data entries found in database"
      '500':
        description: Internal server error
        content:
          application/json:
            example:
              detail: "Internal server error occurred"
    """
    count = request.count

    # Input validation
    if count <= 0:
        raise HTTPException(status_code=400, detail="Count must be greater than 0")
    if count > 1000:
        raise HTTPException(status_code=400, detail="Count must be 1000 or fewer")

    # Fetch and return results with error handling
    try:
        results = fetch_fake_data(count)
        if not results:
            raise HTTPException(status_code=404, detail="No data entries found in database")
        return results
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Internal server error occurred")
```

Entrypoint to run the app
Start the app with Uvicorn for local testing and to view the generated docs.

```python theme={null}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Request and response examples
These examples help API consumers understand the expected input and output formats.

Request (example)

```json theme={null}
{
  "count": 2
}
```

Response (example)

```json theme={null}
[
  {
    "first_name": "John",
    "last_name": "Doe",
    "email_address": "john.doe@example.com",
    "age": 30,
    "city": "New York",
    "occupation": "Software Engineer"
  },
  {
    "first_name": "Jane",
    "last_name": "Smith",
    "email_address": "jane.smith@example.com",
    "age": 25,
    "city": "San Francisco",
    "occupation": "Data Scientist"
  }
]
```

Typical startup and doc access log
After running the server you should see logs similar to:

```text theme={null}
INFO:     Started server process [14253]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:52513 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:52517 - "GET /redoc HTTP/1.1" 200 OK
INFO:     127.0.0.1:52513 - "GET /openapi.json HTTP/1.1" 200 OK
```

Quick reference: response codes and examples

| HTTP Code | Meaning                            | Example response                                      |
| --------- | ---------------------------------- | ----------------------------------------------------- |
| 200       | Successful retrieval of data       | `[{ "first_name": "John", "last_name": "Doe", ... }]` |
| 400       | Invalid request (validation error) | `{"detail":"Count must be greater than 0"}`           |
| 404       | No data found                      | `{"detail":"No data entries found in database"}`      |
| 500       | Internal server error (DB error)   | `{"detail":"Internal server error occurred"}`         |

<Callout icon="warning">
  When running locally or in production, never expose an open database file directly without proper access controls. Apply rate limiting, input validation, and authentication for public APIs to prevent abuse and protect sensitive data.
</Callout>

Tips and best practices for API documentation (SEO-friendly)

* Use Pydantic models for request and response schemas — FastAPI surfaces these types in generated docs and OpenAPI schemas.
* Write clear docstrings: include a concise summary, a descriptive body, and examples. These show up in Swagger UI and ReDoc and help search engines index descriptive content.
* Document possible responses and error cases (400/404/500) with examples to help API consumers implement robust clients.
* Keep function signatures and type hints accurate — the OpenAPI schema is built from these.
* Consider adding operation-level tags and summaries to group endpoints and improve discoverability in interactive docs.
* Use external YAML snippets or tools if you need to extend the generated OpenAPI beyond what FastAPI infers, but verify how those tools integrate into your pipeline.
* Treat AI assistants (e.g., GitHub Copilot) as collaborators: ask for docstring suggestions, then review and refine to align with your documentation standards.

Links and references

* FastAPI documentation: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
* Pydantic models: [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/)
* SQLite: [https://sqlite.org/index.html](https://sqlite.org/index.html)
* Uvicorn: [https://www.uvicorn.org/](https://www.uvicorn.org/)
* Example course: [GitHub Copilot in Action](https://learn.kodekloud.com/user/courses/github-copilot-in-action)

That concludes this lesson on creating API documentation using FastAPI. Thank you for reading.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-copilot-in-action/module/5c3827f4-b200-4c22-90bb-e7c6540d96d8/lesson/f3b936e1-1a95-4520-9952-01faeaf10e91" />
</CardGroup>


# Creating In code documentation

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-in-Action/Using-Copilot-Efficiently/Creating-In-code-documentation/page

Guide to writing concise in-code documentation, using inline comments, docstrings, examples, and AI assistants like Copilot, plus README generation and practical verification tips.

In this lesson we cover practical, code-first techniques for writing clear in-code documentation. We'll demonstrate inline comments, simple docstrings, common styles (PEP 257, Google, NumPy), and how to accelerate the process with tools like GitHub Copilot. The aim is to help you generate useful, accurate documentation quickly — while emphasizing the essential verification and editing steps.

Key topics:

* Inline comments and compact docstrings for endpoints
* Using AI assistants (e.g., GitHub Copilot) to generate or improve comments
* Before/after examples to illustrate improvements
* Generating README.md skeletons with AI
* Console/runtime troubleshooting and practical tips

## 1. Inline comments and simple docstrings

For small endpoints, a concise docstring plus a couple of inline comments is often sufficient. Keep the docstring focused on purpose, inputs, outputs, and example request/response shapes.

Example (FastAPI):

```python theme={null}
from fastapi import APIRouter
from api.models.fake_data_request import FakeDataRequest
from data.fake_data_repository import get_fake_data

router = APIRouter()

@router.post("/getfakedata")
async def generate_fake_data(request: FakeDataRequest) -> dict:
    """
    Generate fake data based on the incoming request model.

    Args:
        request (FakeDataRequest): Request model that contains a `count`
            parameter indicating how many fake items to generate.

    Returns:
        dict: JSON response containing generated fake data under the
            `data` key.

    Example:
        Request:
        {
            "count": 5
        }

        Response:
        {
            "data": [...generated items...]
        }
    """
    # Fetch fake data using the repository function
    data = get_fake_data(request.count)

    # Return data wrapped in a dictionary for JSON response
    return {"data": data}
```

Best practices:

* Keep the docstring short and focused on the function's role, inputs, and output format.
* Use inline comments sparingly for non-obvious logic, edge cases, or performance implications.
* Use typing annotations to make the signature self-documenting.

<Callout icon="lightbulb">
  AI-generated comments are a great starting point, but always review them for accuracy and to remove stale or incorrect details.
</Callout>

## 2. Asking GitHub Copilot (or other assistants) to comment code

If you prefer automated assistance, you can ask Copilot to annotate code. Typical workflow:

* Open the file you want documented in your editor.
* Prompt the assistant, for example: "Please comment this code to explain it clearly."
* Review the generated docstrings and inline comments; edit them to ensure correctness.

Example prompt:

```text theme={null}
Please comment this code to explain it clearly.
```

Checklist after generation:

* Verify that parameter names match the current model and code (AI may refer to removed fields).
* Confirm examples reflect actual requests/responses.
* Remove any speculative or hallucinated details (e.g., fields that no longer exist).

<Callout icon="warning">
  AI assistants can hallucinate parameters or behavior. Always validate generated comments against the current code and tests before committing.
</Callout>

## 3. Example — before and after

Before (minimal comments):

```python theme={null}
from fastapi import APIRouter
from api.models.fake_data_request import FakeDataRequest
from data.fake_data_repository import get_fake_data

router = APIRouter()

@router.post("/getfakedata")
async def generate_fake_data(request: FakeDataRequest) -> dict:
    data = get_fake_data(request.count)
    return {"data": data}
```

After (annotated and documented):

```python theme={null}
from fastapi import APIRouter
from api.models.fake_data_request import FakeDataRequest
from data.fake_data_repository import get_fake_data
