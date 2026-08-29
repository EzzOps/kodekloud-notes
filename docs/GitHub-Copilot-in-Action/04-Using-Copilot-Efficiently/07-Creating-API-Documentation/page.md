# data/fake_data_repository.py
"""Database operations for fake data."""
import sqlite3
from typing import List, Dict, Any
from fastapi import HTTPException

def get_db_connection() -> sqlite3.Connection:
    """
    Create a connection to the SQLite database.

    Returns:
        sqlite3.Connection: Database connection object

    Raises:
        HTTPException: If database connection fails
    """
    try:
        # Use the relative path to the DB from where your app runs
        conn = sqlite3.connect('./fakedata.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
```

Important: adjust `'./fakedata.db'` to the correct path relative to your application process. Common mistakes are running the server from a different working directory or deploying with a different file layout.

***

## 4) Implement repository function to fetch rows

Add a repository function that executes a parameterized query and returns a list of dictionaries. Use `LIMIT ?` with parameters passed as a tuple (e.g., `(count,)`) to avoid binding errors and SQL injection risks:

```python theme={null}
# data/fake_data_repository.py (continued)
def get_fake_data(count: int) -> List[Dict[str, Any]]:
    """
    Retrieve fake data records from database.

    Args:
        count (int): Number of records to return

    Returns:
        List[Dict[str, Any]]: List of complete fake data records
    """
    query = """
    SELECT first_name, last_name, email_address, age, city, occupation
    FROM fake_data
    ORDER BY RANDOM()
    LIMIT ?
    """

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (count,))
        results = cursor.fetchall()
        return [dict(row) for row in results]
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()
```

Key points:

* Use `LIMIT ?` and pass parameters as a tuple: `(count,)`.
* Convert `sqlite3.Row` to a `dict` before returning so FastAPI can JSON-serialize the response cleanly.

***

## 5) Update the router to call the repository

Replace the Faker-based business logic with a simple repository call. The router should be a thin adapter that validates the request, calls the repository, and returns the rows in a JSON response:

```python theme={null}
# api/endpoints/router.py
from fastapi import APIRouter
from api.models.fake_data_request import FakeDataRequest
from data.fake_data_repository import get_fake_data

router = APIRouter()

@router.post("/getfakedata")
async def generate_fake_data(request: FakeDataRequest) -> dict:
    """
    Endpoint to retrieve fake data.

    Args:
        request (FakeDataRequest): Request parameters

    Returns:
        dict: Object containing retrieved fake data
    """
    data = get_fake_data(request.count)
    return {"data": data}
```

Note: ensure your import paths match the actual package layout. In this project the working solution used `api.models.fake_data_request` and `data.fake_data_repository`.

***

## 6) Request model (Pydantic)

Keep the Pydantic model small and focused. For the repository-driven endpoint you primarily need `count`. Optionally include `locale` if you plan to keep locale-aware behavior later:

```python theme={null}
# api/models/fake_data_request.py
from pydantic import BaseModel
from typing import Optional

class FakeDataRequest(BaseModel):
    """
    Request model for fake data generation.

    Attributes:
        count (int): Number of records to generate
        locale (str, optional): Locale for data generation (default: 'en_US')
    """
    count: int
    locale: Optional[str] = "en_US"
```

If you later reintroduce per-field selection (e.g., `data_type`), extend this model and update repository logic accordingly.

***

## 7) Common errors encountered (and how to fix them)

When wiring DB-backed repositories into existing projects, these issues are common. The table below summarizes errors and remedies.

| Symptom / Error message                                           | Likely cause                                                        | Fix / diagnostic steps                                                                                                                      |
| ----------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'src'`                      | Incorrect imports or running from wrong working directory           | Run the app from the project root and use package imports (e.g., `api.models...`, `data...`). Verify `PYTHONPATH` if needed.                |
| `ImportError: attempted relative import beyond top-level package` | Relative imports exceeding package boundaries                       | Use absolute package imports or correct the package structure so relative imports stay within the package.                                  |
| `Database error: no such table: fake_data`                        | DB file missing or wrong file path, or table not created in that DB | Confirm DB path (`./fakedata.db`) from the running process. Inspect file with DB Browser for SQLite or run `PRAGMA table_info(fake_data);`. |
| `sqlite3.ProgrammingError: Incorrect number of bindings supplied` | Parameterized query placeholders mismatch                           | When using `?` placeholders, pass parameters as a tuple, e.g., `(count,)`.                                                                  |
| Unexpected empty result set                                       | Table exists but has no rows or random ordering excluded rows       | Verify table contents and adjust query (remove `ORDER BY RANDOM()` for deterministic results while testing).                                |

Debugging tips:

