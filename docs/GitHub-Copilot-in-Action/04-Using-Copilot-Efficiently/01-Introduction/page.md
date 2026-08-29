# main.py
import sys

class FakeDataGenerator:
    """
    A class to generate fake data.
    """

    def run(self) -> None:
        """
        Runs the fake data generator.
        """
        print("Fake data generator is running...")


def main() -> None:
    """
    Main function to run the FakeDataGenerator.
    """
    generator = FakeDataGenerator()
    generator.run()


if __name__ == "__main__":
    main()
```

Run it to verify:

```bash theme={null}
(.venv) jeremy@Jeremys-Mac-Studio FakeDataGenerator % python main.py
Fake data generator is running...
```

***

## 3) Move the generator into its own module

As projects grow, keeping classes and functions in focused modules improves maintainability. Move `FakeDataGenerator` into `fake_data_generator.py` and import it from `main.py`.

`fake_data_generator.py`:

```python theme={null}
# fake_data_generator.py
class FakeDataGenerator:
    """
    A class to generate fake data.
    """

    def run(self) -> None:
        """
        Runs the fake data generator.
        """
        print("Fake data generator is running...")
```

Update `main.py` to import the class:

```python theme={null}
# main.py
from fake_data_generator import FakeDataGenerator

def main() -> None:
    """
    Main function to run the FakeDataGenerator.
    """
    generator = FakeDataGenerator()
    generator.run()

if __name__ == "__main__":
    main()
```

Run again to confirm behavior remains the same:

```bash theme={null}
(.venv) jeremy@Jeremys-Mac-Studio FakeDataGenerator % python main.py
Fake data generator is running...
```

***

## 4) Add a utility to request fake data from a local Ollama model

Create `create_fake_data.py`. It sends a prompt to an Ollama server running locally at `http://localhost:11434/api/generate`, asks for CSV-formatted fake data, and saves the returned raw CSV text to `fake_data.csv`.

`create_fake_data.py`:

```python theme={null}
# create_fake_data.py
from typing import Any, Dict, Optional
import requests

def create_ollama_prompt() -> str:
    """
    Returns:
        str: Formatted prompt for the model.
    """
    return """Generate fake data for 5 people in CSV format with these columns:
first_name,last_name,email_address,age,city,occupation
Please only return the raw CSV data without any additional text."""

def call_ollama_api(prompt: str) -> Optional[Dict[str, Any]]:
    """
    Sends a prompt to the Ollama API and returns the parsed JSON response.

    Args:
        prompt (str): The prompt to send to the model.

    Returns:
        Optional[Dict[str, Any]]: API response JSON or None on error.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "phi4:latest",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        return None

def main() -> None:
    """
    Main function to generate fake data and save to CSV.
    """
    prompt = create_ollama_prompt()
    response = call_ollama_api(prompt)

    # The exact response schema may vary depending on Ollama server version.
    # This example assumes the server returns a key named 'response' containing raw CSV text.
    if response and "response" in response:
        output_file = "fake_data.csv"
        with open(output_file, "w", newline="") as f:
            f.write(response["response"])
        print(f"Fake data has been saved to {output_file}")
    else:
        print("Failed to generate fake data or unexpected response format")

if __name__ == "__main__":
    main()
```

> **warning** Ollama's JSON schema can change across versions. If the server returns fields like `output` or nested objects, inspect the raw JSON and update the key access accordingly before writing to disk.

Install `requests` in the virtual environment:

```bash theme={null}
(.venv) jeremy@Jeremys-Mac-Studio FakeDataGenerator % pip install requests
```

Run the script:

```bash theme={null}
(.venv) jeremy@Jeremys-Mac-Studio FakeDataGenerator % python create_fake_data.py
Fake data has been saved to fake_data.csv
```

Sample generated CSV (example):

```text theme={null}
first_name,last_name,email_address,age,city,occupation
John,Doe,john.doe@example.com,28,New York,Software Engineer
Jane,Smith,jane.smith@example.com,34,San Francisco,Data Scientist
Emily,Jones,emily.jones@example.com,27,Boston,Graphic Designer
Michael,Taylor,michael.taylor@example.com,40,Chicago,Lawyer
Sarah,Garcia,sarah.garcia@example.com,31,Austin,Marketing Manager
```

***

## 5) Track project dependencies with requirements.txt

After installing project packages (for example, `requests`), capture them in `requirements.txt` so collaborators can recreate your environment.

Example:

```bash theme={null}
(.venv) jeremy@Jeremys-Mac-Studio FakeDataGenerator % pip freeze
certifi==2024.12.14
charset-normalizer==3.4.1
idna==3.10
requests==2.32.3
urllib3==2.3.0

(.venv) jeremy@Jeremys-Mac-Studio FakeDataGenerator % pip freeze > requirements.txt
```

Recreate the environment from `requirements.txt`:

```bash theme={null}
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

***

## 6) Create a robust .gitignore

Exclude the virtual environment directory and other generated artifacts from Git. Below is a practical `.gitignore` example to keep your repository clean.

<Frame>
  <img alt="A dark-themed code editor/chat screenshot showing a user asking how to keep git from seeing a .venv folder. GitHub Copilot is generating a reply that suggests creating a .gitignore file to exclude the virtual environment." />
</Frame>

Example `.gitignore` (partial):

```text theme={null}
# Virtual Environment
.venv/
venv/
ENV/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/

