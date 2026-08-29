# main.py
import sys

class FakeDataGenerator:
    """
    Generates fake data.
    """
    def run(self):
        print("Fake data generator is running...")

def main():
    """Entrypoint for FakeDataGenerator."""
    generator = FakeDataGenerator()
    generator.run()

if __name__ == "__main__":
    main()
```

Save and execute:

```bash theme={null}
(.venv) $ python main.py
Fake data generator is running...
```

![The image shows a Visual Studio Code interface with a Python file named "main.py" open and a terminal at the bottom. The right panel features the "Ask Copilot" section for AI assistance.](https://kodekloud.com/kk-media/image/upload/v1752876964/notes-assets/images/GitHub-Copilot-Certification-Creating-a-New-Project/visual-studio-code-python-terminal.jpg)

***

## 4. Refactor Code into Modules

Clean architecture separates concerns. Ask Copilot to extract `FakeDataGenerator`:

**fake\_data\_generator.py**

```python theme={null}
class FakeDataGenerator:
    """
    Generates fake data.
    """
    def run(self):
        print("Fake data generator is running...")
```

Update **main.py** to import the module:

```python theme={null}
from fake_data_generator import FakeDataGenerator

def main():
    generator = FakeDataGenerator()
    generator.run()

if __name__ == "__main__":
    main()
```

Re-run to confirm:

```bash theme={null}
(.venv) $ python main.py
Fake data generator is running...
```

***

## 5. Generate Fake Data via Ollama (Local LLM)

We’ll create `create_fake_data.py` to call a local Ollama API at `http://localhost:11434/api/generate`, request CSV-formatted rows, and write them to `fake_data.csv`.

In Copilot Chat, prompt:

> “Generate a script that sends a CSV fake-data request to Ollama and saves the response.”

**create\_fake\_data.py**

```python theme={null}
import requests
from typing import Dict, Any

def create_ollama_prompt() -> str:
    return (
        "Generate fake data for 5 people in CSV format with these columns:\n"
        "first_name,last_name,email_address,age,city,occupation\n"
        "Only return raw CSV data."
    )

def call_ollama_api(prompt: str) -> Dict[Any, Any]:
    url = "http://localhost:11434/api/generate"
    payload = {"model": "phi4:latest", "prompt": prompt, "stream": False}
    try:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"API error: {e}")
        return {}

def main():
    prompt = create_ollama_prompt()
    result = call_ollama_api(prompt)
    if csv_data := result.get("response"):
        with open("fake_data.csv", "w", newline="") as f:
            f.write(csv_data)
        print("Saved fake_data.csv")
    else:
        print("Failed to generate data")

if __name__ == "__main__":
    main()
```

Install `requests` and run:

```bash theme={null}
(.venv) $ pip install requests
(.venv) $ python create_fake_data.py
Saved fake_data.csv
```

