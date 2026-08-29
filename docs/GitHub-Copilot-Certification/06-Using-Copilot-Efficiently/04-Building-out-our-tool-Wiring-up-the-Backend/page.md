# main.py
import sys
from fake_data_generator import FakeDataGenerator

def main():
    """
    Entry point for the FakeDataGenerator CLI.
    """
    generator = FakeDataGenerator()
    generator.run()

if __name__ == "__main__":
    main()
```

Open **GitHub Copilot Chat** in VS Code and ask:

```text theme={null}
I would like to create a web API in Python with my existing file.
```

If it suggests the wrong stack (e.g., TypeScript), use the context menu to clear or restart:

![The image shows a code editor with a file directory on the right, and a context menu open with options related to code suggestions or issues.](https://kodekloud.com/kk-media/image/upload/v1752876957/notes-assets/images/GitHub-Copilot-Certification-Building-out-our-tool-Creating-the-API/code-editor-file-directory-menu.jpg)

> **triangle-alert** Refine prompts carefully. Copilot can veer off into other languages or frameworks if not guided.

## Choosing the Right Framework

Let Copilot compare FastAPI, Flask, and Django REST Framework:

```text theme={null}
Which is the best Python framework for building a web API? List the pros and cons.
```

![The image shows a comparison of pros and cons for FastAPI, Flask, and Django REST Framework, highlighting features like performance, documentation, and community support.](https://kodekloud.com/kk-media/image/upload/v1752876958/notes-assets/images/GitHub-Copilot-Certification-Building-out-our-tool-Creating-the-API/fastapi-flask-django-comparison.jpg)

Here’s a quick comparison:

| Framework             | Pros                                     | Cons                                |
| --------------------- | ---------------------------------------- | ----------------------------------- |
| FastAPI               | High performance, auto-docs, async-ready | Learning curve for async patterns   |
| Flask                 | Lightweight, simple                      | Manual docs, slower for heavy loads |
| Django REST Framework | Batteries-included, admin UI             | Heavier footprint, more boilerplate |

We’ll proceed with **FastAPI** for its speed and automatic documentation.

## Generating the FastAPI Project Structure

Ask Copilot:

```text theme={null}
Create a FastAPI project with best practices.
```

It may suggest:

```text theme={null}
fastapi-project
└── src
    ├── api
    │   └── endpoints
    ├── core
    ├── db
    └── models
```

Open the workspace, rename it to **FakeDataGeneratorAPI**, then:

1. Move `src` contents to the project root.
2. Remove unused files (`.env`, `README.md`, etc.).
3. Add a `tests` folder at the root.

![The image shows a Visual Studio Code interface with a Python project directory structure for a REST API. The left panel displays the file explorer, and the right panel shows a proposed directory structure and a chat with GitHub Copilot.](https://kodekloud.com/kk-media/image/upload/v1752876960/notes-assets/images/GitHub-Copilot-Certification-Building-out-our-tool-Creating-the-API/vscode-python-rest-api-directory.jpg)

Final layout:

```text theme={null}
FakeDataGeneratorAPI
├── api
│   └── endpoints
├── core
├── db
├── models
├── main.py
└── tests
```

Use Copilot iteratively until you’re happy:

![The image shows a Visual Studio Code interface with a project directory structure for a FastAPI project, including various Python files and folders. The right panel displays a GitHub Copilot chat discussing the setup of the project.](https://kodekloud.com/kk-media/image/upload/v1752876961/notes-assets/images/GitHub-Copilot-Certification-Building-out-our-tool-Creating-the-API/vscode-fastapi-project-structure.jpg)

## Implementing the FastAPI Application

Install dependencies:

```bash theme={null}
pip install fastapi uvicorn
```

Create `main.py` at the root:

```python theme={null}
# main.py
from fastapi import FastAPI
from api.endpoints.router import router

