# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')  # Change in production
app.config['DATABASE'] = os.path.join(app.instance_path, 'task_manager.sqlite')

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Database connection function
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db
```

> **triangle-alert** Always replace the default `SECRET_KEY` with a strong, unpredictable string before deploying to production.

***

## Specific vs. Creative Prompts

Knowing when to lock down every detail versus when to let the model surprise you is crucial:

* **Specific Prompts**\
  Provide clear objectives, constraints, and examples. Ideal for scaffolding or boilerplate code that must meet exact requirements.
* **Creative Prompts**\
  Offer a high-level request (e.g., “Build a task manager in Python”) and let the model explore solutions. Great for brainstorming or exploring alternatives.

![The image shows a code editor with a markdown file open, detailing the objectives and requirements for creating a task management application using Flask and SQLite. The editor interface includes a file explorer on the left and a chat or assistant panel on the right.](https://kodekloud.com/kk-media/image/upload/v1752872759/notes-assets/images/Cursor-AI-Demo-Essential-Prompt-Engineering/code-editor-markdown-flask-sqlite.jpg)

***

## Zero-Shot Prompting

Zero-shot means “no examples provided.” You simply state the task and expect the model to understand it.

**Use case:** Quick utility functions or well-defined algorithms.

**Example prompt:**
“Write a function that calculates the Fibonacci sequence up to *n* terms.”

```python theme={null}
def fibonacci(n):
    """Return the first n numbers in the Fibonacci sequence."""
    if n <= 0:
        return []
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

# Example usage:
print(fibonacci(10))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

> **lightbulb** Zero-shot is fast and straightforward, but your prompt must be unambiguous.

***

## One-Shot Prompting

One-shot gives the model one example of the desired format, then asks it to generalize.

**Prompt:**

1. Here’s a JavaScript function that sorts objects by a property:
   ```javascript theme={null}
   function sortByProperty(array, property) {
     // ...
   }
   ```
2. Now write a function that finds the intersection of two arrays.

**Model’s response:**

```javascript theme={null}
function findIntersection(arr1, arr2) {
  const set = new Set(arr1);
  return arr2.filter(item => set.has(item));
}

// Deep comparison for objects
function findIntersectionDeep(arr1, arr2) {
  return arr1.filter(item1 =>
    arr2.some(item2 => JSON.stringify(item1) === JSON.stringify(item2))
  );
}
```

***

## Few-Shot Prompting (Viewport Prompting)

Few-shot provides multiple examples so the model can learn a pattern before continuing.

**Examples:**

```javascript theme={null}
describe('User Authentication', () => {
  test('allows login with valid credentials', () => {
    // ...
  });

  test('rejects login with invalid password', () => {
    // ...
  });
});
```

**Prompt:**\
“Convert the requirement *User session expires after 30 minutes of inactivity* into a Jest test case.”

**Model’s response:**

```javascript theme={null}
describe('User Session Management', () => {
  beforeEach(() => jest.useFakeTimers());
  afterEach(() => jest.useRealTimers());

  test('expires session after 30 minutes of inactivity', () => {
    const session = createUserSession('testUser');
    expect(session.isActive()).toBe(true);

    jest.advanceTimersByTime(29 * 60 * 1000);
    expect(session.isActive()).toBe(true);

    jest.advanceTimersByTime(60 * 1000);
    expect(session.isActive()).toBe(false);
  });
});
```

***

## Chain-of-Thought Prompting

Ask the model to “think aloud,” providing step-by-step reasoning before delivering a solution.

**Prompt:**\
“Design a database schema for a social media app, reasoning through entities, relationships, and constraints.”