* Temporarily log the query and params to the application logs while debugging (remove or lower log level in production):

```python theme={null}
print("Query:", query)
print("Params:", (count,))
```

* Confirm the Python process' current working directory and the absolute path of the DB file:

```python theme={null}
import os
print("CWD:", os.getcwd())
print("DB exists:", os.path.exists('./fakedata.db'))
```

***

## 8) Example client requests & responses

Request to retrieve 3 records:

```json theme={null}
POST /getfakedata
Content-Type: application/json

{
  "count": 3
}
```

Example successful response:

```json theme={null}
{
  "data": [
    {
      "first_name": "Carol",
      "last_name": "Smith",
      "email_address": "carol.smith@example.com",
      "age": 45,
      "city": "Austin",
      "occupation": "Teacher"
    },
    {
      "first_name": "Tina",
      "last_name": "Lee",
      "email_address": "tina.lee@example.com",
      "age": 45,
      "city": "New York",
      "occupation": "Professor"
    },
    {
      "first_name": "Quinn",
      "last_name": "Gilbert",
      "email_address": "quinn.gilbert@example.com",
      "age": 33,
      "city": "Oklahoma City",
      "occupation": "Hairdresser"
    }
  ]
}
```

If the DB file is missing or the table doesn't exist you will get a 500 with a detail message like:

```json theme={null}
{
  "detail": "Database error: no such table: fake_data"
}
```

This error is useful during development because it proves the endpoint is hitting the DB path instead of returning stubbed results.

> **lightbulb** Use tools like [GitHub Copilot](https://github.com/features/copilot) to accelerate repetitive tasks, but keep full control of architecture and imports. The LLM can suggest code and new files, but you must verify project structure, package imports, and the database path/permissions.

***

## 9) Summary / next steps

What we changed and next improvements:

* Replaced Faker-based generation with a repository that reads rows from an SQLite `fake_data` table.
* Added a DB connection helper that sets `row_factory` for easy dict conversion.
* Implemented a repository function using parameterized queries and safe bindings.
* Simplified the router to be a lightweight adapter that returns JSON-ready dicts.
* Covered common integration errors: import paths, DB location, missing tables, and incorrect parameter bindings.

Next steps:

* Add robust validation and error messages on the Pydantic model (e.g., ensure `count` is positive).
* Add optional query filters and field selectors to the repository/API for more flexible responses.
* Add unit and integration tests that exercise the database layer using a temporary test DB file or an in-memory SQLite DB.
* Consider migrating to a connection pool (e.g., `aiosqlite` or a higher-level ORM) for production workloads that need concurrency.

***

## Links and references

* [FastAPI documentation](https://fastapi.tiangolo.com/)
* [SQLite documentation](https://www.sqlite.org/)
* [DB Browser for SQLite](https://sqlitebrowser.org/)
* [Faker (original approach)](https://faker.readthedocs.io/en/latest/)
* [GitHub Copilot](https://github.com/features/copilot)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-copilot-in-action/module/5c3827f4-b200-4c22-90bb-e7c6540d96d8/lesson/fdcc8eb1-4bef-4530-b07d-b846b76235f8)


# Creating API Documentation

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-in-Action/Using-Copilot-Efficiently/Creating-API-Documentation/page

How to create clear OpenAPI and interactive Swagger documentation with FastAPI using Pydantic models, docstrings, endpoints, validation, and example responses.

In this lesson we'll walk through creating clear, usable API documentation using FastAPI. FastAPI automatically generates OpenAPI/Swagger documentation (Swagger UI at `/docs`, ReDoc at `/redoc`) from your function signatures, Pydantic models, and docstrings — making it an excellent choice for building well-documented APIs quickly.

<Frame>
  <img alt="A presentation slide titled &#x22;Creating API Documentation&#x22; with a large dark curved shape on the right containing the word &#x22;Demo&#x22; in blue. The bottom-left corner shows a small &#x22;© Copyright KodeKloud&#x22; notice." />
</Frame>

> **lightbulb** FastAPI auto-generates OpenAPI/Swagger documentation from path operation signatures, Pydantic models, and docstrings. Well-structured docstrings and typed models greatly improve the generated docs and the developer experience.

Overview

* Why FastAPI: automatic OpenAPI generation, interactive docs, type-driven validation.
* What this example shows: Pydantic request model, SQLite path setup, a context manager for DB connections, a helper to fetch randomized fake data, and a POST endpoint that returns that data.
* Result: interactive docs available at `/docs` (Swagger UI) and `/redoc` (ReDoc) after running the app.

Code example (concise, cleaned-up)
The following blocks show the full example used in the lesson. Each block is explained briefly before the code so the flow and purpose are clear.

```python theme={null}
