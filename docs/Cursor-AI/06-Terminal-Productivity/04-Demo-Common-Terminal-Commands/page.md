# Before Cursor
def fetch_user(id):
    response = requests.get(f"https://api.example.com/users/{id}")
    return response.json()

# After Cursor suggests and adds:
import requests
```

You can fine-tune import behavior in Composer:

| Setting                   | Description                                |
| ------------------------- | ------------------------------------------ |
| Auto Import On Completion | Insert imports when selecting a completion |
| Import Style              | Choose between absolute and relative paths |

***

## 4. Essential Prompt Engineering

Fine-tune your prompts to get the best results:

* **Be specific**: Include function signatures or expected return types.
* **Use context**: Provide surrounding code snippets for better accuracy.
* **Iterate quickly**: Refine your prompt based on Cursor’s initial suggestions.

```bash theme={null}
# Prompt example in Ask Mode
# “Generate a TypeScript interface for a REST response with fields: id, name, email.”
```

***

## 5. Using Ask Mode for Interactive Assistance

Ask Mode transforms your editor into an AI chat interface. Use it to:

* Debug errors by pasting stack traces
* Refactor code snippets on the fly
* Generate documentation or unit tests

Press `Ctrl+Shift+P` and select **Cursor: Open Ask Mode** to begin.

***

## References

* [Cursor Documentation](https://docs.cursor.dev/)
* [Visual Studio Code](https://code.visualstudio.com/)
* [Prompt Engineering Best Practices](https://ai.googleblog.com/2021/04/prompt-engineering.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/cursor-ai/module/e11e1c1e-9b6b-4c53-b14a-24babbd114a5/lesson/0fde7f79-2d60-4881-b2a7-22b2882b50e7)


# Demo Common Terminal Commands

Source: https://notes.kodekloud.com/docs/Cursor-AI/Terminal-Productivity/Demo-Common-Terminal-Commands/page

Learn to generate and execute terminal commands using Cursor AI for macOS, Linux, and Windows by describing tasks in plain English.

In this tutorial, you’ll learn how to generate and execute common terminal commands using Cursor AI. Whether you’re a beginner or an experienced user, Cursor AI lets you describe tasks in plain English and receive the correct CLI syntax for macOS, Linux, and Windows.

## Activating Cursor AI in Your Shell

Press **Command+K** (macOS) or **Ctrl+K** (Windows/Linux) to open the Cursor AI prompt. Then type your instruction in natural language. Cursor AI will suggest the corresponding shell command.

***

## 1. Creating a Directory

### English Prompt

```text theme={null}
create a new directory called project files
```

### Generated Command

```bash theme={null}
mkdir "project files"
```

### Execution

```bash theme={null}
venvjeremy@MACSTUDIO KodeKloudTaskManager % mkdir "project files"
```

> **lightbulb** Always wrap directory names containing spaces in quotes (`" "`).

***

## 2. Creating Multiple Files

### English Prompt

```text theme={null}
create five blank text files named test1.txt through test5.txt in project files
```

### Generated Command

```bash theme={null}
touch "project files/test1.txt" "project files/test2.txt" "project files/test3.txt" "project files/test4.txt" "project files/test5.txt"
```

### Execution

```bash theme={null}
venvjeremy@MACSTUDIO KodeKloudTaskManager % touch "project files/test1.txt" "project files/test2.txt" "project files/test3.txt" "project files/test4.txt" "project files/test5.txt"
```

***

## 3. Moving Files into a Subdirectory

### English Prompt

```text theme={null}
create a directory named test and move all .txt files from project files into test
```

### Generated Commands

```bash theme={null}
mkdir test
mv "project files/"*.txt test/
```

### Execution

```bash theme={null}
venvjeremy@MACSTUDIO KodeKloudTaskManager % mkdir test
venvjeremy@MACSTUDIO KodeKloudTaskManager % mv "project files/"*.txt test/
```

***

## 4. Displaying Date and Time

To display the current system date and time:

```bash theme={null}
venvjeremy@MACSTUDIO KodeKloudTaskManager % date
```

***

## 5. Viewing System Resource Usage

### English Prompt

```text theme={null}
display system resource usage
```

### Generated Command

```bash theme={null}
top
```

### Execution

```bash theme={null}
venvjeremy@MACSTUDIO KodeKloudTaskManager % top
```

Sample output:

```text theme={null}
Processes: 809 total, 4 running, 805 sleeping, 5693 threads
Load Avg: 4.08, 3.48, 3.20  CPU usage: 5.48% user, 6.29% sys, 88.22% idle
MemRegions: 764871 total, 226M resident, 1282M private, 7780M shared
PhysMem: 67G used (3369M wired), 60G unused
```

> Press **Ctrl+C** to exit `top`.

***

## 6. Updating All Python Packages

### English Prompt

```text theme={null}
update all python packages
```

Cursor AI may suggest:

```bash theme={null}
pip install --upgrade pip && \
pip list --outdated --format=freeze | \
grep -v '^\-e' | cut -d= -f1 | xargs -n1 pip install -U
```

If you encounter:

```bash theme={null}
ERROR: List format 'freeze' cannot be used with the --outdated option.
```

Refine your prompt:

```text theme={null}
update all python packages without using freeze format
```

### Updated Commands

```bash theme={null}
pip install --upgrade pip
pip list --outdated --format=columns | \
tail -n +3 | awk '{print $1}' | xargs -n1 pip install -U
```

> **triangle-alert** Using `xargs` can install many packages at once—ensure you trust the source before running.

***

## 7. Showing Recent Git Commits

### English Prompt

```text theme={null}
show the last five git commits
```

### Generated Command

```bash theme={null}
git log -5 --oneline
```

In a Git repository, this will list the five most recent commits. Outside a repo, you’ll see:

```bash theme={null}
fatal: not a git repository (or any of the parent directories): .git
```

***

## Command Reference Table

| Command   | Description                               | Example                                                                        |
| --------- | ----------------------------------------- | ------------------------------------------------------------------------------ |
| `mkdir`   | Create a new directory                    | `mkdir "project files"`                                                        |
| `touch`   | Create empty files                        | `touch "project files/test1.txt" ... "project files/test5.txt"`                |
| `mv`      | Move or rename files                      | `mv "project files/"*.txt test/`                                               |
| `date`    | Display current date and time             | `date`                                                                         |
| `top`     | Show real-time system resource statistics | `top`                                                                          |
| `pip`     | Install and upgrade Python packages       | `pip install --upgrade pip && pip list --outdated \| xargs -n1 pip install -U` |
| `git log` | View recent Git commits                   | `git log -5 --oneline`                                                         |

***

## Links and References

* [Cursor AI Documentation](https://cursor.com/docs)
* [GNU Coreutils (mkdir, mv, touch)](https://www.gnu.org/software/coreutils/)
* [pip User Guide](https://pip.pypa.io/en/stable/user_guide/)
* [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)

With Cursor AI, managing your shell tasks is faster and more intuitive—just ask in plain English!

- [Watch Video](https://learn.kodekloud.com/user/courses/cursor-ai/module/90a13f7e-74a3-4207-8c34-c81c14757507/lesson/b2fc8d40-f707-4b20-9cdb-a188a89d9ef7)
