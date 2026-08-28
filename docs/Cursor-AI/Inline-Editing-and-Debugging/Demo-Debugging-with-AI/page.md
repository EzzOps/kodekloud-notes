# Demo Debugging with AI

Source: https://notes.kodekloud.com/docs/Cursor-AI/Inline-Editing-and-Debugging/Demo-Debugging-with-AI/page

Learn to use AI with Composer for debugging a Flask application by capturing errors and applying suggested fixes.

In this lesson, you’ll learn how to leverage AI (via Composer) to debug a Flask application. We’ll capture runtime errors in the browser or terminal, feed them into Composer alongside the relevant code, and apply the suggested fixes—all while applying your own programmer intuition.

## 1. Reproducing & Resolving a Jinja2 Template Error

1. Start your Flask development server and navigate to the login page.
2. Log in with valid credentials.

<Frame>
  ![The image shows a login page for a "Task Manager" application with fields for username and password. The browser window is open alongside a code editor displaying project files.](https://kodekloud.com/kk-media/image/upload/v1752872690/notes-assets/images/Cursor-AI-Demo-Debugging-with-AI/task-manager-login-page-code-editor.jpg)
</Frame>

3. After logging in, you may encounter:

<Frame>
  ![The image shows a web browser displaying a Jinja2 "TemplateNotFound" error for "dash.html" with a traceback of the error. On the left, there's a file explorer showing project files in a code editor.](https://kodekloud.com/kk-media/image/upload/v1752872692/notes-assets/images/Cursor-AI-Demo-Debugging-with-AI/jinja2-templatenotfound-error-dash-html.jpg)
</Frame>

```plaintext theme={null}
jinja2.exceptions.TemplateNotFound: dash.html
127.0.0.1 - - [20/Mar/2025 21:37:51] "GET /dashboard HTTP/1.1" 500 -
```

### The Faulty Route

In **app.py**, the dashboard route is defined as:

```python theme={null}
@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    # ... build query ...
    return render_template('dash.html', tasks=tasks, users=users, statuses=statuses)
```

#### Feeding the Error and Code to Composer

```plaintext theme={null}
jinja2.exceptions.TemplateNotFound: dash.html
```

```python theme={null}
