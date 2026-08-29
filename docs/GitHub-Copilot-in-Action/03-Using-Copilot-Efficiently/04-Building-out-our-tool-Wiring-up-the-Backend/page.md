# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./fakeData.db"  # update path if needed

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    FastAPI dependency that yields a DB session and closes it afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Use `get_db()` in endpoints that need to query the `fake_data` table (example wiring is listed in "Next steps" below).

## Choosing a Python web framework

FastAPI was selected for this project due to its performance, developer ergonomics, and automatic OpenAPI docs. Flask and Django are valid alternatives depending on project needs:

| Framework | Use case                                                      |
| --------: | ------------------------------------------------------------- |
|   FastAPI | High-performance APIs, automatic documentation, async support |
|     Flask | Lightweight microservices and simple endpoints                |
|    Django | Full-featured applications with built-in ORM and admin UI     |

An annotated comparison screenshot used during exploration:

<Frame>
  <img alt="A dark-themed screenshot showing a comparison list of web frameworks (FastAPI and Flask) with bullet-pointed pros and cons. A white mouse cursor is visible over the text." />
</Frame>

## Project scaffold

A minimal project layout used for this example:

```text theme={null}
fastapi-project
├── src
│   ├── api
│   │   ├── __init__.py
│   │   └── endpoints
│   │       └── router.py
│   ├── core
│   ├── db
│   │   └── database.py
│   ├── models
│   │   └── fake_data_request.py
│   ├── services
│   └── main.py
├── requirements.txt
└── README.md
```

## main.py — start the FastAPI app

A minimal `main.py` that mounts the router and runs via Uvicorn:

```python theme={null}
# main.py
from fastapi import FastAPI
from api.endpoints.router import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

If FastAPI or Uvicorn are not installed, running `python main.py` will raise an import error:

```text theme={null}
(.venv) $ python main.py
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    from fastapi import FastAPI
ModuleNotFoundError: No module named 'fastapi'
```

Install the runtime dependencies:

```bash theme={null}
pip install fastapi uvicorn
```

When the app starts successfully you'll see logs like:

```text theme={null}
INFO:     Started server process [83597]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:61992 - "GET / HTTP/1.1" 200 OK
```

## Request model (Pydantic)

Use a Pydantic model to validate incoming POST requests for fake-data generation:

```python theme={null}
# src/models/fake_data_request.py
from pydantic import BaseModel
from typing import Optional

class FakeDataRequest(BaseModel):
    """
    Request model for fake data generation.

    Attributes:
        data_type (str): Type of fake data to generate (e.g., "name", "email", "phone")
        count (int): Number of records to generate
        locale (str, optional): Locale for data generation (not used in our generators)
    """
    data_type: str
    count: int
    locale: Optional[str] = "en_US"
```

Pydantic provides automatic validation and descriptive errors for missing/invalid fields.

## Router and generating fake data (no third-party Faker)

To keep dependencies minimal, this project uses simple Python-based generators rather than the external `faker` library. The API exposes a POST endpoint `/getfakedata` which maps `data_type` to a generator function:

```python theme={null}
# src/api/endpoints/router.py
from fastapi import APIRouter, HTTPException
from api.models.fake_data_request import FakeDataRequest
import random
import string

router = APIRouter()

def generate_random_name() -> str:
    first_names = ["John", "Jane", "Michael", "Sarah", "David", "Lisa"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_email() -> str:
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "example.com"]
    username = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"{username}@{random.choice(domains)}"

def generate_random_phone() -> str:
    area_code = random.randint(100, 999)
    prefix = random.randint(100, 999)
    line = random.randint(1000, 9999)
    return f"{area_code}-{prefix}-{line}"

DATA_GENERATORS = {
    "name": generate_random_name,
    "email": generate_random_email,
    "phone": generate_random_phone
}

@router.get("/")
async def read_root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to the FastAPI application!"}