app = FastAPI(title="FakeDataGeneratorAPI")
app.include_router(router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to FakeDataGeneratorAPI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run and verify:

```bash theme={null}
python main.py
# Visit http://localhost:8000
```

## Defining the Database Dependency

In `db/database.py`, configure SQLAlchemy for SQLite:

```python theme={null}
# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./fake_data_generator.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Yields a database session and ensures it closes after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Creating the Pydantic Request Model

Define `models/fake_data_request.py`:

```python theme={null}
# models/fake_data_request.py
from pydantic import BaseModel
from typing import Optional

class FakeDataRequest(BaseModel):
    """
    Schema for fake data generation requests.
    """
    data_type: str            # e.g., 'name', 'email'
    count: int                # number of records to generate
    locale: Optional[str] = "en_US"
```

## Implementing the Fake Data Endpoint

Install Faker:

```bash theme={null}
pip install faker
```

Add `/getfakedata` in `api/endpoints/router.py`:

```python theme={null}
# api/endpoints/router.py
from fastapi import APIRouter, HTTPException, Depends
from faker import Faker
from sqlalchemy.orm import Session
from models.fake_data_request import FakeDataRequest
from db.database import get_db

router = APIRouter()

@router.post("/getfakedata")
async def generate_fake_data(
    request: FakeDataRequest,
    db: Session = Depends(get_db)
) -> dict:
    """
    Generate and return fake data based on request parameters.
    """
    fake = Faker(request.locale)
    if not hasattr(fake, request.data_type):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid data_type: {request.data_type}"
        )

    data = [getattr(fake, request.data_type)() for _ in range(request.count)]
    # TODO: Persist `data` to the database using `db`
    return {"data": data}
```

## Testing the POST Endpoint

Send this request:

```http theme={null}
POST http://localhost:8000/api/getfakedata
Content-Type: application/json

{
  "data_type": "name",
  "count": 3
}
```

Expected response:

```json theme={null}
{
  "data": [
    "John Doe",
    "Jane Smith",
    "Michael Johnson"
  ]
}
```

## Next Steps

* Persist generated records into SQLite.
* Add OpenAPI metadata and detailed endpoint docs.
* Write tests in `tests/` to validate both database and API layers.

## Links and References

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
* [Pydantic Docs](https://pydantic-docs.helpmanual.io/)
* [Faker Library](https://faker.readthedocs.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-copilot-certification/module/a8b1c2a2-f3f7-4470-9347-0ad31f2ab3cc/lesson/6d744be0-5629-41a8-9435-1cde4802185b)


# Building out our tool Wiring up the Backend

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-Certification/Using-Copilot-Efficiently/Building-out-our-tool-Wiring-up-the-Backend/page

This lesson covers integrating a FastAPI application with an SQLite database, including repository creation, request modeling, and testing.

In this lesson, we’ll finish wiring our FastAPI application to an SQLite database—replacing the previous Faker-based generator. We will:

1. Create a repository module for database operations
2. Define a Pydantic request model
3. Refactor our router to call the repository
4. Integrate the router into the main application
5. Test and debug the implementation

> **lightbulb** This tutorial assumes you have a working FastAPI project structure and `uvicorn` installed.

***

## Table of Contents

* [Module Overview](#module-overview)
* [1. Database Repository](#1-database-repository)
* [2. Request Model](#2-request-model)
* [3. API Endpoint Router](#3-api-endpoint-router)
* [4. Main Application Integration](#4-main-application-integration)
* [5. Testing & Debugging](#5-testing--debugging)
* [6. Takeaways](#6-takeaways)
* [References](#references)

***

## Module Overview

| Module                  | File Path                             | Responsibility                         |
| ----------------------- | ------------------------------------- | -------------------------------------- |
| Repository Layer        | `src/data/fake_data_repository.py`    | Encapsulate SQLite operations          |
| Request Validation      | `src/api/models/fake_data_request.py` | Define Pydantic model for requests     |
| API Router              | `src/api/endpoints/router.py`         | Handle incoming requests and call repo |
| Application Entry Point | `src/main.py`                         | Initialize FastAPI and include router  |

***

## 1. Database Repository

Create `src/data/fake_data_repository.py` to centralize all SQLite interactions following the repository pattern.

```python theme={null}
