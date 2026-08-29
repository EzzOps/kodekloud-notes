# function to calculate the sum of two integers
def add(a, b):
    return a + b  # return the sum of a and b

# function to calculate the difference of two integers
def subtract(a, b):
    return a - b  # return the difference of a and b
```

Example: Chat-generated, PEP 8-aligned implementation

```python theme={null}
def calculate_sum(a: int, b: int) -> int:
    """
    Calculate the sum of two integers.

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        int: Sum of the two numbers.
    """
    return a + b
```

If inline suggestions remain minimal even with an instruction file in place:

* Try the same prompt in Copilot Chat — it often respects repository-level guidance more fully.
* Make inline prompts slightly more explicit (add a short comment specifying style or types).

Resources:

* [Copilot Chat overview](https://docs.github.com/en/copilot/getting-started-with-github-copilot/about-github-copilot-chat)

## 3) Use the Completions panel to compare suggestions

The Completions panel displays multiple alternative implementations. Use it to compare different approaches (concise vs. documented, typed vs. untyped), then accept the variant that best matches your codebase.

Workflow:

1. Open the Completions panel in the Copilot UI.
2. Page through suggestions to review variations.
3. Accept the suggestion that fits style, performance, or readability goals — you can also edit the accepted suggestion afterward.

Example prompt: "Create square of a number"

One suggested completion:

```python theme={null}
def square_number(num: int) -> int:
    """
    Calculate the square of a number.

    Args:
        num (int): Number to find the square of.

    Returns:
        int: Square of the number.
    """
    return num * num
```

Comparing several of these helps you pick the best fit without losing context.

## 4) Keyboard shortcuts and keybindings

Speed up acceptance and navigation by learning or customizing a few keybindings. VS Code lets you view and remap Copilot-related shortcuts from the Keyboard Shortcuts panel.

Common actions you may want shortcuts for:

* Open Copilot Chat
* Toggle Copilot inline suggestions
* Open the Completions panel
* Accept the current suggestion
* Cycle through alternative suggestions

Open and customize shortcuts:

* In VS Code: File > Preferences > Keyboard Shortcuts (or press `Ctrl+K Ctrl+S` / `Cmd+K Cmd+S`)
* See Copilot command names in the Keyboard Shortcuts UI

<Frame>
  <img alt="A screenshot of Visual Studio Code's Keyboard Shortcuts panel filtered for &#x22;copilot,&#x22; showing a list of GitHub Copilot commands, keybindings, conditions and sources. The &#x22;Chat: Open Copilot Edits&#x22; entry is highlighted with a mouse cursor over a keybinding." />
</Frame>

Memorize or remap the few shortcuts you use most; this reduces context switching and speeds up acceptance.

## 5) Model selection and context windows

Model choice and the editor context you expose both affect suggestion quality:

* Inside Copilot Chat you can select different underlying models (e.g., GPT-4o or other code-optimized models). Test models on representative tasks and keep the one that balances accuracy, conciseness, and code quality for your workflows.
* Limit the number of open files/tabs to the modules relevant to the task. Copilot's context window is finite — opening too many unrelated files can dilute suggestion relevance.

<Callout icon="warning">
  Avoid opening too many files at once: Copilot has a limited context window. Close unrelated tabs to improve suggestion relevance for the code you're actively editing.
</Callout>

Practical tips:

* Focus on the directory or package you are editing (e.g., database layers and config when making DB changes).
* If suggestions degrade, close non-essential tabs and re-run generation.

## Next steps: comment-driven development and a sample project

With a repository-level instruction file and familiarity with Completions and Chat, you can scale from small edits to larger features using comment-driven development:

1. Start a small sample project (for example, a fake data generator).
2. Use inline comments to scaffold small functions and use Copilot to complete them.
3. Switch to Copilot Chat for larger tasks or when you want full docstrings and typed signatures.
4. Iterate: accept a suggestion, refactor, re-prompt with clearer constraints, and repeat.

Further reading and resources

* [GitHub Copilot documentation](https://docs.github.com/en/copilot)
* [Copilot Chat overview](https://docs.github.com/en/copilot/getting-started-with-github-copilot/about-github-copilot-chat)
* [Visual Studio Code keybindings](https://code.visualstudio.com/docs/getstarted/keybindings)

Apply these quick wins to make Copilot more consistent with your project's style and to speed up development cycles.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-copilot-in-action/module/192b5dd0-981d-43ef-80e9-b4189b3877af/lesson/54127571-05ca-48d7-bc66-269b94873930" />
</CardGroup>


# Configuring Copilot Visual Studio

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-in-Action/Introduction-to-GitHub-Copilot/Configuring-Copilot-Visual-Studio/page

Guide to installing and configuring GitHub Copilot and Copilot Chat in Visual Studio Code, including settings, workspace instructions, language tips, and an example Flask context.

I have [Visual Studio Code](https://code.visualstudio.com/) open with the project I'm about to work on. In this guide we'll install and configure [GitHub Copilot](https://github.com/features/copilot) so it can assist while you code.

## Install the extension

1. Open View → Extensions (or press `Ctrl+Shift+X` / `Cmd+Shift+X`).
2. Search for "GitHub" and locate **GitHub Copilot**.
3. Click **Install**. After installation the extension will prompt you to sign in to [GitHub](https://github.com/) via your browser if you haven't already authenticated.

If you already have GitHub authentication configured in VS Code (for example via the official "GitHub" extension), Copilot will reuse that and you can skip the browser login.

Example terminal prompt you may see while signing in:

```bash theme={null}
jeremy@Jeremys-Mac-Studio fakedatagenerator %
```

## About GitHub Copilot Chat

When you install GitHub Copilot, the "GitHub Copilot Chat" extension is often added alongside it. Open the Copilot Chat panel from the status area (lower-right). Unlike a standard web chat, Copilot Chat can read the files in your workspace to provide context-aware suggestions—this makes generated code, refactors, and explanations more relevant to the project you're editing.

<Callout icon="lightbulb">
  [GitHub Copilot Chat](https://docs.github.com/en/copilot/getting-started-with-github-copilot/about-github-copilot-chat) can read files in your workspace to provide context-aware suggestions and to help with code generation, refactors, and explanations.
</Callout>

You can enable or disable inline completions from the Copilot menu. Some developers prefer to disable completions while sketching ideas and re-enable them when ready for suggestions.

<Frame>
  <img alt="A screenshot of the GitHub Copilot menu in a dark-themed editor showing options like &#x22;Status: Ready,&#x22; &#x22;GitHub Copilot Chat,&#x22; and &#x22;Disable Completions.&#x22; A hand-shaped cursor is hovering over the &#x22;Disable Completions&#x22; option." />
</Frame>

## Settings overview

GitHub Copilot exposes several settings inside VS Code. Review these areas to tailor Copilot to your workflow:

| Area                        | Why it matters                                                                              | Example / Setting                                                                                                    |
| --------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Window profiles             | Choose which VS Code profile opens a new window (useful if you maintain multiple profiles). | Use the VS Code Profiles UI to switch contexts.                                                                      |
| Formatters                  | Default formatters may change how Copilot suggestions are applied.                          | Ensure your preferred formatter is selected in Settings.                                                             |
| Extensions & authentication | If you have the official GitHub extension with auth configured, Copilot will reuse it.      | No extra sign-in required when auth is present.                                                                      |
| Language enable/disable     | Enable Copilot per-language using pattern matching.                                         | Set patterns such as `\{ "*": true, "plaintext": false \}` or in Settings: `"{ \"*\": true, \"plaintext\": false }"` |

<Frame>
  <img alt="A screenshot of an editor's Settings panel showing GitHub Copilot configuration. It displays an &#x22;Enable Auto Completions&#x22; checkbox and a table listing languages with true/false values for Copilot completions." />
</Frame>

### Common Copilot settings examples

* Enable Copilot for all files except a few types:
  * In Settings JSON: `"{ \"*\": true, \"plaintext\": false, \"markdown\": false }"`
* Disable inline completions temporarily via the Copilot menu or Settings.

<Callout icon="warning">
  Experimental or preview features can add capabilities but may be unstable. Enable preview features only if you want to test new behavior and accept potential instability.
</Callout>

## Tips on language-specific settings

* YAML: Copilot often generates helpful YAML for CI/CD and configuration files, but it can also produce irrelevant suggestions. Toggle Copilot for YAML per project if it becomes noisy.
* Experimental features: Enable preview features selectively when you want to try new capabilities, but be aware they can change frequently.

## Workspace instructions via settings.json

You can provide project-specific instructions that Copilot Chat will consult during code generation. Add these to your workspace `settings.json` to encode style or domain-specific guidance:

```json theme={null}
{
  "github.copilot.chat.codeGeneration.instructions": [
    "Use underscore for field names.",
    "Use conventional commit message format."
  ]
}
```

This is useful to keep repository-wide conventions consistent when generating code with Copilot.

## Example code context (Flask)

Copilot is most useful when it can read and reason about your existing project files. Below is a small, corrected [Flask](https://flask.palletsprojects.com/) example that Copilot can use as context to suggest completions or new routes:

```python theme={null}
from flask import Flask, render_template, request, redirect
import uuid
import os

