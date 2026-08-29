# Demo Basic Code Completion

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-in-Action/Introduction-to-GitHub-Copilot/Demo-Basic-Code-Completion/page

A tutorial demonstrating GitHub Copilot usage for Python code completion, docstring-driven implementations, common idioms, error handling, and Copilot Chat debugging.

In this lesson we'll explore basic code completion with GitHub Copilot inside an editor and Copilot Chat. Using a small Python project, you'll see how Copilot suggests completions, responds to docstrings and type hints, and helps diagnose and fix common runtime errors.

> **lightbulb** This tutorial covers practical Copilot usage patterns for Python: completing boilerplate, implementing functions from docstrings, generating list comprehensions, handling file errors, and using Copilot Chat to debug exceptions. Follow along by creating a simple `main.py`.

Relevant links:

* [GitHub Copilot](https://docs.github.com/en/copilot)
* [Copilot Chat](https://docs.github.com/en/copilot/copilot-chat)
* [requests documentation](https://docs.python-requests.org/en/latest/)

## 1) Create a Python file

Create a new file for this demo:

```bash theme={null}
jeremy@Jeremys-Mac-Studio fakedatagenerator % touch main.py
jeremy@Jeremys-Mac-Studio fakedatagenerator %
```

This minimal step prepares the editor for Copilot to begin suggesting completions.

## 2) Hello World

Start with a simple `main` entry point. Copilot often recognizes this pattern and suggests the complete implementation immediately:

```python theme={null}
def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()
```

Run it to confirm everything works:

```bash theme={null}
jeremy@Jeremys-Mac-Studio fakedatagenerator % python3 main.py
Hello, World!
jeremy@Jeremys-Mac-Studio fakedatagenerator %
```

Tip: For trivial patterns like this, accept the suggestion or regenerate if you want stylistic variations.

## 3) Generate a factorial function from a docstring

Copilot leverages function names, type hints, and docstrings to infer implementations. For example, provide a brief signature and docstring:

```python theme={null}
def factorial(n: int) -> int:
    """Returns the factorial of a given number."""
```

Copilot commonly completes it as a recursive solution:

```python theme={null}
def factorial(n: int) -> int:
    """Returns the factorial of a given number."""
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

If you prefer an iterative approach, Copilot may instead generate a loop-based implementation depending on surrounding code and your editing history.

## 4) Extract usernames from a list of dictionaries

Copilot recognizes common Python idioms such as list comprehensions. When you start typing, it often suggests the full comprehension:

```python theme={null}
users = [
    {"name": "Michael", "id": 1},
    {"name": "Sanjeev", "id": 2},
    {"name": "Jeremy", "id": 3},
]

usernames = [user["name"] for user in users]
