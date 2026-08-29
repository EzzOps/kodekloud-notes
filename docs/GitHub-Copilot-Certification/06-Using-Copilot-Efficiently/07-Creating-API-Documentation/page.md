# src/data/fake_data_repository.py
"""Database operations for fake data using SQLite."""
import sqlite3
from typing import List, Dict, Any
from fastapi import HTTPException

def get_db_connection() -> sqlite3.Connection:
    """
    Establish a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object with row factory set.

    Raises:
        HTTPException: If the database connection fails.
    """
    try:
        conn = sqlite3.connect("fakedata.db")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection error: {e}"
        )

def get_fake_data(count: int) -> List[Dict[str, Any]]:
    """
    Retrieve a specified number of random records from the database.

    Args:
        count (int): How many records to retrieve.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing fake data.

    Raises:
        HTTPException: On query execution error.
    """
    query = """
        SELECT first_name,
               last_name,
               email_address,
               age,
               city,
               occupation
        FROM fake_data
        ORDER BY RANDOM()
        LIMIT ?
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, (count,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()
```

***

## 2. Request Model

Define a Pydantic model in `src/api/models/fake_data_request.py` to validate incoming JSON payloads.

```python theme={null}
# src/api/models/fake_data_request.py
from pydantic import BaseModel
from typing import Optional

class FakeDataRequest(BaseModel):
    """
    Model to validate fake data retrieval requests.

    Attributes:
        count (int): Number of records to return.
        locale (Optional[str]): Locale code (unused in SQLite).
    """
    count: int
    locale: Optional[str] = "en_US"
```

***

## 3. API Endpoint Router

Refactor your router in `src/api/endpoints/router.py` to delegate data retrieval to the repository.

```python theme={null}
# src/api/endpoints/router.py
from fastapi import APIRouter
from api.models.fake_data_request import FakeDataRequest
from data.fake_data_repository import get_fake_data

router = APIRouter()

@router.post("/getfakedata", tags=["Fake Data"])
async def generate_fake_data(request: FakeDataRequest) -> dict:
    """
    POST endpoint to fetch fake data from SQLite.

    Args:
        request (FakeDataRequest): Request schema with parameters.

    Returns:
        dict: Contains a list of fake data objects.
    """
    data = get_fake_data(request.count)
    return {"data": data}
```

***

## 4. Main Application Integration

Include the endpoint router in your FastAPI app entry point at `src/main.py`.

```python theme={null}
# src/main.py
from fastapi import FastAPI
from api.endpoints.router import router as fake_data_router

app = FastAPI(
    title="FastAPI Fake Data Generator",
    description="API that serves random fake data from an SQLite database",
    version="1.0.0",
)

app.include_router(fake_data_router, prefix="/api")
```

> **triangle-alert** Always close the database connection in a `finally` block to prevent resource leaks.

***

## 5. Testing & Debugging

1. Start the server with hot reload:

   ```bash theme={null}
   uvicorn src.main:app --reload
   ```

2. Send a POST request to `/api/getfakedata`:

   ```json theme={null}
   {
     "count": 5
   }
   ```

3. Example successful response:

   ```json theme={null}
   {
     "data": [
       {
         "first_name": "Alice",
         "last_name": "Smith",
         "email_address": "alice.smith@example.com",
         "age": 29,
         "city": "Seattle",
         "occupation": "Engineer"
       },
       ...
     ]
   }
   ```

4. If you encounter `no such table: fake_data`, verify your database schema:

   ```sql theme={null}
   -- List existing tables
   SELECT name FROM sqlite_master WHERE type='table';

   -- Inspect table columns
   PRAGMA table_info(fake_data);
   ```

***

## 6. Takeaways

* **Separation of Concerns**: Keep database logic in a repository and routing logic in the API layer.
* **Validation**: Use Pydantic models for input validation and automatic documentation.
* **Clean Architecture**: Slim routers and well-documented modules lead to maintainable code.
* **Automation with Oversight**: Tools like GitHub Copilot can accelerate development but always review generated code.

***

## References

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [SQLite Official Documentation](https://www.sqlite.org/docs.html)
* [Pydantic User Guide](https://pydantic-docs.helpmanual.io/)
* [Uvicorn Server](https://www.uvicorn.org/)
* [Repository Pattern in Python](https://martinfowler.com/eaaCatalog/repository.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-copilot-certification/module/a8b1c2a2-f3f7-4470-9347-0ad31f2ab3cc/lesson/0c92989b-a5cd-4094-893b-e0167f376eda)


# Creating API Documentation

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-Certification/Using-Copilot-Efficiently/Creating-API-Documentation/page

Learn to build interactive API documentation with FastAPI using OpenAPI, including setting up a Fake Data API and customizing Swagger UI and Redoc interfaces.

Learn how to build and refine interactive API docs using FastAPI’s built-in OpenAPI support. You’ll set up a simple “Fake Data API,” write clear docstrings, and customize the generated Swagger UI and Redoc interfaces.

> **lightbulb** * Python 3.7 or higher
  * A virtual environment with `fastapi`, `uvicorn`, and `pydantic` installed
  * SQLite for a local database

## Table of Contents

1. [Project Layout & Dependencies](#1-project-layout--dependencies)
2. [Initializing the FastAPI App](#2-initializing-the-fastapi-app)
3. [Database Context Manager](#3-database-context-manager)
4. [Fetching Fake Data](#4-fetching-fake-data)
5. [Defining the API Endpoint](#5-defining-the-api-endpoint)
6. [Running the Server](#6-running-the-server)
7. [Swagger UI & Redoc Interfaces](#7-swagger-ui--redoc-interfaces)
8. [Fine-Tuning Your OpenAPI Schema](#8-fine-tuning-your-openapi-schema)
9. [Links and References](#9-links-and-references)

***

## 1. Project Layout & Dependencies

Ensure your project uses this structure:

```text theme={null}
.
├── main.py
└── data
    └── db
        └── fakedata.db
```

| Dependency | Purpose                            |
| ---------- | ---------------------------------- |
| fastapi    | Web framework with OpenAPI support |
| uvicorn    | ASGI server                        |
| pydantic   | Data validation and settings       |

## 2. Initializing the FastAPI App

```python theme={null}
