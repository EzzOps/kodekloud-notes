# app.py
import hashlib
import functools
from flask import Flask, request, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your-secret-key'

def hash_password(password: str) -> str:
    """Simple password hashing (not secure for production)."""
    return hashlib.sha1(password.encode()).hexdigest()

def login_required(view):
    """Decorator to ensure a user is logged in."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            # Insert user into the database...
            pass
    return f"Register Page. Error: {error}"
```

> **triangle-alert** Using SHA-1 for password hashing is not secure for production. Consider `bcrypt` or `scrypt` for real-world applications.

***

## Inline Prompt vs Separate Chat

Most AI coding tools offer two modes. Choose based on your task:

| Mode          | Shortcut           | Best Use Cases                                       |
| ------------- | ------------------ | ---------------------------------------------------- |
| Separate Chat | Command L / Ctrl L | Deep discussions, design reviews, large refactors    |
| Inline Prompt | Command K / Ctrl K | Quick edits, helper functions, localized refactoring |

***

## Generating a Helper Function Inline

1. Highlight the code location.
2. Invoke the inline prompt (⌘-K / Ctrl-K).
3. Ask for a helper function, e.g., *“Create a function to reverse a string.”*

The AI will generate:

```python theme={null}
def reverse_string(s: str) -> str:
    """
    Reverses a string.

    Args:
        s (str): The string to reverse.

    Returns:
        str: The reversed string.
    """
    return s[::-1]
```

Green lines indicate additions; red lines show removals. Press **⌘-Y / Ctrl-Y** to accept or **⌘-N / Ctrl-N** to reject.

***

## Evolving Code with Inline Edits

You can request optimizations or new features inline. For example, add logging and error handling to your `login_required` decorator:

```python theme={null}
def login_required(view):
    """Decorator to ensure a user is logged in, with logging and error handling."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        try:
            if 'user_id' not in session:
                app.logger.warning(f"Unauthorized access attempt to {request.path}")
                flash("Please log in to access this page", "error")
                return redirect(url_for('login'))
            return view(**kwargs)
        except Exception as e:
            app.logger.error(f"Error in login_required decorator: {e}")
            flash("An unexpected error occurred. Please try again.", "error")
            return redirect(url_for('login'))
    return wrapped_view
```

By refining code inline, you maintain momentum and iterate faster on performance, security, and feature improvements.

***

## When to Use Each Mode

* **Separate Chat**
  * Deep architectural discussions
  * Reviewing or documenting large codebases
* **Inline Prompt**
  * Fast helper functions
  * Small bug fixes or refactors
  * Localized testing and debugging

Experiment with both to find the balance that boosts your productivity and minimizes context switching.

***

## Links and References

* [Flask Documentation](https://flask.palletsprojects.com/)
* [Python `hashlib` Module](https://docs.python.org/3/library/hashlib.html)
* [bcrypt on PyPI](https://pypi.org/project/bcrypt/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cursor-ai/module/d1d14592-151e-49c5-912f-1070dae4d5a8/lesson/7a7f60e2-e53c-4291-a0f9-0c2486a20650)


# Demo Lint Error Resolution

Source: https://notes.kodekloud.com/docs/Cursor-AI/Inline-Editing-and-Debugging/Demo-Lint-Error-Resolution/page

This guide covers resolving linting errors in Python projects using Flake8, Pylint, and isort for improved code quality and PEP 8 compliance.

In this guide, we’ll walk through resolving linting errors in a Python project using Flake8, Pylint, and isort. You’ll learn how to install and configure these tools, run them against your codebase, and fix common issues such as trailing whitespace, missing newlines, import order problems, and missing docstrings. By the end, your Python code will be more readable, consistent, and PEP 8–compliant.

## Table of Contents

1. [Install Linters and Formatters](#1-install-linters-and-formatters)
2. [Configure Pylint](#2-configure-pylint)
3. [Running and Fixing Pylint Errors](#3-running-and-fixing-pylint-errors)
   * 3.1 [Trailing Whitespace (C0303)](#31-trailing-whitespace-c0303)
   * 3.2 [Missing Final Newline (C0304)](#32-missing-final-newline-c0304)
   * 3.3 [Import Order (C0411)](#33-import-order-c0411)
   * 3.4 [Missing Docstrings (C0116)](#34-missing-docstrings-c0116)
   * 3.5 [Redefining Built-ins (W0622)](#35-redefining-built-ins-w0622)
4. [Example Application Snippet](#4-example-application-snippet)
5. [Database Schema Definition](#5-database-schema-definition)
6. [Automating Lint Fixes](#6-automating-lint-fixes)
7. [References](#7-references)

***

## 1. Install Linters and Formatters

Install Flake8, Pylint, isort, and their dependencies:

```bash theme={null}
pip install flake8 pylint isort tomlkit pyflakes pycodestyle mccabe
```

Verify installation:

```plaintext theme={null}
Successfully installed flake8-7.1.2 pylint-3.3.6 isort-5.12.0 ...
```

| Tool   | Purpose                      | Command         |
| ------ | ---------------------------- | --------------- |
| Flake8 | Combined style & error check | `flake8 .`      |
| Pylint | Static code analysis         | `pylint app.py` |
| isort  | Automatic import sorting     | `isort .`       |

## 2. Configure Pylint

Create a `.pylintrc` at the project root:

```ini theme={null}
[MASTER]
jobs=1