app = Flask(__name__)
app.debug = True if os.getenv("ENV") == "development" else False

todos = []

@app.route("/")
def home():
    return render_template("index.html", todos=todos)

@app.route("/create-todo", methods=["POST"])
def create_todo():
    new_todo = {
        "id": str(uuid.uuid4()),
        "title": request.form["title"],
        "completed": False,
    }
    todos.append(new_todo)
    return redirect("/")

@app.route("/update-todo/<id>", methods=["POST"])
def update_todo(id):
    for todo in todos:
        if todo["id"] == id:
            todo["completed"] = not todo["completed"]
            break
    return redirect("/")
```

Keep your code well-structured and properly documented—Copilot performs best when it has clear context from existing files.

## Next steps

Once Copilot and Copilot Chat are installed and configured:

* Try inline completions while editing real files to see contextual suggestions.
* Use the Copilot Chat pane to ask for code generation, explanations, or refactors—because the chat can read your workspace, answers are tailored to your codebase.
* Iterate on your workspace `settings.json` instructions to bake in repository conventions (naming, formatting, commit messages).

Try different workflows (completions on/off, chat prompts, project-specific instructions) to refine how Copilot supports your development process.

## Links and references

* [Visual Studio Code](https://code.visualstudio.com/)
* [GitHub Copilot](https://github.com/features/copilot)
* [GitHub Copilot Chat documentation](https://docs.github.com/en/copilot/getting-started-with-github-copilot/about-github-copilot-chat)
* [Flask documentation](https://flask.palletsprojects.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-copilot-in-action/module/fb848134-d908-42a6-b195-1ea9c9cd1ffe/lesson/14b41d10-1b43-4808-bc07-82a9cfdfc6d9" />
</CardGroup>
