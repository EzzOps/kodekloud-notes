# Copilot Custom Instructions
- Use snake_case for JSON keys.
- Prefer f-strings in Python code.
- Include docstrings for all public functions.
```

> **lightbulb** Commit this file to version control so that all collaborators benefit from the same Copilot behavior.

***

## Links and References

* [GitHub Copilot Overview](https://github.com/features/copilot)
* [Visual Studio Code Documentation](https://code.visualstudio.com/docs)
* [Flask Official Site](https://flask.palletsprojects.com/)

You’re all set! Enjoy AI-powered completions, advanced settings, and the collaborative power of Copilot Chat to accelerate your development.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-copilot-certification/module/b02a5227-ee17-43dc-b006-51fef8272f13/lesson/f7cc5c19-f952-4a7e-92d6-2e77f1f1d82f)


# Quick Wins for Immediate Productivity Gains

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-Certification/Introduction/Quick-Wins-for-Immediate-Productivity-Gains/page

This guide explores six strategies to configure GitHub Copilot for immediate productivity improvements.

In this guide, we’ll explore six strategies to configure GitHub Copilot for immediate productivity improvements:

1. File-Based Configuration
2. Testing in `main.py`
3. Using the Completions Panel
4. Keyboard Shortcuts
5. Switching AI Models
6. Managing Context Windows

***

## 1. File-Based Configuration

Store custom instructions at the repository root to steer Copilot’s code generation.

```bash theme={null}
mkdir .github
touch .github/copilot-instructions.md
```

Anything you add to `copilot-instructions.md` will shape Copilot’s output. For example, to enforce PEP 8 in Python:

```markdown theme={null}