@router.post("/getfakedata")
async def generate_fake_data(request: FakeDataRequest) -> dict:
    """
    Generate fake data based on the provided parameters.

    Request body example:
    {
        "data_type": "name",
        "count": 3
    }

    Supported data_type values: "name", "email", "phone"
    """
    try:
        if request.data_type not in DATA_GENERATORS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid data_type. Supported types: {list(DATA_GENERATORS.keys())}"
            )

        generator = DATA_GENERATORS[request.data_type]
        data = [generator() for _ in range(request.count)]

        return {"data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

This single router organizes endpoints and keeps a clear mapping between `data_type` and the generator function.

Supported data types and generators:

| data\_type | Generator                             |
| ---------: | ------------------------------------- |
|     `name` | Random first + last name              |
|    `email` | Random 8-char username + domain       |
|    `phone` | US-style numeric phone `XXX-XXX-XXXX` |

## Example request / response

Send a POST to `/getfakedata` with JSON:

```json theme={null}
{
  "data_type": "name",
  "count": 3
}
```

A typical successful response:

```json theme={null}
{
  "data": [
    "David Williams",
    "Michael Johnson",
    "John Smith"
  ]
}
```

Validation error when required fields are missing (FastAPI returns 422):

```json theme={null}
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

Invalid `data_type` example (400 response):

```json theme={null}
{
  "detail": "Invalid data_type. Supported types: ['name', 'email', 'phone']"
}
```

## Running and testing

Start the app:

```bash theme={null}
python main.py
```

Use curl, httpie, or Postman to test endpoints:

* POST `http://localhost:8000/getfakedata` with JSON shown above.
* Visit `http://localhost:8000/docs` for automatically generated OpenAPI docs.

Watch Uvicorn logs to see incoming requests and response codes (200/422/400).

> **lightbulb** When using Copilot or any code generator, treat the output as a draft: validate imports, run tests, and adapt generated code to your project structure (packages, relative imports, DB paths). In this example we intentionally replaced external Faker usage with small local generators to reduce dependencies and keep full control over output.

## Next steps (wiring DB queries and expanding features)

Suggested enhancements to connect the API to the SQLite dataset and make it production-ready:

* Wire endpoints to query `fake_data` using `get_db()` (SQLAlchemy session). Example pattern:
  ```python theme={null}
  from fastapi import Depends
  from db.database import get_db
  from sqlalchemy.orm import Session

  @router.get("/rows")
  def read_rows(limit: int = 10, db: Session = Depends(get_db)):
      # use raw SQL or SQLAlchemy models to query `fake_data` table
      rows = db.execute("SELECT * FROM fake_data LIMIT :limit", {"limit": limit}).fetchall()
      return {"rows": [dict(r) for r in rows]}
  ```
* Add query parameters or dedicated endpoints for filtering (by city, age, occupation), sorting, and pagination.
* Add unit tests for endpoints and generator functions (pytest).
* Add API documentation notes and curated OpenAPI examples (FastAPI supports `response_model` and `examples`).
* Consider using SQLAlchemy models to map `fake_data` rows to ORM objects for cleaner queries.

## Links and references

* FastAPI docs: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
* SQLAlchemy: [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)
* SQLite: [https://www.sqlite.org/docs.html](https://www.sqlite.org/docs.html)
* Pydantic: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)

This completes the initial API scaffolding and simple fake-data generator. Next, we'll connect the API to the SQLite dataset and expand the feature set (filtering, pagination, and documentation).

- [Watch Video](https://learn.kodekloud.com/user/courses/github-copilot-in-action/module/5c3827f4-b200-4c22-90bb-e7c6540d96d8/lesson/d26b10e6-06a9-45c1-b7eb-ba284b532fe3)


# Building out our tool Wiring up the Backend

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-in-Action/Using-Copilot-Efficiently/Building-out-our-tool-Wiring-up-the-Backend/page

Guide showing how to replace Faker with an SQLite-backed repository in FastAPI, including a DB helper, parameterized queries, and debugging tips

In this lesson we finish wiring the fake-data tool so the FastAPI endpoint reads real rows from a local SQLite database (`fakedata.db`) instead of generating values with Faker. This walkthrough demonstrates how to:

* Replace in-memory or stub logic with a repository-backed data source
* Create a small DB helper for SQLite connections and row-to-dict conversion
* Use parameterized queries (`LIMIT ?`) and avoid common pitfalls (bindings, imports, DB path)
* Debug integration issues (module paths, missing tables, binding errors)

This is practical guidance for adapting an existing endpoint to a persistent data source while keeping the router thin and testable.

***

## 1) Original endpoint (Faker-based)

This was the original FastAPI endpoint that used the Faker library as a source of stubbed values:

```python theme={null}
from fastapi import APIRouter, HTTPException
from faker import Faker
from ..models.fake_data_request import FakeDataRequest

router = APIRouter()

@router.post("/getfakedata")
async def generate_fake_data(request: FakeDataRequest) -> dict:
    """
    Generate fake data based on the provided parameters.

    Args:
        request (FakeDataRequest): Request parameters for data generation

    Returns:
        dict: Generated fake data
    """
    try:
        fake = Faker(request.locale)

        if not hasattr(fake, request.data_type):
            raise HTTPException(status_code=400, detail="Invalid data type")

        # ... generate using Faker ...
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

Goal: replace the Faker generation with queries against an SQLite table so the endpoint returns real rows stored in `fake_data`.

***

## 2) Database table (reference)

Here is a sample table DDL used for the demo database:

```sql theme={null}
CREATE TABLE fake_data (
    first_name TEXT,
    last_name TEXT,
    email_address TEXT,
    age INTEGER,
    city TEXT,
    occupation TEXT
);
```

Validate the table schema with:

```sql theme={null}
PRAGMA table_info(fake_data);
```

This returns rows for the columns: `first_name`, `last_name`, `email_address`, `age`, `city`, `occupation`.

Table summary:

| Column name    | Type    | Description      |
| -------------- | ------- | ---------------- |
| first\_name    | TEXT    | Given name       |
| last\_name     | TEXT    | Family name      |
| email\_address | TEXT    | Contact email    |
| age            | INTEGER | Age in years     |
| city           | TEXT    | City name        |
| occupation     | TEXT    | Job / profession |

Tip: Use DB Browser for SQLite or the sqlite3 CLI to inspect the file and verify the `fake_data` table exists.

***

## 3) Add a DB connection helper

Create a tiny utility that opens the SQLite connection and sets `row_factory` so rows are easily converted to dictionaries for JSON responses:

```python theme={null}