![The image shows a code editor with a Python script for a Flask application on the left and a chat interface on the right discussing the design of a database schema for a social media application.](https://kodekloud.com/kk-media/image/upload/v1752872760/notes-assets/images/Cursor-AI-Demo-Essential-Prompt-Engineering/flask-app-chat-database-schema.jpg)

**Generated SQL:**

```sql theme={null}
CREATE TABLE users ( ... );
CREATE TABLE posts ( ... );
-- and so on...
```

***

## Self-Consistency Prompting

Generate multiple candidate solutions, evaluate each, and select the best. This boosts reliability for critical tasks.

**Prompt:**\
“Write a regex matching valid email addresses, test it against these samples:

* [valid@example.com](mailto:valid@example.com)
* invalid@
* [user.name+tag@example.co.uk](mailto:user.name+tag@example.co.uk)
* @example.com”

```python theme={null}
import re

pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
tests = ['valid@example.com', 'invalid@', 'user.name+tag@example.co.uk', '@example.com']

for email in tests:
    print(email, 'Valid' if re.match(pattern, email) else 'Invalid')
```

**Advanced:** Use the `email-validator` library for robust checks.

***

## General Rules for Effective Prompting

1. Be specific and clear.
2. Provide context—code snippets, error logs, folder structure.
3. Use structured formats: bullets, numbered steps, or tables.
4. Specify output format (e.g., “Return TypeScript definitions”).
5. Iterate and refine based on model feedback.

![The image shows a code editor with a markdown file open, detailing the objectives and requirements for creating a task management application using Flask and SQLite. The editor sidebar displays a project directory structure.](https://kodekloud.com/kk-media/image/upload/v1752872762/notes-assets/images/Cursor-AI-Demo-Essential-Prompt-Engineering/code-editor-markdown-flask-sqlite-2.jpg)

### Prompting Techniques at a Glance

| Prompt Type      | Description                                  | Best For                              |
| ---------------- | -------------------------------------------- | ------------------------------------- |
| Zero-Shot        | No examples; rely on clear instructions      | Simple, well-defined tasks            |
| One-Shot         | Single example to demonstrate desired output | Specific formatting or pattern        |
| Few-Shot         | Multiple examples to establish a pattern     | Complex transformations               |
| Chain-of-Thought | Step-by-step reasoning before the answer     | Design, architecture, problem solving |
| Self-Consistency | Generate and compare several solutions       | High-stakes or precision requirements |

***

With these prompt engineering strategies in your toolkit, you can direct LLMs to produce consistent, accurate, and well-structured results. Happy prompting!

## Links and References

* [Flask Quickstart](https://flask.palletsprojects.com/en/latest/quickstart/)
* [SQLite Documentation](https://www.sqlite.org/docs.html)
* [Jest Testing Framework](https://jestjs.io/)
* [email-validator on PyPI](https://pypi.org/project/email-validator/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cursor-ai/module/e11e1c1e-9b6b-4c53-b14a-24babbd114a5/lesson/17047ff4-c233-4a86-8a14-4430c13ea027)


# Demo Getting Started with Composer

Source: https://notes.kodekloud.com/docs/Cursor-AI/Mastering-Autocompletion/Demo-Getting-Started-with-Composer/page

Build a lightweight task management app using Composer, Flask, and SQLite to track tasks without extra overhead.

Build a lightweight task management app using Composer, Flask, and SQLite. Track tasks—create, assign, update status—without extra overhead.

## Table of Contents

1. [Clone the Repository](#1-cloning-the-repository)
2. [Define the Project in Composer](#2-defining-the-project-with-composer)
3. [Composer Output Overview](#3-prompt-details-and-composer-output)
4. [Review the Database Schema](#4-reviewing-the-database-schema)
5. [Quick Project Structure](#5-quick-project-structure)
6. [Key Application Code (`app.py`)](#6-key-application-code-apppy)
7. [Install & Run](#7-installing--running)
8. [Inspect with DB Browser](#8-inspecting-with-db-browser)
9. [Use the Task Manager](#9-using-the-task-manager)
10. [Conclusion & References](#10-conclusion--references)

***

## 1. Cloning the Repository

Start by cloning a new, empty GitHub repo into your workspace.

![The image shows a software interface with options to open a project, clone a repository, or connect via SSH. A cursor is hovering over the "Clone repo" button.](https://kodekloud.com/kk-media/image/upload/v1752872763/notes-assets/images/Cursor-AI-Demo-Getting-Started-with-Composer/software-interface-clone-repo.jpg)

Select your destination folder (e.g., `projects/KodeKloud/task-manager`) and open it:

![The image shows a computer file browser window with folders and files displayed, including a highlighted folder named "jeremy" under the year 2024. The interface includes options for selecting a repository destination.](https://kodekloud.com/kk-media/image/upload/v1752872764/notes-assets/images/Cursor-AI-Demo-Getting-Started-with-Composer/file-browser-window-jeremy-folder.jpg)

We’ll commit all changes with Git as we proceed.

## 2. Defining the Project with Composer

Open Composer (⌘L / Ctrl+L). Craft a precise prompt so the LLM generates only what you need: Flask + SQLite, raw SQL, no JS frameworks.

![The image shows a text editor with a project objective to create a task management application using Flask and SQLite, detailing features like user authentication and task assignment.](https://kodekloud.com/kk-media/image/upload/v1752872766/notes-assets/images/Cursor-AI-Demo-Getting-Started-with-Composer/task-management-flask-sqlite-editor.jpg)

### Prompt Highlights

* **Objective:** Proof-of-concept task manager using Flask & SQLite3.
* **Features:**
  * Username/password authentication (Werkzeug hashing).
  * Task CRUD: create, assign, update status (`Not started`, `In progress`, `Complete`, `Blocked`, `Closed`).
  * List tasks with filters by status or assignee.
  * Jinja2 HTML/CSS templates (no React/Angular).
* **Requirements:**
  * Python 3.13+ & virtual environment
  * Single or minimal tables (no migrations)
  * Self-hosted development setup

> **lightbulb** Use strong hashing algorithms (e.g., `werkzeug.security`) and rotate your `SECRET_KEY` in production.

## 3. Prompt Details and Composer Output

Select your model (we used **Cloud 3.7 Sonnet**). Composer generates:

* `schema.sql`
* `app.py`
* `templates/` (`base.html`, `login.html`, `register.html`, `dashboard.html`)
* `static/style.css`
* `requirements.txt`

![The image shows a text editor with a list of requirements for a project, including using Python 3.13, Flask for front-end templates, and SQLite for data storage.](https://kodekloud.com/kk-media/image/upload/v1752872767/notes-assets/images/Cursor-AI-Demo-Getting-Started-with-Composer/text-editor-project-requirements-python-flask-sqlite.jpg)

![The image shows a text interface outlining the functionality of a task management application, including user account creation, task management, and main view features.](https://kodekloud.com/kk-media/image/upload/v1752872769/notes-assets/images/Cursor-AI-Demo-Getting-Started-with-Composer/task-management-app-interface.jpg)

![The image shows a dark-themed interface with text instructions for a task management application using Flask. It includes guidelines for displaying tasks, using basic HTML/CSS templates, and deployment in a self-hosted environment.](https://kodekloud.com/kk-media/image/upload/v1752872770/notes-assets/images/Cursor-AI-Demo-Getting-Started-with-Composer/flask-task-management-interface-guide.jpg)

After confirming, Composer scaffolds your project:

![The image shows a code editor with a project structure for a Flask task management application, including details about the main application, database schema, static files, HTML templates, and project dependencies.](https://kodekloud.com/kk-media/image/upload/v1752872772/notes-assets/images/Cursor-AI-Demo-Getting-Started-with-Composer/flask-task-manager-code-editor.jpg)

## 4. Reviewing the Database Schema

Open **schema.sql** to inspect `users` and `tasks` tables:

```sql theme={null}
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS tasks;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER NOT NULL,
    assigned_to INTEGER NOT NULL,
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (assigned_to) REFERENCES users(id)
);
```

## 5. Quick Project Structure

```text theme={null}
.
├── app.py
├── schema.sql
├── requirements.txt
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── login.html
    ├── register.html
    └── dashboard.html
```

## 6. Key Application Code (`app.py`)

```python theme={null}
import os, sqlite3, logging
from flask import Flask, g, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # Rotate in prod
app.config['DATABASE'] = os.path.join(app.instance_path, 'task_manager.sqlite')

def get_db():
    if 'db' not in g:
        os.makedirs(app.instance_path, exist_ok=True)
        g.db = sqlite3.connect(app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db: db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@app.cli.command('init-db')
def init_db_command():
    """Initialize the database."""
    init_db()
    print('Initialized the database.')