[MESSAGES CONTROL]
disable=
    C0114,  # Missing module docstring
    C0115,  # Missing class docstring
    C0116   # Missing function docstring

[REPORTS]
output-format=colorized
score=yes
reports=no

[FORMAT]
max-line-length=79
indent-string=' '
indent-after-paren=4
expected-line-ending-format=LF

[DESIGN]
max-args=5
max-locals=15
```

> **lightbulb** Adjust `max-line-length` and other limits to match your team's style guide.

## 3. Running and Fixing Pylint Errors

Run Pylint on your main file:

```bash theme={null}
pylint app.py
```

Sample output:

```plaintext theme={null}
app.py:14:4: C0303: Trailing whitespace
app.py:136:0: C0304: Final newline missing
app.py:144:0: C0116: Missing function docstring
...
Your code has been rated at 7.11/10
```

| Code  | Description                | Fix Example                        |
| ----- | -------------------------- | ---------------------------------- |
| C0303 | Trailing whitespace        | Remove trailing spaces on a line   |
| C0304 | Missing final newline      | Add a blank line at end of file    |
| C0116 | Missing function docstring | Write a docstring for the function |
| C0411 | Incorrect import order     | Group and reorder imports          |
| W0622 | Redefining built-in        | Rename variable to avoid shadowing |

### 3.1 Trailing Whitespace (C0303)

Before:

```python theme={null}
@app.route('/dashboard')
@login_required  
def dashboard():
    ...
```

Remove the extra spaces:

```bash theme={null}
pylint app.py
```

### 3.2 Missing Final Newline (C0304)

Add a blank line at the end:

```diff theme={null}
-    return result
+    return result
+
```

### 3.3 Import Order (C0411)

Incorrect:

```python theme={null}
import flask
from datetime import datetime
```

Correct:

```python theme={null}
import os
from datetime import datetime

import flask
from flask import Flask
```

Automatically sort imports:

```bash theme={null}
isort app.py
```

### 3.4 Missing Docstrings (C0116)

Before:

```python theme={null}
def get_db():
    if 'db' not in g:
        ...
    return g.db
```

After adding:

```python theme={null}
def get_db():
    """Return a database connection, creating it if necessary."""
    if 'db' not in g:
        ...
    return g.db
```

### 3.5 Redefining Built-ins (W0622)

Rename variables that shadow built-ins:

Before:

```python theme={null}
def get_task(id):
    # ...
```

After:

```python theme={null}
def get_task(task_id):
    # ...
```

## 4. Example Application Snippet

```python theme={null}
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from datetime import datetime
import os
import sqlite3
import csv