# IDE
.idea/
.vscode/
*.swp
.DS_Store
```

If your `.venv` was already committed, remove it from tracking:

```bash theme={null}
git rm -r --cached .venv
git commit -m "Remove .venv from git tracking"
```

Then add and commit the `.gitignore`:

```bash theme={null}
git add .gitignore
git commit -m "Add .gitignore file"
```

***

## Summary

* Created a new Python project with an isolated virtual environment.
* Scaffoled a minimal `FakeDataGenerator` and moved it into a dedicated module.
* Built `create_fake_data.py` to call a local Ollama model and save CSV-formatted fake data.
* Captured dependencies in `requirements.txt` and protected the repo with `.gitignore`.
* This example demonstrates how GitHub Copilot can accelerate boilerplate creation; future articles will show importing generated data into a database and using it for more advanced workflows.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-copilot-in-action/module/5c3827f4-b200-4c22-90bb-e7c6540d96d8/lesson/d6c93d07-7c40-4bc5-aadc-c2ba049145fd)


# Introduction

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-in-Action/Using-Copilot-Efficiently/Introduction/page

Guide to building a FastAPI fake data generator API with Copilot, including scaffolding, endpoints, CSV/JSON/text exports, unit tests, and OpenAPI documentation

In this final section we'll master GitHub Copilot in Action and the core features used to build a simple, production-like tool: a Fake Data Generator API built with FastAPI.

In this module we'll:

* Provide a concise project introduction and outline goals.
* Create a new Python project scaffold.
* Implement a fake data generator service with inline code documentation.
* Add unit tests to verify behavior.
* Generate and enhance API documentation (OpenAPI).
* Demonstrate how AI pair programming (Copilot) can accelerate each step.

What are we going to build?

Your organization now prohibits the use of real customer data for testing. To comply, tests and development must rely on synthetic—but realistic—data. The solution here is a small API that generates structured mock data suitable for tests and demos, and that can export results as JSON, plain text, or CSV.

> **warning** Do not use real customer data for testing. Generate synthetic data that resembles real-world records while preserving privacy.

Key features of the Fake Data Generator API:

* Generate a configurable number of fake records (names, emails, ages, city, occupation).
* Export generated data in JSON, CSV, or plain text formats.
* Provide a clean REST endpoint surface for easy consumption by tests or other services.
* Include automated unit tests and comprehensive API documentation.

Example output produced by the API:

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

This API will be implemented with Python and FastAPI (see: [Python API Development with FastAPI](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi)). It will expose endpoints for generating data and downloading it in multiple formats.

<Frame>
  <img alt="A presentation slide titled &#x22;What We'll Build&#x22; showing a &#x22;Build an API in Python&#x22; box with an API icon and the Python logo. Below it are stacked file icons and text indicating generation of fake data (text files/CSV)." />
</Frame>

API design overview

| Resource                   | Purpose                             | Example / Notes                                                         |     |        |
| -------------------------- | ----------------------------------- | ----------------------------------------------------------------------- | --- | ------ |
| `POST /api/v1/getfakedata` | Generate N fake records             | Request body: `{"count": 10}` — supports query params for \`format=json | csv | text\` |
| `GET /api/v1/health`       | Simple health check                 | Returns `{"status": "ok"}`                                              |     |        |
| Documentation              | Auto-generated OpenAPI (Swagger UI) | FastAPI provides `/docs` and `/redoc` out of the box                    |     |        |

Example request body for generating data:

* `{"count": 2}` (wrap JSON in the request when calling the endpoint)

Unit testing

We'll add pytest-based unit tests that patch the data generation function. Here's a sample test that verifies the POST endpoint returns the expected fake data:

```python theme={null}
def test_get_fake_data_endpoint_success(sample_data):
    """Test successful API endpoint call."""
    with patch('app.main.fetch_fake_data', return_value=sample_data):
        response = client.post("/api/v1/getfakedata", json={"count": 2})

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json() == sample_data
```

Testing notes:

* Use fixtures (`sample_data`) to provide deterministic expected results.
* Patch the internal data-fetching/generation function to isolate endpoint behavior.
* Validate status codes, payload shape, and content.

Documentation and discoverability

FastAPI automatically generates OpenAPI documentation and interactive UIs at `/docs` (Swagger UI) and `/redoc`. To make the API easy for engineering teams to consume:

* Add detailed Pydantic models with field descriptions.
* Provide example request/response bodies in endpoint docstrings.
* Include usage examples for each supported export format (JSON/CSV/text).

> **lightbulb** Best practice: add small, copy-pasteable examples in your docstrings and OpenAPI `examples` so other teams can quickly integrate the fake-data generator into CI tests and development workflows.

Next steps (recommended development checklist)

1. Scaffold the project (virtualenv/poetry, FastAPI, Uvicorn, Faker for realistic data).
2. Implement endpoints and Pydantic models for strong typing and auto-docs.
3. Add CSV/text serialization helpers (ensure correct CSV headers and escaping).
4. Write pytest tests with fixtures and function patching to ensure deterministic outcomes.
5. Use Copilot as an assistant: generate stubs, create example tests, and refine docstrings.
6. Publish README with usage examples and link to `/docs`.

References

* FastAPI documentation: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
* pytest documentation: [https://docs.pytest.org/en/stable/](https://docs.pytest.org/en/stable/)
* Faker library for realistic fake data: [https://faker.readthedocs.io/](https://faker.readthedocs.io/)

This completes the planning and overview. The following sections will guide you through scaffolding the project, implementing the generator, writing tests, and publishing documentation — all while demonstrating how Copilot can accelerate each task.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-copilot-in-action/module/5c3827f4-b200-4c22-90bb-e7c6540d96d8/lesson/66b0f39e-c626-4903-a97f-6f7222a53225)