![The image shows a Visual Studio Code interface with a Python project open, displaying a file named create\_fake\_data.py. The terminal at the bottom shows commands related to running a fake data generator and listing models, while the right panel contains GitHub Copilot suggestions.](https://kodekloud.com/kk-media/image/upload/v1752876966/notes-assets/images/GitHub-Copilot-Certification-Creating-a-New-Project/vscode-python-project-create-fake-data.jpg)

**Sample `fake_data.csv`:**

```csv theme={null}
first_name,last_name,email_address,age,city,occupation
John,Doe,john.doe@example.com,28,New York,Software Engineer
Jane,Smith,jane.smith@example.com,34,San Francisco,Data Scientist
Emily,Jones,emily.jones@example.com,27,Boston,Graphic Designer
Michael,Taylor,michael.taylor@example.com,40,Chicago,Lawyer
Sarah,Garcia,sarah.garcia@example.com,31,Austin,Marketing Manager
```

***

## 6. Manage Dependencies and `.gitignore`

Export your locked dependencies:

```bash theme={null}
(.venv) $ pip freeze > requirements.txt
```

| File               | Purpose                                          |
| ------------------ | ------------------------------------------------ |
| `requirements.txt` | Lists exact package versions for reproducibility |
| `.gitignore`       | Omits local venvs, caches, and editor settings   |

**.gitignore**

```gitignore theme={null}
# Virtual environments
.venv/
venv/

# Python cache
__pycache__/
*.py[cod]

# VS Code settings
.vscode/

# macOS files
.DS_Store
```

> **triangle-alert** After adding `.gitignore`, remove any committed virtual environment:

  ```bash theme={null}
  git rm -r --cached .venv
  git commit -m "Remove venv from tracking"
  ```

Finally, commit your changes:

```bash theme={null}
git add requirements.txt .gitignore
git commit -m "Add dependencies and gitignore"
```

***

## Next Steps

You’ve successfully:

* Bootstrapped a Python repo with Git and Copilot
* Isolated dependencies in a virtual environment
* Scaffolded, refactored, and modularized code
* Integrated with a local Ollama LLM for data generation
* Locked dependencies and configured `.gitignore`

Next, connect your fake data pipeline to a database, add unit tests, or deploy to a cloud service.

***

## References

* [GitHub Copilot Documentation]
* [Python Virtual Environments]
* [Ollama API Docs]
* [VS Code]

[GitHub Copilot Documentation]: https://docs.github.com/en/copilot

[Python Virtual Environments]: https://docs.python.org/3/tutorial/venv.html

[Ollama API Docs]: https://ollama.com/docs/api

[VS Code]: https://code.visualstudio.com/

- [Watch Video](https://learn.kodekloud.com/user/courses/github-copilot-certification/module/a8b1c2a2-f3f7-4470-9347-0ad31f2ab3cc/lesson/a6662c6f-2a3a-457e-8953-d9b4074d660e)


# Introduction

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-Certification/Using-Copilot-Efficiently/Introduction/page

Learn to build a Fake Data Generator API in Python using GitHub Copilot for generating mock customer records in various formats.

In this guide, you’ll learn how to build a Fake Data Generator API in Python using GitHub Copilot. By the end, you’ll have a service that produces mock customer records in JSON, CSV, or plain text—perfect for development and testing without exposing real personal data.

## Table of Contents

* [Module Overview](#module-overview)
* [Project Scenario](#project-scenario)
* [Prerequisites](#prerequisites)
* [Setup and Installation](#setup-and-installation)
* [API Implementation](#api-implementation)
* [In-Code Documentation](#in-code-documentation)
* [Unit Testing with Pytest](#unit-testing-with-pytest)
* [Generate API Documentation](#generate-api-documentation)
* [AI Pair Programming](#ai-pair-programming)
* [References](#references)

***

## Module Overview

In this module, we will:

* Initialize a new Python project
* Implement the Fake Data Generator API using FastAPI
* Add comprehensive docstrings and inline comments
* Write unit tests with Pytest
* Auto-generate interactive API documentation
* Demonstrate AI pair programming with GitHub Copilot

***

## Project Scenario

A new company policy prohibits using real customer data in test environments. To comply and maintain developer productivity, we’ll build an API service that generates synthetic customer records on demand.

Example JSON output:

```json theme={null}
[
  {
    "first_name": "Catherine",
    "last_name": "Parker",
    "email_address": "catherine.parker@example.com",
    "age": 27,
    "city": "Austin",
    "occupation": "Graphic Designer"
  },
  {
    "first_name": "Ethan",
    "last_name": "Roberts",
    "email_address": "ethanroberts@fakemail.com",
    "age": 26,
    "city": "Denver",
    "occupation": "Photographer"
  }
]
```

![The image outlines a project to build an API in Python, which will generate fake data in formats like text files or CSV.](https://kodekloud.com/kk-media/image/upload/v1752876967/notes-assets/images/GitHub-Copilot-Certification-Introduction/python-api-fake-data-project.jpg)

***

## Prerequisites

* Python 3.8+
* [FastAPI](https://fastapi.tiangolo.com/)
* [Uvicorn](https://www.uvicorn.org/) or another ASGI server
* [Pytest](https://docs.pytest.org/)
* GitHub Copilot extension enabled in your IDE

> **lightbulb** Ensure your environment has Python 3.8 or later. Use a virtual environment to isolate dependencies.

***

## Setup and Installation

1. Create a project directory and initialize Git:
   ```bash theme={null}
   mkdir fake-data-api
   cd fake-data-api
   git init
   ```
2. Set up a virtual environment and install dependencies:
   ```bash theme={null}
   python -m venv venv
   source venv/bin/activate
   pip install fastapi uvicorn pytest github-copilot
   ```
3. Define the project structure:
   ```text theme={null}
   fake-data-api/
   ├── app/
   │   ├── main.py
   │   ├── schemas.py
   │   └── utils.py
   ├── tests/
   │   └── test_main.py
   ├── requirements.txt
   └── README.md
   ```

***

## API Implementation

In **app/main.py**, set up the FastAPI app and fake data endpoint:

```python theme={null}
from fastapi import FastAPI
from app.utils import generate_fake_customers
from app.schemas import RequestModel, CustomerModel

app = FastAPI(title="Fake Data Generator API", version="1.0.0")

@app.post("/api/v1/getfakedata", response_model=list[CustomerModel])
def get_fake_data(request: RequestModel):
    """
    Generate synthetic customer records.
    - **count**: Number of records to generate.
    - **format**: Output format (json, csv, text).
    """
    return generate_fake_customers(request.count)
```

In **app/schemas.py**, define Pydantic models:

```python theme={null}
from pydantic import BaseModel, Field

class RequestModel(BaseModel):
    count: int = Field(..., gt=0, description="Number of records to generate")

class CustomerModel(BaseModel):
    first_name: str
    last_name: str
    email_address: str
    age: int
    city: str
    occupation: str
```

In **app/utils.py**, use Faker to produce data:

```python theme={null}
from faker import Faker
from app.schemas import CustomerModel

fake = Faker()

def generate_fake_customers(count: int) -> list[CustomerModel]:
    return [
        CustomerModel(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email_address=fake.email(),
            age=fake.random_int(min=18, max=80),
            city=fake.city(),
            occupation=fake.job(),
        )
        for _ in range(count)
    ]
```

***

## In-Code Documentation

Each function and class includes a clear docstring and `Field` descriptions. This ensures that generated API docs are populated with useful information.

***

## Unit Testing with Pytest

In **tests/test\_main.py**, add tests for the `/api/v1/getfakedata` endpoint:

```python theme={null}
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

sample_data = [
    {
        "first_name": "Alice",
        "last_name": "Smith",
        "email_address": "alice.smith@example.com",
        "age": 30,
        "city": "Seattle",
        "occupation": "Engineer"
    }
]

def test_get_fake_data_endpoint_success():
    """Validate successful API call returns the requested number of records."""
    with patch("app.main.generate_fake_customers", return_value=sample_data):
        response = client.post("/api/v1/getfakedata", json={"count": 1})
    assert response.status_code == 200
    assert response.json() == sample_data
```

> **triangle-alert** Always mock external dependencies when unit testing to isolate behaviour and improve test reliability.

***

## Generate API Documentation

FastAPI automatically provides interactive docs:

* Swagger UI: `http://localhost:8000/docs`
* Redoc: `http://localhost:8000/redoc`

Start the server with:

```bash theme={null}
uvicorn app.main:app --reload
```

***

## AI Pair Programming

Use GitHub Copilot to accelerate:

* Generate boilerplate code for models and endpoints
* Write repetitive test cases
* Suggest docstrings and type hints

Copilot can turn comments into working code snippets—just review and adjust as needed.

![The image shows a digital illustration of two people interacting with a computer interface, alongside a detailed API response example. The text "What We'll Build" is displayed at the top.](https://kodekloud.com/kk-media/image/upload/v1752876968/notes-assets/images/GitHub-Copilot-Certification-Introduction/people-interacting-computer-api-response.jpg)

***

## References

| Resource       | Description                    | Link                                                                       |
| -------------- | ------------------------------ | -------------------------------------------------------------------------- |
| FastAPI Docs   | Official FastAPI documentation | [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)             |
| Pytest Docs    | Pytest testing framework       | [https://docs.pytest.org/](https://docs.pytest.org/)                       |
| Faker Library  | Generate fake data in Python   | [https://faker.readthedocs.io/](https://faker.readthedocs.io/)             |
| GitHub Copilot | AI coding assistant by GitHub  | [https://github.com/features/copilot](https://github.com/features/copilot) |

Feel free to explore and extend this Fake Data Generator API to suit your organization’s testing needs!

- [Watch Video](https://learn.kodekloud.com/user/courses/github-copilot-certification/module/a8b1c2a2-f3f7-4470-9347-0ad31f2ab3cc/lesson/25454073-c3f9-4576-aeaa-5ad000dc448e)
