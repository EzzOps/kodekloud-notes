# app.py
import csv
import sqlite3
import os
import hashlib
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, g

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # Change this to a random secret key in production
app.config['DATABASE'] = os.path.join(app.instance_path, 'task_manager.sqlite')

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

def read_csv(file_path):
    """Read rows from a CSV file and print them."""
    with open(file_path, 'r') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            print(row)

# Database connection functions
def get_db():
    """Return a database connection, creating it if necessary."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Close the database connection at teardown."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

app.teardown_appcontext(close_db)

# Initialize the database using a schema file
def init_db():
    db = get_db()
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    print('Initialized the database.')

@app.cli.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    print('Initialized the database.')
```

<Callout icon="triangle-alert">
  Be sure to replace `app.config['SECRET_KEY']` with a secure, random value before deploying to production.
</Callout>

## Querying the Codebase

Leverage natural-language queries to pinpoint exactly what you need:

### 1. Finding the Database Connection

Ask: “Show me all the code used to connect to the database.”

```python theme={null}
def get_db():
    """Return a database connection, creating it if necessary."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db
```

Configuration line:

```python theme={null}
app.config['DATABASE'] = os.path.join(app.instance_path, 'task_manager.sqlite')
```

Teardown registration:

```python theme={null}
app.teardown_appcontext(close_db)
```

### 2. Locating CSV-Related Code

Ask: “Which parts of the code deal with CSV files?”

```python theme={null}
def read_csv(file_path):
    """Read rows from a CSV file and print them."""
    with open(file_path, 'r') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            print(row)
```

### 3. How the Database Is Initialized

Ask: “How does our application initialize a database?”

```python theme={null}
def init_db():
    db = get_db()
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    print('Initialized the database.')
```

And the CLI command:

```python theme={null}
@app.cli.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    print('Initialized the database.')
```

## Advanced Codebase Queries

Use `@codebase` filters to refine searches by file type or pattern:

```plaintext theme={null}
@codebase include:*.py exclude:*.js Show me all functions related to authentication
```

| Filter          | Description                                 | Example        |
| --------------- | ------------------------------------------- | -------------- |
| include:\<ext>  | Include only files with the given extension | `include:*.py` |
| exclude:\<ext>  | Exclude files by extension                  | `exclude:*.js` |
| name:\<pattern> | Search files by name pattern                | `name:auth*`   |

## Why Use This Feature?

* Rapidly locate configuration and connection logic
* Explore data-processing functions (e.g., CSV import)
* Inspect CLI commands and initialization routines
* Simplify refactoring by searching specific patterns

<Callout icon="lightbulb">
  Combine multiple filters and search terms to focus on specific modules or code patterns across your project.
</Callout>

Whether you’re migrating from [SQLite](https://www.sqlite.org/) to [PostgreSQL](https://www.postgresql.org/), integrating an ORM like [SQLAlchemy](https://www.sqlalchemy.org/), or diving into an unfamiliar codebase, the codebase feature provides instant, context-aware insights into your entire repository.

## Links and References

* [Flask Documentation](https://flask.palletsprojects.com/)
* [SQLite](https://www.sqlite.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cursor-ai/module/68862e8d-747f-43b7-9411-80812e93a277/lesson/7da299d0-e912-4a66-8718-f641167ebebf" />
</CardGroup>


# Demo Contextual References

Source: https://notes.kodekloud.com/docs/Cursor-AI/Interacting-with-your-Codebase/Demo-Contextual-References/page

This guide explores using Cursor AI’s contextual references for precise code exploration and review by including or excluding specific contexts.

In this guide, we’ll explore how to harness Cursor AI’s contextual references to focus on exactly the code you need—whether it’s specific files, functions, or even GitHub pull requests. By including or excluding contexts, you’ll get sharper, more relevant answers for code exploration and review.

## 1. Adding Context from Your Codebase

You can click **Add Context** on any file (or even just select particular functions) to include them in your AI session. For example, here’s our `app.py`:

```python theme={null}
import csv
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from datetime import datetime
import h5lib
import logging
