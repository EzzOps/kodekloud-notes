# Output:
# Hello, World!
```

Copilot handles the boilerplate so you can jump straight to running your code.

***

## 3. Factorial Function

### 3.1 Complete from the Signature

Type the function signature, and Copilot will fill in the implementation:

```python theme={null}
def factorial(n: int) -> int:
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
```

### 3.2 Guide with a Docstring

Alternatively, add a descriptive docstring to guide Copilot:

```python theme={null}
def factorial(n: int) -> int:
    """Return the factorial of a non-negative integer."""
```

Copilot may then suggest:

```python theme={null}
def factorial(n: int) -> int:
    """Return the factorial of a non-negative integer."""
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

You can invoke it from `main()` or any other part of your script.

***

## 4. List Comprehension Example

Imagine you have a list of user dictionaries:

```python theme={null}
users = [
    {"name": "Michael", "id": 1},
    {"name": "Sanjeev",  "id": 2},
    {"name": "Jeremy",   "id": 3}
]
```

Start typing:

```python theme={null}
usernames = 
```

Copilot suggests:

```python theme={null}
usernames = [user["name"] for user in users]
```

Print them with:

```python theme={null}
for username in usernames:
    print(username)
```

Run to see the output:

```bash theme={null}
python3 main.py
# Michael
# Sanjeev
# Jeremy
```

***

## 5. File I/O with Exception Handling

When working with file operations, Copilot can quickly generate a `try/except` block.

```python theme={null}
try:
    with open("data.txt", "r") as f:
        data = f.read()
except FileNotFoundError:
    data = "No data available"

print(data)
```

If **data.txt** is missing:

```bash theme={null}
python3 main.py
# No data available
```

<Callout icon="lightbulb">
  For very large files, consider reading in chunks or using `file.readline()` to avoid high memory usage.
</Callout>

To catch all exceptions and log error details:

```python theme={null}
try:
    with open("data.txt", "r") as f:
        data = f.read()
except Exception as e:
    print(f"Error reading file: {e}")
    data = "default data"

print(data)
```

***

## 6. HTTP Requests with the `requests` Library

### 6.1 Installing and Importing

Type and let Copilot complete:

```python theme={null}
import requests
```

If you haven’t installed it yet:

```bash theme={null}
pip install requests
```

### 6.2 Making a GET Request

Copilot suggests the typical pattern:

```python theme={null}
response = requests.get("https://api.github.com")
print(response.status_code)
```

### 6.3 Handling Request Errors

Use Copilot to scaffold robust error handling:

