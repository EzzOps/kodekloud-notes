# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # Use a secure random key in production
app.config['DATABASE'] = os.path.join(app.instance_path, 'task_manager.sqlite')

def read_csv(file_path):
    """Read and print rows from a CSV file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            print(row)

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

def get_db():
    """Get or create the SQLite database connection."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Close the database connection if it exists."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.teardown_appcontext
def teardown_db(exception):
    """Teardown database connection after request."""
    close_db()
```

## 5. Database Schema Definition

```sql theme={null}
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS tasks;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
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
    FOREIGN KEY (created_by) REFERENCES users (id),
    FOREIGN KEY (assigned_to) REFERENCES users (id)
);
```

## 6. Automating Lint Fixes

You can integrate AI assistants or editor plugins to highlight lint errors and suggest fixes inline. For example, selecting an error message and asking “Help me fix this error” can automatically apply minor corrections like adding newlines or renaming variables.

<Callout icon="triangle-alert">
  Relying solely on automated fixes may overlook context-specific issues. Always review changes before committing.
</Callout>

## 7. References

* [Flake8 Documentation](https://flake8.pycqa.org/)
* [Pylint Documentation](https://pylint.pycqa.org/)
* [isort Documentation](https://pycqa.github.io/isort/)
* [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cursor-ai/module/d1d14592-151e-49c5-912f-1070dae4d5a8/lesson/90fdaf83-1575-4804-9513-16f836f9becc" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Cursor-AI/Inline-Editing-and-Debugging/Introduction/page

Learn to enhance your development workflow with inline editing and AI-driven debugging without switching contexts.

In this lesson, you’ll learn how to streamline your development workflow with powerful **inline editing** and **AI-driven debugging**—all without switching contexts. Using Cursor’s integrated tools, you can:

* Instantly apply AI-powered code edits
* Debug errors with intelligent suggestions
* Resolve lint issues on the fly

By the end of this guide, you’ll understand how to maintain a seamless coding experience by writing, editing, and debugging code directly in your editor.

<Callout icon="lightbulb">
  Before you begin, ensure you have Cursor installed and authenticated in your editor. Check out the [Cursor Quickstart Guide](https://cursor.so/docs/quickstart) for setup instructions.
</Callout>

## Key Features at a Glance

| Feature               | Benefit                                     | Example Command                               |
| --------------------- | ------------------------------------------- | --------------------------------------------- |
| AI-Powered Editing    | Refactor code in-line with natural prompts  | `// fix: simplify this function`              |
| AI-Assisted Debugging | Identify and patch runtime errors instantly | `// debug: why is this throwing NullPointer?` |
| Lint Error Resolution | Auto-fix common style and syntax issues     | `// lint: fix ESLint warnings in this file`   |

## What You’ll Achieve

1. Keep your hands on the keyboard—no more context switching
2. Leverage AI suggestions to write cleaner, bug-free code
3. Resolve lint and style violations without leaving your editor

With these tools at your fingertips, inline editing and debugging become part of your natural coding flow—boosting productivity and code quality from day one.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cursor-ai/module/d1d14592-151e-49c5-912f-1070dae4d5a8/lesson/65a2cdb3-f6e0-4a16-b10a-6cfa98a802aa" />
</CardGroup>
