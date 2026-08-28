# Clone the repository passed as the first argument
git clone "$1"

# Count files in the cloned repo
find . -type f | wc -l
```

Run it as:

```bash theme={null}
$ ./clone-and-count.sh git@github.com:kodedkloud/kodekloud-advanced-shell-scripting.git
```

Now the script clones any repository you specify.

***

## Common Special Variables

| Variable      | Description                                   | Example Output        |
| ------------- | --------------------------------------------- | --------------------- |
| `$0`          | Script name                                   | `./myscript.sh`       |
| `$1`, `$2`, … | First, second, … arguments                    | `apple banana`        |
| `$#`          | Total number of arguments                     | `3`                   |
| `$@`          | All arguments as separate words               | `apple banana cherry` |
| `$*`          | All arguments as a single word (`"$*"` joins) | `apple banana cherry` |

Example:

```bash theme={null}
#!/bin/bash
echo "Script name: $0"
echo "Number of arguments: $#"
echo "All arguments (\$@): $@"
```

```bash theme={null}
$ ./myscript.sh apple banana cherry
Script name: ./myscript.sh
Number of arguments: 3
All arguments ($@): apple banana cherry
```

***

## Handling Maximum Argument Size (`ARG_MAX`)

Unix-like systems impose a limit on the total size of command-line arguments. Check it with:

```bash theme={null}
$ getconf ARG_MAX
1048576
```

On most Linux distributions, `ARG_MAX` is around 1 MiB, which is sufficient for tens of thousands of small arguments.

<Callout icon="triangle-alert">
  Exceeding `ARG_MAX` will cause a “Argument list too long” error. For bulk operations, consider using `xargs` or reading from a file.
</Callout>

***

## Iterating with `shift`

The `shift` command discards `$1` and shifts all other parameters down by one. This is useful when you don’t know the number of arguments in advance:

```bash theme={null}
#!/bin/bash

# Loop through all arguments
while [ $# -gt 0 ]; do
  echo "Current argument: $1"
  shift
done
```

```bash theme={null}
$ ./shift-example.sh arg1 arg2 arg3
Current argument: arg1
Current argument: arg2
Current argument: arg3
```

***

Command-line arguments empower you to build dynamic, user-driven shell scripts. Next up: advanced option parsing with `getopts` and long-form flags.

## References

* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
* [getconf](https://man7.org/linux/man-pages/man1/getconf.1.html)
* [find(1) — Find Files](https://man7.org/linux/man-pages/man1/find.1.html)
* [wc(1) — Word, Line, Character, and Byte Count](https://man7.org/linux/man-pages/man1/wc.1.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/397a2175-a186-4a6d-916e-d688c8def203/lesson/6e6bb850-f9cf-4691-8989-90c04cfa5ed0" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/397a2175-a186-4a6d-916e-d688c8def203/lesson/0a5601db-062f-4f6e-b630-c6cca0d2b275" />
</CardGroup>


# Functions

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Refresher/Functions/page

This article explains how to use Bash functions for structuring, reusing, and maintaining scripts, enhancing modularity and readability in coding.

In this lesson, you’ll learn how Bash functions help you structure, reuse, and maintain your scripts. While Bash offers conditionals, loops, and script sourcing, functions are key to modular, readable code.

<Frame>
  ![The image shows a diagram with four interconnected squares labeled "Conditional Statement," "Loops," "Functions," and "Source Code," under the title "Function."](https://kodekloud.com/kk-media/image/upload/v1752868590/notes-assets/images/Advanced-Bash-Scripting-Functions/function-diagram-conditional-loops-functions.jpg)
</Frame>

## Why Define Functions in Bash?

Functions encapsulate a sequence of commands into a single callable unit. This reduces repetition, minimizes errors, and makes your scripts easier to update and test.

Imagine a chef perfecting a recipe once and reusing it whenever needed—functions work the same way in scripting.

### Backup Script: Before vs. After

Without a function:

```bash theme={null}
#!/bin/bash

mkdir backup
cd backup
cp -r "${1}" .
tar -czvf backup.tar.gz *
echo "Backup complete!"
```

Refactored with a function:

```bash theme={null}
#!/bin/bash

perform_backup() {
    mkdir -p backup
    cd backup || exit 1
    cp -r "${1}" .
    tar -czvf backup.tar.gz *
    echo "Backup complete!"
}

perform_backup "${1}"
exit 0
```

<Callout icon="triangle-alert">
  Always use `mkdir -p` to avoid errors if the directory already exists, and add `|| exit 1` after `cd` to stop the script on failure.
</Callout>

## Refactoring a Git Clone Example

Grouping related tasks into functions clarifies your script’s main flow.

| Script Version | Content                                                                                                                                                                        |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Ad-hoc         | `bash<br># Clone and count files<br>git clone "${1}"<br>find . -type f \| wc -l`                                                                                               |
| Refactored     | `bash<br>git_url="${1}"<br><br>clone_git() {<br>  git clone "${1}"<br>}<br><br>count_files() {<br>  find . -type f \| wc -l<br>}<br><br>clone_git "${git_url}"<br>count_files` |

By naming `clone_git` and `count_files`, you isolate logic and make testing easier.

## Function Declaration Syntax

Bash supports two portable styles. Use the first for maximum compatibility:

| Style                        | Syntax Example                                                               |
| ---------------------------- | ---------------------------------------------------------------------------- |
| Preferred (POSIX-compatible) | `bash<br>my_function() {<br>  echo "Hello from my_function"<br>}<br>`        |
| Using `function` keyword     | `bash<br>function my_function {<br>  echo "Hello from my_function"<br>}<br>` |

You can even define and call a function inline:

```bash theme={null}
$ hello() { echo "Hi there"; }
$ hello
Hi there
```

## Local Variables in Functions

Limit variable scope inside functions with `local` to avoid unintended side effects.

Example where `var1` is not visible outside:

```bash theme={null}
#!/bin/bash

my_function() {
    local var1="Hello"
}

my_function
echo "${var1}"  # No output
```

Example printing the local variable:

```bash theme={null}
#!/bin/bash

my_function() {
    local var1="Hello"
    echo "${var1}"
}

my_function  # Outputs: Hello
```

<Callout icon="lightbulb">
  Using `local` helps prevent variable collisions in larger scripts. For more details, see [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/).
</Callout>

## Benefits of Using Functions

* **Organization**: Break large scripts into logical units.
* **Reusability**: Call the same code multiple times without duplication.
* **Readability**: Name complex logic for better clarity.
* **Maintainability**: Update one function rather than many code blocks.

<Frame>
  ![The image lists the benefits of using functions in programming, including organization, code reuse, readability, shorter code, and manageability.](https://kodekloud.com/kk-media/image/upload/v1752868591/notes-assets/images/Advanced-Bash-Scripting-Functions/benefits-of-functions-in-programming.jpg)
</Frame>

## Links and References

* [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
* [LinuxCommand.org: Bash Functions](https://linuxcommand.org/lc3_writing_shell_scripts.php)
* [Stack Overflow: Bash Function Best Practices](https://stackoverflow.com/questions/9198033/defining-functions-in-bash)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/397a2175-a186-4a6d-916e-d688c8def203/lesson/9b870907-f664-4a9b-95d7-eb8d7d7b8389" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/397a2175-a186-4a6d-916e-d688c8def203/lesson/c50ba9ff-761a-4c43-b8e0-d7ea00aed7ae" />
</CardGroup>
