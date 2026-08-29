# Guard clause: expect exactly one argument
if [[ $# -ne 1 ]]; then
  terminate "Please provide exactly one argument (number of steps)" "$CL_ARGS_ERROR"
fi

steps=$1
calories=$(echo "$steps * $CAL_PER_STEP" | bc)
echo "Calories burned for $steps steps: $calories"
exit 0
```

#### Usage

```bash theme={null}
$ ./calorie.sh
Error: Please provide exactly one argument (number of steps)
$ echo $?
155

$ ./calorie.sh 10000
Calories burned for 10000 steps: 400.00
$ echo $?
0
```

***

## Summary of Key Variables

| Variable | Description                                        | Example                          |
| -------- | -------------------------------------------------- | -------------------------------- |
| `$?`     | Exit status of the last command                    | `echo $?`                        |
| `$#`     | Number of positional parameters passed to a script | `if [[ $# -ne 1 ]]; then ... fi` |
| `$1, $2` | Positional parameters (first, second, etc.)        | `echo "First: $1"`               |

***

## Links and References

* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
* [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
* [Shell Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/7ff1ccc1-5a14-41fc-817c-c0ec4a100231/lesson/6014e99a-9416-4048-aab7-11ed7b4a39b9)


# Overview

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Special-Shell-Variables/Overview/page

This article explains special shell variables in Bash for better script feedback and error handling.

Shell scripting thrives on feedback—knowing whether each step succeeded, failed, or requires special handling. Special shell variables provide this introspection by exposing the shell environment, command-line arguments, process identifiers, and more. Leveraging these built-in indicators leads to more robust, maintainable scripts.

![The image is a slide titled "Special Shell Variables," explaining that these variables allow access to information about the current shell environment and command-line arguments.](../../../../images/kodekloud.com/kk-media/image/upload/v1752868622/notes-assets/images/Advanced-Bash-Scripting-Overview/special-shell-variables-explanation.jpg)

## Understanding Exit Status in Bash

Every command you run returns an **exit status**:

* `0` means **success**
* Any nonzero value indicates **failure**

The special variable `$?` always holds the exit status of the last executed command:

```bash theme={null}
$ ls /nonexistent
ls: cannot access '/nonexistent': No such file or directory
$ echo $?
2
$ echo "Listing current directory:"
$ ls
KodeKloud_introduction
$ echo $?
0
```

> **lightbulb** Use `echo $?` immediately after a command to capture its exit status—subsequent commands will overwrite this value.

## Exploring Common Special Shell Variables

Here’s a quick reference for the most widely used POSIX-compliant special parameters:

| Variable | Description                                | Example                     |
| -------- | ------------------------------------------ | --------------------------- |
| `$*`     | All positional parameters as a single word | `echo "Args: $*"`           |
| `$#`     | Number of positional parameters            | `echo "Count: $#"`          |
| `$0`     | Name of the script or shell                | `echo "Script: $0"`         |
| `$!`     | PID of the last background command         | `sleep 30 &` then `echo $!` |
| `$-`     | Current shell options (flags) as a string  | `echo "Options: $-"`        |

Each of these variables updates dynamically based on the context in which your script runs.

> **triangle-alert** Expanding `$*` without quotes can lead to word splitting and unintended globbing. Use quotes or consider `$@` when preserving argument boundaries is critical.

## Practical Use Cases

1. **Argument Validation**
   ```bash theme={null}
   if [ $# -lt 2 ]; then
     echo "Usage: $0 <source> <destination>"
     exit 1
   fi
   ```
2. **Logging Script Name**
   ```bash theme={null}
   echo "[$(date)] Starting backup script: $0"
   ```
3. **Background Job Monitoring**
   ```bash theme={null}
   long_running_task &
   bg_pid=$!
   wait $bg_pid
   echo "Job $bg_pid finished with status $?"
   ```

## Links and References

* [GNU Bash Manual: Special Parameters](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html)
* [POSIX Shell Command Language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
* [Shell Scripting Best Practices](https://www.shellscript.sh/)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/7ff1ccc1-5a14-41fc-817c-c0ec4a100231/lesson/0f61e382-4963-4f0e-af0d-c924d3e663cd)
