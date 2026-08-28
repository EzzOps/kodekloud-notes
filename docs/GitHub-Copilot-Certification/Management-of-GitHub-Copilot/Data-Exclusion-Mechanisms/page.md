# Purpose
This document guides GitHub Copilot to produce Python code that strictly follows PEP 8 standards for readability and maintainability.

## General Guidelines
- Adhere to PEP 8: https://peps.python.org/pep-0008/  
- Use four spaces per indentation level.  
- Limit lines to 79 characters.  
- Include docstrings for all modules, classes, and functions.

## Naming Conventions
- snake_case for variables, functions, and methods  
- PascalCase for class names  
- ALL_CAPS for constants

## Imports
1. Place imports at the top.  
2. Order: standard → third-party → local.  
3. One import per line.  
4. Avoid wildcard imports.
```

<Frame>
  ![The image shows a code editor with a markdown file open, containing instructions for GitHub Copilot to follow PEP8 Python coding standards. The text includes guidelines on indentation, line length, naming conventions, and import statements.](https://kodekloud.com/kk-media/image/upload/v1752876857/notes-assets/images/GitHub-Copilot-Certification-Quick-Wins-for-Immediate-Productivity-Gains/code-editor-markdown-github-copilot-pep8.jpg)
</Frame>

With these guidelines, Copilot will generate clean, compliant code:

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

<Callout icon="lightbulb">
  Well-defined instructions ensure consistent, high-quality suggestions across your team.
</Callout>

***

## 2. Testing in `main.py`

Validate that Copilot respects your file-based configuration:

```python theme={null}
# create a function to calculate the square of a number
```

Trigger Copilot and you may see:

```python theme={null}
def square_number(num: int) -> int:
    """
    Calculate the square of a number.

    Args:
        num (int): Number to square.

    Returns:
        int: Square of the input number.
    """
    return num * num
