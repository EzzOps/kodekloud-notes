# Check if a file exists
if [[ -e myfile.txt ]]; then
    echo "File exists"
else
    echo "File does not exist"
fi
```

Now compare that to a more deeply nested script that validates a user and file conditions before running a process:

```bash theme={null}
#!/bin/bash

if [[ "${USER_NAME}" == "admin" ]]; then
    if [[ -e "${FILE_PATH}" ]]; then
        if [[ -s "${FILE_PATH}" ]]; then
            run_process
        else
            echo "File exists but is empty"
        fi
    else
        echo "File does not exist"
    fi
else
    echo "User is not admin"
fi

exit 0
```

Deep nesting like this makes control flow harder to follow and increases the cognitive load when scanning code or debugging.

## Use guard clauses to fail fast

A cleaner approach is to check preconditions early and exit immediately when they fail. This keeps the successful execution path flat and easy to read.

Here is an idiomatic version of the previous script using guard clauses. Each critical condition is checked up front and exits on failure, leaving the main logic simple:

```bash theme={null}
#!/bin/bash
readonly FILE_PATH="/home/ubuntu/guard_clause/file.txt"
readonly USER_NAME="admin"

run_process() {
    echo "running process..."
}

if [[ "${USER_NAME}" != "admin" ]]; then
    echo "User is not admin"
    exit 1
fi

if [[ ! -e "${FILE_PATH}" ]]; then
    echo "File does not exist"
    exit 1
fi

if [[ ! -s "${FILE_PATH}" ]]; then
    echo "File exists but is empty"
    exit 1
fi

run_process

exit 0
```

By reversing conditionals (using ! where appropriate) and exiting immediately on failure, the main successful path of the script is simple and unindented.

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Guard Clause&#x22; with a small check/cross icon on the left. On the right are three checked points: &#x22;Improve code readability&#x22;, &#x22;Reduce the nesting depth or conditional statements&#x22;, and &#x22;Prevent hard-to-find bugs.&#x22;" />
</Frame>

Guard clauses are like preparing tools before disassembling a car — you check essentials first so the rest of the work assumes those conditions are met.

## Minimal guard example

A very small guard clause to ensure a file exists:

```bash theme={null}
if [[ ! -f ${file} ]]; then
    exit 1
fi
```

This ensures subsequent code runs only when the file is present.

## Practical example: require a CLI argument

A common guard is verifying the presence of required command-line arguments before proceeding. Example for `git clone`:

```bash theme={null}
#!/bin/bash

if [[ -z "${1}" ]]; then
    echo "Usage: $0 <git-repository-url>"
    exit 1
fi

git_url="${1}"

git clone "${git_url}"

exit 0
```

Tips:

* For scripts that take multiple or optional flags, prefer getopts or a parsing library.
* Use special shell variables like `$#`, `$@`, and positional parameters to write robust argument checks.

## One-line guard idioms

Shell short-circuit logic is often used for concise guard patterns:

* OR (||) — run the right-hand side if the left-hand side fails.
* AND (&&) — run the right-hand side only if the left-hand side succeeds.

| Operator | Use case                                  | Example                                          |                                   |                       |   |                            |
| -------: | ----------------------------------------- | ------------------------------------------------ | --------------------------------- | --------------------- | - | -------------------------- |
|          |                                           |                                                  | Fail fast with a fallback command | \[\[ -f "file.txt" ]] |   | echo "file does not exist" |
|       && | Execute follow-up command only on success | \[\[ -n "${1}" ]] && echo "argument provided: $" |                                   |                       |   |                            |

When using multiple commands on the right-hand side (for example, printing a message then exiting), group them with braces:

```bash theme={null}
[[ -f "file.txt" ]] || { echo "file does not exist"; exit 1; }
```

## References

* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
* [Shell Scripting Best Practices](https://www.shellscript.sh/)
* [Git Documentation - git-clone](https://git-scm.com/docs/git-clone)

> **lightbulb** Guard clauses improve readability by reducing nesting, making successful execution paths clear, and failing early on error conditions.

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/397a2175-a186-4a6d-916e-d688c8def203/lesson/15034de9-a52e-40bc-8099-230a7f14c177)


# Keywords builtins

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Refresher/Keywords-builtins/page

This article explores the differences between Bash built-in commands and shell keywords, focusing on execution, process forking, and their roles in scripting.

In this lesson, we explore the fundamental distinctions between Bash built-in commands and shell keywords. Built-ins execute inside the shell without spawning extra processes, whereas keywords are parsed tokens that implement control structures and logic flow.

## Shell Built-ins vs Keywords

| Aspect          | Built-in Commands         | Keywords                    |
| --------------- | ------------------------- | --------------------------- |
| Execution       | Runs inside the shell     | Parsed by the shell         |
| Process Forking | No new process            | No new process              |
| Documentation   | `help` or `man` available | No separate manual page     |
| Role            | Utility operations        | Control structures & tokens |

![The image compares "Shell-Builtin" and "Keywords," highlighting that shell-builtins are executables with flags and a man page, while keywords are special words for controlling execution structure parsed by the shell.](https://kodekloud.com/kk-media/image/upload/v1752868593/notes-assets/images/Advanced-Bash-Scripting-Keywords-builtins/shell-builtins-vs-keywords-comparison.jpg)

Shell built-ins (like `echo`, `cd`, or `[ ]`) are implemented directly within Bash, complete with flags and documentation via `help` or `man`. Keywords (like `if`, `for`, or `[[ ]]`) are special words the shell interpreter parses to direct execution order and logic.

> **lightbulb** Built-in commands minimize overhead by avoiding additional process creation. Keywords define the script’s flow without calling external binaries.

## Single vs Double Square Brackets

Single brackets (`[ ]`) are a built-in alias for the `test` command. Double brackets (`[[ ]]`) are keywords with enhanced features and direct parsing by Bash.

### builtin-sample.sh

```bash theme={null}
#!/bin/bash
if [ 2 -eq 2 ]; then
    echo "two equals two"
fi
```

```bash theme={null}
$ ./builtin-sample.sh
two equals two
```

### keyword-sample.sh

```bash theme={null}
#!/bin/bash
if [[ 2 -eq 2 ]]; then
    echo "two equals two"
fi
```

```bash theme={null}
$ ./keyword-sample.sh
two equals two
```

## `[` vs `test`

Under the hood, `[ ]` is just the `test` built-in. You can invoke either name interchangeably:

```bash theme={null}
$ test 2 -eq 2 && echo "two equals two"
two equals two
```

View its documentation with:

```bash theme={null}
$ man test
```

Since `[[ ]]` has no external binary, Bash handles it entirely as a keyword.

## Built-in vs Keyword Evaluations

![The image compares "Built-in" and "Keyword" condition evaluations using brackets and double brackets, respectively. It visually distinguishes between the two types of condition evaluations.](https://kodekloud.com/kk-media/image/upload/v1752868595/notes-assets/images/Advanced-Bash-Scripting-Keywords-builtins/built-in-vs-keyword-evaluations.jpg)

Single brackets interpret `<` as a redirection operator:

```bash theme={null}
$ [ 1 < 2 ] && echo "1 is less than 2"
-bash: 2: No such file or directory
```

Double brackets support `<` as a comparison operator:

```bash theme={null}
$ [[ 5 < 7 ]] && echo "5 is less than 7"
5 is less than 7
```

## Advanced Double Bracket Features

Double brackets unlock logical grouping, glob patterns, and regular expressions:

```bash theme={null}
$ [[ 3 -eq 3 && (2 -eq 2 && 1 -eq 1) ]] && echo "Parentheses can be used"
Parentheses can be used

$ name="Bob Doe"
$ [[ $name = *o* ]] && echo "Patterns can be used"
Patterns can be used

$ name="Bob Doe"
$ [[ $name =~ B.*Doe ]] && echo "Regular expressions can be used"
Regular expressions can be used
```

> **triangle-alert** The `[[ ]]` syntax is not POSIX compliant and may not be available in all shells. Use it only when Bash-specific features are acceptable.

## Advantages and Disadvantages

### Single Square Brackets (`[ ]`)

![The image compares keywords and built-in features, highlighting that keywords are more portable and widely supported, while built-in features have a narrower selection of conditionals.](https://kodekloud.com/kk-media/image/upload/v1752868596/notes-assets/images/Advanced-Bash-Scripting-Keywords-builtins/keywords-vs-built-in-features-comparison.jpg)

Advantages:

* Portable across POSIX-compliant shells
* Standard conditional syntax

Disadvantages:

* Limited to basic comparisons
* No pattern matching or grouping

### Double Square Brackets (`[[ ]]`)

<Frame>
  ![The image compares the advantages and disadvantages of using double square brackets "\[\[ \]\]" in programming, highlighting more support and wider conditional evaluation versus lack of backward compatibility and non-compliance with POSIX.](https://kodekloud.com/kk-media/image/upload/v1752868596/notes-assets/images/Advanced-Bash-Scripting-Keywords-builtins/double-square-brackets-comparison.jpg)
</Frame>

Advantages:

* Extended conditionals (regex, globs, grouping)
* Safer string comparisons

Disadvantages:

* Not POSIX compliant
* Bash-specific feature

## Summary: Built-ins vs Keywords

![The image is a slide titled "Guard Clause" with three check-marked statements about shell commands and keywords.](https://kodekloud.com/kk-media/image/upload/v1752868597/notes-assets/images/Advanced-Bash-Scripting-Keywords-builtins/guard-clause-shell-commands-slide.jpg)

* Shell built-ins run inside Bash without forking.
* Keywords are parsed tokens controlling flow or behavior.
* Neither built-ins nor keywords spawn external processes.

Certain keywords (e.g., `time`) act like directives rather than forming explicit control structures. Armed with these distinctions, you can choose the most efficient and appropriate syntax for your Bash scripts.

## Links and References

* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
* [POSIX Shell Syntax](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
* [Bash Conditional Expression Documentation](https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/397a2175-a186-4a6d-916e-d688c8def203/lesson/fc38a23f-6af6-4415-b451-c1073291096d)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/397a2175-a186-4a6d-916e-d688c8def203/lesson/369ebee0-f833-42f8-ac55-41c73bb16a5b)
