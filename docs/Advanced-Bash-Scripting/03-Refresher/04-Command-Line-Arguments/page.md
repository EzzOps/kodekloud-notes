# real 0m0.000s
```

Built-in `echo` completes instantly compared to the external `/usr/bin/echo`.

## Listing Built-ins and Keywords

* **List built-in commands:**
  ```bash theme={null}
  $ compgen -b
  ```
* **List shell keywords:**
  ```bash theme={null}
  $ compgen -k
  ```
* **Check if a word is a keyword:**
  ```bash theme={null}
  $ type time
  time is a shell keyword
  ```

> **triangle-alert** Keywords (like `time`, `if`, `for`) are parsed by the shell and do **not** spawn new processes. Confusing them with external binaries can lead to unexpected behavior.

For a comprehensive list of shell built-ins and keywords, see the Bash manual:

* [Bash BUILTIN Commands](https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html)
* [Shell Keywords](https://www.gnu.org/software/bash/manual/html_node/Shell-Grammar.html)

***

## References

* [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
* [Linux `strace` Documentation](https://strace.io/)
* [Bash Performance Tuning Tips](https://mywiki.wooledge.org/BashPitfalls)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/397a2175-a186-4a6d-916e-d688c8def203/lesson/a90e183a-7528-4b0b-862f-1ab175155a65)


# Command Line Arguments

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Refresher/Command-Line-Arguments/page

This guide covers command-line arguments in shell scripting, from basic parameters to advanced techniques for creating flexible scripts.

Command-line arguments are essential in shell scripting for creating flexible, reusable scripts. Instead of hard-coding values, you can accept inputs at runtime—much like using a remote control to switch channels on a TV. This guide covers everything from basic positional parameters to advanced iteration techniques.

## Table of Contents

* [Understanding Positional Parameters](#understanding-positional-parameters)
* [Practical Example: Cloning and Counting Files](#practical-example-cloning-and-counting-files)
* [Parameterizing Your Script](#parameterizing-your-script)
* [Common Special Variables](#common-special-variables)
* [Handling Maximum Argument Size (`ARG_MAX`)](#handling-maximum-argument-size-arg_max)
* [Iterating with `shift`](#iterating-with-shift)
* [References](#references)

***

## Understanding Positional Parameters

When you invoke a script with arguments:

```bash theme={null}
$ ./myscript.sh foo bar baz
```

Inside `myscript.sh`, the inputs map to:

```bash theme={null}
#!/bin/bash
echo "First argument: $1"
echo "Second argument: $2"
echo "Third argument: $3"
```

Output:

```bash theme={null}
First argument: foo
Second argument: bar
Third argument: baz
```

> **lightbulb** Always quote your positional parameters to handle spaces and special characters safely:

  ```bash theme={null}
  echo "User provided: $1"
  ```

***

## Practical Example: Cloning and Counting Files

Suppose you need to clone a Git repository and count its files. A hard-coded approach looks like this:

```bash theme={null}
#!/bin/bash

git clone git@github.com:kodedkloud/kodekloud-advanced-shell-scripting.git
find . -type f | wc -l
```

This works but requires editing the script for each repository URL.

***

## Parameterizing Your Script

By using `$1`, you can pass the repository URL when running the script:

```bash theme={null}
#!/bin/bash
