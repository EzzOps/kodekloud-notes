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

DATA_DIR.mkdir(parents=True, exist_ok=True)

@contextmanager
def get_db_connection():
    """
    Context manager for SQLite connections.
    Yields:
        sqlite3.Connection
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def fetch_fake_data(count: int) -> List[Dict]:
    """
    Retrieve `count` random records from fake_data.
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
            (count,),
        )
        rows = cursor.fetchall()
    return [dict(row) for row in rows]

@app.post("/api/v1/getfakedata", response_model=List[Dict])
async def get_fake_data_endpoint(request: DataRequest) -> List[Dict]:
    """
    Endpoint to fetch fake data.
    Raises HTTPException for invalid counts or database errors.
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
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

<Callout icon="lightbulb">
  Consolidating your endpoints and database logic makes it easier to write targeted unit tests and debug issues.
</Callout>

Test the refactored API manually:

```bash theme={null}
curl -X POST http://0.0.0.0:8000/api/v1/getfakedata \
     -H "Content-Type: application/json" \
     -d '{"count":3}'
```

## Writing Tests with pytest

Follow these steps to create and execute Pytest tests for your FastAPI app:

1. **Setup**\
   Create a `tests/` directory in your project root.

2. **Create Tests**\
   Add `tests/test_main.py` with fixtures and test cases:

```python theme={null}
# tests/test_main.py
import pytest
import sqlite3
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app, get_db_connection, fetch_fake_data, DB_PATH

client = TestClient(app)

@pytest.fixture
def sample_data():
    return [
        {
            "first_name": "John",
            "last_name": "Doe",
            "email_address": "john@example.com",
            "age": 30,
            "city": "New York",
            "occupation": "Engineer",
        }
    ]

@pytest.fixture
def mock_db_cursor(sample_data):
    cursor = MagicMock()
    cursor.fetchall.return_value = [
        (item["first_name"], item["last_name"], item["email_address"],
         item["age"], item["city"], item["occupation"])
        for item in sample_data
    ]
    return cursor

@pytest.fixture
def mock_db_connection(mock_db_cursor):
    conn = MagicMock()
    conn.cursor.return_value = mock_db_cursor
    return conn

def test_get_db_connection_context_manager(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    sqlite3.connect(str(test_db)).close()
    monkeypatch.setattr("app.main.DB_PATH", test_db)
    with get_db_connection() as conn:
        assert hasattr(conn, "cursor")

def test_fetch_fake_data_success(mock_db_connection, monkeypatch, sample_data):
    monkeypatch.setattr("app.main.sqlite3.connect", lambda _: mock_db_connection)
    result = fetch_fake_data(1)
    assert result == sample_data
    mock_db_connection.cursor().execute.assert_called_once()

def test_get_fake_data_endpoint_success(sample_data):
    with patch("app.main.fetch_fake_data", return_value=sample_data):
        response = client.post("/api/v1/getfakedata", json={"count": 1})
    assert response.status_code == 200
    assert response.json() == sample_data

def test_get_fake_data_endpoint_invalid_count():
    response = client.post("/api/v1/getfakedata", json={"count": 0})
    assert response.status_code == 400
    assert "Count must be greater than 0" in response.json()["detail"]

    response = client.post("/api/v1/getfakedata", json={"count": 1001})
    assert response.status_code == 400
    assert "Count must not exceed 1000" in response.json()["detail"]

def test_get_fake_data_endpoint_no_data():
    with patch("app.main.fetch_fake_data", return_value=[]):
        response = client.post("/api/v1/getfakedata", json={"count": 1})
    assert response.status_code == 404
    assert "No data found" in response.json()["detail"]

def test_get_fake_data_endpoint_database_error():
    with patch("app.main.fetch_fake_data", side_effect=sqlite3.Error("Database error")):
        response = client.post("/api/v1/getfakedata", json={"count": 1})
    assert response.status_code == 500
    assert "Database error" in response.json()["detail"]
```

3. **Install Dependencies & Run**
   ```bash theme={null}
   pip install pytest fastapi uvicorn pydantic pytest
   pytest
   ```

You’ll see:

```text theme={null}
============================= test session starts =============================
platform darwin -- Python 3.12.6, pytest-8.3.4
collected 6 items

tests/test_main.py ......                                           [100%]

============================== 6 passed in 0.21s ===============================
```

| Tool     | Purpose                                         | Install Command               |
| -------- | ----------------------------------------------- | ----------------------------- |
| pytest   | Testing framework with fixtures & plugins       | `pip install pytest`          |
| FastAPI  | Web framework for building APIs                 | `pip install fastapi uvicorn` |
| pydantic | Data validation and settings management library | `pip install pydantic`        |

## Adding a Basic `unittest` Example

If you prefer Python’s built-in testing library, create `tests/test_db_connectivity.py`:

```python theme={null}
# tests/test_db_connectivity.py
import unittest
import sqlite3

class TestDatabaseConnectivity(unittest.TestCase):
    def test_db_connection(self):
        conn = sqlite3.connect(":memory:")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            self.assertIsNotNone(result)
        finally:
            conn.close()

if __name__ == "__main__":
    unittest.main()
```

Run all `unittest` cases with:

```bash theme={null}
python -m unittest discover -s tests
```

<Callout icon="triangle-alert">
  In-memory SQLite databases (`":memory:"`) are destroyed when the connection closes. Use file-based DBs for persistence.
</Callout>

## Links and References

* [FastAPI Documentation](https://fastapi.tiangolo.com)
* [Pytest Official Guide](https://docs.pytest.org/en/stable/)
* [Python unittest](https://docs.python.org/3/library/unittest.html)
* [GitHub Copilot](https://github.com/features/copilot)
* [SQLite3 Python Module](https://docs.python.org/3/library/sqlite3.html)
* [Uvicorn ASGI Server](https://www.uvicorn.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-copilot-certification/module/a8b1c2a2-f3f7-4470-9347-0ad31f2ab3cc/lesson/66522e53-7d6b-4933-9af6-e90043729c86" />
</CardGroup>


# Creating a New Project

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-Certification/Using-Copilot-Efficiently/Creating-a-New-Project/page

Learn to create a Python project using GitHub Copilot, virtual environments, and a local LLM for generating fake data.

Kick off your development workflow by leveraging GitHub Copilot, Python virtual environments, and a local Ollama LLM for fake data generation. In this guide, you’ll learn how to:

1. Initialize a Git repository
2. Configure a Python virtual environment
3. Scaffold and modularize code with Copilot
4. Generate CSV data via Ollama (local LLM)
5. Manage dependencies and `.gitignore`

***

## 1. Initialize the Git Repository

First, clone or fork your project on GitHub. Your starter repository includes:

* `LICENSE`
* `.gitignore` (baseline)
* GitHub Copilot instructions
* `main.py` (empty stub)

Open your terminal or [VS Code][VS Code] integrated shell:

```bash theme={null}
mkdir my_project
cd my_project
git init
code .
```

This sets up an empty Git repository and launches VS Code in your project folder.

***

## 2. Configure a Python Virtual Environment

Isolating your dependencies prevents conflicts and keeps your project portable. You can follow Copilot’s suggestions or use these commands:

| Step                           | Command (macOS/Linux)               | Command (Windows PowerShell)      |
| ------------------------------ | ----------------------------------- | --------------------------------- |
| Create project folder & venv   | `mkdir my_project && cd my_project` | `mkdir my_project; cd my_project` |
| Initialize virtual environment | `python3 -m venv .venv`             | `python -m venv .venv`            |
| Activate environment           | `source .venv/bin/activate`         | `.venv\Scripts\Activate.ps1`      |
| Verify activation              | Look for `(.venv)` in your prompt   | Look for `(.venv)` in your prompt |

<Callout icon="lightbulb">
  Virtual environments ensure that `pip install` only affects your project and avoids version clashes globally. See [Python Virtual Environments].
</Callout>

With the environment active, install packages locally:

```bash theme={null}
pip install <package_name>
```

***

## 3. Scaffold `main.py` with GitHub Copilot

Use the [GitHub Copilot][GitHub Copilot Documentation] extension in VS Code. In Copilot Chat, request:

> “Scaffold a `main.py` that defines a `FakeDataGenerator` class and runs it in `main()`.”

Copilot will generate something like this:

```python theme={null}
