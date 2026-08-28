# app.py (excerpt)
@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    # Build the SELECT query...
    return render_template('dash.html', tasks=tasks, users=users, statuses=statuses)
```

Ask Composer:

> “Help me debug this error.”

Composer identifies:

> **Issue:** You reference `dash.html`, but your templates directory contains `dashboard.html`.\
> **Solution:** Rename the template or update the call to `render_template('dashboard.html', …)`.

<Callout icon="lightbulb">
  Always verify your `templates/` folder matches the filenames you pass to `render_template()`.
</Callout>

### Applying the Fix

```diff theme={null}
-    return render_template('dash.html', tasks=tasks, users=users, statuses=statuses)
+    return render_template('dashboard.html', tasks=tasks, users=users, statuses=statuses)
```

Reload the page—the dashboard now renders correctly.

***

## 2. Debugging a Database Column Typo

Next, attempt to create a new task via the web interface:

<Frame>
  ![The image shows a "Task Manager" web application interface where a user can create a new task by entering details like title, description, assignee, and status. The interface also includes options to filter tasks by status and assignee.](https://kodekloud.com/kk-media/image/upload/v1752872693/notes-assets/images/Cursor-AI-Demo-Debugging-with-AI/task-manager-web-app-interface.jpg)
</Frame>

Submitting the form triggers:

```plaintext theme={null}
sqlite3.OperationalError: table tasks has no column named statu3

Traceback (most recent call last):
  File ".../flask/app.py", line 1478, in __call__
    response = self.handle_exception(e)
  ...
  File "app.py", line 193, in create_task
    db.execute(...)
```

### The Faulty INSERT Statement

In **app.py**, the handler is:

```python theme={null}
@app.route('/task/create', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        assigned_to = request.form['assignee']

        db.execute(
            'INSERT INTO tasks (title, description, statu3, created_by, assigned_to) '
            'VALUES (?, ?, ?, ?, ?)',
            (title, description, status, session['user_id'], assigned_to)
        )
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_task.html')
```

#### Feeding Code and Error to Composer

```plaintext theme={null}
sqlite3.OperationalError: table tasks has no column named statu3
```

```python theme={null}
db.execute(
    'INSERT INTO tasks (title, description, statu3, created_by, assigned_to) VALUES (?, ?, ?, ?, ?)',
    (title, description, status, session['user_id'], assigned_to)
)
```

Composer responds:

> **Cause:** The column name `statu3` is mistyped. It should be `status`.\
> **Fix:** Correct the column name in the SQL statement.

<Callout icon="triangle-alert">
  Double-check your database schema (e.g., `schema.sql`) before running migrations or inserts.
</Callout>

### Applying the Fix

```diff theme={null}
-    'INSERT INTO tasks (title, description, statu3, created_by, assigned_to) VALUES (?, ?, ?, ?, ?)',
+    'INSERT INTO tasks (title, description, status, created_by, assigned_to) VALUES (?, ?, ?, ?, ?)',
```

Save and refresh—the new task is created successfully.

***

## 3. Best Practices for AI-Assisted Debugging

| Error Type               | Common Cause      | Recommended Fix                                |
| ------------------------ | ----------------- | ---------------------------------------------- |
| Jinja2 TemplateNotFound  | Filename mismatch | Update `render_template()` to the correct name |
| sqlite3.OperationalError | Column name typo  | Correct the column in your SQL statement       |

1. Capture Complete Context
   * Include full tracebacks or error messages.
   * Paste only the relevant code where the error occurred.

2. Provide Schema or Definitions
   * Share your `schema.sql` or data models so the AI can verify table and column names.

3. Trust but Verify
   * Apply your own programming knowledge to confirm suggested changes align with your codebase.

4. Experiment with Multiple Models
   * If Composer’s recommendation isn’t clear, try another model (e.g., GPT-3.5, GPT-4, Gemini) or start a fresh session.

5. Use Logs as Supplemental Context
   * Include application or server logs (from SSH sessions or production environments) for deeper insights.

***

## Links and References

* [Flask Documentation](https://flask.palletsprojects.com/)
* [Jinja2 Error Handling](https://jinja.palletsprojects.com/en/latest/errors/)
* [SQLite Documentation](https://www.sqlite.org/docs.html)
* [Composer AI Assistant Guide](/docs/composer/usage)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cursor-ai/module/d1d14592-151e-49c5-912f-1070dae4d5a8/lesson/044c4552-89dd-4754-a8ce-810783ce56da" />
</CardGroup>


# Demo Inline AI Edits

Source: https://notes.kodekloud.com/docs/Cursor-AI/Inline-Editing-and-Debugging/Demo-Inline-AI-Edits/page

Learn to use inline AI-assisted editing in your code editor, comparing separate chat windows and inline prompts for improved workflow.

In this guide, you’ll learn how to use inline AI-assisted editing directly within your code editor. We’ll compare two common modes—**separate chat windows** versus **inline prompts**—and demonstrate how inline editing can streamline your workflow and reduce context switching.

## Why Inline AI Editing?

* Keeps you in the flow of coding
* Provides suggestions as diffs you can accept or reject
* Accelerates prototyping, refactoring, and helper-function generation

<Callout icon="lightbulb">
  Inline prompts work best for focused, localized changes. For broad design discussions, consider a separate chat to maintain context.
</Callout>

***

## Example: Simple Flask Authentication

Below is a minimal Flask app that demonstrates password hashing, an authentication decorator, and basic routes. We’ll use this code to show inline AI-powered enhancements.

```python theme={null}