```

<Callout icon="triangle-alert">
  If the generated code doesn’t match your standards, retry or use Copilot Chat for better fidelity.
</Callout>

***

## 3. Using the Completions Panel

The Completions Panel lets you review multiple suggestions side-by-side:

1. Open with the Copilot icon or run **GitHub Copilot: Open Completions Panel**.
2. Enter your prompt, e.g.:
   ```python theme={null}
   # create a function to calculate the square of a number
   ```
3. Compare suggestions and pick the one that aligns with your style.

***

## 4. Keyboard Shortcuts

Master these keybindings to speed up your workflow:

<Frame>
  ![The image shows a list of keyboard shortcuts for GitHub Copilot in a code editor, with commands, keybindings, and conditions for their use. A cursor is pointing at one of the keybindings.](https://kodekloud.com/kk-media/image/upload/v1752876859/notes-assets/images/GitHub-Copilot-Certification-Quick-Wins-for-Immediate-Productivity-Gains/github-copilot-keyboard-shortcuts.jpg)
</Frame>

| Command                     | Keybinding | Condition                                             |
| --------------------------- | ---------- | ----------------------------------------------------- |
| Chat: Open Copilot Edits    | —          | chatEditingParticipantRegistered && chatIsEnabled     |
| Accept panel suggestion     | ⌥\\        | github.copilot.acceptCursorPanelSolution              |
| Next panel suggestion       | ⌥\\        | github.copilot.nextPanelSolution                      |
| Previous panel suggestion   | ⌥\[        | github.copilot.previousPanelSolution                  |
| Open Completions Panel      | —          | github.copilot.generate                               |
| Start Inline Chat in Editor | Enter      | editorTextFocus && github.copilot.chat.editor.enabled |
| Trigger Inline Suggestion   | ⌥\\        | editorFocus && github.copilot.chat.editor.enabled     |

(On Windows/Linux, replace ⌥ with Alt.)

***

## 5. Switching AI Models

Different Copilot models excel at different tasks. Click the model selector in the lower-right corner to choose:

| Model      | Strength                           | Ideal Use Case                        |
| ---------- | ---------------------------------- | ------------------------------------- |
| Claude 3.5 | Deep contextual reasoning          | Summaries, refactoring                |
| Sonnet     | Fast, lightweight completions      | Short snippets, boilerplate code      |
| GPT-4      | Broad language understanding       | Complex logic, detailed explanations  |
| O1 Preview | Optimized for multi-step workflows | Step-by-step guides, automation flows |

For more details, see the [GitHub Copilot Models](https://docs.github.com/copilot).

***

## 6. Managing Context Windows

Copilot’s suggestions depend on the active context. Keep only your current files open to maintain focused and relevant completions.

<Callout icon="lightbulb">
  Closing inactive tabs prevents context dilution and improves suggestion accuracy.
</Callout>

***

In this lesson, we covered:

* Defining file-based instructions
* Verifying behavior in `main.py`
* Leveraging the Completions Panel
* Memorizing keyboard shortcuts
* Selecting the optimal AI model
* Managing editor context

Next up: **Comment-Driven Development** and building a **Fake Data Generator**.

## Links and References

* [GitHub Copilot Documentation](https://docs.github.com/copilot)
* [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
* [GitHub Copilot Models](https://docs.github.com/copilot)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-copilot-certification/module/b02a5227-ee17-43dc-b006-51fef8272f13/lesson/54127571-05ca-48d7-bc66-269b94873930" />
</CardGroup>


# Data Exclusion Mechanisms

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-Certification/Management-of-GitHub-Copilot/Data-Exclusion-Mechanisms/page

Learn to configure content exclusion in GitHub Copilot to protect sensitive data by ignoring specific files or directories.

Learn how to configure content exclusion in GitHub Copilot to safeguard sensitive data. By specifying files or directories to ignore, you can prevent accidental exposure of proprietary code, customer data, and credentials.

Content exclusion offers three key benefits:

* No code completions in excluded files
* Excluded content has zero influence on suggestions in other files
* Copilot Chat will not reference excluded content

<Frame>
  ![The image outlines "Content Exclusion" with three points: no code completions, no suggestions, and no chat data, explaining how excluded content affects these areas.](https://kodekloud.com/kk-media/image/upload/v1752876871/notes-assets/images/GitHub-Copilot-Certification-Data-Exclusion-Mechanisms/content-exclusion-no-suggestions-diagram.jpg)
</Frame>

## Who Can Configure Exclusions?

Different roles can manage content exclusion at various scopes:

| Role                     | Scope            | Permissions                                |
| ------------------------ | ---------------- | ------------------------------------------ |
| Repository Administrator | Individual repo  | Create, update, and remove exclusion rules |
| Organization Owner       | All organization | Define patterns for every Copilot user     |
| Maintainer               | Individual repo  | View settings; cannot modify               |

<Frame>
  ![The image explains who can configure content exclusion, detailing roles such as Repository Administrators, Organization Owners, and those with a "Maintain" role, along with their specific permissions.](https://kodekloud.com/kk-media/image/upload/v1752876872/notes-assets/images/GitHub-Copilot-Certification-Data-Exclusion-Mechanisms/content-exclusion-configuration-roles.jpg)
</Frame>

<Callout icon="triangle-alert">
  Content exclusion is available only to GitHub Copilot Business and Enterprise subscribers. It is not included in individual plans.
</Callout>

***

## Repository-Level Exclusion

Exclude sensitive directories or files within a single repository:

1. Navigate to **Settings** → **Copilot** → **Content Exclusion**.
2. Add fnmatch patterns (wildcards supported).
3. Click **Save** to apply immediately.

<Frame>
  ![The image shows a code editor with a file directory on the left and JavaScript code on the right. There's also a section titled "Repository-Level Exclusion" with instructions on specifying a pattern for exclusion.](https://kodekloud.com/kk-media/image/upload/v1752876873/notes-assets/images/GitHub-Copilot-Certification-Data-Exclusion-Mechanisms/code-editor-repository-exclusion.jpg)
</Frame>

Example: Exclude a `config/` directory and its contents.

```bash theme={null}
