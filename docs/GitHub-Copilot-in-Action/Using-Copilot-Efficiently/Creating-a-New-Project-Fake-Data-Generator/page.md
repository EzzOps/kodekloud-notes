# Initialize FastAPI router instance
router = APIRouter()

@router.post("/getfakedata", response_model=dict)  # Changed from /fake-data to /getfakedata
async def generate_fake_data(request: FakeDataRequest) -> dict:
    """
    Generate fake data based on request parameters.
    """
    try:
        data = await get_fake_data(request.dict())
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

Refactoring into a single module simplifies test setup and makes it clear where to patch for unit tests.

## Refactored, testable implementation (`app/main.py`)

The following is a self-contained FastAPI app that uses SQLite and provides a helper to fetch random rows. It includes validation, explicit errors, and a context manager for DB connections.

```python theme={null}
# app/main.py
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

@contextmanager
def get_db_connection():
    """
    Create and manage a SQLite database connection as a context manager.

    Yields:
        sqlite3.Connection: An active connection to the SQLite database.

    Notes:
        - Sets `row_factory` to `sqlite3.Row` to allow `dict(row)` conversion.
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def fetch_fake_data(count: int) -> List[Dict]:
    """
    Fetch `count` random rows from the `fake_data` table.

    Args:
        count (int): Number of rows to return.

    Returns:
        List[Dict]: List of dictionary rows.

    Raises:
        sqlite3.Error: If there's an error executing the query or fetching results.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT first_name, last_name, email_address, age, city, occupation
            FROM fake_data
            ORDER BY RANDOM()
            LIMIT ?
            """,
            (count,)
        )
        rows = cursor.fetchall()
    return [dict(row) for row in rows]

@app.post("/api/v1/getfakedata")
async def get_fake_data(request: DataRequest):
    """
    Retrieve a specified number of fake data entries.

    Validation and error responses:
    - 400 if `count` <= 0 ("Count must be greater than 0")
    - 400 if `count` > 1000 ("Count must not exceed 1000")
    - 404 if no data is found ("No data found")
    - 500 if a database error occurs ("Database error: ...")
    """
    count = request.count
    if count <= 0:
        raise HTTPException(status_code=400, detail="Count must be greater than 0")
    if count > 1000:
        raise HTTPException(status_code=400, detail="Count must not exceed 1000")

    try:
        data = fetch_fake_data(count)
        if not data:
            raise HTTPException(status_code=404, detail="No data found")
        return data
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Note: The endpoint expects a JSON body like `{"count": 2}` and is available at POST `/api/v1/getfakedata`.

<Callout icon="lightbulb">
  Before running tests, ensure you have the required test packages installed, for example: `pip install pytest pytest-mock fastapi[all]`. The tests below use `pytest`, `unittest.mock.patch`, and FastAPI's `TestClient`.
</Callout>

## Test strategy

* Unit tests should avoid hitting a real database — patch `sqlite3.connect` or `fetch_fake_data` so tests stay fast and deterministic.
* Use `fastapi.testclient.TestClient` to exercise endpoints.
* Keep tests close to the module for small projects (e.g., `app/test_main.py`) or use a top-level `tests/` directory for larger projects.

### Example pytest file (`app/test_main.py`)

Place this file next to `app/main.py`. It demonstrates:

* Mocking the DB connection for `fetch_fake_data`
* Patching `fetch_fake_data` when testing the endpoint behavior
* Verifying validation and error responses

```python theme={null}
# app/test_main.py
import pytest
from unittest.mock import MagicMock, patch
import sqlite3
from fastapi.testclient import TestClient

from app.main import app, fetch_fake_data

client = TestClient(app)

@pytest.fixture
def sample_data():
    """Fixture providing sample fake data for testing."""
    return [
        {
            "first_name": "John",
            "last_name": "Doe",
            "email_address": "john@example.com",
            "age": 30,
            "city": "New York",
            "occupation": "Engineer"
        },
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "email_address": "jane@example.com",
            "age": 25,
            "city": "Boston",
            "occupation": "Designer"
        }
    ]

