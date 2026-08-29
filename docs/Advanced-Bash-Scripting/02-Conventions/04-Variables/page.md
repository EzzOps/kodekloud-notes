# Variables

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Conventions/Variables/page

Proper variable management in Bash scripts enhances readability, prevents overwrites, and simplifies code maintenance through best practices for naming, constants, and exporting values.

Proper variable management in Bash scripts improves readability, prevents accidental overwrites, and makes your code easier to maintain. In this guide, you’ll learn best practices for naming variables, defining constants, and exporting values for child processes.

***

## Table of Contents

* [1. Naming Conventions](#1-naming-conventions)
* [2. Defining Constants](#2-defining-constants)
* [3. Exporting Variables](#3-exporting-variables)
* [4. References](#4-references)

***

## 1. Naming Conventions

Follow these guidelines to create clear, self-documenting variable names:

| Convention               | Description                                        | Example                        |
| ------------------------ | -------------------------------------------------- | ------------------------------ |
| Lowercase                | All variable names in lowercase to avoid conflicts | `username="alice"`             |
| Snake case               | Use underscores for multi-word names               | `first_name_last_name="Alice"` |
| Descriptive names        | Reflect the variable’s purpose                     | `config_file="/etc/app.conf"`  |
| Single-letter (optional) | Only for simple counters or arithmetic operations  | `x=10`                         |

Example:

```bash theme={null}
first_name_last_name="Alice"
source_file="/etc/config.yaml"
count=42
x=10
```

<Callout icon="lightbulb">
  Avoid uppercase names for regular variables—uppercase is conventionally reserved for constants (see [Defining Constants](#2-defining-constants)).
</Callout>

***

## 2. Defining Constants

When you have values that should never change, define them in uppercase snake\_case and mark them as read-only:

```bash theme={null}
readonly FILE_NAME="file.txt"
readonly MAX_RETRIES=5
readonly PI=3.14159
```

Using `readonly` serves two purposes:

1. **Clarity:** Signals to readers that these values are fixed.
2. **Safety:** Prevents accidental reassignment later in the script.

<Callout icon="triangle-alert">
  Attempting to modify a `readonly` variable will produce an error:

  ```bash theme={null}
  PI=3.14   # bash: PI: readonly variable
  ```
</Callout>

***

## 3. Exporting Variables

Export variables when you need them in child processes, subshells, or external scripts.

### Export an existing variable

```bash theme={null}
source_file="/etc/config.yaml"
export source_file
```

### Define and export in one step

```bash theme={null}
export HOME_DIR="/home/user"
```

Exported variables become part of the environment for all subsequent commands and processes started from the current shell.

***

## 4. References

* [Bash Reference Manual – Variables](https://www.gnu.org/software/bash/manual/html_node/Shell-Variables.html)
* [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/06219b3e-dc63-404c-a9df-3ea035628308/lesson/4c6c4d36-08a6-4632-ba8a-79827c7f0cf5" />
</CardGroup>
