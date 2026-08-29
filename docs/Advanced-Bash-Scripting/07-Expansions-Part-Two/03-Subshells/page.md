# Output: John
```

> **lightbulb** Always quote your variable expansions (`"${var}"`) to preserve whitespace and avoid unexpected globbing.

## What Is Command Substitution?

Command substitution runs a command in a subshell and replaces the command with its standard output. There are two syntaxes:

| Syntax      | Description                            |
| ----------- | -------------------------------------- |
| `$( ... )`  | Preferred form; allows nesting easily. |
| `` `...` `` | Deprecated; harder to read and nest.   |

### Example: Counting Files on the Command Line

```bash theme={null}
$ ls
DEV001  DEV002  DEV003  DEV004  MKT001  MKT002  MKT003  MKT004  command-substitution.sh
$ find . -type f | wc -l
9
```

### Using `$( ... )`

Create `command-substitution.sh`:

```bash theme={null}
#!/usr/bin/env bash
file_count=$(find . -type f | wc -l)
echo "Total files: ${file_count}"
```

Run it:

```bash theme={null}
$ chmod +x command-substitution.sh
$ ./command-substitution.sh
Total files: 9
```

### Using Backticks (Deprecated)

```bash theme={null}
#!/usr/bin/env bash
file_count=`find . -type f | wc -l`
echo "Total files: ${file_count}"
```

> **triangle-alert** Backticks are deprecated. They complicate nesting and reduce readability. Always prefer `$( ... )` in modern Bash scripts.

## Accepting a Directory Argument

Require the user to specify a target directory:

```bash theme={null}
#!/usr/bin/env bash
if [[ -z "${1}" ]]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

file_count=$(find "${1}" -type f | wc -l)
echo "Files in ${1}: ${file_count}"
```

```bash theme={null}
$ ./command-substitution-v2.sh .
Files in .: 9
```

## Timing Considerations

Command substitution runs once when assigned. If you modify files later, the stored value stays unchanged until you reassign it.

```bash theme={null}
#!/usr/bin/env bash
if [[ -z "${1}" ]]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

file_count=$(find "${1}" -type f | wc -l)
echo "Initial count: ${file_count}"

touch samplefile
echo "After touch: ${file_count}"
```

```bash theme={null}
$ ./command-substitution-v3.sh .
Initial count: 9
After touch: 9
```

Re-running the script updates the count:

```bash theme={null}
$ ./command-substitution-v3.sh .
Initial count: 10
After touch: 10
```

## Subshell Scope

Command substitution executes in a subshell. Variables modified inside do not affect the parent shell:

```bash theme={null}
#!/usr/bin/env bash
if [[ -z "${1}" ]]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

dir=${1}
file_count=$(find "${dir}" -type f | wc -l)

sub_output=$(
  dir="/some/other/dir"
  echo "Dir in subshell: ${dir}"
)

echo "Dir in parent shell: ${dir}"
echo "${sub_output}"
```

```plaintext theme={null}
$ ./command-substitution-v4.sh /usr/bin
Dir in parent shell: /usr/bin
Dir in subshell: /some/other/dir
```

![The image explains that a subshell is a child process spawned by a parent shell, inheriting environment variables but not propagating them back to the parent shell.](https://kodekloud.com/kk-media/image/upload/v1752868563/notes-assets/images/Advanced-Bash-Scripting-Command-Substitution/subshell-child-process-inheritance.jpg)

A subshell inherits your environment but keeps its changes local.

## Performance Considerations

Each command substitution spawns a new process. In most scripts this overhead is negligible, but in performance-critical loops, minimize unnecessary substitutions.

> **triangle-alert** Avoid placing heavy command substitutions inside tight loops. Consider alternatives like `readarray` or built-in string operations when processing large datasets.

## Honorable Mentions

| Use Case          | Example                |
| ----------------- | ---------------------- |
| Capture `stderr`  | `files=$(ls -j 2>&1)`  |
| Capture timestamp | `current_date=$(date)` |

```bash theme={null}
echo "Errors: ${files}"
echo "Today's date: ${current_date}"
```

## Links and References

* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
* [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
* [ShellCheck: Shell Script Analysis](https://www.shellcheck.net/)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/3fde6601-133e-4f17-bea6-482a206dba5c/lesson/8437d090-c5f8-45ea-8d11-0d088276f55e)


# Subshells

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Expansions-Part-Two/Subshells/page

This article explains subshells in Bash, covering command substitution, syntax, common scenarios, and how to manage variable scope and process IDs.

Command substitution with `$(…)` captures the output of commands into a variable, but it does so by spawning a *subshell*—a child process separate from your main shell:

```bash theme={null}
#!/usr/bin/env bash
file_count=$(find . -type f | wc -l)
```

> **lightbulb** Assignments made inside the subshell do *not* affect variables in the parent shell.

Because a new process is created, there’s a small performance cost compared to running commands directly in the parent shell.

> **triangle-alert** Overusing complex command substitutions inside tight loops can degrade script performance. Measure and optimize if needed.

```bash theme={null}
#!/usr/bin/env bash
var="a"
subshell=$( var="b" )
echo "$var"        # still "a"
echo "$subshell"   # empty, because var="b" was in the subshell
```

![The image explains that a subshell is a child process spawned by a parent shell, inheriting environment variables but not propagating them back to the parent shell.](https://kodekloud.com/kk-media/image/upload/v1752868564/notes-assets/images/Advanced-Bash-Scripting-Subshells/subshell-child-process-explanation.jpg)

***

## 1. Subshell Syntax

Wrap commands in parentheses to run them in a subshell:

![The image illustrates subshell syntax, showing a command enclosed in parentheses, with a note about script execution context.](https://kodekloud.com/kk-media/image/upload/v1752868565/notes-assets/images/Advanced-Bash-Scripting-Subshells/subshell-syntax-command-illustration.jpg)

```bash theme={null}
#!/usr/bin/env bash
current_env="shell"
(
  echo "This is running in a ${current_env}"
)
```

```plaintext theme={null}
$ ./subshell-v0.sh
This is running in a shell
```

To prove isolation:

```bash theme={null}
#!/usr/bin/env bash
current_env="a"
(
  current_env="b"
  echo "Inside subshell: $current_env"
)
echo "Outside subshell: $current_env"
```

```plaintext theme={null}
$ ./subshell-v1.sh
Inside subshell: b
Outside subshell: a
```

***

## 2. Command Substitution with a Subshell

Combine a subshell with `$(…)` to capture its output separately from the parent shell:

```bash theme={null}
#!/usr/bin/env bash
current_env="a"

subsh_var=$(
  current_env="b"
  echo "$current_env"
)

echo "Parent environment: $current_env"
echo "Subshell output: $subsh_var"
```

```plaintext theme={null}
$ ./subshell-v2.sh
Parent environment: a
Subshell output: b
```

Errors inside the subshell still appear on the terminal:

```bash theme={null}
#!/usr/bin/env bash
subsh_var=$(
  echo "Output"
  ls -fakeoption
)
```

```plaintext theme={null}
$ ./subshell-v2-stderr.sh
ls: unrecognized option '--fakeoption'
```

***

## 3. Command Layout in Subshells

Within parentheses, you can:

* Put commands on separate lines
* Separate with semicolons (`;`)
* Pipe between them (`|`)
* Chain with `&&` or `||`

```bash theme={null}