def test_fetch_fake_data_success(sample_data):
    """Test `fetch_fake_data` works when the DB returns rows."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = sample_data
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.main.sqlite3.connect", return_value=mock_conn):
        result = fetch_fake_data(2)
        assert isinstance(result, list)
        assert len(result) == 2
        assert result == sample_data
        mock_conn.cursor.assert_called_once()

def test_get_fake_data_endpoint_success(sample_data):
    """Test successful API endpoint call (200)."""
    with patch("app.main.fetch_fake_data", return_value=sample_data):
        response = client.post("/api/v1/getfakedata", json={"count": 2})
        assert response.status_code == 200
        assert len(response.json()) == len(sample_data)
        assert response.json() == sample_data

def test_get_fake_data_endpoint_invalid_count():
    """Test API endpoint with invalid count values (<=0 and >1000)."""
    # count <= 0
    response = client.post("/api/v1/getfakedata", json={"count": 0})
    assert response.status_code == 400
    assert "Count must be greater than 0" in response.json()["detail"]

    # count > 1000
    response = client.post("/api/v1/getfakedata", json={"count": 1001})
    assert response.status_code == 400
    assert "Count must not exceed 1000" in response.json()["detail"]

def test_get_fake_data_endpoint_no_data():
    """Test API endpoint when no data is found (404)."""
    with patch("app.main.fetch_fake_data", return_value=[]):
        response = client.post("/api/v1/getfakedata", json={"count": 1})
        assert response.status_code == 404
        assert "No data found" in response.json()["detail"]

def test_get_fake_data_endpoint_database_error():
    """Test API endpoint handling of database errors (500)."""
    with patch("app.main.fetch_fake_data", side_effect=sqlite3.Error("Database error")):
        response = client.post("/api/v1/getfakedata", json={"count": 1})
        assert response.status_code == 500
        assert "Database error" in response.json()["detail"]
```

## Test cases matrix

| Test name                                    | Scenario                                  | Expected response                 |
| -------------------------------------------- | ----------------------------------------- | --------------------------------- |
| `test_fetch_fake_data_success`               | DB returns rows                           | `200` (function returns a `list`) |
| `test_get_fake_data_endpoint_success`        | Patching `fetch_fake_data` to return data | `200` with JSON array             |
| `test_get_fake_data_endpoint_invalid_count`  | `count` \<= 0 and `count` > 1000          | `400` with validation message     |
| `test_get_fake_data_endpoint_no_data`        | `fetch_fake_data` returns `[]`            | `404` with `"No data found"`      |
| `test_get_fake_data_endpoint_database_error` | `fetch_fake_data` raises `sqlite3.Error`  | `500` with `"Database error"`     |

When listing example JSON payloads or code snippets in tables, wrap them in backticks, for example: use `{"count": 2}` as the request body.

## Run tests

From project root run:

* Discover and run tests with pytest:
  * `pytest`

Example successful output:

```bash theme={null}
$ pytest
============================= test session starts =============================
platform darwin -- Python 3.12.x, pytest-8.x.x
rootdir: /path/to/project
collected 6 items

app/test_main.py ......                                                  [100%]

6 passed in 0.21s
```

## Tips and best practices

* Keep business logic (e.g., `fetch_fake_data`) separate from framework glue (FastAPI route handlers) so you can unit test logic without spinning up the full app.
* For unit tests: mock external state (DB, network) to keep tests fast and deterministic.
* For integration tests: use a disposable test database and clean up state using fixtures.
* Use `TestClient` for endpoint-level tests and patch the underlying helpers for unit-style tests.
* When using GitHub Copilot to scaffold tests: treat outputs as a starting point — verify correctness, edge cases, and error handling.

<Callout icon="warning">
  Avoid running unit tests against your production database. Use mocks for unit tests and a separate ephemeral/test DB for integration tests to prevent data corruption or flaky results.
</Callout>

## Wrap up

* Refactoring to a single, well-structured module simplifies testing and reduces coupling between layers.
* Use pytest with FastAPI's TestClient and mock the database layer to write fast, reliable unit tests.
* Leverage tools like GitHub Copilot to generate test scaffolding quickly, but always review generated code to ensure accurate assertions and coverage.

Further reading and references:

* FastAPI testing: [https://fastapi.tiangolo.com/tutorial/testing/](https://fastapi.tiangolo.com/tutorial/testing/)
* pytest: [https://docs.pytest.org/](https://docs.pytest.org/)
* sqlite: [https://www.sqlite.org/docs.html](https://www.sqlite.org/docs.html)
* GitHub Copilot in Action course: [https://learn.kodekloud.com/user/courses/github-copilot-in-action](https://learn.kodekloud.com/user/courses/github-copilot-in-action)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-copilot-in-action/module/5c3827f4-b200-4c22-90bb-e7c6540d96d8/lesson/e0fd6b9d-de96-436a-941e-ada00ffca77d" />
</CardGroup>


# Creating a New Project Fake Data Generator

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-in-Action/Using-Copilot-Efficiently/Creating-a-New-Project-Fake-Data-Generator/page

Guide to building a Python project that generates CSV fake data from a local Ollama model, including venv setup, modular code, API request utility, dependencies, and gitignore

In this guide you'll create a small Python project that generates fake CSV data by querying a local Ollama model. The lesson covers:

* Creating a project folder and a Python virtual environment
* Scaffolding a minimal application and organizing code into modules
* Adding a utility that calls a local Ollama server to produce CSV-formatted fake data
* Capturing dependencies in `requirements.txt`
* Creating a `.gitignore` to keep the repo clean

This walkthrough is optimized for clarity and searchability with actionable commands, code examples, and links to relevant tools and docs.

Overview of steps:

* Create project folder and virtual environment
* Scaffold `main.py` and a `FakeDataGenerator` class
* Move the class to `fake_data_generator.py` and import it from `main.py`
* Add `create_fake_data.py` to call a local Ollama server and save CSV
* Install dependencies and produce `requirements.txt`
* Create a `.gitignore` to exclude the virtual environment and other artifacts

References:

* Python virtual environments: [https://docs.python.org/3/tutorial/venv.html](https://docs.python.org/3/tutorial/venv.html)
* Requests library: [https://docs.python-requests.org/](https://docs.python-requests.org/)
* Ollama docs: [https://docs.ollama.ai](https://docs.ollama.ai)
* GitHub Copilot: [https://github.com/features/copilot](https://github.com/features/copilot)
* VS Code: [https://code.visualstudio.com](https://code.visualstudio.com)

***

## Quick file summary

| File                     | Purpose                                                      |
| ------------------------ | ------------------------------------------------------------ |
| `main.py`                | Minimal entrypoint that runs the generator                   |
| `fake_data_generator.py` | `FakeDataGenerator` class implementation                     |
| `create_fake_data.py`    | Calls a local Ollama model and writes CSV to `fake_data.csv` |
| `requirements.txt`       | Project dependencies captured via `pip freeze`               |
| `.gitignore`             | Exclude virtual env, build artifacts, IDE files              |

***

## 1) Create the project folder and virtual environment

Create the project folder, open it in your editor (e.g., VS Code), and create a Python virtual environment.

Example CLI commands:

```bash theme={null}
mkdir FakeDataGenerator
cd FakeDataGenerator
code .
python3 -m venv .venv
```

Activate the virtual environment:

* macOS / Linux:

```bash theme={null}
source .venv/bin/activate
```

* Windows (PowerShell):

```powershell theme={null}
.venv\Scripts\Activate.ps1
```

When activated your prompt will indicate the venv, for example:

```bash theme={null}
(.venv) jeremy@Jeremys-Mac-Studio FakeDataGenerator %
```

<Callout icon="lightbulb">
  Use `python3 -m venv .venv` to create a portable local environment. Always activate it before installing project dependencies so packages are isolated to this project.
</Callout>

***

## 2) Scaffold a minimal application

Start with a simple `main.py` that defines a `FakeDataGenerator` class and runs when executed. This keeps the initial project minimal and testable.

`main.py`:

```python theme={null}
