# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['DATABASE'] = os.path.join(app.instance_path, 'task_manager.sqlite')

# Ensure instance folder exists and write to CSV
try:
    os.makedirs(app.instance_path)
    with open('file.csv', 'w') as f:
        f.write('Hello, World!')
    with open('file.csv', 'r') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            print(row)
except OSError:
    pass
```

Because `csv` is not imported, `csv.reader` will trigger a quick fix. Press `⌘.` (macOS) or `Ctrl+.` (Windows/Linux), choose **Import 'csv'**, and Cursor auto-inserts:

```python theme={null}
import csv
import sqlite3
import os
# ...other imports
```

Your application runs without `ModuleNotFoundError`.

> **lightbulb** Use the auto-import feature to speed up development and avoid manual import typos.

## Quick Fix Menu

Beyond imports, the Quick Fix menu helps with:

* Renaming symbols
* Searching for import candidates
* Suppressing linter warnings

Navigate to suggested actions with `Ctrl+.` / `⌘.`.

## Python Auto Import (Beta)

The Python auto-import (Beta) proactively adds necessary imports as you type. Example:

```python theme={null}
def read_csv(file_path):
    with open(file_path, 'r') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            print(row)

def write_csv(file_path, data):
    with open(file_path, 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows(data)
```

Press **Tab** inside the function, save the file, and watch `import csv` appear at the top.

## Customizing Settings in Cursor

Access global settings with `⌘⇧J` (macOS) or `Ctrl+Shift+J` (Windows/Linux). Here you can adjust AI rules, feature toggles, editor themes, and more.

### Importing VS Code Settings

Mirror your [VS Code](https://code.visualstudio.com) preferences by importing your settings and extensions into Cursor.

![The image shows a dark-themed code editor interface with a file explorer on the left and a settings panel on the right, where a confirmation dialog is open for importing VS Code settings.](https://kodekloud.com/kk-media/image/upload/v1752872746/notes-assets/images/Cursor-AI-Demo-Auto-Imports-and-Customizing-Settings/dark-code-editor-vs-code-settings.jpg)

After import, extensions like [TabNine](https://www.tabnine.com) and your preferred theme sync automatically.

```text theme={null}
[2025-03-19 21:44:41.900] Extension version: 0.88.5
[2025-03-19 21:44:41.901] LLM bundle: none
[2025-03-19 21:44:41.901] WSL extension is supported only in Microsoft versions of VS Code
```

### Project-Specific Cursor Rules

Define a `.cursor-rules` file at your project root to override global AI instructions. These per-project settings ensure consistent code style.

![The image shows a code editor interface with a file directory on the left and a "Cursor Settings" panel on the right, displaying rules for AI and project settings. The terminal at the bottom shows a command prompt.](https://kodekloud.com/kk-media/image/upload/v1752872747/notes-assets/images/Cursor-AI-Demo-Auto-Imports-and-Customizing-Settings/code-editor-cursor-settings-terminal.jpg)

Example `.cursor-rules`:

```txt theme={null}
# .cursor-rules
always generate Python code that is simple and PEP 8 compliant
```

### Feature Toggles

Enable or disable Cursor IDE features according to your workflow:

| Feature                          | Description                            |
| -------------------------------- | -------------------------------------- |
| Cursor predictions               | Real-time code suggestions             |
| Auto import for Python (Beta)    | Automatic import insertion as you code |
| Partial accepts                  | Accept suggestions in segments         |
| Show whitespace-only suggestions | Display whitespace completions         |

![The image shows a code editor interface with a file directory on the left and "Cursor Settings" options in the center. The terminal is visible at the bottom, and a chat panel is on the right.](https://kodekloud.com/kk-media/image/upload/v1752872749/notes-assets/images/Cursor-AI-Demo-Auto-Imports-and-Customizing-Settings/code-editor-cursor-settings-interface.jpg)

![The image shows a code editor interface with a "Cursor Settings" menu open, displaying options for features and a disclaimer about "Yolo mode." A file directory is visible on the left side.](https://kodekloud.com/kk-media/image/upload/v1752872750/notes-assets/images/Cursor-AI-Demo-Auto-Imports-and-Customizing-Settings/code-editor-cursor-settings-yolo.jpg)

> **triangle-alert** Keep your API keys secure. Do not commit them to public repositories.

## AI Models and API Keys

Under **Models**, select your preferred AI backend. To unlock premium capabilities, add API keys for:

* OpenAI
* Anthropic
* Google Cloud AI
* Azure AI

![The image shows a code editor interface with a file directory on the left and a "Cursor Settings" panel on the right, displaying a list of model names. The terminal is visible at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752872751/notes-assets/images/Cursor-AI-Demo-Auto-Imports-and-Customizing-Settings/code-editor-cursor-settings-terminal-2.jpg)

![The image shows a code editor interface with a file directory on the left and a "Cursor Settings" panel on the right, displaying options for entering various API keys.](https://kodekloud.com/kk-media/image/upload/v1752872752/notes-assets/images/Cursor-AI-Demo-Auto-Imports-and-Customizing-Settings/code-editor-cursor-settings-api-keys.jpg)

## Beta Features

Join the cutting edge by toggling beta features for early access to new AI capabilities.

![The image shows a code editor interface with a file directory on the left and "Cursor Settings" options in the center. The terminal is visible at the bottom, displaying a command prompt.](https://kodekloud.com/kk-media/image/upload/v1752872754/notes-assets/images/Cursor-AI-Demo-Auto-Imports-and-Customizing-Settings/code-editor-cursor-settings-terminal-3.jpg)

## Next Steps

Now that you’ve configured Cursor’s auto-imports and personalized your IDE, proceed to explore advanced prompt engineering and delve deeper into Cursor’s AI-driven development workflow.

## Links and References

* [Cursor IDE Documentation](https://cursor.so/docs/)
* [VS Code Official Site](https://code.visualstudio.com)
* [TabNine AI Autocomplete](https://www.tabnine.com)

- [Watch Video](https://learn.kodekloud.com/user/courses/cursor-ai/module/e11e1c1e-9b6b-4c53-b14a-24babbd114a5/lesson/77c1697f-a322-4c85-a18b-971df1a08c16)


# Demo Cursor Ask Mode

Source: https://notes.kodekloud.com/docs/Cursor-AI/Mastering-Autocompletion/Demo-Cursor-Ask-Mode/page

This article explains Composers chat pane modes for streamlining development workflows, including generating code, adding context, and inline editing.

During this lesson, you’ll notice Composer’s chat pane now offers three modes—Agent, Cursor Ask, and Edit—accessible via Command-L on Mac or Control-L on Windows/Linux. Although the labels have changed, all previous functionality remains intact. Let’s explore each mode and see how they streamline your development workflow.

## Opening the Chat and Selecting Models

Press Command-L (Mac) or Control-L (Windows/Linux) to open the Composer chat pane. You’ll find three tabs:

* Agent mode
* Cursor Ask mode
* Edit mode

In the model dropdown, choose **Auto-select** to let Composer pick the optimal model, or manually select one (for example, **Cloud 3.7**):

![The image shows a software interface with a dropdown menu for selecting AI models, including options like "Auto-select" and various model names. A tooltip explains that the cursor helps select the best model based on availability and performance.](https://kodekloud.com/kk-media/image/upload/v1752872755/notes-assets/images/Cursor-AI-Demo-Cursor-Ask-Mode/ai-model-selection-interface-dropdown.jpg)

## Adding Files as Context

Composer can reference files or entire folders when generating or editing code. To upload files:

1. In the **Files & Folders** panel, right-click and select **Add context**.
2. Choose your file (e.g., `test.py` or `grades.csv`).

![The image shows a dark-themed interface with a context menu open, displaying options like "test.py" and "mockdata.csv" under "Add context." A cursor is hovering over "test.py."](https://kodekloud.com/kk-media/image/upload/v1752872756/notes-assets/images/Cursor-AI-Demo-Cursor-Ask-Mode/dark-interface-context-menu-test-py.jpg)

Now Composer will include these files in its context for more accurate suggestions.

***

## Example: Generating a `grades.py` Script

Suppose you have a CSV file named `grades.csv`:

```csv theme={null}
student,math,science,history
Alice,85,90,88
Bob,78,75,80
Charlie,92,88,91
David,75,80,78
Eve,88,85,90
Frank,70,72,75
Grace,84,87,89
Helen,76,79,82
```

1. In **Files & Folders**, search for `grades.csv` and add it as context.
2. Switch to **Cursor Ask mode** and enter:

   > Write a Python function to parse `grades.csv` containing student grades and calculate the average score for each student, using [Pandas](https://pandas.pydata.org). Apply it to `grades.py`.

Composer will detect that `grades.py` is empty and suggest code. Click **Apply to grades.py**:

![The image shows a dark-themed code editor with a file selection dropdown, highlighting a file named "test.py" among other files like "grades.csv" and "matrix.py". A chat window on the right contains a prompt about processing student grades.](https://kodekloud.com/kk-media/image/upload/v1752872757/notes-assets/images/Cursor-AI-Demo-Cursor-Ask-Mode/dark-code-editor-file-selection.jpg)

Composer inserts the following into `grades.py`:

```python theme={null}
import pandas as pd

def calculate_student_averages(file_path: str) -> pd.DataFrame:
    """
    Parse a CSV file containing student grades and calculate the average score for each student.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pandas.DataFrame: DataFrame with student names and their average scores.
    """
    df = pd.read_csv(file_path)
    df['average'] = df.iloc[:, 1:].mean(axis=1)
    return df[['student', 'average']]

if __name__ == "__main__":
    result = calculate_student_averages('grades.csv')
    print(result)
```

> **lightbulb** Before running the script, install Pandas:

  ```bash theme={null}
  pip install pandas
  ```

Run the script:

```bash theme={null}
python grades.py
```

You’ll see each student’s average score printed to the console.

***

## Zero-Shot Prompts

You’re not limited to files in context. In a new chat, ask for any snippet:

> Create a function to fetch current weather data from the [OpenWeatherMap API](https://openweathermap.org/api) for a given city.

Composer returns:

```python theme={null}
import requests

def get_weather_data(city: str, api_key: str) -> dict:
    """
    Fetch current weather data from OpenWeatherMap API for a given city.

    Args:
        city (str): Name of the city.
        api_key (str): Your OpenWeatherMap API key.

    Returns:
        dict: Weather data if successful, None otherwise.
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
```

You can then apply this snippet directly into any open file.

***

## Inline Edits with Edit Mode

In **Edit mode**, select existing code, press Control-K, and provide instructions. For example, highlight `calculate_student_averages` and say:

> Optimize this function for performance.

Or:

> Add a timing decorator to measure execution time.

Composer refactors inline, generating:

```python theme={null}
import time
from functools import wraps
import pandas as pd

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def calculate_student_averages(file_path: str) -> pd.DataFrame:
    """Parse a CSV file containing student grades and calculate the average score."""
    df = pd.read_csv(file_path)
    df['average'] = df.iloc[:, 1:].mean(axis=1)
    return df[['student', 'average']]
```

Run `python grades.py` again to see timing information alongside the results.

***

## Summary

Composer’s three modes enable you to:

| Mode       | Function                                         | Shortcut                |
| ---------- | ------------------------------------------------ | ----------------------- |
| Agent mode | Orchestrate multi-step workflows                 | Command-L / Ctrl-L      |
| Cursor Ask | Generate new files or code based on context      | Command-L / Ctrl-L      |
| Edit mode  | Inline AI-assisted refactoring and documentation | Select code + Control-K |

Composer brings AI-driven development directly into your editor, allowing you to generate, refactor, and optimize code with minimal context switching.

***

## Links and References

* [Composer Documentation](https://aka.ms/composer/docs)
* [Pandas Official Site](https://pandas.pydata.org/)
* [OpenWeatherMap API](https://openweathermap.org/api)

- [Watch Video](https://learn.kodekloud.com/user/courses/cursor-ai/module/e11e1c1e-9b6b-4c53-b14a-24babbd114a5/lesson/b0b6c4ae-3dc0-45d1-9c38-ed25aa72e5d6)
