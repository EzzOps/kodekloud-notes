# Quick Wins for Immediate Productivity Gains

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-in-Action/Core-Features/Quick-Wins-for-Immediate-Productivity-Gains/page

Tips to improve GitHub Copilot productivity through repository instructions, editor versus chat usage, Completions panel, keyboard shortcuts, and model and context selection

Boost your GitHub Copilot productivity with a few focused configurations and workflows you can apply immediately. This guide covers repository-level instructions, comparing editor vs. chat behavior, using the Completions panel, keyboard shortcuts, and choosing models and context for better suggestions.

Quick reference

| Tip                                   | Why it helps                                                 | Example / Link                                                                                                        |
| ------------------------------------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| Repository-level Copilot instructions | Ensures project-specific style and constraints are respected | Add `.github/copilot-instructions.md`                                                                                 |
| Editor vs. Copilot Chat               | Chat often produces fuller, annotated implementations        | [Copilot Chat docs](https://docs.github.com/en/copilot/getting-started-with-github-copilot/about-github-copilot-chat) |
| Completions panel                     | Compare multiple variants before accepting                   | Use the Completions panel in the Copilot UI                                                                           |
| Keyboard shortcuts                    | Accept suggestions faster and stay in flow                   | Configure in VS Code Keybindings                                                                                      |
| Model & context selection             | Different models & focused files give better results         | Switch models inside Copilot Chat and close irrelevant files                                                          |

## 1) Add a repository-level Copilot instruction file

Place project-specific guidance where Copilot will read it automatically: create a Markdown file in the repository's `.github/` folder named `copilot-instructions.md` (or create a Markdown file titled "Copilot Instructions" inside `.github`). Use this file to state coding standards, preferred patterns, and generation preferences so Copilot generates code aligned with your project.

Example: create the `.github` directory

```bash theme={null}
(venv) jeremy@Jeremys-Mac-Studio FakeDataGenerator % mkdir .github
(venv) jeremy@Jeremys-Mac-Studio FakeDataGenerator %
```

Then add `.github/copilot-instructions.md` with your project's conventions — formatting, naming, import ordering, docstring expectations, and any edge-case guidance.

<Callout icon="lightbulb">
  Name the file `.github/copilot-instructions.md` and commit it to the repository so Copilot can discover and apply it automatically.
</Callout>

Example PEP 8-focused `copilot-instructions.md` (practical starting point)

```markdown theme={null}
## Purpose
Provide instructions for GitHub Copilot to generate PEP8-compliant Python code: readable, documented, and consistent.

## General Guidelines
1. Follow the [PEP 8](https://peps.python.org/pep-0008/) style guide.
2. Use 4 spaces per indentation level.
3. Keep lines <= 79 characters when possible.
4. Include docstrings for classes, methods, and public functions.
5. Avoid trailing whitespace.

## Naming Conventions
- Use `snake_case` for variables and functions.
- Use `PascalCase` for class names.
- Constants in `ALL_CAPS`.

## Imports
- Place imports at the top of the file.
- Group imports: standard library, third-party, local.
- One import per line; avoid wildcards.
```

You can make this stricter (for CI or linters) or lighter (for rapid prototyping) depending on team needs.

## 2) Test how Copilot responds: editor inline suggestions vs. Copilot Chat

Copilot behaves differently depending on how you prompt it:

* Inline (editor) suggestions often aim for brevity and fast completion. They are great for small, routine edits.
* Copilot Chat usually produces more thorough results — typed signatures, docstrings, and explanatory comments — especially when you provide a detailed prompt or reference the repository instruction file.

Example: minimal inline suggestion (editor)

```python theme={null}