```python theme={null}
try:
    response = requests.get("https://api.github.com")
    response.raise_for_status()
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

<Callout icon="triangle-alert">
  Always validate or sanitize external data returned from HTTP calls to prevent security issues.
</Callout>

***

## Conclusion & Key Takeaways

GitHub Copilot streamlines your Python development by:

* Automating boilerplate code
* Reducing syntax errors and runtime bugs
* Suggesting idiomatic patterns (comprehensions, recursion, error handling)
* Assisting with package installation and debugging

| Task                    | Copilot Prompt Example              | Benefit                   |
| ----------------------- | ----------------------------------- | ------------------------- |
| Hello, World!           | Type `def main():`                  | Instant program scaffold  |
| Recursive algorithms    | Add `def factorial(n: int) -> int:` | Correct recursive logic   |
| List comprehensions     | Start `usernames = [`               | Compact data extraction   |
| File I/O error handling | Begin `try:`                        | Robust file operations    |
| HTTP requests & errors  | Type `import requests`              | Reliable API interactions |

Master these patterns to focus on solving complex problems instead of writing repetitive code.

***

## Links and References

* [GitHub Copilot](https://github.com/features/copilot)
* [Python Official Website](https://www.python.org/)
* [requests Library Documentation](https://docs.python-requests.org/en/latest/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-copilot-certification/module/b02a5227-ee17-43dc-b006-51fef8272f13/lesson/73b6deac-6b87-4d73-9321-85cf364cb833" />
</CardGroup>


# Demo Setup and Configuring Copilot

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-Certification/Introduction/Demo-Setup-and-Configuring-Copilot/page

Learn to integrate GitHub Copilot into Visual Studio Code, customize settings, and use Copilot Chat for enhanced coding assistance.

In this guide, you’ll learn how to integrate GitHub Copilot into Visual Studio Code, customize its behavior, and leverage Copilot Chat for conversational code assistance. We’ll cover:

1. Installing the Copilot extension
2. Trying a simple Flask example
3. Configuring Copilot settings
4. Exploring Copilot Chat
5. Using contextual prompts
6. Adding workspace-specific instructions

***

## 1. Install the GitHub Copilot Extension

1. Launch [Visual Studio Code](https://code.visualstudio.com/) and open the **Extensions** view (`Ctrl+Shift+X`).
2. Search for **GitHub Copilot**.
3. Click **Install**.
4. Authenticate with your GitHub account when prompted.

<Callout icon="triangle-alert">
  You must have a valid Copilot subscription or trial to authenticate. Visit [GitHub Copilot Pricing](https://github.com/features/copilot#pricing) for more details.
</Callout>

<Frame>
  ![The image shows the GitHub Copilot extension page in Visual Studio Code, highlighting its features and installation details. The interface includes a sidebar with other extensions and a terminal at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752876847/notes-assets/images/GitHub-Copilot-Certification-Demo-Setup-and-Configuring-Copilot/github-copilot-vscode-extension.jpg)
</Frame>

***

## 2. Try a Simple Flask Example

After installation, Copilot will suggest code completions inline. Here’s a minimal Flask app with an in-memory database and a POST endpoint:

```python theme={null}
from flask import Flask, request, jsonify
from models import Item

app = Flask(__name__)
items_db = []
current_id = 1

@app.route('/items', methods=['POST'])
def create_item():
    global current_id
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400

    new_item = Item(
        id=current_id,
        name=data['name'],
        description=data.get('description', '')
    )
    items_db.append(new_item)
    current_id += 1

    return jsonify(new_item.to_dict()), 201
```

Place your cursor inside the function and start typing to see Copilot’s suggestions.

<Callout icon="lightbulb">
  Ensure you have Flask installed:

  ```bash theme={null}
  pip install flask
  ```
</Callout>

***

## 3. Configure Copilot Settings

VS Code lets you enable or disable Copilot features globally or per language. Open **Settings** (`Ctrl+,`) and search for “Copilot.” Key options include:

| Setting                             | Description                                 | Default     |
| ----------------------------------- | ------------------------------------------- | ----------- |
| Inline Completions                  | Show suggestions as you type                | Enabled     |
| Model Selection                     | Select a specific Copilot model             | `default`   |
| Language-Specific Activation        | Toggle Copilot for individual languages     | All enabled |
| Automatic Test-Failure Fixes (Chat) | Auto-correct failing tests via Copilot Chat | Disabled    |

You can also edit `settings.json` directly:

```json theme={null}
{
  "github.copilot.enable": true,
  "github.copilot.inlineSuggest.enable": true,
  "github.copilot.model": "gpt-4",
  "github.copilot.languages": {
    "markdown": false
  }
}
```

<Frame>
  ![The image shows a Visual Studio Code interface with the GitHub Copilot extension settings open, displaying options for enabling auto completions and configuring language-specific settings. The terminal at the bottom shows a command prompt.](https://kodekloud.com/kk-media/image/upload/v1752876847/notes-assets/images/GitHub-Copilot-Certification-Demo-Setup-and-Configuring-Copilot/vscode-github-copilot-settings-interface.jpg)
</Frame>

***

## 4. Explore GitHub Copilot Chat

Copilot Chat provides an interactive panel for code explanations, refactoring, and test generation.

* Click the **Copilot Chat** icon in the sidebar or status bar.
* Ask questions like “Explain this function” or “Generate unit tests.”

<Frame>
  ![The image shows a settings interface for GitHub Copilot, displaying various options and features related to code actions, renaming suggestions, and code generation.](https://kodekloud.com/kk-media/image/upload/v1752876848/notes-assets/images/GitHub-Copilot-Certification-Demo-Setup-and-Configuring-Copilot/github-copilot-settings-interface.jpg)
</Frame>

### Chat Configuration

Within the **Copilot Chat** settings, you can:

* Enable automatic test-failure fixes
* Suggest follow-up messages
* Override locale (`en`, `fr`, etc.)
* Define the default chat panel location
* Include or exclude enterprise repositories

<Frame>
  ![The image shows a settings interface for GitHub Copilot Chat, displaying various experimental features related to edits, tests, and language context.](https://kodekloud.com/kk-media/image/upload/v1752876849/notes-assets/images/GitHub-Copilot-Certification-Demo-Setup-and-Configuring-Copilot/github-copilot-chat-settings-interface.jpg)
</Frame>

***

## 5. Use Context with Copilot Chat

1. Open any file (e.g., `app.py`).
2. Select or add code snippets.
3. Launch Copilot Chat and ask targeted questions:

```python theme={null}
@app.route('/items', methods=['GET'])
def list_items():
    return jsonify([item.to_dict() for item in items_db]), 200
```

Copilot Chat will include the current file name and selection context for more accurate responses.

***

## 6. Add Custom Instructions

To guide Copilot across your repository, create a custom instructions file:

```bash theme={null}
mkdir -p .github/copilot
touch .github/copilot/instructions.md
```

Populate `.github/copilot/instructions.md` with workspace-specific guidelines:

```markdown theme={null}
