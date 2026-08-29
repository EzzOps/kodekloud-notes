# Production: replace with a secure random key
app.config["SECRET_KEY"] = "dev"
app.config["DATABASE"] = os.path.join(app.instance_path, "task_manager.sqlite")
```

You can reference external guides:

* [Flask Documentation](https://flask.palletsprojects.com/)
* [Python CSV Module](https://docs.python.org/3/library/csv.html)

## Generating Documentation with AI Agents

Leverage AI to scan code and generate or enhance PEP 8-style docstrings automatically.

### Example: `app.py`

```python theme={null}
import csv
import sqlite3
import os
from flask import Flask, g

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"  # Change for production
app.config["DATABASE"] = os.path.join(app.instance_path, "task_manager.sqlite")

def read_csv(file_path):
    with open(file_path, "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            print(row)

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)
```

**AI-Enhanced Version** (agent prompt: “Create PEP 8 documentation for this file”):

```python theme={null}
def read_csv(file_path):
    """
    Read data from a CSV file and print each row.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        None

    Example:
        >>> read_csv("data.csv")
        ['header1', 'header2']
        ['value1', 'value2']
    """
    with open(file_path, "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            print(row)
```

## Using Cursor AI Rules to Enforce Documentation Standards

Define a `documentation_standards.mdc` to guide every AI invocation:

```text theme={null}
# documentation_standards.mdc
# - Use clear, concise language.
# - Document all parameters and return values.
# - Include usage examples for non-trivial functions.
# - Follow PEP 8 formatting: docstring quotes, indentation, line length.
# - Highlight edge cases and error handling in examples.
```

```python theme={null}
# Apply standards to read_csv
import csv

def read_csv(file_path):
    """
    Read data from a CSV file and print each row.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        None

    Example:
        >>> read_csv("data.csv")
        ['header1', 'header2']
        ['value1', 'value2']
    """
    with open(file_path, "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            ...
```

![The image shows a code editor with a split view. The left side displays a file directory, and the right side shows code and documentation guidelines for a Python project.](https://kodekloud.com/kk-media/image/upload/v1752872793/notes-assets/images/Cursor-AI-Demo-Documentation-Management/code-editor-split-view-python.jpg)

When you run the agent against a test file (e.g., `test_app.py`), it will produce a PEP 8-compliant suite:

```python theme={null}
# Write the content to the rule file
with open(rule_file_path, "w") as file:
    file.write(rule_content)

import os
import tempfile
import pytest

def test_read_csv(tmp_path):
    """
    Test read_csv with a temporary CSV file.
    """
    data = tmp_path / "test.csv"
    data.write_text("a,b\n1,2\n")
    read_csv(str(data))
    # assertions here...
```

![The image shows a code editor with a Python script open, displaying documentation standards and test functions. The left sidebar lists project files, and the right side shows detailed comments and guidelines for generating documentation.](https://kodekloud.com/kk-media/image/upload/v1752872794/notes-assets/images/Cursor-AI-Demo-Documentation-Management/python-script-documentation-editor.jpg)

## Best Practices for AI-Friendly Documentation

* Keep prompts concise and focused on one file or function.
* Group related rules and examples together in your standards file.
* Include representative code snippets in your rule set.
* Iterate on the rule file to refine style and edge-case coverage.
* Review and edit generated docs for correctness and clarity.

## Links and References

* [PEP 8 – Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
* [Flask Documentation](https://flask.palletsprojects.com/)
* [Cursor AI](https://cursor.so/)

By combining inline docstrings, external references, AI-generated content, and a robust rule set, you’ll ensure your Python code remains well-documented, consistent, and up to date.

- [Watch Video](https://learn.kodekloud.com/user/courses/cursor-ai/module/fcc10c1c-5240-4626-9bfc-bf172a3a00c6/lesson/c0e52af1-e24f-4d5d-bd9c-79d9dd6c9a61)


# Demo Privacy

Source: https://notes.kodekloud.com/docs/Cursor-AI/Understanding-and-Customizing-Cursor/Demo-Privacy/page

Learn to secure your development workflow with Cursor AI’s Privacy Mode, data handling guarantees, and custom security rules.

Secure your development workflow with Cursor AI’s Privacy Mode, data handling guarantees, and custom security rules. In this guide, you’ll learn how to:

* Configure and compare Privacy Mode settings
* Understand Cursor’s privacy policy and data flow
* Enable semantic codebase indexing securely
* Define and apply custom security rules

## Privacy Mode Overview

Cursor AI offers a **Privacy Mode** setting that controls whether your code and prompts are stored or discarded. By default, Cursor sends an `X-Ghost-Mode` header on every request to keep your usage anonymous.

| Privacy Mode | Behavior                        | Data Retention     |
| ------------ | ------------------------------- | ------------------ |
| Enabled      | No storage of prompts or code   | Zero retention     |
| Disabled     | Prompts and telemetry collected | Used to improve AI |

> **triangle-alert** If you’re working with sensitive, proprietary, or regulated code, **always enable Privacy Mode** to prevent any data persistence.

![The image shows a code editor interface with a sidebar of files and a settings panel open, displaying options for VS Code import, appearance, and privacy mode. A terminal is visible at the bottom with a command prompt.](https://kodekloud.com/kk-media/image/upload/v1752872795/notes-assets/images/Cursor-AI-Demo-Privacy/code-editor-vs-code-settings-terminal.jpg)

## Privacy Policy Details

Cursor’s official [Privacy Policy](https://cursor.com/privacy) outlines strict rules when Privacy Mode is on:

* TLDR: **Zero data retention** of your code, prompts, or interactions
* Other notes: No third-party sharing or AI training on your private code

When Privacy Mode is off, Cursor collects:

* Prompts and code snippets
* Editor actions and code edits
* Inference-provider telemetry to speed up responses

![The image shows a webpage from Cursor's privacy policy section, detailing information about "Privacy Mode" and data handling practices. It includes sections labeled "TLDR" and "Other notes" with bullet points explaining data retention and processing.](https://kodekloud.com/kk-media/image/upload/v1752872796/notes-assets/images/Cursor-AI-Demo-Privacy/cursor-privacy-policy-privacy-mode.jpg)

### Additional Policy Notes

* All requests, even with your own API key, route through Cursor’s backend for prompt assembly.
* Cursor crafts final prompts and context before reaching [OpenAI’s API](https://platform.openai.com/docs/api-reference).
* If you index your codebase, Cursor uploads snippets temporarily to compute embeddings, then discards plaintext.

![The image shows a webpage displaying the privacy policy of a website called Cursor, with sections explaining data retention and privacy mode settings.](https://kodekloud.com/kk-media/image/upload/v1752872797/notes-assets/images/Cursor-AI-Demo-Privacy/cursor-privacy-policy-webpage.jpg)

> **lightbulb** Embeddings and metadata may be cached briefly to optimize search performance but are not stored long-term in plaintext.

![The image shows a webpage from Cursor's security section, specifically detailing their "Privacy Mode Guarantee." The page includes a sidebar with various security-related topics and a main section explaining how privacy mode works and its importance.](https://kodekloud.com/kk-media/image/upload/v1752872798/notes-assets/images/Cursor-AI-Demo-Privacy/cursor-privacy-mode-guarantee.jpg)

## Codebase Indexing

Cursor supports **semantic indexing** of your repositories. By default, files in `.gitignore` or `cursor.ignore` are omitted. Indexing works as follows:

1. **Secure Chunk Upload**: Code is uploaded in encrypted chunks for embedding computation.
2. **Embedding Generation**: Uses Merkle tree structures and Turbopuffer for integrity.
3. **Ephemeral Storage**: Plaintext is discarded immediately; only embeddings & metadata remain temporarily.

For full details, see the [Cursor Security Documentation](https://cursor.com/security).

![The image shows a webpage from Cursor's security section, detailing their codebase indexing feature. It explains how the feature works, including the use of a Merkle tree and Turbopuffer for secure code indexing and retrieval.](https://kodekloud.com/kk-media/image/upload/v1752872800/notes-assets/images/Cursor-AI-Demo-Privacy/cursor-security-codebase-indexing.jpg)

## Custom Security Rules

Guide Cursor’s AI to generate secure code by defining custom rules.

1. Create `security-best-practices.md` in your Cursor rules folder:
   ```markdown theme={null}
   # Security Best Practices
   Applies to: JavaScript, TypeScript, JSX, TSX, Python, Ruby

   - Never use `eval` or similar dynamic execution methods.
   - Sanitize all user inputs before processing.
   - Use parameterized queries for database access.
   - Employ secure, up-to-date encryption algorithms.
   - Do not hardcode credentials or secrets.
   - Validate and encode outputs to prevent injection attacks.
   ```

![The image shows a code editor with a document titled "Security Best Practices," listing guidelines for secure coding, authentication, and API endpoints. The editor sidebar displays a file directory with various text and Python files.](https://kodekloud.com/kk-media/image/upload/v1752872801/notes-assets/images/Cursor-AI-Demo-Privacy/security-best-practices-code-editor.jpg)

2. For framework-specific rules, add files like `react-security.md`:
   ```markdown theme={null}
   # React Security Rules
   Applies to: React (JSX, TSX)

   - Avoid `dangerouslySetInnerHTML` without sanitation.
   - Leverage React’s built-in XSS protections.
   - Validate component props to enforce data integrity.
   ```

![The image shows a code editor with a file open titled "react-security.mdc," containing a list of React security rules and best practices. The sidebar displays a directory structure with various files and folders.](https://kodekloud.com/kk-media/image/upload/v1752872802/notes-assets/images/Cursor-AI-Demo-Privacy/react-security-rules-code-editor.jpg)

These rule sets ensure Cursor’s code suggestions adhere to your organization’s security standards.

## Conclusion

Enabling Privacy Mode and configuring custom security rules in Cursor AI protects your code and enhances compliance—at no extra cost. Whether you’re prototyping or working in a high-security environment, these features keep your data private and your workflows seamless.

## Links and References

* [Cursor Privacy Policy](https://cursor.com/privacy)
* [Cursor Security Documentation](https://cursor.com/security)
* [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

- [Watch Video](https://learn.kodekloud.com/user/courses/cursor-ai/module/fcc10c1c-5240-4626-9bfc-bf172a3a00c6/lesson/e40ccb9d-d7e4-4821-bca6-d6d3556a203e)
