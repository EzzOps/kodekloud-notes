# Overview

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Expansions-Part-One/Overview/page

This guide explores core shell expansions in POSIX-compliant shells to enhance shell scripts and command-line workflows.

In this guide, we’ll dive into the core shell expansions available in POSIX-compliant shells (like Bash and Zsh). You’ll learn how to use:

* Brace expansions
* Parameter expansions
* Command substitutions
* Filename generation (globs)

These mechanisms let you generate sequences, extract substrings, capture command output, and match multiple filenames—streamlining your shell scripts and command-line workflows.

## Table of Expansion Types

| Expansion Type       | Description                                       | Example                                   |
| -------------------- | ------------------------------------------------- | ----------------------------------------- |
| Brace                | Generate comma- or range-separated strings        | `echo {A,B,C}` → A B C                    |
| Parameter            | Manipulate variable values (substrings, defaults) | `${var##*/}` → strips longest `*/` prefix |
| Command Substitution | Insert command output into another command        | `echo "Date: $(date +%F)"`                |
| Filename Generation  | Match files with wildcards (globs)                | `ls *.txt` → lists all `.txt` files       |

For an in-depth reference, see the [Bash manual on Shell Expansions][bash-expansion].

[bash-expansion]: https://www.gnu.org/software/bash/manual/html_node/Shell-Expansions.html

***

## 1. Brace Expansion

Brace expansion quickly generates arbitrary strings. It’s purely a string generation mechanism—no variables or globs involved.

```bash theme={null}
