# app.py
import csv
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from datetime import datetime
import hashlib
import logging

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # Change this to a random secret key in production
app.config['DATABASE'] = os.path.join(app.instance_path, 'task_manager.sqlite')

def read_csv(file_path):
    """Read and print rows from a CSV file."""
    with open(file_path, 'r') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            print(row)

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

def init_db():
    """Initialize the SQLite database with the required schema."""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        due_date TEXT,
                        created_at TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()
```

With this context loaded, Cursor AI can suggest commands and scaffolding that align perfectly with your codebase.

## 1. Installing PyTest and Updating Dependencies

To add testing support to your project:

```bash theme={null}
pip install pytest
pip freeze | grep pytest >> requirements.txt
```

You can prompt Cursor AI with:

> Install PyTest and update requirements.txt

…and it will execute the above two commands for you.

> **lightbulb** Pin your test dependencies to avoid version conflicts. For example, add `pytest>=8.0,<9.0` in your `requirements.txt`.

## 2. Generating a Test Suite

Cursor AI can scaffold test files based on your code structure. For example:

```bash theme={null}
touch tests/test_app.py
```

And populate it with:

```python theme={null}
# tests/test_app.py
import os
import tempfile
import pytest
from app import app, init_db

@pytest.fixture
def client():
    # Create a temporary database
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_delete_task(client):
    response = client.post('/task/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Task deleted successfully!' in response.data
    assert b'Test Task' not in response.data
```

## 3. Running Tests and Interpreting Failures

To run your tests:

```bash theme={null}
python -m pytest tests/test_app.py
```

Example output:

```plaintext theme={null}
=================================== test session starts ====================================
platform darwin -- Python 3.13.1, pytest-8.3.5, pluggy-1.5.0
rootdir: /Users/jeremy/Projects/KodeKloudTaskManager
collected 6 items

tests/test_app.py .....F.                                                        [100%]
========================================= FAILURES =========================================
___________________________________ test_register __________________________________________

    def test_register(client):
>       assert b'Account created successfully!' in response.data
E       AssertionError: assert b'Account created successfully!' in b'<!DOCTYPE html>\n<html lang="en">\n<head>...'
```

Failures like these are expected. Refining your prompt—by specifying file paths, function names, or expected output—will help Cursor AI generate more accurate assertions.

## 4. Profiling Data Processing

To profile your `app.py` or any CPU-bound function:

```bash theme={null}
python -m cProfile -o profile.stats app.py
```

Analyze the results:

```plaintext theme={null}
197138 function calls (190006 primitive calls) in 0.138 seconds

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   ...
```

## 5. Handling Port Conflicts

When you start the Flask server and port 5000 is occupied, you’ll see an error:

```plaintext theme={null}
OSError: [Errno 98] Address already in use
```

> **triangle-alert** If you encounter a port conflict, restart the server on a different port:

  ```bash theme={null}
  flask run --port=5001
  ```

## Best Practices for Context-Aware Commands

| Best Practice                      | Description                                                                       |
| ---------------------------------- | --------------------------------------------------------------------------------- |
| Provide a Project Overview         | Explain your app’s framework (e.g., Flask), directory layout, and key components. |
| Reference Actual Files and Paths   | Use exact file names like `app.py` or `tests/test_app.py` in your prompt.         |
| Specify Environment Details        | Include Python version, virtual environment name, and dependency constraints.     |
| Define Constraints or Requirements | For example: “Use `httpx` instead of `requests`” or “No global variables.”        |

### Example Prompt Context

```plaintext theme={null}
This is a Flask project at ~/Projects/KodeKloudTaskManager.
I want to run only tests in tests/test_app.py using Python 3.13.1 in my venv.
```

## Inline Terminal Questions

You can ask quick questions directly in the terminal:

```bash theme={null}
# Ask: What is pylintrc?
```

Cursor AI responds:

> A `.pylintrc` file is the configuration for [pylint][pylint-doc], a static code analysis tool for Python.

***

## Links and References

* [Flask Documentation][flask-doc]
* [pytest Documentation][pytest-doc]
* [cProfile Usage Guide][cprofile-doc]
* [pylint Configuration][pylint-doc]
* [Stack Overflow][stackoverflow]

[flask-doc]: https://flask.palletsprojects.com/en/latest/

[pytest-doc]: https://docs.pytest.org/en/stable/

[cprofile-doc]: https://docs.python.org/3/library/profile.html

[pylint-doc]: https://pylint.org/

[stackoverflow]: https://stackoverflow.com/

- [Watch Video](https://learn.kodekloud.com/user/courses/cursor-ai/module/90a13f7e-74a3-4207-8c34-c81c14757507/lesson/33201b75-117a-4299-9be5-9f8fe1651fd3)


# Demo Natural Language Commands

Source: https://notes.kodekloud.com/docs/Cursor-AI/Terminal-Productivity/Demo-Natural-Language-Commands/page

Explore how Cursor’s integrated terminal lets you run plain-language instructions to automate your development workflow.

Explore how Cursor’s integrated terminal—powered by Visual Studio Code—lets you run plain-language instructions to automate your development workflow.

## Prerequisites

* Visual Studio Code with Cursor AI extension installed
* Python 3.x and `venv` support
* Z Shell (Zsh) configured as your default shell

## 1. Open the Integrated Terminal

Open the terminal via **Terminal > New Terminal** (or press Ctrl+` on Windows/Linux, ⌘+` on macOS). You’ll start in a Z Shell session:

```bash theme={null}
jeremy@MACSTUDIO kodekloud1 % ps
  PID   TTY          TIME CMD
 70600 ttys000    0:00.00 -zsh
 80016 ttys002    0:00.01 /bin/zsh -i
 80061 ttys006    0:00.02 /bin/zsh -i
jeremy@MACSTUDIO kodekloud1 % ls -la
total 0
drwxr-xr-x   2 jeremy  staff   64 Mar 24 21:26 .
drwxr-xr-x  28 jeremy  staff  896 Mar 24 21:26 ..
```

| Action          | Shortcut / Command       | Description                               |
| --------------- | ------------------------ | ----------------------------------------- |
| Open Terminal   | Ctrl+` / ⌘+`             | Launches the integrated terminal          |
| Command Palette | Ctrl+Shift+P / ⌘+Shift+P | Opens the Command Palette for NL commands |

## 2. Generate a Flask API Project

Invoke the Command Palette (Ctrl+Shift+P / ⌘+Shift+P) and type your natural-language instruction:

> “Create a Flask API project with SQLAlchemy.”

After hitting Enter, Cursor AI runs:

```bash theme={null}
jeremy@MACSTUDIO kodekloud1 % mkdir -p app/models app/routes \
  && touch app/__init__.py app/models/__init__.py app/routes/__init__.py \
  && echo -e "flask\nflask-sqlalchemy\nflask-migrate" > requirements.txt
```

## 3. Set Up a Python Virtual Environment

Next, ask:

> “Create a Python virtual environment and activate it.”

```bash theme={null}
jeremy@MACSTUDIO kodekloud1 % python3 -m venv venv && source venv/bin/activate
(venv) jeremy@MACSTUDIO kodekloud1 %
```

> **lightbulb** Using virtual environments isolates dependencies per project. Always activate your `venv` before installing packages.

## 4. Install Testing and Database Drivers

Ask Cursor AI:

> “Install PyTest and the PostgreSQL driver.”

```bash theme={null}
(venv) jeremy@MACSTUDIO kodekloud1 % pip install pytest psycopg2-binary
Collecting pytest
  Downloading pytest-8.3.5-py3-none-any.whl
Collecting psycopg2-binary
  Downloading psycopg2_binary-2.9.10-cp313-cp313-macosx_*.whl
Successfully installed pytest-8.3.5 psycopg2-binary-2.9.10
```

Then update your `requirements.txt`:

```bash theme={null}
(venv) jeremy@MACSTUDIO kodekloud1 % pip freeze > requirements.txt
```

## 5. Handling Import Errors

If you encounter:

```text theme={null}
ModuleNotFoundError: No module named 'flask_sqlalchemy'
```

simply instruct Cursor AI:

```bash theme={null}
(venv) jeremy@MACSTUDIO kodekloud1 % pip install flask-sqlalchemy
```

## 6. Best Practices for Natural Language Commands

| Best Practice                 | Description                                                          |
| ----------------------------- | -------------------------------------------------------------------- |
| Be Specific Yet Concise       | Focus on required packages, directories, or flags without fluff.     |
| Include Essential Details     | Specify file names, frameworks, or versions in your instruction.     |
| Iterate: Run, Observe, Refine | Adjust your prompt based on Cursor’s output for accuracy.            |
| Combine Related Tasks         | Group folder creation, file initialization, and dependency installs. |
| Learn from AI Suggestions     | Study generated commands to level up your CLI proficiency.           |

> **triangle-alert** Overly vague instructions may lead to unexpected operations. Always review generated commands before executing.

***

By leveraging Cursor AI’s natural language commands, you reduce context switching and automate routine setup tasks. Extend this workflow to SSH sessions, container orchestrations, and more advanced development scenarios.

## Links and References

* [Visual Studio Code Integrated Terminal](https://code.visualstudio.com/docs/editor/integrated-terminal)
* [Cursor AI Extension](https://marketplace.visualstudio.com/)
* [Python `venv` Documentation](https://docs.python.org/3/library/venv.html)
* [Flask Official Docs](https://flask.palletsprojects.com/)
* [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
* [pytest Documentation](https://docs.pytest.org/)
* [psycopg2-binary on PyPI](https://pypi.org/project/psycopg2-binary/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cursor-ai/module/90a13f7e-74a3-4207-8c34-c81c14757507/lesson/bfdf5529-37b9-4663-8b78-a73acb77e7e7)
