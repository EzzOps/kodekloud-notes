# Guard clause

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Refresher/Guard-clause/page

Explains using guard clauses in shell scripts to fail fast, reduce nesting, and improve readability and maintainability of scripts

In this lesson we cover the guard-clause pattern for Shell scripting — a simple technique that reduces nesting by checking and failing fast on preconditions. Guard clauses make the primary, successful path of your script clear and unindented, improving readability and maintainability.

## Why avoid deep nesting?

Consider a basic file-exists check:

```bash theme={null}
#!/bin/bash
