# Shell scripting vs Bash scripting

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Introduction/Shell-scripting-vs-Bash-scripting/page

This article compares shell scripting and Bash scripting, highlighting their differences, features, and when to use each.

Shell scripting is the practice of writing executable text files that interpret and execute commands in a Unix-like shell. While **Bash** (Bourne Again SHell) is the most common shell today, there are many others:

| Shell         | Year Introduced | Key Feature                       |
| ------------- | --------------- | --------------------------------- |
| Bourne `sh`   | 1979            | Original shell scripting standard |
| Bash          | 1989            | Rich scripting constructs         |
| Z shell `zsh` | 1990            | Typo correction & plugin system   |
| Korn `ksh`    | 1983            | Advanced variables & functions    |
| Dash          | 1997            | Focus on speed & minimalism       |

Use **shell scripting** when referring to any shell. If you depend on Bash-specific features (arrays, `[[ … ]]`, process substitution), say **shell scripting with Bash**.

<Callout icon="lightbulb">
  Always include a shebang (`#!`) at the top of your scripts to declare which shell to use:

  ```bash theme={null}
  #!/usr/bin/env bash
  ```
</Callout>

## When to Use “Shell” vs. “Bash” Scripting

* **Shell scripting** – generic term for writing scripts in any shell
* **Shell scripting with Bash** – when your code relies on Bash-only features
* **Shell scripting with zsh**, **ksh**, etc. – when targeting those environments

## Illustrative Differences Between Bash and Other Shells

Below are two examples that show how Bash and other shells (like `sh` and `zsh`) can behave differently.

### 1. zsh Autocorrects Typos

Zsh offers a user‐friendly autocorrect feature:

```zsh theme={null}
$ LS -l FILE.TXT
file.txt
```

Here, `zsh` automatically corrects `LS` → `ls` and `FILE.TXT` → `file.txt`. Bash does not do this by default.

### 2. `echo -n` Behavior

The `-n` flag suppresses the trailing newline in Bash, but not in all `sh` implementations:

```bash theme={null}
